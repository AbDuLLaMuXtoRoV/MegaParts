"""Sellers' own price lists: reading slang names, any layout, and buying across sellers."""

from datetime import UTC, datetime
from io import BytesIO

import pytest
from openpyxl import Workbook
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from app.database import get_session
from app.main import app, settings
from app.models import (
    Base,
    CatalogReviewItem,
    Fitment,
    Product,
    ProductAudit,
    ReferenceNumber,
    SupplierOffer,
    Vehicle,
)
from app.normalization import normalize_text
from app.part_names import display_names, part_numbers, read_part_name
from app.price_list_import import import_price_list, reference_type, supplier_by_name
from app.price_list_reader import parse_price_list, promo, warranty
from app.product_context import alternatives
from app.search import search_products
from tests.conftest import admin_login

RECEIVED = datetime(2026, 10, 22, tzinfo=UTC)


def workbook(rows: list[list]) -> bytes:
    book = Workbook()
    sheet = book.active
    for row in rows:
        sheet.append(row)
    buffer = BytesIO()
    book.save(buffer)
    return buffer.getvalue()


# A list like BOS-KOS's: contacts on top, warranty headings between rows, a status column.
BOSKOS = workbook([
    ["BOS-KOS"],
    ["+998 90 000-00-01 ZAKAS BERISH     +998900000002  TELEGRAM"],
    ["№", "Наименование Товаров", "ЕдИзм", "BREND", "KAROBKA", "Модел", "ZAKAS"],
    [],
    ["AMARTIZATOR    GARANTIYA  10.000 KM   3 OY"],
    [1, "AMORTIZATOR OLDI LH (96394572)", "DONA", "BOSKOS", 10, "NEXIA", None, "YANGI KELDI"],
    [2, "KALODKA ORQA (96226110)   PREMIUM", "KOMP", "BOSKOS   KOREA", 10, "NEXIA", None,
     "-20%  AKSIYA"],
    [3, "PORSHEN STD", "KOMP", "BOSKOS", 12, "PORTER 2"],
    ["Жами:"],
])
# A list like "BIZDA BOR": no titles over the code, name and model columns, prices in dollars.
BIZDA = workbook([
    ["KURS 6,7  18 FOIZ", None, None, None, None, "YUAN", "NARXI"],
    ["96394572 WSM", "Амортизатор передний L", "NEXIA", 1, "шт", 55, 9.69],
    ["96226110-N/WSM", "колодка задняя", "NEXIA", 1, "к-т", 20, 3.52],
    [None, "РЕЛЕ БЕНЗАНСОС НЕКСИЯ 0644 WSM", None, 1, "шт", 0.7, 0.12],
])


@pytest.fixture
def engine():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        for vehicle_id, make, model, generation in (
            ("V-00002", "Daewoo", "Nexia", "N100 · 1.5 SOHC 8V"),
            ("V-00003", "Daewoo", "Nexia", "N100 · 1.5 DOHC 16V"),
            ("V-00004", "Daewoo", "Nexia", "N150 · 1.5 SOHC 8V"),
            ("V-00005", "Daewoo", "Nexia", "N150 · 1.6 DOHC 16V"),
            ("V-00022", "Chevrolet", "Cobalt", "II · 1.5"),
            ("V-00017", "Chevrolet", "Lacetti", "J200 · 1.6"),
        ):
            session.add(Vehicle(id=vehicle_id, make=make, model=model, generation=generation,
                                normalized_text=normalize_text(f"{make} {model} {generation}")))
        session.commit()
    return engine


def test_slang_names_become_part_types_with_position_side_and_numbers() -> None:
    shock = read_part_name("AMORTIZATOR OLDI LH 96394572")
    assert (shock.type_id, shock.position, shock.side) == ("CAT-SUS-SHOCK", "front", "left")
    assert shock.numbers == ["96394572"]
    # Rear pads are drum-brake shoes on a Nexia, but pads on a Lacetti with rear discs.
    assert read_part_name("KALODKA ORQA", "NEXIA").type_id == "CAT-BRK-SHOE"
    assert read_part_name("KALODKA ORQA", "LACETTI").type_id == "CAT-BRK-PAD"
    # "PRAVODA" is a wire, not the right side; a relay is not the pump it switches.
    wires = read_part_name("SVECHA PRAVODA (96288956)")
    assert (wires.type_id, wires.side) == ("CAT-IGN-WIRE", None)
    assert read_part_name("РЕЛЕ БЕНЗАНСОС НЕКСИЯ 0644 WSM").type_id == "CAT-EL-RELAY"
    assert read_part_name("амортнзатор задней").type_id == "CAT-SUS-SHOCK"
    assert read_part_name("PORSHEN 0,25").size == "0.25"
    assert part_numbers("ESHIK REZINA 96267421/22/23/24") == [
        "96267421", "96267422", "96267423", "96267424"
    ]
    assert part_numbers("BENZIN NASOS 0580453434") == ["0580453434"]


