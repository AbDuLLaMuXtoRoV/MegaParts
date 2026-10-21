from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

BIGINT_PK = BigInteger().with_variant(Integer, "sqlite")


class Base(DeclarativeBase):
    pass


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), unique=True)
    normalized_name: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    source_id: Mapped[str | None] = mapped_column(String(64), unique=True)
    code: Mapped[str | None] = mapped_column(String(200))
    aliases: Mapped[str | None] = mapped_column(Text)
    brand_type: Mapped[str | None] = mapped_column(String(50))
    quality_tier: Mapped[str | None] = mapped_column(String(50))
    country: Mapped[str | None] = mapped_column(String(100))
    tecdoc_brand_id: Mapped[str | None] = mapped_column(String(64))
    website: Mapped[str | None] = mapped_column(String(300))
    notes: Mapped[str | None] = mapped_column(Text)

    products: Mapped[list[Product]] = relationship(back_populates="brand")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    parent_id: Mapped[str | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), index=True
    )
    name_uz: Mapped[str] = mapped_column(String(300))
    name_ru: Mapped[str | None] = mapped_column(String(300))
    name_en: Mapped[str | None] = mapped_column(String(300))
    is_leaf: Mapped[bool] = mapped_column(Boolean, default=True)
    tecdoc_generic_article_id: Mapped[str | None] = mapped_column(String(64))
    pcdb_part_type_id: Mapped[str | None] = mapped_column(String(64))

    parent: Mapped[Category | None] = relationship(remote_side="Category.id")
    attributes: Mapped[list[CategoryAttribute]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",
        order_by="CategoryAttribute.sort_order",
    )


