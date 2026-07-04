from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class DistributionPlan(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "distribution_plans"

    content_piece_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("content_pieces.id"), nullable=False, index=True
    )
    news_item_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("news_items.id"), nullable=False, index=True
    )
    primary_channel: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    secondary_channels: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    distribution_type: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="proposed", index=True)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    owner: Mapped[str | None] = mapped_column(String(120), nullable=True)
    dependencies: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    metric_plan: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    risk_level: Mapped[str] = mapped_column(String(40), nullable=False, default="unknown")
    publication_readiness: Mapped[str] = mapped_column(String(80), nullable=False, default="draft")
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
