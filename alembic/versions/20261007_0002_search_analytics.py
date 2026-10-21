"""Add pilot search analytics and feedback."""

import sqlalchemy as sa

from alembic import op

revision = "20261007_0002"
down_revision = "20261007_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "search_events",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.String(100), nullable=True),
        sa.Column("session_id", sa.String(100), nullable=False),
        sa.Column("query_raw", sa.String(500), nullable=False),
        sa.Column("query_normalized", sa.String(500), nullable=False),
        sa.Column("result_count", sa.Integer(), nullable=False),
        sa.Column("search_time_ms", sa.Numeric(12, 3), nullable=False),
        sa.Column("top_product_ids", sa.JSON(), nullable=False),
        sa.Column("clicked_product_id", sa.String(64), nullable=True),
        sa.Column("clicked_supplier_id", sa.BigInteger(), nullable=True),
        sa.Column("action", sa.String(30), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["clicked_product_id"], ["products.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["clicked_supplier_id"], ["suppliers.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "pilot_feedback",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("search_event_id", sa.BigInteger(), nullable=False),
        sa.Column("found_correct_part", sa.Boolean(), nullable=False),
        sa.Column("correct_in_top_3", sa.Boolean(), nullable=False),
        sa.Column("user_rating", sa.Integer(), nullable=True),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint(
            "user_rating IS NULL OR (user_rating >= 1 AND user_rating <= 5)",
            name="ck_pilot_feedback_rating",
        ),
        sa.ForeignKeyConstraint(["search_event_id"], ["search_events.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("search_event_id"),
    )
    for table, column in (
        ("search_events", "user_id"),
        ("search_events", "session_id"),
        ("search_events", "query_normalized"),
        ("search_events", "clicked_product_id"),
        ("search_events", "clicked_supplier_id"),
        ("search_events", "action"),
        ("search_events", "created_at"),
        ("pilot_feedback", "search_event_id"),
    ):
        op.create_index(f"ix_{table}_{column}", table, [column])


def downgrade() -> None:
    op.drop_table("pilot_feedback")
    op.drop_table("search_events")
