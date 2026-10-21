from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models import (
    Base,
    Brand,
    Fitment,
    Product,
    ReferenceNumber,
    Supplier,
    SupplierOffer,
    Vehicle,
)
from app.normalization import normalize_code, normalize_text
from app.search import get_product_detail, search_products


def make_session() -> Session:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    return Session(engine)


def seed(session: Session, *, conflict: bool = False) -> Product:
    brand = Brand(name="BOSKOS", normalized_name="boskos")
    supplier = Supplier(name="KOREA Distributor", normalized_name="korea distributor")
    vehicle = Vehicle(id="V1", make="Chevrolet", model="Cobalt", normalized_text="chevrolet cobalt")
    product = Product(
        id="P1",
        name="AMORTIZATOR OLDI LH",
        normalized_name=normalize_text("AMORTIZATOR OLDI LH"),
        brand=brand,
        position="Front",
        side="Left",
        audit_status="CONFLICT" if conflict else "CONFIRMED",
        is_searchable=not conflict,
        search_text=normalize_text("AMORTIZATOR OLDI LH BOSKOS Chevrolet Cobalt ABS PT 43"),
    )
    product.reference_numbers.append(
        ReferenceNumber(number="94544449", normalized_number="94544449", type="ARTICLE")
    )
    product.fitments.append(Fitment(vehicle=vehicle, source_vehicle_text="COBALT"))
    product.supplier_offers.append(
        SupplierOffer(
            source_offer_id="O1",
            supplier=supplier,
            supplier_sku="PT 43",
            normalized_supplier_sku=normalize_code("PT 43"),
            price=100_000,
            stock_qty=2,
            data_status="DEMO",
        )
    )
    session.add(product)
    session.commit()
    return product


def test_exact_reference_and_normalized_supplier_code() -> None:
    with make_session() as session:
        seed(session)
        assert search_products(session, "94544449").items[0].id == "P1"
        result = search_products(session, "PT43")
        assert result.items[0].id == "P1"
        assert result.items[0].relevance_score >= 90


def test_combination_search_uses_vehicle_position_and_side_aliases() -> None:
    with make_session() as session:
        seed(session)
        result = search_products(session, "Cobalt amortizator oldi LH")
        assert result.total == 1
        assert result.items[0].position == "Front"
        assert result.items[0].side == "Left"


def test_conflicted_master_product_is_quarantined() -> None:
    with make_session() as session:
        seed(session, conflict=True)
        assert search_products(session, "94544449").total == 0
        assert get_product_detail(session, "P1") is None


def test_product_detail_contains_fitments_and_supplier_offers() -> None:
    with make_session() as session:
        seed(session)
        detail = get_product_detail(session, "P1")
        assert detail is not None
        assert detail.vehicle_fitments[0].vehicle.model == "Cobalt"
        assert detail.supplier_offers[0].supplier.name == "KOREA Distributor"
