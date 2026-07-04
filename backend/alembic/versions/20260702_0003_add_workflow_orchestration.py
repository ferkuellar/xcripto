"""add workflow orchestration

Revision ID: 20260702_0003
Revises: 20260702_0002
Create Date: 2026-07-02
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260702_0003"
down_revision: str | None = "20260702_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "workflow_runs",
        sa.Column("news_item_id", sa.String(length=36), nullable=False),
        sa.Column("workflow_type", sa.String(length=80), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("current_step", sa.String(length=80), nullable=False),
        sa.Column("readiness_status", sa.String(length=40), nullable=False),
        sa.Column("blocked", sa.Boolean(), nullable=False),
        sa.Column("blocking_reasons", sa.JSON(), nullable=False),
        sa.Column("missing_requirements", sa.JSON(), nullable=False),
        sa.Column("recommended_next_action", sa.Text(), nullable=True),
        sa.Column("next_agent", sa.String(length=80), nullable=False),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["news_item_id"], ["news_items.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_workflow_runs_correlation_id"), "workflow_runs", ["correlation_id"])
    op.create_index(op.f("ix_workflow_runs_news_item_id"), "workflow_runs", ["news_item_id"])
    op.create_index(
        op.f("ix_workflow_runs_readiness_status"), "workflow_runs", ["readiness_status"]
    )
    op.create_index(op.f("ix_workflow_runs_status"), "workflow_runs", ["status"])
    op.create_index(
        op.f("ix_workflow_runs_workflow_type"), "workflow_runs", ["workflow_type"]
    )

    op.create_table(
        "workflow_steps",
        sa.Column("workflow_run_id", sa.String(length=36), nullable=False),
        sa.Column("step_name", sa.String(length=80), nullable=False),
        sa.Column("step_status", sa.String(length=40), nullable=False),
        sa.Column("required", sa.Boolean(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.Column("entity_type", sa.String(length=80), nullable=True),
        sa.Column("entity_id", sa.String(length=80), nullable=True),
        sa.Column("blocking", sa.Boolean(), nullable=False),
        sa.Column("blocking_reason", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["workflow_run_id"], ["workflow_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_workflow_steps_correlation_id"), "workflow_steps", ["correlation_id"]
    )
    op.create_index(op.f("ix_workflow_steps_step_name"), "workflow_steps", ["step_name"])
    op.create_index(
        op.f("ix_workflow_steps_workflow_run_id"), "workflow_steps", ["workflow_run_id"]
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_workflow_steps_workflow_run_id"), table_name="workflow_steps")
    op.drop_index(op.f("ix_workflow_steps_step_name"), table_name="workflow_steps")
    op.drop_index(op.f("ix_workflow_steps_correlation_id"), table_name="workflow_steps")
    op.drop_table("workflow_steps")

    op.drop_index(op.f("ix_workflow_runs_workflow_type"), table_name="workflow_runs")
    op.drop_index(op.f("ix_workflow_runs_status"), table_name="workflow_runs")
    op.drop_index(op.f("ix_workflow_runs_readiness_status"), table_name="workflow_runs")
    op.drop_index(op.f("ix_workflow_runs_news_item_id"), table_name="workflow_runs")
    op.drop_index(op.f("ix_workflow_runs_correlation_id"), table_name="workflow_runs")
    op.drop_table("workflow_runs")
