from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.session import get_session
from app.services.public_news_service import (
    build_public_news_payload,
    build_sitemap_xml,
    list_public_news_items,
    normalize_public_base_url,
)

router = APIRouter(tags=["public"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


def _site_base_url(request: Request) -> str:
    settings = get_settings()
    forwarded_host = request.headers.get("x-forwarded-host")
    request_origin = f"{request.url.scheme}://{forwarded_host or request.url.netloc}"
    return normalize_public_base_url(settings.public_web_base_url, request_origin)


@router.get("/sitemap.xml")
async def sitemap(request: Request, session: SessionDep) -> Response:
    base_url = _site_base_url(request)
    items = await list_public_news_items(session, limit=200, offset=0)
    payload = [await build_public_news_payload(session, item, base_url) for item in items]
    xml = build_sitemap_xml(payload, base_url)
    return Response(content=xml, media_type="application/xml; charset=utf-8")
