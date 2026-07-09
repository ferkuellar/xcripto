from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.errors import NotFoundError
from app.db.session import get_session
from app.schemas.public_news import PublicArticleRead, PublicNewsRead
from app.services.public_news_service import (
    build_public_article_payload,
    build_public_news_payload,
    build_rss_xml,
    get_public_categories,
    get_public_news_item_by_slug,
    list_public_news_items,
    normalize_public_base_url,
)

router = APIRouter(prefix="/public", tags=["public-news"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


def _site_base_url(request: Request) -> str:
    settings = get_settings()
    forwarded_host = request.headers.get("x-forwarded-host")
    request_origin = f"{request.url.scheme}://{forwarded_host or request.url.netloc}"
    return normalize_public_base_url(settings.public_site_url, request_origin)


@router.get("/news", response_model=list[PublicNewsRead])
async def list_public_news(
    request: Request,
    session: SessionDep,
    q: str | None = Query(default=None),
    category: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[PublicNewsRead]:
    items = await list_public_news_items(
        session,
        q=q,
        category=category,
        limit=limit,
        offset=offset,
    )
    base_url = _site_base_url(request)
    return [
        PublicNewsRead.model_validate(
            await build_public_news_payload(session, item, base_url)
        )
        for item in items
    ]


@router.get("/news/{slug}", response_model=PublicArticleRead)
async def get_public_news_by_slug(
    slug: str,
    request: Request,
    session: SessionDep,
) -> PublicArticleRead:
    item = await get_public_news_item_by_slug(session, slug)
    if item is None:
        raise NotFoundError("Public news item")
    base_url = _site_base_url(request)
    return PublicArticleRead.model_validate(
        await build_public_article_payload(session, item, base_url)
    )


@router.get("/categories", response_model=list[str])
async def list_public_categories(session: SessionDep) -> list[str]:
    return await get_public_categories(session)


@router.get("/search", response_model=list[PublicNewsRead])
async def search_public_news(
    request: Request,
    session: SessionDep,
    q: str = Query(min_length=1),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[PublicNewsRead]:
    items = await list_public_news_items(session, q=q, limit=limit, offset=offset)
    base_url = _site_base_url(request)
    return [
        PublicNewsRead.model_validate(
            await build_public_news_payload(session, item, base_url)
        )
        for item in items
    ]


@router.get("/rss.xml")
async def public_rss(request: Request, session: SessionDep) -> Response:
    base_url = _site_base_url(request)
    items = await list_public_news_items(session, limit=50, offset=0)
    payload = [await build_public_news_payload(session, item, base_url) for item in items]
    xml = build_rss_xml(payload, f"{base_url.rstrip('/')}/rss.xml")
    return Response(content=xml, media_type="application/rss+xml; charset=utf-8")
