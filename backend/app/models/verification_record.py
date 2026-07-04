from sqlalchemy import JSON, Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class VerificationRecord(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "verification_records"

    news_item_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("news_items.id"), nullable=False, index=True
    )
    verification_status: Mapped[str] = mapped_column(
        String(40), nullable=False, default="unverified", index=True
    )
    evidence_level: Mapped[str] = mapped_column(String(20), nullable=False, default="unknown")
    confidence_level: Mapped[str] = mapped_column(String(20), nullable=False, default="unknown")
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    verified_claims: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    unverified_claims: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    contradictions: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    source_refs: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    human_review_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    reviewer: Mapped[str | None] = mapped_column(String(120), nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
