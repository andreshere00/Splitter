import json
import os

import pytest
from fastapi.testclient import TestClient

# dummy env so Settings() passes before "app" import
os.environ.setdefault("AZURE_OPENAI_API_KEY", "dummy")
os.environ.setdefault("AZURE_OPENAI_API_VERSION", "2024-04-15")
os.environ.setdefault("AZURE_OPENAI_ENDPOINT", "https://example.com")
os.environ.setdefault("AZURE_OPENAI_DEPLOYMENT", "dummy")
os.environ.setdefault("OPENAI_API_KEY", "dummy")
os.environ.setdefault("OPENAI_MODEL", "dummy")

from src.application.api.app import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_split_valid_file_upload_zip(client):
    with open("data/test/input/test_1.pdf", "rb") as fh:
        r = client.post(
            "/split",
            data={
                "document_path": "data/test/input",
                "split_method": "word",
                "download_zip": "true",
                "split_params": json.dumps({"num_words": 1000}),
                "ocr_method": "none",
                "conversion_method": "none",
                "document_name": "",
                "metadata": "",
                "chunk_path": "data/test/output",
                "document_id": "",
                "reader_method": "markitdown",
            },
            files={"file": ("test_1.pdf", fh, "application/pdf")},
        )
    assert r.status_code == 200
    assert "application/zip" in r.headers.get("content-type", "")


def test_split_valid_file_path_no_zip(client):
    with open("data/test/input/test_1.pdf", "rb") as fh:
        r = client.post(
            "/split",
            data={
                "document_path": "data/test/input",
                "split_method": "word",
                "download_zip": "false",
                "split_params": json.dumps({"num_words": 1000}),
                "ocr_method": "none",
                "conversion_method": "none",
                "document_name": "",
                "metadata": "",
                "chunk_path": "data/test/output",
                "document_id": "",
                "reader_method": "markitdown",
            },
            files={"file": ("test_1.pdf", fh, "application/pdf")},
        )
    assert r.status_code == 200
    assert "chunks" in r.json()


def test_split_default_params(client):
    with open("data/test/input/test_1.pdf", "rb") as fh:
        r = client.post(
            "/split",
            data={
                "document_path": "data/test/input",
                "split_method": "word",
                "download_zip": "false",
                "split_params": json.dumps({}),
                "ocr_method": "none",
                "conversion_method": "none",
                "document_name": "",
                "metadata": "",
                "chunk_path": "data/test/output",
                "document_id": "",
                "reader_method": "markitdown",
            },
            files={"file": ("test_1.pdf", fh, "application/pdf")},
        )
    assert r.status_code == 200
    assert r.json()["split_params"] is None


def test_split_custom_params(client):
    with open("data/test/input/test_1.pdf", "rb") as fh:
        r = client.post(
            "/split",
            data={
                "document_path": "data/test/input",
                "split_method": "word",
                "download_zip": "false",
                "split_params": json.dumps({"num_words": 1000}),
                "ocr_method": "none",
                "conversion_method": "none",
                "document_name": "",
                "metadata": "",
                "chunk_path": "data/test/output",
                "document_id": "",
                "reader_method": "markitdown",
            },
            files={"file": ("test_1.pdf", fh, "application/pdf")},
        )
    assert r.status_code == 200
    assert r.json()["split_params"] == {"num_words": 1000}


def test_split_invalid_params(client):
    with open("data/test/input/test_1.pdf", "rb") as fh:
        r = client.post(
            "/split",
            data={
                "document_path": "data/test/input",
                "split_method": "word",
                "download_zip": "false",
                "split_params": json.dumps({"num_words": -58}),
                "ocr_method": "none",
                "conversion_method": "none",
                "document_name": "",
                "metadata": "",
                "chunk_path": "data/test/output",
                "document_id": "",
                "reader_method": "markitdown",
            },
            files={"file": ("test_1.pdf", fh, "application/pdf")},
        )
    assert r.status_code == 400
