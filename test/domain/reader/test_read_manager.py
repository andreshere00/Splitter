import io
import os

import pytest
from fastapi import UploadFile

from src.infrastructure.model.llm_client import LLMClient
from src.domain.reader.read_manager import ReadManager
from src.domain.reader.readers.markitdown_reader import MarkItDownReader


# Fixture: use the actual test input folder.
@pytest.fixture
def temp_config():
    # Use the actual data/test/input directory.
    config_data = {
        "file_io": {"input_path": "data/test/input"},
        "ocr": {"method": "none"},
    }
    return config_data, "data/test/input"


@pytest.fixture
def read_manager(temp_config):
    config, _ = temp_config
    return ReadManager(config=config)


def test_read_valid_md_file(read_manager, temp_config):
    """Test reading a valid markdown file from disk using an existing file."""
    _, input_path = temp_config
    content = read_manager.read_file("test_1.md")
    # Check that some content is returned.
    assert content is not None
    assert isinstance(content, str)
    assert len(content) > 0


def test_read_valid_pdf_file(read_manager, temp_config):
    """Test reading a valid PDF file from disk using an existing file."""
    _, input_path = temp_config
    content = read_manager.read_file("test_1.pdf")
    assert content is not None
    assert isinstance(content, str)
    assert len(content) > 0


def test_read_valid_txt_file(read_manager, temp_config):
    """Test reading a valid TXT file from disk using an existing file."""
    _, input_path = temp_config
    content = read_manager.read_file("test_1.txt")
    assert content is not None
    assert isinstance(content, str)
    assert len(content) > 0


def test_read_file_not_found(read_manager):
    """Test that reading a non-existing file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        read_manager.read_file("nonexistent.txt")


def test_read_empty_file(temp_config):
    """Test that reading an empty file raises ValueError."""
    config, input_path = temp_config
    empty_file = "empty.txt"
    # Create an empty file.
    with open(empty_file, "w", encoding="utf-8") as f:
        f.write("")
    rm = ReadManager(config=config)
    with pytest.raises(ValueError, match="File is empty"):
        rm.read_file(empty_file)
    os.remove(empty_file)


def test_read_invalid_extension(temp_config):
    """Test that reading a file with an unsupported extension raises ValueError."""
    config, input_path = temp_config
    invalid_file = "malicious.exe"
    with open(invalid_file, "w", encoding="utf-8") as f:
        f.write("EXE file content")
    rm = ReadManager(config=config)
    with pytest.raises(ValueError, match="Unsupported file extension"):
        rm.read_file(invalid_file)
    os.remove(invalid_file)


def test_read_file_object(read_manager, temp_config):
    """Test reading from an UploadFile object using an existing PDF file."""
    _, input_path = temp_config
    file_path = os.path.join(input_path, "test_1.pdf")
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    stream = io.BytesIO(file_bytes)
    stream.name = "test_1.pdf"
    upload_file = UploadFile(filename="test_1.pdf", file=stream)
    result = read_manager.read_file_object(upload_file)
    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0


def test_markitdown_instantiation(temp_config, monkeypatch):
    """
    Test that _get_converter_for_extension instantiates a MarkItDownReader
    with non-void client and model parameters.
    """
    config, _ = temp_config

    class DummyLLMClient:
        def get_client(self):
            return "dummy_client"

        def get_model(self):
            return "dummy_model"

    # Monkey-patch LLMClient so that it returns dummy values.
    monkeypatch.setattr(LLMClient, "__init__", lambda self, method: None)
    monkeypatch.setattr(LLMClient, "get_client", lambda self: "dummy_client")
    monkeypatch.setattr(LLMClient, "get_model", lambda self: "dummy_model")

    # Set OCR method to a valid value.
    config["ocr"] = {"method": "openai"}
    rm = ReadManager(config=config)
    converter = rm._get_converter_for_extension("txt")
    assert isinstance(converter, MarkItDownReader)
    # Verify that the converter's stored parameters are not void.
    assert converter.llm_client == "dummy_client"
    assert converter.llm_model == "dummy_model"
