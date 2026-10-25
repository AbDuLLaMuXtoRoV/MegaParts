from pathlib import Path

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from app.database import get_session
from app.import_catalog import import_workbook
from app.main import app, settings
from app.models import (
    Base,
    CatalogListValue,
    Category,
    ProductAudit,
    SearchSynonym,
    SupplierOffer,
)
from app.search import search_products
from tests.conftest import admin_login

WORKBOOK = Path(__file__).resolve().parents[1] / "IRIZON_Master_Catalog_v2.0 (1).xlsx"
pytestmark = pytest.mark.skipif(not WORKBOOK.exists(), reason="IRIZON workbook not present")


@pytest.fixture(scope="module")
def engine():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        import_workbook(session, WORKBOOK)
    return engine


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
            admin_login(test_client)
            yield test_client
    finally:
        settings.pilot_mode = previous
        app.dependency_overrides.clear()


def editable(record: dict) -> dict:
    """Turn a GET record into the PUT body the profile form sends back."""
    body = {
        key: record[key]
        for key in (
            "name",
            "name_ru",
            "name_en",
            "brand_id",
            "category_id",
            "article_number",
            "origin",
            "status",
            "unit",
            "pack_qty",
            "weight_kg",
            "length_mm",
            "width_mm",
            "height_mm",
            "ean",
            "country_of_origin",
            "description",
            "universal",
            "attributes",
            "references",
            "fitments",
            "offers",
        )
    }
    body["expected_updated_at"] = record["updated_at"]
    return body


def test_every_workbook_sheet_is_in_the_database(engine) -> None:
    with Session(engine) as session:
        # 47 workbook categories plus the 96 standard part types the workbook lacks.
        assert session.scalar(select(func.count(Category.id))) == 47 + 96
        assert session.scalar(select(func.count(SearchSynonym.id))) == 120
        # Four products carry two audit findings each; none may be dropped.
        assert session.scalar(select(func.count(ProductAudit.id))) == 36
        assert session.scalar(select(func.count(CatalogListValue.id))) > 100


def test_cyrillic_vehicle_synonyms_are_searchable(engine) -> None:
    with Session(engine) as session:
        response = search_products(session, "Тико")
        assert response.parsed_query_internal["vehicle"] == "Daewoo Tico"
        assert response.total > 0


def test_profile_and_options_expose_the_full_catalog(client: TestClient) -> None:
    profile = client.get("/api/admin/catalog/profile").json()
    assert profile["username"] == "irizon"
    assert profile["suppliers"][0]["name"] == "IRIZON (distribyutor)"
    assert profile["stats"]["products"] == 258
    assert profile["stats"]["hidden_conflicts"] == 8

    options = client.get("/api/admin/catalog/options").json()
    assert "AFTERMARKET" in options["lists"]["origin"]
    assert any(category["attributes"] for category in options["categories"])
    assert options["help"]["Products.product_name_uz"]
    assert len(options["vehicles"]) == 97


def test_product_record_has_every_workbook_field(client: TestClient) -> None:
    record = client.get("/api/admin/catalog/products/P-000001").json()
    assert record["name_ru"] == "Бабина"
    assert record["name_en"] == "Ignition coil"
    assert record["category_id"] == "CAT-IGN-COIL"
    assert record["country_of_origin"] == "CN"
    assert record["references"][0]["number"] == "3555"
    assert record["fitments"][0]["vehicle_label"].startswith("Daewoo Matiz")
    assert record["offers"][0]["supplier_id"]


def test_editing_a_product_updates_the_database_and_search(client: TestClient, engine) -> None:
    record = client.get("/api/admin/catalog/products/P-000001").json()
    body = editable(record)
    body["name_ru"] = "Катушка зажигания"
    body["references"].append({"number": "ZX-90210", "type": "OE", "confidence": "HIGH"})
    body["fitments"].append({"vehicle_id": "V-00001", "position": "N/A", "side": "N/A"})
    body["offers"][0]["price"] = "125000"
    body["offers"][0]["stock_qty"] = 7

    saved = client.put("/api/admin/catalog/products/P-000001", json=body)
    assert saved.status_code == 200, saved.text
    record = saved.json()
    assert record["name_ru"] == "Катушка зажигания"
    assert {ref["number"] for ref in record["references"]} == {"3555", "ZX-90210"}
    assert record["offers"][0]["price"] == "125000"
    assert record["offers"][0]["data_status"] == "LIVE"

    with Session(engine) as session:
        assert [item.id for item in search_products(session, "ZX90210").items] == ["P-000001"]
        tico = search_products(session, "Tico babina")
        assert "P-000001" in [item.id for item in tico.items]


