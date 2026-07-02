from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.audit_check import AuditCheckCreate, AuditCheckRead
from app.services import audit_check_service

router = APIRouter(prefix="/audit/checks", tags=["audit-checks"])


@router.post("", response_model=AuditCheckRead, status_code=201)
async def create_audit_check(
    payload: AuditCheckCreate,
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> AuditCheckRead:
    check = await audit_check_service.create_audit_check(
        session, payload, request.state.correlation_id
    )
    return AuditCheckRead.model_validate(check)


@router.get("", response_model=list[AuditCheckRead])
async def list_audit_checks(
    entity_type: str | None = Query(default=None),
    entity_id: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
) -> list[AuditCheckRead]:
    checks = await audit_check_service.list_audit_checks(
        session, entity_type=entity_type, entity_id=entity_id, limit=limit, offset=offset
    )
    return [AuditCheckRead.model_validate(check) for check in checks]


@router.get("/{audit_check_id}", response_model=AuditCheckRead)
async def get_audit_check(
    audit_check_id: str, session: AsyncSession = Depends(get_session)
) -> AuditCheckRead:
    check = await audit_check_service.get_audit_check(session, audit_check_id)
    return AuditCheckRead.model_validate(check)
