from __future__ import annotations

import asyncio
import json
import logging
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.errors import ConflictError, NotFoundError
from app.integrations.binance_square_client import (
    BinanceSquarePublishError,
    BinanceSquarePublishResult,
    build_binance_square_post,
    publish_binance_square_post,
)
from app.integrations.x_client import (
    XPublishError,
    XPublishResult,
    build_x_post,
    publish_x_post,
)
from app.models import ContentPiece, NewsItem, PublicationRecord
from app.services.public_news_service import slugify

logger = logging.getLogger(__name__)

TELEGRAM_CHANNEL = "Telegram"
BINANCE_SQUARE_CHANNEL = "BINANCE_SQUARE"
BINANCE_SQUARE_CHANNEL_ALIASES = {BINANCE_SQUARE_CHANNEL, "Binance Square"}
X_CHANNEL_ALIASES = {"X", "X / Twitter"}
TELEGRAM_API_BASE_URL = "https://api.telegram.org"


@dataclass(slots=True)
class PublicationDispatchResult:
    publication_record_id: str
    channel: str
    dispatched: bool
    dry_run: bool
    idempotent: bool = False
    external_id: str | None = None
    published_url: str | None = None
    message: str | None = None
    reason: str | None = None


def _telegram_message_url(channel_id: str, message_id: str) -> str | None:
    normalized = channel_id.strip()
    if not normalized:
        return None
    if normalized.startswith("@"):
        return f"https://t.me/{normalized.removeprefix('@')}/{message_id}"
    if normalized.startswith("-100") and normalized[4:].isdigit():
        return f"https://t.me/c/{normalized[4:]}/{message_id}"
    if normalized.isdigit():
        return f"https://t.me/c/{normalized.lstrip('-')}/{message_id}"
    return None


def _telegram_message_text(
    news_item: NewsItem,
    content_piece: ContentPiece,
    canonical_url: str,
) -> str:
    parts: list[str] = [content_piece.title or news_item.title]
    summary = content_piece.summary or news_item.summary
    if summary:
        parts.extend(["", summary])
    parts.extend(["", canonical_url])
    if news_item.source_name:
        source_line = news_item.source_name
        if news_item.source_url:
            source_line = f"{source_line} ({news_item.source_url})"
        parts.extend(["", f"Source: {source_line}"])
    return "\n".join(parts).strip()


