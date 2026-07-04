from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class ExternalConnector(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "external_connectors"

    connector_name: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    connector_type: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    connector_status: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    provider: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    base_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    capabilities: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    configuration: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    secret_ref: Mapped[str | None] = mapped_column(String(240), nullable=True)
    auth_type: Mapped[str] = mapped_column(String(60), nullable=False, default="none")
    rate_limit_policy: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    dry_run_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    last_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_success_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_failure_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
