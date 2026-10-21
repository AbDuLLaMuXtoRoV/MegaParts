from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from difflib import SequenceMatcher

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models import Brand, Category, Fitment, Product, SupplierOffer, Vehicle
from app.normalization import normalize_code, normalize_text
from app.offers import active_sorted_offers, offer_out
from app.part_types import fits_vehicles
from app.product_context import (
    alternatives,
    complete_the_job,
    fit_report_summary,
    reservation_counts,
)
from app.query_parser import ParsedQuery, parse_query
from app.schemas import (
    CategoryOut,
    ProductDetail,
    ProductSearchResult,
    SearchResponse,
    VehicleFilterOut,
)
from app.search_vocabulary import RELATED_PRODUCT_MARKERS
from app.vocabulary import (
    SearchVocabulary,
    correction_candidates,
    load_vocabulary,
    without_unknown_words,
)


@dataclass(frozen=True)
class ScoredProduct:
    product: Product
    score: float
    scoring: dict[str, float]
    result_group: str
    matched_vehicle: bool | None
    matched_product_terms: list[str]
    matched_position: bool | None
    matched_side: bool | None
    fitment_match: bool | None

    @property
    def priority(self) -> int:
        if any(
            key in self.scoring
            for key in (
                "exact_reference",
                "normalized_reference",
                "exact_supplier_code",
                "normalized_supplier_code",
            )
        ):
            return 0
        return {"EXACT": 1, "COMPATIBLE": 2, "RELATED": 3}[self.result_group]


def _phrase_in(text: str, phrase: str) -> bool:
    return f" {phrase} " in f" {text} "


def _vehicle_text(product: Product) -> str:
    return " ".join(
        filter(
            None,
            (
                " ".join(
                    filter(
                        None,
                        [fit.vehicle.normalized_text, normalize_text(fit.source_vehicle_text)],
                    )
                )
                for fit in product.fitments
            ),
        )
    )


