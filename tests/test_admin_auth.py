import re

import pytest
from fastapi.routing import APIRoute
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from app.auth import COOKIE_NAME, MAX_FAILED_LOGINS, is_admin_path, issue_session, session_user
from app.database import get_session
from app.main import app, login_throttle, settings
from app.models import Base
from tests.conftest import TEST_ADMIN_PASSWORD


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(engine)

    def override_session():
        with factory() as session:
            yield session

    previous = settings.pilot_mode
    settings.pilot_mode = True
    app.dependency_overrides[get_session] = override_session
    login_throttle.reset("testclient")
    try:
        with TestClient(app, follow_redirects=False) as test_client:
            yield test_client
    finally:
        settings.pilot_mode = previous
        app.dependency_overrides.clear()
        login_throttle.reset("testclient")


def admin_routes() -> list[tuple[str, str]]:
    routes = []
    for route in app.routes:
        if isinstance(route, APIRoute) and is_admin_path(re.sub(r"\{[^}]+\}", "1", route.path)):
            for method in route.methods:
                routes.append((method, re.sub(r"\{[^}]+\}", "1", route.path)))
    return routes


def test_every_admin_route_is_locked_without_login(client: TestClient) -> None:
    routes = admin_routes()
    assert len(routes) >= 12
    for method, path in routes:
        response = client.request(method, path)
        if path.startswith("/api/"):
            assert response.status_code == 401, (method, path)
        else:
            assert response.status_code == 303, (method, path)
            assert response.headers["location"].startswith("/admin/login?next=")


def test_login_unlocks_admin_and_logout_locks_it_again(client: TestClient) -> None:
    page = client.get("/admin/search-analytics")
    assert page.headers["location"] == "/admin/login?next=/admin/search-analytics"
    assert client.get("/admin/login").status_code == 200

    response = client.post(
        "/api/admin/login", json={"username": "irizon", "password": TEST_ADMIN_PASSWORD}
    )
    assert response.status_code == 200
    cookie_header = response.headers["set-cookie"].lower()
    assert "httponly" in cookie_header and "samesite=lax" in cookie_header

    assert client.get("/api/admin/me").json() == {"username": "irizon"}
    assert client.get("/api/admin/search-aliases").status_code == 200
    assert client.get("/admin/search-analytics").status_code == 200
    assert client.get("/admin/login").headers["location"] == "/admin/catalog"

    assert client.post("/api/admin/logout").status_code == 204
    assert client.get("/api/admin/search-aliases").status_code == 401


def test_public_pages_stay_public(client: TestClient) -> None:
    assert client.get("/").status_code == 200
    assert client.get("/api/v1/vehicles").status_code == 200
    assert client.get("/api/pilot-config").status_code == 200


def test_wrong_credentials_are_rejected_then_throttled(client: TestClient) -> None:
    for attempt in range(MAX_FAILED_LOGINS):
        response = client.post(
            "/api/admin/login", json={"username": "irizon", "password": f"guess-{attempt}"}
        )
        assert response.status_code == 401
    wrong_user = client.post(
        "/api/admin/login", json={"username": "admin", "password": TEST_ADMIN_PASSWORD}
    )
    assert wrong_user.status_code == 429
    locked = client.post(
        "/api/admin/login", json={"username": "irizon", "password": TEST_ADMIN_PASSWORD}
    )
    assert locked.status_code == 429
    assert int(locked.headers["retry-after"]) > 0


def test_forged_expired_and_stale_sessions_are_rejected(client: TestClient) -> None:
    token = issue_session(settings)
    assert session_user(settings, token) == "irizon"

    username, expires, signature = token.split("|")
    assert session_user(settings, f"{username}|{int(expires) + 999999}|{signature}") is None
    assert session_user(settings, f"admin|{expires}|{signature}") is None
    assert session_user(settings, "garbage") is None
    assert session_user(settings, token, now=int(expires) + 1) is None

    client.cookies.set(COOKIE_NAME, token)
    assert client.get("/api/admin/me").status_code == 200
    settings.admin_password = "rotated-password"  # restored by the conftest fixture
    assert client.get("/api/admin/me").status_code == 401


def test_admin_stays_locked_when_no_password_is_configured(client: TestClient) -> None:
    settings.admin_password = ""  # restored by the conftest fixture
    response = client.post("/api/admin/login", json={"username": "irizon", "password": "x"})
    assert response.status_code == 503
    assert client.get("/api/admin/search-aliases").status_code == 401
