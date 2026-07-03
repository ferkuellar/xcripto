from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class KnowledgeNode(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "knowledge_nodes"

    node_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    label: Mapped[str] = mapped_column(String(280), nullable=False, index=True)
    external_ref: Mapped[str | None] = mapped_column(String(180), nullable=True, index=True)
    entity_type: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    entity_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    confidence_level: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="proposed", index=True)
    source_or_origin: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[dict | list | None] = mapped_column("metadata", JSON, nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
