from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class WorkflowStep(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workflow_steps"

    workflow_run_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("workflow_runs.id"), nullable=False, index=True
    )
    step_name: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    step_status: Mapped[str] = mapped_column(String(40), nullable=False, default="pending")
    required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    entity_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    entity_id: Mapped[str | None] = mapped_column(String(80), nullable=True)
    blocking: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    blocking_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
