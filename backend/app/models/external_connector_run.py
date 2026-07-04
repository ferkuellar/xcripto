from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class ExternalConnectorRun(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "external_connector_runs"

    connector_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("external_connectors.id"), nullable=False, index=True
    )
    run_type: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    run_status: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    triggered_by: Mapped[str | None] = mapped_column(String(120), nullable=True)
    input_payload: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    result_payload: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    signals_created_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    agent_outputs_created_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    publication_records_created_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    metric_snapshots_created_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
