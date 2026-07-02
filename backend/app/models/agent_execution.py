from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class AgentExecution(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "agent_executions"

    agent_name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    agent_version: Mapped[str] = mapped_column(String(40), nullable=False)
    input_ref: Mapped[str | None] = mapped_column(String(180), nullable=True)
    output_ref: Mapped[str | None] = mapped_column(String(180), nullable=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="queued", index=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)

