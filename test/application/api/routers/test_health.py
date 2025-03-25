import datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.application.api.routers.health import router as health_router


@pytest.fixture
def app() -> FastAPI:
    """Create a FastAPI app with the health-check router included."""
    app = FastAPI()
    app.include_router(health_router)
    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """Create a TestClient using the FastAPI app."""
    return TestClient(app)


def test_health_check(client: TestClient) -> None:
    """
    Test the health-check endpoint.

    Verifies that the response status code is 200, that the response JSON contains a "status"
    field equal to "ok", and that the "timestamp" field is a valid ISO formatted datetime string.
    """
    response = client.get("/health-check")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "ok"
    timestamp = data.get("timestamp")
    assert timestamp is not None
    # Verify that the timestamp can be parsed as an ISO formatted datetime.
    datetime.datetime.fromisoformat(timestamp)
