from sqlalchemy import JSON, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class AuditCheck(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "audit_checks"

    entity_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    audit_status: Mapped[str] = mapped_column(String(40), nullable=False, default="pending")
    severity: Mapped[str] = mapped_column(String(40), nullable=False, default="medium")
    decision_recommendation: Mapped[str | None] = mapped_column(String(240), nullable=True)
    ready_to_advance: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    publication_block_recommended: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    missing_requirements: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    audit_flags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
