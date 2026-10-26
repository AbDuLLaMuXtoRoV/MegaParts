"""Load a seller's price list into the catalog: parts, part numbers, cars, and the offer.

Unlike the strict offer upload (app.supplier_import), which only prices parts already in
the catalog, a price list brings its own parts. Each row becomes a catalog part in the
buyer's languages (app.part_names), fitted to the cars the seller names, with this
seller's offer on it. The same part from another seller (same brand and part number)
becomes a second offer on one part, which is what lets buyers compare sellers.

Run from the command line:
    python -m app.price_list_import --supplier "BOS-KOS" path/to/list.xlsx [...]
"""

from __future__ import annotations

import argparse
import hashlib
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.catalog import compatible_variants, refresh_products, variant_of
from app.models import (
    Brand,
    CatalogReviewItem,
    Category,
    Fitment,
    Product,
    ProductAttribute,
    ProductAudit,
    RawSupplierProduct,
    ReferenceNumber,
    Supplier,
    SupplierImport,
    SupplierOffer,
    Vehicle,
)
from app.normalization import normalize_code, normalize_text
from app.oem import split_numbers, valid_oem
from app.part_names import PartName, display_names, latin_upper, part_numbers, read_part_name
from app.part_types import ensure_standard_part_types
from app.price_list_reader import PriceRow, parse_price_list, promo, warranty

SOURCE_TYPE = "PRICE_LIST"

# Brand column spellings, and the codes sellers append to part numbers ("96553241-N/WSM").
BRAND_ALIASES = {
    "BOS KOS": "BOSKOS", "BOS-KOS": "BOSKOS", "BOSKOS KOREA": "BOSKOS", "NEW BOSKOS": "BOSKOS",
    "SECO KOREA": "SECO", "KPR OEM": "KPR", "GM OEM": "GM", "N/WSM": "NEW WEISMO",
    "NWSM": "NEW WEISMO", "WSM": "WEISMO", "ACDCE": "ACDelco", "AC": "ACDelco",
    "SEOUL KASKET": "SEOUL GASKET", "G": "GM",
}
BUDGET_WORDS = {"ARZONI", "ORZONI", "ARZON"}
COUNTRY_WORDS = {"KOREA": "KR", "KOREYA": "KR", "XITOY": "CN", "KITAY": "CN", "CHINA": "CN",
                 "UZBEKISTAN": "UZ", "O'ZBEKISTON": "UZ", "TURKIYA": "TR", "YAPONIYA": "JP"}
GENUINE_BRANDS = {"GM", "DAEWOO", "GM UZBEKISTAN", "GM KOREA"}
OE_BRANDS = {"OEM", "ACDelco"}
NO_BRAND = "Brendsiz (NO-BREND)"
# Parts that fit any car when the seller names none.
UNIVERSAL_TYPES = {"CAT-DRV-BRG", "CAT-ACC-FAST", "CAT-EL-BULB", "CAT-EL-RELAY", "CAT-OIL",
                   "CAT-OIL-ENG", "CAT-OIL-COOL", "CAT-OIL-BRK", "CAT-EL-WIRE"}


@dataclass(frozen=True)
class ModelRule:
    pattern: str
    make: str
    model: str
    # Generation qualifiers written after the model: "NEXIA 2", "MALIBU 1", "TRACKER 2".
    generations: dict[str, str] = field(default_factory=dict)


