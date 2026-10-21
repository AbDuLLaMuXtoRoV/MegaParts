from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

from app.normalization import normalize_code, normalize_text, sanitize_query
from app.search_vocabulary import (
    POSITION_SYNONYMS,
    PRODUCT_SYNONYMS,
    SIDE_SYNONYMS,
    STOP_WORDS,
    VEHICLE_ALIASES,
)


@dataclass
class ParsedQuery:
    sanitized: str
    normalized: str
    product_terms: list[str] = field(default_factory=list)
    product_expansions: dict[str, tuple[str, ...]] = field(default_factory=dict)
    vehicle: str | None = None
    vehicle_terms: tuple[str, ...] = ()
    brand: str | None = None
    reference: str | None = None
    position: str | None = None
    side: str | None = None

    def public_dict(self) -> dict:
        data = asdict(self)
        for key in ("sanitized", "normalized", "product_expansions", "vehicle_terms"):
            data.pop(key)
        return data


def _contains_phrase(text: str, phrase: str) -> bool:
    return f" {phrase} " in f" {text} "


def _remove_phrase(text: str, phrase: str) -> str:
    return " ".join(re.sub(rf"(?<!\w){re.escape(phrase)}(?!\w)", " ", text).split())


def _find_alias(text: str, groups: dict[str, tuple[str, ...]]) -> tuple[str | None, str | None]:
    choices = sorted(
        (
            (canonical, normalize_text(alias))
            for canonical, aliases in groups.items()
            for alias in aliases
        ),
        key=lambda item: len(item[1]),
        reverse=True,
    )
    for canonical, alias in choices:
        if _contains_phrase(text, alias):
            return canonical, alias
    return None, None


def parse_query(
    query: str,
    brand_names: list[str] | None = None,
    product_synonyms: dict[str, tuple[str, ...]] | None = None,
    vehicle_aliases: dict[str, tuple[str, ...]] | None = None,
) -> ParsedQuery:
    product_synonyms = product_synonyms or PRODUCT_SYNONYMS
    vehicle_aliases = vehicle_aliases or VEHICLE_ALIASES
    sanitized = sanitize_query(query)
    normalized = normalize_text(sanitized)
    position, position_alias = _find_alias(normalized, POSITION_SYNONYMS)
    side, side_alias = _find_alias(normalized, SIDE_SYNONYMS)

    # Product concepts come first so English "spark plug" does not classify
    # "spark" as the Chevrolet model.
    residual = normalized
    product_terms: list[str] = []
    product_expansions: dict[str, tuple[str, ...]] = {}
    choices = sorted(
        (
            (canonical, normalize_text(alias))
            for canonical, aliases in product_synonyms.items()
            for alias in aliases
        ),
        key=lambda item: len(item[1]),
        reverse=True,
    )
    for canonical, alias in choices:
        if canonical not in product_terms and _contains_phrase(residual, alias):
            product_terms.append(canonical)
            product_expansions[canonical] = tuple(
                dict.fromkeys(normalize_text(value) for value in product_synonyms[canonical])
            )
            residual = _remove_phrase(residual, alias)

    vehicle, vehicle_alias = _find_alias(residual, vehicle_aliases)
    vehicle_terms: tuple[str, ...] = ()
    if vehicle and vehicle_alias:
        residual = _remove_phrase(residual, vehicle_alias)
        vehicle_terms = tuple(
            dict.fromkeys(normalize_text(value) for value in vehicle_aliases[vehicle])
        )

    for attribute in filter(None, [position_alias, side_alias]):
        residual = _remove_phrase(residual, attribute)

    brand = None
    for candidate in sorted(brand_names or [], key=len, reverse=True):
        normalized_brand = normalize_text(candidate)
        if _contains_phrase(residual, normalized_brand):
            brand = candidate
            residual = _remove_phrase(residual, normalized_brand)
            break

    compact = normalize_code(query)
    looks_like_reference = bool(
        compact
        and any(char.isdigit() for char in compact)
        and len(compact) >= 4
        and not product_terms
        and vehicle is None
        and brand is None
        and position is None
        and side is None
    )
    unknown_terms = [
        token
        for token in residual.split()
        if (len(token) > 1 or token.isdigit()) and token not in STOP_WORDS
    ]
    if unknown_terms and not looks_like_reference:
        # Each word is its own term, so word order does not matter
        # ("масляный фильтр" finds "Фильтр масляный").
        for term in dict.fromkeys(unknown_terms):
            product_terms.append(term)
            product_expansions[term] = (term,)

    reference = sanitized if looks_like_reference else None
    return ParsedQuery(
        sanitized=sanitized,
        normalized=normalized,
        product_terms=product_terms,
        product_expansions=product_expansions,
        vehicle=vehicle,
        vehicle_terms=vehicle_terms,
        brand=brand,
        reference=reference,
        position=position,
        side=side,
    )
