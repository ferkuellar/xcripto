from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.models import NewsItem, RiskReview
from app.schemas.risk_review import RiskReviewCreate


async def create_risk_review(
    session: AsyncSession,
    payload: RiskReviewCreate,
    correlation_id: str | None = None,
) -> RiskReview:
    if await session.get(NewsItem, payload.news_item_id) is None:
        raise NotFoundError("News item")

    review = RiskReview(**payload.model_dump())
    if review.correlation_id is None:
        review.correlation_id = correlation_id
    session.add(review)
    await session.commit()
    await session.refresh(review)
    return review


async def list_risk_reviews(
    session: AsyncSession,
    news_item_id: str | None = None,
    entity_type: str | None = None,
    entity_id: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[RiskReview]:
    stmt = select(RiskReview).order_by(RiskReview.created_at.desc())
    if news_item_id is not None:
        stmt = stmt.where(RiskReview.news_item_id == news_item_id)
    if entity_type is not None:
        stmt = stmt.where(RiskReview.entity_type == entity_type)
    if entity_id is not None:
        stmt = stmt.where(RiskReview.entity_id == entity_id)
    stmt = stmt.limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_risk_review(session: AsyncSession, risk_review_id: str) -> RiskReview:
    review = await session.get(RiskReview, risk_review_id)
    if review is None:
        raise NotFoundError("Risk review")
    return review