# The car names sellers write, Latin or Cyrillic, with common misspellings.
MODEL_RULES: tuple[ModelRule, ...] = (
    ModelRule(r"\bNE(X|KS)I?Y?A ?-?(3|III)\b|\bR3\b", "Chevrolet", "Nexia 3"),
    ModelRule(r"\bNE(X|KS)I?Y?A\b|\bNE(X|KS)I?Y?A(?=\d)", "Daewoo", "Nexia",
              {"1": "N100", "2": "N150", "II": "N150"}),
    ModelRule(r"\bCIELO\b|\bSIELO\b", "Daewoo", "Nexia", {"": "N100"}),
    ModelRule(r"\bMA[IT]+Z\b|\bMATIZ\b|\bBEST\b", "Daewoo", "Matiz"),
    ModelRule(r"\bTI[CK]O\b", "Daewoo", "Tico"),
    ModelRule(r"\bDAMA[SDZ]\b", "Daewoo", "Damas"),
    ModelRule(r"\bLABO\b", "Daewoo", "Labo"),
    ModelRule(r"\bSPARK\b", "Chevrolet", "Spark"),
    ModelRule(r"\bLA[CSN]+ET+I\b", "Chevrolet", "Lacetti"),
    ModelRule(r"\b(D?J|G)ENTI?RA\b", "Chevrolet", "Gentra"),
    ModelRule(r"\b[CK]OBALT\b", "Chevrolet", "Cobalt"),
    ModelRule(r"\bONI(X|KS)\b", "Chevrolet", "Onix"),
    ModelRule(r"\bMALIBU\b", "Chevrolet", "Malibu", {"1": "VIII", "2": "IX"}),
    ModelRule(r"\b[CK]APTIVA\b", "Chevrolet", "Captiva", {"1": "C100", "2": "C140"}),
    ModelRule(r"\bEPI[CK]A\b|\bTOS[CK]A\b", "Chevrolet", "Epica"),
    ModelRule(r"\bCRU[ZS]E?\b|\bKRUZ\b", "Chevrolet", "Cruze"),
    ModelRule(r"\bORLANDO\b", "Chevrolet", "Orlando"),
    ModelRule(r"\bTRA[CK]+ER\b", "Chevrolet", "Tracker", {"1": "I (", "2": "II "}),
    ModelRule(r"\bEQUINOX\b", "Chevrolet", "Equinox"),
    ModelRule(r"\bMONZA\b", "Chevrolet", "Monza"),
    ModelRule(r"\bAVEO\b|\bKALOS\b", "Chevrolet", "Aveo"),
    ModelRule(r"\bLANOS\b", "Daewoo", "Lanos"),
    ModelRule(r"\bESPERO\b", "Daewoo", "Espero"),
    ModelRule(r"\bLEGANZA\b", "Daewoo", "Leganza"),
    ModelRule(r"\bNUBIRA\b", "Daewoo", "Nubira"),
    ModelRule(r"\bPRINCE\b", "Daewoo", "Prince"),
    ModelRule(r"\bGRACE\b|\bGREYS\b", "Hyundai", "Grace"),
    ModelRule(r"\bPORTER\b", "Hyundai", "Porter"),
    ModelRule(r"\bSTAREKS?\b|\bSTAREX\b", "Hyundai", "Starex"),
    ModelRule(r"\bGRAND[UE]+R\b", "Hyundai", "Grandeur"),
    ModelRule(r"\bBONGO\b", "Kia", "Bongo"),
    ModelRule(r"\bSORENTO\b", "Kia", "Sorento"),
    ModelRule(r"\bISUZ[UI]\b", "Isuzu", "(model aniqlanmagan)"),
    ModelRule(r"\bBYD ?SONG\b|\bBYDSONG\b", "BYD", "Song Plus"),
    ModelRule(r"\bCHAZOR\b|\bCHASER\b", "BYD", "Chazor"),
    ModelRule(r"\bSEAGULL\b", "BYD", "Seagull"),
    ModelRule(r"\bBYD SEAL\b", "BYD", "Seal"),
    ModelRule(r"\bTIGGO ?8\b", "Chery", "Tiggo 8 Pro"),
    ModelRule(r"\bJETOUR\b", "Jetour", "(model aniqlanmagan)"),
)
_COMPILED_MODELS = tuple((re.compile(rule.pattern), rule) for rule in MODEL_RULES)
# Cars sellers name that the catalog did not list yet: (make, model) -> (generation, aliases).
NEW_VEHICLES: dict[tuple[str, str], tuple[str, str]] = {
    ("Chevrolet", "Aveo"): ("T250 · 1.5", "Авео;Kalos;Калос"),
    ("Daewoo", "Lanos"): ("T100 · 1.5", "Ланос"),
    ("Daewoo", "Espero"): ("— · 1.5 / 2.0", "Эсперо"),
    ("Daewoo", "Leganza"): ("— · 2.0", "Леганза"),
    ("Daewoo", "Nubira"): ("— · 1.6", "Нубира"),
    ("Daewoo", "Prince"): ("— · 2.0", "Принц"),
    ("Hyundai", "Grace"): ("H-100 · 2.5 dizel", "Грейс;H-100;H100"),
    ("Hyundai", "Porter"): ("II · 2.5 dizel", "Портер;Porter 2;Porter II"),
    ("Hyundai", "Starex"): ("— · 2.5 dizel", "Старекс;H-1;H1"),
    ("Hyundai", "Grandeur"): ("— · 3.0", "Грандер;Grandeur"),
    ("Kia", "Bongo"): ("III · 2.5 / 2.7 dizel", "Бонго;Bongo 3;Bongo III"),
    ("Isuzu", "(model aniqlanmagan)"): ("Model aniqlanmagan — fitmentni aniqlang", ""),
    ("BYD", "Seal"): ("— · EV", "Сил"),
}
_ENGINE = re.compile(r"\b(\d\.\d{1,2})\b")


def _model_text(text: str) -> str:
    value = latin_upper(text)
    value = re.sub(r"(\d),(\d)", r"\1.\2", value)
    value = re.sub(r"1\.616V", "1.6 16V", value)
    value = re.sub(r"(?<=[A-Z])\.(?=[A-Z\d])", " ", value)
    value = re.sub(r"(?<=[A-Z]{3})(?=\d)", " ", value)
    value = re.sub(r"\bDONS\b", "DOHC", value)
    return " ".join(re.sub(r"[,/()+]", " / ", value).split())


