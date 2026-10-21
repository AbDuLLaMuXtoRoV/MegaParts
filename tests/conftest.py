import pytest
from starlette.testclient import TestClient

from app.main import settings

TEST_ADMIN_PASSWORD = "test-admin-password"


@pytest.fixture(autouse=True)
def admin_password():
    """Every test runs with a known admin password, independent of the local .env."""
    previous = settings.admin_password
    settings.admin_password = TEST_ADMIN_PASSWORD
    yield TEST_ADMIN_PASSWORD
    settings.admin_password = previous


def admin_login(client: TestClient) -> None:
    response = client.post(
        "/api/admin/login",
        json={"username": settings.admin_username, "password": TEST_ADMIN_PASSWORD},
    )
    assert response.status_code == 200, response.text
