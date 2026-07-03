from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_permission
from app.db.session import get_session
from app.schemas.external_connector import (
    ExternalConnectorContractValidation,
    ExternalConnectorCreate,
    ExternalConnectorDryRunRequest,
    ExternalConnectorDryRunResponse,
    ExternalConnectorRead,
    ExternalConnectorRunRead,
    ExternalConnectorUpdate,
)
from app.services import external_connector_service, operational_audit_service

router = APIRouter(prefix="/connectors", tags=["connectors"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "",
    response_model=ExternalConnectorRead,
    status_code=201,
    dependencies=[Depends(require_permission("connector.create"))],
)
async def create_connector(
    payload: ExternalConnectorCreate,
    request: Request,
    session: SessionDep,
) -> ExternalConnectorRead:
    connector = await external_connector_service.create_connector(
        session, payload, request.state.correlation_id
    )
    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="system_event",
        action="connector.create",
        permission="connector.create",
        decision="created",
        entity_type="ExternalConnector",
        entity_id=connector.id,
        metadata=_audit_metadata(connector),
    )
    return ExternalConnectorRead.model_validate(connector)


@router.get(
    "",
    response_model=list[ExternalConnectorRead],
    dependencies=[Depends(require_permission("connector.read"))],
)
async def list_connectors(
    session: SessionDep,
    connector_type: str | None = Query(default=None),
    connector_status: str | None = Query(default=None),
    provider: str | None = Query(default=None),
    enabled: bool | None = Query(default=None),
    dry_run_only: bool | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[ExternalConnectorRead]:
    connectors = await external_connector_service.list_connectors(
        session,
        connector_type=connector_type,
        connector_status=connector_status,
        provider=provider,
        enabled=enabled,
        dry_run_only=dry_run_only,
        limit=limit,
        offset=offset,
    )
    return [ExternalConnectorRead.model_validate(connector) for connector in connectors]


@router.get(
    "/runs/{run_id}",
    response_model=ExternalConnectorRunRead,
    dependencies=[Depends(require_permission("connector.read"))],
)
async def get_connector_run(run_id: str, session: SessionDep) -> ExternalConnectorRunRead:
    run = await external_connector_service.get_connector_run(session, run_id)
    return ExternalConnectorRunRead.model_validate(run)


@router.get(
    "/{connector_id}",
    response_model=ExternalConnectorRead,
    dependencies=[Depends(require_permission("connector.read"))],
)
async def get_connector(connector_id: str, session: SessionDep) -> ExternalConnectorRead:
    connector = await external_connector_service.get_connector(session, connector_id)
    return ExternalConnectorRead.model_validate(connector)


@router.patch(
    "/{connector_id}",
    response_model=ExternalConnectorRead,
    dependencies=[Depends(require_permission("connector.update"))],
)
async def update_connector(
    connector_id: str,
    payload: ExternalConnectorUpdate,
    request: Request,
    session: SessionDep,
) -> ExternalConnectorRead:
    connector = await external_connector_service.update_connector(session, connector_id, payload)
    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="system_event",
        action="connector.update",
        permission="connector.update",
        decision="updated",
        entity_type="ExternalConnector",
        entity_id=connector.id,
        metadata=_audit_metadata(connector),
    )
    return ExternalConnectorRead.model_validate(connector)


@router.patch(
    "/{connector_id}/enable",
    response_model=ExternalConnectorRead,
    dependencies=[Depends(require_permission("connector.update"))],
)
async def enable_connector(
    connector_id: str,
    request: Request,
    session: SessionDep,
) -> ExternalConnectorRead:
    connector = await external_connector_service.enable_connector(session, connector_id)
    await _record_connector_event(
        session,
        request,
        connector,
        action="connector.enable",
        permission="connector.update",
        decision="updated",
    )
    return ExternalConnectorRead.model_validate(connector)