def _score(
    product: Product, query: str, parsed: ParsedQuery, category_text: str = ""
) -> ScoredProduct:
    code = normalize_code(query)
    raw = query.strip().casefold()
    name = product.normalized_name
    brand = product.brand.normalized_name if product.brand else ""
    vehicles = _vehicle_text(product)
    attributes = normalize_text(
        " ".join(filter(None, [product.name, product.position, product.side]))
    )
    reference_values = {ref.number.strip().casefold() for ref in product.reference_numbers}
    reference_codes = {ref.normalized_number for ref in product.reference_numbers}
    sku_values = {
        offer.supplier_sku.strip().casefold()
        for offer in product.supplier_offers
        if offer.supplier_sku
    }
    sku_codes = {
        offer.normalized_supplier_sku
        for offer in product.supplier_offers
        if offer.normalized_supplier_sku
    }
    parts: dict[str, float] = {}
    matched_product_terms: list[str] = []

    if raw and raw in reference_values:
        parts["exact_reference"] = 170
    elif code and code in reference_codes:
        parts["normalized_reference"] = 155
    if raw and raw in sku_values:
        parts["exact_supplier_code"] = 165
    elif code and code in sku_codes:
        parts["normalized_supplier_code"] = 150

    for term in parsed.product_terms:
        expansions = parsed.product_expansions[term]
        if any(name == expansion for expansion in expansions):
            parts[f"product:{term}"] = 55
            matched_product_terms.append(term)
        elif any(_phrase_in(name, expansion) for expansion in expansions):
            parts[f"product:{term}"] = 45
            matched_product_terms.append(term)
        elif any(expansion in name for expansion in expansions):
            parts[f"product:{term}"] = 35
            matched_product_terms.append(term)
        elif any(expansion in category_text for expansion in expansions):
            # The word names the part type ("шрус", "катушка зажигания"), not the part.
            parts[f"category:{term}"] = 30
            matched_product_terms.append(term)
        else:
            ratio = max(SequenceMatcher(None, expansion, name).ratio() for expansion in expansions)
            if ratio >= 0.55:
                parts[f"fuzzy_product:{term}"] = round(ratio * 18, 2)

    related_variant = any(
        marker in name
        for term in parsed.product_terms
        for marker in RELATED_PRODUCT_MARKERS.get(term, ())
    )
    if related_variant:
        parts["related_product_variant"] = -40

    matched_vehicle = None
    if parsed.vehicle:
        matched_vehicle = any(
            _phrase_in(vehicles, term) or term in vehicles for term in parsed.vehicle_terms
        )
        parts["vehicle_fitment"] = 60 if matched_vehicle else -30

    if parsed.brand:
        parts["brand"] = 30 if brand == normalize_text(parsed.brand) else -12

    matched_position = None
    position_conflict = False
    if parsed.position:
        if _phrase_in(attributes, parsed.position):
            matched_position = True
            parts["position"] = 18
        elif _phrase_in(attributes, "rear" if parsed.position == "front" else "front"):
            matched_position = False
            position_conflict = True
            parts["position_conflict"] = -25
        else:
            matched_position = False

    matched_side = None
    side_conflict = False
    if parsed.side:
        if _phrase_in(attributes, parsed.side):
            matched_side = True
            parts["side"] = 18
        elif _phrase_in(attributes, "right" if parsed.side == "left" else "left"):
            matched_side = False
            side_conflict = True
            parts["side_conflict"] = -25
        else:
            matched_side = False

    parts["offer_availability"] = min(len(product.supplier_offers), 5) * 0.1
    exact_code = any(
        key in parts
        for key in (
            "exact_reference",
            "normalized_reference",
            "exact_supplier_code",
            "normalized_supplier_code",
        )
    )
    product_match = len(matched_product_terms) == len(parsed.product_terms)
    brand_match = parsed.brand is None or parts.get("brand") == 30
    vehicle_match = parsed.vehicle is None or matched_vehicle is True
    position_match = parsed.position is None or matched_position is True
    side_match = parsed.side is None or matched_side is True
    all_explicit_match = (
        product_match
        and brand_match
        and vehicle_match
        and position_match
        and side_match
        and not related_variant
    )
    if exact_code or all_explicit_match:
        result_group = "EXACT"
    elif (
        product_match
        and brand_match
        and vehicle_match
        and not position_conflict
        and not side_conflict
        and not related_variant
    ):
        result_group = "COMPATIBLE"
    else:
        result_group = "RELATED"
    return ScoredProduct(
        product=product,
        score=round(sum(parts.values()), 2),
        scoring=parts,
        result_group=result_group,
        matched_vehicle=matched_vehicle,
        matched_product_terms=matched_product_terms,
        matched_position=matched_position,
        matched_side=matched_side,
        fitment_match=matched_vehicle,
    )


def _loading_options():
    return (
        selectinload(Product.brand),
        selectinload(Product.category),
        selectinload(Product.reference_numbers),
        selectinload(Product.fitments).selectinload(Fitment.vehicle),
        selectinload(Product.supplier_offers).selectinload(SupplierOffer.supplier),
    )


def _candidate_condition(parsed: ParsedQuery, code: str, category_texts: dict[str, str]):
    conditions = []
    if code:
        conditions.append(
            or_(
                Product.reference_numbers.any(normalized_number=code),
                Product.supplier_offers.any(normalized_supplier_sku=code),
            )
        )

    product_conditions = []
    for term in parsed.product_terms:
        values = parsed.product_expansions[term]
        named_categories = [
            category_id
            for category_id, text in category_texts.items()
            if any(value in text for value in values)
        ]
        product_conditions.append(
            or_(
                *(Product.normalized_name.contains(value) for value in values),
                *([Product.category_id.in_(named_categories)] if named_categories else []),
            )
        )
    if product_conditions:
        conditions.append(and_(*product_conditions))
    elif parsed.vehicle_terms:
        vehicle_condition = or_(
            *(
                or_(
                    Fitment.vehicle.has(Vehicle.normalized_text.contains(term)),
                    Fitment.source_vehicle_text.contains(term),
                )
                for term in parsed.vehicle_terms
            )
        )
        conditions.append(Product.fitments.any(vehicle_condition))
    elif parsed.brand:
        conditions.append(Product.brand.has(Brand.normalized_name == normalize_text(parsed.brand)))
    elif parsed.position or parsed.side:
        attributes = [value for value in (parsed.position, parsed.side) if value]
        conditions.append(and_(*(Product.search_text.contains(value) for value in attributes)))

    return or_(*conditions) if conditions else None


