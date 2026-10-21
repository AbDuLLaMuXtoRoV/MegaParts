"""Add admin-curated search aliases."""

import sqlalchemy as sa

from alembic import op

revision = "20261010_0006"
down_revision = "20261008_0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "search_aliases",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("kind", sa.String(20), nullable=False),
        sa.Column("alias", sa.String(200), nullable=False),
        sa.Column("canonical", sa.String(200), nullable=False),
        sa.Column("source_query", sa.String(500)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("kind", "alias", name="uq_search_alias_kind_alias"),
        sa.CheckConstraint("kind IN ('product', 'vehicle')", name="ck_search_alias_kind"),
    )
    op.create_index("ix_search_aliases_kind", "search_aliases", ["kind"])


def downgrade() -> None:
    op.drop_index("ix_search_aliases_kind", table_name="search_aliases")
    op.drop_table("search_aliases")
