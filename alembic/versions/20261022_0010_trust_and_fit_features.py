"""Seller verification, offer labels, reservation details, part requests and fit reports.

Revision ID: 20261022_0010
Revises: 20261021_0009
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20261022_0010"
down_revision: str | None = "20261021_0009"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "suppliers",
        sa.Column("reliability_sample", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column("suppliers", sa.Column("legal_name", sa.String(300)))
    op.add_column("suppliers", sa.Column("inn", sa.String(20)))
    op.add_column("suppliers", sa.Column("licence_number", sa.String(100)))
    op.add_column("suppliers", sa.Column("work_hours", sa.String(200)))
    op.add_column("suppliers", sa.Column("map_url", sa.String(500)))
    op.add_column("suppliers", sa.Column("verified_at", sa.DateTime(timezone=True)))

    op.add_column("supplier_offers", sa.Column("part_origin", sa.String(20)))
    op.add_column("supplier_offers", sa.Column("warranty_months", sa.Integer()))
    op.add_column("supplier_offers", sa.Column("return_days", sa.Integer()))

    op.add_column("reservation_requests", sa.Column("outcome", sa.String(30)))
    op.add_column(
        "reservation_requests",
        sa.Column(
            "vehicle_id", sa.String(64), sa.ForeignKey("vehicles.id", ondelete="SET NULL")
        ),
    )
    op.add_column("reservation_requests", sa.Column("vehicle_label", sa.String(300)))
    op.add_column("reservation_requests", sa.Column("vin", sa.String(17)))
    op.add_column("reservation_requests", sa.Column("note", sa.Text()))
    op.add_column("reservation_requests", sa.Column("updated_at", sa.DateTime(timezone=True)))
    op.create_index("ix_reservation_requests_outcome", "reservation_requests", ["outcome"])
    op.create_index("ix_reservation_requests_vehicle_id", "reservation_requests", ["vehicle_id"])

    op.create_table(
        "part_requests",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("session_id", sa.String(100), nullable=False),
        sa.Column("query", sa.String(300), nullable=False),
        sa.Column("vehicle_id", sa.String(64), sa.ForeignKey("vehicles.id", ondelete="SET NULL")),
        sa.Column("vehicle_label", sa.String(300)),
        sa.Column("vin", sa.String(17)),
        sa.Column("contact", sa.String(200), nullable=False),
        sa.Column("note", sa.Text()),
        sa.Column("status", sa.String(20), nullable=False, server_default="OPEN"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_part_requests_session_id", "part_requests", ["session_id"])
    op.create_index("ix_part_requests_status", "part_requests", ["status"])
    op.create_index("ix_part_requests_created_at", "part_requests", ["created_at"])

    op.create_table(
        "fit_reports",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("session_id", sa.String(100), nullable=False),
        sa.Column(
            "product_id",
            sa.String(64),
            sa.ForeignKey("products.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("vehicle_id", sa.String(64), sa.ForeignKey("vehicles.id", ondelete="SET NULL")),
        sa.Column("vehicle_label", sa.String(300)),
        sa.Column("fits", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_fit_reports_session_id", "fit_reports", ["session_id"])
    op.create_index("ix_fit_reports_product_id", "fit_reports", ["product_id"])
    op.create_index("ix_fit_reports_vehicle_id", "fit_reports", ["vehicle_id"])
    op.create_index("ix_fit_reports_created_at", "fit_reports", ["created_at"])


def downgrade() -> None:
    op.drop_table("fit_reports")
    op.drop_table("part_requests")
    op.drop_index("ix_reservation_requests_vehicle_id", table_name="reservation_requests")
    op.drop_index("ix_reservation_requests_outcome", table_name="reservation_requests")
    for column in ("updated_at", "note", "vin", "vehicle_label", "vehicle_id", "outcome"):
        op.drop_column("reservation_requests", column)
    for column in ("return_days", "warranty_months", "part_origin"):
        op.drop_column("supplier_offers", column)
    for column in (
        "verified_at",
        "map_url",
        "work_hours",
        "licence_number",
        "inn",
        "legal_name",
        "reliability_sample",
    ):
        op.drop_column("suppliers", column)
