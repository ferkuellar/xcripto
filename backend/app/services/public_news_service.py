from __future__ import annotations

import re
import unicodedata
from html import escape
from urllib.parse import urlsplit, urlunsplit

from sqlalchemy import Select, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.models import ContentPiece, NewsItem, PublicationRecord

PUBLIC_NEWS_STATUSES = {"approved", "scheduled", "published", "distributed"}
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


def _apply_public_filters(
    stmt: Select,
    q: str | None = None,
    category: str | None = None,
) -> Select:
    stmt = stmt.where(NewsItem.status.in_(PUBLIC_NEWS_STATUSES))
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
        select(NewsItem)
        .where(NewsItem.status.in_(PUBLIC_NEWS_STATUSES))
        .order_by(desc(NewsItem.updated_at), desc(NewsItem.created_at))
    )
    for item in result.scalars().all():
        if slugify(item.title) == slug:
            return item
    return None


async def get_public_categories(session: AsyncSession) -> list[str]:
    result = await session.execute(
        select(NewsItem.category)
        .where(NewsItem.status.in_(PUBLIC_NEWS_STATUSES))
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
    publication_record = await latest_publication_record(session, item.id)
    slug = slugify(item.title)
    canonical_url = public_news_url(base_url, slug)
    author = (
        publication_record.owner
        if publication_record and publication_record.owner
        else item.source_name
    )
    published_at = publication_record.published_at if publication_record else None
    if published_at is None and item.status == "published":
        published_at = item.updated_at

    return {
        "id": item.id,
        "slug": slug,
        "title": item.title,
        "summary": item.summary,
        "category": item.category,
        "source_name": item.source_name,
        "source_url": item.source_url,
        "status": item.status,
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

    publication_record = await latest_publication_record(session, item.id)
    summary = content_piece.summary or item.summary
    title = content_piece.title or item.title
    slug = slugify(item.title)
    canonical_url = public_news_url(base_url, slug)
    author = (
        publication_record.owner
        if publication_record and publication_record.owner
        else content_piece.owner
        if content_piece.owner
        else item.source_name
    )
    published_at = publication_record.published_at if publication_record else None
    if published_at is None:
        published_at = content_piece.updated_at or item.updated_at

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
        "status": item.status,
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
