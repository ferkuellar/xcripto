"""add metrics memory and knowledge core

Revision ID: 20260702_0006
Revises: 20260702_0005
Create Date: 2026-07-02
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260702_0006"
down_revision: str | None = "20260702_0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "metric_snapshots",
        sa.Column("entity_type", sa.String(length=80), nullable=True),
        sa.Column("entity_id", sa.String(length=80), nullable=True),
        sa.Column("news_item_id", sa.String(length=36), nullable=True),
        sa.Column("content_piece_id", sa.String(length=36), nullable=True),
        sa.Column("distribution_plan_id", sa.String(length=36), nullable=True),
        sa.Column("publication_record_id", sa.String(length=36), nullable=True),
        sa.Column("workflow_run_id", sa.String(length=36), nullable=True),
        sa.Column("workflow_task_id", sa.String(length=36), nullable=True),
        sa.Column("agent_execution_id", sa.String(length=36), nullable=True),
        sa.Column("agent_output_id", sa.String(length=36), nullable=True),
        sa.Column("metric_category", sa.String(length=80), nullable=False),
        sa.Column("channel", sa.String(length=120), nullable=True),
        sa.Column("measurement_window", sa.String(length=20), nullable=False),
        sa.Column("metric_name", sa.String(length=120), nullable=False),
        sa.Column("metric_value", sa.Float(), nullable=False),
        sa.Column("snapshot_payload", sa.JSON(), nullable=True),
        sa.Column("source_or_origin", sa.Text(), nullable=False),
        sa.Column("data_quality", sa.String(length=20), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["agent_execution_id"], ["agent_executions.id"]),
        sa.ForeignKeyConstraint(["agent_output_id"], ["agent_outputs.id"]),
        sa.ForeignKeyConstraint(["content_piece_id"], ["content_pieces.id"]),
        sa.ForeignKeyConstraint(["distribution_plan_id"], ["distribution_plans.id"]),
        sa.ForeignKeyConstraint(["news_item_id"], ["news_items.id"]),
        sa.ForeignKeyConstraint(["publication_record_id"], ["publication_records.id"]),
        sa.ForeignKeyConstraint(["workflow_run_id"], ["workflow_runs.id"]),
        sa.ForeignKeyConstraint(["workflow_task_id"], ["workflow_tasks.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in [
        "agent_execution_id",
        "agent_output_id",
        "channel",
        "content_piece_id",
        "created_at",
        "correlation_id",
        "data_quality",
        "distribution_plan_id",
        "entity_id",
        "entity_type",
        "measurement_window",
        "metric_category",
        "metric_name",
        "news_item_id",
        "publication_record_id",
        "workflow_run_id",
        "workflow_task_id",
    ]:
        op.create_index(op.f(f"ix_metric_snapshots_{column}"), "metric_snapshots", [column])

    op.create_table(
        "memory_items",
        sa.Column("memory_type", sa.String(length=80), nullable=False),
        sa.Column("memory_status", sa.String(length=40), nullable=False),
        sa.Column("title", sa.String(length=280), nullable=False),
        sa.Column("memory_statement", sa.Text(), nullable=False),
        sa.Column("why_it_matters", sa.Text(), nullable=True),
        sa.Column("how_to_use", sa.Text(), nullable=True),
        sa.Column("how_not_to_use", sa.Text(), nullable=True),
        sa.Column("source_or_origin", sa.Text(), nullable=False),
        sa.Column("entity_type", sa.String(length=80), nullable=True),
        sa.Column("entity_id", sa.String(length=80), nullable=True),
        sa.Column("news_item_id", sa.String(length=36), nullable=True),
        sa.Column("workflow_run_id", sa.String(length=36), nullable=True),
        sa.Column("agent_output_id", sa.String(length=36), nullable=True),
        sa.Column("audit_check_id", sa.String(length=36), nullable=True),
        sa.Column("metric_snapshot_id", sa.String(length=36), nullable=True),
        sa.Column("confidence_level", sa.String(length=20), nullable=False),
        sa.Column("persistence_level", sa.String(length=20), nullable=False),
        sa.Column("scope", sa.String(length=40), nullable=False),
        sa.Column("risk_flags", sa.JSON(), nullable=False),
        sa.Column("expiration_recommendation", sa.String(length=40), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("human_review_required", sa.Boolean(), nullable=False),
        sa.Column("approved_by", sa.String(length=120), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("invalidated_by", sa.String(length=120), nullable=True),
        sa.Column("invalidated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("invalidation_reason", sa.Text(), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["agent_output_id"], ["agent_outputs.id"]),
        sa.ForeignKeyConstraint(["audit_check_id"], ["audit_checks.id"]),
        sa.ForeignKeyConstraint(["metric_snapshot_id"], ["metric_snapshots.id"]),
        sa.ForeignKeyConstraint(["news_item_id"], ["news_items.id"]),
        sa.ForeignKeyConstraint(["workflow_run_id"], ["workflow_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in [
        "agent_output_id",
        "approved_at",
        "confidence_level",
        "correlation_id",
        "created_at",
        "entity_id",
        "entity_type",
        "expiration_recommendation",
        "human_review_required",
        "invalidated_at",
        "memory_status",
        "memory_type",
        "news_item_id",
        "persistence_level",
        "scope",
        "workflow_run_id",
    ]:
        op.create_index(op.f(f"ix_memory_items_{column}"), "memory_items", [column])

    op.create_table(
        "knowledge_nodes",
        sa.Column("node_type", sa.String(length=80), nullable=False),
        sa.Column("label", sa.String(length=280), nullable=False),
        sa.Column("external_ref", sa.String(length=180), nullable=True),
        sa.Column("entity_type", sa.String(length=80), nullable=True),
        sa.Column("entity_id", sa.String(length=80), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("confidence_level", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("source_or_origin", sa.Text(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in [
        "confidence_level",
        "correlation_id",
        "created_at",
        "entity_id",
        "entity_type",
        "label",
        "node_type",
        "status",
    ]:
        op.create_index(op.f(f"ix_knowledge_nodes_{column}"), "knowledge_nodes", [column])

    op.create_table(
        "knowledge_edges",
        sa.Column("source_node_id", sa.String(length=36), nullable=False),
        sa.Column("target_node_id", sa.String(length=36), nullable=False),
        sa.Column("relationship_type", sa.String(length=80), nullable=False),
        sa.Column("scope", sa.String(length=40), nullable=False),
        sa.Column("confidence_level", sa.String(length=20), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("risk_flags", sa.JSON(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["source_node_id"], ["knowledge_nodes.id"]),
        sa.ForeignKeyConstraint(["target_node_id"], ["knowledge_nodes.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in [
        "confidence_level",
        "correlation_id",
        "created_at",
        "relationship_type",
        "scope",
        "source_node_id",
        "status",
        "target_node_id",
    ]:
        op.create_index(op.f(f"ix_knowledge_edges_{column}"), "knowledge_edges", [column])


def downgrade() -> None:
    for column in [
        "target_node_id",
        "status",
        "source_node_id",
        "scope",
        "relationship_type",
        "created_at",
        "correlation_id",
        "confidence_level",
    ]:
        op.drop_index(op.f(f"ix_knowledge_edges_{column}"), table_name="knowledge_edges")
    op.drop_table("knowledge_edges")

    for column in [
        "status",
        "node_type",
        "label",
        "entity_type",
        "entity_id",
        "created_at",
        "correlation_id",
        "confidence_level",
    ]:
        op.drop_index(op.f(f"ix_knowledge_nodes_{column}"), table_name="knowledge_nodes")
    op.drop_table("knowledge_nodes")

    for column in [
        "workflow_run_id",
        "scope",
        "persistence_level",
        "news_item_id",
        "memory_type",
        "memory_status",
        "invalidated_at",
        "human_review_required",
        "expiration_recommendation",
        "entity_type",
        "entity_id",
        "created_at",
        "correlation_id",
        "confidence_level",
        "approved_at",
        "agent_output_id",
    ]:
        op.drop_index(op.f(f"ix_memory_items_{column}"), table_name="memory_items")
    op.drop_table("memory_items")

    for column in [
        "workflow_task_id",
        "workflow_run_id",
        "publication_record_id",
        "news_item_id",
        "metric_name",
        "metric_category",
        "measurement_window",
        "entity_type",
        "entity_id",
        "data_quality",
        "correlation_id",
        "created_at",
        "content_piece_id",
        "channel",
        "agent_output_id",
        "agent_execution_id",
    ]:
        op.drop_index(op.f(f"ix_metric_snapshots_{column}"), table_name="metric_snapshots")
    op.drop_table("metric_snapshots")