def test_names_are_written_in_uzbek_russian_and_english() -> None:
    part = read_part_name("SINXRON 4/5 M/T 94582234")
    names = display_names(part, ("Uzatmalar qutisi qismlari", "Детали КПП", "Gearbox parts"))
    assert names == ("Sinxronizator, MT", "Синхронизатор МКПП", "Synchronizer, manual")
    shock = read_part_name("AMORTIZATOR OLDI LH")
    assert display_names(shock, ("Amortizator", "Амортизатор", "Shock absorber")) == (
        "Amortizator, oldi chap", "Амортизатор пер. лев.", "Shock absorber, front left"
    )
    unknown = read_part_name("KULACHOK")
    assert display_names(unknown, None) == ("Kulachok", "Кулачок", "Kulachok")


def test_any_layout_is_read_with_contacts_warranty_and_labels() -> None:
    bos = parse_price_list(BOSKOS, "BOS-KOS.xlsx")
    assert [row.name for row in bos.rows] == [
        "AMORTIZATOR OLDI LH (96394572)", "KALODKA ORQA (96226110) PREMIUM", "PORSHEN STD",
    ]
    assert bos.phones == ["+998900000001", "+998900000002"]
    assert bos.telegram == "+998900000002"
    first = bos.rows[0]
    assert (first.brand, first.model, first.pack_qty, first.status) == (
        "BOSKOS", "NEXIA", 10, "YANGI KELDI"
    )
    assert warranty(first.section) == (3, 10000)
    assert promo(bos.rows[1].status) == ("DISCOUNT", 20)

    bizda = parse_price_list(BIZDA, "BIZDA BOR ZAPCHAS 02,10,2026.xlsx")
    assert {"code", "name", "model", "unit", "price"} <= set(bizda.columns)
    assert bizda.document_date.isoformat() == "2026-10-02"
    assert [(row.code, str(row.price), row.currency) for row in bizda.rows[:2]] == [
        ("96394572 WSM", "9.69", "USD"), ("96226110-N/WSM", "3.52", "USD"),
    ]


def test_two_sellers_of_one_part_become_two_offers_to_compare(engine) -> None:
    with Session(engine) as session:
        boskos = supplier_by_name(session, "BOS-KOS")
        result = import_price_list(session, boskos, BOSKOS, "BOS-KOS.xlsx", RECEIVED)
        assert result.products_created == 3
        # The Porter is a car the catalog did not list yet.
        assert result.vehicles_created == ["Hyundai Porter"]
        assert boskos.telegram == "+998900000002"

        shock = session.scalar(select(Product).where(Product.article_number == "96394572"))
        assert shock.category_id == "CAT-SUS-SHOCK"
        assert shock.name_ru == "Амортизатор пер. лев."
        # "NEXIA" without a generation means every Nexia, flagged to check.
        fitted = {fitment.vehicle_id for fitment in shock.fitments}
        assert fitted == {"V-00002", "V-00003", "V-00004", "V-00005"}
        assert "avlodni tekshiring" in shock.fitments[0].condition_note
        offer = shock.supplier_offers[0]
        assert (offer.warranty_months, offer.warranty_km, offer.promo, offer.pack_qty) == (
            3, 10000, "NEW_ARRIVAL", 10
        )

        # Another seller lists the same brand and number: one part, two offers.
        other = supplier_by_name(session, "Second seller")
        same = workbook([
            ["Наименование", "Модел", "Бренд", "Ед изм", "Ишлаб чикарувчи"],
            ["AMORTIZATOR OLDI LH 96394572", "NEXIA", "BOSKOS", "DONA", "KOREA"],
        ])
        second = import_price_list(session, other, same, "second.xlsx", RECEIVED)
        assert (second.products_created, second.products_reused) == (0, 1)
        session.refresh(shock)
        assert len(shock.supplier_offers) == 2
        assert shock.country_of_origin == "KR"
        session.commit()

        # The seller's own wording finds the part too.
        found = search_products(session, "amartizator oldi")
        assert shock.id in [item.id for item in found.items]


