from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class WorkflowRun(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workflow_runs"

    news_item_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("news_items.id"), nullable=False, index=True
    )
    workflow_type: Mapped[str] = mapped_column(
        String(80), nullable=False, default="editorial_pipeline", index=True
    )
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="created", index=True)
    current_step: Mapped[str] = mapped_column(String(80), nullable=False, default="intake")
    readiness_status: Mapped[str] = mapped_column(
        String(40), nullable=False, default="not_ready", index=True
    )
    blocked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    blocking_reasons: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    missing_requirements: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    recommended_next_action: Mapped[str | None] = mapped_column(Text, nullable=True)
    next_agent: Mapped[str] = mapped_column(String(80), nullable=False, default="None")
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
