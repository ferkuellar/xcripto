from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class IntakeSignal(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "intake_signals"

    signal_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    signal_status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    source_name: Mapped[str | None] = mapped_column(String(180), nullable=True, index=True)
    source_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    source_type: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    source_published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    raw_title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    raw_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    normalized_title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    normalized_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    language: Mapped[str | None] = mapped_column(String(20), nullable=True)
    topic: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    asset_symbols: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    entities: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    keywords: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    url_canonical: Mapped[str | None] = mapped_column(String(2048), nullable=True, index=True)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    dedupe_key: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    priority: Mapped[str] = mapped_column(String(2), nullable=False, default="P3", index=True)
    confidence_level: Mapped[str] = mapped_column(String(20), nullable=False, default="unknown")
    risk_flags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    adapter_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    adapter_version: Mapped[str | None] = mapped_column(String(40), nullable=True)
    raw_payload: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    normalized_payload: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    duplicate_of_signal_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("intake_signals.id"), nullable=True
    )
    linked_news_item_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("news_items.id"), nullable=True, index=True
    )
    promoted_news_item_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("news_items.id"), nullable=True, index=True
    )
    dedupe_status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    dedupe_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
