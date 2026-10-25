from collections import Counter
from datetime import UTC, date, datetime
from pathlib import Path
from time import perf_counter
from typing import Annotated, Literal
from urllib.parse import quote
from uuid import uuid4

from fastapi import (
    Depends,
    FastAPI,
    File,
    Header,
    HTTPException,
    Query,
    Request,
    Response,
    UploadFile,
)
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import func, select, text
from sqlalchemy.orm import Session, selectinload

from app.analytics import build_analytics
from app.auth import (
    COOKIE_NAME,
    LoginThrottle,
    credentials_match,
    is_admin_path,
    issue_session,
    session_user,
)
from app.catalog_admin import router as catalog_admin_router
from app.config import get_settings
from app.database import get_session
from app.models import (
    Brand,
    Category,
    Fitment,
    FitReport,
    OfferImportReview,
    PartRequest,
    PilotFeedback,
    Product,
    ReservationRequest,
    SearchAlias,
    SearchEvent,
    SearchEventAction,
    SellerApplication,
    Supplier,
    SupplierImport,
    SupplierOffer,
    Vehicle,
)
from app.normalization import normalize_text, sanitize_query
from app.offers import active_sorted_offers, freshness_status, supplier_summary
from app.part_types import category_with_descendants, part_groups
from app.price_list_import import import_price_list
from app.product_context import fit_report_summary
from app.query_parser import parse_query
from app.reservations import admin_reservation_out, my_reservation_out, recompute_reliability
from app.schemas import (
    AdminFitReportOut,
    AdminLogin,
    AdminReservationOut,
    BasketCreate,
    BasketOfferOut,
    BasketOut,
    FitReportCreate,
    FitReportSummary,
    JobOut,
    MyReservationOut,
    PartGroupOut,
    PartRequestCreate,
    PartRequestOut,
    PartRequestUpdate,
    PartTypeOut,
    PilotFeedbackCreate,
    PilotFeedbackOut,
    PriceListImportOut,
    ProductDetail,
    ReservationCancel,
    ReservationCreate,
    ReservationOut,
    ReservationUpdate,
    SearchActionCreate,
    SearchAliasCreate,
    SearchAliasOut,
    SearchAliasTargetsOut,
    SearchClickCreate,
    SearchEventCreate,
    SearchEventOut,
    SearchResponse,
    SellerApplicationCreate,
    SellerApplicationOut,
    SellerApplicationUpdate,
    SellerCardOut,
    SuggestedProductOut,
    SuggestResponse,
    SupplierAdminOut,
    SupplierCreate,
    SupplierDetailOut,
    SupplierImportOut,
    SupplierProductOut,
    SupplierUpdate,
    VehicleOptionOut,
)
from app.search import get_product_detail, product_search_out, search_products
from app.search_vocabulary import PRODUCT_SYNONYMS, VEHICLE_ALIASES
from app.seo import part_page, robots, sitemap
from app.shop import basket_offers, create_basket, job_lists, sellers_directory
from app.supplier_import import import_supplier_workbook

settings = get_settings()
app = FastAPI(title="MegaParts Catalog API", version="0.2.0")
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")
login_throttle = LoginThrottle()
app.include_router(catalog_admin_router)


@app.middleware("http")
async def require_admin_login(request: Request, call_next):
    """Gate every /admin page and /api/admin endpoint, including ones added later."""
    if is_admin_path(request.url.path) and not session_user(
        settings, request.cookies.get(COOKIE_NAME)
    ):
        if request.url.path.startswith("/api/"):
            return JSONResponse({"detail": "Login required"}, status_code=401)
        return RedirectResponse(
            f"/admin/login?next={quote(request.url.path)}", status_code=303
        )
    return await call_next(request)


def admin_home() -> str:
    return "/admin/catalog"


@app.get("/admin/catalog", include_in_schema=False)
def catalog_profile_page() -> FileResponse:
    return FileResponse(static_dir / "catalog.html")


@app.get("/admin/login", include_in_schema=False, response_model=None)
def admin_login_page(request: Request) -> FileResponse | RedirectResponse:
    if session_user(settings, request.cookies.get(COOKIE_NAME)):
        return RedirectResponse(admin_home(), status_code=303)
    return FileResponse(static_dir / "login.html")


@app.get("/admin", include_in_schema=False)
def admin_index() -> RedirectResponse:
    return RedirectResponse(admin_home(), status_code=303)


@app.post("/api/admin/login")
def admin_login(payload: AdminLogin, request: Request, response: Response) -> dict[str, str]:
    if not settings.admin_password:
        raise HTTPException(
            status_code=503, detail="Admin login is not configured. Set ADMIN_PASSWORD in .env."
        )
    client = request.client.host if request.client else "unknown"
    retry_after = login_throttle.retry_after(client)
    if retry_after:
        raise HTTPException(
            status_code=429,
            detail=f"Too many failed attempts. Try again in {(retry_after + 59) // 60} min.",
            headers={"Retry-After": str(retry_after)},
        )
    if not credentials_match(settings, payload.username, payload.password):
        login_throttle.fail(client)
        raise HTTPException(status_code=401, detail="Wrong username or password")
    login_throttle.reset(client)
    response.set_cookie(
        COOKIE_NAME,
        issue_session(settings),
        max_age=int(settings.admin_session_hours * 3600),
        httponly=True,
        samesite="lax",
        secure=settings.secure_cookies,
        path="/",
    )
    return {"username": settings.admin_username, "next": admin_home()}


@app.post("/api/admin/logout", status_code=204)
def admin_logout(response: Response) -> None:
    response.delete_cookie(
        COOKIE_NAME, path="/", httponly=True, samesite="lax", secure=settings.secure_cookies
    )


