from __future__ import annotations

import re
import unicodedata
from html import escape
from urllib.parse import urlsplit, urlunsplit

from sqlalchemy import Select, desc, exists, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import XCRIPTO_WEB_CHANNEL
from app.core.errors import NotFoundError
from app.models import ContentPiece, NewsItem, PublicationRecord

PUBLIC_ARTICLE_BODY_STATUSES = {"approved"}

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = _SLUG_RE.sub("-", ascii_value).strip("-")
    return slug or "news"


def normalize_public_base_url(value: str | None, fallback: str) -> str:
    raw = (value or "").strip() or fallback
    if "://" not in raw:
        raw = f"https://{raw}"
    parts = urlsplit(raw)
    scheme = parts.scheme or "https"
    netloc = parts.netloc or parts.path
    return urlunsplit((scheme, netloc.rstrip("/"), "", "", ""))


def public_news_url(base_url: str, slug: str) -> str:
    return f"{base_url.rstrip('/')}/news/{slug}"


def canonical_slug_from_url(value: str | None) -> str | None:
    if not value:
        return None
    path = urlsplit(value).path.rstrip("/")
    if not path:
        return None
    slug = path.rsplit("/", 1)[-1].strip()
    return slug or None


async def latest_canonical_publication_record(
    session: AsyncSession,
    news_item_id: str,
) -> PublicationRecord | None:
    result = await session.execute(
        select(PublicationRecord)
        .where(
            PublicationRecord.news_item_id == news_item_id,
            PublicationRecord.channel == XCRIPTO_WEB_CHANNEL,
            PublicationRecord.publication_status == "published",
        )
        .order_by(PublicationRecord.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def resolve_canonical_slug(
    session: AsyncSession,
    news_item_id: str,
    title: str,
) -> str:
    existing = await latest_canonical_publication_record(session, news_item_id)
    if existing and existing.canonical_slug:
        return existing.canonical_slug
    if existing and existing.published_url:
        existing_slug = canonical_slug_from_url(existing.published_url)
        if existing_slug:
            return existing_slug

    candidate = slugify(title)
    result = await session.execute(
        select(
            PublicationRecord.news_item_id,
            PublicationRecord.canonical_slug,
            PublicationRecord.published_url,
        )
        .where(
            PublicationRecord.channel == XCRIPTO_WEB_CHANNEL,
            PublicationRecord.publication_status == "published",
        )
    )
    for row_news_item_id, row_slug, row_published_url in result.all():
        slug = row_slug or canonical_slug_from_url(row_published_url)
        if slug == candidate and row_news_item_id != news_item_id:
            return f"{candidate}-{news_item_id[:8]}"
    return candidate


def _apply_public_filters(
    stmt: Select,
    q: str | None = None,
    category: str | None = None,
) -> Select:
    stmt = stmt.where(
        exists(
            select(1).where(
                PublicationRecord.news_item_id == NewsItem.id,
                PublicationRecord.channel == XCRIPTO_WEB_CHANNEL,
                PublicationRecord.publication_status == "published",
            )
        )
    )
    if category is not None:
        stmt = stmt.where(NewsItem.category == category)
    if q is not None:
        pattern = f"%{_escape_like(q)}%"
        stmt = stmt.where(
            or_(
                NewsItem.title.ilike(pattern, escape="\\"),
                NewsItem.summary.ilike(pattern, escape="\\"),
                NewsItem.source_name.ilike(pattern, escape="\\"),
                NewsItem.source_url.ilike(pattern, escape="\\"),
                NewsItem.category.ilike(pattern, escape="\\"),
            )
        )
    return stmt


async def list_public_news_items(
    session: AsyncSession,
    q: str | None = None,
    category: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[NewsItem]:
    stmt = _apply_public_filters(
        select(NewsItem).order_by(desc(NewsItem.updated_at), desc(NewsItem.created_at)),
        q=q,
        category=category,
    )
    stmt = stmt.offset(offset).limit(limit)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def count_public_news_items(
    session: AsyncSession,
    q: str | None = None,
    category: str | None = None,
) -> int:
    stmt = _apply_public_filters(select(func.count()).select_from(NewsItem), q=q, category=category)
    result = await session.execute(stmt)
    return int(result.scalar_one())


async def get_public_news_item_by_slug(session: AsyncSession, slug: str) -> NewsItem | None:
    result = await session.execute(
        select(NewsItem, PublicationRecord)
        .join(PublicationRecord, PublicationRecord.news_item_id == NewsItem.id)
        .where(
            PublicationRecord.channel == XCRIPTO_WEB_CHANNEL,
            PublicationRecord.publication_status == "published",
        )
        .order_by(desc(PublicationRecord.created_at), desc(NewsItem.updated_at))
    )
    for item, publication_record in result.all():
        item_slug = publication_record.canonical_slug or canonical_slug_from_url(
            publication_record.published_url
        )
        if item_slug is None:
            item_slug = slugify(item.title)
        if item_slug == slug:
            return item
    return None


async def get_public_categories(session: AsyncSession) -> list[str]:
    result = await session.execute(
        select(NewsItem.category)
        .where(
            exists(
                select(1).where(
                    PublicationRecord.news_item_id == NewsItem.id,
                    PublicationRecord.channel == XCRIPTO_WEB_CHANNEL,
                    PublicationRecord.publication_status == "published",
                )
            )
        )
        .distinct()
        .order_by(NewsItem.category.asc())
    )
    return [category for category in result.scalars().all() if category]


async def latest_publication_record(
    session: AsyncSession,
    news_item_id: str,
) -> PublicationRecord | None:
    result = await session.execute(
        select(PublicationRecord)
        .where(PublicationRecord.news_item_id == news_item_id)
        .order_by(PublicationRecord.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def latest_public_content_piece(
    session: AsyncSession,
    news_item_id: str,
) -> ContentPiece | None:
    result = await session.execute(
        select(ContentPiece)
        .where(
            ContentPiece.news_item_id == news_item_id,
            ContentPiece.status.in_(PUBLIC_ARTICLE_BODY_STATUSES),
        )
        .order_by(ContentPiece.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def build_public_news_payload(
    session: AsyncSession,
    item: NewsItem,
    base_url: str,
) -> dict:
    publication_record = await latest_canonical_publication_record(session, item.id)
    if publication_record is None:
        raise NotFoundError("Public news item")
    slug = (
        publication_record.canonical_slug
        or canonical_slug_from_url(publication_record.published_url)
        or slugify(item.title)
    )
    canonical_url = publication_record.published_url or public_news_url(base_url, slug)
    content_piece = await latest_public_content_piece(session, item.id)
    title = content_piece.title if content_piece else item.title
    summary = content_piece.summary if content_piece else item.summary
    author = (
        publication_record.owner
        if publication_record and publication_record.owner
        else content_piece.owner
        if content_piece and content_piece.owner
        else item.source_name
    )
    published_at = publication_record.published_at or item.updated_at

    return {
        "id": item.id,
        "slug": slug,
        "title": title,
        "summary": summary,
        "category": item.category,
        "source_name": item.source_name,
        "source_url": item.source_url,
        "status": publication_record.publication_status,
        "author": author,
        "published_at": published_at,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
        "cover_image_url": None,
        "tags": [item.category],
        "canonical_url": canonical_url,
        "seo_title": item.title,
        "seo_description": item.summary,
        "og_title": item.title,
        "og_description": item.summary,
        "og_image": None,
        "json_ld_type": "NewsArticle",
    }


async def build_public_article_payload(
    session: AsyncSession,
    item: NewsItem,
    base_url: str,
) -> dict:
    content_piece = await latest_public_content_piece(session, item.id)
    if content_piece is None:
        raise NotFoundError("Public article")

    publication_record = await latest_canonical_publication_record(session, item.id)
    if publication_record is None:
        raise NotFoundError("Public article")
    summary = content_piece.summary or item.summary
    title = content_piece.title or item.title
    slug = (
        publication_record.canonical_slug
        or canonical_slug_from_url(publication_record.published_url)
        or slugify(title)
    )
    canonical_url = publication_record.published_url or public_news_url(base_url, slug)
    author = (
        publication_record.owner
        if publication_record and publication_record.owner
        else content_piece.owner
        if content_piece.owner
        else item.source_name
    )
    published_at = publication_record.published_at or content_piece.updated_at or item.updated_at

    return {
        "id": item.id,
        "slug": slug,
        "title": title,
        "summary": summary,
        "body": content_piece.body,
        "body_format": "markdown",
        "category": content_piece.category or item.category,
        "source_name": item.source_name,
        "source_url": item.source_url,
        "status": publication_record.publication_status,
        "author": author,
        "published_at": published_at,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
        "cover_image_url": None,
        "tags": [content_piece.category or item.category],
        "canonical_url": canonical_url,
        "seo_title": title,
        "seo_description": summary,
        "og_title": title,
        "og_description": summary,
        "og_image": None,
        "json_ld_type": "NewsArticle",
    }


def build_rss_xml(items: list[dict], feed_url: str) -> str:
    channel_items = []
    for item in items:
        pub_date = item["published_at"] or item["updated_at"]
        pub_date_value = pub_date.strftime("%a, %d %b %Y %H:%M:%S +0000") if pub_date else ""
        channel_items.append(
            "\n".join(
                [
                    "    <item>",
                    f"      <title>{escape(item['title'])}</title>",
                    f"      <link>{escape(item['canonical_url'])}</link>",
                    f"      <guid isPermaLink=\"false\">{escape(item['id'])}</guid>",
                    f"      <description>{escape(item['summary'])}</description>",
                    f"      <pubDate>{escape(pub_date_value)}</pubDate>",
                    "    </item>",
                ]
            )
        )
    return "\n".join(
        [
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
            "<rss version=\"2.0\">",
            "  <channel>",
            "    <title>XCripto News</title>",
            f"    <link>{escape(feed_url)}</link>",
            "    <description>XCripto public news feed</description>",
            *channel_items,
            "  </channel>",
            "</rss>",
        ]
    )


def build_sitemap_xml(items: list[dict], site_url: str) -> str:
    urls = []
    for item in items:
        lastmod = item["published_at"] or item["updated_at"]
        lastmod_value = lastmod.strftime("%Y-%m-%dT%H:%M:%S%z") if lastmod else ""
        urls.append(
            "\n".join(
                [
                    "  <url>",
                    f"    <loc>{escape(item['canonical_url'])}</loc>",
                    f"    <lastmod>{escape(lastmod_value)}</lastmod>",
                    "  </url>",
                ]
            )
        )
    return "\n".join(
        [
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            *urls,
            "</urlset>",
        ]
    )


def _escape_like(value: str) -> str:
    return value.replace("\\", "\\\\").replace("%", r"\%").replace("_", r"\_")