@router.patch(
    "/{connector_id}/disable",
    response_model=ExternalConnectorRead,
    dependencies=[Depends(require_permission("connector.update"))],
)
async def disable_connector(
    connector_id: str,
    request: Request,
    session: SessionDep,
) -> ExternalConnectorRead:
    connector = await external_connector_service.disable_connector(session, connector_id)
    await _record_connector_event(
        session,
        request,
        connector,
        action="connector.disable",
        permission="connector.update",
        decision="updated",
    )
    return ExternalConnectorRead.model_validate(connector)


@router.patch(
    "/{connector_id}/archive",
    response_model=ExternalConnectorRead,
    dependencies=[Depends(require_permission("connector.archive"))],
)
async def archive_connector(
    connector_id: str,
    request: Request,
    session: SessionDep,
) -> ExternalConnectorRead:
    connector = await external_connector_service.archive_connector(session, connector_id)
    await _record_connector_event(
        session,
        request,
        connector,
        action="connector.archive",
        permission="connector.archive",
        decision="archived",
    )
    return ExternalConnectorRead.model_validate(connector)


@router.post(
    "/{connector_id}/validate",
    response_model=ExternalConnectorContractValidation,
    dependencies=[Depends(require_permission("connector.run"))],
)
async def validate_connector(
    connector_id: str,
    request: Request,
    session: SessionDep,
) -> ExternalConnectorContractValidation:
    validation = await external_connector_service.validate_connector_contract(
        session, connector_id
    )
    connector = await external_connector_service.get_connector(session, connector_id)
    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="system_event",
        action="connector.validate",
        permission="connector.run",
        outcome="succeeded" if validation.passed else "blocked",
        decision="no_op",
        entity_type="ExternalConnector",
        entity_id=connector.id,
        metadata={
            **_audit_metadata(connector),
            "warnings": validation.warnings,
            "errors": validation.errors,
        },
    )
    return validation


@router.post(
    "/{connector_id}/dry-run",
    response_model=ExternalConnectorDryRunResponse,
    dependencies=[Depends(require_permission("connector.run"))],
)
async def dry_run_connector(
    connector_id: str,
    payload: ExternalConnectorDryRunRequest,
    request: Request,
    session: SessionDep,
) -> ExternalConnectorDryRunResponse:
    connector, run, validation = await external_connector_service.dry_run_connector(
        session,
        connector_id,
        payload,
        request.state.correlation_id,
    )
    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="system_event",
        action="connector.dry_run",
        permission="connector.run",
        outcome="succeeded" if validation.passed else "blocked",
        decision="no_op",
        entity_type="ExternalConnector",
        entity_id=connector.id,
        metadata={
            **_audit_metadata(connector),
            "run_id": run.id,
            "run_type": run.run_type,
            "run_status": run.run_status,
        },
    )
    return ExternalConnectorDryRunResponse(
        connector=ExternalConnectorRead.model_validate(connector),
        run=ExternalConnectorRunRead.model_validate(run),
        validation=validation,
    )


@router.get(
    "/{connector_id}/runs",
    response_model=list[ExternalConnectorRunRead],
    dependencies=[Depends(require_permission("connector.read"))],
)
async def list_connector_runs(
    connector_id: str,
    session: SessionDep,
    run_type: str | None = Query(default=None),
    run_status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[ExternalConnectorRunRead]:
    runs = await external_connector_service.list_connector_runs(
        session,
        connector_id,
        run_type=run_type,
        run_status=run_status,
        limit=limit,
        offset=offset,
    )
    return [ExternalConnectorRunRead.model_validate(run) for run in runs]


def _audit_metadata(connector) -> dict:
    return {
        "connector_type": connector.connector_type,
        "provider": connector.provider,
        "dry_run_only": connector.dry_run_only,
        "enabled": connector.enabled,
    }


async def _record_connector_event(
    session: AsyncSession,
    request: Request,
    connector,
    *,
    action: str,
    permission: str,
    decision: str,
) -> None:
    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="system_event",
        action=action,
        permission=permission,
        decision=decision,
        entity_type="ExternalConnector",
        entity_id=connector.id,
        metadata=_audit_metadata(connector),
    )
