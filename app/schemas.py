from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ReferenceOut(BaseModel):
    number: str
    type: str

    model_config = ConfigDict(from_attributes=True)


class VehicleOut(BaseModel):
    id: str
    make: str | None
    model: str
    generation: str | None
    year_from: int | None = None
    year_to: int | None = None

    model_config = ConfigDict(from_attributes=True)


class FitmentOut(BaseModel):
    vehicle: VehicleOut
    source_vehicle_text: str | None
    position: str | None = None
    side: str | None = None
    qty_per_vehicle: int | None = None
    # Conditions for the fit, e.g. "KPP: AT" or "check the model year".
    condition_note: str | None = None

    model_config = ConfigDict(from_attributes=True)


class SupplierSummary(BaseModel):
    id: int
    name: str
    supplier_type: str | None = None
    phone: str | None = None
    telegram: str | None = None
    address: str | None = None
    city: str | None = None
    work_hours: str | None = None
    map_url: str | None = None
    verified: bool = False
    member_since: datetime | None = None
    # Shown only once enough reservations have an outcome to mean something.
    reliability_score: Decimal | None = None
    reliability_sample: int = 0

    model_config = ConfigDict(from_attributes=True)


class OfferOut(BaseModel):
    id: int
    supplier_id: int
    supplier_name: str
    supplier: SupplierSummary
    supplier_sku: str | None
    price: Decimal | None
    currency: str
    stock_qty: int | None
    warehouse: str | None
    updated_at: datetime | None
    freshness_status: Literal["FRESH", "RECENT", "STALE", "OUTDATED", "UNKNOWN"]
    data_status: str
    part_origin: str | None = None
    condition: str | None = None
    warranty_months: int | None = None
    warranty_km: int | None = None
    return_days: int | None = None
    # 0 means in stock now; more means "to order, arrives in N days".
    lead_time_days: int | None = None
    # The seller's label from their price list, e.g. NEW_ARRIVAL or DISCOUNT (with percent).
    promo: str | None = None
    discount_percent: int | None = None
    pack_qty: int | None = None

    model_config = ConfigDict(from_attributes=True)


class BrandOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class CategoryOut(BaseModel):
    id: str
    name_uz: str
    name_ru: str | None
    name_en: str | None

    model_config = ConfigDict(from_attributes=True)


class PartTypeOut(CategoryOut):
    part_count: int


class PartGroupOut(PartTypeOut):
    types: list[PartTypeOut]


class ProductSearchResult(BaseModel):
    id: str
    name: str
    name_ru: str | None = None
    name_en: str | None = None
    brand: BrandOut | None
    category: CategoryOut | None = None
    universal: bool = False
    origin: str | None
    position: str | None
    side: str | None
    engine_hint: str | None
    audit_status: str
    reference_numbers: list[ReferenceOut]
    vehicle_fitments: list[FitmentOut]
    supplier_offers: list[OfferOut]
    offers: list[OfferOut]
    # ORIGINAL (carmaker part), KOREA (Korean-made or OE supplier), CHINA, BUDGET or OTHER.
    quality: str | None = None
    country_of_origin: str | None = None
    relevance_score: float
    result_group: Literal["EXACT", "COMPATIBLE", "RELATED"] = "RELATED"
    # Reservations in the last 90 days, for the "often reserved" badge.
    reservation_count: int = 0


class BrandFacetOut(BaseModel):
    id: int
    name: str
    count: int


class VehicleFilterOut(BaseModel):
    label: str
    vehicle_ids: list[str]


class SearchResponse(BaseModel):
    query: str
    normalized_query: str
    corrected_query: str | None = None
    vehicle_filter: VehicleFilterOut | None = None
    category_filter: CategoryOut | None = None
    total: int
    # Matches per part type across every page, for "narrow down by part type".
    category_counts: dict[str, int] = Field(default_factory=dict)
    # Matches per brand and per quality grade, before those two filters apply.
    brand_facets: list[BrandFacetOut] = Field(default_factory=list)
    quality_counts: dict[str, int] = Field(default_factory=dict)
    items: list[ProductSearchResult]
    search_event_id: int | None = None
    search_debug: dict | None = None
    parsed_query_internal: dict = Field(default_factory=dict, exclude=True)
    result_group_distribution_internal: dict[str, int] = Field(default_factory=dict, exclude=True)


