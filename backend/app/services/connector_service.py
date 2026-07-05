"""Controlled connector rollout service (P9).

Runs a real RSS connector in-process: fetch -> parse -> allowed-domain filter ->
IntakeSignal (with dedup) -> SourceReference (quality from the registry) -> audit.
Disabled by default; honours kill switches and per-run limits. Never promotes or
publishes (CONNECTOR_AUTO_PROMOTE must stay false in P9).
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.connectors import rss_connector
from app.connectors.base import ConnectorRunResult, NormalizedItem, fetch_url
from app.core import source_registry
from app.core.config import get_settings
from app.models import IntakeAdapterRun, SourceReference
from app.schemas.intake import IntakeAdapterRunCreate, IntakeSignalCreate
from app.schemas.operational_audit import OperationalAuditLogCreate
from app.services import intake_service, operational_audit_service

FetchFn = Callable[[str], bytes]


async def _audit(
    session: AsyncSession,
    *,
    action: str,
    decision: str,
    outcome: str,
    correlation_id: str | None,
    actor_role: str,
    metadata: dict[str, Any],
    reason: str | None = None,
) -> None:
    if not get_settings().connector_audit_enabled:
        return
    await operational_audit_service.create_audit_event(
        session,
        OperationalAuditLogCreate(
            event_type="connector_event",
            action=action,
            actor_role=actor_role,
            actor_source="system",
            outcome=outcome,
            decision=decision,
            reason=reason,
            metadata=metadata,
            correlation_id=correlation_id,
        ),
        correlation_id,
    )


async def _ensure_source_reference(
    session: AsyncSession,
    *,
    source_url: str,
    source_name: str,
    trust_level: str,
    correlation_id: str | None,
) -> None:
    canonical_url = _canonical_source_url(source_url)
    existing = await session.execute(
        select(SourceReference)
        .where(
            SourceReference.source_type == "rss_feed",
            SourceReference.source_url == canonical_url,
        )
        .limit(1)
    )
    if existing.scalar_one_or_none() is not None:
        return
    session.add(
        SourceReference(
            source_name=source_name,
            source_url=canonical_url,
            source_type="rss_feed",
            source_status="active",
            trust_level=trust_level,
            notes="Registered by RSS connector rollout (P9).",
            correlation_id=correlation_id,
        )
    )
    await session.commit()


def _signal_payload(
    item: NormalizedItem,
    provider: source_registry.FeedProviderEntry,
) -> IntakeSignalCreate:
    return IntakeSignalCreate(
        signal_type="rss",
        source_name=provider.source_name,
        source_url=item.url,
        source_type="rss_feed",
        source_published_at=item.published_at,
        raw_title=item.title,
        raw_summary=item.summary or item.title,
        topic="crypto",
        priority="P3",
        confidence_level="IC1",
        adapter_name="rss_connector",
        adapter_version="0.1",
        raw_payload={
            "external_id": item.external_id,
            "feed_provider": provider.provider_key,
            "source_domain": item.source_domain,
            "raw_payload_hash": item.raw_payload_hash,
        },
    )


async def run_rss_connector(
    session: AsyncSession,
    feed_url: str,
    *,
    fetch: FetchFn | None = None,
    max_items: int | None = None,
    correlation_id: str | None = None,
    actor_role: str = "system",
) -> ConnectorRunResult:
    settings = get_settings()
    result = ConnectorRunResult(connector_name="rss")

    # --- Kill switches ---
    if not settings.connectors_enabled or not settings.rss_connector_enabled:
        result.disabled = True
        result.reason = "connectors disabled"
        return result

    limit = settings.rss_connector_max_items if max_items is None else max_items
    limit = max(0, min(limit, settings.rss_connector_max_items))
    allowed = set(settings.rss_allowed_domains)
    try:
        provider = source_registry.provider_for_feed_url(feed_url, allowed)
    except ValueError as exc:
        result.errors.append(str(exc))
        return result

    run = await intake_service.create_adapter_run(
        session,
        IntakeAdapterRunCreate(
            adapter_name="rss_connector",
            adapter_version="0.1",
            adapter_type="rss",
            status="running",
            input_payload={"feed_url": feed_url, "max_items": limit},
            started_at=datetime.now(UTC),
        ),
        correlation_id,
    )
    result.adapter_run_id = run.id
    await _audit(
        session, action="connector.run.started", decision="started", outcome="succeeded",
        correlation_id=correlation_id, actor_role=actor_role,
        metadata={"connector_name": "rss", "feed_url": feed_url, "max_items": limit},
    )

    # --- Fetch + parse (fail-soft) ---
    try:
        raw = (fetch or _default_fetch(settings, provider))(feed_url)
        items = rss_connector.parse_feed(raw)
    except Exception as exc:  # noqa: BLE001 — connector must not crash the caller
        result.errors.append(f"fetch/parse: {exc}")
        await _finish_run(session, run, result, status="failed", error=str(exc))
        await _audit(
            session, action="connector.item.error", decision="error", outcome="failed",
            correlation_id=correlation_id, actor_role=actor_role,
            metadata={"connector_name": "rss", "feed_url": feed_url}, reason=str(exc),
        )
        return result

    result.fetched_count = len(items)

    for item in items[:limit]:
        try:
            await _ingest_item(session, item, provider, result, correlation_id, actor_role)
        except Exception as exc:  # noqa: BLE001
            result.rejected_count += 1
            result.errors.append(f"{item.url}: {exc}")
            await _audit(
                session, action="connector.item.error", decision="error", outcome="failed",
                correlation_id=correlation_id, actor_role=actor_role,
                metadata={"connector_name": "rss", "url": item.url}, reason=str(exc),
            )

    status = "completed_with_warnings" if result.errors else "completed"
    await _finish_run(session, run, result, status=status)
    await _audit(
        session, action="connector.run.completed", decision="completed", outcome="succeeded",
        correlation_id=correlation_id, actor_role=actor_role, metadata=result.as_dict(),
    )
    return result


async def _ingest_item(
    session: AsyncSession,
    item: NormalizedItem,
    provider: source_registry.FeedProviderEntry,
    result: ConnectorRunResult,
    correlation_id: str | None,
    actor_role: str,
) -> None:
    if not source_registry.provider_allows_item(provider, item.url):
        result.rejected_count += 1
        await _audit(
            session, action="connector.item.rejected", decision="rejected", outcome="blocked",
            correlation_id=correlation_id, actor_role=actor_role,
            metadata={
                "connector_name": "rss", "url": item.url, "source_domain": item.source_domain,
                "feed_provider": provider.provider_key,
            },
            reason="item link is not allowed for feed provider",
        )
        return

    signal = await intake_service.create_intake_signal(
        session, _signal_payload(item, provider), correlation_id
    )
    settings = get_settings()
    if settings.connector_require_source_reference:
        await _ensure_source_reference(
            session,
            source_url=f"https://{provider.canonical_domain}",
            source_name=provider.source_name,
            trust_level=provider.trust_level,
            correlation_id=correlation_id,
        )

    if signal.dedupe_status in {"exact_duplicate", "probable_duplicate"}:
        result.duplicate_count += 1
        await _audit(
            session, action="connector.item.duplicate", decision="no_op", outcome="skipped",
            correlation_id=correlation_id, actor_role=actor_role,
            metadata={
                "connector_name": "rss",
                "url": item.url,
                "signal_id": signal.id,
                "dedupe_status": signal.dedupe_status,
            },
        )
        return

    result.accepted_count += 1
    await _audit(
        session, action="connector.item.ingested", decision="created", outcome="succeeded",
        correlation_id=correlation_id, actor_role=actor_role,
        metadata={
            "connector_name": "rss",
            "url": item.url,
            "signal_id": signal.id,
            "feed_provider": provider.provider_key,
            "source_domain": item.source_domain,
            "trust_level": provider.trust_level,
        },
    )


async def _finish_run(
    session: AsyncSession,
    run: IntakeAdapterRun,
    result: ConnectorRunResult,
    *,
    status: str,
    error: str | None = None,
) -> None:
    run.status = status
    run.signals_created_count = result.accepted_count
    run.signals_duplicate_count = result.duplicate_count
    run.signals_error_count = result.rejected_count
    run.result_payload = result.as_dict()
    run.completed_at = datetime.now(UTC)
    if error:
        run.error_message = error
    await session.commit()


def _default_fetch(settings, provider: source_registry.FeedProviderEntry) -> FetchFn:
    return lambda url: fetch_url(
        url,
        timeout=settings.rss_connector_timeout_seconds,
        user_agent=settings.rss_connector_user_agent,
        allowed_domains=set(provider.feed_domains),
    )


def _canonical_source_url(source_url: str) -> str:
    parsed = urlsplit(source_url)
    scheme = parsed.scheme.lower() or "https"
    host = (parsed.hostname or "").lower().rstrip(".")
    netloc = host[4:] if host.startswith("www.") else host
    path = parsed.path.rstrip("/")
    return urlunsplit((scheme, netloc, path, "", ""))
