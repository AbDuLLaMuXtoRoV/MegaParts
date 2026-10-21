import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from app.database import get_session
from app.main import app, settings
from app.models import Base, Fitment, Product, ReferenceNumber, SearchAlias, SearchEvent, Vehicle
from app.normalization import normalize_code, normalize_text
from app.search import search_products
from app.vocabulary import correct_query, edit_distance, load_vocabulary
from tests.conftest import admin_login


def add_vehicle(session: Session, vehicle_id: str, make: str, model: str, generation=None):
    vehicle = Vehicle(
        id=vehicle_id,
        make=make,
        model=model,
        generation=generation,
        normalized_text=normalize_text(f"{make} {model} {generation or ''}"),
    )
    session.add(vehicle)
    return vehicle


def add_product(session: Session, product_id: str, name: str, *vehicles: Vehicle) -> Product:
    product = Product(
        id=product_id,
        name=name,
        normalized_name=normalize_text(name),
        audit_status="CONFIRMED",
        is_searchable=True,
        search_text=normalize_text(name),
    )
    for vehicle in vehicles:
        product.fitments.append(Fitment(vehicle=vehicle, source_vehicle_text=vehicle.model))
    session.add(product)
    return product


def make_engine():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        cobalt = add_vehicle(session, "V-COB", "Chevrolet", "Cobalt")
        nexia_old = add_vehicle(session, "V-N100", "Daewoo", "Nexia", "N100")
        nexia_new = add_vehicle(session, "V-N150", "Daewoo", "Nexia", "N150")
        placeholder = add_vehicle(session, "V-BYD", "BYD", "(model aniqlanmagan)")
        add_product(session, "SHOCK-N", "AMORTIZATOR ORQA", nexia_old, nexia_new)
        add_product(session, "PUMP-N", "BENZONASOS", nexia_old)
        add_product(session, "PLUG-C", "SVECHA", cobalt)
        add_product(session, "PAD-C", "KOLODKA OLDI", cobalt)
        add_product(session, "BYD-X", "FILTR", placeholder)
        plug = session.get(Product, "PLUG-C")
        plug.reference_numbers.append(
            ReferenceNumber(number="PT 43", normalized_number=normalize_code("PT 43"), type="OEM")
        )
        session.commit()
    return engine


@pytest.fixture
def session():
    with Session(make_engine()) as session:
        yield session


@pytest.fixture
def client():
    factory = sessionmaker(make_engine(), expire_on_commit=False)

    def override_session():
        with factory() as session:
            yield session

    previous = settings.pilot_mode
    settings.pilot_mode = True
    app.dependency_overrides[get_session] = override_session
    try:
        with TestClient(app) as test_client:
            test_client.factory = factory
            yield test_client
    finally:
        settings.pilot_mode = previous
        app.dependency_overrides.clear()


def test_edit_distance_counts_transpositions_and_stops_at_limit() -> None:
    assert edit_distance("amortizator", "amortizatr", 2) == 1
    assert edit_distance("datchik", "dacthik", 2) == 1
    assert edit_distance("nexia", "cobalt", 2) == 3


def test_known_words_prefixes_and_codes_are_not_corrected(session: Session) -> None:
    vocabulary = load_vocabulary(session)
    assert correct_query("amortizator orqa", vocabulary) is None
    assert correct_query("amort", vocabulary) is None
    assert correct_query("pt 43 9454449", vocabulary) is None
    assert correct_query("amortizatr oldi", vocabulary) == "amortizator oldi"


def test_misspelled_product_is_corrected(session: Session) -> None:
    response = search_products(session, "amortizatr")
    assert response.corrected_query == "amortizator"
    assert [(item.id, item.result_group) for item in response.items] == [("SHOCK-N", "EXACT")]


def test_spellcheck_can_be_disabled(session: Session) -> None:
    # Without correction only the weak whole-name fuzzy fallback is left.
    response = search_products(session, "amortizatr", spellcheck=False)
    assert response.corrected_query is None
    assert {item.result_group for item in response.items} <= {"RELATED"}


def test_strong_results_are_never_replaced_by_a_correction(session: Session) -> None:
    response = search_products(session, "PT 43")
    assert response.corrected_query is None
    assert response.items[0].id == "PLUG-C"


