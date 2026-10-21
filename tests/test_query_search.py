import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models import (
    Base,
    Fitment,
    Product,
    ReferenceNumber,
    Supplier,
    SupplierOffer,
    Vehicle,
)
from app.normalization import normalize_code, normalize_text
from app.query_parser import parse_query
from app.search import search_products


def add_product(
    session: Session,
    product_id: str,
    name: str,
    vehicle_id: str,
    vehicle_model: str,
    *,
    position: str | None = None,
    side: str | None = None,
) -> Product:
    vehicle = Vehicle(
        id=vehicle_id,
        make="Chevrolet",
        model=vehicle_model,
        normalized_text=normalize_text(f"Chevrolet {vehicle_model}"),
    )
    product = Product(
        id=product_id,
        name=name,
        normalized_name=normalize_text(name),
        position=position,
        side=side,
        audit_status="CONFIRMED",
        is_searchable=True,
        search_text=normalize_text(f"{name} Chevrolet {vehicle_model} {position} {side}"),
    )
    product.fitments.append(Fitment(vehicle=vehicle, source_vehicle_text=vehicle_model))
    session.add(product)
    return product


@pytest.fixture
def catalog() -> Session:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    session = Session(engine)
    supplier = Supplier(name="Pilot Supplier", normalized_name="pilot supplier")

    cobalt_plug = add_product(session, "PLUG-C", "SVECHA", "VC", "Cobalt")
    add_product(session, "PLUG-M", "Свеча зажигания", "VM", "Matiz")
    add_product(session, "SHOCK-R", "AMORTIZATOR ORQA", "VN1", "Nexia 3", position="Rear")
    for number in range(2, 7):
        add_product(
            session,
            f"SHOCK-R{number}",
            f"AMORTIZATOR ORQA {number}",
            f"VN-R{number}",
            "Nexia 3",
            position="Rear",
        )
    add_product(session, "SHOCK-F", "AMORTIZATOR OLDI", "VN2", "Nexia 3", position="Front")
    add_product(
        session, "ABS-L", "ABC DACHCHIK OLDI LH", "VA1", "Cobalt", position="Front", side="Left"
    )
    add_product(
        session, "ABS-R", "ABC DACHCHIK OLDI RH", "VA2", "Cobalt", position="Front", side="Right"
    )
    add_product(session, "SHOCK-CR", "AMORTIZATOR ORQA", "VCR", "Cobalt", position="Rear")
    add_product(session, "SHOCK-CF", "AMORTIZATOR OLDI", "VCF", "Cobalt", position="Front")
    add_product(session, "PUMP-S", "BENZIN NASOS", "VS-P", "Spark")
    add_product(session, "PUMP-C", "BENZIN NASOS", "VC-P", "Cobalt")
    cobalt_plug.reference_numbers.append(
        ReferenceNumber(number="94544449", normalized_number="94544449", type="ARTICLE")
    )
    cobalt_plug.supplier_offers.extend(
        [
            SupplierOffer(
                source_offer_id="O-PT",
                supplier=supplier,
                supplier_sku="PT 43",
                normalized_supplier_sku=normalize_code("PT 43"),
            ),
            SupplierOffer(
                source_offer_id="O-B",
                supplier=supplier,
                supplier_sku="0788B",
                normalized_supplier_sku=normalize_code("0788B"),
            ),
        ]
    )
    session.commit()
    yield session
    session.close()


@pytest.mark.parametrize(
    "query",
    ["свеча cobalt", "свеча cobalt\\", "svecha cobalt", "Cobalt svecha"],
)
def test_product_and_vehicle_intents_are_independent(catalog: Session, query: str) -> None:
    result = search_products(catalog, query)
    assert result.total >= 1
    assert result.items[0].id == "PLUG-C"


def test_trailing_noise_returns_same_logical_results(catalog: Session) -> None:
    clean = search_products(catalog, "свеча cobalt")
    noisy = search_products(catalog, "свеча cobalt\\")
    assert [(item.id, item.result_group) for item in clean.items] == [
        (item.id, item.result_group) for item in noisy.items
    ]


def test_single_product_term_expands_across_scripts(catalog: Session) -> None:
    result = search_products(catalog, "свеча")
    assert {item.id for item in result.items} >= {"PLUG-C", "PLUG-M"}


@pytest.mark.parametrize("query", ["94544449", "PT43", "PT 43", "0788B"])
def test_exact_reference_and_supplier_codes_remain_highest_priority(
    catalog: Session, query: str
) -> None:
    result = search_products(catalog, query)
    assert result.items[0].id == "PLUG-C"
    assert result.items[0].relevance_score >= 150
    assert result.items[0].result_group == "EXACT"


def test_vehicle_position_and_side_ranking(catalog: Session) -> None:
    assert search_products(catalog, "Nexia 3 amortizator").items[0].id in {
        "SHOCK-R",
        "SHOCK-F",
    }
    rear = search_products(catalog, "Nexia 3 amortizator orqa")
    assert all(item.result_group == "EXACT" for item in rear.items[:5])
    assert all(item.position == "Rear" for item in rear.items[:5])
    assert all(
        any("nexia 3" in fitment.vehicle.model.casefold() for fitment in item.vehicle_fitments)
        for item in rear.items
    )
    front = search_products(catalog, "Nexia 3 amortizator oldi")
    assert front.items[0].id == "SHOCK-F"
    assert front.items[0].result_group == "EXACT"
    cobalt_rear = search_products(catalog, "Cobalt amortizator orqa")
    assert cobalt_rear.items[0].id == "SHOCK-CR"
    assert cobalt_rear.items[0].result_group == "EXACT"
    assert search_products(catalog, "Cobalt ABS oldi LH").items[0].id == "ABS-L"
    assert search_products(catalog, "Cobalt ABS oldi RH").items[0].id == "ABS-R"
    assert search_products(catalog, "Spark benzin nasos").items[0].id == "PUMP-S"


def test_development_debug_has_normalized_score_components(catalog: Session) -> None:
    result = search_products(catalog, "Cobalt ABS oldi LH", include_debug=True)
    debug = result.search_debug["scoring"][result.items[0].id]
    assert debug["total_score"] == result.items[0].relevance_score
    assert debug["product_score"] > 0
    assert debug["vehicle_fitment_score"] > 0
    assert debug["position_score"] > 0
    assert debug["side_score"] > 0
    assert debug["result_group"] == "EXACT"


def test_parser_exposes_structured_intents() -> None:
    parsed = parse_query("Cobalt ABS oldi LH")
    assert parsed.vehicle == "Chevrolet Cobalt"
    assert parsed.product_terms == ["abs"]
    assert parsed.position == "front"
    assert parsed.side == "left"
