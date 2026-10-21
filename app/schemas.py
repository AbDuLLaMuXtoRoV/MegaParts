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

    model_config = ConfigDict(from_attributes=True)


class FitmentOut(BaseModel):
    vehicle: VehicleOut
    source_vehicle_text: str | None

    model_config = ConfigDict(from_attributes=True)


class SupplierSummary(BaseModel):
    id: int
    name: str
    phone: str | None = None
    telegram: str | None = None

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
    freshness_status: Literal["FRESH", "RECENT", "STALE", "UNKNOWN"]
    data_status: str

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
    relevance_score: float
    result_group: Literal["EXACT", "COMPATIBLE", "RELATED"] = "RELATED"


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
    items: list[ProductSearchResult]
    search_event_id: int | None = None
    search_debug: dict | None = None
    parsed_query_internal: dict = Field(default_factory=dict, exclude=True)
    result_group_distribution_internal: dict[str, int] = Field(default_factory=dict, exclude=True)


class SuggestedProductOut(BaseModel):
    id: str
    name: str
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
    ]
    product_id: str | None = None
    supplier_id: int | None = None
    supplier_offer_id: int | None = None


class ReservationCreate(BaseModel):
    session_id: str
    user_id: str | None = None
    search_event_id: int | None = None
    product_id: str
    supplier_offer_id: int
    quantity: int = Field(default=1, ge=1)
    phone: str | None = None


class ReservationOut(BaseModel):
    id: int
    session_id: str
    user_id: str | None
    product_id: str
    supplier_offer_id: int
    quantity: int
    phone: str | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SupplierUpdate(BaseModel):
    phone: str | None = None
    telegram: str | None = None
    address: str | None = None
    is_active: bool | None = None


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


class SupplierProductOut(BaseModel):
    id: str
    name: str
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
