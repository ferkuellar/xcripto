from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_api_key
from app.db.session import get_session
from app.schemas.distribution_plan import (
    DistributionPlanCreate,
    DistributionPlanRead,
    DistributionPlanStatusUpdate,
)
from app.services import distribution_plan_service

router = APIRouter(tags=["distribution-plans"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "/distribution-plans",
    response_model=DistributionPlanRead,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
async def create_distribution_plan(
    payload: DistributionPlanCreate,
    request: Request,
    session: SessionDep,
) -> DistributionPlanRead:
    plan = await distribution_plan_service.create_distribution_plan(
        session, payload, request.state.correlation_id
    )
    return DistributionPlanRead.model_validate(plan)


@router.get("/distribution-plans", response_model=list[DistributionPlanRead])
async def list_distribution_plans(
    session: SessionDep,
    content_piece_id: str | None = Query(default=None),
    news_item_id: str | None = Query(default=None),
    status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[DistributionPlanRead]:
    plans = await distribution_plan_service.list_distribution_plans(
        session,
        content_piece_id=content_piece_id,
        news_item_id=news_item_id,
        status=status,
        limit=limit,
        offset=offset,
    )
    return [DistributionPlanRead.model_validate(plan) for plan in plans]


@router.get(
    "/content-pieces/{content_piece_id}/distribution-plans",
    response_model=list[DistributionPlanRead],
)
async def list_content_piece_distribution_plans(
    content_piece_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[DistributionPlanRead]:
    plans = await distribution_plan_service.list_distribution_plans(
        session, content_piece_id=content_piece_id, limit=limit, offset=offset
    )
    return [DistributionPlanRead.model_validate(plan) for plan in plans]


@router.patch(
    "/distribution-plans/{distribution_plan_id}/status",
    response_model=DistributionPlanRead,
    dependencies=[Depends(require_api_key)],
)
async def update_distribution_plan_status(
    distribution_plan_id: str,
    payload: DistributionPlanStatusUpdate,
    session: SessionDep,
) -> DistributionPlanRead:
    plan = await distribution_plan_service.update_distribution_plan_status(
        session, distribution_plan_id, payload.status
    )
    return DistributionPlanRead.model_validate(plan)


@router.get("/distribution-plans/{distribution_plan_id}", response_model=DistributionPlanRead)
async def get_distribution_plan(
    distribution_plan_id: str,
    session: SessionDep,
) -> DistributionPlanRead:
    plan = await distribution_plan_service.get_distribution_plan(session, distribution_plan_id)
    return DistributionPlanRead.model_validate(plan)
