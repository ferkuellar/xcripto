"""add operational audit log

Revision ID: 20260702_0010
Revises: 20260702_0009
Create Date: 2026-07-02
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260702_0010"
down_revision: str | None = "20260702_0009"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "operational_audit_logs",
        sa.Column("event_type", sa.String(length=60), nullable=False),
        sa.Column("action", sa.String(length=120), nullable=False),
        sa.Column("permission", sa.String(length=120), nullable=True),
        sa.Column("actor_id", sa.String(length=120), nullable=True),
        sa.Column("actor_role", sa.String(length=60), nullable=True),
        sa.Column("actor_display", sa.String(length=180), nullable=True),
        sa.Column("actor_source", sa.String(length=40), nullable=True),
        sa.Column("request_method", sa.String(length=12), nullable=True),
        sa.Column("request_path", sa.String(length=500), nullable=True),
        sa.Column("entity_type", sa.String(length=120), nullable=True),
        sa.Column("entity_id", sa.String(length=120), nullable=True),
        sa.Column("news_item_id", sa.String(length=36), nullable=True),
        sa.Column("workflow_run_id", sa.String(length=36), nullable=True),
        sa.Column("workflow_task_id", sa.String(length=36), nullable=True),
        sa.Column("agent_output_id", sa.String(length=36), nullable=True),
        sa.Column("ownership_id", sa.String(length=36), nullable=True),
        sa.Column("user_id", sa.String(length=36), nullable=True),
        sa.Column("outcome", sa.String(length=40), nullable=False),
        sa.Column("decision", sa.String(length=40), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("before_state", sa.JSON(), nullable=True),
        sa.Column("after_state", sa.JSON(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("error_code", sa.String(length=80), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    for index_name, column in [
        ("ix_operational_audit_logs_event_type", "event_type"),
        ("ix_operational_audit_logs_action", "action"),
        ("ix_operational_audit_logs_permission", "permission"),
        ("ix_operational_audit_logs_actor_id", "actor_id"),
        ("ix_operational_audit_logs_actor_role", "actor_role"),
        ("ix_operational_audit_logs_entity_type", "entity_type"),
        ("ix_operational_audit_logs_entity_id", "entity_id"),
        ("ix_operational_audit_logs_news_item_id", "news_item_id"),
        ("ix_operational_audit_logs_workflow_run_id", "workflow_run_id"),
        ("ix_operational_audit_logs_workflow_task_id", "workflow_task_id"),
        ("ix_operational_audit_logs_agent_output_id", "agent_output_id"),
        ("ix_operational_audit_logs_ownership_id", "ownership_id"),
        ("ix_operational_audit_logs_user_id", "user_id"),
        ("ix_operational_audit_logs_outcome", "outcome"),
        ("ix_operational_audit_logs_decision", "decision"),
        ("ix_operational_audit_logs_correlation_id", "correlation_id"),
        ("ix_operational_audit_logs_created_at", "created_at"),
    ]:
        op.create_index(op.f(index_name), "operational_audit_logs", [column])


def downgrade() -> None:
    for index_name in [
        "ix_operational_audit_logs_created_at",
        "ix_operational_audit_logs_correlation_id",
        "ix_operational_audit_logs_decision",
        "ix_operational_audit_logs_outcome",
        "ix_operational_audit_logs_user_id",
        "ix_operational_audit_logs_ownership_id",
        "ix_operational_audit_logs_agent_output_id",
        "ix_operational_audit_logs_workflow_task_id",
        "ix_operational_audit_logs_workflow_run_id",
        "ix_operational_audit_logs_news_item_id",
        "ix_operational_audit_logs_entity_id",
        "ix_operational_audit_logs_entity_type",
        "ix_operational_audit_logs_actor_role",
        "ix_operational_audit_logs_actor_id",
        "ix_operational_audit_logs_permission",
        "ix_operational_audit_logs_action",
        "ix_operational_audit_logs_event_type",
    ]:
        op.drop_index(op.f(index_name), table_name="operational_audit_logs")
    op.drop_table("operational_audit_logs")