def test_a_new_list_replaces_the_old_one(engine) -> None:
    with Session(engine) as session:
        bizda = supplier_by_name(session, "BIZDA BOR")
        first = import_price_list(session, bizda, BIZDA, "bizda.xlsx", RECEIVED)
        assert first.offers_created == 3
        shorter = workbook([
            ["KURS 6,7", None, None, None, None, "YUAN", "NARXI"],
            ["96394572 WSM", "Амортизатор передний L", "NEXIA", 1, "шт", 60, 10.5],
            ["96226110-N/WSM", "колодка задняя", "NEXIA", 1, "к-т", 20, 3.52],
        ])
        second = import_price_list(session, bizda, shorter, "bizda-2.xlsx", RECEIVED)
        assert (second.offers_updated, second.offers_closed, second.products_created) == (2, 1, 0)
        prices = session.scalars(
            select(SupplierOffer.price).where(SupplierOffer.is_active.is_(True))
        ).all()
        assert sorted(map(str, prices)) == ["10.50", "3.52"]
        assert session.scalar(select(func.count(Product.id))) == 3


# A third seller with BOS-KOS's shock absorber, for comparing sellers of one part.
KOREA = workbook([
    ["", "Наименование", "Модел", "Бренд", "Ед изм", "Ишлаб чикарувчи"],
    ["", "AMORTIZATOR OLDI LH 96394572", "NEXIA", "BOSKOS", "DONA", "KOREA"],
    ["", "AMORTIZATOR OLDI RH 96394573", "NEXIA", "GM", "DONA", "KOREA"],
])


@pytest.fixture
def client(engine):
    with Session(engine) as session:
        for name, content in (("BOS-KOS", BOSKOS), ("BIZDA BOR", BIZDA), ("KOREA", KOREA)):
            import_price_list(session, supplier_by_name(session, name), content, name, RECEIVED)
        session.commit()
    factory = sessionmaker(engine, expire_on_commit=False)

    def override_session():
        with factory() as session:
            yield session

    previous = settings.pilot_mode
    settings.pilot_mode = False
    app.dependency_overrides[get_session] = override_session
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        settings.pilot_mode = previous
        app.dependency_overrides.clear()


def test_basket_reserves_across_sellers_in_one_go(client) -> None:
    found = client.get("/api/v1/search", params={"q": "96394572"}).json()["items"]
    shock = next(item for item in found if item["brand"]["name"] == "BOSKOS")
    offers = shock["offers"]
    assert {offer["supplier"]["name"] for offer in offers} == {"BOS-KOS", "KOREA"}
    # The same number from another brand is an analog, graded by quality.
    detail = client.get(f"/api/v1/products/{shock['id']}").json()
    analogs = {alt["brand"]["name"]: alt["quality"] for alt in detail["alternatives"]
               if alt["relation"] == "SAME_NUMBER"}
    assert analogs == {"WEISMO": "OTHER"}
    looked_up = client.get("/api/v1/offers", params={"ids": ",".join(str(o["id"]) for o in offers)})
    assert {entry["product_id"] for entry in looked_up.json()} == {shock["id"]}

    basket = client.post("/api/v1/reservations/basket", json={
        "session_id": "basket-session-1",
        "items": [{"product_id": shock["id"], "supplier_offer_id": offer["id"], "quantity": 2}
                  for offer in offers],
        "vin": "XWB3K32CDJA123456",
    })
    assert basket.status_code == 201, basket.text
    reservations = basket.json()["reservations"]
    assert len(reservations) == 2
    assert {reservation["basket_id"] for reservation in reservations} == {basket.json()["basket_id"]}
    mine = client.get("/api/v1/reservations", params={"session_id": "basket-session-1"}).json()
    assert {entry["basket_id"] for entry in mine} == {basket.json()["basket_id"]}

    gone = client.post("/api/v1/reservations/basket", json={
        "session_id": "basket-session-1",
        "items": [{"product_id": shock["id"], "supplier_offer_id": 999999}],
    })
    assert gone.status_code == 404


