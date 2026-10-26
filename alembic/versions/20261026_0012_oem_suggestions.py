"""OEM codes buyers and mechanics send for parts that have none yet.

Revision ID: 20261026_0012
Revises: 20261023_0011
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20261026_0012"
down_revision: str | None = "20261023_0011"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "oem_suggestions",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("session_id", sa.String(100), nullable=False),
        sa.Column(
            "product_id",
            sa.String(64),
            sa.ForeignKey("products.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("number", sa.String(200), nullable=False),
        sa.Column("normalized_number", sa.String(200), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="NEW"),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("reviewed_at", sa.DateTime(timezone=True)),
    )
    for column in ("session_id", "product_id", "normalized_number", "status", "created_at"):
        op.create_index(f"ix_oem_suggestions_{column}", "oem_suggestions", [column])


def downgrade() -> None:
    op.drop_table("oem_suggestions")