class CategoryAttribute(Base):
    __tablename__ = "category_attributes"
    __table_args__ = (
        UniqueConstraint("category_id", "attribute_code", name="uq_category_attribute"),
    )

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    category_id: Mapped[str] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), index=True
    )
    attribute_code: Mapped[str] = mapped_column(String(100))
    name_uz: Mapped[str] = mapped_column(String(300))
    name_ru: Mapped[str | None] = mapped_column(String(300))
    unit: Mapped[str | None] = mapped_column(String(50))
    data_type: Mapped[str] = mapped_column(String(30), default="TEXT")
    required: Mapped[bool] = mapped_column(Boolean, default=False)
    allowed_values: Mapped[str | None] = mapped_column(Text)
    is_filter: Mapped[bool] = mapped_column(Boolean, default=False)
    sort_order: Mapped[int | None] = mapped_column(Integer)

    category: Mapped[Category] = relationship(back_populates="attributes")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(500), index=True)
    normalized_name: Mapped[str] = mapped_column(String(500), index=True)
    brand_id: Mapped[int | None] = mapped_column(ForeignKey("brands.id", ondelete="SET NULL"))
    category_id: Mapped[str | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), index=True
    )
    article_number: Mapped[str | None] = mapped_column(String(200), index=True)
    name_ru: Mapped[str | None] = mapped_column(String(500))
    name_en: Mapped[str | None] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(30), default="ACTIVE", index=True)
    unit: Mapped[str | None] = mapped_column(String(20))
    pack_qty: Mapped[int | None] = mapped_column(Integer)
    weight_kg: Mapped[Decimal | None] = mapped_column(Numeric(12, 3))
    length_mm: Mapped[Decimal | None] = mapped_column(Numeric(12, 1))
    width_mm: Mapped[Decimal | None] = mapped_column(Numeric(12, 1))
    height_mm: Mapped[Decimal | None] = mapped_column(Numeric(12, 1))
    ean: Mapped[str | None] = mapped_column(String(32))
    country_of_origin: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    universal: Mapped[bool] = mapped_column(Boolean, default=False)
    source_rows: Mapped[str | None] = mapped_column(Text)
    origin: Mapped[str | None] = mapped_column(String(100))
    position: Mapped[str | None] = mapped_column(String(50))
    side: Mapped[str | None] = mapped_column(String(50))
    engine_hint: Mapped[str | None] = mapped_column(String(100))
    merge_basis: Mapped[str | None] = mapped_column(String(50))
    audit_status: Mapped[str] = mapped_column(String(30), default="UNAUDITED", index=True)
    audit_reason: Mapped[str | None] = mapped_column(Text)
    is_searchable: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    search_text: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    brand: Mapped[Brand | None] = relationship(back_populates="products")
    category: Mapped[Category | None] = relationship()
    attributes: Mapped[list[ProductAttribute]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    reference_numbers: Mapped[list[ReferenceNumber]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    fitments: Mapped[list[Fitment]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    supplier_offers: Mapped[list[SupplierOffer]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    raw_supplier_products: Mapped[list[RawSupplierProduct]] = relationship(back_populates="product")


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), unique=True)
    normalized_name: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(50))
    telegram: Mapped[str | None] = mapped_column(String(100))
    address: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    source_id: Mapped[str | None] = mapped_column(String(64), unique=True)
    supplier_type: Mapped[str | None] = mapped_column(String(50))
    city: Mapped[str | None] = mapped_column(String(200))
    contact: Mapped[str | None] = mapped_column(Text)
    default_currency: Mapped[str | None] = mapped_column(String(3))
    integration: Mapped[str | None] = mapped_column(String(50))
    update_frequency_days: Mapped[int | None] = mapped_column(Integer)
    default_lead_time_days: Mapped[int | None] = mapped_column(Integer)
    # Share of finished reservations the supplier honoured (0-100), over reliability_sample.
    reliability_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    reliability_sample: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    # Business identity checked by the MegaParts team; shown to buyers as "verified seller".
    legal_name: Mapped[str | None] = mapped_column(String(300))
    inn: Mapped[str | None] = mapped_column(String(20))
    licence_number: Mapped[str | None] = mapped_column(String(100))
    work_hours: Mapped[str | None] = mapped_column(String(200))
    map_url: Mapped[str | None] = mapped_column(String(500))
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    offers: Mapped[list[SupplierOffer]] = relationship(back_populates="supplier")
    raw_products: Mapped[list[RawSupplierProduct]] = relationship(back_populates="supplier")


class ReferenceNumber(Base):
    __tablename__ = "reference_numbers"
    __table_args__ = (
        UniqueConstraint("product_id", "normalized_number", "type", name="uq_product_reference"),
    )

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    number: Mapped[str] = mapped_column(String(200))
    normalized_number: Mapped[str] = mapped_column(String(200), index=True)
    type: Mapped[str] = mapped_column(String(50), index=True)
    source_supplier_id: Mapped[int | None] = mapped_column(
        ForeignKey("suppliers.id", ondelete="SET NULL")
    )
    source_id: Mapped[str | None] = mapped_column(String(64))
    number_brand_id: Mapped[int | None] = mapped_column(
        ForeignKey("brands.id", ondelete="SET NULL")
    )
    cross_source: Mapped[str | None] = mapped_column(String(50))
    confidence: Mapped[str | None] = mapped_column(String(20))
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verified_by: Mapped[str | None] = mapped_column(String(100))
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    notes: Mapped[str | None] = mapped_column(Text)

    product: Mapped[Product] = relationship(back_populates="reference_numbers")
    source_supplier: Mapped[Supplier | None] = relationship()
    number_brand: Mapped[Brand | None] = relationship()


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    make: Mapped[str | None] = mapped_column(String(150))
    model: Mapped[str] = mapped_column(String(300), index=True)
    generation: Mapped[str | None] = mapped_column(String(150))
    normalized_text: Mapped[str] = mapped_column(String(600), index=True)
    generation_code: Mapped[str | None] = mapped_column(String(100))
    modification: Mapped[str | None] = mapped_column(String(200))
    year_from: Mapped[int | None] = mapped_column(Integer)
    year_to: Mapped[int | None] = mapped_column(Integer)
    body_type: Mapped[str | None] = mapped_column(String(50))
    engine_code: Mapped[str | None] = mapped_column(String(100))
    displacement_cc: Mapped[int | None] = mapped_column(Integer)
    power_kw: Mapped[int | None] = mapped_column(Integer)
    fuel_type: Mapped[str | None] = mapped_column(String(50))
    transmission: Mapped[str | None] = mapped_column(String(50))
    drive_type: Mapped[str | None] = mapped_column(String(50))
    market: Mapped[str | None] = mapped_column(String(50))
    vin_wmi: Mapped[str | None] = mapped_column(String(20))
    vin_vds_pattern: Mapped[str | None] = mapped_column(String(50))
    tecdoc_ktype: Mapped[str | None] = mapped_column(String(64))
    vehicle_source: Mapped[str | None] = mapped_column(String(50))
    origin_type: Mapped[str | None] = mapped_column(String(50))
    plant: Mapped[str | None] = mapped_column(String(200))
    aliases: Mapped[str | None] = mapped_column(Text)
    parc_priority: Mapped[str | None] = mapped_column(String(20))
    data_confidence: Mapped[str | None] = mapped_column(String(20))
    notes: Mapped[str | None] = mapped_column(Text)

    fitments: Mapped[list[Fitment]] = relationship(back_populates="vehicle")


class Fitment(Base):
    __tablename__ = "fitments"
    __table_args__ = (
        UniqueConstraint(
            "product_id", "vehicle_id", "source_supplier_id", name="uq_product_vehicle_supplier"
        ),
    )

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    vehicle_id: Mapped[str] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE"), index=True
    )
    source_vehicle_text: Mapped[str | None] = mapped_column(Text)
    source_supplier_id: Mapped[int | None] = mapped_column(
        ForeignKey("suppliers.id", ondelete="SET NULL")
    )
    source_id: Mapped[str | None] = mapped_column(String(64))
    position: Mapped[str | None] = mapped_column(String(30))
    side: Mapped[str | None] = mapped_column(String(30))
    vertical: Mapped[str | None] = mapped_column(String(30))
    qty_per_vehicle: Mapped[int | None] = mapped_column(Integer)
    year_from: Mapped[int | None] = mapped_column(Integer)
    year_to: Mapped[int | None] = mapped_column(Integer)
    vin_from: Mapped[str | None] = mapped_column(String(30))
    vin_to: Mapped[str | None] = mapped_column(String(30))
    condition_note: Mapped[str | None] = mapped_column(Text)
    fitment_source: Mapped[str | None] = mapped_column(String(50))
    confidence: Mapped[str | None] = mapped_column(String(20))
    verified: Mapped[bool] = mapped_column(Boolean, default=False)

    product: Mapped[Product] = relationship(back_populates="fitments")
    vehicle: Mapped[Vehicle] = relationship(back_populates="fitments")
    source_supplier: Mapped[Supplier | None] = relationship()


