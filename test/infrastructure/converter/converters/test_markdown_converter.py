from pathlib import Path

import pytest

from src.infrastructure.converter.base_converter import ConversionError
from src.infrastructure.converter.converters.markdown_converter import MarkdownConverter

# Directory containing test input files
DATA_DIR = Path(__file__).parents[4] / "data" / "test" / "input"

# Supported formats (Markdown output)
SUPPORTED_FILES = [
    "test_1.txt",
    "test_1.pdf",
    "test_1.html",
    "test_1.xml",
    "test_1.xlsx",
]

# Unsupported formats should raise ConversionError
UNSUPPORTED_FILES = [
    "empty.txt",  # plain text but empty
    "malicious.exe",
    "test.csv",
    "test_1.json",
    "test_1.md",
    "test_1.pptx",
    "test_1.docx",
    "test_1.yaml",
]


@pytest.mark.parametrize("filename", SUPPORTED_FILES)
def test_supported_conversion(tmp_path, filename: str):
    """
    Ensure MarkItDownConverter successfully converts supported file formats to Markdown.
    """
    converter = MarkdownConverter()
    input_path = DATA_DIR / filename
    output_path = tmp_path / f"{Path(filename).stem}.md"

    # Perform conversion
    converter.convert(input_path, output_path)

    # Verify output exists and is non-empty
    assert output_path.exists(), f"Output MD not found for {filename}"
    assert output_path.stat().st_size > 0, f"Generated MD is empty for {filename}"


@pytest.mark.parametrize("filename", UNSUPPORTED_FILES)
def test_unsupported_conversion(tmp_path, filename: str):
    """
    Ensure MarkItDownConverter raises ConversionError for unsupported file types.
    """
    converter = MarkdownConverter()
    input_path = DATA_DIR / filename
    output_path = tmp_path / f"{Path(filename).stem}.md"

    with pytest.raises(ConversionError):
        converter.convert(input_path, output_path)
