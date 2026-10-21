"""Initial audited catalog schema."""

import sqlalchemy as sa

from alembic import op

revision = "20261007_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.create_table(
        "brands",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("normalized_name", sa.String(200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("normalized_name"),
    )
    op.create_table(
        "suppliers",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("normalized_name", sa.String(200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("normalized_name"),
    )
    op.create_table(
        "products",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("name", sa.String(500), nullable=False),
        sa.Column("normalized_name", sa.String(500), nullable=False),
        sa.Column("brand_id", sa.BigInteger(), nullable=True),
        sa.Column("origin", sa.String(100), nullable=True),
        sa.Column("position", sa.String(50), nullable=True),
        sa.Column("side", sa.String(50), nullable=True),
        sa.Column("engine_hint", sa.String(100), nullable=True),
        sa.Column("merge_basis", sa.String(50), nullable=True),
        sa.Column("audit_status", sa.String(30), nullable=False),
        sa.Column("audit_reason", sa.Text(), nullable=True),
        sa.Column("is_searchable", sa.Boolean(), nullable=False),
        sa.Column("search_text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["brand_id"], ["brands.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "vehicles",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("make", sa.String(150), nullable=True),
        sa.Column("model", sa.String(300), nullable=False),
        sa.Column("generation", sa.String(150), nullable=True),
        sa.Column("normalized_text", sa.String(600), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "reference_numbers",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("product_id", sa.String(64), nullable=False),
        sa.Column("number", sa.String(200), nullable=False),
        sa.Column("normalized_number", sa.String(200), nullable=False),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("source_supplier_id", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_supplier_id"], ["suppliers.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("product_id", "normalized_number", "type", name="uq_product_reference"),
    )
    op.create_table(
        "fitments",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("product_id", sa.String(64), nullable=False),
        sa.Column("vehicle_id", sa.String(64), nullable=False),
        sa.Column("source_vehicle_text", sa.Text(), nullable=True),
        sa.Column("source_supplier_id", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["vehicle_id"], ["vehicles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_supplier_id"], ["suppliers.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "product_id", "vehicle_id", "source_supplier_id", name="uq_product_vehicle_supplier"
        ),
    )
    op.create_table(
        "supplier_offers",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("source_offer_id", sa.String(64), nullable=False),
        sa.Column("supplier_id", sa.BigInteger(), nullable=False),
        sa.Column("product_id", sa.String(64), nullable=False),
        sa.Column("supplier_sku", sa.String(200), nullable=True),
        sa.Column("normalized_supplier_sku", sa.String(200), nullable=True),
        sa.Column("price_uzs", sa.Numeric(18, 2), nullable=True),
        sa.Column("stock", sa.Integer(), nullable=True),
        sa.Column("data_status", sa.String(50), nullable=True),
        sa.ForeignKeyConstraint(["supplier_id"], ["suppliers.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source_offer_id", name="uq_source_offer_id"),
    )
    op.create_table(
        "raw_supplier_products",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("source_raw_id", sa.String(64), nullable=False),
        sa.Column("supplier_id", sa.BigInteger(), nullable=False),
        sa.Column("source_row", sa.Integer(), nullable=True),
        sa.Column("product_id", sa.String(64), nullable=True),
        sa.Column("raw_name", sa.Text(), nullable=False),
        sa.Column("parsed_product_name", sa.Text(), nullable=True),
        sa.Column("raw_brand", sa.String(200), nullable=True),
        sa.Column("supplier_code", sa.String(200), nullable=True),
        sa.Column("supplier_code_type", sa.String(50), nullable=True),
        sa.Column("origin", sa.String(100), nullable=True),
        sa.Column("unit", sa.String(50), nullable=True),
        sa.Column("vehicle_raw", sa.Text(), nullable=True),
        sa.Column("position", sa.String(50), nullable=True),
        sa.Column("side", sa.String(50), nullable=True),
        sa.Column("engine_hint", sa.String(100), nullable=True),
        sa.Column("audit_status", sa.String(30), nullable=False),
        sa.Column("audit_reason", sa.Text(), nullable=True),
        sa.Column("source_payload", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["supplier_id"], ["suppliers.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source_raw_id", name="uq_source_raw_id"),
    )

    for table, column in (
        ("brands", "normalized_name"),
        ("suppliers", "normalized_name"),
        ("products", "name"),
        ("products", "normalized_name"),
        ("products", "audit_status"),
        ("products", "is_searchable"),
        ("vehicles", "model"),
        ("vehicles", "normalized_text"),
        ("reference_numbers", "product_id"),
        ("reference_numbers", "normalized_number"),
        ("reference_numbers", "type"),
        ("fitments", "product_id"),
        ("fitments", "vehicle_id"),
        ("supplier_offers", "supplier_id"),
        ("supplier_offers", "product_id"),
        ("supplier_offers", "normalized_supplier_sku"),
        ("raw_supplier_products", "supplier_id"),
        ("raw_supplier_products", "product_id"),
        ("raw_supplier_products", "audit_status"),
    ):
        op.create_index(f"ix_{table}_{column}", table, [column])
    op.create_index("ix_products_name_brand", "products", ["normalized_name", "brand_id"])
    op.create_index("ix_products_searchable_status", "products", ["is_searchable", "audit_status"])
    op.create_index(
        "ix_products_search_text_trgm",
        "products",
        ["search_text"],
        postgresql_using="gin",
        postgresql_ops={"search_text": "gin_trgm_ops"},
    )


def downgrade() -> None:
    op.drop_table("raw_supplier_products")
    op.drop_table("supplier_offers")
    op.drop_table("fitments")
    op.drop_table("reference_numbers")
    op.drop_table("vehicles")
    op.drop_table("products")
    op.drop_table("suppliers")
    op.drop_table("brands")