class SupplierOffer(Base):
    __tablename__ = "supplier_offers"
    __table_args__ = (
        UniqueConstraint("source_offer_id", name="uq_source_offer_id"),
        Index(
            "uq_active_supplier_product_sku",
            "supplier_id",
            "product_id",
            "normalized_supplier_sku",
            unique=True,
            postgresql_where=text("is_active AND normalized_supplier_sku IS NOT NULL"),
            sqlite_where=text("is_active = 1 AND normalized_supplier_sku IS NOT NULL"),
        ),
    )

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    source_offer_id: Mapped[str] = mapped_column(String(64))
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id", ondelete="CASCADE"), index=True
    )
    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    supplier_sku: Mapped[str | None] = mapped_column(String(200))
    normalized_supplier_sku: Mapped[str | None] = mapped_column(String(200), index=True)
    price: Mapped[Decimal | None] = mapped_column(Numeric(18, 2))
    currency: Mapped[str] = mapped_column(String(3), default="UZS")
    stock_qty: Mapped[int | None] = mapped_column(Integer)
    warehouse: Mapped[str | None] = mapped_column(String(200))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    source_type: Mapped[str] = mapped_column(String(20), default="EXCEL")
    source_reference: Mapped[str | None] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    data_status: Mapped[str] = mapped_column(String(50), default="DEMO")
    price_type: Mapped[str | None] = mapped_column(String(30))
    lead_time_days: Mapped[int | None] = mapped_column(Integer)
    min_order_qty: Mapped[int | None] = mapped_column(Integer)
    condition: Mapped[str | None] = mapped_column(String(30))
    source_data_status: Mapped[str | None] = mapped_column(String(30))
    # GENUINE (carmaker part), OE (original-equipment maker's brand), AFTERMARKET or BUDGET.
    part_origin: Mapped[str | None] = mapped_column(String(20))
    warranty_months: Mapped[int | None] = mapped_column(Integer)
    return_days: Mapped[int | None] = mapped_column(Integer)

    supplier: Mapped[Supplier] = relationship(back_populates="offers")
    product: Mapped[Product] = relationship(back_populates="supplier_offers")


