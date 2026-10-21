"""Features adopted from leading parts sites: offer trust, fit help, reservations, SEO pages."""

from datetime import UTC, datetime, timedelta
from io import BytesIO

import pytest
from openpyxl import Workbook
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from app.catalog import refresh_products
from app.database import get_session
from app.main import app, settings
from app.models import (
    Base,
    Brand,
    Category,
    Fitment,
    Product,
    ReferenceNumber,
    Supplier,
    SupplierOffer,
    Vehicle,
)
from app.normalization import normalize_code, normalize_text
from app.search import search_products
from app.supplier_import import import_supplier_workbook
from tests.conftest import admin_login

NOW = datetime.now(UTC)
VIN = "XWB3K32CDJA123456"


def add_product(session, product_id, name, category_id, vehicles, brand, number, *, note=None):
    product = Product(
        id=product_id,
        name=name,
        normalized_name="",
        brand=brand,
        category_id=category_id,
        audit_status="CONFIRMED",
        is_searchable=True,
    )
    for vehicle in vehicles:
        product.fitments.append(
            Fitment(vehicle=vehicle, source_vehicle_text=vehicle.model, condition_note=note)
        )
    product.reference_numbers.append(
        ReferenceNumber(number=number, normalized_number=normalize_code(number), type="OE")
    )
    session.add(product)
    return product


def make_engine():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all(
            [
                Category(id="CAT-BRK", name_uz="Tormoz tizimi", is_leaf=False),
                Category(id="CAT-BRK-PAD", parent_id="CAT-BRK", name_uz="Tormoz kolodkalari"),
                Category(id="CAT-BRK-DISC", parent_id="CAT-BRK", name_uz="Tormoz disklari"),
            ]
        )
        cobalt = Vehicle(
            id="COB",
            make="Chevrolet",
            model="Cobalt",
            generation="II · 1.5",
            normalized_text="chevrolet cobalt",
        )
        nexia = Vehicle(id="NEX", make="Daewoo", model="Nexia", normalized_text="daewoo nexia")
        unicar = Brand(name="UNICAR", normalized_name="unicar")
        nero = Brand(name="NERO", normalized_name="nero")
        session.flush()
        add_product(session, "PAD-U", "Tormoz kolodkalari old", "CAT-BRK-PAD", [cobalt], unicar,
                    "96534653", note="KPP: AT")
        add_product(session, "PAD-N", "Tormoz kolodkalari old", "CAT-BRK-PAD", [cobalt], nero,
                    "96534653")
        add_product(session, "PAD-X", "Tormoz kolodkalari orqa", "CAT-BRK-PAD", [nexia], nero,
                    "11111111")
        add_product(session, "DISC", "Tormoz diski", "CAT-BRK-DISC", [cobalt], unicar, "22222222")
        supplier = Supplier(
            name="Sergeli 9-qator",
            normalized_name="sergeli 9 qator",
            telegram="@sergeli9",
            default_lead_time_days=3,
        )
        session.add(supplier)
        session.flush()
        for offer_id, product_id, age_days, extra in (
            ("O-FRESH", "PAD-U", 3, {"part_origin": "GENUINE", "warranty_months": 12}),
            ("O-OLD", "PAD-N", 10, {"lead_time_days": 0}),
            ("O-GONE", "DISC", 20, {}),
        ):
            session.add(
                SupplierOffer(
                    source_offer_id=offer_id,
                    supplier_id=supplier.id,
                    product_id=product_id,
                    price=100_000,
                    stock_qty=2,
                    updated_at=NOW - timedelta(days=age_days),
                    data_status="LIVE",
                    **extra,
                )
            )
        session.flush()
        refresh_products(session)
        session.commit()
    return engine


@pytest.fixture
def engine():
    return make_engine()


@pytest.fixture
def client(engine):
    factory = sessionmaker(engine, expire_on_commit=False)

    def override_session():
        with factory() as session:
            yield session

    previous = settings.pilot_mode
    settings.pilot_mode = False
    app.dependency_overrides[get_session] = override_session
    try:
        with TestClient(app) as test_client:
            test_client.factory = factory
            yield test_client
    finally:
        settings.pilot_mode = previous
        app.dependency_overrides.clear()


