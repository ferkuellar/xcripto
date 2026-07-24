"""add news cover image url

Revision ID: 20260721_0001
Revises: 20260714_0001
Create Date: 2026-07-21
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260721_0001"
down_revision: str | None = "20260714_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "news_items",
        sa.Column("cover_image_url", sa.String(length=2048), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("news_items", "cover_image_url")