@dataclass
class CarMatch:
    vehicle_ids: list[str]
    note: str | None


class VehicleIndex:
    """The catalog's cars, found by the names sellers write; missing ones are added."""

    def __init__(self, session: Session):
        self.session = session
        self.by_model: dict[tuple[str, str], list[Vehicle]] = defaultdict(list)
        for vehicle in session.scalars(select(Vehicle)):
            self.by_model[(vehicle.make or "", vehicle.model)].append(vehicle)
        self.created: list[Vehicle] = []

    def _vehicles(self, make: str, model: str) -> list[Vehicle]:
        found = self.by_model.get((make, model))
        if found:
            return found
        if (make, model) not in NEW_VEHICLES:
            return []
        generation, aliases = NEW_VEHICLES[(make, model)]
        numbers = [
            int(match.group(1))
            for vehicle_id in self.session.scalars(select(Vehicle.id))
            if (match := re.fullmatch(r"V-(\d+)", vehicle_id))
        ]
        vehicle = Vehicle(
            id=f"V-{max(numbers, default=0) + 1:05d}",
            make=make,
            model=model,
            generation=generation,
            aliases=aliases or None,
            normalized_text=normalize_text(" ".join(filter(None, [make, model, generation,
                                                                  aliases])))[:600],
            vehicle_source="MANUAL",
            data_confidence="LOW",
        )
        self.session.add(vehicle)
        self.session.flush()
        self.by_model[(make, model)] = [vehicle]
        self.created.append(vehicle)
        return [vehicle]

    def match(self, text: str | None) -> CarMatch:
        if not text or not text.strip():
            return CarMatch([], None)
        value = _model_text(text)
        hits = []
        for pattern, rule in _COMPILED_MODELS:
            for found in pattern.finditer(value):
                if not any(start <= found.start() < end for start, end, _ in hits):
                    hits.append((found.start(), found.end(), rule))
        if not hits and re.search(r"\b(DOHC|SOHC|16V|8V)\b", value):
            hits = [(0, 0, MODEL_RULES[1])]  # "DOHC" alone is how sellers write the Nexia.
        hits.sort(key=lambda hit: hit[0])

        ids: list[str] = []
        broad = False
        for index, (start, end, rule) in enumerate(hits):
            tail = value[end: hits[index + 1][0] if index + 1 < len(hits) else len(value)]
            vehicles = list(self._vehicles(rule.make, rule.model))
            if not vehicles:
                continue
            vehicles = self._narrow(rule, vehicles, tail)
            generations = {vehicle.generation_code or vehicle.generation for vehicle in vehicles}
            broad = broad or len(vehicles) > 1 and len(generations) > 1
            ids.extend(vehicle.id for vehicle in vehicles)
        notes = []
        if re.search(r"\bA ?/ ?T\b|\bAT\b|\bAKPP\b", value):
            notes.append("KPP: AT")
        elif re.search(r"\bM ?/ ?T\b|\bMT\b|\bMKPP\b", value):
            notes.append("KPP: MT")
        if broad:
            notes.insert(0, f"'{text.strip()}' deb yozilgan — avlodni tekshiring")
        return CarMatch(list(dict.fromkeys(ids)), "; ".join(notes) or None)

    @staticmethod
    def _narrow(rule: ModelRule, vehicles: list[Vehicle], tail: str) -> list[Vehicle]:
        """Keep the generations the seller's qualifiers point at, when any match."""

        def keep(test) -> None:
            nonlocal vehicles
            kept = [vehicle for vehicle in vehicles if test(vehicle.generation or "")]
            if kept:
                vehicles = kept

        tokens = tail.split()
        if "" in rule.generations:
            keep(lambda gen: rule.generations[""] in gen)
        for token in tokens[:2]:
            if token in rule.generations:
                keep(lambda gen, mark=rule.generations[token]: mark in gen)
                break
        if re.search(r"\b(DOHC|16V)\b", tail):
            keep(lambda gen: "DOHC" in gen)
        elif re.search(r"\b(SOHC|8V)\b", tail):
            keep(lambda gen: "SOHC" in gen)
        if engine := _ENGINE.search(tail):
            size = engine.group(1)
            if rule.model == "Spark" and size in {"1.2", "1.25"}:
                size = "1.25"
            elif rule.model == "Spark" and size in {"1.0", "1.1"}:
                size = "1.0"
            keep(lambda gen: re.search(rf"(?<![\d.]){re.escape(size)}(?![\d])", gen) is not None)
        elif rule.model == "Spark" and re.match(r"^1\b", tail.strip()):
            keep(lambda gen: "1.0" in gen)
        return vehicles


@dataclass
class ImportResult:
    batch: SupplierImport
    products_created: int = 0
    products_reused: int = 0
    offers_created: int = 0
    offers_updated: int = 0
    offers_closed: int = 0
    vehicles_created: list[str] = field(default_factory=list)
    unrecognised: list[str] = field(default_factory=list)
    without_car: int = 0


