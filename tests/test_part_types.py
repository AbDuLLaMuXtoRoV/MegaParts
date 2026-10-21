import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from app.database import get_session
from app.main import app, settings
from app.models import Base, Category, Fitment, Product, Vehicle
from app.normalization import normalize_text
from app.part_types import PART_GROUPS, ensure_standard_part_types, part_groups
from app.search import search_products


def add_product(
    session: Session,
    product_id: str,
    name: str,
    category_id: str,
    vehicle: Vehicle | None = None,
    *,
    universal: bool = False,
) -> None:
    product = Product(
        id=product_id,
        name=name,
        normalized_name=normalize_text(name),
        category_id=category_id,
        universal=universal,
        audit_status="CONFIRMED",
        is_searchable=True,
        search_text=normalize_text(name),
    )
    if vehicle:
        product.fitments.append(Fitment(vehicle=vehicle, source_vehicle_text=vehicle.model))
    session.add(product)


@pytest.fixture
def engine():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        # A workbook-defined group and type, as the importer would load them.
        session.add(Category(id="CAT-BRK", name_uz="Tormozlar", is_leaf=False))
        session.add(
            Category(id="CAT-BRK-PAD", parent_id="CAT-BRK", name_uz="Kolodka", is_leaf=True)
        )
        session.flush()
        ensure_standard_part_types(session)
        cobalt = Vehicle(
            id="V1", make="Chevrolet", model="Cobalt", normalized_text="chevrolet cobalt"
        )
        nexia = Vehicle(id="V2", make="Daewoo", model="Nexia", normalized_text="daewoo nexia")
        add_product(session, "P1", "Kolodka oldi", "CAT-BRK-PAD", cobalt)
        add_product(session, "P2", "Tormoz diski", "CAT-BRK-DISC", nexia)
        add_product(session, "P3", "Havo filtri", "CAT-FLT-AIR", cobalt)
        add_product(session, "P4", "Tormoz suyuqligi DOT4", "CAT-OIL-BRK", universal=True)
        session.commit()
    return engine


def test_standard_types_are_added_once_and_workbook_rows_win(engine) -> None:
    with Session(engine) as session:
        assert ensure_standard_part_types(session) == 0
        assert session.get(Category, "CAT-BRK").name_uz == "Tormozlar"
        disc = session.get(Category, "CAT-BRK-DISC")
        assert disc.parent_id == "CAT-BRK" and disc.is_leaf
        expected = {group.id for group in PART_GROUPS} | {
            part_type.id for group in PART_GROUPS for part_type in group.types
        }
        assert expected <= set(session.scalars(select(Category.id)))


def test_part_groups_follow_display_order_and_count_parts(engine) -> None:
    with Session(engine) as session:
        groups = part_groups(session)
    assert [group["id"] for group in groups] == [group.id for group in PART_GROUPS]
    brakes = next(group for group in groups if group["id"] == "CAT-BRK")
    assert brakes["part_count"] == 2
    counts = {part_type["id"]: part_type["part_count"] for part_type in brakes["types"]}
    assert counts["CAT-BRK-PAD"] == 1 and counts["CAT-BRK-DISC"] == 1
    assert next(group for group in groups if group["id"] == "CAT-STR")["part_count"] == 0


def test_part_group_counts_for_a_car_include_universal_parts(engine) -> None:
    with Session(engine) as session:
        groups = {group["id"]: group for group in part_groups(session, {"V1"})}
    assert groups["CAT-BRK"]["part_count"] == 1  # the Nexia brake disc does not fit
    assert groups["CAT-FLT"]["part_count"] == 1
    assert groups["CAT-OIL"]["part_count"] == 1  # brake fluid fits every car


def test_browse_a_part_group_without_typing(engine) -> None:
    with Session(engine) as session:
        brake_ids = {"CAT-BRK", "CAT-BRK-PAD", "CAT-BRK-DISC"}
        response = search_products(session, "", category_ids=brake_ids)
        assert [item.id for item in response.items] == ["P1", "P2"]
        assert response.items[0].category.id == "CAT-BRK-PAD"

        both = search_products(session, "", vehicle_ids={"V1"}, category_ids=brake_ids)
        assert [item.id for item in both.items] == ["P1"]


def test_car_browse_lists_fitted_parts_before_universal_ones(engine) -> None:
    with Session(engine) as session:
        response = search_products(session, "", vehicle_ids={"V1"})
    assert [item.id for item in response.items] == ["P3", "P1", "P4"]
    assert response.items[-1].universal is True


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
            yield test_client
    finally:
        settings.pilot_mode = previous
        app.dependency_overrides.clear()


def test_part_groups_and_category_search_api(client) -> None:
    groups = client.get("/api/v1/part-groups", params={"make": "Chevrolet"}).json()
    assert groups[0]["id"] == "CAT-ENG"
    assert {"name_uz", "name_ru", "name_en", "part_count", "types"} <= groups[0].keys()

    response = client.get("/api/v1/search", params={"category": "CAT-BRK"})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["category_filter"]["name_uz"] == "Tormozlar"

    typed = client.get("/api/v1/search", params={"q": "kolodka", "category": "CAT-FLT"})
    assert typed.json()["total"] == 0

    assert client.get("/api/v1/search", params={"category": "CAT-NOPE"}).status_code == 404
    assert client.get("/api/v1/search").status_code == 422
