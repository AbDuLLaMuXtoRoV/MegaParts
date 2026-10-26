"""OEM codes: the carmaker's own number for a part, shown on every part page.

Sellers' lists give most codes. Staff fill in the rest, one part at a time or as an Excel
file, and check codes that buyers and mechanics send. A code that the same part from
another seller carries is only offered as a suggestion: the blueprint keeps weak matches
out of the catalog until a person confirms them.
"""

from __future__ import annotations

import re
from collections import defaultdict
from datetime import UTC, datetime
from difflib import SequenceMatcher
from io import BytesIO
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, File, HTTPException, Query, Request, UploadFile
from fastapi.responses import Response
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from pydantic import BaseModel, Field
from sqlalchemy import case, exists, func, select
from sqlalchemy.orm import Session

from app.auth import COOKIE_NAME, session_user
from app.catalog import (
    compatible_variants,
    product_loading_options,
    product_variant,
    refresh_product,
)
from app.config import get_settings
from app.database import get_session
from app.models import OemSuggestion, Product, ReferenceNumber, Supplier, SupplierOffer
from app.normalization import normalize_code, normalize_text
from app.part_names import part_numbers

settings = get_settings()
router = APIRouter(prefix="/api/admin/oem", tags=["OEM codes"])
public_router = APIRouter(prefix=settings.api_prefix, tags=["OEM codes"])
SessionDep = Annotated[Session, Depends(get_session)]

OEM_TYPES = ("OE", "OES")
PAGE_SIZE = 50
MAX_CANDIDATES = 3
# How alike two parts' names must be ("Shpilka" / "Shpilka, oldi g'ildirak") to offer the
# other part's OEM code; a vague name ("Kuzov detallari") matches nothing.
CANDIDATE_NAME_RATIO = 0.6
# GM 96273708, Hyundai/Kia 58101-1RA00, Toyota 04465-33450: letters and digits, mostly digits.
_MIN_LENGTH, _MAX_LENGTH, _MIN_DIGITS = 5, 30, 3
_SEPARATORS = re.compile(r"[,;\n]+")

EXCEL_COLUMNS = (
    ("Part ID", 12), ("Part", 40), ("Part type", 28), ("Brand", 16), ("Sellers", 22),
    ("Sellers' names", 50), ("Cars", 30), ("Other numbers", 24), ("Possible OEM (check)", 28),
    ("OEM code", 22),
)
_ID_HEADERS = {"part id", "product id", "id", "detal id"}
_OEM_HEADERS = {"oem code", "oem codes", "oem", "oem kodi", "oem код", "oem kod"}


def clean_number(value: str) -> str:
    number = " ".join(str(value).split()).upper()
    # Digits typed in groups ("96 273 708") are one number.
    return number.replace(" ", "") if re.fullmatch(r"[\d ]+", number) else number


def valid_oem(number: str) -> bool:
    code = normalize_code(number)
    return _MIN_LENGTH <= len(code) <= _MAX_LENGTH and sum(c.isdigit() for c in code) >= _MIN_DIGITS


def split_numbers(value: object | None) -> list[str]:
    """The codes in a cell: commas or new lines separate them, and "96267421/22/23" is the
    sellers' short form of three codes."""
    numbers = []
    for part in _SEPARATORS.split(str(value or "")):
        if part.strip():
            numbers.extend(part_numbers(part) if "/" in part else [clean_number(part)])
    return list(dict.fromkeys(numbers))


def has_oem(product: Product) -> bool:
    return any(reference.type in OEM_TYPES for reference in product.reference_numbers)


def _has_oem_clause(product_id_column):
    return exists().where(
        ReferenceNumber.product_id == product_id_column, ReferenceNumber.type.in_(OEM_TYPES)
    )


def add_oem_numbers(product: Product, numbers: list[str], note: str) -> list[str]:
    """Save numbers as checked OEM codes of the part; returns the ones it did not have.

    A number the part already carries as a seller's code or a maker's article becomes its
    OEM code: staff say what the number is.
    """
    added = []
    existing = {reference.normalized_number: reference for reference in product.reference_numbers}
    for number in numbers:
        normalized = normalize_code(number)
        reference = existing.get(normalized)
        if reference is not None and reference.type in OEM_TYPES:
            continue
        if reference is None:
            reference = ReferenceNumber(number=number, normalized_number=normalized)
            product.reference_numbers.append(reference)
            existing[normalized] = reference
        reference.type = "OE"
        reference.cross_source = "MANUAL"
        reference.confidence = "HIGH"
        reference.verified = True
        reference.notes = note
        added.append(reference.number)
    if added:
        refresh_product(product)
    return added