# A maker's article typed into the brand column ("KOS-1101"): the letters are the brand.
_BRAND_COLUMN_ARTICLE = re.compile(r"([A-Z][A-Z&]+)[- ]?(\d{3,}[A-Z0-9]*)")


def _brand_column_article(row: PriceRow) -> str | None:
    text = " ".join(latin_upper(row.brand or "").split())
    return text if _BRAND_COLUMN_ARTICLE.fullmatch(text) else None


def number_kind(number: str, oem: dict[str, str], brand_name: str | None) -> str:
    """OE for numbers from the seller's OEM column; a number that starts with the part's own
    brand ("KOS-1303" on a KOS seal) is that maker's article; otherwise by its shape."""
    normalized = normalize_code(number)
    if normalized in oem:
        return "OE"
    prefix = normalize_code(brand_name or "")
    if prefix and normalized.startswith(prefix) and normalized[len(prefix):][:3].isdigit():
        return "AFTERMARKET"
    return reference_type(number)


def _brand_name(row: PriceRow, part: PartName) -> tuple[str | None, str | None, bool]:
    """(brand, country, budget) from the brand column, the code suffix or the name."""
    country = COUNTRY_WORDS.get(latin_upper(row.country or ""))
    budget = False
    raw = latin_upper(row.brand or "")
    for word, code in COUNTRY_WORDS.items():
        if re.search(rf"\b{word}\b", raw):
            country = country or code
            raw = re.sub(rf"\b{word}\b", " ", raw)
    raw = " ".join(raw.split())
    if article := _BRAND_COLUMN_ARTICLE.fullmatch(raw):
        raw = article.group(1)
    if raw in BUDGET_WORDS:
        raw, budget = "", True
    if not raw and row.code:
        # "96181229 WSM", "96553241-N/WSM", "96983945-G", "S4511003-AC", "CBKD-1 CTR".
        suffix = re.search(r"(?:\s|-)(N/WSM|WSM|AC|G|CTR)\s*$", latin_upper(row.code))
        raw = suffix.group(1) if suffix else ""
    name_upper = latin_upper(row.name)
    if not raw:
        for candidate in ("NEW WEISMO", "WEISMO", "WSM", "DONGIL", "GMB", "SIB", "CTR", "SLT",
                          "VALEO", "YURA", "BOSKOS"):
            if re.search(rf"\b{re.escape(candidate)}\b", name_upper):
                raw = candidate
                break
    if any(word in name_upper.split() for word in BUDGET_WORDS):
        budget = True
    if country is None:
        country = next(
            (code for word, code in COUNTRY_WORDS.items() if re.search(rf"\b{word}\b", name_upper)),
            None,
        )
    brand = BRAND_ALIASES.get(raw, raw) or None
    return brand, country, budget


def _origin(brand: str | None) -> str:
    """The catalog's origin list: ORIGINAL (carmaker), OES (factory supplier), AFTERMARKET."""
    if brand in GENUINE_BRANDS:
        return "ORIGINAL"
    if brand in OE_BRANDS:
        return "OES"
    return "AFTERMARKET"


def _offer_origin(brand: str | None, budget: bool) -> str:
    """The label on the seller's offer: genuine, factory supplier, analog or budget."""
    if budget:
        return "BUDGET"
    return {"ORIGINAL": "GENUINE", "OES": "OE"}.get(_origin(brand), "AFTERMARKET")


def _unit(value: str | None) -> str | None:
    text = latin_upper(value or "").replace(".", "")
    if text in {"KOMP", "K-T", "KT", "KOMPLEKT", "SET", "JUFT", "PAR"}:
        return "SET"
    if text in {"DONA", "SHT", "SH-T", "PCS"}:
        return "PCS"
    return None


# Carmaker numbers: GM (96273708, 7848744), Suzuki-built Damas/Tico (74120A78B00),
# Hyundai/Kia (54300-4E400).
_OE_NUMBER = (
    re.compile(r"\d{7,8}"),
    re.compile(r"\d{5}[A-Z]\d{2}[A-Z0-9]\d{2}(?:-\d{3})?"),
    re.compile(r"\d{5}-[0-9A-Z]{5}(?:-\d{3})?"),
)
# Part makers' own articles: CTR (CBKD-15), bearings (6203-RS, TP-32004J), Bosch (0580453434).
_BRAND_ARTICLE = (
    re.compile(r"C[BREQT][A-Z]{2}-?\d{1,3}[RL]?"),
    re.compile(r"\d{4,5}-?2?RS"),
    re.compile(r"[A-Z]{2}-\d{4,6}[A-Z0-9-]*"),
    re.compile(r"DT\d{4,}"),
    re.compile(r"\d{9,10}"),
)


