from sqlalchemy import JSON, Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class RiskReview(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "risk_reviews"

    news_item_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("news_items.id"), nullable=False, index=True
    )
    entity_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    risk_level: Mapped[str] = mapped_column(String(40), nullable=False, default="unknown")
    severity: Mapped[str] = mapped_column(String(40), nullable=False, default="R-SEV-1")
    decision_recommendation: Mapped[str] = mapped_column(String(80), nullable=False)
    risk_flags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    required_disclaimers: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    language_restrictions: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    human_review_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    publication_block_recommended: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    reviewer: Mapped[str | None] = mapped_column(String(120), nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
