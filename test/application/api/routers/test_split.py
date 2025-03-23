import io
import json

from fastapi.testclient import TestClient

from src.application.api.app import app

client = TestClient(app)


# 1. Test successful response using file upload (download_zip=true)
def test_split_valid_file_upload_zip():
    # Simulate a file upload using a TXT file.
    file_content = b"This is a test document. " * 50
    file = io.BytesIO(file_content)
    file.name = "test_1.txt"

    response = client.post(
        "/documents/split",
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
        files={"file": ("test_1.txt", file, "text/plain")},
    )
    # Expect a ZIP response
    assert response.status_code == 200
    assert "application/zip" in response.headers.get("content-type", "")


# 2. Test successful response using file path (download_zip=false)
def test_split_valid_file_path_no_zip():
    test_file_path = "data/test/input/test_1.txt"

    response = client.post(
        "/documents/split",
        data={
            "document_path": test_file_path,
            "split_method": "word",
            "download_zip": "false",
            "split_params": json.dumps({"num_words": 1000}),
            "document_name": "test_1.txt",
            "metadata": "",
            "chunk_path": "data/test/output",
            "document_id": "3739202c838a3831_20250323_141321_test_1",
        },
        files={"file": ("", "", "application/octet-stream")},
    )
    assert response.status_code == 200
    data = response.json()
    assert "chunks" in data


# 3. Test that default parameters are used when split_params is an empty JSON object
def test_split_default_params():
    file_content = b"This is a test document. " * 50
    file = io.BytesIO(file_content)
    file.name = "test_1.txt"

    response = client.post(
        "/documents/split",
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
        files={"file": ("test_1.txt", file, "text/plain")},
    )
    assert response.status_code == 200
    data = response.json()
    # When empty JSON is provided, our code sets custom_split_params to None.
    assert data["split_params"] is None


# 4. Test that non-default parameters are applied
def test_split_custom_params():
    file_content = b"This is a test document. " * 50
    file = io.BytesIO(file_content)
    file.name = "test_1.txt"

    response = client.post(
        "/documents/split",
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
        files={"file": ("test_1.txt", file, "text/plain")},
    )

    print("=" * 80)
    print(response.status_code)
    print("=" * 80)
    assert response.status_code == 200
    data = response.json()
    assert data["split_params"] == {"num_words": 1000}


# 5. Test unsuccessful response with invalid parameters (e.g., negative num_words)
def test_split_invalid_params():
    file_content = b"This is a test document. " * 50
    file = io.BytesIO(file_content)
    file.name = "test_1.txt"

    response = client.post(
        "/documents/split",
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
        files={"file": ("test_1.txt", file, "text/plain")},
    )

    # Assuming your splitting logic validates and rejects negative num_words,
    # expect a 400 error.
    assert response.status_code == 400