def reference_type(number: str) -> str:
    """OE for carmaker numbers, AFTERMARKET for part makers' articles, and SUPPLIER_SKU for
    everything else: a seller's own code (NP1013, 0829, PT 43) is never a part number."""
    if any(pattern.fullmatch(number) for pattern in _OE_NUMBER):
        return "OE"
    if any(pattern.fullmatch(number) for pattern in _BRAND_ARTICLE):
        return "AFTERMARKET"
    return "SUPPLIER_SKU"


DESCRIPTOR_ATTRIBUTES = {"AT": ("transmission", "AT"), "MT": ("transmission", "MT"),
                         "DOHC": ("engine_type", "DOHC"), "SOHC": ("engine_type", "SOHC")}


def part_attributes(part: PartName) -> dict[str, str]:
    """The attributes a seller's name gives, in the catalog's codes and list values."""
    values = {
        "position": (part.position or "").upper() or None,
        "side": (part.side or "").upper() or None,
        "repair_size": part.size,
        "placement": {"outer": "OUTER", "inner": "INNER"}.get(part.placement or ""),
    }
    for names in part.descriptors:
        if names[0] in DESCRIPTOR_ATTRIBUTES:
            code, value = DESCRIPTOR_ATTRIBUTES[names[0]]
            values[code] = value
    if part.specs:
        values["spec_code"] = " ".join(part.specs)
    return {code: value for code, value in values.items() if value}


def _next_product_ids(session: Session):
    numbers = [
        int(match.group(1))
        for product_id in session.scalars(select(Product.id))
        if (match := re.fullmatch(r"P-(\d+)", product_id))
    ]
    current = max(numbers, default=0)
    while True:
        current += 1
        yield f"P-{current:06d}"


def _creator(product: Product) -> int | None:
    """The seller whose price list created the part ("PRICE_LIST:{supplier}:{row}")."""
    parts = (product.source_rows or "").split(":")
    return int(parts[1]) if len(parts) > 2 and parts[0] == SOURCE_TYPE and parts[1].isdigit() else None


class _Catalog:
    """Lookups the import needs, kept in memory so a 2,000-row list stays quick.

    Parts are matched across sellers only on a strong signal: the same brand and the same
    carmaker number or part maker's article, with no conflicting variant (front/rear,
    left/right, repair size). A seller's own code and a similar name are never enough; a
    similar name from another seller is only suggested for review.
    """

    def __init__(self, session: Session):
        self.session = session
        self.categories = {category.id: category for category in session.scalars(select(Category))}
        self.brands = {brand.normalized_name: brand for brand in session.scalars(select(Brand))}
        self.by_number: dict[tuple[int | None, str], list[Product]] = defaultdict(list)
        self.by_name: dict[tuple, list[Product]] = defaultdict(list)
        self.variants: dict[str, tuple] = {}
        products = session.scalars(
            select(Product).options(
                selectinload(Product.reference_numbers),
                selectinload(Product.fitments),
                selectinload(Product.attributes),
            )
        ).all()
        for product in products:
            self.variants[product.id] = variant_of(
                {attribute.attribute_code: attribute.value for attribute in product.attributes}
            )
            for reference in product.reference_numbers:
                if reference.type != "SUPPLIER_SKU":
                    self.by_number[(product.brand_id, reference.normalized_number)].append(product)
            if _creator(product) is not None:
                self.by_name[self.name_key(product.brand_id, product.name, product.fitments)].append(
                    product
                )
        self.ids = _next_product_ids(session)

    @staticmethod
    def name_key(brand_id, name, fitments) -> tuple:
        vehicles = frozenset(fit.vehicle_id if hasattr(fit, "vehicle_id") else fit for fit in fitments)
        return (brand_id, (name or "").casefold(), vehicles)

    def by_part_number(self, brand_id, numbers: list[str], variant: tuple) -> tuple:
        """(the part to add to, a part this one collides with) for the strong numbers."""
        collision = None
        for number in numbers:
            for product in self.by_number.get((brand_id, normalize_code(number)), []):
                if compatible_variants(self.variants.get(product.id, (None,) * 4), variant):
                    return product, None
                collision = collision or product
        return None, collision

    def brand(self, name: str | None) -> Brand:
        name = name or NO_BRAND
        key = normalize_text(name)
        if key not in self.brands:
            brand = Brand(
                name=name,
                normalized_name=key,
                brand_type="OE" if name in GENUINE_BRANDS else "AFTERMARKET",
                # Parts sold without a brand are the budget choice.
                quality_tier="ECONOMY" if name == NO_BRAND else "UNKNOWN",
            )
            self.session.add(brand)
            self.session.flush()
            self.brands[key] = brand
        return self.brands[key]


