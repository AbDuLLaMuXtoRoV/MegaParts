from datetime import UTC, datetime

from app.config import get_settings
from app.models import SupplierOffer
from app.schemas import OfferOut


def freshness_status(updated_at: datetime | None, now: datetime | None = None) -> str:
    if updated_at is None:
        return "UNKNOWN"
    current = now or datetime.now(UTC)
    timestamp = updated_at if updated_at.tzinfo else updated_at.replace(tzinfo=UTC)
    age_hours = max(0.0, (current - timestamp).total_seconds() / 3600)
    settings = get_settings()
    if age_hours < settings.offer_fresh_hours:
        return "FRESH"
    if age_hours <= settings.offer_recent_hours:
        return "RECENT"
    return "STALE"


def _preferred_ids() -> set[int]:
    return {
        int(value.strip())
        for value in get_settings().preferred_supplier_ids.split(",")
        if value.strip().isdigit()
    }


def offer_sort_key(offer: SupplierOffer) -> tuple:
    freshness_rank = {"FRESH": 0, "RECENT": 1, "UNKNOWN": 2, "STALE": 3}
    stock_rank = 0 if offer.stock_qty is not None and offer.stock_qty > 0 else 1
    preferred_rank = 0 if offer.supplier_id in _preferred_ids() else 1
    price_rank = float(offer.price) if offer.price is not None else float("inf")
    return (
        stock_rank,
        freshness_rank[freshness_status(offer.updated_at)],
        preferred_rank,
        price_rank,
        offer.id or 0,
    )


def active_sorted_offers(offers: list[SupplierOffer]) -> list[SupplierOffer]:
    return sorted(
        (offer for offer in offers if offer.is_active and offer.supplier.is_active),
        key=offer_sort_key,
    )


def offer_out(offer: SupplierOffer) -> OfferOut:
    return OfferOut(
        id=offer.id,
        supplier_id=offer.supplier_id,
        supplier_name=offer.supplier.name,
        supplier=offer.supplier,
        supplier_sku=offer.supplier_sku,
        price=offer.price,
        currency=offer.currency,
        stock_qty=offer.stock_qty,
        warehouse=offer.warehouse,
        updated_at=offer.updated_at,
        freshness_status=freshness_status(offer.updated_at),
        data_status=offer.data_status,
    )
