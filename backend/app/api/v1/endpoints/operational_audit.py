from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_permission
from app.db.session import get_session
from app.schemas.operational_audit import OperationalAuditLogCreate, OperationalAuditLogRead
from app.services import operational_audit_service

router = APIRouter(prefix="/operational-audit", tags=["operational-audit"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get(
    "/events",
    response_model=list[OperationalAuditLogRead],
    dependencies=[Depends(require_permission("operational_audit.read"))],
)
async def list_audit_events(
    session: SessionDep,
    event_type: str | None = Query(default=None),
    action: str | None = Query(default=None),
    permission: str | None = Query(default=None),
    actor_id: str | None = Query(default=None),
    actor_role: str | None = Query(default=None),
    entity_type: str | None = Query(default=None),
    entity_id: str | None = Query(default=None),
    news_item_id: str | None = Query(default=None),
    workflow_run_id: str | None = Query(default=None),
    workflow_task_id: str | None = Query(default=None),
    agent_output_id: str | None = Query(default=None),
    outcome: str | None = Query(default=None),
    decision: str | None = Query(default=None),
    correlation_id: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[OperationalAuditLogRead]:
    events = await operational_audit_service.list_audit_events(
        session,
        event_type=event_type,
        action=action,
        permission=permission,
        actor_id=actor_id,
        actor_role=actor_role,
        entity_type=entity_type,
        entity_id=entity_id,
        news_item_id=news_item_id,
        workflow_run_id=workflow_run_id,
        workflow_task_id=workflow_task_id,
        agent_output_id=agent_output_id,
        outcome=outcome,
        decision=decision,
        correlation_id=correlation_id,
        limit=limit,
        offset=offset,
    )
    return [OperationalAuditLogRead.model_validate(event) for event in events]


@router.post(
    "/events",
    response_model=OperationalAuditLogRead,
    status_code=201,
    dependencies=[Depends(require_permission("operational_audit.create"))],
)
async def create_audit_event(
    payload: OperationalAuditLogCreate,
    request: Request,
    session: SessionDep,
) -> OperationalAuditLogRead:
    event = await operational_audit_service.create_audit_event(
        session, payload, request.state.correlation_id
    )
    return OperationalAuditLogRead.model_validate(event)


@router.get(
    "/events/{event_id}",
    response_model=OperationalAuditLogRead,
    dependencies=[Depends(require_permission("operational_audit.read"))],
)
async def get_audit_event(event_id: str, session: SessionDep) -> OperationalAuditLogRead:
    event = await operational_audit_service.get_audit_event(session, event_id)
    return OperationalAuditLogRead.model_validate(event)


@router.get(
    "/correlation/{correlation_id}",
    response_model=list[OperationalAuditLogRead],
    dependencies=[Depends(require_permission("operational_audit.read"))],
)
async def get_audit_events_by_correlation_id(
    correlation_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[OperationalAuditLogRead]:
    events = await operational_audit_service.get_audit_events_by_correlation_id(
        session, correlation_id, limit=limit, offset=offset
    )
    return [OperationalAuditLogRead.model_validate(event) for event in events]


@router.get(
    "/actors/{actor_id}",
    response_model=list[OperationalAuditLogRead],
    dependencies=[Depends(require_permission("operational_audit.read"))],
)
async def get_audit_events_by_actor(
    actor_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[OperationalAuditLogRead]:
    events = await operational_audit_service.get_audit_events_by_actor(
        session, actor_id, limit=limit, offset=offset
    )
    return [OperationalAuditLogRead.model_validate(event) for event in events]


@router.get(
    "/entity/{entity_type}/{entity_id}",
    response_model=list[OperationalAuditLogRead],
    dependencies=[Depends(require_permission("operational_audit.read"))],
)
async def get_audit_events_by_entity(
    entity_type: str,
    entity_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[OperationalAuditLogRead]:
    events = await operational_audit_service.get_audit_events_by_entity(
        session, entity_type, entity_id, limit=limit, offset=offset
    )
    return [OperationalAuditLogRead.model_validate(event) for event in events]
