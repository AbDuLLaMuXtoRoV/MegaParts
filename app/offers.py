from datetime import UTC, datetime

from app.config import get_settings
from app.models import Supplier, SupplierOffer
from app.schemas import OfferOut, SupplierSummary

# A supplier's reliability is shown once this many reservations have an outcome.
MIN_RELIABILITY_SAMPLE = 5


def _age_hours(updated_at: datetime, now: datetime | None = None) -> float:
    current = now or datetime.now(UTC)
    timestamp = updated_at if updated_at.tzinfo else updated_at.replace(tzinfo=UTC)
    return max(0.0, (current - timestamp).total_seconds() / 3600)


def freshness_status(updated_at: datetime | None, now: datetime | None = None) -> str:
    if updated_at is None:
        return "UNKNOWN"
    age_hours = _age_hours(updated_at, now)
    settings = get_settings()
    if age_hours < settings.offer_fresh_hours:
        return "FRESH"
    if age_hours <= settings.offer_recent_hours:
        return "RECENT"
    if age_hours <= settings.offer_outdated_days * 24:
        return "STALE"
    return "OUTDATED"


def is_expired(offer: SupplierOffer, now: datetime | None = None) -> bool:
    """A price list nobody refreshed for two weeks no longer describes real stock.

    A list that names parts without price or stock ("ask the seller") claims nothing that
    goes stale, so it stays until the seller sends a new list.
    """
    if offer.updated_at is None or (offer.price is None and offer.stock_qty is None):
        return False
    return _age_hours(offer.updated_at, now) > get_settings().offer_hidden_days * 24


def _preferred_ids() -> set[int]:
    return {
        int(value.strip())
        for value in get_settings().preferred_supplier_ids.split(",")
        if value.strip().isdigit()
    }


def offer_sort_key(offer: SupplierOffer) -> tuple:
    """Who will actually have the part comes before who is cheapest.

    The product blueprint's order: available stock, then freshness (a stale cheap offer is
    not above fresh stock), then preferred suppliers, then price, then reliability and the
    quickest hand-over.
    """
    freshness_rank = {"FRESH": 0, "RECENT": 1, "UNKNOWN": 2, "STALE": 3, "OUTDATED": 4}
    stock_rank = 0 if offer.stock_qty is not None and offer.stock_qty > 0 else 1
    supplier = offer.supplier
    reliable = supplier is not None and (supplier.reliability_sample or 0) >= MIN_RELIABILITY_SAMPLE
    # A seller without enough history sits between a good and a poor record.
    reliability_rank = -float(supplier.reliability_score) if reliable else -75.0
    lead_time = offer.lead_time_days
    if lead_time is None and supplier is not None:
        lead_time = supplier.default_lead_time_days
    preferred_rank = 0 if offer.supplier_id in _preferred_ids() else 1
    price_rank = float(offer.price) if offer.price is not None else float("inf")
    return (
        stock_rank,
        freshness_rank[freshness_status(offer.updated_at)],
        preferred_rank,
        price_rank,
        reliability_rank,
        lead_time if lead_time is not None else 99,
        offer.id or 0,
    )


def active_sorted_offers(offers: list[SupplierOffer]) -> list[SupplierOffer]:
    return sorted(
        (
            offer
            for offer in offers
            if offer.is_active and offer.supplier.is_active and not is_expired(offer)
        ),
        key=offer_sort_key,
    )


def supplier_summary(supplier: Supplier) -> SupplierSummary:
    """What a buyer sees about a seller: contacts, where and when, and how trustworthy."""
    reliable = (supplier.reliability_sample or 0) >= MIN_RELIABILITY_SAMPLE
    return SupplierSummary(
        id=supplier.id,
        name=supplier.name,
        supplier_type=supplier.supplier_type,
        phone=supplier.phone,
        telegram=supplier.telegram,
        address=supplier.address,
        city=supplier.city,
        work_hours=supplier.work_hours,
        map_url=supplier.map_url,
        verified=supplier.verified_at is not None,
        member_since=supplier.created_at,
        reliability_score=supplier.reliability_score if reliable else None,
        reliability_sample=supplier.reliability_sample or 0,
    )


def offer_out(offer: SupplierOffer) -> OfferOut:
    supplier = offer.supplier
    return OfferOut(
        id=offer.id,
        supplier_id=offer.supplier_id,
        supplier_name=supplier.name,
        supplier=supplier_summary(supplier),
        supplier_sku=offer.supplier_sku,
        price=offer.price,
        currency=offer.currency,
        stock_qty=offer.stock_qty,
        warehouse=offer.warehouse,
        updated_at=offer.updated_at,
        freshness_status=freshness_status(offer.updated_at),
        data_status=offer.data_status,
        part_origin=offer.part_origin,
        condition=offer.condition,
        warranty_months=offer.warranty_months,
        warranty_km=offer.warranty_km,
        return_days=offer.return_days,
        promo=offer.promo,
        discount_percent=offer.discount_percent,
        pack_qty=offer.pack_qty,
        lead_time_days=(
            offer.lead_time_days
            if offer.lead_time_days is not None
            else supplier.default_lead_time_days
        ),
    )
