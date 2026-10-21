from __future__ import annotations

from collections import defaultdict
from datetime import UTC, date, datetime, time, timedelta
from statistics import median
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import (
    Product,
    ReservationRequest,
    SearchEvent,
    SearchEventAction,
    Supplier,
    SupplierOffer,
)


def date_window(
    period: str, date_from: date | None = None, date_to: date | None = None
) -> tuple[datetime, datetime]:
    now = datetime.now(UTC)
    if period == "today":
        start = datetime.combine(now.date(), time.min, tzinfo=UTC)
    elif period == "30d":
        start = now - timedelta(days=30)
    elif period == "custom" and date_from:
        start = datetime.combine(date_from, time.min, tzinfo=UTC)
    else:
        start = now - timedelta(days=7)
    if period == "custom" and date_to:
        end = datetime.combine(date_to + timedelta(days=1), time.min, tzinfo=UTC)
    else:
        end = now
    return start, end


def build_analytics(
    session: Session,
    period: str = "7d",
    date_from: date | None = None,
    date_to: date | None = None,
) -> dict[str, Any]:
    start, end = date_window(period, date_from, date_to)
    events = session.scalars(
        select(SearchEvent)
        .where(SearchEvent.created_at >= start, SearchEvent.created_at < end)
        .options(selectinload(SearchEvent.feedback))
        .order_by(SearchEvent.created_at.desc())
    ).all()
    total = len(events)
    event_ids = [event.id for event in events]
    actions = (
        session.scalars(
            select(SearchEventAction).where(
                SearchEventAction.search_event_id.in_(event_ids),
                SearchEventAction.created_at >= start,
                SearchEventAction.created_at < end,
            )
        ).all()
        if event_ids
        else []
    )
    actions_by_event: dict[int, list[SearchEventAction]] = defaultdict(list)
    for action in actions:
        actions_by_event[action.search_event_id].append(action)
    feedback = [event.feedback for event in events if event.feedback]
    positive = [item for item in feedback if item and item.found_correct_part]

    grouped: dict[str, list[SearchEvent]] = defaultdict(list)
    for event in events:
        grouped[event.query_normalized].append(event)

    rows = []
    needs_work = []
    poor_queries = []
    for query, items in grouped.items():
        item_feedback = [item.feedback for item in items if item.feedback]
        successes = [fb for fb in item_feedback if fb and fb.found_correct_part]
        top3 = [fb for fb in item_feedback if fb and fb.correct_in_top_3]
        clicks = sum(
            item.clicked_product_id is not None
            or any(action.action == "product_click" for action in actions_by_event[item.id])
            for item in items
        )
        contacts = sum(
            any(
                action.action in {"contact_supplier", "phone_click", "telegram_click"}
                for action in actions_by_event[item.id]
            )
            or item.action == "contact_supplier"
            for item in items
        )
        average_results = sum(item.result_count for item in items) / len(items)
        row = {
            "query": items[0].query_raw,
            "normalized_query": query,
            "search_count": len(items),
            "result_count": round(average_results, 1),
            "success_rate": round(100 * len(successes) / len(item_feedback), 1)
            if item_feedback
            else None,
            "top3_rate": round(100 * len(top3) / len(item_feedback), 1) if item_feedback else None,
            "clicks": clicks,
            "contacts": contacts,
            "average_response_time_ms": round(
                sum(float(item.search_time_ms) for item in items) / len(items), 1
            ),
        }
        rows.append(row)

        reasons = []
        if all(item.result_count == 0 for item in items):
            reasons.append("Zero results")
        if any(fb and not fb.found_correct_part for fb in item_feedback):
            reasons.append("Negative feedback")
        if len(items) >= 2 and clicks == 0:
            reasons.append("Repeated searches without a click")
        if average_results >= 50 and clicks == 0:
            reasons.append("Too many results without a click")
        if reasons:
            needs_work.append({**row, "reasons": reasons})
        if any(fb and not fb.found_correct_part for fb in item_feedback):
            poor_queries.append(row)

    rows.sort(key=lambda row: (-row["search_count"], row["query"]))
    zero_rows = [row for row in rows if row["result_count"] == 0]
    zero_rows.sort(key=lambda row: -row["search_count"])
    needs_work.sort(key=lambda row: (-len(row["reasons"]), -row["search_count"]))
    response_times = [float(event.search_time_ms) for event in events]
    action_counts = {
        action_name: sum(action.action == action_name for action in actions)
        for action_name in (
            "supplier_offer_view",
            "supplier_click",
            "phone_click",
            "telegram_click",
            "reservation_request",
        )
    }
    selected_supplier_counts: dict[int, int] = defaultdict(int)
    for action in actions:
        if action.supplier_id and action.action in {
            "supplier_click",
            "phone_click",
            "telegram_click",
            "contact_supplier",
            "reservation_request",
        }:
            selected_supplier_counts[action.supplier_id] += 1
    supplier_names = (
        {
            supplier.id: supplier.name
            for supplier in session.scalars(
                select(Supplier).where(Supplier.id.in_(selected_supplier_counts))
            ).all()
        }
        if selected_supplier_counts
        else {}
    )

    all_top_ids = {product_id for event in events for product_id in event.top_product_ids}
    products = (
        session.scalars(
            select(Product)
            .where(Product.id.in_(all_top_ids))
            .options(selectinload(Product.supplier_offers).selectinload(SupplierOffer.supplier))
        )
        .unique()
        .all()
        if all_top_ids
        else []
    )
    supply_by_product = {
        product.id: [
            offer
            for offer in product.supplier_offers
            if offer.is_active
            and offer.supplier.is_active
            and (offer.stock_qty is None or offer.stock_qty > 0)
        ]
        for product in products
    }
    reservations = session.scalars(
        select(ReservationRequest).where(
            ReservationRequest.created_at >= start, ReservationRequest.created_at < end
        )
    ).all()
    reservation_by_event: dict[int, int] = defaultdict(int)
    for reservation in reservations:
        if reservation.search_event_id:
            reservation_by_event[reservation.search_event_id] += 1
    demand_without_supply = []
    for query, items in grouped.items():
        product_ids = {product_id for item in items for product_id in item.top_product_ids}
        available = [
            offer for product_id in product_ids for offer in supply_by_product.get(product_id, [])
        ]
        if product_ids and not available:
            demand_without_supply.append(
                {
                    "query": items[0].query_raw,
                    "product_ids": sorted(product_ids),
                    "search_count": len(items),
                    "supplier_count": 0,
                    "available_offer_count": 0,
                    "reservation_requests": sum(reservation_by_event[item.id] for item in items),
                }
            )
    demand_without_supply.sort(key=lambda item: (-item["search_count"], item["query"]))

    return {
        "period": {"start": start.isoformat(), "end": end.isoformat()},
        "metrics": {
            "total_searches": total,
            "unique_sessions": len({event.session_id for event in events}),
            "zero_result_rate": round(
                100 * sum(event.result_count == 0 for event in events) / total, 1
            )
            if total
            else 0,
            "successful_search_rate": round(100 * len(positive) / len(feedback), 1)
            if feedback
            else 0,
            "correct_in_top_3_rate": round(
                100 * sum(item.correct_in_top_3 for item in feedback) / len(feedback), 1
            )
            if feedback
            else 0,
            "median_search_response_time_ms": round(median(response_times), 1)
            if response_times
            else 0,
            "product_click_through_rate": round(
                100 * sum(event.clicked_product_id is not None for event in events) / total, 1
            )
            if total
            else 0,
            "supplier_click_through_rate": round(
                100 * sum(event.clicked_supplier_id is not None for event in events) / total, 1
            )
            if total
            else 0,
            "contact_supplier_conversion": round(
                100
                * sum(
                    any(
                        action.action in {"contact_supplier", "phone_click", "telegram_click"}
                        for action in actions_by_event[event.id]
                    )
                    or event.action == "contact_supplier"
                    for event in events
                )
                / total,
                1,
            )
            if total
            else 0,
            "supplier_offer_views": action_counts["supplier_offer_view"],
            "supplier_clicks": action_counts["supplier_click"],
            "phone_clicks": action_counts["phone_click"],
            "telegram_clicks": action_counts["telegram_click"],
            "reservation_requests": len(reservations),
        },
        "most_selected_suppliers": [
            {"supplier": supplier_names.get(supplier_id, str(supplier_id)), "selections": count}
            for supplier_id, count in sorted(
                selected_supplier_counts.items(), key=lambda item: (-item[1], item[0])
            )[:10]
        ],
        "demand_without_supply": demand_without_supply[:20],
        "most_searched_queries": rows[:10],
        "top_zero_result_queries": zero_rows[:10],
        "queries_with_poor_feedback": poor_queries[:10],
        "query_rows": rows,
        "needs_catalog_work": needs_work,
    }