class ProductAttributeOut(BaseModel):
    attribute_code: str
    value: str
    unit: str | None = None

    model_config = ConfigDict(from_attributes=True)


class RelatedProductOut(BaseModel):
    id: str
    name: str
    name_ru: str | None = None
    name_en: str | None = None
    brand: BrandOut | None
    category: CategoryOut | None = None
    # SAME_NUMBER: another brand of the same part number (analog);
    # SAME_TYPE: another option of the same part type for the same car;
    # COMPLETE_THE_JOB: a part usually replaced together with this one.
    relation: Literal["SAME_NUMBER", "SAME_TYPE", "COMPLETE_THE_JOB"]
    shared_number: str | None = None
    lowest_price: Decimal | None = None
    currency: str | None = None
    offer_count: int = 0
    quality: str | None = None
    # False for the same number in another size or side (STD and 0.25 pistons).
    same_variant: bool = True


class FitReportSummary(BaseModel):
    vehicle_id: str | None
    vehicle_label: str | None
    fits: int
    does_not_fit: int


class SuggestedProductOut(BaseModel):
    id: str
    name: str
    name_ru: str | None = None
    name_en: str | None = None
    brand: BrandOut | None
    category: CategoryOut | None = None


class SuggestResponse(BaseModel):
    query: str
    corrected_query: str | None = None
    part_types: list[PartTypeOut] = Field(default_factory=list)
    products: list[SuggestedProductOut] = Field(default_factory=list)


class ProductDetail(BaseModel):
    id: str
    name: str
    name_ru: str | None = None
    name_en: str | None = None
    brand: BrandOut | None
    category: CategoryOut | None = None
    universal: bool = False
    origin: str | None
    position: str | None
    side: str | None
    engine_hint: str | None
    audit_status: str
    reference_numbers: list[ReferenceOut]
    vehicle_fitments: list[FitmentOut]
    supplier_offers: list[OfferOut]
    offers: list[OfferOut]
    # ORIGINAL (carmaker part), KOREA (Korean-made or OE supplier), CHINA, BUDGET or OTHER.
    quality: str | None = None
    country_of_origin: str | None = None
    # Category attributes such as repair_size, placement, transmission, engine_type.
    attributes: list[ProductAttributeOut] = Field(default_factory=list)
    reservation_count: int = 0
    alternatives: list[RelatedProductOut] = Field(default_factory=list)
    complete_the_job: list[RelatedProductOut] = Field(default_factory=list)
    fit_reports: list[FitReportSummary] = Field(default_factory=list)


class SearchEventCreate(BaseModel):
    session_id: str
    user_id: str | None = None
    query_raw: str
    query_normalized: str | None = None
    result_count: int = 0
    search_time_ms: float = 0
    top_product_ids: list[str] = Field(default_factory=list)


class SearchEventOut(BaseModel):
    id: int
    user_id: str | None
    session_id: str
    query_raw: str
    query_normalized: str
    result_count: int
    search_time_ms: float
    top_product_ids: list[str]
    clicked_product_id: str | None
    clicked_supplier_id: int | None
    action: str | None
    detected_vehicle: str | None
    detected_product_terms: list[str]
    detected_reference: str | None
    detected_brand: str | None
    detected_position: str | None
    detected_side: str | None
    result_group_distribution: dict[str, int]
    top_result_score: float | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SearchClickCreate(BaseModel):
    product_id: str | None = None
    supplier_id: int | None = None


class SearchActionCreate(BaseModel):
    action: Literal[
        "contact_supplier",
        "reserve",
        "supplier_offer_view",
        "supplier_click",
        "phone_click",
        "telegram_click",
        "reservation_request",
        "basket_add",
    ]
    product_id: str | None = None
    supplier_id: int | None = None
    supplier_offer_id: int | None = None


VIN_PATTERN = r"^[A-HJ-NPR-Z0-9]{17}$"  # 17 characters; I, O and Q are never used


class ReservationCreate(BaseModel):
    session_id: str = Field(max_length=100)
    user_id: str | None = None
    search_event_id: int | None = None
    product_id: str
    supplier_offer_id: int
    quantity: int = Field(default=1, ge=1, le=1000)
    phone: str | None = Field(default=None, max_length=50)
    vehicle_id: str | None = Field(default=None, max_length=64)
    vehicle_label: str | None = Field(default=None, max_length=300)
    vin: str | None = Field(default=None, pattern=VIN_PATTERN)
    note: str | None = Field(default=None, max_length=1000)


