from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from app.analytics import build_analytics
from app.database import get_session
from app.main import app, settings
from app.models import Base, Brand, PilotFeedback, Product, SearchEvent, Supplier
from app.normalization import normalize_text
from tests.conftest import admin_login


def make_engine():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    return engine


def seed_catalog(session: Session) -> None:
    session.add(
        Product(
            id="P1",
            name="SVECHA",
            normalized_name="svecha",
            brand=Brand(name="NGK", normalized_name="ngk"),
            audit_status="CONFIRMED",
            is_searchable=True,
            search_text=normalize_text("svecha spark"),
        )
    )
    session.add(Supplier(name="Supplier One", normalized_name="supplier one"))
    session.commit()


def test_analytics_metrics_and_catalog_work_signals() -> None:
    engine = make_engine()
    with Session(engine) as session:
        session.add_all(
            [
                SearchEvent(
                    session_id="s1",
                    query_raw="spark plug",
                    query_normalized="spark plug",
                    result_count=4,
                    search_time_ms=12,
                    top_product_ids=["P1"],
                    clicked_product_id=None,
                    action="search",
                    feedback=PilotFeedback(
                        found_correct_part=False, correct_in_top_3=False, user_rating=2
                    ),
                ),
                SearchEvent(
                    session_id="s2",
                    query_raw="unknown",
                    query_normalized="unknown",
                    result_count=0,
                    search_time_ms=20,
                    top_product_ids=[],
                    action="search",
                ),
            ]
        )
        session.commit()
        report = build_analytics(session)

    assert report["metrics"]["total_searches"] == 2
    assert report["metrics"]["zero_result_rate"] == 50
    assert {row["normalized_query"] for row in report["needs_catalog_work"]} == {
        "spark plug",
        "unknown",
    }


def test_search_click_feedback_and_admin_api() -> None:
    engine = make_engine()
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    with factory() as session:
        seed_catalog(session)
        supplier_id = session.query(Supplier.id).scalar()

    def override_session():
        with factory() as session:
            yield session

    previous = settings.pilot_mode
    settings.pilot_mode = True
    app.dependency_overrides[get_session] = override_session
    try:
        with TestClient(app) as client:
            response = client.get("/api/v1/search", params={"q": "svecha", "session_id": "pilot-1"})
            assert response.status_code == 200
            event_id = response.json()["search_event_id"]
            assert event_id is not None
            assert "search_debug" not in response.json()

            click = client.post(f"/api/search-events/{event_id}/click", json={"product_id": "P1"})
            assert click.status_code == 200
            assert click.json()["action"] == "product_click"
            assert click.json()["result_group_distribution"]["EXACT"] >= 1
            assert click.json()["top_result_score"] is not None

            supplier = client.post(
                f"/api/search-events/{event_id}/click", json={"supplier_id": supplier_id}
            )
            assert supplier.status_code == 200

            action = client.post(
                f"/api/search-events/{event_id}/action",
                json={"action": "contact_supplier", "supplier_id": supplier_id},
            )
            assert action.status_code == 200

            phone = client.post(
                f"/api/search-events/{event_id}/action",
                json={"action": "phone_click", "supplier_id": supplier_id},
            )
            assert phone.status_code == 200

            # The part page records adding a seller's part to the basket.
            basket = client.post(
                f"/api/search-events/{event_id}/action",
                json={"action": "basket_add", "supplier_id": supplier_id},
            )
            assert basket.status_code == 200

            feedback = client.post(
                f"/api/search-events/{event_id}/feedback",
                json={
                    "found_correct_part": True,
                    "correct_in_top_3": True,
                    "user_rating": 5,
                },
            )
            assert feedback.status_code == 200

            admin_login(client)
            report = client.get("/api/admin/search-analytics", params={"period": "today"})
            assert report.status_code == 200
            assert report.json()["metrics"]["total_searches"] == 1
            assert report.json()["metrics"]["contact_supplier_conversion"] == 100
            assert report.json()["metrics"]["phone_clicks"] == 1
    finally:
        settings.pilot_mode = previous
        app.dependency_overrides.clear()
