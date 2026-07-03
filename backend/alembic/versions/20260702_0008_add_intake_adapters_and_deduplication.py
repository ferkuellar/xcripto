"""add intake adapters and deduplication

Revision ID: 20260702_0008
Revises: 20260702_0007
Create Date: 2026-07-02
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260702_0008"
down_revision: str | None = "20260702_0007"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "intake_signals",
        sa.Column("signal_type", sa.String(length=40), nullable=False),
        sa.Column("signal_status", sa.String(length=40), nullable=False),
        sa.Column("source_name", sa.String(length=180), nullable=True),
        sa.Column("source_url", sa.String(length=2048), nullable=True),
        sa.Column("source_type", sa.String(length=80), nullable=True),
        sa.Column("source_published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("raw_title", sa.String(length=500), nullable=True),
        sa.Column("raw_summary", sa.Text(), nullable=True),
        sa.Column("raw_content", sa.Text(), nullable=True),
        sa.Column("normalized_title", sa.String(length=500), nullable=True),
        sa.Column("normalized_summary", sa.Text(), nullable=True),
        sa.Column("language", sa.String(length=20), nullable=True),
        sa.Column("topic", sa.String(length=120), nullable=True),
        sa.Column("asset_symbols", sa.JSON(), nullable=False),
        sa.Column("entities", sa.JSON(), nullable=False),
        sa.Column("keywords", sa.JSON(), nullable=False),
        sa.Column("url_canonical", sa.String(length=2048), nullable=True),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("dedupe_key", sa.String(length=255), nullable=False),
        sa.Column("priority", sa.String(length=2), nullable=False),
        sa.Column("confidence_level", sa.String(length=20), nullable=False),
        sa.Column("risk_flags", sa.JSON(), nullable=False),
        sa.Column("adapter_name", sa.String(length=120), nullable=True),
        sa.Column("adapter_version", sa.String(length=40), nullable=True),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.Column("normalized_payload", sa.JSON(), nullable=True),
        sa.Column("duplicate_of_signal_id", sa.String(length=36), nullable=True),
        sa.Column("linked_news_item_id", sa.String(length=36), nullable=True),
        sa.Column("promoted_news_item_id", sa.String(length=36), nullable=True),
        sa.Column("dedupe_status", sa.String(length=40), nullable=False),
        sa.Column("dedupe_score", sa.Float(), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["duplicate_of_signal_id"], ["intake_signals.id"]),
        sa.ForeignKeyConstraint(["linked_news_item_id"], ["news_items.id"]),
        sa.ForeignKeyConstraint(["promoted_news_item_id"], ["news_items.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for index_name, column in [
        ("ix_intake_signals_signal_type", "signal_type"),
        ("ix_intake_signals_signal_status", "signal_status"),
        ("ix_intake_signals_dedupe_status", "dedupe_status"),
        ("ix_intake_signals_source_name", "source_name"),
        ("ix_intake_signals_source_type", "source_type"),
        ("ix_intake_signals_url_canonical", "url_canonical"),
        ("ix_intake_signals_content_hash", "content_hash"),
        ("ix_intake_signals_dedupe_key", "dedupe_key"),
        ("ix_intake_signals_linked_news_item_id", "linked_news_item_id"),
        ("ix_intake_signals_promoted_news_item_id", "promoted_news_item_id"),
        ("ix_intake_signals_correlation_id", "correlation_id"),
        ("ix_intake_signals_created_at", "created_at"),
    ]:
        op.create_index(op.f(index_name), "intake_signals", [column])

    op.create_table(
        "intake_adapter_runs",
        sa.Column("adapter_name", sa.String(length=120), nullable=False),
        sa.Column("adapter_version", sa.String(length=40), nullable=True),
        sa.Column("adapter_type", sa.String(length=40), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("input_payload", sa.JSON(), nullable=True),
        sa.Column("result_payload", sa.JSON(), nullable=True),
        sa.Column("signals_created_count", sa.Integer(), nullable=False),
        sa.Column("signals_duplicate_count", sa.Integer(), nullable=False),
        sa.Column("signals_error_count", sa.Integer(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    for index_name, column in [
        ("ix_intake_adapter_runs_adapter_name", "adapter_name"),
        ("ix_intake_adapter_runs_adapter_type", "adapter_type"),
        ("ix_intake_adapter_runs_status", "status"),
        ("ix_intake_adapter_runs_correlation_id", "correlation_id"),
        ("ix_intake_adapter_runs_created_at", "created_at"),
    ]:
        op.create_index(op.f(index_name), "intake_adapter_runs", [column])


def downgrade() -> None:
    for index_name in [
        "ix_intake_adapter_runs_created_at",
        "ix_intake_adapter_runs_correlation_id",
        "ix_intake_adapter_runs_status",
        "ix_intake_adapter_runs_adapter_type",
        "ix_intake_adapter_runs_adapter_name",
    ]:
        op.drop_index(op.f(index_name), table_name="intake_adapter_runs")
    op.drop_table("intake_adapter_runs")

    for index_name in [
        "ix_intake_signals_created_at",
        "ix_intake_signals_correlation_id",
        "ix_intake_signals_promoted_news_item_id",
        "ix_intake_signals_linked_news_item_id",
        "ix_intake_signals_dedupe_key",
        "ix_intake_signals_content_hash",
        "ix_intake_signals_url_canonical",
        "ix_intake_signals_source_type",
        "ix_intake_signals_source_name",
        "ix_intake_signals_dedupe_status",
        "ix_intake_signals_signal_status",
        "ix_intake_signals_signal_type",
    ]:
        op.drop_index(op.f(index_name), table_name="intake_signals")
    op.drop_table("intake_signals")
