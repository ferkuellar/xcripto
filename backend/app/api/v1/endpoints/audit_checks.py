from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_permission
from app.db.session import get_session
from app.schemas.audit_check import AuditCheckCreate, AuditCheckRead
from app.services import audit_check_service, operational_audit_service

router = APIRouter(prefix="/audit/checks", tags=["audit-checks"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "",
    response_model=AuditCheckRead,
    status_code=201,
    dependencies=[Depends(require_permission("audit.create"))],
)
async def create_audit_check(
    payload: AuditCheckCreate,
    request: Request,
    session: SessionDep,
) -> AuditCheckRead:
    check = await audit_check_service.create_audit_check(
        session, payload, request.state.correlation_id
    )
    response = AuditCheckRead.model_validate(check)
    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="audit_event",
        action="audit.create",
        permission="audit.create",
        decision="created",
        entity_type="AuditCheck",
        entity_id=check.id,
        news_item_id=check.entity_id if check.entity_type == "news_item" else None,
        metadata={
            "audit_status": check.audit_status,
            "entity_type": check.entity_type,
            "entity_id": check.entity_id,
            "ready_to_advance": check.ready_to_advance,
            "publication_block_recommended": check.publication_block_recommended,
        },
    )
    return response


@router.get("", response_model=list[AuditCheckRead])
async def list_audit_checks(
    session: SessionDep,
    entity_type: str | None = Query(default=None),
    entity_id: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[AuditCheckRead]:
    checks = await audit_check_service.list_audit_checks(
        session, entity_type=entity_type, entity_id=entity_id, limit=limit, offset=offset
    )
    return [AuditCheckRead.model_validate(check) for check in checks]


@router.get("/{audit_check_id}", response_model=AuditCheckRead)
async def get_audit_check(audit_check_id: str, session: SessionDep) -> AuditCheckRead:
    check = await audit_check_service.get_audit_check(session, audit_check_id)
    return AuditCheckRead.model_validate(check)