class RawSupplierProduct(Base):
    __tablename__ = "raw_supplier_products"
    __table_args__ = (UniqueConstraint("source_raw_id", name="uq_source_raw_id"),)

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    source_raw_id: Mapped[str] = mapped_column(String(64))
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id", ondelete="CASCADE"), index=True
    )
    source_row: Mapped[int | None] = mapped_column(Integer)
    product_id: Mapped[str | None] = mapped_column(
        ForeignKey("products.id", ondelete="SET NULL"), index=True
    )
    raw_name: Mapped[str] = mapped_column(Text)
    parsed_product_name: Mapped[str | None] = mapped_column(Text)
    raw_brand: Mapped[str | None] = mapped_column(String(200))
    supplier_code: Mapped[str | None] = mapped_column(String(200))
    supplier_code_type: Mapped[str | None] = mapped_column(String(50))
    origin: Mapped[str | None] = mapped_column(String(100))
    unit: Mapped[str | None] = mapped_column(String(50))
    vehicle_raw: Mapped[str | None] = mapped_column(Text)
    position: Mapped[str | None] = mapped_column(String(50))
    side: Mapped[str | None] = mapped_column(String(50))
    engine_hint: Mapped[str | None] = mapped_column(String(100))
    audit_status: Mapped[str] = mapped_column(String(30), default="UNAUDITED", index=True)
    audit_reason: Mapped[str | None] = mapped_column(Text)
    source_payload: Mapped[dict] = mapped_column(JSON, default=dict)

    supplier: Mapped[Supplier] = relationship(back_populates="raw_products")
    product: Mapped[Product | None] = relationship(back_populates="raw_supplier_products")


class SearchEvent(Base):
    __tablename__ = "search_events"

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    user_id: Mapped[str | None] = mapped_column(String(100), index=True)
    session_id: Mapped[str] = mapped_column(String(100), index=True)
    query_raw: Mapped[str] = mapped_column(String(500))
    query_normalized: Mapped[str] = mapped_column(String(500), index=True)
    result_count: Mapped[int] = mapped_column(Integer)
    search_time_ms: Mapped[float] = mapped_column(Numeric(12, 3))
    top_product_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    clicked_product_id: Mapped[str | None] = mapped_column(
        ForeignKey("products.id", ondelete="SET NULL"), index=True
    )
    clicked_supplier_id: Mapped[int | None] = mapped_column(
        ForeignKey("suppliers.id", ondelete="SET NULL"), index=True
    )
    action: Mapped[str | None] = mapped_column(String(30), index=True, default="search")
    detected_vehicle: Mapped[str | None] = mapped_column(String(200), index=True)
    detected_product_terms: Mapped[list[str]] = mapped_column(JSON, default=list)
    detected_reference: Mapped[str | None] = mapped_column(String(200), index=True)
    detected_brand: Mapped[str | None] = mapped_column(String(200), index=True)
    detected_position: Mapped[str | None] = mapped_column(String(50), index=True)
    detected_side: Mapped[str | None] = mapped_column(String(50), index=True)
    result_group_distribution: Mapped[dict[str, int]] = mapped_column(JSON, default=dict)
    top_result_score: Mapped[float | None] = mapped_column(Numeric(12, 3))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )

    clicked_product: Mapped[Product | None] = relationship()
    clicked_supplier: Mapped[Supplier | None] = relationship()
    feedback: Mapped[PilotFeedback | None] = relationship(
        back_populates="search_event", cascade="all, delete-orphan", uselist=False
    )