def test_old_prices_grey_out_after_a_week_and_disappear_after_two(client) -> None:
    fresh = client.get("/api/v1/products/PAD-U").json()["offers"][0]
    assert fresh["freshness_status"] == "STALE"
    assert fresh["part_origin"] == "GENUINE" and fresh["warranty_months"] == 12
    assert fresh["lead_time_days"] == 3  # the supplier's default
    old = client.get("/api/v1/products/PAD-N").json()["offers"][0]
    assert old["freshness_status"] == "OUTDATED" and old["lead_time_days"] == 0
    assert client.get("/api/v1/products/DISC").json()["offers"] == []


def test_alternatives_and_complete_the_job_for_the_buyers_car(client) -> None:
    detail = client.get("/api/v1/products/PAD-U", params={"vehicle_id": "COB"}).json()
    relations = {(item["id"], item["relation"]) for item in detail["alternatives"]}
    # Same OEM number from another brand; the Nexia pad does not fit a Cobalt.
    assert relations == {("PAD-N", "SAME_NUMBER")}
    assert detail["alternatives"][0]["shared_number"] == "96534653"
    assert [item["id"] for item in detail["complete_the_job"]] == ["DISC"]
    assert detail["vehicle_fitments"][0]["condition_note"] == "KPP: AT"


def test_supplier_verification_needs_documents_and_shows_on_offers(client) -> None:
    admin_login(client)
    supplier_id = client.get("/api/admin/suppliers").json()[0]["id"]
    refused = client.patch(f"/api/admin/suppliers/{supplier_id}", json={"verified": True})
    assert refused.status_code == 422
    saved = client.patch(
        f"/api/admin/suppliers/{supplier_id}",
        json={
            "verified": True,
            "legal_name": "Sergeli Avto MChJ",
            "inn": "301234567",
            "work_hours": "9:00–18:00",
            "address": "Sergeli avtobozori, 9-qator",
        },
    ).json()
    assert saved["verified_at"] is not None
    seller = client.get("/api/v1/products/PAD-U").json()["offers"][0]["supplier"]
    assert seller["verified"] is True
    assert seller["address"] == "Sergeli avtobozori, 9-qator"
    assert seller["reliability_score"] is None  # not enough history yet


def test_reservation_carries_the_car_and_feeds_supplier_reliability(client) -> None:
    offer_id = client.get("/api/v1/products/PAD-U").json()["offers"][0]["id"]
    base = {"session_id": "browser-1", "product_id": "PAD-U", "supplier_offer_id": offer_id}
    bad_vin = client.post("/api/v1/reservations", json={**base, "vin": "XWB0O0"})
    assert bad_vin.status_code == 422
    created = client.post(
        "/api/v1/reservations",
        json={**base, "vehicle_id": "COB", "vehicle_label": "Chevrolet Cobalt", "vin": VIN},
    )
    assert created.status_code == 201
    mine = client.get("/api/v1/reservations", params={"session_id": "browser-1"}).json()
    assert mine[0]["vin"] == VIN and mine[0]["status"] == "REQUESTED"
    assert mine[0]["supplier"]["telegram"] == "@sergeli9"
    assert mine[0]["reference_numbers"] == ["96534653"]

    admin_login(client)
    outcomes = ["HONOURED", "HONOURED", "HONOURED", "OUT_OF_STOCK", "NO_SHOW", "HONOURED"]
    for outcome in outcomes:
        reservation_id = client.post("/api/v1/reservations", json=base).json()["id"]
        updated = client.patch(
            f"/api/admin/reservations/{reservation_id}",
            json={"status": "COMPLETED", "outcome": outcome},
        )
        assert updated.status_code == 200
    supplier = client.get("/api/admin/suppliers").json()[0]
    # The buyer's no-show does not count: 4 honoured of 5.
    assert supplier["reliability_sample"] == 5
    assert float(supplier["reliability_score"]) == 80.0
    seller = client.get("/api/v1/products/PAD-U").json()["offers"][0]["supplier"]
    assert float(seller["reliability_score"]) == 80.0

    popular = client.get("/api/v1/search", params={"q": "kolodka"}).json()["items"]
    assert next(item for item in popular if item["id"] == "PAD-U")["reservation_count"] == 7