def _review(session: Session, raw_id: str, supplier: Supplier, product: Product, row: PriceRow,
            name: str, reason: str) -> None:
    """A question for the catalog team, shown on the part in the catalog editor."""
    session.flush()  # the review points at the part, which must be saved first
    session.merge(
        CatalogReviewItem(
            raw_id=raw_id[:64], supplier=supplier.name, product_id=product.id, raw_name=row.name,
            parsed_product_name=name, brand=row.brand, reference=row.code, vehicle_raw=row.model,
            review_reason=reason, status="TO REVIEW",
        )
    )


def import_price_list(
    session: Session,
    supplier: Supplier,
    content: bytes,
    filename: str | None = None,
    received_at: datetime | None = None,
) -> ImportResult:
    """Add the list's parts to the catalog and replace this seller's price-list offers."""
    received_at = received_at or datetime.now(UTC)
    price_list = parse_price_list(content, filename)
    batch = SupplierImport(
        supplier_id=supplier.id, source_filename=filename, source_type="EXCEL",
        status="PROCESSING",
    )
    session.add(batch)
    session.flush()
    result = ImportResult(batch=batch)

    if price_list.phones and not supplier.phone:
        supplier.phone = price_list.phones[0]
    if price_list.telegram and not supplier.telegram:
        supplier.telegram = price_list.telegram
    supplier.integration = supplier.integration or "EXCEL"

    ensure_standard_part_types(session)
    catalog = _Catalog(session)
    cars = VehicleIndex(session)
    offers = {
        offer.product_id: offer
        for offer in session.scalars(
            select(SupplierOffer).where(
                SupplierOffer.supplier_id == supplier.id,
                SupplierOffer.source_reference.like(f"{SOURCE_TYPE}:%"),
            )
        )
    }
    seen_offers: set[int] = set()
    touched: set[str] = set()
    file_tag = hashlib.sha1((filename or "").encode()).hexdigest()[:8]

    for row in price_list.rows:
        batch.rows_received += 1
        raw_id = f"PL-{supplier.id}-{file_tag}-{row.row_number}"
        part = read_part_name(row.name, row.model or "")
        # Numbers from a column the seller titled OEM are the carmaker's, whatever their shape.
        oem = {
            normalize_code(number): number for number in split_numbers(row.oem) if valid_oem(number)
        }
        brand_name, country, budget = _brand_name(row, part)
        article = _brand_column_article(row)
        numbers = list(dict.fromkeys(
            [*oem.values(), *([article] if article else []), *part_numbers(row.code or ""), *part.numbers]
        ))
        if part.side is None and row.code:
            code = latin_upper(row.code)
            part.side = "left" if re.search(r"\dL\b|-L\b", code) else (
                "right" if re.search(r"\dR\b|-R\b", code) else None)
        attributes = part_attributes(part)
        variant = variant_of(attributes)
        strong = [number for number in numbers if number_kind(number, oem, brand_name) != "SUPPLIER_SKU"]
        brand = catalog.brand(brand_name)
        car = cars.match(row.model or "") if row.model else cars.match(row.name)
        if not car.vehicle_ids:
            result.without_car += 1
        category = catalog.categories.get(part.type_id) if part.type_id else None
        if category is None:
            result.unrecognised.append(row.name)
        type_names = (
            (category.name_uz, category.name_ru or category.name_uz,
             category.name_en or category.name_uz) if category else None
        )
        name_uz, name_ru, name_en = display_names(part, type_names)

        product, collision = catalog.by_part_number(brand.id, strong, variant)
        reviews = []
        match_status = "MATCHED_AUTO"
        name_key = catalog.name_key(brand.id, name_uz, car.vehicle_ids)
        if product is None and not strong:
            # Without a part number, only this seller's own earlier row is the same part.
            product = next(
                (candidate for candidate in catalog.by_name.get(name_key, [])
                 if _creator(candidate) == supplier.id),
                None,
            )
        if product is None:
            match_status = "NEW_PRODUCT"
            product = Product(
                id=next(catalog.ids),
                name=name_uz,
                name_ru=name_ru,
                name_en=name_en,
                normalized_name=normalize_text(f"{name_uz} {name_ru} {name_en}"),
                brand=brand,
                category=category,
                article_number=(strong or numbers or [None])[0],
                unit=_unit(row.unit),
                country_of_origin=country,
                origin=_origin(brand_name),
                universal=not car.vehicle_ids and part.type_id in UNIVERSAL_TYPES,
                status="ACTIVE",
                audit_status="UNAUDITED",
                merge_basis="BRAND_REFERENCE" if strong else "SUPPLIER_ROW",
                source_rows=f"{SOURCE_TYPE}:{supplier.id}:{row.row_number}",
            )
            for code, value in attributes.items():
                product.attributes.append(
                    ProductAttribute(attribute_code=code, value=value, source=SOURCE_TYPE)
                )
            session.add(product)
            result.products_created += 1
            catalog.variants[product.id] = variant
            catalog.by_name[name_key].append(product)
            if collision is not None:
                reviews.append(
                    f"Bir xil brend va raqam ({strong[0]}), lekin variant boshqa: "
                    f"{collision.id} '{collision.name}' bilan solishtiring"
                )
            elif not strong:
                twins = [candidate for candidate in catalog.by_name.get(name_key, [])
                         if candidate is not product and _creator(candidate) != supplier.id]
                if twins:
                    reviews.append(
                        f"Boshqa sotuvchida shu nom, brend va mashina: {twins[0].id} — "
                        "bir xil detalmi? (raqamsiz, avtomatik birlashtirilmadi)"
                    )
            if category is None:
                reviews.append("Detal turi aniqlanmadi — sotuvchi nomi bilan qoldirildi")
        else:
            result.products_reused += 1
            if product.country_of_origin is None:
                product.country_of_origin = country
            have = {attribute.attribute_code for attribute in product.attributes}
            for code, value in attributes.items():
                if code not in have:
                    product.attributes.append(
                        ProductAttribute(attribute_code=code, value=value, source=SOURCE_TYPE)
                    )
            catalog.variants[product.id] = tuple(
                a or b for a, b in zip(catalog.variants.get(product.id, (None,) * 4), variant,
                                       strict=True)
            )

        have_numbers = {reference.normalized_number: reference for reference in product.reference_numbers}
        for number in numbers:
            normalized = normalize_code(number)
            known = have_numbers.get(normalized)
            if known is not None and normalized in oem and known.type not in ("OE", "OES"):
                known.type = "OE"
            if not normalized or known is not None:
                continue
            kind = number_kind(number, oem, brand_name)
            product.reference_numbers.append(
                ReferenceNumber(number=number, normalized_number=normalized, type=kind,
                                source_supplier_id=supplier.id, cross_source="SUPPLIER",
                                confidence="MEDIUM")
            )
            have_numbers[normalized] = product.reference_numbers[-1]
            if kind != "SUPPLIER_SKU":
                catalog.by_number[(brand.id, normalized)].append(product)
        fitted = {
            fit.vehicle_id for fit in product.fitments if fit.source_supplier_id == supplier.id
        }
        for vehicle_id in car.vehicle_ids:
            if vehicle_id not in fitted:
                product.fitments.append(
                    Fitment(vehicle_id=vehicle_id, source_supplier_id=supplier.id,
                            source_vehicle_text=row.model or None,
                            position=attributes.get("position"), side=attributes.get("side"),
                            condition_note=car.note, fitment_source="SUPPLIER",
                            confidence="LOW")
                )
                fitted.add(vehicle_id)
        for reason in reviews:
            _review(session, raw_id, supplier, product, row, name_uz, reason)

        # The seller's own wording stays searchable, even on a repeated row.
        session.add(
            RawSupplierProduct(
                source_raw_id=raw_id, supplier_id=supplier.id, source_row=row.row_number,
                product=product, raw_name=row.name, parsed_product_name=name_uz,
                raw_brand=row.brand, supplier_code=row.code,
                supplier_code_type="SUPPLIER_SKU" if row.code else None, origin=country,
                unit=row.unit, vehicle_raw=row.model, position=part.position, side=part.side,
                audit_status=match_status,
                audit_reason="; ".join(reviews) or None,
                source_payload={"price_list": True, "file": filename, "import_id": batch.id,
                                "section": row.section, "status": row.status},
            )
        )
        touched.add(product.id)
        offer = offers.get(product.id)
        if offer is None:
            offer = SupplierOffer(
                source_offer_id=uuid4().hex, supplier_id=supplier.id, product=product,
                source_type="EXCEL",
            )
            session.add(offer)
            offers[product.id] = offer
            result.offers_created += 1
        elif offer.id in seen_offers:
            # The same part twice in one list: the first row's price stands.
            batch.rows_matched += 1
            continue
        else:
            result.offers_updated += 1
        months, km = warranty(row.section)
        label, discount = promo(row.status)
        sku = (row.code or "").strip() or None
        offer.supplier_sku = sku
        offer.normalized_supplier_sku = normalize_code(sku) or None
        offer.price = row.price
        offer.currency = row.currency or supplier.default_currency or "UZS"
        offer.stock_qty = row.stock_qty
        offer.pack_qty = row.pack_qty
        offer.updated_at = received_at
        offer.source_type = "EXCEL"
        offer.data_status = "LIVE"
        offer.is_active = True
        offer.part_origin = _offer_origin(brand_name, budget)
        offer.warranty_months = months
        offer.warranty_km = km
        offer.promo = label
        offer.discount_percent = discount
        offer.source_reference = f"{SOURCE_TYPE}:{batch.id}:row:{row.row_number}"
        session.flush()
        seen_offers.add(offer.id)
        batch.rows_matched += 1

    # Parts the seller no longer lists are no longer on offer.
    for offer in offers.values():
        if offer.id not in seen_offers and offer.is_active:
            offer.is_active = False
            result.offers_closed += 1

    session.flush()
    _audit_merges(session, touched)
    refresh_products(session, touched)
    batch.new_offers = result.offers_created
    batch.updated_offers = result.offers_updated
    batch.unmatched_rows = len(result.unrecognised)
    batch.status = "COMPLETED"
    result.vehicles_created = [f"{v.make} {v.model}" for v in cars.created]
    session.flush()
    return result


