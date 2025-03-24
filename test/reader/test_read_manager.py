import os
from unittest.mock import MagicMock

import pytest

from src.reader.read_manager import ReadManager


@pytest.fixture
def temp_config(tmp_path):
    """Creates a temporary config dictionary for testing."""
    config_data = {
        "file_io": {"input_path": str(tmp_path)},
        "logging": {"enabled": False},
    }
    return config_data, str(tmp_path)


@pytest.fixture
def read_manager(temp_config):
    """Creates a ReadManager instance with test config and a dummy converter."""
    config, _ = temp_config
    # Create a dummy markdown converter.
    dummy_converter = MagicMock()
    dummy_converter.convert.return_value.text_content = "Converted Markdown"
    return ReadManager(config=config, markdown_converter=dummy_converter)


def create_test_file(directory, filename, content="test content"):
    """Helper function to create test files."""
    file_path = os.path.join(directory, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    return file_path


def test_read_valid_docx_file(read_manager, temp_config):
    """Test reading a valid docx file."""
    _, input_path = temp_config
    create_test_file(input_path, "tmp/test_1.docx", "Converted Markdown")
    content = read_manager.read_file("tmp/test_1.docx")
    assert content == "Converted Markdown"


def test_read_valid_md_file(read_manager, temp_config):
    """Test reading a valid md file."""
    _, input_path = temp_config
    create_test_file(input_path, "tmp/test_1.md", "Converted Markdown")
    content = read_manager.read_file("tmp/test_1.md")
    assert content == "Converted Markdown"


def test_read_valid_pdf_file(read_manager, temp_config):
    """Test reading a valid pdf file."""
    _, input_path = temp_config
    create_test_file(input_path, "tmp/test_1.pdf", "Converted Markdown")
    content = read_manager.read_file("tmp/test_1.pdf")
    assert content == "Converted Markdown"


def test_read_valid_txt_file(read_manager, temp_config):
    """Test reading a valid txt file."""
    _, input_path = temp_config
    create_test_file(input_path, "tmp/test_1.txt", "Converted Markdown")
    content = read_manager.read_file("tmp/test_1.txt")
    assert content == "Converted Markdown"


def test_read_valid_pptx_file(read_manager, temp_config):
    """Test reading a valid pptx file."""
    _, input_path = temp_config
    create_test_file(input_path, "tmp/test_1.pptx", "Converted Markdown")
    content = read_manager.read_file("tmp/test_1.pptx")
    assert content == "Converted Markdown"


def test_read_valid_xlsx_file(read_manager, temp_config):
    """Test reading a valid xlsx file."""
    _, input_path = temp_config
    create_test_file(input_path, "tmp/test_1.xlsx", "Converted Markdown")
    content = read_manager.read_file("tmp/test_1.xlsx")
    assert content == "Converted Markdown"


def test_read_from_non_existing_folder(read_manager):
    """Test reading from a non-existing file."""
    with pytest.raises(FileNotFoundError):
        read_manager.read_file("nonexistent.txt")


def test_read_from_empty_file(read_manager, temp_config):
    """Test reading from an empty file."""
    _, input_path = temp_config
    create_test_file(input_path, "empty.md", "")
    with pytest.raises(ValueError, match="File is empty"):
        read_manager.read_file("empty.md")


def test_read_invalid_extension(read_manager, temp_config):
    """Test reading from a file with an invalid extension."""
    _, input_path = temp_config
    create_test_file(input_path, "malicious.exe", "EXE file content")
    with pytest.raises(ValueError, match="Invalid file extension"):
        read_manager.read_file("malicious.exe")