class ReservationOut(BaseModel):
    id: int
    session_id: str
    user_id: str | None
    product_id: str
    supplier_offer_id: int
    quantity: int
    phone: str | None
    status: str
    vehicle_label: str | None = None
    vin: str | None = None
    note: str | None = None
    basket_id: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReservationCancel(BaseModel):
    """The browser's session id proves the reservation is the buyer's own."""

    session_id: str = Field(min_length=8, max_length=100)


class MyReservationOut(BaseModel):
    id: int
    status: str
    quantity: int
    vehicle_label: str | None
    vin: str | None
    note: str | None
    created_at: datetime
    updated_at: datetime | None
    product_id: str
    product_name: str
    product_name_ru: str | None = None
    product_name_en: str | None = None
    reference_numbers: list[str]
    supplier: SupplierSummary
    price: Decimal | None
    currency: str
    basket_id: str | None = None


class PartRequestCreate(BaseModel):
    session_id: str = Field(max_length=100)
    query: str = Field(min_length=1, max_length=300)
    contact: str = Field(min_length=3, max_length=200)
    vehicle_id: str | None = Field(default=None, max_length=64)
    vehicle_label: str | None = Field(default=None, max_length=300)
    vin: str | None = Field(default=None, pattern=VIN_PATTERN)
    note: str | None = Field(default=None, max_length=1000)


class PartRequestOut(BaseModel):
    id: int
    query: str
    contact: str
    vehicle_label: str | None
    vin: str | None
    note: str | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PartRequestUpdate(BaseModel):
    status: Literal["OPEN", "ANSWERED", "CLOSED"]


class FitReportCreate(BaseModel):
    session_id: str = Field(max_length=100)
    fits: bool
    vehicle_id: str | None = Field(default=None, max_length=64)
    vehicle_label: str | None = Field(default=None, max_length=300)


class AdminReservationOut(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime | None
    status: str
    outcome: str | None
    quantity: int
    phone: str | None
    vehicle_label: str | None
    vin: str | None
    note: str | None
    product_id: str
    product_name: str
    supplier_id: int
    supplier_name: str
    supplier_sku: str | None


class ReservationUpdate(BaseModel):
    status: Literal["REQUESTED", "CONFIRMED", "READY", "COMPLETED", "CANCELLED"] | None = None
    outcome: (
        Literal["HONOURED", "WRONG_FIT", "OUT_OF_STOCK", "PRICE_CHANGED", "NO_SHOW"] | None
    ) = None


class AdminFitReportOut(BaseModel):
    product_id: str
    product_name: str
    vehicle_label: str | None
    fits: int
    does_not_fit: int
    last_report: datetime


class SupplierUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=200)
    phone: str | None = None
    telegram: str | None = None
    address: str | None = None
    is_active: bool | None = None
    city: str | None = Field(default=None, max_length=200)
    legal_name: str | None = Field(default=None, max_length=300)
    inn: str | None = Field(default=None, pattern=r"^\d{9}$|^\d{14}$")
    licence_number: str | None = Field(default=None, max_length=100)
    work_hours: str | None = Field(default=None, max_length=200)
    map_url: str | None = Field(default=None, max_length=500, pattern=r"^https?://")
    # Ticking "verified" records when the team checked the documents.
    verified: bool | None = None


class SupplierAdminOut(BaseModel):
    id: int
    name: str
    phone: str | None
    telegram: str | None
    address: str | None
    is_active: bool
    created_at: datetime
    active_offers_count: int
    latest_data_update: datetime | None
    city: str | None = None
    legal_name: str | None = None
    inn: str | None = None
    licence_number: str | None = None
    work_hours: str | None = None
    map_url: str | None = None
    verified_at: datetime | None = None
    reliability_score: Decimal | None = None
    reliability_sample: int = 0


class SupplierProductOut(BaseModel):
    id: str
    name: str
    name_ru: str | None = None
    name_en: str | None = None
    brand: str | None
    supplier_sku: str | None
    price: Decimal | None
    currency: str
    stock_qty: int | None
    warehouse: str | None
    updated_at: datetime | None
    freshness_status: str
    data_status: str


class SupplierDetailOut(BaseModel):
    id: int
    name: str
    phone: str | None
    telegram: str | None
    address: str | None
    trust: SupplierSummary | None = None
    brands: list[str]
    active_offers_count: int
    last_data_update: datetime | None
    products: list[SupplierProductOut]


