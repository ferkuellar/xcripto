from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class PublicationRecord(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "publication_records"

    content_piece_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("content_pieces.id"), nullable=False, index=True
    )
    distribution_plan_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("distribution_plans.id"), nullable=False, index=True
    )
    news_item_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("news_items.id"), nullable=False, index=True
    )
    channel: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    publication_status: Mapped[str] = mapped_column(
        String(40), nullable=False, default="scheduled", index=True
    )
    published_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    external_id: Mapped[str | None] = mapped_column(String(180), nullable=True)
    canonical_slug: Mapped[str | None] = mapped_column(String(280), nullable=True, index=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    owner: Mapped[str | None] = mapped_column(String(120), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
