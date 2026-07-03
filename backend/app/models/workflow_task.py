from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class WorkflowTask(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workflow_tasks"

    workflow_run_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("workflow_runs.id"), nullable=False, index=True
    )
    workflow_step_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("workflow_steps.id"), nullable=True, index=True
    )
    news_item_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("news_items.id"), nullable=True, index=True
    )
    task_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    task_status: Mapped[str] = mapped_column(
        String(40), nullable=False, default="queued", index=True
    )
    priority: Mapped[str] = mapped_column(String(2), nullable=False, default="P3", index=True)
    assigned_agent: Mapped[str] = mapped_column(
        String(120), nullable=False, default="None", index=True
    )
    assigned_to: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(280), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    input_payload: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    output_ref: Mapped[str | None] = mapped_column(String(180), nullable=True)
    agent_execution_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("agent_executions.id"), nullable=True, index=True
    )
    agent_output_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("agent_outputs.id"), nullable=True, index=True
    )
    blocking: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    blocking_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    failed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
