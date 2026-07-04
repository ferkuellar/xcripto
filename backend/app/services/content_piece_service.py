from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ConflictError, NotFoundError
from app.models import ContentPiece, NewsItem
from app.schemas.content_piece import ContentPieceCreate


async def create_content_piece(
    session: AsyncSession,
    payload: ContentPieceCreate,
    correlation_id: str | None = None,
) -> ContentPiece:
    if await session.get(NewsItem, payload.news_item_id) is None:
        raise NotFoundError("News item")
    if payload.verification_status == "unverified":
        raise ConflictError("ContentPiece cannot be created with unverified verification_status")
    if payload.risk_level == "critical":
        raise ConflictError("ContentPiece cannot be created with critical risk_level")

    piece = ContentPiece(**payload.model_dump())
    if piece.correlation_id is None:
        piece.correlation_id = correlation_id
    session.add(piece)
    await session.commit()
    await session.refresh(piece)
    return piece


async def list_content_pieces(
    session: AsyncSession,
    news_item_id: str | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[ContentPiece]:
    stmt = select(ContentPiece).order_by(ContentPiece.created_at.desc())
    if news_item_id is not None:
        stmt = stmt.where(ContentPiece.news_item_id == news_item_id)
    if status is not None:
        stmt = stmt.where(ContentPiece.status == status)
    stmt = stmt.limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_content_piece(session: AsyncSession, content_piece_id: str) -> ContentPiece:
    piece = await session.get(ContentPiece, content_piece_id)
    if piece is None:
        raise NotFoundError("Content piece")
    return piece


async def update_content_piece_status(
    session: AsyncSession,
    content_piece_id: str,
    status: str,
) -> ContentPiece:
    piece = await get_content_piece(session, content_piece_id)
    piece.status = status
    await session.commit()
    await session.refresh(piece)
    return piece