def test_repair_lists_quality_filters_sellers_and_applications(client) -> None:
    jobs = client.get("/api/v1/jobs", params={"make": "Daewoo", "model": "Nexia"}).json()
    suspension = next(job for job in jobs if job["id"] == "front-suspension")
    shocks = next(part for part in suspension["parts"] if part["type_id"] == "CAT-SUS-SHOCK")
    assert shocks["product"]["category"]["id"] == "CAT-SUS-SHOCK"
    assert shocks["options"] >= 1 and suspension["available"] >= 1

    results = client.get("/api/v1/search", params={"q": "amortizator"}).json()
    assert results["quality_counts"]
    korea = client.get("/api/v1/search", params={"q": "amortizator", "quality": "KOREA"}).json()
    assert all(item["quality"] == "KOREA" for item in korea["items"])
    brand = results["brand_facets"][0]
    narrowed = client.get("/api/v1/search", params={"q": "amortizator", "brand": brand["id"]})
    assert {item["brand"]["id"] for item in narrowed.json()["items"]} == {brand["id"]}
    cheapest = client.get("/api/v1/search", params={"q": "nexia", "sort": "price"}).json()
    priced = [item for item in cheapest["items"] if any(o.get("price") for o in item["offers"])]
    assert priced and priced == cheapest["items"][: len(priced)]

    sellers = client.get("/api/v1/sellers").json()
    assert {card["supplier"]["name"] for card in sellers} == {"BOS-KOS", "BIZDA BOR", "KOREA"}

    applied = client.post("/api/v1/seller-applications", json={
        "business_name": "Malika bozori 3-qator", "phone": "+998901234567", "cars": "Nexia, Damas",
    })
    assert applied.status_code == 201
    assert client.get("/api/admin/seller-applications").status_code == 401
    admin_login(client)
    listed = client.get("/api/admin/seller-applications").json()
    assert listed[0]["business_name"] == "Malika bozori 3-qator"
    assert client.patch(f"/api/admin/seller-applications/{listed[0]['id']}",
                        json={"status": "CONTACTED"}).json()["status"] == "CONTACTED"


def test_staff_add_a_seller_and_upload_their_list(client) -> None:
    admin_login(client)
    created = client.post("/api/admin/suppliers", json={"name": "Sergeli 9-qator"})
    assert created.status_code == 201
    supplier_id = created.json()["id"]
    assert client.post("/api/admin/suppliers", json={"name": "sergeli 9 qator"}).status_code == 409
    renamed = client.patch(f"/api/admin/suppliers/{supplier_id}", json={"name": "Sergeli 9-qator, 12"})
    assert renamed.json()["name"] == "Sergeli 9-qator, 12"

    uploaded = client.post(
        f"/api/admin/suppliers/{supplier_id}/price-list",
        files={"file": ("list.xlsx", BOSKOS, "application/vnd.ms-excel")},
    )
    assert uploaded.status_code == 200, uploaded.text
    summary = uploaded.json()
    # The two numbered parts join BOS-KOS's; "PORSHEN STD" has no number, so it stays apart.
    assert (summary["rows"], summary["parts_reused"], summary["offers_created"]) == (3, 2, 3)
    bad = client.post(
        f"/api/admin/suppliers/{supplier_id}/price-list",
        files={"file": ("empty.xlsx", workbook([[1, 2], [3, 4]]), "application/vnd.ms-excel")},
    )
    assert bad.status_code == 422


def test_lists_without_prices_do_not_expire(engine) -> None:
    with Session(engine) as session:
        supplier = supplier_by_name(session, "BOS-KOS")
        long_ago = datetime(2025, 1, 1, tzinfo=UTC)
        import_price_list(session, supplier, BOSKOS, "old.xlsx", long_ago)
        session.commit()
        found = search_products(session, "96394572")
        assert found.items[0].offers, "a list naming parts without prices stays until replaced"
        assert session.scalar(select(func.count(Fitment.id))) > 0


