import datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.application.api.routers.health import router as health_router


@pytest.fixture
def app() -> FastAPI:
    """Create a FastAPI app with the health-check router attached."""
    app = FastAPI()
    app.include_router(health_router)
    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """Return a TestClient bound to the temporary FastAPI app."""
    return TestClient(app)


def test_health_check(client: TestClient) -> None:
    """Health endpoint returns 200 and a valid ISO timestamp."""
    resp = client.get("/health-check")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    datetime.datetime.fromisoformat(data["timestamp"])
