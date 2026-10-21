"""Import every IRIZON workbook sheet

Revision ID: 20261010_0007
Revises: 20261010_0006
Create Date: 2026-10-10 14:14:21.924961
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20261010_0007"
down_revision: str | None = "20261010_0006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "catalog_field_docs",
        sa.Column("sheet", sa.String(length=100), nullable=False),
        sa.Column("column", sa.String(length=100), nullable=False),
        sa.Column("required", sa.Boolean(), nullable=False),
        sa.Column("kind", sa.String(length=50), nullable=True),
        sa.Column("allowed_values", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("sheet", "column"),
    )
    op.create_table(
        "catalog_list_values",
        sa.Column(
            "id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("list_name", sa.String(length=100), nullable=False),
        sa.Column("value", sa.String(length=200), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("list_name", "value", name="uq_catalog_list_value"),
    )
    op.create_index(
        op.f("ix_catalog_list_values_list_name"), "catalog_list_values", ["list_name"], unique=False
    )
    op.create_table(
        "catalog_settings",
        sa.Column("key", sa.String(length=100), nullable=False),
        sa.Column("value", sa.Text(), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("key"),
    )
    op.create_table(
        "categories",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("parent_id", sa.String(length=64), nullable=True),
        sa.Column("name_uz", sa.String(length=300), nullable=False),
        sa.Column("name_ru", sa.String(length=300), nullable=True),
        sa.Column("name_en", sa.String(length=300), nullable=True),
        sa.Column("is_leaf", sa.Boolean(), nullable=False),
        sa.Column("tecdoc_generic_article_id", sa.String(length=64), nullable=True),
        sa.Column("pcdb_part_type_id", sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(["parent_id"], ["categories.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_categories_parent_id"), "categories", ["parent_id"], unique=False)
    op.create_table(
        "search_synonyms",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("target_type", sa.String(length=30), nullable=False),
        sa.Column("target_id", sa.String(length=64), nullable=False),
        sa.Column("term", sa.String(length=300), nullable=False),
        sa.Column("lang", sa.String(length=10), nullable=True),
        sa.Column("synonym_type", sa.String(length=30), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_search_synonyms_target_id"), "search_synonyms", ["target_id"], unique=False
    )
    op.create_index(
        op.f("ix_search_synonyms_target_type"), "search_synonyms", ["target_type"], unique=False
    )
    op.create_table(
        "category_attributes",
        sa.Column(
            "id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("category_id", sa.String(length=64), nullable=False),
        sa.Column("attribute_code", sa.String(length=100), nullable=False),
        sa.Column("name_uz", sa.String(length=300), nullable=False),
        sa.Column("name_ru", sa.String(length=300), nullable=True),
        sa.Column("unit", sa.String(length=50), nullable=True),
        sa.Column("data_type", sa.String(length=30), nullable=False),
        sa.Column("required", sa.Boolean(), nullable=False),
        sa.Column("allowed_values", sa.Text(), nullable=True),
        sa.Column("is_filter", sa.Boolean(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("category_id", "attribute_code", name="uq_category_attribute"),
    )
    op.create_index(
        op.f("ix_category_attributes_category_id"),
        "category_attributes",
        ["category_id"],
        unique=False,
    )
    op.create_table(
        "catalog_review_items",
        sa.Column("raw_id", sa.String(length=64), nullable=False),
        sa.Column("supplier", sa.String(length=200), nullable=True),
        sa.Column("product_id", sa.String(length=64), nullable=True),
        sa.Column("raw_name", sa.Text(), nullable=True),
        sa.Column("parsed_product_name", sa.Text(), nullable=True),
        sa.Column("brand", sa.String(length=200), nullable=True),
        sa.Column("reference", sa.String(length=200), nullable=True),
        sa.Column("vehicle_raw", sa.Text(), nullable=True),
        sa.Column("review_reason", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="ACTIVE"),
        sa.Column("reviewer", sa.String(length=100), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolution_note", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("raw_id"),
    )
    op.create_index(
        op.f("ix_catalog_review_items_product_id"),
        "catalog_review_items",
        ["product_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_catalog_review_items_status"), "catalog_review_items", ["status"], unique=False
    )
    op.create_table(
        "kit_components",
        sa.Column(
            "id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("kit_product_id", sa.String(length=64), nullable=False),
        sa.Column("component_product_id", sa.String(length=64), nullable=False),
        sa.Column("qty", sa.Integer(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["component_product_id"], ["products.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["kit_product_id"], ["products.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("kit_product_id", "component_product_id", name="uq_kit_component"),
    )
    op.create_index(
        op.f("ix_kit_components_component_product_id"),
        "kit_components",
        ["component_product_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_kit_components_kit_product_id"), "kit_components", ["kit_product_id"], unique=False
    )
    op.create_table(
        "product_attributes",
        sa.Column(
            "id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("product_id", sa.String(length=64), nullable=False),
        sa.Column("attribute_code", sa.String(length=100), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("unit", sa.String(length=50), nullable=True),
        sa.Column("source", sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("product_id", "attribute_code", name="uq_product_attribute"),
    )
    op.create_index(
        op.f("ix_product_attributes_product_id"), "product_attributes", ["product_id"], unique=False
    )
    op.create_table(
        "product_audits",
        sa.Column(
            "id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("product_id", sa.String(length=64), nullable=False),
        sa.Column("brand", sa.String(length=300), nullable=True),
        sa.Column("reference", sa.String(length=300), nullable=True),
        sa.Column("master_name", sa.Text(), nullable=True),
        sa.Column("supplier_count", sa.Integer(), nullable=True),
        sa.Column("suppliers", sa.Text(), nullable=True),
        sa.Column("cross_name_similarity", sa.String(length=30), nullable=True),
        sa.Column("internal_collision", sa.String(length=10), nullable=True),
        sa.Column("positions", sa.Text(), nullable=True),
        sa.Column("sides", sa.Text(), nullable=True),
        sa.Column("merge_status", sa.String(length=30), nullable=False),
        sa.Column("audit_reason", sa.Text(), nullable=True),
        sa.Column("source_rows", sa.Text(), nullable=True),
        sa.Column("attr_conflict", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_product_audits_merge_status"), "product_audits", ["merge_status"], unique=False
    )
    op.create_index(
        op.f("ix_product_audits_product_id"), "product_audits", ["product_id"], unique=False
    )
    op.create_table(
        "product_media",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("product_id", sa.String(length=64), nullable=False),
        sa.Column("media_type", sa.String(length=30), nullable=False),
        sa.Column("url_or_path", sa.Text(), nullable=False),
        sa.Column("is_primary", sa.Boolean(), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=True),
        sa.Column("license_note", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_product_media_product_id"), "product_media", ["product_id"], unique=False
    )
    op.create_table(
        "supersessions",
        sa.Column(
            "id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("old_number_raw", sa.String(length=200), nullable=False),
        sa.Column(
            "old_brand_id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=True
        ),
        sa.Column("old_product_id", sa.String(length=64), nullable=True),
        sa.Column("new_product_id", sa.String(length=64), nullable=False),
        sa.Column("interchangeability", sa.String(length=30), nullable=True),
        sa.Column("effective_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("source", sa.String(length=100), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["new_product_id"], ["products.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["old_brand_id"], ["brands.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["old_product_id"], ["products.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_supersessions_new_product_id"), "supersessions", ["new_product_id"], unique=False
    )
    op.add_column("brands", sa.Column("source_id", sa.String(length=64), nullable=True))
    op.add_column("brands", sa.Column("code", sa.String(length=200), nullable=True))
    op.add_column("brands", sa.Column("aliases", sa.Text(), nullable=True))
    op.add_column("brands", sa.Column("brand_type", sa.String(length=50), nullable=True))
    op.add_column("brands", sa.Column("quality_tier", sa.String(length=50), nullable=True))
    op.add_column("brands", sa.Column("country", sa.String(length=100), nullable=True))
    op.add_column("brands", sa.Column("tecdoc_brand_id", sa.String(length=64), nullable=True))
    op.add_column("brands", sa.Column("website", sa.String(length=300), nullable=True))
    op.add_column("brands", sa.Column("notes", sa.Text(), nullable=True))
    op.create_unique_constraint("uq_brands_source_id", "brands", ["source_id"])
    op.add_column("fitments", sa.Column("source_id", sa.String(length=64), nullable=True))
    op.add_column("fitments", sa.Column("position", sa.String(length=30), nullable=True))
    op.add_column("fitments", sa.Column("side", sa.String(length=30), nullable=True))
    op.add_column("fitments", sa.Column("vertical", sa.String(length=30), nullable=True))
    op.add_column("fitments", sa.Column("qty_per_vehicle", sa.Integer(), nullable=True))
    op.add_column("fitments", sa.Column("year_from", sa.Integer(), nullable=True))
    op.add_column("fitments", sa.Column("year_to", sa.Integer(), nullable=True))
    op.add_column("fitments", sa.Column("vin_from", sa.String(length=30), nullable=True))
    op.add_column("fitments", sa.Column("vin_to", sa.String(length=30), nullable=True))
    op.add_column("fitments", sa.Column("condition_note", sa.Text(), nullable=True))
    op.add_column("fitments", sa.Column("fitment_source", sa.String(length=50), nullable=True))
    op.add_column("fitments", sa.Column("confidence", sa.String(length=20), nullable=True))
    op.add_column(
        "fitments", sa.Column("verified", sa.Boolean(), nullable=False, server_default=sa.false())
    )
    op.add_column("products", sa.Column("category_id", sa.String(length=64), nullable=True))
    op.add_column("products", sa.Column("article_number", sa.String(length=200), nullable=True))
    op.add_column("products", sa.Column("name_ru", sa.String(length=500), nullable=True))
    op.add_column("products", sa.Column("name_en", sa.String(length=500), nullable=True))
    op.add_column(
        "products",
        sa.Column("status", sa.String(length=30), nullable=False, server_default="ACTIVE"),
    )
    op.add_column("products", sa.Column("unit", sa.String(length=20), nullable=True))
    op.add_column("products", sa.Column("pack_qty", sa.Integer(), nullable=True))
    op.add_column(
        "products", sa.Column("weight_kg", sa.Numeric(precision=12, scale=3), nullable=True)
    )
    op.add_column(
        "products", sa.Column("length_mm", sa.Numeric(precision=12, scale=1), nullable=True)
    )
    op.add_column(
        "products", sa.Column("width_mm", sa.Numeric(precision=12, scale=1), nullable=True)
    )
    op.add_column(
        "products", sa.Column("height_mm", sa.Numeric(precision=12, scale=1), nullable=True)
    )
    op.add_column("products", sa.Column("ean", sa.String(length=32), nullable=True))
    op.add_column("products", sa.Column("country_of_origin", sa.String(length=100), nullable=True))
    op.add_column("products", sa.Column("description", sa.Text(), nullable=True))
    op.add_column(
        "products", sa.Column("universal", sa.Boolean(), nullable=False, server_default=sa.false())
    )
    op.add_column("products", sa.Column("source_rows", sa.Text(), nullable=True))
    op.create_index(
        op.f("ix_products_article_number"), "products", ["article_number"], unique=False
    )
    op.create_index(op.f("ix_products_category_id"), "products", ["category_id"], unique=False)
    op.create_index(op.f("ix_products_status"), "products", ["status"], unique=False)
    op.create_foreign_key(
        "fk_products_category_id",
        "products",
        "categories",
        ["category_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.add_column("reference_numbers", sa.Column("source_id", sa.String(length=64), nullable=True))
    op.add_column(
        "reference_numbers",
        sa.Column(
            "number_brand_id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=True
        ),
    )
    op.add_column(
        "reference_numbers", sa.Column("cross_source", sa.String(length=50), nullable=True)
    )
    op.add_column("reference_numbers", sa.Column("confidence", sa.String(length=20), nullable=True))
    op.add_column(
        "reference_numbers",
        sa.Column("verified", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "reference_numbers", sa.Column("verified_by", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "reference_numbers", sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column("reference_numbers", sa.Column("notes", sa.Text(), nullable=True))
    op.create_foreign_key(
        "fk_reference_numbers_number_brand_id",
        "reference_numbers",
        "brands",
        ["number_brand_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.add_column("supplier_offers", sa.Column("price_type", sa.String(length=30), nullable=True))
    op.add_column("supplier_offers", sa.Column("lead_time_days", sa.Integer(), nullable=True))
    op.add_column("supplier_offers", sa.Column("min_order_qty", sa.Integer(), nullable=True))
    op.add_column("supplier_offers", sa.Column("condition", sa.String(length=30), nullable=True))
    op.add_column(
        "supplier_offers", sa.Column("source_data_status", sa.String(length=30), nullable=True)
    )
    op.add_column("suppliers", sa.Column("source_id", sa.String(length=64), nullable=True))
    op.add_column("suppliers", sa.Column("supplier_type", sa.String(length=50), nullable=True))
    op.add_column("suppliers", sa.Column("city", sa.String(length=200), nullable=True))
    op.add_column("suppliers", sa.Column("contact", sa.Text(), nullable=True))
    op.add_column("suppliers", sa.Column("default_currency", sa.String(length=3), nullable=True))
    op.add_column("suppliers", sa.Column("integration", sa.String(length=50), nullable=True))
    op.add_column("suppliers", sa.Column("update_frequency_days", sa.Integer(), nullable=True))
    op.add_column("suppliers", sa.Column("default_lead_time_days", sa.Integer(), nullable=True))
    op.add_column(
        "suppliers", sa.Column("reliability_score", sa.Numeric(precision=5, scale=2), nullable=True)
    )
    op.create_unique_constraint("uq_suppliers_source_id", "suppliers", ["source_id"])
    op.add_column("vehicles", sa.Column("generation_code", sa.String(length=100), nullable=True))
    op.add_column("vehicles", sa.Column("modification", sa.String(length=200), nullable=True))
    op.add_column("vehicles", sa.Column("year_from", sa.Integer(), nullable=True))
    op.add_column("vehicles", sa.Column("year_to", sa.Integer(), nullable=True))
    op.add_column("vehicles", sa.Column("body_type", sa.String(length=50), nullable=True))
    op.add_column("vehicles", sa.Column("engine_code", sa.String(length=100), nullable=True))
    op.add_column("vehicles", sa.Column("displacement_cc", sa.Integer(), nullable=True))
    op.add_column("vehicles", sa.Column("power_kw", sa.Integer(), nullable=True))
    op.add_column("vehicles", sa.Column("fuel_type", sa.String(length=50), nullable=True))
    op.add_column("vehicles", sa.Column("transmission", sa.String(length=50), nullable=True))
    op.add_column("vehicles", sa.Column("drive_type", sa.String(length=50), nullable=True))
    op.add_column("vehicles", sa.Column("market", sa.String(length=50), nullable=True))
    op.add_column("vehicles", sa.Column("vin_wmi", sa.String(length=20), nullable=True))
    op.add_column("vehicles", sa.Column("vin_vds_pattern", sa.String(length=50), nullable=True))
    op.add_column("vehicles", sa.Column("tecdoc_ktype", sa.String(length=64), nullable=True))
    op.add_column("vehicles", sa.Column("vehicle_source", sa.String(length=50), nullable=True))
    op.add_column("vehicles", sa.Column("origin_type", sa.String(length=50), nullable=True))
    op.add_column("vehicles", sa.Column("plant", sa.String(length=200), nullable=True))
    op.add_column("vehicles", sa.Column("aliases", sa.Text(), nullable=True))
    op.add_column("vehicles", sa.Column("parc_priority", sa.String(length=20), nullable=True))
    op.add_column("vehicles", sa.Column("data_confidence", sa.String(length=20), nullable=True))
    op.add_column("vehicles", sa.Column("notes", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("vehicles", "notes")
    op.drop_column("vehicles", "data_confidence")
    op.drop_column("vehicles", "parc_priority")
    op.drop_column("vehicles", "aliases")
    op.drop_column("vehicles", "plant")
    op.drop_column("vehicles", "origin_type")
    op.drop_column("vehicles", "vehicle_source")
    op.drop_column("vehicles", "tecdoc_ktype")
    op.drop_column("vehicles", "vin_vds_pattern")
    op.drop_column("vehicles", "vin_wmi")
    op.drop_column("vehicles", "market")
    op.drop_column("vehicles", "drive_type")
    op.drop_column("vehicles", "transmission")
    op.drop_column("vehicles", "fuel_type")
    op.drop_column("vehicles", "power_kw")
    op.drop_column("vehicles", "displacement_cc")
    op.drop_column("vehicles", "engine_code")
    op.drop_column("vehicles", "body_type")
    op.drop_column("vehicles", "year_to")
    op.drop_column("vehicles", "year_from")
    op.drop_column("vehicles", "modification")
    op.drop_column("vehicles", "generation_code")
    op.drop_constraint("uq_suppliers_source_id", "suppliers", type_="unique")
    op.drop_column("suppliers", "reliability_score")
    op.drop_column("suppliers", "default_lead_time_days")
    op.drop_column("suppliers", "update_frequency_days")
    op.drop_column("suppliers", "integration")
    op.drop_column("suppliers", "default_currency")
    op.drop_column("suppliers", "contact")
    op.drop_column("suppliers", "city")
    op.drop_column("suppliers", "supplier_type")
    op.drop_column("suppliers", "source_id")
    op.drop_column("supplier_offers", "source_data_status")
    op.drop_column("supplier_offers", "condition")
    op.drop_column("supplier_offers", "min_order_qty")
    op.drop_column("supplier_offers", "lead_time_days")
    op.drop_column("supplier_offers", "price_type")
    op.drop_constraint(
        "fk_reference_numbers_number_brand_id", "reference_numbers", type_="foreignkey"
    )
    op.drop_column("reference_numbers", "notes")
    op.drop_column("reference_numbers", "verified_at")
    op.drop_column("reference_numbers", "verified_by")
    op.drop_column("reference_numbers", "verified")
    op.drop_column("reference_numbers", "confidence")
    op.drop_column("reference_numbers", "cross_source")
    op.drop_column("reference_numbers", "number_brand_id")
    op.drop_column("reference_numbers", "source_id")
    op.drop_constraint("fk_products_category_id", "products", type_="foreignkey")
    op.drop_index(op.f("ix_products_status"), table_name="products")
    op.drop_index(op.f("ix_products_category_id"), table_name="products")
    op.drop_index(op.f("ix_products_article_number"), table_name="products")
    op.drop_column("products", "source_rows")
    op.drop_column("products", "universal")
    op.drop_column("products", "description")
    op.drop_column("products", "country_of_origin")
    op.drop_column("products", "ean")
    op.drop_column("products", "height_mm")
    op.drop_column("products", "width_mm")
    op.drop_column("products", "length_mm")
    op.drop_column("products", "weight_kg")
    op.drop_column("products", "pack_qty")
    op.drop_column("products", "unit")
    op.drop_column("products", "status")
    op.drop_column("products", "name_en")
    op.drop_column("products", "name_ru")
    op.drop_column("products", "article_number")
    op.drop_column("products", "category_id")
    op.drop_column("fitments", "verified")
    op.drop_column("fitments", "confidence")
    op.drop_column("fitments", "fitment_source")
    op.drop_column("fitments", "condition_note")
    op.drop_column("fitments", "vin_to")
    op.drop_column("fitments", "vin_from")
    op.drop_column("fitments", "year_to")
    op.drop_column("fitments", "year_from")
    op.drop_column("fitments", "qty_per_vehicle")
    op.drop_column("fitments", "vertical")
    op.drop_column("fitments", "side")
    op.drop_column("fitments", "position")
    op.drop_column("fitments", "source_id")
    op.drop_constraint("uq_brands_source_id", "brands", type_="unique")
    op.drop_column("brands", "notes")
    op.drop_column("brands", "website")
    op.drop_column("brands", "tecdoc_brand_id")
    op.drop_column("brands", "country")
    op.drop_column("brands", "quality_tier")
    op.drop_column("brands", "brand_type")
    op.drop_column("brands", "aliases")
    op.drop_column("brands", "code")
    op.drop_column("brands", "source_id")
    op.drop_index(op.f("ix_supersessions_new_product_id"), table_name="supersessions")
    op.drop_table("supersessions")
    op.drop_index(op.f("ix_product_media_product_id"), table_name="product_media")
    op.drop_table("product_media")
    op.drop_index(op.f("ix_product_audits_product_id"), table_name="product_audits")
    op.drop_index(op.f("ix_product_audits_merge_status"), table_name="product_audits")
    op.drop_table("product_audits")
    op.drop_index(op.f("ix_product_attributes_product_id"), table_name="product_attributes")
    op.drop_table("product_attributes")
    op.drop_index(op.f("ix_kit_components_kit_product_id"), table_name="kit_components")
    op.drop_index(op.f("ix_kit_components_component_product_id"), table_name="kit_components")
    op.drop_table("kit_components")
    op.drop_index(op.f("ix_catalog_review_items_status"), table_name="catalog_review_items")
    op.drop_index(op.f("ix_catalog_review_items_product_id"), table_name="catalog_review_items")
    op.drop_table("catalog_review_items")
    op.drop_index(op.f("ix_category_attributes_category_id"), table_name="category_attributes")
    op.drop_table("category_attributes")
    op.drop_index(op.f("ix_search_synonyms_target_type"), table_name="search_synonyms")
    op.drop_index(op.f("ix_search_synonyms_target_id"), table_name="search_synonyms")
    op.drop_table("search_synonyms")
    op.drop_index(op.f("ix_categories_parent_id"), table_name="categories")
    op.drop_table("categories")
    op.drop_table("catalog_settings")
    op.drop_index(op.f("ix_catalog_list_values_list_name"), table_name="catalog_list_values")
    op.drop_table("catalog_list_values")
    op.drop_table("catalog_field_docs")
