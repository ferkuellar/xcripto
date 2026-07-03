from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class KnowledgeEdge(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "knowledge_edges"

    source_node_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("knowledge_nodes.id"), nullable=False, index=True
    )
    target_node_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("knowledge_nodes.id"), nullable=False, index=True
    )
    relationship_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    scope: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    confidence_level: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="proposed", index=True)
    risk_flags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    metadata_json: Mapped[dict | list | None] = mapped_column("metadata", JSON, nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
