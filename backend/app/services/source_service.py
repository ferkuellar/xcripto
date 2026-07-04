from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.models import NewsItem, SourceReference
from app.schemas.source import SourceCreate


async def create_source(
    session: AsyncSession, payload: SourceCreate, correlation_id: str | None = None
) -> SourceReference:
    source = SourceReference(**payload.model_dump())
    if source.correlation_id is None:
        source.correlation_id = correlation_id
    session.add(source)
    await session.commit()
    await session.refresh(source)
    return source


async def list_sources(
    session: AsyncSession,
    source_status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[SourceReference]:
    stmt = (
        select(SourceReference)
        .order_by(SourceReference.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    if source_status is not None:
        stmt = stmt.where(SourceReference.source_status == source_status)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_source(session: AsyncSession, source_id: str) -> SourceReference:
    source = await session.get(SourceReference, source_id)
    if source is None:
        raise NotFoundError("Source")
    return source


async def get_source_for_news_item(
    session: AsyncSession, news: NewsItem
) -> SourceReference | None:
    """Resuelve la SourceReference que sostiene una noticia por URL o nombre.

    Fuente única de verdad para el scoring de readiness y el gate de calidad de
    fuente; devuelve ``None`` cuando la noticia solo tiene campos denormalizados.
    """
    result = await session.execute(
        select(SourceReference)
        .where(
            or_(
                SourceReference.source_url == news.source_url,
                SourceReference.source_name == news.source_name,
            )
        )
        .limit(1)
    )
    return result.scalar_one_or_none()