def _rank(
    session: Session,
    query: str,
    vocabulary: SearchVocabulary,
    vehicle_ids: set[str] | None,
    category_ids: set[str] | None = None,
) -> tuple[ParsedQuery, list[ScoredProduct], bool]:
    """Rank one query; returns (parsed, ranked, vehicle_filter_applied)."""
    parsed = parse_query(
        query,
        vocabulary.brand_names,
        vocabulary.product_synonyms,
        vocabulary.vehicle_aliases,
    )
    code = normalize_code(query)
    # A vehicle typed into the query is more specific than the remembered car.
    filter_applied = bool(vehicle_ids) and parsed.vehicle is None
    if not parsed.normalized and not code and not filter_applied and not category_ids:
        return parsed, [], False

    condition = _candidate_condition(parsed, code, vocabulary.category_texts)
    stmt = select(Product).where(Product.is_searchable.is_(True)).options(*_loading_options())
    if filter_applied:
        stmt = stmt.where(fits_vehicles(vehicle_ids))
    if category_ids:
        stmt = stmt.where(Product.category_id.in_(category_ids))
    products = (
        session.scalars(stmt.where(condition) if condition is not None else stmt).unique().all()
    )

    # A miss on product text gets one bounded fuzzy pass over this small catalog.
    fuzzy_fallback = bool(parsed.product_terms and not products)
    if fuzzy_fallback:
        products = session.scalars(stmt).unique().all()

    scored = [
        _score(product, query, parsed, vocabulary.category_texts.get(product.category_id, ""))
        for product in products
    ]
    if fuzzy_fallback:
        scored = [
            item for item in scored if any(key.startswith("fuzzy_product:") for key in item.scoring)
        ]
    # Once the catalog has compatible fitments, suppress other vehicles entirely.
    # If it has none (for example, the current "свеча cobalt" data), retain
    # product-relevant RELATED results instead of incorrectly returning zero.
    if parsed.vehicle and any(item.matched_vehicle is True for item in scored):
        scored = [item for item in scored if item.matched_vehicle is True or item.priority == 0]
    if (filter_applied or category_ids) and not parsed.normalized:
        # Browsing has no relevance; parts fitted to the car come before universal ones.
        ranked = sorted(
            scored,
            key=lambda item: (
                bool(item.product.universal),
                item.product.name.casefold(),
                item.product.id,
            ),
        )
    else:
        ranked = sorted(scored, key=lambda item: (item.priority, -item.score, item.product.id))
    return parsed, ranked, filter_applied