@app.get("/api/admin/me")
def admin_me(request: Request) -> dict[str, str]:
    return {"username": session_user(settings, request.cookies.get(COOKIE_NAME)) or ""}


def require_pilot_mode() -> None:
    if not settings.pilot_mode:
        raise HTTPException(status_code=404, detail="Pilot mode is disabled")


def find_event(session: Session, event_id: int) -> SearchEvent:
    event = session.get(SearchEvent, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Search event not found")
    return event


@app.get("/", include_in_schema=False)
def catalog_page() -> FileResponse:
    return FileResponse(static_dir / "index.html")


@app.get("/health")
def health(session: Annotated[Session, Depends(get_session)]) -> dict[str, str]:
    session.execute(text("SELECT 1"))
    return {"status": "ok"}


@app.get(
    f"{settings.api_prefix}/search",
    response_model=SearchResponse,
    response_model_exclude_none=True,
)
def search(
    session: Annotated[Session, Depends(get_session)],
    q: Annotated[str, Query(max_length=200)] = "",
    make: Annotated[str | None, Query(max_length=150)] = None,
    model: Annotated[str | None, Query(max_length=300)] = None,
    vehicle_id: Annotated[str | None, Query(max_length=64)] = None,
    category: Annotated[str | None, Query(max_length=64)] = None,
    brand: int | None = None,
    quality: Literal["ORIGINAL", "KOREA", "CHINA", "BUDGET", "OTHER"] | None = None,
    sort: Literal["relevance", "price"] = "relevance",
    spellcheck: bool = True,
    session_id: Annotated[str | None, Query(max_length=100)] = None,
    x_session_id: Annotated[str | None, Header(max_length=100)] = None,
    x_user_id: Annotated[str | None, Header(max_length=100)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> SearchResponse:
    vehicle_ids, vehicle_label = resolve_vehicle_filter(session, make, model, vehicle_id)
    category_row, category_ids = resolve_category_filter(session, category)
    if not q.strip() and not vehicle_ids and not category_ids:
        raise HTTPException(
            status_code=422, detail="Provide a search query, a vehicle, or a part category"
        )
    started = perf_counter()
    response = search_products(
        session,
        q,
        limit=limit,
        offset=offset,
        include_debug=settings.search_debug,
        vehicle_ids=vehicle_ids,
        vehicle_label=vehicle_label,
        spellcheck=spellcheck,
        category=category_row,
        category_ids=category_ids,
        brand_id=brand,
        quality=quality,
        sort=sort,
    )
    elapsed_ms = (perf_counter() - started) * 1000
    if settings.pilot_mode:
        parsed = response.parsed_query_internal
        # Analytics keep what the customer typed, not the spelling correction.
        typed = normalize_text(sanitize_query(q))
        browsed = [vehicle_label if response.vehicle_filter else None]
        browsed.append(category_row.name_uz if category_row else None)
        browse_label = f"[{' · '.join(filter(None, browsed))}]" if any(browsed) else ""
        event = SearchEvent(
            user_id=x_user_id,
            session_id=session_id or x_session_id or str(uuid4()),
            query_raw=" ".join(filter(None, [q.strip(), browse_label])),
            query_normalized=" ".join(filter(None, [typed, browse_label.casefold()])),
            result_count=response.total,
            search_time_ms=elapsed_ms,
            top_product_ids=[item.id for item in response.items[:5]],
            action="search",
            detected_vehicle=parsed.get("vehicle")
            or (vehicle_label if response.vehicle_filter else None),
            detected_product_terms=parsed.get("product_terms", []),
            detected_reference=parsed.get("reference"),
            detected_brand=parsed.get("brand"),
            detected_position=parsed.get("position"),
            detected_side=parsed.get("side"),
            result_group_distribution=response.result_group_distribution_internal,
            top_result_score=response.items[0].relevance_score if response.items else None,
        )
        session.add(event)
        session.commit()
        response.search_event_id = event.id
    return response


def resolve_vehicle_filter(
    session: Session, make: str | None, model: str | None, vehicle_id: str | None
) -> tuple[set[str] | None, str | None]:
    if vehicle_id:
        vehicle = session.get(Vehicle, vehicle_id)
        if vehicle is None:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        label = " ".join(filter(None, [vehicle.make, vehicle.model, vehicle.generation]))
        return {vehicle.id}, label
    if not make:
        return None, None
    stmt = select(Vehicle.id).where(Vehicle.make == make)
    if model:
        stmt = stmt.where(Vehicle.model == model)
    ids = set(session.scalars(stmt).all())
    if not ids:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return ids, " ".join(filter(None, [make, model]))


def resolve_category_filter(
    session: Session, category_id: str | None
) -> tuple[Category | None, set[str] | None]:
    """A part group or part type, with every category below it."""
    if not category_id:
        return None, None
    category = session.get(Category, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Part category not found")
    return category, category_with_descendants(session, category_id)


SUGGESTED_PART_TYPES = 4
SUGGESTED_PRODUCTS = 4


@app.get(
    f"{settings.api_prefix}/suggest",
    response_model=SuggestResponse,
    response_model_exclude_none=True,
)
def suggest(
    session: Annotated[Session, Depends(get_session)],
    q: Annotated[str, Query(max_length=200)] = "",
    make: Annotated[str | None, Query(max_length=150)] = None,
    model: Annotated[str | None, Query(max_length=300)] = None,
    vehicle_id: Annotated[str | None, Query(max_length=64)] = None,
) -> SuggestResponse:
    """Type-ahead for the search box: the spelling fix, matching part types, and top parts.

    Keystrokes are not searches, so nothing is recorded in pilot analytics.
    """
    if len(q.strip()) < 2:
        return SuggestResponse(query=q)
    vehicle_ids, _ = resolve_vehicle_filter(session, make, model, vehicle_id)
    response = search_products(session, q, limit=100, vehicle_ids=vehicle_ids)
    # Loose fuzzy guesses are fine on a results page but would be noise in a short list.
    strong = [item for item in response.items if item.result_group != "RELATED"]
    categories = {item.category.id: item.category for item in strong if item.category}
    type_counts = Counter(item.category.id for item in strong if item.category)
    products = list({(item.name, item.brand and item.brand.id): item for item in strong}.values())
    return SuggestResponse(
        query=q,
        corrected_query=response.corrected_query,
        part_types=[
            PartTypeOut(**categories[category_id].model_dump(), part_count=count)
            for category_id, count in type_counts.most_common(SUGGESTED_PART_TYPES)
        ],
        products=[
            SuggestedProductOut(
                id=item.id,
                name=item.name,
                name_ru=item.name_ru,
                name_en=item.name_en,
                brand=item.brand,
                category=item.category,
            )
            for item in products[:SUGGESTED_PRODUCTS]
        ],
    )


@app.get(f"{settings.api_prefix}/part-groups", response_model=list[PartGroupOut])
def list_part_groups(
    session: Annotated[Session, Depends(get_session)],
    make: Annotated[str | None, Query(max_length=150)] = None,
    model: Annotated[str | None, Query(max_length=300)] = None,
    vehicle_id: Annotated[str | None, Query(max_length=64)] = None,
) -> list[dict]:
    """Part groups and types for the browse filters, counted for the chosen car if any."""
    vehicle_ids, _ = resolve_vehicle_filter(session, make, model, vehicle_id)
    return part_groups(session, vehicle_ids)


@app.get(f"{settings.api_prefix}/vehicles", response_model=list[VehicleOptionOut])
def vehicles(session: Annotated[Session, Depends(get_session)]) -> list[VehicleOptionOut]:
    """Vehicles with at least one searchable fitted part, for the "my car" picker."""
    part_count = func.count(func.distinct(Product.id))
    rows = session.execute(
        select(Vehicle, part_count)
        .join(Fitment, Fitment.vehicle_id == Vehicle.id)
        .join(Product, Product.id == Fitment.product_id)
        .where(Product.is_searchable.is_(True))
        # "(model aniqlanmagan)" rows are importer placeholders, not choosable cars.
        .where(Vehicle.model.not_like("(%"))
        .group_by(Vehicle.id)
        .order_by(Vehicle.make, Vehicle.model, Vehicle.generation)
    ).all()
    return [
        VehicleOptionOut(
            id=vehicle.id,
            make=vehicle.make,
            model=vehicle.model,
            generation=vehicle.generation,
            part_count=count,
        )
        for vehicle, count in rows
    ]


@app.get(f"{settings.api_prefix}/products/{{product_id}}", response_model=ProductDetail)
def product_detail(
    product_id: str,
    session: Annotated[Session, Depends(get_session)],
    make: Annotated[str | None, Query(max_length=150)] = None,
    model: Annotated[str | None, Query(max_length=300)] = None,
    vehicle_id: Annotated[str | None, Query(max_length=64)] = None,
) -> ProductDetail:
    """The part; alternatives and job parts are chosen for the buyer's car when given."""
    vehicle_ids, _ = resolve_vehicle_filter(session, make, model, vehicle_id)
    product = get_product_detail(session, product_id, vehicle_ids)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post(
    f"{settings.api_prefix}/products/{{product_id}}/fit-reports",
    status_code=201,
    response_model=list[FitReportSummary],
)
def report_fit(
    product_id: str,
    payload: FitReportCreate,
    session: Annotated[Session, Depends(get_session)],
) -> list[FitReportSummary]:
    """A buyer says whether the part fitted their car; repeated 'no' flags bad fitment data."""
    if session.get(Product, product_id) is None:
        raise HTTPException(status_code=404, detail="Product not found")
    vehicle_id = payload.vehicle_id if session.get(Vehicle, payload.vehicle_id or "") else None
    session.add(
        FitReport(
            session_id=payload.session_id,
            product_id=product_id,
            vehicle_id=vehicle_id,
            vehicle_label=payload.vehicle_label,
            fits=payload.fits,
        )
    )
    session.commit()
    return fit_report_summary(session, product_id)


@app.post(
    f"{settings.api_prefix}/part-requests", response_model=PartRequestOut, status_code=201
)
def create_part_request(
    payload: PartRequestCreate,
    session: Annotated[Session, Depends(get_session)],
) -> PartRequest:
    """A part the buyer could not find, handed to staff and suppliers instead of a dead end."""
    data = payload.model_dump()
    if not session.get(Vehicle, data["vehicle_id"] or ""):
        data["vehicle_id"] = None
    request = PartRequest(**data)
    session.add(request)
    session.commit()
    session.refresh(request)
    return request


@app.get("/api/pilot-config")
def pilot_config() -> dict[str, bool]:
    return {"pilot_mode": settings.pilot_mode}


@app.post("/api/search-events", response_model=SearchEventOut, status_code=201)
def create_search_event(
    payload: SearchEventCreate,
    session: Annotated[Session, Depends(get_session)],
) -> SearchEvent:
    require_pilot_mode()
    parsed = parse_query(payload.query_raw, list(session.scalars(select(Brand.name)).all()))
    parsed_fields = parsed.public_dict()
    event = SearchEvent(
        **payload.model_dump(exclude={"query_normalized"}),
        query_normalized=payload.query_normalized or normalize_text(payload.query_raw),
        action="search",
        detected_vehicle=parsed_fields.get("vehicle"),
        detected_product_terms=parsed_fields.get("product_terms", []),
        detected_reference=parsed_fields.get("reference"),
        detected_brand=parsed_fields.get("brand"),
        detected_position=parsed_fields.get("position"),
        detected_side=parsed_fields.get("side"),
        result_group_distribution={},
        top_result_score=None,
    )
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@app.post("/api/search-events/{event_id}/click", response_model=SearchEventOut)
def record_search_click(
    event_id: int,
    payload: SearchClickCreate,
    session: Annotated[Session, Depends(get_session)],
) -> SearchEvent:
    require_pilot_mode()
    if (payload.product_id is None) == (payload.supplier_id is None):
        raise HTTPException(status_code=422, detail="Provide exactly one product_id or supplier_id")
    event = find_event(session, event_id)
    if payload.product_id is not None:
        if session.get(Product, payload.product_id) is None:
            raise HTTPException(status_code=404, detail="Product not found")
        event.clicked_product_id = payload.product_id
        event.action = "product_click"
    else:
        if session.get(Supplier, payload.supplier_id) is None:
            raise HTTPException(status_code=404, detail="Supplier not found")
        event.clicked_supplier_id = payload.supplier_id
        event.action = "supplier_click"
    session.add(
        SearchEventAction(
            search_event_id=event.id,
            action=event.action,
            product_id=payload.product_id,
            supplier_id=payload.supplier_id,
        )
    )
    session.commit()
    session.refresh(event)
    return event


@app.post("/api/search-events/{event_id}/action", response_model=SearchEventOut)
def record_search_action(
    event_id: int,
    payload: SearchActionCreate,
    session: Annotated[Session, Depends(get_session)],
) -> SearchEvent:
    require_pilot_mode()
    event = find_event(session, event_id)
    if payload.product_id is not None:
        if session.get(Product, payload.product_id) is None:
            raise HTTPException(status_code=404, detail="Product not found")
        event.clicked_product_id = payload.product_id
    if payload.supplier_id is not None:
        if session.get(Supplier, payload.supplier_id) is None:
            raise HTTPException(status_code=404, detail="Supplier not found")
        event.clicked_supplier_id = payload.supplier_id
    if payload.supplier_offer_id is not None:
        offer = session.get(SupplierOffer, payload.supplier_offer_id)
        if offer is None:
            raise HTTPException(status_code=404, detail="Supplier offer not found")
        if payload.product_id is not None and payload.product_id != offer.product_id:
            raise HTTPException(status_code=422, detail="Offer does not belong to product")
        if payload.supplier_id is not None and payload.supplier_id != offer.supplier_id:
            raise HTTPException(status_code=422, detail="Offer does not belong to supplier")
        if payload.product_id is None:
            event.clicked_product_id = offer.product_id
        if payload.supplier_id is None:
            event.clicked_supplier_id = offer.supplier_id
    event.action = payload.action
    session.add(
        SearchEventAction(
            search_event_id=event.id,
            action=payload.action,
            product_id=payload.product_id or (offer.product_id if payload.supplier_offer_id else None),
            supplier_id=payload.supplier_id
            or (offer.supplier_id if payload.supplier_offer_id else None),
            supplier_offer_id=payload.supplier_offer_id,
        )
    )
    session.commit()
    session.refresh(event)
    return event


@app.post("/api/search-events/{event_id}/feedback", response_model=PilotFeedbackOut)
def record_pilot_feedback(
    event_id: int,
    payload: PilotFeedbackCreate,
    session: Annotated[Session, Depends(get_session)],
) -> PilotFeedback:
    require_pilot_mode()
    event = find_event(session, event_id)
    feedback = event.feedback
    if feedback is None:
        feedback = PilotFeedback(search_event_id=event.id, **payload.model_dump())
        session.add(feedback)
    else:
        for key, value in payload.model_dump().items():
            setattr(feedback, key, value)
    session.commit()
    session.refresh(feedback)
    return feedback


@app.get("/api/admin/search-analytics")
def search_analytics(
    session: Annotated[Session, Depends(get_session)],
    period: Annotated[str, Query(pattern="^(today|7d|30d|custom)$")] = "7d",
    date_from: Annotated[date | None, Query()] = None,
    date_to: Annotated[date | None, Query()] = None,
) -> dict:
    require_pilot_mode()
    return build_analytics(session, period, date_from, date_to)


@app.get("/admin/search-analytics", include_in_schema=False)
def search_analytics_page() -> FileResponse:
    require_pilot_mode()
    return FileResponse(static_dir / "admin.html")


@app.post(f"{settings.api_prefix}/reservations", response_model=ReservationOut, status_code=201)
def create_reservation(
    payload: ReservationCreate,
    session: Annotated[Session, Depends(get_session)],
) -> ReservationRequest:
    offer = session.scalar(
        select(SupplierOffer).where(
            SupplierOffer.id == payload.supplier_offer_id,
            SupplierOffer.product_id == payload.product_id,
            SupplierOffer.is_active.is_(True),
        )
    )
    if offer is None:
        raise HTTPException(status_code=404, detail="Active offer not found for this product")
    if payload.search_event_id is not None:
        find_event(session, payload.search_event_id)
    data = payload.model_dump()
    if not session.get(Vehicle, data["vehicle_id"] or ""):
        data["vehicle_id"] = None
    reservation = ReservationRequest(**data, updated_at=datetime.now(UTC))
    session.add(reservation)
    session.flush()
    if settings.pilot_mode and payload.search_event_id is not None:
        session.add(
            SearchEventAction(
                search_event_id=payload.search_event_id,
                action="reservation_request",
                product_id=payload.product_id,
                supplier_id=offer.supplier_id,
                supplier_offer_id=offer.id,
            )
        )
    session.commit()
    session.refresh(reservation)
    return reservation


@app.get(f"{settings.api_prefix}/reservations", response_model=list[MyReservationOut])
def my_reservations(
    session: Annotated[Session, Depends(get_session)],
    session_id: Annotated[str, Query(min_length=8, max_length=100)],
) -> list[MyReservationOut]:
    """This browser's reservations with their current status, newest first."""
    reservations = session.scalars(
        select(ReservationRequest)
        .where(ReservationRequest.session_id == session_id)
        .options(
            selectinload(ReservationRequest.product).selectinload(Product.reference_numbers),
            selectinload(ReservationRequest.supplier_offer).selectinload(SupplierOffer.supplier),
        )
        .order_by(ReservationRequest.created_at.desc(), ReservationRequest.id.desc())
        .limit(50)
    ).all()
    return [my_reservation_out(reservation) for reservation in reservations]



@app.get(f"{settings.api_prefix}/jobs", response_model=list[JobOut])
def repair_lists(
    session: Annotated[Session, Depends(get_session)],
    make: Annotated[str | None, Query(max_length=150)] = None,
    model: Annotated[str | None, Query(max_length=300)] = None,
    vehicle_id: Annotated[str | None, Query(max_length=64)] = None,
) -> list[JobOut]:
    """Ready repair lists ("front brakes") with the part to pick at each step for the car."""
    vehicle_ids, _ = resolve_vehicle_filter(session, make, model, vehicle_id)
    return job_lists(session, vehicle_ids, product_search_out)


@app.get(f"{settings.api_prefix}/offers", response_model=list[BasketOfferOut])
def offers_for_basket(
    session: Annotated[Session, Depends(get_session)],
    ids: Annotated[str, Query(max_length=600, pattern=r"^\d+(,\d+)*$")],
) -> list[BasketOfferOut]:
    return basket_offers(session, [int(value) for value in ids.split(",")][:60])


@app.post(f"{settings.api_prefix}/reservations/basket", response_model=BasketOut, status_code=201)
def reserve_basket(
    payload: BasketCreate,
    session: Annotated[Session, Depends(get_session)],
) -> BasketOut:
    """Reserve every part in the basket at once; each seller gets their own reservations."""
    return create_basket(session, payload)


@app.get(f"{settings.api_prefix}/sellers", response_model=list[SellerCardOut])
def sellers(session: Annotated[Session, Depends(get_session)]) -> list[SellerCardOut]:
    return sellers_directory(session)


@app.post(
    f"{settings.api_prefix}/seller-applications",
    response_model=SellerApplicationOut,
    status_code=201,
)
def apply_to_sell(
    payload: SellerApplicationCreate,
    session: Annotated[Session, Depends(get_session)],
) -> SellerApplication:
    """A shop asking to sell on MegaParts; the team calls them back."""
    application = SellerApplication(**payload.model_dump())
    session.add(application)
    session.commit()
    session.refresh(application)
    return application

# A buyer can cancel until the part is collected; the seller's reliability is not affected.
OPEN_RESERVATION_STATUSES = ("REQUESTED", "CONFIRMED", "READY")


def _cancel_reservations(
    session: Session, session_id: str, *conditions
) -> list[MyReservationOut]:
    reservations = session.scalars(
        select(ReservationRequest)
        .where(ReservationRequest.session_id == session_id, *conditions)
        .options(
            selectinload(ReservationRequest.product).selectinload(Product.reference_numbers),
            selectinload(ReservationRequest.supplier_offer).selectinload(SupplierOffer.supplier),
        )
        .order_by(ReservationRequest.id)
    ).all()
    if not reservations:
        raise HTTPException(status_code=404, detail="Reservation not found")
    now = datetime.now(UTC)
    for reservation in reservations:
        if reservation.status in OPEN_RESERVATION_STATUSES:
            reservation.status = "CANCELLED"
            reservation.updated_at = now
    session.commit()
    return [my_reservation_out(reservation) for reservation in reservations]


@app.post(
    f"{settings.api_prefix}/reservations/{{reservation_id}}/cancel",
    response_model=MyReservationOut,
)
def cancel_reservation(
    reservation_id: int,
    payload: ReservationCancel,
    session: Annotated[Session, Depends(get_session)],
) -> MyReservationOut:
    """The buyer cancels one reservation made from this browser."""
    return _cancel_reservations(
        session, payload.session_id, ReservationRequest.id == reservation_id
    )[0]


@app.post(
    f"{settings.api_prefix}/reservations/basket/{{basket_id}}/cancel",
    response_model=list[MyReservationOut],
)
def cancel_basket(
    basket_id: str,
    payload: ReservationCancel,
    session: Annotated[Session, Depends(get_session)],
) -> list[MyReservationOut]:
    """The buyer cancels every open reservation sent from one basket."""
    return _cancel_reservations(session, payload.session_id, ReservationRequest.basket_id == basket_id)


@app.get(f"{settings.api_prefix}/suppliers/{{supplier_id}}", response_model=SupplierDetailOut)
def supplier_detail(
    supplier_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> SupplierDetailOut:
    supplier = session.scalar(
        select(Supplier)
        .where(Supplier.id == supplier_id, Supplier.is_active.is_(True))
        .options(
            selectinload(Supplier.offers)
            .selectinload(SupplierOffer.product)
            .selectinload(Product.brand)
        )
    )
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    offers = active_sorted_offers(supplier.offers)
    return SupplierDetailOut(
        id=supplier.id,
        name=supplier.name,
        phone=supplier.phone,
        telegram=supplier.telegram,
        address=supplier.address,
        trust=supplier_summary(supplier),
        brands=sorted({offer.product.brand.name for offer in offers if offer.product.brand}),
        active_offers_count=len(offers),
        last_data_update=max(
            (offer.updated_at for offer in offers if offer.updated_at), default=None
        ),
        products=[
            SupplierProductOut(
                id=offer.product.id,
                name=offer.product.name,
                name_ru=offer.product.name_ru,
                name_en=offer.product.name_en,
                brand=offer.product.brand.name if offer.product.brand else None,
                supplier_sku=offer.supplier_sku,
                price=offer.price,
                currency=offer.currency,
                stock_qty=offer.stock_qty,
                warehouse=offer.warehouse,
                updated_at=offer.updated_at,
                freshness_status=freshness_status(offer.updated_at),
                data_status=offer.data_status,
            )
            for offer in offers
        ],
    )


def supplier_admin_out(supplier: Supplier) -> SupplierAdminOut:
    return SupplierAdminOut(
        id=supplier.id,
        name=supplier.name,
        phone=supplier.phone,
        telegram=supplier.telegram,
        address=supplier.address,
        is_active=supplier.is_active,
        created_at=supplier.created_at,
        active_offers_count=sum(offer.is_active for offer in supplier.offers),
        latest_data_update=max(
            (offer.updated_at for offer in supplier.offers if offer.is_active and offer.updated_at),
            default=None,
        ),
        city=supplier.city,
        legal_name=supplier.legal_name,
        inn=supplier.inn,
        licence_number=supplier.licence_number,
        work_hours=supplier.work_hours,
        map_url=supplier.map_url,
        verified_at=supplier.verified_at,
        reliability_score=supplier.reliability_score,
        reliability_sample=supplier.reliability_sample or 0,
    )


@app.get("/api/admin/suppliers", response_model=list[SupplierAdminOut])
def admin_suppliers(
    session: Annotated[Session, Depends(get_session)],
) -> list[SupplierAdminOut]:
    suppliers = session.scalars(
        select(Supplier).options(selectinload(Supplier.offers)).order_by(Supplier.name)
    ).all()
    return [supplier_admin_out(supplier) for supplier in suppliers]


@app.patch("/api/admin/suppliers/{supplier_id}", response_model=SupplierAdminOut)
def update_supplier(
    supplier_id: int,
    payload: SupplierUpdate,
    session: Annotated[Session, Depends(get_session)],
) -> SupplierAdminOut:
    supplier = session.scalar(
        select(Supplier).where(Supplier.id == supplier_id).options(selectinload(Supplier.offers))
    )
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    changes = payload.model_dump(exclude_unset=True)
    verified = changes.pop("verified", None)
    if changes.get("name"):
        changes["name"] = changes["name"].strip()
        normalized = normalize_text(changes["name"])
        taken = session.scalar(
            select(Supplier.id).where(
                Supplier.normalized_name == normalized, Supplier.id != supplier.id
            )
        )
        if taken:
            raise HTTPException(status_code=409, detail="A supplier with this name already exists")
        supplier.normalized_name = normalized
    elif "name" in changes:
        changes.pop("name")
    for key, value in changes.items():
        setattr(supplier, key, value)
    if verified is not None:
        # Keep the original check date when the box is simply saved again.
        if not verified:
            supplier.verified_at = None
        elif supplier.verified_at is None:
            if not (supplier.legal_name and supplier.inn):
                session.rollback()
                raise HTTPException(
                    status_code=422,
                    detail="Enter the legal name and INN before marking a supplier verified",
                )
            supplier.verified_at = datetime.now(UTC)
    session.commit()
    session.refresh(supplier)
    return supplier_admin_out(supplier)


@app.post("/api/admin/suppliers/{supplier_id}/offers/import", response_model=SupplierImportOut)
def import_supplier_offers(
    supplier_id: int,
    file: Annotated[UploadFile, File()],
    session: Annotated[Session, Depends(get_session)],
) -> SupplierImportOut:
    supplier = session.get(Supplier, supplier_id)
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    try:
        batch = import_supplier_workbook(session, supplier, file.file.read(), file.filename)
        session.commit()
        session.refresh(batch)
    except ValueError as exc:
        session.rollback()
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return SupplierImportOut(
        **{
            column: getattr(batch, column)
            for column in SupplierImportOut.model_fields
            if column != "supplier_name"
        },
        supplier_name=supplier.name,
    )


@app.post("/api/admin/suppliers", response_model=SupplierAdminOut, status_code=201)
def create_supplier(
    payload: SupplierCreate,
    session: Annotated[Session, Depends(get_session)],
) -> SupplierAdminOut:
    normalized = normalize_text(payload.name)
    if session.scalar(select(Supplier.id).where(Supplier.normalized_name == normalized)):
        raise HTTPException(status_code=409, detail="A supplier with this name already exists")
    supplier = Supplier(
        name=payload.name.strip(),
        normalized_name=normalized,
        phone=payload.phone,
        telegram=payload.telegram,
        city=payload.city,
        is_active=True,
    )
    session.add(supplier)
    session.commit()
    supplier = session.scalar(
        select(Supplier).where(Supplier.id == supplier.id).options(selectinload(Supplier.offers))
    )
    return supplier_admin_out(supplier)


@app.post("/api/admin/suppliers/{supplier_id}/price-list", response_model=PriceListImportOut)
def import_supplier_price_list(
    supplier_id: int,
    file: Annotated[UploadFile, File()],
    session: Annotated[Session, Depends(get_session)],
) -> PriceListImportOut:
    """A seller's own Excel list, in any layout: its parts join the catalog with their offers."""
    supplier = session.get(Supplier, supplier_id)
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    try:
        result = import_price_list(session, supplier, file.file.read(), file.filename)
        session.commit()
    except ValueError as exc:
        session.rollback()
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return PriceListImportOut(
        import_id=result.batch.id,
        supplier_id=supplier.id,
        rows=result.batch.rows_received,
        parts_created=result.products_created,
        parts_reused=result.products_reused,
        offers_created=result.offers_created,
        offers_updated=result.offers_updated,
        offers_closed=result.offers_closed,
        rows_without_car=result.without_car,
        cars_created=result.vehicles_created,
        unrecognised=sorted(set(result.unrecognised))[:100],
    )


@app.get("/api/admin/seller-applications", response_model=list[SellerApplicationOut])
def seller_applications(
    session: Annotated[Session, Depends(get_session)],
) -> list[SellerApplication]:
    return list(
        session.scalars(
            select(SellerApplication).order_by(SellerApplication.created_at.desc()).limit(200)
        )
    )


@app.patch(
    "/api/admin/seller-applications/{application_id}", response_model=SellerApplicationOut
)
def update_seller_application(
    application_id: int,
    payload: SellerApplicationUpdate,
    session: Annotated[Session, Depends(get_session)],
) -> SellerApplication:
    application = session.get(SellerApplication, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    application.status = payload.status
    session.commit()
    session.refresh(application)
    return application


@app.get("/api/admin/supplier-imports", response_model=list[SupplierImportOut])
def supplier_imports(
    session: Annotated[Session, Depends(get_session)],
) -> list[SupplierImportOut]:
    imports = session.scalars(
        select(SupplierImport)
        .options(selectinload(SupplierImport.supplier))
        .order_by(SupplierImport.imported_at.desc())
    ).all()
    return [
        SupplierImportOut(
            **{
                column: getattr(item, column)
                for column in SupplierImportOut.model_fields
                if column != "supplier_name"
            },
            supplier_name=item.supplier.name,
        )
        for item in imports
    ]


@app.get("/api/admin/supplier-imports/{import_id}/review")
def supplier_import_review(
    import_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> list[dict]:
    return [
        {
            "id": row.id,
            "supplier_sku": row.supplier_sku,
            "raw_payload": row.raw_payload,
            "suggested_product_id": row.suggested_product_id,
            "status": row.status,
            "error": row.error,
        }
        for row in session.scalars(
            select(OfferImportReview)
            .where(OfferImportReview.import_id == import_id)
            .order_by(OfferImportReview.id)
        ).all()
    ]


@app.get("/suppliers/{supplier_id}", include_in_schema=False)
def supplier_page(supplier_id: int) -> FileResponse:
    return FileResponse(static_dir / "supplier.html")


@app.get("/admin/suppliers", include_in_schema=False)
def admin_suppliers_page() -> FileResponse:
    return FileResponse(static_dir / "suppliers-admin.html")


@app.get("/admin/supplier-imports", include_in_schema=False)
def admin_supplier_imports_page() -> FileResponse:
    return FileResponse(static_dir / "suppliers-admin.html")


@app.get("/api/admin/search-aliases", response_model=list[SearchAliasOut])
def search_aliases(session: Annotated[Session, Depends(get_session)]) -> list[SearchAlias]:
    return list(
        session.scalars(
            select(SearchAlias).order_by(SearchAlias.created_at.desc(), SearchAlias.id.desc())
        ).all()
    )


@app.get("/api/admin/search-aliases/targets", response_model=SearchAliasTargetsOut)
def search_alias_targets(
    session: Annotated[Session, Depends(get_session)],
) -> SearchAliasTargetsOut:
    stored = session.execute(select(SearchAlias.kind, SearchAlias.canonical)).all()
    fitted = session.execute(
        select(Vehicle.make, Vehicle.model)
        .join(Fitment, Fitment.vehicle_id == Vehicle.id)
        .join(Product, Product.id == Fitment.product_id)
        .where(Product.is_searchable.is_(True), Vehicle.model.not_like("(%"))
        .distinct()
    ).all()
    products = {*PRODUCT_SYNONYMS, *(name for kind, name in stored if kind == "product")}
    vehicle_names = {
        *VEHICLE_ALIASES,
        *(name for kind, name in stored if kind == "vehicle"),
        *(" ".join(filter(None, row)) for row in fitted),
    }
    return SearchAliasTargetsOut(
        product=sorted(products, key=str.casefold),
        vehicle=sorted(vehicle_names, key=str.casefold),
    )


@app.post("/api/admin/search-aliases", response_model=SearchAliasOut, status_code=201)
def create_search_alias(
    payload: SearchAliasCreate,
    session: Annotated[Session, Depends(get_session)],
) -> SearchAliasOut:
    alias = normalize_text(payload.alias)
    canonical = " ".join(payload.canonical.split())
    canonical_key = normalize_text(canonical)
    if not alias or not canonical_key:
        raise HTTPException(
            status_code=422, detail="Alias and target must contain letters or digits"
        )
    if alias == canonical_key:
        raise HTTPException(status_code=422, detail="Alias is the same as its target")

    known = PRODUCT_SYNONYMS if payload.kind == "product" else VEHICLE_ALIASES
    stored = set(
        session.scalars(select(SearchAlias.canonical).where(SearchAlias.kind == payload.kind))
    )
    if canonical not in known and canonical not in stored:
        # A new target must exist in the catalog, otherwise the alias can never match.
        if payload.kind == "product":
            exists = select(Product.id).where(
                Product.is_searchable.is_(True),
                Product.normalized_name.contains(canonical_key),
            )
        else:
            exists = select(Vehicle.id).where(Vehicle.normalized_text.contains(canonical_key))
        if session.scalar(exists.limit(1)) is None:
            raise HTTPException(
                status_code=422,
                detail=f"No {payload.kind} in the catalog matches \u201c{canonical}\u201d",
            )
    duplicate = session.scalar(
        select(SearchAlias).where(SearchAlias.kind == payload.kind, SearchAlias.alias == alias)
    )
    if duplicate is not None:
        raise HTTPException(
            status_code=409,
            detail=f"\u201c{alias}\u201d already points to \u201c{duplicate.canonical}\u201d",
        )

    record = SearchAlias(
        kind=payload.kind,
        alias=alias,
        canonical=canonical,
        source_query=payload.source_query,
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    out = SearchAliasOut.model_validate(record)
    if payload.source_query:
        out.source_query_result_count = search_products(
            session, payload.source_query, limit=1
        ).total
    return out


@app.delete("/api/admin/search-aliases/{alias_id}", status_code=204)
def delete_search_alias(alias_id: int, session: Annotated[Session, Depends(get_session)]) -> None:
    record = session.get(SearchAlias, alias_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Alias not found")
    session.delete(record)
    session.commit()


@app.get("/admin/requests", include_in_schema=False)
def admin_requests_page() -> FileResponse:
    return FileResponse(static_dir / "requests-admin.html")


@app.get("/api/admin/reservations", response_model=list[AdminReservationOut])
def admin_reservations(
    session: Annotated[Session, Depends(get_session)],
    status: Annotated[str | None, Query(max_length=30)] = None,
) -> list[AdminReservationOut]:
    stmt = (
        select(ReservationRequest)
        .options(
            selectinload(ReservationRequest.product),
            selectinload(ReservationRequest.supplier_offer).selectinload(SupplierOffer.supplier),
        )
        .order_by(ReservationRequest.created_at.desc(), ReservationRequest.id.desc())
        .limit(200)
    )
    if status:
        stmt = stmt.where(ReservationRequest.status == status)
    return [admin_reservation_out(reservation) for reservation in session.scalars(stmt)]


@app.patch("/api/admin/reservations/{reservation_id}", response_model=AdminReservationOut)
def update_reservation(
    reservation_id: int,
    payload: ReservationUpdate,
    session: Annotated[Session, Depends(get_session)],
) -> AdminReservationOut:
    """Move a reservation along; its outcome feeds the supplier's reliability score."""
    reservation = session.get(ReservationRequest, reservation_id)
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    changes = payload.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(reservation, key, value)
    reservation.updated_at = datetime.now(UTC)
    session.flush()
    if "outcome" in changes:
        recompute_reliability(session, reservation.supplier_offer.supplier_id)
    session.commit()
    session.refresh(reservation)
    return admin_reservation_out(reservation)


@app.get("/api/admin/part-requests", response_model=list[PartRequestOut])
def admin_part_requests(session: Annotated[Session, Depends(get_session)]) -> list[PartRequest]:
    return list(
        session.scalars(
            select(PartRequest)
            .order_by(PartRequest.status != "OPEN", PartRequest.created_at.desc())
            .limit(200)
        )
    )


@app.patch("/api/admin/part-requests/{request_id}", response_model=PartRequestOut)
def update_part_request(
    request_id: int,
    payload: PartRequestUpdate,
    session: Annotated[Session, Depends(get_session)],
) -> PartRequest:
    request = session.get(PartRequest, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Part request not found")
    request.status = payload.status
    session.commit()
    session.refresh(request)
    return request


@app.get("/api/admin/fit-reports", response_model=list[AdminFitReportOut])
def admin_fit_reports(session: Annotated[Session, Depends(get_session)]) -> list[AdminFitReportOut]:
    """Fit reports per part and car, the parts most often reported as not fitting first."""
    does_not_fit = func.count(FitReport.id).filter(FitReport.fits.is_(False))
    rows = session.execute(
        select(
            FitReport.product_id,
            Product.name,
            FitReport.vehicle_label,
            func.count(FitReport.id).filter(FitReport.fits.is_(True)),
            does_not_fit,
            func.max(FitReport.created_at),
        )
        .join(Product, Product.id == FitReport.product_id)
        .group_by(FitReport.product_id, Product.name, FitReport.vehicle_label)
        .order_by(does_not_fit.desc(), func.max(FitReport.created_at).desc())
        .limit(200)
    ).all()
    return [
        AdminFitReportOut(
            product_id=product_id,
            product_name=name,
            vehicle_label=label,
            fits=fits,
            does_not_fit=not_fit,
            last_report=last,
        )
        for product_id, name, label, fits, not_fit, last in rows
    ]


@app.get("/part/{product_id}", include_in_schema=False, response_class=HTMLResponse)
def part_page_html(
    product_id: str, request: Request, session: Annotated[Session, Depends(get_session)]
) -> HTMLResponse:
    """A part's own address: the catalog page, titled and described for search engines."""
    template = (static_dir / "index.html").read_text(encoding="utf-8")
    product = get_product_detail(session, product_id)
    if product is None:
        return HTMLResponse(template, status_code=404)
    return HTMLResponse(part_page(template, product, str(request.base_url)))


@app.get("/sitemap.xml", include_in_schema=False)
def sitemap_xml(request: Request, session: Annotated[Session, Depends(get_session)]) -> Response:
    rows = session.execute(
        select(Product.id, Product.updated_at)
        .where(Product.is_searchable.is_(True))
        .order_by(Product.id)
    ).all()
    entries = [
        (product_id, updated.date().isoformat() if updated else None)
        for product_id, updated in rows
    ]
    return Response(sitemap(str(request.base_url), entries), media_type="application/xml")


@app.get("/robots.txt", include_in_schema=False)
def robots_txt(request: Request) -> Response:
    return Response(robots(str(request.base_url)), media_type="text/plain")
