"""Reservation follow-up: buyers' own list, staff status updates, and supplier reliability."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import ReservationRequest, Supplier, SupplierOffer
from app.offers import supplier_summary
from app.schemas import AdminReservationOut, MyReservationOut

RELIABILITY_DAYS = 90
# A buyer not turning up says nothing about the supplier.
OUTCOMES_AGAINST_SUPPLIER = ("WRONG_FIT", "OUT_OF_STOCK", "PRICE_CHANGED")


def recompute_reliability(session: Session, supplier_id: int) -> None:
    """Share of the supplier's finished reservations honoured over the last 90 days."""
    since = datetime.now(UTC) - timedelta(days=RELIABILITY_DAYS)
    rows = dict(
        session.execute(
            select(ReservationRequest.outcome, func.count(ReservationRequest.id))
            .join(SupplierOffer, SupplierOffer.id == ReservationRequest.supplier_offer_id)
            .where(
                SupplierOffer.supplier_id == supplier_id,
                ReservationRequest.created_at >= since,
                ReservationRequest.outcome.in_(("HONOURED", *OUTCOMES_AGAINST_SUPPLIER)),
            )
            .group_by(ReservationRequest.outcome)
        ).all()
    )
    sample = sum(rows.values())
    supplier = session.get(Supplier, supplier_id)
    supplier.reliability_sample = sample
    supplier.reliability_score = (
        (Decimal(rows.get("HONOURED", 0)) * 100 / sample).quantize(Decimal("0.1"))
        if sample
        else None
    )


def my_reservation_out(reservation: ReservationRequest) -> MyReservationOut:
    offer = reservation.supplier_offer
    return MyReservationOut(
        id=reservation.id,
        status=reservation.status,
        quantity=reservation.quantity,
        vehicle_label=reservation.vehicle_label,
        vin=reservation.vin,
        note=reservation.note,
        created_at=reservation.created_at,
        updated_at=reservation.updated_at,
        product_id=reservation.product_id,
        product_name=reservation.product.name,
        product_name_ru=reservation.product.name_ru,
        product_name_en=reservation.product.name_en,
        reference_numbers=[ref.number for ref in reservation.product.reference_numbers],
        supplier=supplier_summary(offer.supplier),
        price=offer.price,
        currency=offer.currency,
    )


def admin_reservation_out(reservation: ReservationRequest) -> AdminReservationOut:
    offer = reservation.supplier_offer
    return AdminReservationOut(
        id=reservation.id,
        created_at=reservation.created_at,
        updated_at=reservation.updated_at,
        status=reservation.status,
        outcome=reservation.outcome,
        quantity=reservation.quantity,
        phone=reservation.phone,
        vehicle_label=reservation.vehicle_label,
        vin=reservation.vin,
        note=reservation.note,
        product_id=reservation.product_id,
        product_name=reservation.product.name,
        supplier_id=offer.supplier_id,
        supplier_name=offer.supplier.name,
        supplier_sku=offer.supplier_sku,
    )
