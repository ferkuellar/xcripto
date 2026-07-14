from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import XCRIPTO_WEB_CHANNEL
from app.core.errors import ConflictError, DomainValidationError, NotFoundError
from app.models import ContentPiece, DistributionPlan, PublicationRecord
from app.schemas.publication_record import PublicationRecordCreate
from app.services.publication_dispatch_service import (
    BINANCE_SQUARE_CHANNEL_ALIASES,
    X_CHANNEL_ALIASES,
    dispatch_publication_record,
)


def _validate_published_reference(
    publication_status: str,
    channel: str,
    published_url: str | None,
    external_id: str | None,
) -> None:
    if publication_status == "published" and channel in (
        {"Telegram"}
        | {XCRIPTO_WEB_CHANNEL}
        | X_CHANNEL_ALIASES
        | BINANCE_SQUARE_CHANNEL_ALIASES
    ):
        return
    if publication_status == "published" and not (published_url or external_id):
        raise DomainValidationError(
            "PublicationRecord with published status requires published_url or external_id"
        )


async def create_publication_record(
    session: AsyncSession,
    payload: PublicationRecordCreate,
    correlation_id: str | None = None,
) -> PublicationRecord:
    content_piece = await session.get(ContentPiece, payload.content_piece_id)
    if content_piece is None:
        raise NotFoundError("Content piece")

    distribution_plan = await session.get(DistributionPlan, payload.distribution_plan_id)
    if distribution_plan is None:
        raise NotFoundError("Distribution plan")

    if content_piece.news_item_id != payload.news_item_id:
        raise DomainValidationError("news_item_id must match the ContentPiece news_item_id")
    if distribution_plan.content_piece_id != content_piece.id:
        raise DomainValidationError("distribution_plan_id must belong to the ContentPiece")
    if distribution_plan.news_item_id != payload.news_item_id:
        raise DomainValidationError("news_item_id must match the DistributionPlan news_item_id")
    if content_piece.status != "approved":
        raise ConflictError("PublicationRecord requires an approved ContentPiece")
    if distribution_plan.status not in {"scheduled", "ready_for_review"}:
        raise ConflictError(
            "PublicationRecord requires a DistributionPlan with status "
            "scheduled or ready_for_review"
        )

    _validate_published_reference(
        payload.publication_status,
        payload.channel,
        payload.published_url,
        payload.external_id,
    )

    record = PublicationRecord(**payload.model_dump())
    if record.correlation_id is None:
        record.correlation_id = correlation_id
    session.add(record)
    await session.commit()
    await session.refresh(record)
    await dispatch_publication_record(session, record.id)
    await session.refresh(record)
    return record


async def list_publication_records(
    session: AsyncSession,
    content_piece_id: str | None = None,
    news_item_id: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[PublicationRecord]:
    stmt = select(PublicationRecord).order_by(PublicationRecord.created_at.desc())
    if content_piece_id is not None:
        stmt = stmt.where(PublicationRecord.content_piece_id == content_piece_id)
    if news_item_id is not None:
        stmt = stmt.where(PublicationRecord.news_item_id == news_item_id)
    stmt = stmt.limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_publication_record(
    session: AsyncSession,
    publication_record_id: str,
) -> PublicationRecord:
    record = await session.get(PublicationRecord, publication_record_id)
    if record is None:
        raise NotFoundError("Publication record")
    return record


async def update_publication_record_status(
    session: AsyncSession,
    publication_record_id: str,
    publication_status: str,
) -> PublicationRecord:
    record = await get_publication_record(session, publication_record_id)
    _validate_published_reference(
        publication_status,
        record.channel,
        record.published_url,
        record.external_id,
    )
    record.publication_status = publication_status
    await session.commit()
    await session.refresh(record)
    await dispatch_publication_record(session, record.id)
    await session.refresh(record)
    return record
