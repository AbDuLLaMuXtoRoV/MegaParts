from datetime import UTC, datetime, timedelta
from io import BytesIO

import pytest
from openpyxl import Workbook
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from app.database import get_session
from app.main import app
from app.models import (
    Base,
    OfferImportReview,
    Product,
    Supplier,
    SupplierOffer,
    SupplierProductMapping,
)
from app.normalization import normalize_code
from app.offers import active_sorted_offers, freshness_status
from app.search import get_product_detail, search_products
from app.supplier_import import import_supplier_workbook


def make_engine():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    return engine


def workbook_bytes(rows: list[list[object]]) -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["supplier_sku", "price", "stock", "warehouse"])
    for row in rows:
        sheet.append(row)
    output = BytesIO()
    workbook.save(output)
    return output.getvalue()


def seed(session: Session) -> tuple[Supplier, Product]:
    supplier = Supplier(name="Pilot Supplier", normalized_name="pilot supplier")
    product = Product(
        id="P1",
        name="SVECHA",
        normalized_name="svecha",
        audit_status="CONFIRMED",
        is_searchable=True,
        search_text="svecha cobalt",
    )
    session.add_all([supplier, product])
    session.commit()
    return supplier, product


def test_import_matches_confirmed_sku_and_queues_unmatched_without_creating_product() -> None:
    engine = make_engine()
    with Session(engine) as session:
        supplier, product = seed(session)
        session.add(
            SupplierProductMapping(
                supplier_id=supplier.id,
                product_id=product.id,
                supplier_sku="SP 10",
                normalized_supplier_sku=normalize_code("SP 10"),
                mapping_type="MANUAL",
                is_confirmed=True,
            )
        )
        session.commit()

        batch = import_supplier_workbook(
            session,
            supplier,
            workbook_bytes([["SP 10", None, None, "Main"], ["UNKNOWN", 25_000, 2, None]]),
            "offers.xlsx",
        )
        session.commit()

        assert batch.rows_received == 2
        assert batch.rows_matched == 1
        assert batch.unmatched_rows == 1
        assert batch.new_offers == 1
        offer = session.query(SupplierOffer).one()
        assert offer.product_id == "P1"
        assert offer.price is None
        assert offer.stock_qty is None
        assert offer.data_status == "LIVE"
        assert session.query(OfferImportReview).one().supplier_sku == "UNKNOWN"
        assert session.query(Product).count() == 1


def test_duplicate_active_offer_for_same_supplier_product_sku_is_rejected() -> None:
    engine = make_engine()
    with Session(engine) as session:
        supplier, product = seed(session)
        values = {
            "supplier_id": supplier.id,
            "product_id": product.id,
            "supplier_sku": "PT 43",
            "normalized_supplier_sku": "PT43",
            "is_active": True,
        }
        session.add(SupplierOffer(source_offer_id="O1", **values))
        session.commit()
        session.add(SupplierOffer(source_offer_id="O2", **values))
        with pytest.raises(IntegrityError):
            session.commit()


def test_offer_sorting_and_product_response_use_stock_freshness_then_price() -> None:
    engine = make_engine()
    with Session(engine) as session:
        supplier, product = seed(session)
        second_supplier = Supplier(name="Second Supplier", normalized_name="second supplier")
        session.add(second_supplier)
        fresh = datetime.now(UTC) - timedelta(minutes=20)
        stale = datetime.now(UTC) - timedelta(days=2)
        product.supplier_offers.extend(
            [
                SupplierOffer(
                    source_offer_id="STALE",
                    supplier=supplier,
                    supplier_sku="A",
                    normalized_supplier_sku="A",
                    price=10,
                    stock_qty=4,
                    updated_at=stale,
                ),
                SupplierOffer(
                    source_offer_id="FRESH",
                    supplier=second_supplier,
                    supplier_sku="B",
                    normalized_supplier_sku="B",
                    price=20,
                    stock_qty=2,
                    updated_at=fresh,
                ),
                SupplierOffer(
                    source_offer_id="ZERO",
                    supplier=supplier,
                    supplier_sku="C",
                    normalized_supplier_sku="C",
                    price=1,
                    stock_qty=0,
                    updated_at=datetime.now(UTC),
                ),
            ]
        )
        session.commit()
        assert active_sorted_offers(product.supplier_offers)[0].source_offer_id == "FRESH"
        assert freshness_status(stale) == "STALE"
        detail = get_product_detail(session, product.id)
        assert detail is not None
        assert detail.offers[0].supplier_sku == "B"
        assert detail.offers[0].freshness_status == "FRESH"
        assert detail.offers[-1].supplier_sku == "C"
        assert {offer.supplier.name for offer in detail.offers} == {
            "Pilot Supplier",
            "Second Supplier",
        }
        search_result = search_products(session, "svecha")
        assert len(search_result.items[0].offers) == 3


def test_reservation_api_validates_product_offer_pair() -> None:
    engine = make_engine()
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    with factory() as session:
        supplier, product = seed(session)
        offer = SupplierOffer(
            source_offer_id="O1",
            supplier_id=supplier.id,
            product_id=product.id,
            supplier_sku="SP10",
            normalized_supplier_sku="SP10",
        )
        session.add(offer)
        session.commit()
        offer_id = offer.id

    def override_session():
        with factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_session
    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/reservations",
                json={
                    "session_id": "pilot-1",
                    "product_id": "P1",
                    "supplier_offer_id": offer_id,
                    "quantity": 2,
                },
            )
            assert response.status_code == 201
            assert response.json()["quantity"] == 2
            mismatch = client.post(
                "/api/v1/reservations",
                json={
                    "session_id": "pilot-1",
                    "product_id": "WRONG",
                    "supplier_offer_id": offer_id,
                    "quantity": 1,
                },
            )
            assert mismatch.status_code == 404
    finally:
        app.dependency_overrides.clear()
