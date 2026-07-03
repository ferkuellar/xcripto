"""add editorial readiness scores

Revision ID: 20260702_0007
Revises: 20260702_0006
Create Date: 2026-07-02
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260702_0007"
down_revision: str | None = "20260702_0006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "editorial_readiness_scores",
        sa.Column("news_item_id", sa.String(length=36), nullable=False),
        sa.Column("workflow_run_id", sa.String(length=36), nullable=True),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("score_band", sa.String(length=40), nullable=False),
        sa.Column("readiness_status", sa.String(length=40), nullable=False),
        sa.Column("source_score", sa.Float(), nullable=False),
        sa.Column("verification_score", sa.Float(), nullable=False),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("editorial_score", sa.Float(), nullable=False),
        sa.Column("audit_score", sa.Float(), nullable=False),
        sa.Column("workflow_score", sa.Float(), nullable=False),
        sa.Column("task_score", sa.Float(), nullable=False),
        sa.Column("agent_output_score", sa.Float(), nullable=False),
        sa.Column("distribution_score", sa.Float(), nullable=False),
        sa.Column("publication_score", sa.Float(), nullable=False),
        sa.Column("metrics_score", sa.Float(), nullable=False),
        sa.Column("memory_score", sa.Float(), nullable=False),
        sa.Column("knowledge_score", sa.Float(), nullable=False),
        sa.Column("blocking_reasons", sa.JSON(), nullable=False),
        sa.Column("missing_requirements", sa.JSON(), nullable=False),
        sa.Column("warnings", sa.JSON(), nullable=False),
        sa.Column("recommended_next_action", sa.Text(), nullable=True),
        sa.Column("next_agent", sa.String(length=80), nullable=False),
        sa.Column("human_review_required", sa.Boolean(), nullable=False),
        sa.Column("publication_block_recommended", sa.Boolean(), nullable=False),
        sa.Column("score_payload", sa.JSON(), nullable=False),
        sa.Column("calculated_by", sa.String(length=80), nullable=False),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["news_item_id"], ["news_items.id"]),
        sa.ForeignKeyConstraint(["workflow_run_id"], ["workflow_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    indexes = [
        ("ix_editorial_readiness_scores_correlation_id", "correlation_id"),
        ("ix_editorial_readiness_scores_created_at", "created_at"),
        ("ix_editorial_readiness_scores_human_review_required", "human_review_required"),
        ("ix_editorial_readiness_scores_news_item_id", "news_item_id"),
        ("ix_editorial_readiness_scores_next_agent", "next_agent"),
        (
            "ix_editorial_readiness_scores_publication_block_recommended",
            "publication_block_recommended",
        ),
        ("ix_editorial_readiness_scores_readiness_status", "readiness_status"),
        ("ix_editorial_readiness_scores_score_band", "score_band"),
        ("ix_editorial_readiness_scores_workflow_run_id", "workflow_run_id"),
    ]
    for index_name, column in indexes:
        op.create_index(op.f(index_name), "editorial_readiness_scores", [column])


def downgrade() -> None:
    for index_name in [
        "ix_editorial_readiness_scores_workflow_run_id",
        "ix_editorial_readiness_scores_score_band",
        "ix_editorial_readiness_scores_readiness_status",
        "ix_editorial_readiness_scores_publication_block_recommended",
        "ix_editorial_readiness_scores_next_agent",
        "ix_editorial_readiness_scores_news_item_id",
        "ix_editorial_readiness_scores_human_review_required",
        "ix_editorial_readiness_scores_created_at",
        "ix_editorial_readiness_scores_correlation_id",
    ]:
        op.drop_index(op.f(index_name), table_name="editorial_readiness_scores")
    op.drop_table("editorial_readiness_scores")