def _audit_merges(session: Session, product_ids: set[str]) -> None:
    """Cross-supplier audit for parts several sellers offer: CONFIRMED when their names agree
    on the variant, PROBABLE when one of them leaves it out (as in the workbook's audit)."""
    products = session.scalars(
        select(Product)
        .where(Product.id.in_(product_ids))
        .options(selectinload(Product.raw_supplier_products), selectinload(Product.attributes))
    ).all()
    for product in products:
        rows = [raw for raw in product.raw_supplier_products
                if (raw.source_payload or {}).get("price_list")]
        sellers = {raw.supplier_id for raw in rows}
        if len(sellers) < 2:
            continue
        marks = {(raw.position, raw.side) for raw in rows}
        status = "CONFIRMED" if len(marks) == 1 else "PROBABLE"
        # Read everything before adding a new audit: a lazy load would flush it half-filled.
        reference = next((ref.number for ref in product.reference_numbers
                          if ref.type != "SUPPLIER_SKU"), None)
        brand = product.brand.name if product.brand else None
        supplier_names = ", ".join(sorted({raw.supplier.name for raw in rows}))
        audit = session.scalar(
            select(ProductAudit).where(
                ProductAudit.product_id == product.id,
                ProductAudit.audit_reason.like(f"{SOURCE_TYPE}%"),
            )
        )
        if audit is None:
            audit = ProductAudit(product_id=product.id, merge_status=status)
            session.add(audit)
        audit.brand = brand
        audit.reference = reference
        audit.master_name = product.name
        audit.supplier_count = len(sellers)
        audit.suppliers = supplier_names
        audit.merge_status = status
        audit.audit_reason = f"{SOURCE_TYPE}: brend va raqam bir xil ({reference})"
        audit.source_rows = ", ".join(sorted({raw.source_raw_id for raw in rows}))[:2000]


