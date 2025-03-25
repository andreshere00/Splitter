import json

import pytest
from fastapi.testclient import TestClient

from src.application.api.app import app


# Use a fixture to initialize the FastAPI server and ensure startup/shutdown events are triggered.
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


# 1. Test successful response using file upload (download_zip=true)
def test_split_valid_file_upload_zip(client):
    # Load the PDF file from the folder "data/test/input"
    with open("data/test/input/test_1.pdf", "rb") as file:
        response = client.post(
            "/split",
            data={
                "document_path": "data/test/input",
                "split_method": "word",
                "download_zip": "true",
                "split_params": json.dumps({"num_words": 1000}),
                "document_name": "",
                "metadata": "",
                "chunk_path": "data/test/output",
                "document_id": "",
            },
            files={"file": ("test_1.pdf", file, "application/pdf")},
        )
    # Expect a ZIP response
    assert response.status_code == 200
    assert "application/zip" in response.headers.get("content-type", "")


# 2. Test successful response using file path (download_zip=false)
def test_split_valid_file_path_no_zip(client):
    with open("data/test/input/test_1.pdf", "rb") as file:
        response = client.post(
            "/split",
            data={
                "document_path": "data/test/input",
                "split_method": "word",
                "download_zip": "false",
                "split_params": json.dumps({"num_words": 1000}),
                "document_name": "",
                "metadata": "",
                "chunk_path": "data/test/output",
                "document_id": "",
            },
            files={"file": ("test_1.pdf", file, "application/pdf")},
        )
    assert response.status_code == 200
    data = response.json()
    assert "chunks" in data


# 3. Test that default parameters are used when split_params is an empty JSON object
def test_split_default_params(client):
    with open("data/test/input/test_1.pdf", "rb") as file:
        response = client.post(
            "/split",
            data={
                "document_path": "data/test/input",
                "split_method": "word",
                "download_zip": "false",
                "split_params": json.dumps({}),  # empty JSON
                "document_name": "",
                "metadata": "",
                "chunk_path": "data/test/output",
                "document_id": "",
            },
            files={"file": ("test_1.pdf", file, "application/pdf")},
        )
    assert response.status_code == 200
    data = response.json()
    # When empty JSON is provided, our code sets custom_split_params to None.
    assert data["split_params"] is None


# 4. Test that non-default parameters are applied
def test_split_custom_params(client):
    with open("data/test/input/test_1.pdf", "rb") as file:
        response = client.post(
            "/split",
            data={
                "document_path": "data/test/input",
                "split_method": "word",
                "download_zip": "false",
                "split_params": json.dumps({"num_words": 1000}),
                "document_name": "",
                "metadata": "",
                "chunk_path": "data/test/output",
                "document_id": "",
            },
            files={"file": ("test_1.pdf", file, "application/pdf")},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["split_params"] == {"num_words": 1000}


# 5. Test unsuccessful response with invalid parameters (e.g., negative num_words)
def test_split_invalid_params(client):
    with open("data/test/input/test_1.pdf", "rb") as file:
        response = client.post(
            "/split",
            data={
                "document_path": "data/test/input",
                "split_method": "word",
                "download_zip": "false",
                "split_params": json.dumps({"num_words": -58}),
                "document_name": "",
                "metadata": "",
                "chunk_path": "data/test/output",
                "document_id": "",
            },
            files={"file": ("test_1.pdf", file, "application/pdf")},
        )
    # Assuming your splitting logic validates and rejects negative num_words,
    # expect a 400 error.
    assert response.status_code == 400
