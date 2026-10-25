"""What a part page shows around the part: alternatives, kits, fit reports and popularity."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.catalog import compatible_variants, product_variant
from app.models import (
    FitReport,
    Product,
    ReferenceNumber,
    ReservationRequest,
    SupplierOffer,
)
from app.offers import active_sorted_offers
from app.part_types import COMPLETE_THE_JOB, fits_vehicles
from app.schemas import FitReportSummary, RelatedProductOut
from app.shop import quality_tier

POPULARITY_DAYS = 90
MAX_ALTERNATIVES = 8
MAX_PER_JOB_TYPE = 2
MAX_JOB_PARTS = 6


def reservation_counts(session: Session, product_ids: list[str]) -> dict[str, int]:
    """Reservations per product over the last 90 days, ignoring cancelled ones."""
    if not product_ids:
        return {}
    since = datetime.now(UTC) - timedelta(days=POPULARITY_DAYS)
    rows = session.execute(
        select(ReservationRequest.product_id, func.count(ReservationRequest.id))
        .where(
            ReservationRequest.product_id.in_(product_ids),
            ReservationRequest.created_at >= since,
            ReservationRequest.status != "CANCELLED",
        )
        .group_by(ReservationRequest.product_id)
    ).all()
    return dict(rows)


def _related(
    product: Product, relation: str, shared_number: str | None = None, same_variant: bool = True
):
    offers = active_sorted_offers(product.supplier_offers)
    priced = [offer for offer in offers if offer.price is not None]
    cheapest = min(priced, key=lambda offer: offer.price) if priced else None
    return RelatedProductOut(
        id=product.id,
        name=product.name,
        name_ru=product.name_ru,
        name_en=product.name_en,
        brand=product.brand,
        category=product.category,
        relation=relation,
        shared_number=shared_number,
        lowest_price=cheapest.price if cheapest else None,
        currency=cheapest.currency if cheapest else None,
        offer_count=len(offers),
        quality=quality_tier(product),
        same_variant=same_variant,
    )


def _candidates(session: Session, *conditions):
    return session.scalars(
        select(Product)
        .where(Product.is_searchable.is_(True), *conditions)
        .options(
            selectinload(Product.brand),
            selectinload(Product.category),
            selectinload(Product.reference_numbers),
            selectinload(Product.attributes),
            selectinload(Product.supplier_offers).selectinload(SupplierOffer.supplier),
        )
        .order_by(Product.name, Product.id)
    ).all()


def _fit_condition(product: Product, vehicle_ids: set[str] | None):
    """Parts for the buyer's car, else for the cars this part fits, else universal ones."""
    scope = vehicle_ids or {fitment.vehicle_id for fitment in product.fitments}
    return fits_vehicles(scope) if scope else Product.universal.is_(True)


def alternatives(
    session: Session, product: Product, vehicle_ids: set[str] | None
) -> list[RelatedProductOut]:
    """Analogs sharing a part number first, then other parts of the same type for the car."""
    # A seller's own code is not a part number, so it finds no analogs.
    numbers = {
        ref.normalized_number: ref.number
        for ref in product.reference_numbers
        if ref.type != "SUPPLIER_SKU"
    }
    variant = product_variant(product)
    result: list[RelatedProductOut] = []
    seen = {product.id}
    if numbers:
        for candidate in _candidates(
            session,
            Product.id != product.id,
            Product.reference_numbers.any(ReferenceNumber.normalized_number.in_(numbers)),
        ):
            shared = next(
                numbers[ref.normalized_number]
                for ref in candidate.reference_numbers
                if ref.normalized_number in numbers
            )
            # Same number in another size or side is a variant, not an analog to choose.
            same_variant = compatible_variants(variant, product_variant(candidate))
            result.append(_related(candidate, "SAME_NUMBER", shared, same_variant))
            seen.add(candidate.id)
    if product.category_id:
        for candidate in _candidates(
            session,
            Product.id.not_in(seen),
            Product.category_id == product.category_id,
            _fit_condition(product, vehicle_ids),
        ):
            result.append(_related(candidate, "SAME_TYPE"))
    # Parts with offers first, so the buyer sees real choices.
    result.sort(key=lambda item: (
        item.relation != "SAME_NUMBER", not item.same_variant, item.offer_count == 0
    ))
    return result[:MAX_ALTERNATIVES]


def complete_the_job(
    session: Session, product: Product, vehicle_ids: set[str] | None
) -> list[RelatedProductOut]:
    """Parts usually replaced together with this one, for the same car."""
    result: list[RelatedProductOut] = []
    for category_id in COMPLETE_THE_JOB.get(product.category_id or "", ()):
        found = _candidates(
            session,
            Product.category_id == category_id,
            _fit_condition(product, vehicle_ids),
        )
        found.sort(key=lambda candidate: not candidate.supplier_offers)
        result.extend(
            _related(candidate, "COMPLETE_THE_JOB") for candidate in found[:MAX_PER_JOB_TYPE]
        )
    return result[:MAX_JOB_PARTS]


def fit_report_summary(session: Session, product_id: str) -> list[FitReportSummary]:
    rows = session.execute(
        select(
            FitReport.vehicle_id,
            FitReport.vehicle_label,
            func.count(FitReport.id).filter(FitReport.fits.is_(True)),
            func.count(FitReport.id).filter(FitReport.fits.is_(False)),
        )
        .where(FitReport.product_id == product_id)
        .group_by(FitReport.vehicle_id, FitReport.vehicle_label)
    ).all()
    return [
        FitReportSummary(
            vehicle_id=vehicle_id, vehicle_label=label, fits=fits, does_not_fit=does_not_fit
        )
        for vehicle_id, label, fits, does_not_fit in rows
    ]