def rename_price_list_parts(session: Session) -> int:
    """Re-read every price-list part's name from the seller's wording, after the name rules
    improve; returns how many parts changed. Workbook parts are left alone."""
    ensure_standard_part_types(session)
    categories = {category.id: category for category in session.scalars(select(Category))}
    products = session.scalars(
        select(Product)
        .where(Product.source_rows.like(f"{SOURCE_TYPE}:%"))
        .options(selectinload(Product.raw_supplier_products))
    ).all()
    changed = []
    for product in products:
        raws = sorted(product.raw_supplier_products, key=lambda raw: raw.id)
        if not raws:
            continue
        part = read_part_name(raws[0].raw_name, raws[0].vehicle_raw or "")
        category = categories.get(part.type_id) if part.type_id else None
        type_names = (
            (category.name_uz, category.name_ru or category.name_uz,
             category.name_en or category.name_uz) if category else None
        )
        names = display_names(part, type_names)
        if (product.name, product.name_ru, product.name_en, product.category_id) != (
            *names, category.id if category else None
        ):
            product.name, product.name_ru, product.name_en = names
            product.category = category
            changed.append(product.id)
    session.flush()
    refresh_products(session, changed)
    return len(changed)


def supplier_by_name(session: Session, name: str, **fields) -> Supplier:
    """The seller with this name, created (unverified) when it is new."""
    normalized = normalize_text(name)
    supplier = session.scalar(select(Supplier).where(Supplier.normalized_name == normalized))
    if supplier is None:
        supplier = Supplier(name=name, normalized_name=normalized, is_active=True,
                            supplier_type=fields.pop("supplier_type", None), **fields)
        session.add(supplier)
        session.flush()
    return supplier


def main() -> None:
    from app.database import SessionLocal

    parser = argparse.ArgumentParser(description="Load sellers' price lists into the catalog.")
    parser.add_argument("--supplier", required=True, help="Seller name, created if new")
    parser.add_argument("--city", default=None)
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    with SessionLocal() as session:
        supplier = supplier_by_name(session, args.supplier, city=args.city)
        for path in args.files:
            received = datetime.fromtimestamp(path.stat().st_mtime, UTC)
            result = import_price_list(session, supplier, path.read_bytes(), path.name, received)
            print(
                f"{path.name}: {result.batch.rows_received} rows, "
                f"{result.products_created} new parts, {result.products_reused} existing, "
                f"{result.offers_created} new offers, {result.offers_updated} updated, "
                f"{result.offers_closed} closed, {result.without_car} without a car, "
                f"{len(result.unrecognised)} unrecognised names; new cars: "
                f"{', '.join(result.vehicles_created) or 'none'}"
            )
        session.commit()


if __name__ == "__main__":
    main()
