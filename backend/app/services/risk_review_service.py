from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ConflictError, NotFoundError
from app.models import NewsItem, RiskReview
from app.schemas.risk_review import RiskReviewCreate


async def create_risk_review(
    session: AsyncSession,
    payload: RiskReviewCreate,
    correlation_id: str | None = None,
) -> RiskReview:
    if await session.get(NewsItem, payload.news_item_id) is None:
        raise NotFoundError("News item")

    existing = await _latest_for_entity(
        session,
        news_item_id=payload.news_item_id,
        entity_type=payload.entity_type,
        entity_id=payload.entity_id,
    )
    if existing is not None:
        await _recalculate_news_workflows(session, existing.news_item_id)
        return existing

    review = RiskReview(**payload.model_dump())
    if review.correlation_id is None:
        review.correlation_id = correlation_id
    session.add(review)
    await session.commit()
    await session.refresh(review)
    await _recalculate_news_workflows(session, review.news_item_id)
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


async def latest_risk_review_for_news(
    session: AsyncSession,
    news_item_id: str,
) -> RiskReview | None:
    result = await session.execute(
        select(RiskReview)
        .where(RiskReview.news_item_id == news_item_id)
        .order_by(RiskReview.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def require_risk_approval_for_publication(
    session: AsyncSession,
    news_item_id: str,
) -> RiskReview | None:
    review = await latest_risk_review_for_news(session, news_item_id)
    if review is None:
        raise ConflictError("Publication requires RiskReview before publishing")
    if review.human_review_required:
        raise ConflictError("Publication requires completed human risk decision")
    if review.publication_block_recommended:
        raise ConflictError("Publication blocked by RiskReview recommendation")
    if review.decision_recommendation in {"require_human_review", "block_publication", "reject"}:
        raise ConflictError(
            f"Publication blocked by RiskReview decision {review.decision_recommendation}"
        )
    if review.risk_level == "critical":
        raise ConflictError("Publication blocked by critical RiskReview")
    return review


async def _latest_for_entity(
    session: AsyncSession,
    *,
    news_item_id: str,
    entity_type: str,
    entity_id: str,
) -> RiskReview | None:
    result = await session.execute(
        select(RiskReview)
        .where(
            RiskReview.news_item_id == news_item_id,
            RiskReview.entity_type == entity_type,
            RiskReview.entity_id == entity_id,
        )
        .order_by(RiskReview.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def _recalculate_news_workflows(session: AsyncSession, news_item_id: str) -> None:
    from app.models import WorkflowRun
    from app.services import workflow_service

    result = await session.execute(
        select(WorkflowRun.id).where(WorkflowRun.news_item_id == news_item_id)
    )
    for workflow_run_id in result.scalars().all():
        await workflow_service.recalculate_workflow_run(session, workflow_run_id)