def test_part_requests_and_fit_reports_reach_the_team(client) -> None:
    request = client.post(
        "/api/v1/part-requests",
        json={"session_id": "b", "query": "rul reykasi", "contact": "+998901234567",
              "vehicle_id": "COB", "vehicle_label": "Chevrolet Cobalt"},
    )
    assert request.status_code == 201
    summary = client.post(
        "/api/v1/products/PAD-X/fit-reports",
        json={"session_id": "b", "fits": False, "vehicle_id": "COB", "vehicle_label": "Cobalt"},
    ).json()
    assert summary == [
        {"vehicle_id": "COB", "vehicle_label": "Cobalt", "fits": 0, "does_not_fit": 1}
    ]
    assert client.get("/api/v1/products/PAD-X").json()["fit_reports"][0]["does_not_fit"] == 1

    assert client.get("/admin/requests", follow_redirects=False).status_code == 303
    assert client.get("/api/admin/part-requests").status_code == 401
    admin_login(client)
    assert client.get("/admin/requests").status_code == 200
    requests = client.get("/api/admin/part-requests").json()
    assert requests[0]["query"] == "rul reykasi" and requests[0]["status"] == "OPEN"
    answered = client.patch(
        f"/api/admin/part-requests/{requests[0]['id']}", json={"status": "ANSWERED"}
    )
    assert answered.json()["status"] == "ANSWERED"
    reports = client.get("/api/admin/fit-reports").json()
    assert reports[0]["product_id"] == "PAD-X" and reports[0]["does_not_fit"] == 1


def test_every_part_has_an_indexable_page(client) -> None:
    page = client.get("/part/PAD-U")
    assert page.status_code == 200
    assert "<title>Tormoz kolodkalari old · UNICAR · 96534653 — MegaParts</title>" in page.text
    assert '"mpn": "96534653"' in page.text and '"@type": "Product"' in page.text
    assert '"isAccessoryOrSparePartFor"' in page.text
    assert "<noscript><article><h1>Tormoz kolodkalari old</h1>" in page.text
    assert client.get("/part/NOPE").status_code == 404
    assert "/part/PAD-U</loc>" in client.get("/sitemap.xml").text
    assert "Sitemap: http://testserver/sitemap.xml" in client.get("/robots.txt").text


def test_supplier_price_lists_carry_offer_labels(engine) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(
        ["Article", "Brand", "OEM", "Narx", "Turi", "Holati", "Kafolat", "Qaytarish", "Muddat"]
    )
    sheet.append(
        ["S-77", "UNICAR", "96534653", 150_000, "Аналог", "Б/у", "6 oy", "14 kun", "2"]
    )
    content = BytesIO()
    workbook.save(content)
    with Session(engine) as session:
        supplier = session.query(Supplier).one()
        batch = import_supplier_workbook(session, supplier, content.getvalue(), "list.xlsx")
        session.commit()
        assert batch.rows_matched == 1
        offer = next(
            offer
            for offer in session.query(SupplierOffer)
            if offer.source_reference and offer.source_reference.startswith("import:")
        )
        assert (offer.part_origin, offer.condition) == ("AFTERMARKET", "USED")
        assert (offer.warranty_months, offer.return_days, offer.lead_time_days) == (6, 14, 2)


def test_uzbek_cyrillic_and_ravon_names_find_the_part(engine) -> None:
    with Session(engine) as session:
        cyrillic = search_products(session, "тормоз колодкалари")
        assert {item.id for item in cyrillic.items} >= {"PAD-U", "PAD-N"}
        ravon = search_products(session, "ravon r4 kolodka")
        assert ravon.parsed_query_internal["vehicle"] == "Chevrolet Cobalt"
        assert normalize_text("Tormoz") == "tormoz"