def test_catalog_model_names_are_recognized_and_typos_corrected(session: Session) -> None:
    exact = search_products(session, "nexia amortizator")
    assert exact.parsed_query_internal["vehicle"] == "Daewoo Nexia"
    assert [item.id for item in exact.items] == ["SHOCK-N"]

    typo = search_products(session, "Nexya amortizator")
    assert typo.corrected_query == "nexia amortizator"
    assert [item.id for item in typo.items] == ["SHOCK-N"]


def test_vehicle_filter_browses_and_narrows(session: Session) -> None:
    browse = search_products(session, "", vehicle_ids={"V-N100", "V-N150"}, vehicle_label="Nexia")
    assert browse.vehicle_filter.label == "Nexia"
    assert [item.id for item in browse.items] == ["SHOCK-N", "PUMP-N"]

    narrowed = search_products(session, "benzonasos", vehicle_ids={"V-N100"})
    assert [item.id for item in narrowed.items] == ["PUMP-N"]

    nothing = search_products(session, "svecha", vehicle_ids={"V-N100"})
    assert nothing.total == 0


def test_typed_vehicle_overrides_the_remembered_car(session: Session) -> None:
    response = search_products(session, "cobalt svecha", vehicle_ids={"V-N100"})
    assert response.vehicle_filter is None
    assert [item.id for item in response.items] == ["PLUG-C"]


def test_admin_alias_makes_an_unknown_word_searchable(session: Session) -> None:
    assert search_products(session, "pampers", spellcheck=False).total == 0
    session.add(SearchAlias(kind="product", alias="pampers", canonical="benzonasos"))
    session.add(SearchAlias(kind="vehicle", alias="cobaltik", canonical="Chevrolet Cobalt"))
    session.commit()
    assert [item.id for item in search_products(session, "pampers").items] == ["PUMP-N"]
    response = search_products(session, "cobaltik svecha")
    assert response.parsed_query_internal["vehicle"] == "Chevrolet Cobalt"
    assert [item.id for item in response.items] == ["PLUG-C"]


def test_search_api_requires_query_or_vehicle_and_logs_browsing(client: TestClient) -> None:
    assert client.get("/api/v1/search").status_code == 422
    assert client.get("/api/v1/search", params={"make": "Ford"}).status_code == 404

    response = client.get("/api/v1/search", params={"make": "Daewoo", "model": "Nexia"})
    assert response.status_code == 200
    body = response.json()
    assert body["vehicle_filter"]["label"] == "Daewoo Nexia"
    assert body["total"] == 2

    typo = client.get("/api/v1/search", params={"q": "amortizatr"}).json()
    assert typo["corrected_query"] == "amortizator"

    with client.factory() as session:
        events = session.scalars(select(SearchEvent).order_by(SearchEvent.id)).all()
    assert [event.query_normalized for event in events] == ["[daewoo nexia]", "amortizatr"]
    assert events[0].detected_vehicle == "Daewoo Nexia"


def test_vehicles_endpoint_lists_only_choosable_cars_with_parts(client: TestClient) -> None:
    vehicles = client.get("/api/v1/vehicles").json()
    assert {(row["id"], row["part_count"]) for row in vehicles} == {
        ("V-COB", 2),
        ("V-N100", 2),
        ("V-N150", 1),
    }


def test_alias_admin_api_round_trip(client: TestClient) -> None:
    admin_login(client)
    targets = client.get("/api/admin/search-aliases/targets").json()
    assert "Daewoo Nexia" in targets["vehicle"]
    assert "(model aniqlanmagan)" not in " ".join(targets["vehicle"])
    assert "shock absorber" in targets["product"]

    created = client.post(
        "/api/admin/search-aliases",
        json={
            "kind": "product",
            "alias": "Pampers",
            "canonical": "benzonasos",
            "source_query": "pampers",
        },
    )
    assert created.status_code == 201
    assert created.json()["alias"] == "pampers"
    assert created.json()["source_query_result_count"] == 1

    duplicate = client.post(
        "/api/admin/search-aliases",
        json={"kind": "product", "alias": "pampers", "canonical": "svecha"},
    )
    assert duplicate.status_code == 409

    unknown_target = client.post(
        "/api/admin/search-aliases",
        json={"kind": "vehicle", "alias": "ladushka", "canonical": "Lada Granta"},
    )
    assert unknown_target.status_code == 422

    alias_id = created.json()["id"]
    assert [row["id"] for row in client.get("/api/admin/search-aliases").json()] == [alias_id]
    assert client.delete(f"/api/admin/search-aliases/{alias_id}").status_code == 204
    assert client.get("/api/admin/search-aliases").json() == []