def _load_products(session: Session, product_ids: list[str]) -> dict[str, Product]:
    if not product_ids:
        return {}
    products = session.scalars(
        select(Product).where(Product.id.in_(product_ids)).options(*product_loading_options())
    ).all()
    return {product.id: product for product in products}


def _staff(request: Request) -> str:
    return session_user(settings, request.cookies.get(COOKIE_NAME)) or "staff"


# ---------- What staff see ----------


def coverage(session: Session) -> dict:
    searchable = Product.is_searchable.is_(True)
    total = session.scalar(select(func.count(Product.id)).where(searchable)) or 0
    with_oem = session.scalar(
        select(func.count(Product.id)).where(searchable, _has_oem_clause(Product.id))
    ) or 0
    product_has_oem = _has_oem_clause(SupplierOffer.product_id)
    rows = session.execute(
        select(
            Supplier.id,
            Supplier.name,
            func.count(func.distinct(SupplierOffer.product_id)),
            func.count(func.distinct(case((product_has_oem, SupplierOffer.product_id)))),
        )
        .join(SupplierOffer, SupplierOffer.supplier_id == Supplier.id)
        .join(Product, Product.id == SupplierOffer.product_id)
        .where(SupplierOffer.is_active.is_(True), searchable)
        .group_by(Supplier.id, Supplier.name)
        .order_by(Supplier.name)
    ).all()
    return {
        "total": total,
        "with_oem": with_oem,
        "sellers": [
            {"id": supplier_id, "name": name, "parts": parts, "with_oem": known}
            for supplier_id, name, parts, known in rows
        ],
    }


def _missing_query(supplier_id: int | None, q: str | None):
    stmt = select(Product.id).where(
        Product.is_searchable.is_(True), ~_has_oem_clause(Product.id)
    )
    if supplier_id is not None:
        stmt = stmt.where(
            Product.supplier_offers.any(
                (SupplierOffer.supplier_id == supplier_id) & SupplierOffer.is_active.is_(True)
            )
        )
    for word in normalize_text(q or "").split():
        stmt = stmt.where(Product.search_text.contains(word))
    return stmt


def _short_name(product: Product) -> str:
    return normalize_text(product.name)


def _cars(product: Product) -> list[str]:
    return list(dict.fromkeys(
        f"{fitment.vehicle.make} {fitment.vehicle.model}" for fitment in product.fitments
        if fitment.vehicle is not None
    ))


def _candidates(session: Session, products: list[Product]) -> dict[str, list[dict]]:
    """OEM codes of parts that look like the same part from another seller: same part type,
    a shared car and no conflicting position, side or size."""
    categories = {product.category_id for product in products if product.category_id}
    if not categories:
        return {}
    known = session.scalars(
        select(Product)
        .where(Product.category_id.in_(categories), Product.is_searchable.is_(True),
               _has_oem_clause(Product.id))
        .options(*product_loading_options())
    ).all()
    by_category: dict[str, list[Product]] = defaultdict(list)
    for other in known:
        by_category[other.category_id].append(other)

    found: dict[str, list[dict]] = {}
    for product in products:
        cars = {fitment.vehicle_id for fitment in product.fitments}
        if not cars:
            continue
        variant, name = product_variant(product), _short_name(product)
        scored = []
        for other in by_category.get(product.category_id, []):
            if not cars & {fitment.vehicle_id for fitment in other.fitments}:
                continue
            if not compatible_variants(variant, product_variant(other)):
                continue
            score = SequenceMatcher(None, name, _short_name(other)).ratio()
            if score < CANDIDATE_NAME_RATIO:
                continue
            score += 0.2 if other.brand_id == product.brand_id else 0
            scored.append((score, other))
        seen: set[str] = set()
        picks = []
        for _, other in sorted(scored, key=lambda pair: -pair[0]):
            for reference in other.reference_numbers:
                if reference.type in OEM_TYPES and reference.normalized_number not in seen:
                    seen.add(reference.normalized_number)
                    picks.append({
                        "number": reference.number,
                        "product_id": other.id,
                        "name": other.name,
                        "brand": other.brand.name if other.brand else None,
                    })
            if len(picks) >= MAX_CANDIDATES:
                break
        if picks:
            found[product.id] = picks[:MAX_CANDIDATES]
    return found