class PilotFeedback(Base):
    __tablename__ = "pilot_feedback"
    __table_args__ = (
        CheckConstraint(
            "user_rating IS NULL OR (user_rating >= 1 AND user_rating <= 5)",
            name="ck_pilot_feedback_rating",
        ),
    )

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    search_event_id: Mapped[int] = mapped_column(
        ForeignKey("search_events.id", ondelete="CASCADE"), unique=True, index=True
    )
    found_correct_part: Mapped[bool] = mapped_column(Boolean)
    correct_in_top_3: Mapped[bool] = mapped_column(Boolean)
    user_rating: Mapped[int | None] = mapped_column(Integer)
    comment: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    search_event: Mapped[SearchEvent] = relationship(back_populates="feedback")


class SupplierProductMapping(Base):
    __tablename__ = "supplier_product_mappings"
    __table_args__ = (
        UniqueConstraint("supplier_id", "normalized_supplier_sku", name="uq_supplier_sku_mapping"),
    )

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id", ondelete="CASCADE"), index=True
    )
    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    supplier_sku: Mapped[str] = mapped_column(String(200))
    normalized_supplier_sku: Mapped[str] = mapped_column(String(200))
    mapping_type: Mapped[str] = mapped_column(String(30), default="CONFIRMED")
    is_confirmed: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    supplier: Mapped[Supplier] = relationship()
    product: Mapped[Product] = relationship()


class SupplierImport(Base):
    __tablename__ = "supplier_imports"

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id", ondelete="CASCADE"), index=True
    )
    source_filename: Mapped[str | None] = mapped_column(String(500))
    source_type: Mapped[str] = mapped_column(String(20), default="EXCEL")
    rows_received: Mapped[int] = mapped_column(Integer, default=0)
    rows_matched: Mapped[int] = mapped_column(Integer, default=0)
    unmatched_rows: Mapped[int] = mapped_column(Integer, default=0)
    updated_offers: Mapped[int] = mapped_column(Integer, default=0)
    new_offers: Mapped[int] = mapped_column(Integer, default=0)
    errors: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(30), default="PROCESSING")
    imported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )

    supplier: Mapped[Supplier] = relationship()


class OfferImportReview(Base):
    __tablename__ = "offer_import_review"

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    import_id: Mapped[int] = mapped_column(
        ForeignKey("supplier_imports.id", ondelete="CASCADE"), index=True
    )
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id", ondelete="CASCADE"), index=True
    )
    supplier_sku: Mapped[str | None] = mapped_column(String(200))
    raw_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    suggested_product_id: Mapped[str | None] = mapped_column(
        ForeignKey("products.id", ondelete="SET NULL")
    )
    status: Mapped[str] = mapped_column(String(30), default="PENDING", index=True)
    error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    supplier_import: Mapped[SupplierImport] = relationship()
    supplier: Mapped[Supplier] = relationship()
    suggested_product: Mapped[Product | None] = relationship()


class ReservationRequest(Base):
    __tablename__ = "reservation_requests"
    __table_args__ = (CheckConstraint("quantity > 0", name="ck_reservation_quantity_positive"),)

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    user_id: Mapped[str | None] = mapped_column(String(100), index=True)
    session_id: Mapped[str] = mapped_column(String(100), index=True)
    search_event_id: Mapped[int | None] = mapped_column(
        ForeignKey("search_events.id", ondelete="SET NULL"), index=True
    )
    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    supplier_offer_id: Mapped[int] = mapped_column(
        ForeignKey("supplier_offers.id", ondelete="CASCADE"), index=True
    )
    quantity: Mapped[int] = mapped_column(Integer)
    phone: Mapped[str | None] = mapped_column(String(50))
    # REQUESTED -> CONFIRMED -> READY -> COMPLETED, or CANCELLED at any point.
    status: Mapped[str] = mapped_column(String(30), default="REQUESTED", index=True)
    # How it ended, for supplier reliability: HONOURED, WRONG_FIT, OUT_OF_STOCK,
    # PRICE_CHANGED or NO_SHOW (the buyer's doing, so it does not count against the supplier).
    outcome: Mapped[str | None] = mapped_column(String(30), index=True)
    # The buyer's car and VIN go to the supplier so fit can be checked before pickup.
    vehicle_id: Mapped[str | None] = mapped_column(
        ForeignKey("vehicles.id", ondelete="SET NULL"), index=True
    )
    vehicle_label: Mapped[str | None] = mapped_column(String(300))
    vin: Mapped[str | None] = mapped_column(String(17))
    note: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    product: Mapped[Product] = relationship()
    supplier_offer: Mapped[SupplierOffer] = relationship()
    search_event: Mapped[SearchEvent | None] = relationship()


