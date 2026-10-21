"""Store result-group distribution and top score."""

import sqlalchemy as sa

from alembic import op

revision = "20261008_0004"
down_revision = "20261008_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "search_events",
        sa.Column("result_group_distribution", sa.JSON(), nullable=False, server_default="{}"),
    )
    op.alter_column("search_events", "result_group_distribution", server_default=None)
    op.add_column("search_events", sa.Column("top_result_score", sa.Numeric(12, 3)))


def downgrade() -> None:
    op.drop_column("search_events", "top_result_score")
    op.drop_column("search_events", "result_group_distribution")