def _row(product: Product, suggestions: list[OemSuggestion], candidates: list[dict]) -> dict:
    offers = [offer for offer in product.supplier_offers if offer.is_active]
    return {
        "id": product.id,
        "name": product.name,
        "category": product.category.name_uz if product.category else None,
        "brand": product.brand.name if product.brand else None,
        "sellers": list(dict.fromkeys(offer.supplier.name for offer in offers if offer.supplier)),
        "seller_names": list(dict.fromkeys(raw.raw_name for raw in product.raw_supplier_products))[:3],
        "cars": _cars(product)[:6],
        "numbers": [
            {"number": reference.number, "type": reference.type}
            for reference in product.reference_numbers if reference.type not in OEM_TYPES
        ],
        "suggestions": [
            {"id": suggestion.id, "number": suggestion.number, "created_at": suggestion.created_at}
            for suggestion in suggestions
        ],
        "candidates": candidates,
    }


def missing_parts(
    session: Session, supplier_id: int | None = None, q: str | None = None,
    offset: int = 0, limit: int | None = PAGE_SIZE,
) -> dict:
    """Parts without an OEM code: ones buyers sent a code for first, then by part type so
    staff look up similar parts together."""
    ids = _missing_query(supplier_id, q).subquery()
    total = session.scalar(select(func.count()).select_from(ids)) or 0
    asked = exists().where(OemSuggestion.product_id == Product.id, OemSuggestion.status == "NEW")
    stmt = (
        select(Product.id)
        .where(Product.id.in_(select(ids.c.id)))
        .order_by(asked.desc(), Product.category_id, Product.name, Product.id)
        .offset(offset)
    )
    if limit is not None:
        stmt = stmt.limit(limit)
    page_ids = list(session.scalars(stmt))
    products = _load_products(session, page_ids)
    ordered = [products[product_id] for product_id in page_ids]
    suggestions: dict[str, list[OemSuggestion]] = defaultdict(list)
    for suggestion in session.scalars(
        select(OemSuggestion)
        .where(OemSuggestion.product_id.in_(page_ids), OemSuggestion.status == "NEW")
        .order_by(OemSuggestion.created_at)
    ):
        suggestions[suggestion.product_id].append(suggestion)
    candidates = _candidates(session, ordered)
    return {
        "total": total,
        "items": [
            _row(product, suggestions[product.id], candidates.get(product.id, []))
            for product in ordered
        ],
    }


# ---------- Excel round trip ----------


def missing_workbook(session: Session, supplier_id: int | None = None, q: str | None = None) -> bytes:
    rows = missing_parts(session, supplier_id, q, limit=None)["items"]
    book = Workbook()
    sheet = book.active
    sheet.title = "Parts without OEM"
    sheet.append([title for title, _ in EXCEL_COLUMNS])
    for cell in sheet[1]:
        cell.font = Font(bold=True)
    for index, (_, width) in enumerate(EXCEL_COLUMNS):
        sheet.column_dimensions[chr(ord("A") + index)].width = width
    sheet.freeze_panes = "B2"
    for row in rows:
        sheet.append([
            row["id"], row["name"], row["category"], row["brand"], ", ".join(row["sellers"]),
            " | ".join(row["seller_names"]), ", ".join(row["cars"]),
            ", ".join(f"{item['number']} ({item['type']})" for item in row["numbers"]),
            ", ".join(item["number"] for item in [*row["suggestions"], *row["candidates"]]),
            None,
        ])
    notes = book.create_sheet("How to fill")
    for line in (
        "Write each part's OEM code in the last column, \"OEM code\".",
        "Several codes for one part: separate them with commas.",
        (
            "\"Possible OEM (check)\" lists codes buyers sent and codes of similar parts from "
            "other sellers. Check them in a catalog before copying."
        ),
        "Leave the cell empty when the code is not known. Do not change the Part ID column.",
        "Upload the file on the OEM codes admin page (/admin/oem).",
    ):
        notes.append([line])
    notes.column_dimensions["A"].width = 110
    buffer = BytesIO()
    book.save(buffer)
    return buffer.getvalue()