class SupplierImportOut(BaseModel):
    id: int
    supplier_id: int
    supplier_name: str
    source_filename: str | None
    source_type: str
    rows_received: int
    rows_matched: int
    unmatched_rows: int
    updated_offers: int
    new_offers: int
    errors: int
    status: str
    imported_at: datetime


class PilotFeedbackCreate(BaseModel):
    found_correct_part: bool
    correct_in_top_3: bool = False
    user_rating: int | None = Field(default=None, ge=1, le=5)
    comment: str | None = None


class PilotFeedbackOut(PilotFeedbackCreate):
    id: int
    search_event_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VehicleOptionOut(BaseModel):
    id: str
    make: str | None
    model: str
    generation: str | None
    part_count: int


class SearchAliasCreate(BaseModel):
    kind: Literal["product", "vehicle"]
    alias: str = Field(min_length=1, max_length=200)
    canonical: str = Field(min_length=1, max_length=200)
    source_query: str | None = Field(default=None, max_length=500)


class SearchAliasOut(BaseModel):
    id: int
    kind: str
    alias: str
    canonical: str
    source_query: str | None
    created_at: datetime | None
    source_query_result_count: int | None = None

    model_config = ConfigDict(from_attributes=True)


class SearchAliasTargetsOut(BaseModel):
    product: list[str]
    vehicle: list[str]


class AdminLogin(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=200)


class SupplierCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    phone: str | None = Field(default=None, max_length=50)
    telegram: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=200)


class PriceListImportOut(BaseModel):
    """What a seller's price list added: parts, offers, cars, and names to look at."""

    import_id: int
    supplier_id: int
    rows: int
    parts_created: int
    parts_reused: int
    offers_created: int
    offers_updated: int
    offers_closed: int
    rows_without_car: int
    cars_created: list[str]
    unrecognised: list[str]


class JobPartOut(BaseModel):
    type_id: str
    type_name_uz: str
    type_name_ru: str | None = None
    type_name_en: str | None = None
    position: str | None = None
    # The part to pick for the buyer's car, and how many other choices there are.
    product: ProductSearchResult | None = None
    options: int = 0


class JobOut(BaseModel):
    id: str
    name_uz: str
    name_ru: str
    name_en: str
    icon: str
    parts: list[JobPartOut]
    available: int = 0


class BasketItemIn(BaseModel):
    product_id: str = Field(max_length=64)
    supplier_offer_id: int
    quantity: int = Field(default=1, ge=1, le=1000)


class BasketCreate(BaseModel):
    """Several parts, possibly from several sellers, reserved in one go."""

    session_id: str = Field(min_length=8, max_length=100)
    items: list[BasketItemIn] = Field(min_length=1, max_length=30)
    phone: str | None = Field(default=None, max_length=50)
    vehicle_id: str | None = Field(default=None, max_length=64)
    vehicle_label: str | None = Field(default=None, max_length=300)
    vin: str | None = Field(default=None, pattern=VIN_PATTERN)
    note: str | None = Field(default=None, max_length=1000)
    search_event_id: int | None = None


class BasketOut(BaseModel):
    basket_id: str
    reservations: list[ReservationOut]


class BasketOfferOut(BaseModel):
    """An offer as the basket shows it: the part, the seller and the current terms."""

    offer: OfferOut
    product_id: str
    name: str
    name_ru: str | None = None
    name_en: str | None = None
    brand: BrandOut | None = None
    category: CategoryOut | None = None
    reference_numbers: list[str] = Field(default_factory=list)


class SellerCardOut(BaseModel):
    supplier: SupplierSummary
    active_offers_count: int
    priced_offers_count: int
    brands: list[str]
    last_data_update: datetime | None


class SellerApplicationCreate(BaseModel):
    business_name: str = Field(min_length=2, max_length=200)
    contact_name: str | None = Field(default=None, max_length=200)
    phone: str = Field(min_length=7, max_length=50)
    telegram: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=200)
    address: str | None = Field(default=None, max_length=500)
    cars: str | None = Field(default=None, max_length=300)
    note: str | None = Field(default=None, max_length=1000)


class SellerApplicationOut(SellerApplicationCreate):
    id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SellerApplicationUpdate(BaseModel):
    status: Literal["NEW", "CONTACTED", "ONBOARDED", "DECLINED"]
