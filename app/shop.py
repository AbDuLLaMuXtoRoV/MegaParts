"""Buying across sellers: quality grades, ready repair lists, the basket, and the sellers list."""

from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import (
    Category,
    Fitment,
    Product,
    ReservationRequest,
    Supplier,
    SupplierOffer,
    Vehicle,
)
from app.offers import active_sorted_offers, offer_out, offer_sort_key, supplier_summary
from app.part_types import JOBS, fits_vehicles
from app.schemas import (
    BasketCreate,
    BasketOfferOut,
    BasketOut,
    JobOut,
    JobPartOut,
    ReservationOut,
    SellerCardOut,
)

QUALITY_GRADES = ("ORIGINAL", "KOREA", "CHINA", "BUDGET", "OTHER")


def quality_tier(product: Product) -> str:
    """The grade buyers choose by: carmaker original, Korean/OE-supplier, budget, Chinese.

    Read from the catalog's origin list (ORIGINAL, OES, AFTERMARKET), the country of origin
    and the brand's quality tier (ECONOMY for unbranded parts).
    """
    origin = (product.origin or "").upper()
    if origin in {"ORIGINAL", "GENUINE"}:
        return "ORIGINAL"
    if origin in {"OES", "OE"} or product.country_of_origin == "KR":
        return "KOREA"
    if origin == "BUDGET" or (product.brand and product.brand.quality_tier == "ECONOMY"):
        return "BUDGET"
    if product.country_of_origin == "CN":
        return "CHINA"
    return "OTHER"


def _best_offer_key(product: Product) -> tuple:
    offers = active_sorted_offers(product.supplier_offers)
    if not offers:
        return (1,)
    # The best offer decides; more sellers break ties, then the name keeps it stable.
    return (0, *offer_sort_key(offers[0])[:-1], -len(offers), product.name)


def job_lists(session: Session, vehicle_ids: set[str] | None, search_out) -> list[JobOut]:
    """Every repair list with the part to pick for each step, for the buyer's car."""
    type_ids = {part.type_id for job in JOBS for part in job.parts}
    categories = {
        category.id: category
        for category in session.scalars(select(Category).where(Category.id.in_(type_ids)))
    }
    by_type: dict[str, list[Product]] = defaultdict(list)
    if vehicle_ids:
        products = session.scalars(
            select(Product)
            .where(
                Product.is_searchable.is_(True),
                Product.category_id.in_(type_ids),
                fits_vehicles(vehicle_ids),
            )
            .options(
                selectinload(Product.brand),
                selectinload(Product.category),
                selectinload(Product.reference_numbers),
                selectinload(Product.fitments).selectinload(Fitment.vehicle),
                selectinload(Product.supplier_offers).selectinload(SupplierOffer.supplier),
            )
        ).all()
        for product in products:
            if active_sorted_offers(product.supplier_offers):
                by_type[product.category_id].append(product)

    def fits_end(product: Product, position: str | None) -> bool:
        if position is None:
            return True
        ends = {
            (fitment.position or "").upper()
            for fitment in product.fitments
            if not vehicle_ids or fitment.vehicle_id in vehicle_ids
        }
        return position in ends or not (ends & {"FRONT", "REAR"})

    jobs = []
    for job in JOBS:
        parts = []
        for part in job.parts:
            category = categories.get(part.type_id)
            if category is None:
                continue
            choices = sorted(
                (product for product in by_type[part.type_id] if fits_end(product, part.position)),
                key=_best_offer_key,
            )
            parts.append(
                JobPartOut(
                    type_id=part.type_id,
                    type_name_uz=category.name_uz,
                    type_name_ru=category.name_ru,
                    type_name_en=category.name_en,
                    position=part.position,
                    product=search_out(choices[0]) if choices else None,
                    options=len(choices),
                )
            )
        jobs.append(
            JobOut(
                id=job.id,
                name_uz=job.name_uz,
                name_ru=job.name_ru,
                name_en=job.name_en,
                icon=job.icon,
                parts=parts,
                available=sum(1 for part in parts if part.product),
            )
        )
    return jobs


