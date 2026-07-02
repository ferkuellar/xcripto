"""initial schema

Revision ID: 20260702_0001
Revises:
Create Date: 2026-07-02
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260702_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "agent_executions",
        sa.Column("agent_name", sa.String(length=120), nullable=False),
        sa.Column("agent_version", sa.String(length=40), nullable=False),
        sa.Column("input_ref", sa.String(length=180), nullable=True),
        sa.Column("output_ref", sa.String(length=180), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_agent_executions_agent_name"), "agent_executions", ["agent_name"])
    op.create_index(
        op.f("ix_agent_executions_correlation_id"), "agent_executions", ["correlation_id"]
    )
    op.create_index(op.f("ix_agent_executions_status"), "agent_executions", ["status"])

    op.create_table(
        "audit_checks",
        sa.Column("entity_type", sa.String(length=80), nullable=False),
        sa.Column("entity_id", sa.String(length=80), nullable=False),
        sa.Column("audit_status", sa.String(length=40), nullable=False),
        sa.Column("severity", sa.String(length=40), nullable=False),
        sa.Column("decision_recommendation", sa.String(length=240), nullable=True),
        sa.Column("ready_to_advance", sa.Boolean(), nullable=False),
        sa.Column("publication_block_recommended", sa.Boolean(), nullable=False),
        sa.Column("missing_requirements", sa.JSON(), nullable=False),
        sa.Column("audit_flags", sa.JSON(), nullable=False),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_audit_checks_correlation_id"), "audit_checks", ["correlation_id"])
    op.create_index(op.f("ix_audit_checks_entity_id"), "audit_checks", ["entity_id"])
    op.create_index(op.f("ix_audit_checks_entity_type"), "audit_checks", ["entity_type"])

    op.create_table(
        "news_items",
        sa.Column("title", sa.String(length=280), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("priority", sa.String(length=2), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("source_url", sa.String(length=2048), nullable=False),
        sa.Column("source_name", sa.String(length=180), nullable=False),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_news_items_correlation_id"), "news_items", ["correlation_id"])
    op.create_index(op.f("ix_news_items_priority"), "news_items", ["priority"])
    op.create_index(op.f("ix_news_items_status"), "news_items", ["status"])

    op.create_table(
        "source_references",
        sa.Column("source_name", sa.String(length=180), nullable=False),
        sa.Column("source_url", sa.String(length=2048), nullable=False),
        sa.Column("source_type", sa.String(length=80), nullable=False),
        sa.Column("source_status", sa.String(length=40), nullable=False),
        sa.Column("trust_level", sa.String(length=10), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_source_references_correlation_id"), "source_references", ["correlation_id"]
    )
    op.create_index(op.f("ix_source_references_source_name"), "source_references", ["source_name"])


def downgrade() -> None:
    op.drop_index(op.f("ix_source_references_source_name"), table_name="source_references")
    op.drop_index(op.f("ix_source_references_correlation_id"), table_name="source_references")
    op.drop_table("source_references")

    op.drop_index(op.f("ix_news_items_status"), table_name="news_items")
    op.drop_index(op.f("ix_news_items_priority"), table_name="news_items")
    op.drop_index(op.f("ix_news_items_correlation_id"), table_name="news_items")
    op.drop_table("news_items")

    op.drop_index(op.f("ix_audit_checks_entity_type"), table_name="audit_checks")
    op.drop_index(op.f("ix_audit_checks_entity_id"), table_name="audit_checks")
    op.drop_index(op.f("ix_audit_checks_correlation_id"), table_name="audit_checks")
    op.drop_table("audit_checks")

    op.drop_index(op.f("ix_agent_executions_status"), table_name="agent_executions")
    op.drop_index(op.f("ix_agent_executions_correlation_id"), table_name="agent_executions")
    op.drop_index(op.f("ix_agent_executions_agent_name"), table_name="agent_executions")
    op.drop_table("agent_executions")
