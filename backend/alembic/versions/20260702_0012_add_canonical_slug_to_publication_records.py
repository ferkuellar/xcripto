"""add canonical slug to publication records

Revision ID: 20260702_0012
Revises: 20260702_0011
Create Date: 2026-07-09
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260702_0012"
down_revision: str | None = "20260702_0011"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "publication_records",
        sa.Column("canonical_slug", sa.String(length=280), nullable=True),
    )
    op.create_index(
        op.f("ix_publication_records_canonical_slug"),
        "publication_records",
        ["canonical_slug"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_publication_records_canonical_slug"), table_name="publication_records")
    op.drop_column("publication_records", "canonical_slug")
