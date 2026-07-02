from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.editorial_gates import PASSING_AUDIT_ENTITY_TYPES
from app.core.errors import NotFoundError
from app.models import AuditCheck
from app.schemas.audit_check import AuditCheckCreate


async def create_audit_check(
    session: AsyncSession, payload: AuditCheckCreate, correlation_id: str | None = None
) -> AuditCheck:
    check = AuditCheck(**payload.model_dump())
    if check.correlation_id is None:
        check.correlation_id = correlation_id
    session.add(check)
    await session.commit()
    await session.refresh(check)
    return check


async def list_audit_checks(
    session: AsyncSession,
    entity_type: str | None = None,
    entity_id: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[AuditCheck]:
    stmt = select(AuditCheck).order_by(AuditCheck.created_at.desc()).limit(limit).offset(offset)
    if entity_type is not None:
        stmt = stmt.where(AuditCheck.entity_type == entity_type)
    if entity_id is not None:
        stmt = stmt.where(AuditCheck.entity_id == entity_id)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_audit_check(session: AsyncSession, audit_check_id: str) -> AuditCheck:
    check = await session.get(AuditCheck, audit_check_id)
    if check is None:
        raise NotFoundError("Audit check")
    return check


async def get_latest_news_item_audit_check(
    session: AsyncSession,
    news_item_id: str,
) -> AuditCheck | None:
    stmt = (
        select(AuditCheck)
        .where(
            AuditCheck.entity_type.in_(PASSING_AUDIT_ENTITY_TYPES),
            AuditCheck.entity_id == news_item_id,
        )
        .order_by(AuditCheck.created_at.desc())
        .limit(1)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
