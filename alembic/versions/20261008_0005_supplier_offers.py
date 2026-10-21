"""Add supplier offer imports, freshness, actions, and reservations."""

import sqlalchemy as sa

from alembic import op

revision = "20261008_0005"
down_revision = "20261008_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("suppliers", sa.Column("phone", sa.String(50)))
    op.add_column("suppliers", sa.Column("telegram", sa.String(100)))
    op.add_column("suppliers", sa.Column("address", sa.Text()))
    op.add_column(
        "suppliers", sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true())
    )
    op.add_column(
        "suppliers",
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_suppliers_is_active", "suppliers", ["is_active"])

    op.alter_column("supplier_offers", "price_uzs", new_column_name="price")
    op.alter_column("supplier_offers", "stock", new_column_name="stock_qty")
    op.add_column(
        "supplier_offers",
        sa.Column("currency", sa.String(3), nullable=False, server_default="UZS"),
    )
    op.add_column("supplier_offers", sa.Column("warehouse", sa.String(200)))
    op.add_column("supplier_offers", sa.Column("updated_at", sa.DateTime(timezone=True)))
    op.add_column(
        "supplier_offers",
        sa.Column("source_type", sa.String(20), nullable=False, server_default="EXCEL"),
    )
    op.add_column("supplier_offers", sa.Column("source_reference", sa.String(500)))
    op.add_column(
        "supplier_offers",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.execute("UPDATE supplier_offers SET data_status = 'DEMO' WHERE data_status IS NULL OR data_status <> 'LIVE'")
    op.execute(
        """
        WITH ranked AS (
            SELECT id, ROW_NUMBER() OVER (
                PARTITION BY supplier_id, product_id, normalized_supplier_sku ORDER BY id
            ) AS row_num
            FROM supplier_offers
            WHERE normalized_supplier_sku IS NOT NULL
        )
        UPDATE supplier_offers SET is_active = false
        WHERE id IN (SELECT id FROM ranked WHERE row_num > 1)
        """
    )
    op.create_index("ix_supplier_offers_is_active", "supplier_offers", ["is_active"])
    op.create_index(
        "uq_active_supplier_product_sku",
        "supplier_offers",
        ["supplier_id", "product_id", "normalized_supplier_sku"],
        unique=True,
        postgresql_where=sa.text("is_active AND normalized_supplier_sku IS NOT NULL"),
        sqlite_where=sa.text("is_active = 1 AND normalized_supplier_sku IS NOT NULL"),
    )

    op.create_table(
        "supplier_product_mappings",
        sa.Column("id", sa.BigInteger(), autoincrement=True, primary_key=True),
        sa.Column("supplier_id", sa.BigInteger(), nullable=False),
        sa.Column("product_id", sa.String(64), nullable=False),
        sa.Column("supplier_sku", sa.String(200), nullable=False),
        sa.Column("normalized_supplier_sku", sa.String(200), nullable=False),
        sa.Column("mapping_type", sa.String(30), nullable=False, server_default="CONFIRMED"),
        sa.Column("is_confirmed", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["supplier_id"], ["suppliers.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("supplier_id", "normalized_supplier_sku", name="uq_supplier_sku_mapping"),
    )
    op.create_index("ix_supplier_product_mappings_supplier_id", "supplier_product_mappings", ["supplier_id"])
    op.create_index("ix_supplier_product_mappings_product_id", "supplier_product_mappings", ["product_id"])

    op.create_table(
        "supplier_imports",
        sa.Column("id", sa.BigInteger(), autoincrement=True, primary_key=True),
        sa.Column("supplier_id", sa.BigInteger(), nullable=False),
        sa.Column("source_filename", sa.String(500)),
        sa.Column("source_type", sa.String(20), nullable=False, server_default="EXCEL"),
        sa.Column("rows_received", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rows_matched", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("unmatched_rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("updated_offers", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("new_offers", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("errors", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(30), nullable=False, server_default="PROCESSING"),
        sa.Column("imported_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["supplier_id"], ["suppliers.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_supplier_imports_supplier_id", "supplier_imports", ["supplier_id"])
    op.create_index("ix_supplier_imports_imported_at", "supplier_imports", ["imported_at"])

    op.create_table(
        "offer_import_review",
        sa.Column("id", sa.BigInteger(), autoincrement=True, primary_key=True),
        sa.Column("import_id", sa.BigInteger(), nullable=False),
        sa.Column("supplier_id", sa.BigInteger(), nullable=False),
        sa.Column("supplier_sku", sa.String(200)),
        sa.Column("raw_payload", sa.JSON(), nullable=False),
        sa.Column("suggested_product_id", sa.String(64)),
        sa.Column("status", sa.String(30), nullable=False, server_default="PENDING"),
        sa.Column("error", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["import_id"], ["supplier_imports.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["supplier_id"], ["suppliers.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["suggested_product_id"], ["products.id"], ondelete="SET NULL"),
    )
    for column in ("import_id", "supplier_id", "status"):
        op.create_index(f"ix_offer_import_review_{column}", "offer_import_review", [column])

    op.create_table(
        "reservation_requests",
        sa.Column("id", sa.BigInteger(), autoincrement=True, primary_key=True),
        sa.Column("user_id", sa.String(100)),
        sa.Column("session_id", sa.String(100), nullable=False),
        sa.Column("search_event_id", sa.BigInteger()),
        sa.Column("product_id", sa.String(64), nullable=False),
        sa.Column("supplier_offer_id", sa.BigInteger(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("phone", sa.String(50)),
        sa.Column("status", sa.String(30), nullable=False, server_default="REQUESTED"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint("quantity > 0", name="ck_reservation_quantity_positive"),
        sa.ForeignKeyConstraint(["search_event_id"], ["search_events.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["supplier_offer_id"], ["supplier_offers.id"], ondelete="CASCADE"),
    )
    for column in ("user_id", "session_id", "search_event_id", "product_id", "supplier_offer_id", "status", "created_at"):
        op.create_index(f"ix_reservation_requests_{column}", "reservation_requests", [column])

    op.create_table(
        "search_event_actions",
        sa.Column("id", sa.BigInteger(), autoincrement=True, primary_key=True),
        sa.Column("search_event_id", sa.BigInteger(), nullable=False),
        sa.Column("action", sa.String(40), nullable=False),
        sa.Column("product_id", sa.String(64)),
        sa.Column("supplier_id", sa.BigInteger()),
        sa.Column("supplier_offer_id", sa.BigInteger()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["search_event_id"], ["search_events.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["supplier_id"], ["suppliers.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["supplier_offer_id"], ["supplier_offers.id"], ondelete="SET NULL"),
    )
    for column in ("search_event_id", "action", "product_id", "supplier_id", "supplier_offer_id", "created_at"):
        op.create_index(f"ix_search_event_actions_{column}", "search_event_actions", [column])


def downgrade() -> None:
    op.drop_table("search_event_actions")
    op.drop_table("reservation_requests")
    op.drop_table("offer_import_review")
    op.drop_table("supplier_imports")
    op.drop_table("supplier_product_mappings")
    op.drop_index("uq_active_supplier_product_sku", table_name="supplier_offers")
    op.drop_index("ix_supplier_offers_is_active", table_name="supplier_offers")
    for column in ("is_active", "source_reference", "source_type", "updated_at", "warehouse", "currency"):
        op.drop_column("supplier_offers", column)
    op.alter_column("supplier_offers", "stock_qty", new_column_name="stock")
    op.alter_column("supplier_offers", "price", new_column_name="price_uzs")
    op.drop_index("ix_suppliers_is_active", table_name="suppliers")
    for column in ("created_at", "is_active", "address", "telegram", "phone"):
        op.drop_column("suppliers", column)
