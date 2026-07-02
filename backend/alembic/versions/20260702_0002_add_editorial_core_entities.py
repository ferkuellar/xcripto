"""add editorial core entities

Revision ID: 20260702_0002
Revises: 20260702_0001
Create Date: 2026-07-02
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260702_0002"
down_revision: str | None = "20260702_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "verification_records",
        sa.Column("news_item_id", sa.String(length=36), nullable=False),
        sa.Column("verification_status", sa.String(length=40), nullable=False),
        sa.Column("evidence_level", sa.String(length=20), nullable=False),
        sa.Column("confidence_level", sa.String(length=20), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("verified_claims", sa.JSON(), nullable=False),
        sa.Column("unverified_claims", sa.JSON(), nullable=False),
        sa.Column("contradictions", sa.JSON(), nullable=False),
        sa.Column("source_refs", sa.JSON(), nullable=False),
        sa.Column("human_review_required", sa.Boolean(), nullable=False),
        sa.Column("reviewer", sa.String(length=120), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["news_item_id"], ["news_items.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_verification_records_correlation_id"),
        "verification_records",
        ["correlation_id"],
    )
    op.create_index(
        op.f("ix_verification_records_news_item_id"),
        "verification_records",
        ["news_item_id"],
    )
    op.create_index(
        op.f("ix_verification_records_verification_status"),
        "verification_records",
        ["verification_status"],
    )

    op.create_table(
        "risk_reviews",
        sa.Column("news_item_id", sa.String(length=36), nullable=False),
        sa.Column("entity_type", sa.String(length=80), nullable=False),
        sa.Column("entity_id", sa.String(length=80), nullable=False),
        sa.Column("risk_level", sa.String(length=40), nullable=False),
        sa.Column("severity", sa.String(length=40), nullable=False),
        sa.Column("decision_recommendation", sa.String(length=80), nullable=False),
        sa.Column("risk_flags", sa.JSON(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("required_disclaimers", sa.JSON(), nullable=False),
        sa.Column("language_restrictions", sa.JSON(), nullable=False),
        sa.Column("human_review_required", sa.Boolean(), nullable=False),
        sa.Column("publication_block_recommended", sa.Boolean(), nullable=False),
        sa.Column("reviewer", sa.String(length=120), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["news_item_id"], ["news_items.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_risk_reviews_correlation_id"), "risk_reviews", ["correlation_id"])
    op.create_index(op.f("ix_risk_reviews_entity_id"), "risk_reviews", ["entity_id"])
    op.create_index(op.f("ix_risk_reviews_entity_type"), "risk_reviews", ["entity_type"])
    op.create_index(op.f("ix_risk_reviews_news_item_id"), "risk_reviews", ["news_item_id"])

    op.create_table(
        "content_pieces",
        sa.Column("news_item_id", sa.String(length=36), nullable=False),
        sa.Column("content_type", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=280), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("priority", sa.String(length=2), nullable=False),
        sa.Column("verification_status", sa.String(length=40), nullable=False),
        sa.Column("risk_level", sa.String(length=40), nullable=False),
        sa.Column("source_refs", sa.JSON(), nullable=False),
        sa.Column("disclaimer_required", sa.Boolean(), nullable=False),
        sa.Column("human_review_required", sa.Boolean(), nullable=False),
        sa.Column("owner", sa.String(length=120), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["news_item_id"], ["news_items.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_content_pieces_content_type"), "content_pieces", ["content_type"])
    op.create_index(
        op.f("ix_content_pieces_correlation_id"), "content_pieces", ["correlation_id"]
    )
    op.create_index(op.f("ix_content_pieces_news_item_id"), "content_pieces", ["news_item_id"])
    op.create_index(op.f("ix_content_pieces_priority"), "content_pieces", ["priority"])
    op.create_index(op.f("ix_content_pieces_status"), "content_pieces", ["status"])

    op.create_table(
        "distribution_plans",
        sa.Column("content_piece_id", sa.String(length=36), nullable=False),
        sa.Column("news_item_id", sa.String(length=36), nullable=False),
        sa.Column("primary_channel", sa.String(length=80), nullable=False),
        sa.Column("secondary_channels", sa.JSON(), nullable=False),
        sa.Column("distribution_type", sa.String(length=80), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("owner", sa.String(length=120), nullable=True),
        sa.Column("dependencies", sa.JSON(), nullable=False),
        sa.Column("metric_plan", sa.JSON(), nullable=False),
        sa.Column("risk_level", sa.String(length=40), nullable=False),
        sa.Column("publication_readiness", sa.String(length=80), nullable=False),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["content_piece_id"], ["content_pieces.id"]),
        sa.ForeignKeyConstraint(["news_item_id"], ["news_items.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_distribution_plans_content_piece_id"),
        "distribution_plans",
        ["content_piece_id"],
    )
    op.create_index(
        op.f("ix_distribution_plans_correlation_id"),
        "distribution_plans",
        ["correlation_id"],
    )
    op.create_index(
        op.f("ix_distribution_plans_news_item_id"), "distribution_plans", ["news_item_id"]
    )
    op.create_index(
        op.f("ix_distribution_plans_primary_channel"),
        "distribution_plans",
        ["primary_channel"],
    )
    op.create_index(op.f("ix_distribution_plans_status"), "distribution_plans", ["status"])

    op.create_table(
        "publication_records",
        sa.Column("content_piece_id", sa.String(length=36), nullable=False),
        sa.Column("distribution_plan_id", sa.String(length=36), nullable=False),
        sa.Column("news_item_id", sa.String(length=36), nullable=False),
        sa.Column("channel", sa.String(length=80), nullable=False),
        sa.Column("publication_status", sa.String(length=40), nullable=False),
        sa.Column("published_url", sa.String(length=2048), nullable=True),
        sa.Column("external_id", sa.String(length=180), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("owner", sa.String(length=120), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["content_piece_id"], ["content_pieces.id"]),
        sa.ForeignKeyConstraint(["distribution_plan_id"], ["distribution_plans.id"]),
        sa.ForeignKeyConstraint(["news_item_id"], ["news_items.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_publication_records_channel"), "publication_records", ["channel"]
    )
    op.create_index(
        op.f("ix_publication_records_content_piece_id"),
        "publication_records",
        ["content_piece_id"],
    )
    op.create_index(
        op.f("ix_publication_records_correlation_id"),
        "publication_records",
        ["correlation_id"],
    )
    op.create_index(
        op.f("ix_publication_records_distribution_plan_id"),
        "publication_records",
        ["distribution_plan_id"],
    )
    op.create_index(
        op.f("ix_publication_records_news_item_id"),
        "publication_records",
        ["news_item_id"],
    )
    op.create_index(
        op.f("ix_publication_records_publication_status"),
        "publication_records",
        ["publication_status"],
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_publication_records_publication_status"), table_name="publication_records"
    )
    op.drop_index(op.f("ix_publication_records_news_item_id"), table_name="publication_records")
    op.drop_index(
        op.f("ix_publication_records_distribution_plan_id"),
        table_name="publication_records",
    )
    op.drop_index(op.f("ix_publication_records_correlation_id"), table_name="publication_records")
    op.drop_index(op.f("ix_publication_records_content_piece_id"), table_name="publication_records")
    op.drop_index(op.f("ix_publication_records_channel"), table_name="publication_records")
    op.drop_table("publication_records")

    op.drop_index(op.f("ix_distribution_plans_status"), table_name="distribution_plans")
    op.drop_index(op.f("ix_distribution_plans_primary_channel"), table_name="distribution_plans")
    op.drop_index(op.f("ix_distribution_plans_news_item_id"), table_name="distribution_plans")
    op.drop_index(op.f("ix_distribution_plans_correlation_id"), table_name="distribution_plans")
    op.drop_index(op.f("ix_distribution_plans_content_piece_id"), table_name="distribution_plans")
    op.drop_table("distribution_plans")

    op.drop_index(op.f("ix_content_pieces_status"), table_name="content_pieces")
    op.drop_index(op.f("ix_content_pieces_priority"), table_name="content_pieces")
    op.drop_index(op.f("ix_content_pieces_news_item_id"), table_name="content_pieces")
    op.drop_index(op.f("ix_content_pieces_correlation_id"), table_name="content_pieces")
    op.drop_index(op.f("ix_content_pieces_content_type"), table_name="content_pieces")
    op.drop_table("content_pieces")

    op.drop_index(op.f("ix_risk_reviews_news_item_id"), table_name="risk_reviews")
    op.drop_index(op.f("ix_risk_reviews_entity_type"), table_name="risk_reviews")
    op.drop_index(op.f("ix_risk_reviews_entity_id"), table_name="risk_reviews")
    op.drop_index(op.f("ix_risk_reviews_correlation_id"), table_name="risk_reviews")
    op.drop_table("risk_reviews")

    op.drop_index(
        op.f("ix_verification_records_verification_status"),
        table_name="verification_records",
    )
    op.drop_index(op.f("ix_verification_records_news_item_id"), table_name="verification_records")
    op.drop_index(op.f("ix_verification_records_correlation_id"), table_name="verification_records")
    op.drop_table("verification_records")