async def _latest_publication_for_channel(
    session: AsyncSession,
    news_item_id: str,
    channel: str,
) -> PublicationRecord | None:
    channel_aliases = {channel}
    if channel in X_CHANNEL_ALIASES:
        channel_aliases = X_CHANNEL_ALIASES
    if channel in BINANCE_SQUARE_CHANNEL_ALIASES:
        channel_aliases = BINANCE_SQUARE_CHANNEL_ALIASES
    result = await session.execute(
        select(PublicationRecord)
        .where(
            PublicationRecord.news_item_id == news_item_id,
            PublicationRecord.channel.in_(channel_aliases),
            PublicationRecord.publication_status == "published",
        )
        .order_by(PublicationRecord.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def _mark_publication_failed(
    session: AsyncSession,
    record: PublicationRecord,
    note: str,
) -> None:
    record.publication_status = "failed"
    record.external_id = None
    record.published_url = None
    record.published_at = None
    record.notes = _append_note(record.notes, note)
    await session.commit()
    await session.refresh(record)


def _append_note(existing: str | None, note: str) -> str:
    cleaned_existing = (existing or "").strip()
    cleaned_note = note.strip()
    if cleaned_existing and cleaned_note:
        return f"{cleaned_existing}\n{cleaned_note}"
    return cleaned_existing or cleaned_note


async def _send_telegram_message(text: str) -> dict:
    settings = get_settings()
    if not settings.telegram_bot_token or not settings.telegram_channel_id:
        raise ConflictError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID are required")

    payload = {
        "chat_id": settings.telegram_channel_id,
        "text": text,
        "disable_web_page_preview": False,
    }
    request = urllib.request.Request(
        f"{TELEGRAM_API_BASE_URL}/bot{settings.telegram_bot_token}/sendMessage",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    def _do_request() -> dict:
        with urllib.request.urlopen(  # noqa: S310 - Telegram API endpoint is fixed
            request,
            timeout=get_settings().request_timeout_seconds,
        ) as response:
            return json.loads(response.read().decode("utf-8"))

    return await asyncio.to_thread(_do_request)


async def dispatch_publication_record(
    session: AsyncSession,
    publication_record_id: str,
    *,
    dry_run: bool = False,
) -> PublicationDispatchResult:
    record = await session.get(PublicationRecord, publication_record_id)
    if record is None:
        raise NotFoundError("Publication record")

    if record.channel not in (
        {TELEGRAM_CHANNEL} | X_CHANNEL_ALIASES | BINANCE_SQUARE_CHANNEL_ALIASES
    ):
        return PublicationDispatchResult(
            publication_record_id=record.id,
            channel=record.channel,
            dispatched=False,
            dry_run=dry_run,
            reason="channel not implemented",
        )

    if record.publication_status == "published" and (
        record.external_id
        or record.published_url
        or (record.channel in BINANCE_SQUARE_CHANNEL_ALIASES and record.published_at is not None)
    ):
        return PublicationDispatchResult(
            publication_record_id=record.id,
            channel=record.channel,
            dispatched=True,
            dry_run=dry_run,
            idempotent=True,
            external_id=record.external_id,
            published_url=record.published_url,
            reason="already published",
        )

    if record.publication_status not in {"published", "failed"} and not dry_run:
        return PublicationDispatchResult(
            publication_record_id=record.id,
            channel=record.channel,
            dispatched=False,
            dry_run=dry_run,
            reason="publication record is not published",
        )

    existing = await _latest_publication_for_channel(session, record.news_item_id, record.channel)
    if existing is not None and existing.id != record.id:
        record.publication_status = "published"
        record.external_id = existing.external_id
        record.published_url = existing.published_url
        record.published_at = existing.published_at or record.published_at
        await session.commit()
        await session.refresh(record)
        return PublicationDispatchResult(
            publication_record_id=record.id,
            channel=record.channel,
            dispatched=True,
            dry_run=dry_run,
            idempotent=True,
            external_id=existing.external_id,
            published_url=existing.published_url,
            reason="already published for this channel",
        )

    news_item = await session.get(NewsItem, record.news_item_id)
    content_piece = await session.get(ContentPiece, record.content_piece_id)
    if news_item is None:
        raise NotFoundError("News item")
    if content_piece is None:
        raise NotFoundError("Content piece")

    canonical_url = (
        f"{(get_settings().public_site_url or 'https://localhost').rstrip('/')}/news/"
        f"{slugify(content_piece.title or news_item.title)}"
    )
    if record.channel == TELEGRAM_CHANNEL:
        text = _telegram_message_text(news_item, content_piece, canonical_url)
        if dry_run:
            logger.info(
                "telegram publication dry-run",
                extra={
                    "publication_record_id": record.id,
                    "news_item_id": record.news_item_id,
                    "channel": record.channel,
                },
            )
            return PublicationDispatchResult(
                publication_record_id=record.id,
                channel=record.channel,
                dispatched=False,
                dry_run=True,
                message=text,
                reason="dry_run",
            )

        try:
            payload = await _send_telegram_message(text)
        except (urllib.error.URLError, TimeoutError, OSError, ConflictError) as exc:
            await _mark_publication_failed(
                session,
                record,
                f"telegram publish failed: {exc}",
            )
            logger.exception(
                "telegram publication failed",
                extra={
                    "publication_record_id": record.id,
                    "news_item_id": record.news_item_id,
                    "channel": record.channel,
                },
            )
            raise ConflictError("Telegram publication failed") from exc

        result = payload.get("result", {}) if isinstance(payload, dict) else {}
        message_id = str(result.get("message_id") or "")
        if not message_id:
            await _mark_publication_failed(
                session,
                record,
                "telegram publish returned no message_id",
            )
            raise ConflictError("Telegram publication failed")

        published_url = _telegram_message_url(get_settings().telegram_channel_id or "", message_id)
        record.external_id = message_id
        if published_url:
            record.published_url = published_url
        record.publication_status = "published"
        record.published_at = datetime.now(UTC)
        await session.commit()
        await session.refresh(record)

        logger.info(
            "telegram publication dispatched",
            extra={
                "publication_record_id": record.id,
                "news_item_id": record.news_item_id,
                "channel": record.channel,
                "external_id": message_id,
            },
        )
        return PublicationDispatchResult(
            publication_record_id=record.id,
            channel=record.channel,
            dispatched=True,
            dry_run=False,
            external_id=message_id,
            published_url=published_url,
            message=text,
        )

    if record.channel in X_CHANNEL_ALIASES:
        text = build_x_post(
            title=content_piece.title or news_item.title,
            summary=content_piece.summary or news_item.summary,
            canonical_url=canonical_url,
        )
        if dry_run:
            logger.info(
                "x publication dry-run",
                extra={
                    "publication_record_id": record.id,
                    "news_item_id": record.news_item_id,
                    "channel": record.channel,
                },
            )
            return PublicationDispatchResult(
                publication_record_id=record.id,
                channel=record.channel,
                dispatched=False,
                dry_run=True,
                message=text,
                reason="dry_run",
            )

        try:
            result: XPublishResult = await asyncio.to_thread(publish_x_post, text)
        except XPublishError as exc:
            await _mark_publication_failed(
                session,
                record,
                f"x publish failed: {exc}",
            )
            logger.warning(
                "x publication failed",
                extra={
                    "publication_record_id": record.id,
                    "news_item_id": record.news_item_id,
                    "channel": record.channel,
                    "status_code": exc.status_code,
                    "retryable": exc.retryable,
                    "error_type": exc.error_type,
                },
            )
            raise ConflictError("X publication failed") from exc

        record.external_id = result.post_id
        record.published_url = result.post_url
        record.publication_status = "published"
        record.published_at = datetime.now(UTC)
        await session.commit()
        await session.refresh(record)

        logger.info(
            "x publication dispatched",
            extra={
                "publication_record_id": record.id,
                "news_item_id": record.news_item_id,
                "channel": record.channel,
                "external_id": result.post_id,
            },
        )
        return PublicationDispatchResult(
            publication_record_id=record.id,
            channel=record.channel,
            dispatched=True,
            dry_run=False,
            external_id=result.post_id,
            published_url=result.post_url,
            message=text,
        )

    if record.channel in BINANCE_SQUARE_CHANNEL_ALIASES:
        text = build_binance_square_post(
            title=content_piece.title or news_item.title,
            summary=content_piece.summary or news_item.summary,
            canonical_url=canonical_url,
        )
        if dry_run:
            logger.info(
                "binance square publication dry-run",
                extra={
                    "publication_record_id": record.id,
                    "news_item_id": record.news_item_id,
                    "channel": record.channel,
                },
            )
            return PublicationDispatchResult(
                publication_record_id=record.id,
                channel=record.channel,
                dispatched=False,
                dry_run=True,
                message=text,
                reason="dry_run",
            )

        try:
            result: BinanceSquarePublishResult = await asyncio.to_thread(
                publish_binance_square_post,
                text,
            )
        except BinanceSquarePublishError as exc:
            note = f"binance square publish failed: {exc}"
            if exc.ambiguous_outcome:
                note = f"{note} (ambiguous outcome)"
            await _mark_publication_failed(
                session,
                record,
                note,
            )
            logger.warning(
                "binance square publication failed",
                extra={
                    "publication_record_id": record.id,
                    "news_item_id": record.news_item_id,
                    "channel": record.channel,
                    "status_code": exc.status_code,
                    "retryable": exc.retryable,
                    "error_type": exc.error_type,
                    "ambiguous_outcome": exc.ambiguous_outcome,
                },
            )
            raise ConflictError("Binance Square publication failed") from exc

        record.external_id = result.external_id
        record.published_url = result.published_url
        record.publication_status = "published"
        record.published_at = datetime.now(UTC)
        await session.commit()
        await session.refresh(record)

        logger.info(
            "binance square publication dispatched",
            extra={
                "publication_record_id": record.id,
                "news_item_id": record.news_item_id,
                "channel": record.channel,
                "external_id": result.external_id,
            },
        )
        return PublicationDispatchResult(
            publication_record_id=record.id,
            channel=record.channel,
            dispatched=True,
            dry_run=False,
            external_id=result.external_id,
            published_url=result.published_url,
            message=text,
        )

    return PublicationDispatchResult(
        publication_record_id=record.id,
        channel=record.channel,
        dispatched=False,
        dry_run=dry_run,
        reason="channel not implemented",
    )
