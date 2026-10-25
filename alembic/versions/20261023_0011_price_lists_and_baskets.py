"""Sellers' price lists, offer labels, reservation baskets and seller applications.

Revision ID: 20261023_0011
Revises: 20261022_0010
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.orm import Session

from alembic import op
from app.part_types import ensure_standard_part_types

revision: str = "20261023_0011"
down_revision: str | None = "20261022_0010"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("supplier_offers", sa.Column("warranty_km", sa.Integer()))
    op.add_column("supplier_offers", sa.Column("promo", sa.String(30)))
    op.add_column("supplier_offers", sa.Column("discount_percent", sa.Integer()))
    op.add_column("supplier_offers", sa.Column("pack_qty", sa.Integer()))

    op.add_column("reservation_requests", sa.Column("basket_id", sa.String(40)))
    op.create_index("ix_reservation_requests_basket_id", "reservation_requests", ["basket_id"])

    op.create_table(
        "seller_applications",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("business_name", sa.String(200), nullable=False),
        sa.Column("contact_name", sa.String(200)),
        sa.Column("phone", sa.String(50), nullable=False),
        sa.Column("telegram", sa.String(100)),
        sa.Column("city", sa.String(200)),
        sa.Column("address", sa.Text()),
        sa.Column("cars", sa.String(300)),
        sa.Column("note", sa.Text()),
        sa.Column("status", sa.String(20), nullable=False, server_default="NEW"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_seller_applications_status", "seller_applications", ["status"])
    op.create_index("ix_seller_applications_created_at", "seller_applications", ["created_at"])

    # The part types sellers' lists need (cylinder liners, gearbox parts, door seals, ...).
    session = Session(bind=op.get_bind())
    ensure_standard_part_types(session)
    session.flush()


def downgrade() -> None:
    op.drop_index("ix_seller_applications_created_at", table_name="seller_applications")
    op.drop_index("ix_seller_applications_status", table_name="seller_applications")
    op.drop_table("seller_applications")
    op.drop_index("ix_reservation_requests_basket_id", table_name="reservation_requests")
    op.drop_column("reservation_requests", "basket_id")
    for column in ("pack_qty", "discount_percent", "promo", "warranty_km"):
        op.drop_column("supplier_offers", column)