def import_oem_workbook(session: Session, content: bytes, staff: str) -> dict:
    try:
        sheet = load_workbook(BytesIO(content), read_only=True, data_only=True).worksheets[0]
    except Exception as error:  # openpyxl raises many kinds for a file that is not xlsx
        raise ValueError("The file is not an Excel (.xlsx) workbook") from error
    rows = [list(row) for row in sheet.iter_rows(values_only=True)]
    id_column = oem_column = None
    for header_index, row in enumerate(rows[:5]):
        headers = [" ".join(str(value or "").lower().split()) for value in row]
        id_column = next((i for i, value in enumerate(headers) if value in _ID_HEADERS), None)
        oem_column = next((i for i, value in enumerate(headers) if value in _OEM_HEADERS), None)
        if id_column is not None and oem_column is not None:
            break
    if id_column is None or oem_column is None:
        raise ValueError('The file needs a "Part ID" column and an "OEM code" column')

    wanted: dict[str, list[str]] = defaultdict(list)
    result = {"rows": 0, "parts_updated": 0, "codes_added": 0, "already_there": 0,
              "unknown_parts": [], "invalid": []}
    for row in rows[header_index + 1:]:
        product_id = str(row[id_column] or "").strip() if id_column < len(row) else ""
        cell = row[oem_column] if oem_column < len(row) else None
        numbers = split_numbers(cell)
        if not product_id or not numbers:
            continue
        result["rows"] += 1
        for number in numbers:
            if valid_oem(number):
                wanted[product_id].append(number)
            else:
                result["invalid"].append(f"{product_id}: {number}")
    products = _load_products(session, list(wanted))
    note = f"Excel upload by {staff}"
    for product_id, numbers in wanted.items():
        product = products.get(product_id)
        if product is None:
            result["unknown_parts"].append(product_id)
            continue
        added = add_oem_numbers(product, numbers, note)
        result["codes_added"] += len(added)
        result["already_there"] += len(numbers) - len(added)
        result["parts_updated"] += bool(added)
    session.commit()
    return result


# ---------- Admin API ----------


class OemNumbersIn(BaseModel):
    numbers: list[str] = Field(min_length=1, max_length=10)


class SuggestionUpdate(BaseModel):
    status: Literal["ACCEPTED", "REJECTED"]


def _product_or_404(session: Session, product_id: str) -> Product:
    product = _load_products(session, [product_id]).get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Part not found")
    return product


def _oem_out(product: Product) -> list[dict]:
    return [
        {"number": reference.number, "manual": reference.cross_source == "MANUAL"}
        for reference in product.reference_numbers if reference.type in OEM_TYPES
    ]


@router.get("/summary")
def oem_summary(session: SessionDep) -> dict:
    return coverage(session)


@router.get("/missing")
def oem_missing(
    session: SessionDep,
    supplier_id: int | None = None,
    q: Annotated[str | None, Query(max_length=100)] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=200)] = PAGE_SIZE,
) -> dict:
    return missing_parts(session, supplier_id, q, offset, limit)


