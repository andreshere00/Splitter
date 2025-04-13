import os

import pytest

from src.domain.reader.readers.textract_reader import TextractReader


# A dummy client to simulate Textract's DetectDocumentText API responses.
class DummyClient:
    def __init__(self, response=None, raise_exception=False):
        """
        Args:
            response (dict): A dictionary simulating Textract's response.
            raise_exception (bool): If True, detect_document_text will raise an Exception.
        """
        self.response = response
        self.raise_exception = raise_exception

    def detect_document_text(self, Document):
        if self.raise_exception:
            raise Exception("Simulated Textract failure")
        return self.response


class TestTextractReader:
    def test_convert_with_text_blocks(self, tmp_path):
        """
        Test that TextractReader extracts text and groups it by page into Markdown format.
        """
        # Create a temporary file
        dummy_file = tmp_path / "dummy.pdf"
        dummy_file.write_bytes(b"dummy content")

        # Prepare a fake Textract response with text blocks
        response = {
            "Blocks": [
                {"BlockType": "LINE", "Page": 1, "Text": "Hello from page 1"},
                {"BlockType": "LINE", "Page": 1, "Text": "Another line on page 1"},
                {"BlockType": "LINE", "Page": 2, "Text": "Hello from page 2"},
                # A non-LINE block that should be ignored.
                {"BlockType": "WORD", "Page": 2, "Text": "Ignored word"},
            ]
        }
        dummy_client = DummyClient(response=response)
        reader = TextractReader(client=dummy_client)
        result = reader.convert(str(dummy_file))

        # Check that the document header is present.
        expected_header = f"# Document: {dummy_file.name}"
        assert expected_header in result
        # Verify pages and text lines
        assert "## Page 1" in result
        assert "Hello from page 1" in result
        assert "Another line on page 1" in result
        assert "## Page 2" in result
        assert "Hello from page 2" in result
        # Ensure the ignored block did not add extra content.
        assert "Ignored word" not in result

    def test_convert_no_text(self, tmp_path):
        """
        Test that when no LINE blocks are detected, the output indicates no text was found.
        """
        dummy_file = tmp_path / "dummy.pdf"
        dummy_file.write_bytes(b"dummy content")
        # Fake response with no detected LINE blocks.
        response = {"Blocks": []}
        dummy_client = DummyClient(response=response)
        reader = TextractReader(client=dummy_client)
        result = reader.convert(str(dummy_file))
        assert "No text detected." in result

    def test_convert_failure(self, tmp_path):
        """
        Test that TextractReader.convert raises a RuntimeError when the Textract API call fails.
        """
        dummy_file = tmp_path / "dummy.pdf"
        dummy_file.write_bytes(b"dummy content")
        # Configure the dummy client to simulate a failure.
        dummy_client = DummyClient(raise_exception=True)
        reader = TextractReader(client=dummy_client)
        with pytest.raises(RuntimeError, match="Textract detect_document_text failed"):
            reader.convert(str(dummy_file))