def test_stale_edits_are_refused(client: TestClient) -> None:
    record = client.get("/api/admin/catalog/products/P-000002").json()
    first = editable(record)
    first["description"] = "first edit"
    assert client.put("/api/admin/catalog/products/P-000002", json=first).status_code == 200

    second = editable(record)  # still carries the old version
    second["description"] = "second edit"
    assert client.put("/api/admin/catalog/products/P-000002", json=second).status_code == 409


def test_validation_reports_every_problem(client: TestClient) -> None:
    body = editable(client.get("/api/admin/catalog/products/P-000003").json())
    body["status"] = "SOLD_OUT"
    body["category_id"] = "CAT-NOPE"
    body["references"] = [
        {"number": "123", "type": "OE"},
        {"number": "1-2-3", "type": "OE"},
    ]
    body["fitments"] = [{"vehicle_id": "V-99999"}]
    response = client.put("/api/admin/catalog/products/P-000003", json=body)
    assert response.status_code == 422
    fields = {error["field"] for error in response.json()["detail"]["errors"]}
    assert {"status", "category_id", "references.1.number", "fitments.0.vehicle_id"} <= fields


def test_removed_offers_are_deactivated_not_deleted(client: TestClient, engine) -> None:
    record = client.get("/api/admin/catalog/products/P-000004").json()
    offer_id = record["offers"][0]["id"]
    body = editable(record)
    body["offers"] = []
    assert client.put("/api/admin/catalog/products/P-000004", json=body).status_code == 200
    with Session(engine) as session:
        assert session.get(SupplierOffer, offer_id).is_active is False


def test_create_product_gets_next_id_and_is_searchable(client: TestClient, engine) -> None:
    supplier_id = client.get("/api/admin/catalog/profile").json()["suppliers"][0]["id"]
    response = client.post(
        "/api/admin/catalog/products",
        json={
            "name": "Moy filtri test",
            "category_id": "CAT-IGN-COIL",
            "origin": "AFTERMARKET",
            "status": "ACTIVE",
            "unit": "PCS",
            "references": [{"number": "MF-777", "type": "AFTERMARKET"}],
            "offers": [{"supplier_id": supplier_id, "price": "9900", "stock_qty": 3}],
        },
    )
    assert response.status_code == 201, response.text
    created = response.json()
    assert created["id"] == "P-000259"
    assert created["is_searchable"] is True
    with Session(engine) as session:
        assert [item.id for item in search_products(session, "MF-777").items] == ["P-000259"]


def test_supplier_profile_can_be_edited(client: TestClient) -> None:
    supplier = client.get("/api/admin/catalog/profile").json()["suppliers"][0]
    payload = {
        "name": supplier["name"],
        "supplier_type": "DISTRIBUTOR",
        "city": "Toshkent",
        "phone": "+998 90 000 00 00",
        "default_currency": "UZS",
        "integration": "EXCEL",
        "default_lead_time_days": 2,
    }
    assert (
        client.put(f"/api/admin/catalog/suppliers/{supplier['id']}", json=payload).status_code
        == 200
    )
    updated = client.get("/api/admin/catalog/profile").json()["suppliers"][0]
    assert updated["city"] == "Toshkent"
    assert updated["default_lead_time_days"] == 2

    payload["default_currency"] = "XYZ"
    assert (
        client.put(f"/api/admin/catalog/suppliers/{supplier['id']}", json=payload).status_code
        == 422
    )


def test_filters_find_products_needing_work(client: TestClient) -> None:
    conflicts = client.get("/api/admin/catalog/products", params={"issue": "conflict"}).json()
    assert conflicts["total"] == 8
    by_reference = client.get("/api/admin/catalog/products", params={"q": "3555"}).json()
    assert "P-000001" in [item["id"] for item in by_reference["items"]]