def test_matching_follows_the_blueprint_rules(engine) -> None:
    """Brand + number joins sellers only without a variant conflict; a seller's code and a
    similar name never do (they become review items for the catalog team)."""
    assert [reference_type(code) for code in ("96394572", "74120A78B00", "54300-4E400")] == [
        "OE", "OE", "OE"
    ]
    assert [reference_type(code) for code in ("CBKD-15", "6203-RS", "0580453434")] == [
        "AFTERMARKET", "AFTERMARKET", "AFTERMARKET"
    ]
    assert [reference_type(code) for code in ("NP1013", "513315")] == [
        "SUPPLIER_SKU", "SUPPLIER_SKU"
    ]
    with Session(engine) as session:
        first = supplier_by_name(session, "First")
        import_price_list(session, first, workbook([
            ["Наименование", "Модел", "Бренд", "Ед изм"],
            ["PORSHEN STD 12111A78B01", "DAMAS", "GM", "KOMP"],
            ["KOLSA STD", "DAMAS", "MOTECH", "KOMP"],
            ["SVECHA PRAVODA NP1332", "NEXIA", "BOSKOS", "KOMP"],
        ]), "first.xlsx", RECEIVED)
        second = supplier_by_name(session, "Second")
        result = import_price_list(session, second, workbook([
            ["Наименование", "Модел", "Бренд", "Ед изм"],
            ["PORSHEN STD 12111A78B01", "DAMAS", "GM", "KOMP"],
            ["PORSHEN 0.25 12111A78B01", "DAMAS", "GM", "KOMP"],
            ["KOLSA STD", "DAMAS", "MOTECH", "KOMP"],
            ["SVECHA PRAVODA NP1332", "NEXIA", "BOSKOS", "KOMP"],
        ]), "second.xlsx", RECEIVED)
        # Only the STD piston (same brand, number and size) joins the first seller's part.
        assert (result.products_reused, result.products_created) == (1, 3)
        std = session.scalar(select(Product).where(Product.name.like("Porshen%STD%")))
        assert {offer.supplier.name for offer in std.supplier_offers} == {"First", "Second"}
        audit = session.scalar(select(ProductAudit).where(ProductAudit.product_id == std.id))
        assert audit.merge_status == "CONFIRMED" and audit.supplier_count == 2
        reasons = [item.review_reason for item in session.scalars(select(CatalogReviewItem))]
        assert any("variant boshqa" in reason for reason in reasons)  # 0.25 against STD
        assert any("avtomatik birlashtirilmadi" in reason for reason in reasons)  # KOLSA STD
        # NP1332 is the seller's own code: kept and searchable, but it joins nothing.
        codes = session.scalars(
            select(ReferenceNumber.type).where(ReferenceNumber.normalized_number == "np1332")
        ).all()
        assert codes == ["SUPPLIER_SKU", "SUPPLIER_SKU"]
        piston = session.scalar(select(Product).where(Product.name.like("Porshen%0.25%")))
        assert {a.attribute_code: a.value for a in piston.attributes}["repair_size"] == "0.25"
        # On the part page the STD piston is the same number in another size, not an analog.
        related = {item.id: item for item in alternatives(session, piston, None)}
        assert related[std.id].relation == "SAME_NUMBER"
        assert related[std.id].same_variant is False


def test_buyers_cancel_their_own_reservations(client) -> None:
    found = client.get("/api/v1/search", params={"q": "96394572"}).json()["items"]
    shock = next(item for item in found if item["brand"]["name"] == "BOSKOS")
    basket = client.post("/api/v1/reservations/basket", json={
        "session_id": "cancel-session-1",
        "items": [{"product_id": shock["id"], "supplier_offer_id": offer["id"]}
                  for offer in shock["offers"]],
    }).json()
    first, second = basket["reservations"]

    # Someone else's browser cannot cancel it.
    stranger = client.post(f"/api/v1/reservations/{first['id']}/cancel",
                           json={"session_id": "someone-else-1"})
    assert stranger.status_code == 404
    one = client.post(f"/api/v1/reservations/{first['id']}/cancel",
                      json={"session_id": "cancel-session-1"})
    assert one.json()["status"] == "CANCELLED"

    rest = client.post(f"/api/v1/reservations/basket/{basket['basket_id']}/cancel",
                       json={"session_id": "cancel-session-1"}).json()
    assert {entry["id"]: entry["status"] for entry in rest} == {
        first["id"]: "CANCELLED", second["id"]: "CANCELLED"
    }
    # A buyer cancelling says nothing about the seller.
    admin_login(client)
    assert all(
        supplier["reliability_sample"] == 0 for supplier in client.get("/api/admin/suppliers").json()
    )
