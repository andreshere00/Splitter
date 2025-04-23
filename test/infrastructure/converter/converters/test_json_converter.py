import json
from pathlib import Path

import pytest

from src.infrastructure.converter.base_converter import ConversionError
from src.infrastructure.converter.converters.json_converter import JSONConverter

# Directory containing test input files
DATA_DIR = Path(__file__).parents[4] / "data" / "test" / "input"

# Supported formats for JSONConverter
SUPPORTED_FILES = [
    "test_1.xml",
    "test_1.yaml",
    "test_1.xlsx",
]

# Unsupported formats should raise ConversionError
UNSUPPORTED_FILES = [
    "empty.txt",
    "malicious.exe",
    "test.csv",
    "test_1.docx",
    "test_1.html",
    "test_1.json",
    "test_1.md",
    "test_1.pdf",
    "test_1.pptx",
    "test_1.txt",
    # any other unsupported extension
]


@pytest.mark.parametrize("filename", SUPPORTED_FILES)
def test_supported_conversion(tmp_path, filename: str):
    """
    Ensure JSONConverter successfully converts supported formats to JSON.
    """
    converter = JSONConverter()
    input_path = DATA_DIR / filename
    output_path = tmp_path / f"{Path(filename).stem}.json"

    # Perform conversion
    converter.convert(input_path, output_path)

    # Verify output exists
    assert output_path.exists(), f"Output JSON not found for {filename}"
    # Verify output is non-empty and valid JSON
    content = output_path.read_text(encoding="utf-8")
    assert content.strip(), f"Generated JSON is empty for {filename}"

    # Try loading JSON
    try:
        obj = json.loads(content)
    except json.JSONDecodeError as e:
        pytest.fail(f"Generated file is not valid JSON for {filename}: {e}")

    # Loaded object should be dict or list
    assert isinstance(
        obj, (dict, list)
    ), f"JSON root should be dict or list for {filename}"


@pytest.mark.parametrize("filename", UNSUPPORTED_FILES)
def test_unsupported_conversion(tmp_path, filename: str):
    """
    Ensure JSONConverter raises ConversionError for unsupported file types.
    """
    converter = JSONConverter()
    input_path = DATA_DIR / filename
    output_path = tmp_path / f"{Path(filename).stem}.json"

    with pytest.raises(ConversionError):
        converter.convert(input_path, output_path)
