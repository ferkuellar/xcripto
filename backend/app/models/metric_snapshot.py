from sqlalchemy import JSON, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class MetricSnapshot(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "metric_snapshots"

    entity_type: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    entity_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    news_item_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("news_items.id"), nullable=True, index=True
    )
    content_piece_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("content_pieces.id"), nullable=True, index=True
    )
    distribution_plan_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("distribution_plans.id"), nullable=True, index=True
    )
    publication_record_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("publication_records.id"), nullable=True, index=True
    )
    workflow_run_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("workflow_runs.id"), nullable=True, index=True
    )
    workflow_task_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("workflow_tasks.id"), nullable=True, index=True
    )
    agent_execution_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("agent_executions.id"), nullable=True, index=True
    )
    agent_output_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("agent_outputs.id"), nullable=True, index=True
    )
    metric_category: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    channel: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    measurement_window: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    metric_name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)
    snapshot_payload: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    source_or_origin: Mapped[str] = mapped_column(Text, nullable=False)
    data_quality: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
