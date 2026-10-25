"""Derived catalog fields shared by the workbook importer and the catalog editor."""

from __future__ import annotations

from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Fitment, Product, SupplierOffer
from app.normalization import normalize_text

NOT_APPLICABLE = {"N/A", "NA", "NONE", "UNKNOWN", ""}

# Attributes that make two parts with one part number different parts: front/rear,
# left/right, repair size (STD, 0.25) and outer/inner (the blueprint's variant identity).
VARIANT_ATTRIBUTES = ("position", "side", "repair_size", "placement")


def variant_of(attributes: dict[str, str | None]) -> tuple:
    return tuple(attributes.get(code) for code in VARIANT_ATTRIBUTES)


def product_variant(product: Product) -> tuple:
    return variant_of({attribute.attribute_code: attribute.value for attribute in product.attributes})


def compatible_variants(left: tuple, right: tuple) -> bool:
    """Missing is not a conflict; front against rear (or STD against 0.25) is."""
    return all(a is None or b is None or a == b for a, b in zip(left, right, strict=True))


def meaningful(value: str | None) -> bool:
    return bool(value) and value.strip().upper() not in NOT_APPLICABLE


def product_loading_options():
    return (
        selectinload(Product.brand),
        selectinload(Product.category),
        selectinload(Product.attributes),
        selectinload(Product.reference_numbers),
        selectinload(Product.fitments).selectinload(Fitment.vehicle),
        selectinload(Product.supplier_offers).selectinload(SupplierOffer.supplier),
        selectinload(Product.raw_supplier_products),
    )


def refresh_product(product: Product) -> None:
    """Recompute everything search reads from a product's own data and relations."""
    names = [value for value in (product.name, product.name_ru, product.name_en) if value]
    # Sellers' own wording from their price lists ("KALODKA OLDI", "amartizator") finds the
    # part too: buyers search in the same words sellers write.
    seller_names = [
        raw.raw_name
        for raw in product.raw_supplier_products
        if (raw.source_payload or {}).get("price_list")
    ]
    product.normalized_name = normalize_text(
        " ".join([*names, *dict.fromkeys(seller_names)])
    )[:500]

    # A single position/side across all fitments is a property of the part itself.
    positions = {fit.position for fit in product.fitments if meaningful(fit.position)}
    sides = {fit.side for fit in product.fitments if meaningful(fit.side)}
    product.position = next(iter(positions)) if len(positions) == 1 else None
    product.side = next(iter(sides)) if len(sides) == 1 else None

    product.is_searchable = (product.audit_status or "").upper() != "CONFLICT" and (
        product.status or "ACTIVE"
    ).upper() == "ACTIVE"

    category = product.category
    fragments: list[str | None] = [
        *names,
        product.article_number,
        product.brand.name if product.brand else None,
        *((category.name_uz, category.name_ru, category.name_en) if category else ()),
        product.position,
        product.side,
        *(reference.number for reference in product.reference_numbers),
        *(attribute.value for attribute in product.attributes),
    ]
    for fitment in product.fitments:
        fragments.extend([fitment.vehicle.normalized_text, fitment.source_vehicle_text])
    fragments.extend(offer.supplier_sku for offer in product.supplier_offers)
    product.search_text = normalize_text(" ".join(filter(None, fragments)))


def refresh_products(session: Session, product_ids: Iterable[str] | None = None) -> int:
    stmt = select(Product).options(*product_loading_options())
    if product_ids is not None:
        stmt = stmt.where(Product.id.in_(list(product_ids)))
    products = session.scalars(stmt).all()
    for product in products:
        refresh_product(product)
    return len(products)
