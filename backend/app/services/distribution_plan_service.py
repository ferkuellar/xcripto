from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ConflictError, DomainValidationError, NotFoundError
from app.models import ContentPiece, DistributionPlan
from app.schemas.distribution_plan import DistributionPlanCreate


async def create_distribution_plan(
    session: AsyncSession,
    payload: DistributionPlanCreate,
    correlation_id: str | None = None,
) -> DistributionPlan:
    content_piece = await session.get(ContentPiece, payload.content_piece_id)
    if content_piece is None:
        raise NotFoundError("Content piece")
    if content_piece.news_item_id != payload.news_item_id:
        raise DomainValidationError("news_item_id must match the ContentPiece news_item_id")
    if content_piece.status in {"blocked", "rejected"}:
        raise ConflictError(
            "DistributionPlan cannot be created for ContentPiece "
            f"with status {content_piece.status}"
        )

    plan = DistributionPlan(**payload.model_dump())
    if plan.correlation_id is None:
        plan.correlation_id = correlation_id
    session.add(plan)
    await session.commit()
    await session.refresh(plan)
    return plan


async def list_distribution_plans(
    session: AsyncSession,
    content_piece_id: str | None = None,
    news_item_id: str | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[DistributionPlan]:
    stmt = select(DistributionPlan).order_by(DistributionPlan.created_at.desc())
    if content_piece_id is not None:
        stmt = stmt.where(DistributionPlan.content_piece_id == content_piece_id)
    if news_item_id is not None:
        stmt = stmt.where(DistributionPlan.news_item_id == news_item_id)
    if status is not None:
        stmt = stmt.where(DistributionPlan.status == status)
    stmt = stmt.limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_distribution_plan(
    session: AsyncSession,
    distribution_plan_id: str,
) -> DistributionPlan:
    plan = await session.get(DistributionPlan, distribution_plan_id)
    if plan is None:
        raise NotFoundError("Distribution plan")
    return plan


async def update_distribution_plan_status(
    session: AsyncSession,
    distribution_plan_id: str,
    status: str,
) -> DistributionPlan:
    plan = await get_distribution_plan(session, distribution_plan_id)
    plan.status = status
    await session.commit()
    await session.refresh(plan)
    return plan