def basket_offers(session: Session, offer_ids: list[int]) -> list[BasketOfferOut]:
    """The basket's offers as they stand now; withdrawn ones are left out."""
    offers = session.scalars(
        select(SupplierOffer)
        .where(SupplierOffer.id.in_(offer_ids), SupplierOffer.is_active.is_(True))
        .options(
            selectinload(SupplierOffer.supplier),
            selectinload(SupplierOffer.product).selectinload(Product.brand),
            selectinload(SupplierOffer.product).selectinload(Product.category),
            selectinload(SupplierOffer.product).selectinload(Product.reference_numbers),
        )
    ).all()
    return [
        BasketOfferOut(
            offer=offer_out(offer),
            product_id=offer.product.id,
            name=offer.product.name,
            name_ru=offer.product.name_ru,
            name_en=offer.product.name_en,
            brand=offer.product.brand,
            category=offer.product.category,
            reference_numbers=[ref.number for ref in offer.product.reference_numbers],
        )
        for offer in offers
        if offer.supplier.is_active
    ]


def create_basket(session: Session, payload: BasketCreate) -> BasketOut:
    """One reservation per part, all sharing a basket id so seller and buyer see them together."""
    offer_ids = [item.supplier_offer_id for item in payload.items]
    offers = {
        offer.id: offer
        for offer in session.scalars(
            select(SupplierOffer)
            .where(SupplierOffer.id.in_(offer_ids), SupplierOffer.is_active.is_(True))
            .options(selectinload(SupplierOffer.supplier))
        )
    }
    for item in payload.items:
        offer = offers.get(item.supplier_offer_id)
        if offer is None or offer.product_id != item.product_id or not offer.supplier.is_active:
            raise HTTPException(
                status_code=404,
                detail=f"Offer {item.supplier_offer_id} is no longer available",
            )
    vehicle_id = payload.vehicle_id if session.get(Vehicle, payload.vehicle_id or "") else None
    basket_id = uuid4().hex
    now = datetime.now(UTC)
    reservations = [
        ReservationRequest(
            session_id=payload.session_id,
            search_event_id=None,
            product_id=item.product_id,
            supplier_offer_id=item.supplier_offer_id,
            quantity=item.quantity,
            phone=payload.phone,
            vehicle_id=vehicle_id,
            vehicle_label=payload.vehicle_label,
            vin=payload.vin,
            note=payload.note,
            basket_id=basket_id,
            updated_at=now,
        )
        for item in payload.items
    ]
    session.add_all(reservations)
    session.commit()
    for reservation in reservations:
        session.refresh(reservation)
    return BasketOut(
        basket_id=basket_id,
        reservations=[ReservationOut.model_validate(reservation) for reservation in reservations],
    )


def sellers_directory(session: Session) -> list[SellerCardOut]:
    """Every active seller with what they offer, busiest first."""
    suppliers = session.scalars(
        select(Supplier)
        .where(Supplier.is_active.is_(True))
        .options(
            selectinload(Supplier.offers)
            .selectinload(SupplierOffer.product)
            .selectinload(Product.brand)
        )
    ).all()
    cards = []
    for supplier in suppliers:
        offers = active_sorted_offers(supplier.offers)
        if not offers:
            continue
        brands: dict[str, int] = defaultdict(int)
        for offer in offers:
            if offer.product.brand and not offer.product.brand.name.startswith("Brendsiz"):
                brands[offer.product.brand.name] += 1
        cards.append(
            SellerCardOut(
                supplier=supplier_summary(supplier),
                active_offers_count=len(offers),
                priced_offers_count=sum(1 for offer in offers if offer.price is not None),
                brands=[name for name, _ in sorted(brands.items(), key=lambda kv: -kv[1])[:6]],
                last_data_update=max(
                    (offer.updated_at for offer in offers if offer.updated_at), default=None
                ),
            )
        )
    cards.sort(key=lambda card: (-card.active_offers_count, card.supplier.name))
    return cards
