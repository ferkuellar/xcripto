"""add workflow task queue

Revision ID: 20260702_0005
Revises: 20260702_0004
Create Date: 2026-07-02
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260702_0005"
down_revision: str | None = "20260702_0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "workflow_tasks",
        sa.Column("workflow_run_id", sa.String(length=36), nullable=False),
        sa.Column("workflow_step_id", sa.String(length=36), nullable=True),
        sa.Column("news_item_id", sa.String(length=36), nullable=True),
        sa.Column("task_type", sa.String(length=80), nullable=False),
        sa.Column("task_status", sa.String(length=40), nullable=False),
        sa.Column("priority", sa.String(length=2), nullable=False),
        sa.Column("assigned_agent", sa.String(length=120), nullable=False),
        sa.Column("assigned_to", sa.String(length=120), nullable=True),
        sa.Column("title", sa.String(length=280), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("input_payload", sa.JSON(), nullable=True),
        sa.Column("output_ref", sa.String(length=180), nullable=True),
        sa.Column("agent_execution_id", sa.String(length=36), nullable=True),
        sa.Column("agent_output_id", sa.String(length=36), nullable=True),
        sa.Column("blocking", sa.Boolean(), nullable=False),
        sa.Column("blocking_reason", sa.Text(), nullable=True),
        sa.Column("attempt_count", sa.Integer(), nullable=False),
        sa.Column("max_attempts", sa.Integer(), nullable=False),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("failed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["agent_execution_id"], ["agent_executions.id"]),
        sa.ForeignKeyConstraint(["agent_output_id"], ["agent_outputs.id"]),
        sa.ForeignKeyConstraint(["news_item_id"], ["news_items.id"]),
        sa.ForeignKeyConstraint(["workflow_run_id"], ["workflow_runs.id"]),
        sa.ForeignKeyConstraint(["workflow_step_id"], ["workflow_steps.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_workflow_tasks_agent_execution_id"), "workflow_tasks", ["agent_execution_id"]
    )
    op.create_index(
        op.f("ix_workflow_tasks_agent_output_id"), "workflow_tasks", ["agent_output_id"]
    )
    op.create_index(op.f("ix_workflow_tasks_assigned_agent"), "workflow_tasks", ["assigned_agent"])
    op.create_index(op.f("ix_workflow_tasks_assigned_to"), "workflow_tasks", ["assigned_to"])
    op.create_index(op.f("ix_workflow_tasks_blocking"), "workflow_tasks", ["blocking"])
    op.create_index(op.f("ix_workflow_tasks_correlation_id"), "workflow_tasks", ["correlation_id"])
    op.create_index(op.f("ix_workflow_tasks_created_at"), "workflow_tasks", ["created_at"])
    op.create_index(op.f("ix_workflow_tasks_news_item_id"), "workflow_tasks", ["news_item_id"])
    op.create_index(op.f("ix_workflow_tasks_priority"), "workflow_tasks", ["priority"])
    op.create_index(op.f("ix_workflow_tasks_task_status"), "workflow_tasks", ["task_status"])
    op.create_index(op.f("ix_workflow_tasks_task_type"), "workflow_tasks", ["task_type"])
    op.create_index(
        op.f("ix_workflow_tasks_workflow_run_id"), "workflow_tasks", ["workflow_run_id"]
    )
    op.create_index(
        op.f("ix_workflow_tasks_workflow_step_id"), "workflow_tasks", ["workflow_step_id"]
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_workflow_tasks_workflow_step_id"), table_name="workflow_tasks")
    op.drop_index(op.f("ix_workflow_tasks_workflow_run_id"), table_name="workflow_tasks")
    op.drop_index(op.f("ix_workflow_tasks_task_type"), table_name="workflow_tasks")
    op.drop_index(op.f("ix_workflow_tasks_task_status"), table_name="workflow_tasks")
    op.drop_index(op.f("ix_workflow_tasks_priority"), table_name="workflow_tasks")
    op.drop_index(op.f("ix_workflow_tasks_news_item_id"), table_name="workflow_tasks")
    op.drop_index(op.f("ix_workflow_tasks_created_at"), table_name="workflow_tasks")
    op.drop_index(op.f("ix_workflow_tasks_correlation_id"), table_name="workflow_tasks")
    op.drop_index(op.f("ix_workflow_tasks_blocking"), table_name="workflow_tasks")
    op.drop_index(op.f("ix_workflow_tasks_assigned_to"), table_name="workflow_tasks")
    op.drop_index(op.f("ix_workflow_tasks_assigned_agent"), table_name="workflow_tasks")
    op.drop_index(op.f("ix_workflow_tasks_agent_output_id"), table_name="workflow_tasks")
    op.drop_index(op.f("ix_workflow_tasks_agent_execution_id"), table_name="workflow_tasks")
    op.drop_table("workflow_tasks")
