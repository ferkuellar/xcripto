from sqlalchemy import JSON, Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class ContentPiece(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "content_pieces"

    news_item_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("news_items.id"), nullable=False, index=True
    )
    content_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(280), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="drafting", index=True)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    priority: Mapped[str] = mapped_column(String(2), nullable=False, default="P3", index=True)
    verification_status: Mapped[str] = mapped_column(String(40), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(40), nullable=False)
    source_refs: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    disclaimer_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    human_review_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    owner: Mapped[str | None] = mapped_column(String(120), nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
