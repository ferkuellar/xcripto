from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import NEWS_STATUSES
from app.core.errors import DomainValidationError
from app.db.session import get_session
from app.schemas.news import NewsCreate, NewsRead, NewsStatusUpdate
from app.services import news_service

router = APIRouter(prefix="/news", tags=["news"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post("/intake", response_model=NewsRead, status_code=201)
async def intake_news(
    payload: NewsCreate,
    request: Request,
    session: SessionDep,
) -> NewsRead:
    item = await news_service.create_news_item(session, payload, request.state.correlation_id)
    return NewsRead.model_validate(item)


@router.get("", response_model=list[NewsRead])
async def list_news(
    session: SessionDep,
    status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[NewsRead]:
    if status is not None and status not in NEWS_STATUSES:
        raise DomainValidationError(f"status must be one of {sorted(NEWS_STATUSES)}")
    items = await news_service.list_news_items(session, status=status, limit=limit, offset=offset)
    return [NewsRead.model_validate(item) for item in items]


@router.get("/{news_id}", response_model=NewsRead)
async def get_news(news_id: str, session: SessionDep) -> NewsRead:
    item = await news_service.get_news_item(session, news_id)
    return NewsRead.model_validate(item)


@router.patch("/{news_id}/status", response_model=NewsRead)
async def update_news_status(
    news_id: str,
    payload: NewsStatusUpdate,
    session: SessionDep,
) -> NewsRead:
    item = await news_service.update_news_status(session, news_id, payload.status)
    return NewsRead.model_validate(item)
