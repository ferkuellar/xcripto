from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_api_key
from app.db.session import get_session
from app.schemas.content_piece import (
    ContentPieceCreate,
    ContentPieceRead,
    ContentPieceStatusUpdate,
)
from app.services import content_piece_service

router = APIRouter(tags=["content-pieces"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "/content-pieces",
    response_model=ContentPieceRead,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
async def create_content_piece(
    payload: ContentPieceCreate,
    request: Request,
    session: SessionDep,
) -> ContentPieceRead:
    piece = await content_piece_service.create_content_piece(
        session, payload, request.state.correlation_id
    )
    return ContentPieceRead.model_validate(piece)


@router.get("/content-pieces", response_model=list[ContentPieceRead])
async def list_content_pieces(
    session: SessionDep,
    news_item_id: str | None = Query(default=None),
    status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[ContentPieceRead]:
    pieces = await content_piece_service.list_content_pieces(
        session, news_item_id=news_item_id, status=status, limit=limit, offset=offset
    )
    return [ContentPieceRead.model_validate(piece) for piece in pieces]


@router.get("/news/{news_id}/content-pieces", response_model=list[ContentPieceRead])
async def list_news_content_pieces(
    news_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[ContentPieceRead]:
    pieces = await content_piece_service.list_content_pieces(
        session, news_item_id=news_id, limit=limit, offset=offset
    )
    return [ContentPieceRead.model_validate(piece) for piece in pieces]


@router.patch(
    "/content-pieces/{content_piece_id}/status",
    response_model=ContentPieceRead,
    dependencies=[Depends(require_api_key)],
)
async def update_content_piece_status(
    content_piece_id: str,
    payload: ContentPieceStatusUpdate,
    session: SessionDep,
) -> ContentPieceRead:
    piece = await content_piece_service.update_content_piece_status(
        session, content_piece_id, payload.status
    )
    return ContentPieceRead.model_validate(piece)


@router.get("/content-pieces/{content_piece_id}", response_model=ContentPieceRead)
async def get_content_piece(content_piece_id: str, session: SessionDep) -> ContentPieceRead:
    piece = await content_piece_service.get_content_piece(session, content_piece_id)
    return ContentPieceRead.model_validate(piece)
