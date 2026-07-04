from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ConflictError, DomainValidationError, NotFoundError
from app.models import ExternalConnector, ExternalConnectorRun
from app.schemas.external_connector import (
    AdminConnectorRunItem,
    AdminConnectorsSummary,
    ExternalConnectorContractValidation,
    ExternalConnectorCreate,
    ExternalConnectorDryRunRequest,
    ExternalConnectorUpdate,
    contains_secret_key,
)

AUTH_TYPES_REQUIRING_SECRET_REF = {
    "api_key_ref",
    "bearer_token_ref",
    "oauth_ref",
    "basic_ref",
    "signed_request_ref",
}


async def create_connector(
    session: AsyncSession,
    payload: ExternalConnectorCreate,
    correlation_id: str | None = None,
) -> ExternalConnector:
    _ensure_configuration_safe(payload.configuration)
    connector = ExternalConnector(**payload.model_dump())
    if connector.correlation_id is None:
        connector.correlation_id = correlation_id
    session.add(connector)
    await session.commit()
    await session.refresh(connector)
    return connector


async def list_connectors(
    session: AsyncSession,
    connector_type: str | None = None,
    connector_status: str | None = None,
    provider: str | None = None,
    enabled: bool | None = None,
    dry_run_only: bool | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[ExternalConnector]:
    stmt = select(ExternalConnector).order_by(ExternalConnector.created_at.desc())
    filters = {
        "connector_type": connector_type,
        "connector_status": connector_status,
        "provider": provider,
        "enabled": enabled,
        "dry_run_only": dry_run_only,
    }
    for column_name, value in filters.items():
        if value is not None:
            stmt = stmt.where(getattr(ExternalConnector, column_name) == value)
    result = await session.execute(stmt.limit(limit).offset(offset))
    return list(result.scalars().all())


async def get_connector(session: AsyncSession, connector_id: str) -> ExternalConnector:
    connector = await session.get(ExternalConnector, connector_id)
    if connector is None:
        raise NotFoundError("ExternalConnector")
    return connector


async def update_connector(
    session: AsyncSession,
    connector_id: str,
    payload: ExternalConnectorUpdate,
) -> ExternalConnector:
    connector = await get_connector(session, connector_id)
    data = payload.model_dump(exclude_unset=True)
    if "configuration" in data:
        _ensure_configuration_safe(data["configuration"])
    next_enabled = data.get("enabled", connector.enabled)
    next_dry_run_only = data.get("dry_run_only", connector.dry_run_only)
    if next_enabled and not next_dry_run_only:
        raise DomainValidationError("External connectors must remain dry_run_only in this phase")
    for field, value in data.items():
        setattr(connector, field, value)
    await session.commit()
    await session.refresh(connector)
    return connector


async def enable_connector(session: AsyncSession, connector_id: str) -> ExternalConnector:
    connector = await get_connector(session, connector_id)
    if not connector.dry_run_only:
        raise DomainValidationError("External connectors must remain dry_run_only in this phase")
    if connector.connector_status == "archived":
        raise ConflictError("Archived ExternalConnector cannot be enabled")
    connector.enabled = True
    connector.connector_status = "dry_run_only"
    await session.commit()
    await session.refresh(connector)
    return connector


async def disable_connector(session: AsyncSession, connector_id: str) -> ExternalConnector:
    connector = await get_connector(session, connector_id)
    connector.enabled = False
    connector.connector_status = "disabled"
    await session.commit()
    await session.refresh(connector)
    return connector


async def archive_connector(session: AsyncSession, connector_id: str) -> ExternalConnector:
    connector = await get_connector(session, connector_id)
    connector.enabled = False
    connector.connector_status = "archived"
    await session.commit()
    await session.refresh(connector)
    return connector


async def validate_connector_contract(
    session: AsyncSession,
    connector_id: str,
) -> ExternalConnectorContractValidation:
    connector = await get_connector(session, connector_id)
    warnings: list[str] = []
    errors: list[str] = []
    if contains_secret_key(connector.configuration):
        errors.append("Connector configuration must not contain secrets. Use secret_ref instead.")
    if connector.auth_type in AUTH_TYPES_REQUIRING_SECRET_REF and not connector.secret_ref:
        warnings.append("auth_type requires secret_ref before any future real integration.")
    if not connector.dry_run_only:
        errors.append("External connectors must remain dry_run_only in this phase.")
    if connector.enabled and connector.connector_status not in {
        "dry_run_only",
        "configured",
        "ready_for_review",
    }:
        warnings.append("enabled connector is not in an operational review status.")
    if not connector.capabilities:
        warnings.append("Connector has no declared capabilities.")
    return ExternalConnectorContractValidation(
        passed=not errors,
        warnings=warnings,
        errors=errors,
        connector_id=connector.id,
    )


async def dry_run_connector(
    session: AsyncSession,
    connector_id: str,
    payload: ExternalConnectorDryRunRequest,
    correlation_id: str | None = None,
) -> tuple[ExternalConnector, ExternalConnectorRun, ExternalConnectorContractValidation]:
    connector = await get_connector(session, connector_id)
    if connector.connector_status in {"archived", "disabled", "blocked"}:
        raise ConflictError(
            f"ExternalConnector with status {connector.connector_status} cannot run"
        )
    validation = await validate_connector_contract(session, connector_id)
    now = datetime.now(UTC)
    result_payload = _build_dry_run_result(connector, payload, validation)
    run_status = "completed" if validation.passed else "completed_with_warnings"
    run = ExternalConnectorRun(
        connector_id=connector.id,
        run_type=payload.run_type,
        run_status=run_status,
        triggered_by=payload.triggered_by,
        input_payload=payload.input_payload,
        result_payload=result_payload,
        signals_created_count=0,
        agent_outputs_created_count=0,
        publication_records_created_count=0,
        metric_snapshots_created_count=0,
        started_at=now,
        completed_at=now,
        correlation_id=correlation_id,
    )
    connector.last_run_at = now
    if validation.passed:
        connector.last_success_at = now
    else:
        connector.last_failure_at = now
    session.add(run)
    await session.commit()
    await session.refresh(connector)
    await session.refresh(run)
    return connector, run, validation


async def list_connector_runs(
    session: AsyncSession,
    connector_id: str,
    run_type: str | None = None,
    run_status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[ExternalConnectorRun]:
    await get_connector(session, connector_id)
    stmt = (
        select(ExternalConnectorRun)
        .where(ExternalConnectorRun.connector_id == connector_id)
        .order_by(ExternalConnectorRun.created_at.desc())
    )
    if run_type is not None:
        stmt = stmt.where(ExternalConnectorRun.run_type == run_type)
    if run_status is not None:
        stmt = stmt.where(ExternalConnectorRun.run_status == run_status)
    result = await session.execute(stmt.limit(limit).offset(offset))
    return list(result.scalars().all())


async def get_connector_run(session: AsyncSession, run_id: str) -> ExternalConnectorRun:
    run = await session.get(ExternalConnectorRun, run_id)
    if run is None:
        raise NotFoundError("ExternalConnectorRun")
    return run


async def get_admin_connectors_summary(session: AsyncSession) -> AdminConnectorsSummary:
    total = await _count(session, ExternalConnector)
    enabled = await _count_where(session, ExternalConnector.enabled.is_(True))
    dry_run_only = await _count_where(session, ExternalConnector.dry_run_only.is_(True))
    by_type = await _group_counts(session, ExternalConnector.connector_type)
    by_status = await _group_counts(session, ExternalConnector.connector_status)
    failed_runs = await _count_where(
        session,
        ExternalConnectorRun.run_status.in_({"failed", "blocked"}),
        model=ExternalConnectorRun,
    )
    result = await session.execute(
        select(ExternalConnectorRun).order_by(ExternalConnectorRun.created_at.desc()).limit(10)
    )
    recent_runs = [
        AdminConnectorRunItem(
            id=run.id,
            connector_id=run.connector_id,
            run_type=run.run_type,
            run_status=run.run_status,
            created_at=run.created_at,
            completed_at=run.completed_at,
        )
        for run in result.scalars().all()
    ]
    return AdminConnectorsSummary(
        total_connectors=total,
        enabled_connectors=enabled,
        dry_run_only_connectors=dry_run_only,
        connectors_by_type=by_type,
        connectors_by_status=by_status,
        recent_connector_runs=recent_runs,
        failed_connector_runs=failed_runs,
    )


def _ensure_configuration_safe(configuration: dict | list | None) -> None:
    if contains_secret_key(configuration):
        raise DomainValidationError(
            "Connector configuration must not contain secrets. Use secret_ref instead."
        )


def _build_dry_run_result(
    connector: ExternalConnector,
    payload: ExternalConnectorDryRunRequest,
    validation: ExternalConnectorContractValidation,
) -> dict[str, Any]:
    target_entities = _target_entities_for_capabilities(connector.capabilities)
    return {
        "connector_id": connector.id,
        "connector_name": connector.connector_name,
        "connector_type": connector.connector_type,
        "provider": connector.provider,
        "run_type": payload.run_type,
        "dry_run_only": connector.dry_run_only,
        "external_calls_performed": False,
        "would_create": target_entities,
        "warnings": validation.warnings,
        "errors": validation.errors,
        "message": (
            "Dry-run completed locally. No external API, scraping, LLM, "
            "or publishing call was made."
        ),
    }


def _target_entities_for_capabilities(capabilities: list[str]) -> list[str]:
    targets: list[str] = []
    if "ingest_signals" in capabilities or "receive_webhook" in capabilities:
        targets.append("IntakeSignal")
    if "generate_agent_output" in capabilities or "validate_sources" in capabilities:
        targets.append("AgentOutput")
    if "publish_content" in capabilities or "schedule_content" in capabilities:
        targets.append("PublicationRecord")
    if "fetch_metrics" in capabilities:
        targets.append("MetricSnapshot")
    return targets


async def _count(session: AsyncSession, model) -> int:
    result = await session.execute(select(func.count()).select_from(model))
    return int(result.scalar_one())


async def _count_where(session: AsyncSession, criterion, model=ExternalConnector) -> int:
    result = await session.execute(select(func.count()).select_from(model).where(criterion))
    return int(result.scalar_one())


async def _group_counts(session: AsyncSession, column) -> dict[str, int]:
    result = await session.execute(select(column, func.count()).group_by(column))
    return {str(key): int(count) for key, count in result.all()}
