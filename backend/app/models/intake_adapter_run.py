from datetime import datetime

from sqlalchemy import JSON, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class IntakeAdapterRun(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "intake_adapter_runs"

    adapter_name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    adapter_version: Mapped[str | None] = mapped_column(String(40), nullable=True)
    adapter_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="created", index=True)
    input_payload: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    result_payload: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    signals_created_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    signals_duplicate_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    signals_error_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
