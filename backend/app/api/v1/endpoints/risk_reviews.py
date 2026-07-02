from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_api_key
from app.db.session import get_session
from app.schemas.risk_review import RiskReviewCreate, RiskReviewRead
from app.services import risk_review_service

router = APIRouter(tags=["risk-reviews"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "/risk-reviews",
    response_model=RiskReviewRead,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
async def create_risk_review(
    payload: RiskReviewCreate,
    request: Request,
    session: SessionDep,
) -> RiskReviewRead:
    review = await risk_review_service.create_risk_review(
        session, payload, request.state.correlation_id
    )
    return RiskReviewRead.model_validate(review)


@router.get("/risk-reviews", response_model=list[RiskReviewRead])
async def list_risk_reviews(
    session: SessionDep,
    news_item_id: str | None = Query(default=None),
    entity_type: str | None = Query(default=None),
    entity_id: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[RiskReviewRead]:
    reviews = await risk_review_service.list_risk_reviews(
        session,
        news_item_id=news_item_id,
        entity_type=entity_type,
        entity_id=entity_id,
        limit=limit,
        offset=offset,
    )
    return [RiskReviewRead.model_validate(review) for review in reviews]


@router.get("/news/{news_id}/risk-reviews", response_model=list[RiskReviewRead])
async def list_news_risk_reviews(
    news_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[RiskReviewRead]:
    reviews = await risk_review_service.list_risk_reviews(
        session, news_item_id=news_id, limit=limit, offset=offset
    )
    return [RiskReviewRead.model_validate(review) for review in reviews]


@router.get("/risk-reviews/{risk_review_id}", response_model=RiskReviewRead)
async def get_risk_review(risk_review_id: str, session: SessionDep) -> RiskReviewRead:
    review = await risk_review_service.get_risk_review(session, risk_review_id)
    return RiskReviewRead.model_validate(review)
