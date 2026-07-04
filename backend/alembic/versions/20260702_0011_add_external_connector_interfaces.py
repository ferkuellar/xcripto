"""add external connector interfaces

Revision ID: 20260702_0011
Revises: 20260702_0010
Create Date: 2026-07-02
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260702_0011"
down_revision: str | None = "20260702_0010"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "external_connectors",
        sa.Column("connector_name", sa.String(length=160), nullable=False),
        sa.Column("connector_type", sa.String(length=60), nullable=False),
        sa.Column("connector_status", sa.String(length=60), nullable=False),
        sa.Column("provider", sa.String(length=120), nullable=True),
        sa.Column("base_url", sa.String(length=2048), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("capabilities", sa.JSON(), nullable=False),
        sa.Column("configuration", sa.JSON(), nullable=True),
        sa.Column("secret_ref", sa.String(length=240), nullable=True),
        sa.Column("auth_type", sa.String(length=60), nullable=False),
        sa.Column("rate_limit_policy", sa.JSON(), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("dry_run_only", sa.Boolean(), nullable=False),
        sa.Column("last_run_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_success_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_failure_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    for index_name, column in [
        ("ix_external_connectors_connector_name", "connector_name"),
        ("ix_external_connectors_connector_type", "connector_type"),
        ("ix_external_connectors_connector_status", "connector_status"),
        ("ix_external_connectors_provider", "provider"),
        ("ix_external_connectors_enabled", "enabled"),
        ("ix_external_connectors_dry_run_only", "dry_run_only"),
        ("ix_external_connectors_correlation_id", "correlation_id"),
        ("ix_external_connectors_created_at", "created_at"),
    ]:
        op.create_index(op.f(index_name), "external_connectors", [column])

    op.create_table(
        "external_connector_runs",
        sa.Column("connector_id", sa.String(length=36), nullable=False),
        sa.Column("run_type", sa.String(length=60), nullable=False),
        sa.Column("run_status", sa.String(length=60), nullable=False),
        sa.Column("triggered_by", sa.String(length=120), nullable=True),
        sa.Column("input_payload", sa.JSON(), nullable=True),
        sa.Column("result_payload", sa.JSON(), nullable=True),
        sa.Column("signals_created_count", sa.Integer(), nullable=False),
        sa.Column("agent_outputs_created_count", sa.Integer(), nullable=False),
        sa.Column("publication_records_created_count", sa.Integer(), nullable=False),
        sa.Column("metric_snapshots_created_count", sa.Integer(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["connector_id"], ["external_connectors.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for index_name, column in [
        ("ix_external_connector_runs_connector_id", "connector_id"),
        ("ix_external_connector_runs_run_type", "run_type"),
        ("ix_external_connector_runs_run_status", "run_status"),
        ("ix_external_connector_runs_correlation_id", "correlation_id"),
        ("ix_external_connector_runs_created_at", "created_at"),
    ]:
        op.create_index(op.f(index_name), "external_connector_runs", [column])


def downgrade() -> None:
    for index_name in [
        "ix_external_connector_runs_created_at",
        "ix_external_connector_runs_correlation_id",
        "ix_external_connector_runs_run_status",
        "ix_external_connector_runs_run_type",
        "ix_external_connector_runs_connector_id",
    ]:
        op.drop_index(op.f(index_name), table_name="external_connector_runs")
    op.drop_table("external_connector_runs")

    for index_name in [
        "ix_external_connectors_created_at",
        "ix_external_connectors_correlation_id",
        "ix_external_connectors_dry_run_only",
        "ix_external_connectors_enabled",
        "ix_external_connectors_provider",
        "ix_external_connectors_connector_status",
        "ix_external_connectors_connector_type",
        "ix_external_connectors_connector_name",
    ]:
        op.drop_index(op.f(index_name), table_name="external_connectors")
    op.drop_table("external_connectors")
