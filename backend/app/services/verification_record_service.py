from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.models import NewsItem, VerificationRecord
from app.schemas.verification_record import VerificationRecordCreate


async def create_verification_record(
    session: AsyncSession,
    payload: VerificationRecordCreate,
    correlation_id: str | None = None,
) -> VerificationRecord:
    if await session.get(NewsItem, payload.news_item_id) is None:
        raise NotFoundError("News item")

    record = VerificationRecord(**payload.model_dump())
    if record.correlation_id is None:
        record.correlation_id = correlation_id
    session.add(record)
    await session.commit()
    await session.refresh(record)
    return record


async def list_verification_records(
    session: AsyncSession,
    news_item_id: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[VerificationRecord]:
    stmt = select(VerificationRecord).order_by(VerificationRecord.created_at.desc())
    if news_item_id is not None:
        stmt = stmt.where(VerificationRecord.news_item_id == news_item_id)
    stmt = stmt.limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_verification_record(
    session: AsyncSession,
    verification_record_id: str,
) -> VerificationRecord:
    record = await session.get(VerificationRecord, verification_record_id)
    if record is None:
        raise NotFoundError("Verification record")
    return record