class PartRequest(Base):
    """A part the buyer could not find, passed to suppliers instead of a dead end."""

    __tablename__ = "part_requests"

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(100), index=True)
    query: Mapped[str] = mapped_column(String(300))
    vehicle_id: Mapped[str | None] = mapped_column(ForeignKey("vehicles.id", ondelete="SET NULL"))
    vehicle_label: Mapped[str | None] = mapped_column(String(300))
    vin: Mapped[str | None] = mapped_column(String(17))
    contact: Mapped[str] = mapped_column(String(200))
    note: Mapped[str | None] = mapped_column(Text)
    # OPEN -> ANSWERED -> CLOSED
    status: Mapped[str] = mapped_column(String(20), default="OPEN", index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )


class FitReport(Base):
    """A buyer saying whether a part fitted their car, to catch wrong fitment data."""

    __tablename__ = "fit_reports"

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(100), index=True)
    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    vehicle_id: Mapped[str | None] = mapped_column(
        ForeignKey("vehicles.id", ondelete="SET NULL"), index=True
    )
    vehicle_label: Mapped[str | None] = mapped_column(String(300))
    fits: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )


class SearchEventAction(Base):
    __tablename__ = "search_event_actions"

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    search_event_id: Mapped[int] = mapped_column(
        ForeignKey("search_events.id", ondelete="CASCADE"), index=True
    )
    action: Mapped[str] = mapped_column(String(40), index=True)
    product_id: Mapped[str | None] = mapped_column(
        ForeignKey("products.id", ondelete="SET NULL"), index=True
    )
    supplier_id: Mapped[int | None] = mapped_column(
        ForeignKey("suppliers.id", ondelete="SET NULL"), index=True
    )
    supplier_offer_id: Mapped[int | None] = mapped_column(
        ForeignKey("supplier_offers.id", ondelete="SET NULL"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )

    search_event: Mapped[SearchEvent] = relationship()


Index("ix_products_name_brand", Product.normalized_name, Product.brand_id)
Index("ix_products_searchable_status", Product.is_searchable, Product.audit_status)


class SearchAlias(Base):
    """Admin-curated search vocabulary layered over app.search_vocabulary."""

    __tablename__ = "search_aliases"
    __table_args__ = (
        UniqueConstraint("kind", "alias", name="uq_search_alias_kind_alias"),
        CheckConstraint("kind IN ('product', 'vehicle')", name="ck_search_alias_kind"),
    )

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    kind: Mapped[str] = mapped_column(String(20), index=True)
    alias: Mapped[str] = mapped_column(String(200))
    canonical: Mapped[str] = mapped_column(String(200))
    source_query: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class ProductAttribute(Base):
    __tablename__ = "product_attributes"
    __table_args__ = (
        UniqueConstraint("product_id", "attribute_code", name="uq_product_attribute"),
    )

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    attribute_code: Mapped[str] = mapped_column(String(100))
    value: Mapped[str] = mapped_column(Text)
    unit: Mapped[str | None] = mapped_column(String(50))
    source: Mapped[str | None] = mapped_column(String(50))

    product: Mapped[Product] = relationship(back_populates="attributes")


class SearchSynonym(Base):
    """Workbook "Search Synonyms": alternative names (translit, official) for catalog targets."""

    __tablename__ = "search_synonyms"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    target_type: Mapped[str] = mapped_column(String(30), index=True)
    target_id: Mapped[str] = mapped_column(String(64), index=True)
    term: Mapped[str] = mapped_column(String(300))
    lang: Mapped[str | None] = mapped_column(String(10))
    synonym_type: Mapped[str | None] = mapped_column(String(30))


class Supersession(Base):
    __tablename__ = "supersessions"

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    old_number_raw: Mapped[str] = mapped_column(String(200))
    old_brand_id: Mapped[int | None] = mapped_column(ForeignKey("brands.id", ondelete="SET NULL"))
    old_product_id: Mapped[str | None] = mapped_column(
        ForeignKey("products.id", ondelete="SET NULL")
    )
    new_product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    interchangeability: Mapped[str | None] = mapped_column(String(30))
    effective_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    source: Mapped[str | None] = mapped_column(String(100))
    notes: Mapped[str | None] = mapped_column(Text)


class KitComponent(Base):
    __tablename__ = "kit_components"
    __table_args__ = (
        UniqueConstraint("kit_product_id", "component_product_id", name="uq_kit_component"),
    )

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    kit_product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    component_product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    qty: Mapped[int] = mapped_column(Integer, default=1)
    notes: Mapped[str | None] = mapped_column(Text)


class ProductMedia(Base):
    __tablename__ = "product_media"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    media_type: Mapped[str] = mapped_column(String(30))
    url_or_path: Mapped[str] = mapped_column(Text)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    source: Mapped[str | None] = mapped_column(String(100))
    license_note: Mapped[str | None] = mapped_column(Text)


class CatalogReviewItem(Base):
    """Workbook "Review Queue": raw rows a person still has to confirm."""

    __tablename__ = "catalog_review_items"

    raw_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    supplier: Mapped[str | None] = mapped_column(String(200))
    product_id: Mapped[str | None] = mapped_column(
        ForeignKey("products.id", ondelete="SET NULL"), index=True
    )
    raw_name: Mapped[str | None] = mapped_column(Text)
    parsed_product_name: Mapped[str | None] = mapped_column(Text)
    brand: Mapped[str | None] = mapped_column(String(200))
    reference: Mapped[str | None] = mapped_column(String(200))
    vehicle_raw: Mapped[str | None] = mapped_column(Text)
    review_reason: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), index=True)
    reviewer: Mapped[str | None] = mapped_column(String(100))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    resolution_note: Mapped[str | None] = mapped_column(Text)