def search_products(
    session: Session,
    query: str,
    limit: int = 20,
    offset: int = 0,
    include_debug: bool = False,
    vehicle_ids: set[str] | None = None,
    vehicle_label: str | None = None,
    spellcheck: bool = True,
    category: Category | None = None,
    category_ids: set[str] | None = None,
) -> SearchResponse:
    vocabulary = load_vocabulary(session)
    parsed, ranked, filter_applied = _rank(session, query, vocabulary, vehicle_ids, category_ids)
    corrected_query = None
    # Only weak result sets (nothing, or RELATED/fuzzy guesses) are worth replacing.
    if spellcheck and parsed.normalized and not any(item.priority <= 2 for item in ranked):
        fallback = None
        for candidate in correction_candidates(query, vocabulary):
            corrected = _rank(session, candidate, vocabulary, vehicle_ids, category_ids)
            if any(item.priority <= 2 for item in corrected[1]):
                fallback = (candidate, corrected)
                break
            if corrected[1] and fallback is None:
                fallback = (candidate, corrected)
        if fallback is None and (shorter := without_unknown_words(query, vocabulary)):
            corrected = _rank(session, shorter, vocabulary, vehicle_ids, category_ids)
            if corrected[1]:
                fallback = (shorter, corrected)
        if fallback:
            corrected_query, (parsed, ranked, filter_applied) = fallback

    page = ranked[offset : offset + limit]
    group_distribution = {
        group: sum(item.result_group == group for item in ranked)
        for group in ("EXACT", "COMPATIBLE", "RELATED")
    }
    popularity = reservation_counts(session, [item.product.id for item in page])
    items = [_product_search_out(item, popularity.get(item.product.id, 0)) for item in page]
    debug = None
    if include_debug:

        def debug_scores(item: ScoredProduct) -> dict:
            components = item.scoring
            reference_score = sum(
                value
                for key, value in components.items()
                if key
                in {
                    "exact_reference",
                    "normalized_reference",
                    "exact_supplier_code",
                    "normalized_supplier_code",
                }
            )
            product_score = sum(
                value for key, value in components.items() if key.startswith("product:")
            )
            fuzzy_score = sum(
                value for key, value in components.items() if key.startswith("fuzzy_product:")
            )
            return {
                "matched_vehicle": item.matched_vehicle,
                "matched_product_terms": item.matched_product_terms,
                "matched_position": item.matched_position,
                "matched_side": item.matched_side,
                "fitment_match": item.fitment_match,
                "total_score": item.score,
                "reference_score": reference_score,
                "product_score": product_score,
                "vehicle_fitment_score": components.get("vehicle_fitment", 0),
                "position_score": components.get("position", 0)
                + components.get("position_conflict", 0),
                "side_score": components.get("side", 0) + components.get("side_conflict", 0),
                "brand_score": components.get("brand", 0),
                "fuzzy_score": fuzzy_score,
                "result_group": item.result_group,
                "score_components": components,
            }

        debug = {
            "parsed_query": parsed.public_dict(),
            "scoring": {item.product.id: debug_scores(item) for item in page},
        }
    return SearchResponse(
        query=query,
        normalized_query=parsed.normalized,
        corrected_query=corrected_query,
        vehicle_filter=(
            VehicleFilterOut(label=vehicle_label or "", vehicle_ids=sorted(vehicle_ids or ()))
            if filter_applied
            else None
        ),
        category_filter=CategoryOut.model_validate(category) if category else None,
        total=len(ranked),
        category_counts=Counter(
            item.product.category_id for item in ranked if item.product.category_id
        ),
        items=items,
        search_debug=debug,
        parsed_query_internal=parsed.public_dict(),
        result_group_distribution_internal=group_distribution,
    )


def get_product_detail(
    session: Session, product_id: str, vehicle_ids: set[str] | None = None
) -> ProductDetail | None:
    """The part with its offers, plus alternatives and job parts for the buyer's car."""
    stmt = (
        select(Product)
        .where(Product.id == product_id, Product.is_searchable.is_(True))
        .options(*_loading_options())
    )
    product = session.scalar(stmt)
    if product is None:
        return None
    offers = [offer_out(offer) for offer in active_sorted_offers(product.supplier_offers)]
    return ProductDetail(
        name_ru=product.name_ru,
        name_en=product.name_en,
        reservation_count=reservation_counts(session, [product.id]).get(product.id, 0),
        alternatives=alternatives(session, product, vehicle_ids),
        complete_the_job=complete_the_job(session, product, vehicle_ids),
        fit_reports=fit_report_summary(session, product.id),
        id=product.id,
        name=product.name,
        brand=product.brand,
        category=product.category,
        universal=product.universal,
        origin=product.origin,
        position=product.position,
        side=product.side,
        engine_hint=product.engine_hint,
        audit_status=product.audit_status,
        reference_numbers=product.reference_numbers,
        vehicle_fitments=product.fitments,
        supplier_offers=offers,
        offers=offers,
    )


def _product_search_out(item: ScoredProduct, reservation_count: int = 0) -> ProductSearchResult:
    offers = [offer_out(offer) for offer in active_sorted_offers(item.product.supplier_offers)]
    return ProductSearchResult(
        id=item.product.id,
        name=item.product.name,
        name_ru=item.product.name_ru,
        name_en=item.product.name_en,
        brand=item.product.brand,
        category=item.product.category,
        universal=item.product.universal,
        origin=item.product.origin,
        position=item.product.position,
        side=item.product.side,
        engine_hint=item.product.engine_hint,
        audit_status=item.product.audit_status,
        reference_numbers=item.product.reference_numbers,
        vehicle_fitments=item.product.fitments,
        supplier_offers=offers,
        offers=offers,
        relevance_score=item.score,
        result_group=item.result_group,
        reservation_count=reservation_count,
    )
