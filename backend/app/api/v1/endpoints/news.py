from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import NEWS_PRIORITIES, NEWS_STATUSES
from app.core.errors import DomainValidationError
from app.core.security import require_api_key
from app.db.session import get_session
from app.schemas.news import NewsCreate, NewsRead, NewsStatusUpdate
from app.services import news_service

router = APIRouter(prefix="/news", tags=["news"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "/intake",
    response_model=NewsRead,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
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
    response: Response,
    status: str | None = Query(default=None, description="Filtro exacto por estado editorial"),
    q: str | None = Query(
        default=None,
        min_length=1,
        max_length=200,
        description=(
            "Búsqueda case-insensitive en title, summary, source_name, source_url y category"
        ),
    ),
    category: str | None = Query(default=None, description="Filtro exacto por categoría"),
    priority: str | None = Query(default=None, description="Filtro exacto por prioridad (P0-P4)"),
    source: str | None = Query(
        default=None,
        min_length=1,
        max_length=200,
        description="Filtro case-insensitive por nombre o URL de fuente",
    ),
    created_from: Annotated[
        datetime | None,
        Query(description="Noticias creadas en o después de esta fecha (ISO 8601)"),
    ] = None,
    created_to: Annotated[
        datetime | None,
        Query(description="Noticias creadas en o antes de esta fecha (ISO 8601)"),
    ] = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[NewsRead]:
    if status is not None and status not in NEWS_STATUSES:
        raise DomainValidationError(f"status must be one of {sorted(NEWS_STATUSES)}")
    if priority is not None and priority not in NEWS_PRIORITIES:
        raise DomainValidationError(f"priority must be one of {sorted(NEWS_PRIORITIES)}")

    filters = {
        "status": status,
        "q": q,
        "category": category,
        "priority": priority,
        "source": source,
        "created_from": created_from,
        "created_to": created_to,
    }
    items = await news_service.list_news_items(session, limit=limit, offset=offset, **filters)
    total = await news_service.count_news_items(session, **filters)
    response.headers["X-Total-Count"] = str(total)
    return [NewsRead.model_validate(item) for item in items]


@router.get("/{news_id}", response_model=NewsRead)
async def get_news(news_id: str, session: SessionDep) -> NewsRead:
    item = await news_service.get_news_item(session, news_id)
    return NewsRead.model_validate(item)


@router.patch(
    "/{news_id}/status",
    response_model=NewsRead,
    dependencies=[Depends(require_api_key)],
)
async def update_news_status(
    news_id: str,
    payload: NewsStatusUpdate,
    session: SessionDep,
) -> NewsRead:
    item = await news_service.update_news_status(session, news_id, payload.status)
    return NewsRead.model_validate(item)