class ProductAudit(Base):
    """Workbook "Cross Supplier Audit" (its CONFLICT rows are the "Merge Conflicts" sheet).

    A product can have several findings, e.g. analog-group and duplicate checks.
    """

    __tablename__ = "product_audits"

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    brand: Mapped[str | None] = mapped_column(String(300))
    reference: Mapped[str | None] = mapped_column(String(300))
    master_name: Mapped[str | None] = mapped_column(Text)
    supplier_count: Mapped[int | None] = mapped_column(Integer)
    suppliers: Mapped[str | None] = mapped_column(Text)
    cross_name_similarity: Mapped[str | None] = mapped_column(String(30))
    internal_collision: Mapped[str | None] = mapped_column(String(10))
    positions: Mapped[str | None] = mapped_column(Text)
    sides: Mapped[str | None] = mapped_column(Text)
    merge_status: Mapped[str] = mapped_column(String(30), index=True)
    audit_reason: Mapped[str | None] = mapped_column(Text)
    source_rows: Mapped[str | None] = mapped_column(Text)
    attr_conflict: Mapped[str | None] = mapped_column(Text)


class CatalogSetting(Base):
    __tablename__ = "catalog_settings"

    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    value: Mapped[str | None] = mapped_column(Text)
    note: Mapped[str | None] = mapped_column(Text)


class CatalogListValue(Base):
    """Workbook "Lists": allowed values that drive the catalog form dropdowns."""

    __tablename__ = "catalog_list_values"
    __table_args__ = (UniqueConstraint("list_name", "value", name="uq_catalog_list_value"),)

    id: Mapped[int] = mapped_column(BIGINT_PK, primary_key=True, autoincrement=True)
    list_name: Mapped[str] = mapped_column(String(100), index=True)
    value: Mapped[str] = mapped_column(String(200))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)


class CatalogFieldDoc(Base):
    """Workbook "Data Dictionary": per-column help text shown in the catalog forms."""

    __tablename__ = "catalog_field_docs"

    sheet: Mapped[str] = mapped_column(String(100), primary_key=True)
    column: Mapped[str] = mapped_column(String(100), primary_key=True)
    required: Mapped[bool] = mapped_column(Boolean, default=False)
    kind: Mapped[str | None] = mapped_column(String(50))
    allowed_values: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
