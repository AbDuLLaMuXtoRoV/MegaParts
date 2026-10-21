"""IRIZON profile: view and edit the full catalog record of every product.

Every route lives under /api/admin, so the admin login gate in app.main covers it.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.auth import COOKIE_NAME, session_user
from app.catalog import product_loading_options, refresh_product
from app.config import get_settings
from app.database import get_session
from app.models import (
    Brand,
    CatalogFieldDoc,
    CatalogListValue,
    CatalogReviewItem,
    Category,
    Fitment,
    Product,
    ProductAttribute,
    ProductAudit,
    ReferenceNumber,
    Supplier,
    SupplierOffer,
    Vehicle,
)
from app.normalization import normalize_code, normalize_text

router = APIRouter(prefix="/api/admin/catalog", tags=["catalog admin"])
SessionDep = Annotated[Session, Depends(get_session)]

# Field -> workbook "Lists" column whose values it must use.
PRODUCT_LISTS = {"origin": "origin", "status": "product_status", "unit": "unit"}
REFERENCE_LISTS = {"type": "ref_type", "cross_source": "cross_source", "confidence": "confidence"}
FITMENT_LISTS = {
    "position": "position",
    "side": "side",
    "vertical": "vertical",
    "fitment_source": "fitment_source",
    "confidence": "confidence",
}
OFFER_LISTS = {"currency": "currency", "price_type": "price_type", "condition": "condition"}
SUPPLIER_LISTS = {
    "supplier_type": "supplier_type",
    "default_currency": "currency",
    "integration": "integration",
}


class AttributeIn(BaseModel):
    attribute_code: str = Field(min_length=1, max_length=100)
    value: str = Field(max_length=2000)
    unit: str | None = Field(default=None, max_length=50)
    source: str | None = Field(default=None, max_length=50)


class ReferenceIn(BaseModel):
    id: int | None = None
    number: str = Field(min_length=1, max_length=200)
    type: str = Field(min_length=1, max_length=50)
    number_brand_id: int | None = None
    cross_source: str | None = None
    confidence: str | None = None
    verified: bool = False
    notes: str | None = Field(default=None, max_length=2000)


class FitmentIn(BaseModel):
    id: int | None = None
    vehicle_id: str = Field(min_length=1, max_length=64)
    position: str | None = None
    side: str | None = None
    vertical: str | None = None
    qty_per_vehicle: int | None = Field(default=None, ge=0, le=1000)
    year_from: int | None = Field(default=None, ge=1900, le=2100)
    year_to: int | None = Field(default=None, ge=1900, le=2100)
    condition_note: str | None = Field(default=None, max_length=2000)
    fitment_source: str | None = None
    confidence: str | None = None
    verified: bool = False
    source_vehicle_text: str | None = Field(default=None, max_length=500)


class OfferIn(BaseModel):
    id: int | None = None
    supplier_id: int
    supplier_sku: str | None = Field(default=None, max_length=200)
    price: Decimal | None = Field(default=None, ge=0, max_digits=18, decimal_places=2)
    currency: str = Field(default="UZS", min_length=3, max_length=3)
    price_type: str | None = None
    stock_qty: int | None = Field(default=None, ge=0)
    warehouse: str | None = Field(default=None, max_length=200)
    lead_time_days: int | None = Field(default=None, ge=0, le=3650)
    min_order_qty: int | None = Field(default=None, ge=0)
    condition: str | None = None
    is_active: bool = True


class ProductIn(BaseModel):
    name: str = Field(min_length=1, max_length=500)
    name_ru: str | None = Field(default=None, max_length=500)
    name_en: str | None = Field(default=None, max_length=500)
    brand_id: int | None = None
    category_id: str = Field(min_length=1, max_length=64)
    article_number: str | None = Field(default=None, max_length=200)
    origin: str = Field(min_length=1, max_length=100)
    status: str = Field(min_length=1, max_length=30)
    unit: str = Field(min_length=1, max_length=20)
    pack_qty: int | None = Field(default=None, ge=0)
    weight_kg: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=3)
    length_mm: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=1)
    width_mm: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=1)
    height_mm: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=1)
    ean: str | None = Field(default=None, max_length=32)
    country_of_origin: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=5000)
    universal: bool = False
    attributes: list[AttributeIn] = Field(default_factory=list)
    references: list[ReferenceIn] = Field(default_factory=list)
    fitments: list[FitmentIn] = Field(default_factory=list)
    offers: list[OfferIn] = Field(default_factory=list)
    # The record version the editor loaded; a mismatch means someone else saved first.
    expected_updated_at: datetime | None = None


class SupplierProfileIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    supplier_type: str | None = None
    city: str | None = Field(default=None, max_length=200)
    address: str | None = Field(default=None, max_length=1000)
    contact: str | None = Field(default=None, max_length=1000)
    phone: str | None = Field(default=None, max_length=50)
    telegram: str | None = Field(default=None, max_length=100)
    default_currency: str | None = None
    integration: str | None = None
    update_frequency_days: int | None = Field(default=None, ge=0, le=3650)
    default_lead_time_days: int | None = Field(default=None, ge=0, le=3650)
    is_active: bool = True

    model_config = ConfigDict(str_strip_whitespace=True)


def _blank_to_none(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def _list_values(session: Session) -> dict[str, list[str]]:
    lists: dict[str, list[str]] = {}
    for row in session.scalars(
        select(CatalogListValue).order_by(CatalogListValue.list_name, CatalogListValue.sort_order)
    ):
        lists.setdefault(row.list_name, []).append(row.value)
    return lists


class _Validator:
    """Collects every problem so the form can show them all at once."""

    def __init__(self, lists: dict[str, list[str]]) -> None:
        self.lists = lists
        self.errors: list[dict[str, str]] = []

    def add(self, field: str, message: str) -> None:
        self.errors.append({"field": field, "message": message})

    def choice(self, field: str, value: str | None, list_name: str) -> None:
        allowed = self.lists.get(list_name)
        if value and allowed and value not in allowed:
            self.add(field, f"Must be one of: {', '.join(allowed)}")

    def raise_if_any(self) -> None:
        if self.errors:
            raise HTTPException(status_code=422, detail={"errors": self.errors})


def _vehicle_label(vehicle: Vehicle) -> str:
    years = (
        f"{vehicle.year_from or ''}–{vehicle.year_to or ''}"
        if vehicle.year_from or vehicle.year_to
        else ""
    )
    return " · ".join(
        filter(None, [f"{vehicle.make or ''} {vehicle.model}".strip(), vehicle.generation, years])
    )


def _decimal_out(value: Decimal | None) -> str | None:
    return None if value is None else format(value.normalize(), "f")


def product_record(session: Session, product: Product) -> dict:
    audits = session.scalars(
        select(ProductAudit).where(ProductAudit.product_id == product.id).order_by(ProductAudit.id)
    ).all()
    reviews = session.scalars(
        select(CatalogReviewItem)
        .where(CatalogReviewItem.product_id == product.id)
        .order_by(CatalogReviewItem.raw_id)
    ).all()
    category_attributes = product.category.attributes if product.category else []
    present = {attribute.attribute_code for attribute in product.attributes}
    return {
        "id": product.id,
        "name": product.name,
        "name_ru": product.name_ru,
        "name_en": product.name_en,
        "brand_id": product.brand_id,
        "category_id": product.category_id,
        "article_number": product.article_number,
        "origin": product.origin,
        "status": product.status,
        "unit": product.unit,
        "pack_qty": product.pack_qty,
        "weight_kg": _decimal_out(product.weight_kg),
        "length_mm": _decimal_out(product.length_mm),
        "width_mm": _decimal_out(product.width_mm),
        "height_mm": _decimal_out(product.height_mm),
        "ean": product.ean,
        "country_of_origin": product.country_of_origin,
        "description": product.description,
        "universal": product.universal,
        "merge_basis": product.merge_basis,
        "source_rows": product.source_rows,
        "audit_status": product.audit_status,
        "is_searchable": product.is_searchable,
        "updated_at": product.updated_at,
        "missing_required_attributes": [
            attribute.attribute_code
            for attribute in category_attributes
            if attribute.required and attribute.attribute_code not in present
        ],
        "attributes": [
            {
                "attribute_code": attribute.attribute_code,
                "value": attribute.value,
                "unit": attribute.unit,
                "source": attribute.source,
            }
            for attribute in sorted(product.attributes, key=lambda item: item.attribute_code)
        ],
        "references": [
            {
                "id": reference.id,
                "number": reference.number,
                "type": reference.type,
                "number_brand_id": reference.number_brand_id,
                "cross_source": reference.cross_source,
                "confidence": reference.confidence,
                "verified": reference.verified,
                "notes": reference.notes,
            }
            for reference in sorted(product.reference_numbers, key=lambda item: item.id or 0)
        ],
        "fitments": [
            {
                "id": fitment.id,
                "vehicle_id": fitment.vehicle_id,
                "vehicle_label": _vehicle_label(fitment.vehicle),
                "position": fitment.position,
                "side": fitment.side,
                "vertical": fitment.vertical,
                "qty_per_vehicle": fitment.qty_per_vehicle,
                "year_from": fitment.year_from,
                "year_to": fitment.year_to,
                "condition_note": fitment.condition_note,
                "fitment_source": fitment.fitment_source,
                "confidence": fitment.confidence,
                "verified": fitment.verified,
                "source_vehicle_text": fitment.source_vehicle_text,
            }
            for fitment in sorted(product.fitments, key=lambda item: item.id or 0)
        ],
        "offers": [
            {
                "id": offer.id,
                "supplier_id": offer.supplier_id,
                "supplier_sku": offer.supplier_sku,
                "price": _decimal_out(offer.price),
                "currency": offer.currency,
                "price_type": offer.price_type,
                "stock_qty": offer.stock_qty,
                "warehouse": offer.warehouse,
                "lead_time_days": offer.lead_time_days,
                "min_order_qty": offer.min_order_qty,
                "condition": offer.condition,
                "is_active": offer.is_active,
                "data_status": offer.data_status,
                "updated_at": offer.updated_at,
            }
            for offer in sorted(product.supplier_offers, key=lambda item: item.id or 0)
        ],
        "audits": [
            {"merge_status": audit.merge_status, "audit_reason": audit.audit_reason}
            for audit in audits
        ],
        "review_items": [
            {
                "raw_id": item.raw_id,
                "raw_name": item.raw_name,
                "review_reason": item.review_reason,
                "status": item.status,
            }
            for item in reviews
        ],
    }


def _load_product(session: Session, product_id: str) -> Product:
    product = session.scalar(
        select(Product).where(Product.id == product_id).options(*product_loading_options())
    )
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def _next_product_id(session: Session) -> str:
    numbers = [
        int(match[1])
        for product_id in session.scalars(select(Product.id))
        if (match := re.fullmatch(r"P-(\d+)", product_id))
    ]
    return f"P-{max(numbers, default=0) + 1:06d}"


def _validate(session: Session, payload: ProductIn) -> _Validator:
    check = _Validator(_list_values(session))
    if not _blank_to_none(payload.name):
        check.add("name", "Uzbek name is required")
    for field, list_name in PRODUCT_LISTS.items():
        check.choice(field, getattr(payload, field), list_name)
    if session.get(Category, payload.category_id) is None:
        check.add("category_id", "Unknown category")
    if payload.brand_id is not None and session.get(Brand, payload.brand_id) is None:
        check.add("brand_id", "Unknown brand")

    category = session.get(Category, payload.category_id)
    number_attributes = {
        attribute.attribute_code
        for attribute in (category.attributes if category else [])
        if attribute.data_type == "NUMBER"
    }
    codes: set[str] = set()
    for index, attribute in enumerate(payload.attributes):
        if attribute.attribute_code in codes:
            check.add(f"attributes.{index}.attribute_code", "Attribute listed twice")
        codes.add(attribute.attribute_code)
        if attribute.attribute_code in number_attributes and attribute.value.strip():
            try:
                Decimal(attribute.value.strip().replace(",", "."))
            except ArithmeticError:
                check.add(f"attributes.{index}.value", "Must be a number")

    reference_keys: set[tuple[str, str]] = set()
    for index, reference in enumerate(payload.references):
        for field, list_name in REFERENCE_LISTS.items():
            check.choice(f"references.{index}.{field}", getattr(reference, field), list_name)
        key = (normalize_code(reference.number), reference.type)
        if not key[0]:
            check.add(f"references.{index}.number", "Must contain letters or digits")
        elif key in reference_keys:
            check.add(f"references.{index}.number", "Same number and type listed twice")
        reference_keys.add(key)

    vehicles_seen: set[str] = set()
    for index, fitment in enumerate(payload.fitments):
        for field, list_name in FITMENT_LISTS.items():
            check.choice(f"fitments.{index}.{field}", getattr(fitment, field), list_name)
        if session.get(Vehicle, fitment.vehicle_id) is None:
            check.add(f"fitments.{index}.vehicle_id", "Unknown vehicle")
        if fitment.vehicle_id in vehicles_seen:
            check.add(f"fitments.{index}.vehicle_id", "Vehicle listed twice")
        vehicles_seen.add(fitment.vehicle_id)
        if fitment.year_from and fitment.year_to and fitment.year_from > fitment.year_to:
            check.add(f"fitments.{index}.year_to", "Must not be before year from")

    for index, offer in enumerate(payload.offers):
        for field, list_name in OFFER_LISTS.items():
            check.choice(f"offers.{index}.{field}", getattr(offer, field), list_name)
        if session.get(Supplier, offer.supplier_id) is None:
            check.add(f"offers.{index}.supplier_id", "Unknown supplier")
    return check


def _apply(session: Session, product: Product, payload: ProductIn) -> None:
    now = datetime.now(UTC)
    for field in (
        "name",
        "name_ru",
        "name_en",
        "article_number",
        "ean",
        "country_of_origin",
        "description",
    ):
        value = getattr(payload, field)
        setattr(product, field, value.strip() if field == "name" else _blank_to_none(value))
    for field in (
        "brand_id",
        "category_id",
        "origin",
        "status",
        "unit",
        "pack_qty",
        "weight_kg",
        "length_mm",
        "width_mm",
        "height_mm",
        "universal",
    ):
        setattr(product, field, getattr(payload, field))

    # Attributes are keyed by code; blank values remove the attribute.
    existing_attributes = {attribute.attribute_code: attribute for attribute in product.attributes}
    kept_codes = set()
    for item in payload.attributes:
        value = item.value.strip()
        if not value:
            continue
        kept_codes.add(item.attribute_code)
        attribute = existing_attributes.get(item.attribute_code)
        if attribute is None:
            product.attributes.append(
                ProductAttribute(
                    attribute_code=item.attribute_code,
                    value=value,
                    unit=_blank_to_none(item.unit),
                    source=_blank_to_none(item.source) or "MANUAL",
                )
            )
        else:
            if attribute.value != value:
                attribute.source = "MANUAL"
            attribute.value = value
            attribute.unit = _blank_to_none(item.unit)
    for code, attribute in existing_attributes.items():
        if code not in kept_codes:
            product.attributes.remove(attribute)

    existing_references = {reference.id: reference for reference in product.reference_numbers}
    references_by_key = {
        (reference.normalized_number, reference.type): reference
        for reference in product.reference_numbers
    }
    kept_references = []
    for item in payload.references:
        reference = existing_references.get(item.id) if item.id else None
        # A row removed and re-added in one save reuses the stored row (unique key).
        reference = reference or references_by_key.get((normalize_code(item.number), item.type))
        if reference in kept_references:
            reference = None
        if reference is None:
            reference = ReferenceNumber(cross_source="MANUAL")
            product.reference_numbers.append(reference)
        reference.number = item.number.strip()
        reference.normalized_number = normalize_code(item.number)
        reference.type = item.type
        reference.number_brand_id = item.number_brand_id
        reference.cross_source = item.cross_source or reference.cross_source
        reference.confidence = item.confidence
        if item.verified and not reference.verified:
            reference.verified_at = now
            reference.verified_by = "irizon"
        reference.verified = item.verified
        reference.notes = _blank_to_none(item.notes)
        kept_references.append(reference)
    for reference in list(product.reference_numbers):
        if reference not in kept_references:
            product.reference_numbers.remove(reference)

    existing_fitments = {fitment.id: fitment for fitment in product.fitments}
    fitments_by_vehicle = {fitment.vehicle_id: fitment for fitment in product.fitments}
    kept_fitments = []
    for item in payload.fitments:
        fitment = existing_fitments.get(item.id) if item.id else None
        fitment = fitment or fitments_by_vehicle.get(item.vehicle_id)
        if fitment in kept_fitments:
            fitment = None
        if fitment is None:
            fitment = Fitment(fitment_source="MANUAL_VERIFIED")
            product.fitments.append(fitment)
        fitment.vehicle = session.get(Vehicle, item.vehicle_id)
        for field in (
            "position",
            "side",
            "vertical",
            "qty_per_vehicle",
            "year_from",
            "year_to",
            "confidence",
            "verified",
        ):
            setattr(fitment, field, getattr(item, field))
        fitment.fitment_source = item.fitment_source or fitment.fitment_source
        fitment.condition_note = _blank_to_none(item.condition_note)
        fitment.source_vehicle_text = _blank_to_none(item.source_vehicle_text)
        kept_fitments.append(fitment)
    for fitment in list(product.fitments):
        if fitment not in kept_fitments:
            product.fitments.remove(fitment)

    # Offers are never deleted: reservations point at them. Removed rows are deactivated.
    existing_offers = {offer.id: offer for offer in product.supplier_offers}
    kept_offers = []
    for item in payload.offers:
        offer = existing_offers.get(item.id) if item.id else None
        if offer is None:
            offer = SupplierOffer(
                source_offer_id=f"MANUAL-{product.id}-{now:%Y%m%d%H%M%S%f}",
                source_type="MANUAL",
                data_status="LIVE",
                updated_at=now,
            )
            product.supplier_offers.append(offer)
        sku = _blank_to_none(item.supplier_sku)
        changed = (
            offer.price != item.price
            or offer.stock_qty != item.stock_qty
            or offer.supplier_sku != sku
            or offer.supplier_id != item.supplier_id
        )
        offer.supplier = session.get(Supplier, item.supplier_id)
        offer.supplier_sku = sku
        offer.normalized_supplier_sku = normalize_code(sku) or None
        offer.price = item.price
        offer.currency = item.currency.upper()
        offer.price_type = item.price_type
        offer.stock_qty = item.stock_qty
        offer.warehouse = _blank_to_none(item.warehouse)
        offer.lead_time_days = item.lead_time_days
        offer.min_order_qty = item.min_order_qty
        offer.condition = item.condition
        offer.is_active = item.is_active
        if changed:
            # Prices and stock typed in by the supplier are live data, not the demo import.
            offer.data_status = "LIVE"
            offer.source_type = "MANUAL"
            offer.updated_at = now
        kept_offers.append(offer)
    for offer in product.supplier_offers:
        if offer not in kept_offers:
            offer.is_active = False


@router.get("/options")
def catalog_options(session: SessionDep) -> dict:
    """Everything the product form needs for dropdowns, attribute fields, and help text."""
    categories = session.scalars(
        select(Category).options(selectinload(Category.attributes)).order_by(Category.id)
    ).all()
    vehicles = session.scalars(
        select(Vehicle).order_by(Vehicle.make, Vehicle.model, Vehicle.year_from, Vehicle.id)
    ).all()
    return {
        "brands": [
            {"id": brand.id, "name": brand.name, "code": brand.code}
            for brand in session.scalars(select(Brand).order_by(func.lower(Brand.name)))
        ],
        "categories": [
            {
                "id": category.id,
                "parent_id": category.parent_id,
                "name_uz": category.name_uz,
                "name_ru": category.name_ru,
                "name_en": category.name_en,
                "is_leaf": category.is_leaf,
                "attributes": [
                    {
                        "attribute_code": attribute.attribute_code,
                        "name_uz": attribute.name_uz,
                        "name_ru": attribute.name_ru,
                        "unit": attribute.unit,
                        "data_type": attribute.data_type,
                        "required": attribute.required,
                        "allowed_values": [
                            value.strip()
                            for value in (attribute.allowed_values or "").split(";")
                            if value.strip()
                        ],
                    }
                    for attribute in category.attributes
                ],
            }
            for category in categories
        ],
        "vehicles": [{"id": vehicle.id, "label": _vehicle_label(vehicle)} for vehicle in vehicles],
        "suppliers": [
            {"id": supplier.id, "name": supplier.name}
            for supplier in session.scalars(select(Supplier).order_by(Supplier.name))
        ],
        "lists": _list_values(session),
        "help": {
            f"{doc.sheet}.{doc.column}": doc.description
            for doc in session.scalars(select(CatalogFieldDoc))
            if doc.description
        },
    }


@router.get("/profile")
def catalog_profile(request: Request, session: SessionDep) -> dict:
    settings = get_settings()
    suppliers = session.scalars(select(Supplier).order_by(Supplier.id)).all()
    active_offers = select(SupplierOffer).where(SupplierOffer.is_active.is_(True)).subquery()
    return {
        "username": session_user(settings, request.cookies.get(COOKIE_NAME)),
        "suppliers": [
            {
                "id": supplier.id,
                "source_id": supplier.source_id,
                "name": supplier.name,
                "supplier_type": supplier.supplier_type,
                "city": supplier.city,
                "address": supplier.address,
                "contact": supplier.contact,
                "phone": supplier.phone,
                "telegram": supplier.telegram,
                "default_currency": supplier.default_currency,
                "integration": supplier.integration,
                "update_frequency_days": supplier.update_frequency_days,
                "default_lead_time_days": supplier.default_lead_time_days,
                "reliability_score": _decimal_out(supplier.reliability_score),
                "is_active": supplier.is_active,
            }
            for supplier in suppliers
        ],
        "stats": {
            "products": session.scalar(select(func.count(Product.id))),
            "searchable": session.scalar(
                select(func.count(Product.id)).where(Product.is_searchable.is_(True))
            ),
            "hidden_conflicts": session.scalar(
                select(func.count(Product.id)).where(Product.audit_status == "CONFLICT")
            ),
            "open_reviews": session.scalar(
                select(func.count(CatalogReviewItem.raw_id)).where(
                    CatalogReviewItem.status != "RESOLVED"
                )
            ),
            "offers_without_price": session.scalar(
                select(func.count())
                .select_from(active_offers)
                .where(active_offers.c.price.is_(None))
            ),
            "categories": session.scalar(select(func.count(Category.id))),
            "vehicles": session.scalar(select(func.count(Vehicle.id))),
        },
    }


@router.put("/suppliers/{supplier_id}")
def update_supplier_profile(
    supplier_id: int, payload: SupplierProfileIn, session: SessionDep
) -> dict:
    supplier = session.get(Supplier, supplier_id)
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    check = _Validator(_list_values(session))
    for field, list_name in SUPPLIER_LISTS.items():
        check.choice(field, getattr(payload, field), list_name)
    duplicate = session.scalar(
        select(Supplier.id).where(
            Supplier.normalized_name == normalize_text(payload.name), Supplier.id != supplier_id
        )
    )
    if duplicate:
        check.add("name", "Another supplier already uses this name")
    check.raise_if_any()
    for field, value in payload.model_dump().items():
        setattr(supplier, field, _blank_to_none(value) if isinstance(value, str) else value)
    supplier.normalized_name = normalize_text(supplier.name)
    session.commit()
    return {"id": supplier.id, "name": supplier.name}


@router.get("/products")
def catalog_products(
    session: SessionDep,
    q: Annotated[str, Query(max_length=200)] = "",
    category_id: Annotated[str | None, Query(max_length=64)] = None,
    brand_id: int | None = None,
    status: Annotated[str | None, Query(max_length=30)] = None,
    issue: Annotated[str | None, Query(pattern="^(conflict|review|no_price|no_brand)$")] = None,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> dict:
    stmt = select(Product)
    if q.strip():
        text = normalize_text(q)
        stmt = stmt.where(
            or_(
                Product.id.ilike(f"%{q.strip()}%"),
                Product.search_text.contains(text),
                Product.reference_numbers.any(
                    ReferenceNumber.normalized_number.contains(normalize_code(q) or text)
                ),
            )
        )
    if category_id:
        stmt = stmt.where(Product.category_id == category_id)
    if brand_id:
        stmt = stmt.where(Product.brand_id == brand_id)
    if status:
        stmt = stmt.where(Product.status == status)
    if issue == "conflict":
        stmt = stmt.where(Product.audit_status == "CONFLICT")
    elif issue == "review":
        stmt = stmt.where(
            Product.id.in_(
                select(CatalogReviewItem.product_id).where(CatalogReviewItem.status != "RESOLVED")
            )
        )
    elif issue == "no_price":
        stmt = stmt.where(
            Product.supplier_offers.any(
                (SupplierOffer.is_active.is_(True)) & (SupplierOffer.price.is_(None))
            )
        )
    elif issue == "no_brand":
        stmt = stmt.where(Product.brand_id.is_(None))

    total = session.scalar(select(func.count()).select_from(stmt.subquery()))
    products = session.scalars(
        stmt.options(
            selectinload(Product.brand),
            selectinload(Product.category),
            selectinload(Product.reference_numbers),
            selectinload(Product.fitments),
            selectinload(Product.supplier_offers),
        )
        .order_by(Product.id)
        .limit(limit)
        .offset(offset)
    ).all()
    return {
        "total": total,
        "items": [
            {
                "id": product.id,
                "name": product.name,
                "name_ru": product.name_ru,
                "article_number": product.article_number,
                "brand": product.brand.name if product.brand else None,
                "category": product.category.name_uz if product.category else None,
                "status": product.status,
                "audit_status": product.audit_status,
                "is_searchable": product.is_searchable,
                "reference_count": len(product.reference_numbers),
                "fitment_count": len(product.fitments),
                "offer_count": sum(offer.is_active for offer in product.supplier_offers),
            }
            for product in products
        ],
    }


@router.get("/products/{product_id}")
def catalog_product(product_id: str, session: SessionDep) -> dict:
    return product_record(session, _load_product(session, product_id))


@router.put("/products/{product_id}")
def update_catalog_product(product_id: str, payload: ProductIn, session: SessionDep) -> dict:
    product = _load_product(session, product_id)
    if (
        payload.expected_updated_at
        and product.updated_at
        and abs((product.updated_at - payload.expected_updated_at).total_seconds()) > 0.001
    ):
        raise HTTPException(
            status_code=409,
            detail="This product was changed after you opened it. Reload to see the latest.",
        )
    _validate(session, payload).raise_if_any()
    # New child rows are half-built until _apply finishes; don't flush them early.
    with session.no_autoflush:
        _apply(session, product, payload)
    product.updated_at = datetime.now(UTC)
    session.flush()
    session.refresh(product, ["category", "brand"])
    refresh_product(product)
    session.commit()
    return product_record(session, _load_product(session, product_id))


@router.post("/products", status_code=201)
def create_catalog_product(payload: ProductIn, session: SessionDep) -> dict:
    _validate(session, payload).raise_if_any()
    product = Product(
        id=_next_product_id(session),
        name=payload.name.strip(),
        normalized_name="",
        audit_status="MANUAL",
        merge_basis="MANUAL",
        search_text="",
    )
    product.attributes = []
    product.reference_numbers = []
    product.fitments = []
    product.supplier_offers = []
    session.add(product)
    # New child rows are half-built until _apply finishes; don't flush them early.
    with session.no_autoflush:
        _apply(session, product, payload)
    product.updated_at = datetime.now(UTC)
    session.flush()
    session.refresh(product, ["category", "brand"])
    refresh_product(product)
    session.commit()
    return product_record(session, _load_product(session, product.id))
