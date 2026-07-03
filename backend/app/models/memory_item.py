from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class MemoryItem(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "memory_items"

    memory_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    memory_status: Mapped[str] = mapped_column(
        String(40), nullable=False, default="proposed", index=True
    )
    title: Mapped[str] = mapped_column(String(280), nullable=False)
    memory_statement: Mapped[str] = mapped_column(Text, nullable=False)
    why_it_matters: Mapped[str | None] = mapped_column(Text, nullable=True)
    how_to_use: Mapped[str | None] = mapped_column(Text, nullable=True)
    how_not_to_use: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_or_origin: Mapped[str] = mapped_column(Text, nullable=False)
    entity_type: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    entity_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    news_item_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("news_items.id"), nullable=True, index=True
    )
    workflow_run_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("workflow_runs.id"), nullable=True, index=True
    )
    agent_output_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("agent_outputs.id"), nullable=True, index=True
    )
    audit_check_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("audit_checks.id"), nullable=True, index=True
    )
    metric_snapshot_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("metric_snapshots.id"), nullable=True, index=True
    )
    confidence_level: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    persistence_level: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    scope: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    risk_flags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    expiration_recommendation: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    human_review_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    approved_by: Mapped[str | None] = mapped_column(String(120), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    invalidated_by: Mapped[str | None] = mapped_column(String(120), nullable=True)
    invalidated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    invalidation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
