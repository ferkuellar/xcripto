from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.editorial_gates import is_passing_audit_check, requires_passing_audit_check
from app.core.errors import ConflictError, DomainValidationError, NotFoundError
from app.core.state_machine import is_valid_news_status_transition
from app.models import NewsItem
from app.schemas.news import NewsCreate
from app.services.audit_check_service import get_latest_news_item_audit_check


async def create_news_item(
    session: AsyncSession, payload: NewsCreate, correlation_id: str | None = None
) -> NewsItem:
    item = NewsItem(**payload.model_dump())
    if item.correlation_id is None:
        item.correlation_id = correlation_id
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def list_news_items(
    session: AsyncSession,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[NewsItem]:
    stmt = select(NewsItem).order_by(NewsItem.created_at.desc()).limit(limit).offset(offset)
    if status is not None:
        stmt = stmt.where(NewsItem.status == status)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_news_item(session: AsyncSession, news_id: str) -> NewsItem:
    item = await session.get(NewsItem, news_id)
    if item is None:
        raise NotFoundError("News item")
    return item


async def update_news_status(session: AsyncSession, news_id: str, status: str) -> NewsItem:
    item = await get_news_item(session, news_id)
    if not is_valid_news_status_transition(item.status, status):
        raise DomainValidationError(f"Invalid status transition from {item.status} to {status}")

    if requires_passing_audit_check(status):
        latest_audit_check = await get_latest_news_item_audit_check(session, item.id)
        if not is_passing_audit_check(latest_audit_check):
            raise ConflictError(
                f"NewsItem cannot transition to {status} without a passing AuditCheck"
            )

    item.status = status
    await session.commit()
    await session.refresh(item)
    return item
