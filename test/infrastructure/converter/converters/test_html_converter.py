from pathlib import Path

import pytest

from src.infrastructure.converter.base_converter import ConversionError
from src.infrastructure.converter.converters.html_converter import HTMLConverter

# Directory containing test input files
DATA_DIR = Path(__file__).parents[4] / "data" / "test" / "input"

SUPPORTED_FILES = [
    "test_1.xml",
    "test_1.xlsx",
]

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
    "test_1.yaml",
]


@pytest.mark.parametrize("filename", SUPPORTED_FILES)
def test_supported_conversion(tmp_path, filename: str):
    """
    Ensure HTMLConverter successfully converts XML and Excel to HTML.
    """
    converter = HTMLConverter()
    input_path = DATA_DIR / filename
    output_path = tmp_path / f"{Path(filename).stem}.html"

    converter.convert(input_path, output_path)

    assert output_path.exists(), f"HTML output not found for {filename}"
    content = output_path.read_text(encoding="utf-8")
    assert "<html" in content.lower(), f"Output missing HTML tags for {filename}"


def test_svg_conversion(tmp_path):
    """
    Ensure HTMLConverter successfully wraps SVG in HTML.
    """
    converter = HTMLConverter()
    svg_content = (
        '<svg xmlns="http://www.w3.org/2000/svg"><rect width="100" height="50"/></svg>'
    )
    svg_path = tmp_path / "test.svg"
    svg_path.write_text(svg_content, encoding="utf-8")
    output_path = tmp_path / "test.html"

    converter.convert(svg_path, output_path)

    assert output_path.exists(), "HTML output not found for SVG"
    content = output_path.read_text(encoding="utf-8")
    # should include svg content inside body
    assert svg_content in content, "SVG content not embedded in HTML output"


@pytest.mark.parametrize("filename", UNSUPPORTED_FILES)
def test_unsupported_conversion(tmp_path, filename: str):
    """
    Ensure HTMLConverter raises ConversionError for unsupported file types.
    """
    converter = HTMLConverter()
    input_path = DATA_DIR / filename
    output_path = tmp_path / f"{Path(filename).stem}.html"

    with pytest.raises(ConversionError):
        converter.convert(input_path, output_path)
