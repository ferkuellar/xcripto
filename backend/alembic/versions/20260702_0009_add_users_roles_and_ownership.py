"""add users roles and ownership

Revision ID: 20260702_0009
Revises: 20260702_0008
Create Date: 2026-07-02
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260702_0009"
down_revision: str | None = "20260702_0008"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "user_accounts",
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("display_name", sa.String(length=180), nullable=False),
        sa.Column("handle", sa.String(length=80), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("role", sa.String(length=40), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_system_user", sa.Boolean(), nullable=False),
        sa.Column("timezone", sa.String(length=80), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("handle"),
    )
    for index_name, column in [
        ("ix_user_accounts_email", "email"),
        ("ix_user_accounts_handle", "handle"),
        ("ix_user_accounts_role", "role"),
        ("ix_user_accounts_status", "status"),
        ("ix_user_accounts_is_active", "is_active"),
        ("ix_user_accounts_correlation_id", "correlation_id"),
        ("ix_user_accounts_created_at", "created_at"),
    ]:
        op.create_index(op.f(index_name), "user_accounts", [column])

    op.create_table(
        "ownership_assignments",
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("entity_type", sa.String(length=120), nullable=False),
        sa.Column("entity_id", sa.String(length=120), nullable=False),
        sa.Column("ownership_type", sa.String(length=40), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("assigned_by", sa.String(length=120), nullable=True),
        sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("released_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("correlation_id", sa.String(length=80), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user_accounts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for index_name, column in [
        ("ix_ownership_assignments_user_id", "user_id"),
        ("ix_ownership_assignments_entity_type", "entity_type"),
        ("ix_ownership_assignments_entity_id", "entity_id"),
        ("ix_ownership_assignments_ownership_type", "ownership_type"),
        ("ix_ownership_assignments_status", "status"),
        ("ix_ownership_assignments_correlation_id", "correlation_id"),
        ("ix_ownership_assignments_created_at", "created_at"),
    ]:
        op.create_index(op.f(index_name), "ownership_assignments", [column])


def downgrade() -> None:
    for index_name in [
        "ix_ownership_assignments_created_at",
        "ix_ownership_assignments_correlation_id",
        "ix_ownership_assignments_status",
        "ix_ownership_assignments_ownership_type",
        "ix_ownership_assignments_entity_id",
        "ix_ownership_assignments_entity_type",
        "ix_ownership_assignments_user_id",
    ]:
        op.drop_index(op.f(index_name), table_name="ownership_assignments")
    op.drop_table("ownership_assignments")

    for index_name in [
        "ix_user_accounts_created_at",
        "ix_user_accounts_correlation_id",
        "ix_user_accounts_is_active",
        "ix_user_accounts_status",
        "ix_user_accounts_role",
        "ix_user_accounts_handle",
        "ix_user_accounts_email",
    ]:
        op.drop_index(op.f(index_name), table_name="user_accounts")
    op.drop_table("user_accounts")
