from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class OperationalAuditLog(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "operational_audit_logs"

    event_type: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    permission: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    actor_id: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    actor_role: Mapped[str | None] = mapped_column(String(60), nullable=True, index=True)
    actor_display: Mapped[str | None] = mapped_column(String(180), nullable=True)
    actor_source: Mapped[str | None] = mapped_column(String(40), nullable=True)
    request_method: Mapped[str | None] = mapped_column(String(12), nullable=True)
    request_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    entity_type: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    entity_id: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    news_item_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    workflow_run_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    workflow_task_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    agent_output_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    ownership_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    user_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    outcome: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    decision: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    before_state: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    after_state: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    event_metadata: Mapped[dict | list | None] = mapped_column("metadata", JSON, nullable=True)
    error_code: Mapped[str | None] = mapped_column(String(80), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
