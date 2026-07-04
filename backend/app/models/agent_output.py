from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class AgentOutput(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "agent_outputs"

    agent_execution_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("agent_executions.id"), nullable=True, index=True
    )
    agent_name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    agent_version: Mapped[str | None] = mapped_column(String(40), nullable=True)
    output_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="stored", index=True)
    entity_type: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    entity_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    news_item_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("news_items.id"), nullable=True, index=True
    )
    workflow_run_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("workflow_runs.id"), nullable=True, index=True
    )
    workflow_step_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("workflow_steps.id"), nullable=True, index=True
    )
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[dict | list] = mapped_column(JSON, nullable=False)
    risk_flags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    missing_requirements: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    next_agent: Mapped[str | None] = mapped_column(String(80), nullable=True)
    human_review_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    accepted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    accepted_by: Mapped[str | None] = mapped_column(String(120), nullable=True)
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rejected_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    superseded_by_output_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("agent_outputs.id"), nullable=True
    )
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
