from sqlalchemy import JSON, Boolean, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class EditorialReadinessScore(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "editorial_readiness_scores"

    news_item_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("news_items.id"), nullable=False, index=True
    )
    workflow_run_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("workflow_runs.id"), nullable=True, index=True
    )
    score: Mapped[float] = mapped_column(Float, nullable=False)
    score_band: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    readiness_status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    source_score: Mapped[float] = mapped_column(Float, nullable=False)
    verification_score: Mapped[float] = mapped_column(Float, nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    editorial_score: Mapped[float] = mapped_column(Float, nullable=False)
    audit_score: Mapped[float] = mapped_column(Float, nullable=False)
    workflow_score: Mapped[float] = mapped_column(Float, nullable=False)
    task_score: Mapped[float] = mapped_column(Float, nullable=False)
    agent_output_score: Mapped[float] = mapped_column(Float, nullable=False)
    distribution_score: Mapped[float] = mapped_column(Float, nullable=False)
    publication_score: Mapped[float] = mapped_column(Float, nullable=False)
    metrics_score: Mapped[float] = mapped_column(Float, nullable=False)
    memory_score: Mapped[float] = mapped_column(Float, nullable=False)
    knowledge_score: Mapped[float] = mapped_column(Float, nullable=False)
    blocking_reasons: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    missing_requirements: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    warnings: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    recommended_next_action: Mapped[str | None] = mapped_column(Text, nullable=True)
    next_agent: Mapped[str] = mapped_column(String(80), nullable=False, default="None", index=True)
    human_review_required: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, index=True
    )
    publication_block_recommended: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, index=True
    )
    score_payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    calculated_by: Mapped[str] = mapped_column(String(80), nullable=False, default="system")
    correlation_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
