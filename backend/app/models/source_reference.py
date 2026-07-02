from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class SourceReference(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "source_references"

    source_name: Mapped[str] = mapped_column(String(180), nullable=False, index=True)
    source_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    source_type: Mapped[str] = mapped_column(String(80), nullable=False)
    source_status: Mapped[str] = mapped_column(String(40), nullable=False, default="proposed")
    trust_level: Mapped[str] = mapped_column(String(10), nullable=False, default="T2")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)

