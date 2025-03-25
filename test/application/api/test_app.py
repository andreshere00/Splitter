from fastapi.testclient import TestClient

from src.application.api.app import app

client = TestClient(app)


def test_root():
    """
    Test the root endpoint to verify that the API is running.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Document Splitter API is running"}