@router.get("/missing.xlsx")
def oem_missing_excel(
    session: SessionDep,
    supplier_id: int | None = None,
    q: Annotated[str | None, Query(max_length=100)] = None,
) -> Response:
    content = missing_workbook(session, supplier_id, q)
    filename = f"parts-without-oem-{datetime.now(UTC):%Y-%m-%d}.xlsx"
    return Response(
        content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/upload")
async def oem_upload(
    request: Request, session: SessionDep, file: Annotated[UploadFile, File()]
) -> dict:
    try:
        return import_oem_workbook(session, await file.read(), _staff(request))
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.post("/parts/{product_id}")
def oem_add(product_id: str, payload: OemNumbersIn, request: Request, session: SessionDep) -> dict:
    numbers = [number for value in payload.numbers for number in split_numbers(value)]
    invalid = [number for number in numbers if not valid_oem(number)]
    if invalid or not numbers:
        raise HTTPException(
            status_code=422,
            detail=f"Not an OEM code: {', '.join(invalid) or '—'} (5–30 letters/digits, 3+ digits)",
        )
    product = _product_or_404(session, product_id)
    added = add_oem_numbers(product, numbers, f"Added by {_staff(request)}")
    # Codes buyers sent for this part that staff have now saved count as accepted.
    saved = {normalize_code(number) for number in numbers}
    for suggestion in session.scalars(
        select(OemSuggestion).where(
            OemSuggestion.product_id == product.id, OemSuggestion.status == "NEW"
        )
    ):
        if suggestion.normalized_number in saved:
            suggestion.status, suggestion.reviewed_at = "ACCEPTED", datetime.now(UTC)
    session.commit()
    others = session.execute(
        select(Product.id, Product.name)
        .join(ReferenceNumber, ReferenceNumber.product_id == Product.id)
        .where(ReferenceNumber.normalized_number.in_(saved), Product.id != product.id)
        .distinct()
        .limit(5)
    ).all()
    return {
        "added": added,
        "oem": _oem_out(product),
        "also_on": [{"id": other_id, "name": name} for other_id, name in others],
    }


@router.delete("/parts/{product_id}/{number:path}")
def oem_remove(product_id: str, number: str, session: SessionDep) -> dict:
    """Undo a code staff typed in; codes from sellers' lists are fixed in the catalog editor."""
    product = _product_or_404(session, product_id)
    normalized = normalize_code(number)
    reference = next(
        (reference for reference in product.reference_numbers
         if reference.normalized_number == normalized and reference.type in OEM_TYPES
         and reference.cross_source == "MANUAL"),
        None,
    )
    if reference is None:
        raise HTTPException(status_code=404, detail="No OEM code typed in by staff with that number")
    product.reference_numbers.remove(reference)
    session.flush()
    refresh_product(product)
    session.commit()
    return {"oem": _oem_out(product)}


@router.get("/suggestions")
def oem_suggestions(session: SessionDep, status: str = "NEW") -> list[dict]:
    suggestions = session.scalars(
        select(OemSuggestion)
        .where(OemSuggestion.status == status)
        .order_by(OemSuggestion.created_at.desc())
        .limit(200)
    ).all()
    products = _load_products(session, list({suggestion.product_id for suggestion in suggestions}))
    return [
        {
            "id": suggestion.id,
            "number": suggestion.number,
            "status": suggestion.status,
            "created_at": suggestion.created_at,
            "product_id": suggestion.product_id,
            "product_name": products[suggestion.product_id].name,
            "oem": _oem_out(products[suggestion.product_id]),
        }
        for suggestion in suggestions
        if suggestion.product_id in products
    ]


@router.patch("/suggestions/{suggestion_id}")
def oem_review_suggestion(
    suggestion_id: int, payload: SuggestionUpdate, request: Request, session: SessionDep
) -> dict:
    suggestion = session.get(OemSuggestion, suggestion_id)
    if suggestion is None:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    if payload.status == "ACCEPTED":
        product = _product_or_404(session, suggestion.product_id)
        add_oem_numbers(product, [suggestion.number], f"Sent by a buyer, checked by {_staff(request)}")
    suggestion.status, suggestion.reviewed_at = payload.status, datetime.now(UTC)
    session.commit()
    return {"id": suggestion.id, "status": suggestion.status}


# ---------- Buyers and mechanics ----------


class OemSuggestionCreate(BaseModel):
    number: str = Field(min_length=1, max_length=60)
    session_id: str = Field(min_length=8, max_length=100)


@public_router.post("/products/{product_id}/oem-suggestions", status_code=201)
def suggest_oem(product_id: str, payload: OemSuggestionCreate, session: SessionDep) -> dict:
    number = clean_number(payload.number)
    if not valid_oem(number):
        raise HTTPException(status_code=422, detail="Not an OEM code")
    product = session.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Part not found")
    normalized = normalize_code(number)
    repeated = session.scalar(
        select(OemSuggestion).where(
            OemSuggestion.product_id == product_id,
            OemSuggestion.session_id == payload.session_id,
            OemSuggestion.normalized_number == normalized,
        )
    )
    if repeated is None:
        session.add(OemSuggestion(
            session_id=payload.session_id, product_id=product_id, number=number,
            normalized_number=normalized, status="NEW",
        ))
        session.commit()
    return {"status": "RECEIVED"}
