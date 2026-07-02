"""add agent output storage

Revision ID: 20260702_0004
Revises: 20260702_0003
Create Date: 2026-07-02
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260702_0004"
down_revision: str | None = "20260702_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "agent_outputs",
        sa.Column("agent_execution_id", sa.String(length=36), nullable=True),
        sa.Column("agent_name", sa.String(length=120), nullable=False),
        sa.Column("agent_version", sa.String(length=40), nullable=True),
        sa.Column("output_type", sa.String(length=80), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("entity_type", sa.String(length=80), nullable=True),
        sa.Column("entity_id", sa.String(length=80), nullable=True),
        sa.Column("news_item_id", sa.String(length=36), nullable=True),
        sa.Column("workflow_run_id", sa.String(length=36), nullable=True),
        sa.Column("workflow_step_id", sa.String(length=36), nullable=True),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("risk_flags", sa.JSON(), nullable=False),
        sa.Column("missing_requirements", sa.JSON(), nullable=False),
        sa.Column("next_agent", sa.String(length=80), nullable=True),
        sa.Column("human_review_required", sa.Boolean(), nullable=False),
        sa.Column("accepted", sa.Boolean(), nullable=False),
        sa.Column("accepted_by", sa.String(length=120), nullable=True),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rejected_reason", sa.Text(), nullable=True),
        sa.Column("superseded_by_output_id", sa.String(length=36), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["agent_execution_id"], ["agent_executions.id"]),
        sa.ForeignKeyConstraint(["news_item_id"], ["news_items.id"]),
        sa.ForeignKeyConstraint(["superseded_by_output_id"], ["agent_outputs.id"]),
        sa.ForeignKeyConstraint(["workflow_run_id"], ["workflow_runs.id"]),
        sa.ForeignKeyConstraint(["workflow_step_id"], ["workflow_steps.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_agent_outputs_agent_execution_id"),
        "agent_outputs",
        ["agent_execution_id"],
    )
    op.create_index(op.f("ix_agent_outputs_agent_name"), "agent_outputs", ["agent_name"])
    op.create_index(op.f("ix_agent_outputs_correlation_id"), "agent_outputs", ["correlation_id"])
    op.create_index(op.f("ix_agent_outputs_created_at"), "agent_outputs", ["created_at"])
    op.create_index(op.f("ix_agent_outputs_entity_id"), "agent_outputs", ["entity_id"])
    op.create_index(op.f("ix_agent_outputs_entity_type"), "agent_outputs", ["entity_type"])
    op.create_index(op.f("ix_agent_outputs_news_item_id"), "agent_outputs", ["news_item_id"])
    op.create_index(op.f("ix_agent_outputs_output_type"), "agent_outputs", ["output_type"])
    op.create_index(op.f("ix_agent_outputs_status"), "agent_outputs", ["status"])
    op.create_index(op.f("ix_agent_outputs_workflow_run_id"), "agent_outputs", ["workflow_run_id"])
    op.create_index(
        op.f("ix_agent_outputs_workflow_step_id"),
        "agent_outputs",
        ["workflow_step_id"],
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_agent_outputs_workflow_step_id"), table_name="agent_outputs")
    op.drop_index(op.f("ix_agent_outputs_workflow_run_id"), table_name="agent_outputs")
    op.drop_index(op.f("ix_agent_outputs_status"), table_name="agent_outputs")
    op.drop_index(op.f("ix_agent_outputs_output_type"), table_name="agent_outputs")
    op.drop_index(op.f("ix_agent_outputs_news_item_id"), table_name="agent_outputs")
    op.drop_index(op.f("ix_agent_outputs_entity_type"), table_name="agent_outputs")
    op.drop_index(op.f("ix_agent_outputs_entity_id"), table_name="agent_outputs")
    op.drop_index(op.f("ix_agent_outputs_created_at"), table_name="agent_outputs")
    op.drop_index(op.f("ix_agent_outputs_correlation_id"), table_name="agent_outputs")
    op.drop_index(op.f("ix_agent_outputs_agent_name"), table_name="agent_outputs")
    op.drop_index(op.f("ix_agent_outputs_agent_execution_id"), table_name="agent_outputs")
    op.drop_table("agent_outputs")
