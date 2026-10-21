"""Add parsed query intents to search analytics."""

import sqlalchemy as sa

from alembic import op

revision = "20261008_0003"
down_revision = "20261007_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("search_events", sa.Column("detected_vehicle", sa.String(200)))
    op.add_column(
        "search_events",
        sa.Column("detected_product_terms", sa.JSON(), nullable=False, server_default="[]"),
    )
    op.alter_column("search_events", "detected_product_terms", server_default=None)
    op.add_column("search_events", sa.Column("detected_reference", sa.String(200)))
    op.add_column("search_events", sa.Column("detected_brand", sa.String(200)))
    op.add_column("search_events", sa.Column("detected_position", sa.String(50)))
    op.add_column("search_events", sa.Column("detected_side", sa.String(50)))
    for column in (
        "detected_vehicle",
        "detected_reference",
        "detected_brand",
        "detected_position",
        "detected_side",
    ):
        op.create_index(f"ix_search_events_{column}", "search_events", [column])


def downgrade() -> None:
    for column in (
        "detected_side",
        "detected_position",
        "detected_brand",
        "detected_reference",
        "detected_vehicle",
    ):
        op.drop_index(f"ix_search_events_{column}", table_name="search_events")
    for column in (
        "detected_side",
        "detected_position",
        "detected_brand",
        "detected_reference",
        "detected_product_terms",
        "detected_vehicle",
    ):
        op.drop_column("search_events", column)
