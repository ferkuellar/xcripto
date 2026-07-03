from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ConflictError, DomainValidationError, NotFoundError
from app.models import IntakeAdapterRun, IntakeSignal, NewsItem, SourceReference
from app.schemas.intake import IntakeAdapterRunCreate, IntakeSignalCreate
from app.schemas.news import NewsCreate
from app.services import (
    intake_deduplication_service,
    intake_normalization_service,
    news_service,
    workflow_service,
)

NON_PROMOTABLE_SIGNAL_STATUSES = {"duplicate", "rejected", "archived", "error"}


async def create_intake_signal(
    session: AsyncSession,
    payload: IntakeSignalCreate,
    correlation_id: str | None = None,
) -> IntakeSignal:
    data = intake_normalization_service.normalize_signal_payload(payload.model_dump())
    data["signal_status"] = "dedupe_pending"
    signal = IntakeSignal(**data)
    if signal.correlation_id is None:
        signal.correlation_id = correlation_id
    await _validate_linked_news_item(session, signal.linked_news_item_id)
    session.add(signal)
    await session.flush()
    await intake_deduplication_service.apply_deduplication(session, signal)
    await session.commit()
    await session.refresh(signal)
    return signal


async def list_intake_signals(
    session: AsyncSession,
    signal_type: str | None = None,
    signal_status: str | None = None,
    dedupe_status: str | None = None,
    source_name: str | None = None,
    source_type: str | None = None,
    topic: str | None = None,
    priority: str | None = None,
    linked_news_item_id: str | None = None,
    promoted_news_item_id: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[IntakeSignal]:
    stmt = select(IntakeSignal).order_by(IntakeSignal.created_at.desc())
    filters = {
        "signal_type": signal_type,
        "signal_status": signal_status,
        "dedupe_status": dedupe_status,
        "source_name": source_name,
        "source_type": source_type,
        "topic": topic,
        "priority": priority,
        "linked_news_item_id": linked_news_item_id,
        "promoted_news_item_id": promoted_news_item_id,
    }
    for column_name, value in filters.items():
        if value is not None:
            stmt = stmt.where(getattr(IntakeSignal, column_name) == value)
    result = await session.execute(stmt.limit(limit).offset(offset))
    return list(result.scalars().all())


async def get_intake_signal(session: AsyncSession, signal_id: str) -> IntakeSignal:
    signal = await session.get(IntakeSignal, signal_id)
    if signal is None:
        raise NotFoundError("Intake signal")
    return signal


async def recalculate_signal_dedupe(session: AsyncSession, signal_id: str) -> IntakeSignal:
    signal = await get_intake_signal(session, signal_id)
    if signal.signal_status in {"promoted", "rejected", "archived"}:
        raise ConflictError(f"IntakeSignal with status {signal.signal_status} cannot be deduped")
    signal.signal_status = "dedupe_pending"
    signal.dedupe_status = "not_checked"
    signal.duplicate_of_signal_id = None
    signal.dedupe_score = None
    await intake_deduplication_service.apply_deduplication(session, signal)
    await session.commit()
    await session.refresh(signal)
    return signal


async def reject_intake_signal(
    session: AsyncSession,
    signal_id: str,
    reason: str,
) -> IntakeSignal:
    signal = await get_intake_signal(session, signal_id)
    if signal.signal_status == "promoted":
        raise ConflictError("Promoted IntakeSignal cannot be rejected")
    signal.signal_status = "rejected"
    signal.normalized_payload = {
        **(signal.normalized_payload or {}),
        "rejection_reason": reason,
    }
    await session.commit()
    await session.refresh(signal)
    return signal


async def archive_intake_signal(session: AsyncSession, signal_id: str) -> IntakeSignal:
    signal = await get_intake_signal(session, signal_id)
    if signal.signal_status == "promoted":
        raise ConflictError("Promoted IntakeSignal cannot be archived")
    signal.signal_status = "archived"
    await session.commit()
    await session.refresh(signal)
    return signal


async def promote_intake_signal(
    session: AsyncSession,
    signal_id: str,
    create_workflow: bool = False,
    workflow_type: str = "editorial_pipeline",
    correlation_id: str | None = None,
) -> IntakeSignal:
    signal = await get_intake_signal(session, signal_id)
    if signal.signal_status in NON_PROMOTABLE_SIGNAL_STATUSES:
        raise ConflictError(f"IntakeSignal with status {signal.signal_status} cannot be promoted")
    if signal.promoted_news_item_id is not None:
        raise ConflictError("IntakeSignal has already been promoted")
    if not signal.source_url or not signal.source_name:
        raise DomainValidationError("IntakeSignal requires source_url and source_name to promote")

    news = await news_service.create_news_item(
        session,
        NewsCreate(
            title=(signal.normalized_title or signal.raw_title or "Untitled signal")[:280],
            summary=signal.normalized_summary or signal.raw_summary or signal.raw_content or "",
            category=signal.topic or "general",
            priority=signal.priority,
            source_url=signal.url_canonical or signal.source_url,
            source_name=signal.source_name,
            status="detected",
        ),
        correlation_id=correlation_id or signal.correlation_id,
    )
    signal.promoted_news_item_id = news.id
    signal.linked_news_item_id = news.id
    signal.signal_status = "promoted"
    await _ensure_source_reference(session, signal, correlation_id or signal.correlation_id)
    await session.commit()
    await session.refresh(signal)

    if create_workflow:
        await workflow_service.create_workflow_run(
            session,
            news.id,
            workflow_type=workflow_type,
            correlation_id=correlation_id or signal.correlation_id,
        )
        await session.refresh(signal)

    return signal


async def create_adapter_run(
    session: AsyncSession,
    payload: IntakeAdapterRunCreate,
    correlation_id: str | None = None,
) -> IntakeAdapterRun:
    run = IntakeAdapterRun(**payload.model_dump())
    if run.correlation_id is None:
        run.correlation_id = correlation_id
    session.add(run)
    await session.commit()
    await session.refresh(run)
    return run


async def list_adapter_runs(
    session: AsyncSession,
    adapter_name: str | None = None,
    adapter_type: str | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[IntakeAdapterRun]:
    stmt = select(IntakeAdapterRun).order_by(IntakeAdapterRun.created_at.desc())
    if adapter_name is not None:
        stmt = stmt.where(IntakeAdapterRun.adapter_name == adapter_name)
    if adapter_type is not None:
        stmt = stmt.where(IntakeAdapterRun.adapter_type == adapter_type)
    if status is not None:
        stmt = stmt.where(IntakeAdapterRun.status == status)
    result = await session.execute(stmt.limit(limit).offset(offset))
    return list(result.scalars().all())


async def get_adapter_run(session: AsyncSession, adapter_run_id: str) -> IntakeAdapterRun:
    run = await session.get(IntakeAdapterRun, adapter_run_id)
    if run is None:
        raise NotFoundError("Intake adapter run")
    return run


async def _validate_linked_news_item(
    session: AsyncSession, linked_news_item_id: str | None
) -> None:
    if linked_news_item_id and await session.get(NewsItem, linked_news_item_id) is None:
        raise NotFoundError("Linked news item")


async def _ensure_source_reference(
    session: AsyncSession,
    signal: IntakeSignal,
    correlation_id: str | None,
) -> None:
    source_url = signal.url_canonical or signal.source_url
    if not source_url or not signal.source_name:
        return
    result = await session.execute(
        select(SourceReference)
        .where(SourceReference.source_url.in_({source_url, signal.source_url}))
        .limit(1)
    )
    if result.scalar_one_or_none() is not None:
        return
    session.add(
        SourceReference(
            source_name=signal.source_name,
            source_url=source_url,
            source_type=signal.source_type or "manual",
            source_status="proposed",
            trust_level="T2",
            notes=f"Created from IntakeSignal {signal.id}",
            correlation_id=correlation_id,
        )
    )
