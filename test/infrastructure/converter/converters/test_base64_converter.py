import base64
from pathlib import Path

import pytest

from src.infrastructure.converter.base_converter import ConversionError
from src.infrastructure.converter.converters.base64_converter import Base64Converter

# Directory containing test input files
DATA_DIR = Path(__file__).resolve().parents[4] / "data" / "test" / "input"

# Supported raster formats in DATA_DIR
SUPPORTED_RASTER = ["test_1.jpg", "test_1.bmp", "test_1.gif"]
# Unsupported formats
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
    "test_1.xlsx",
    "test_1.xml",
    "test_1.yaml",
]


@pytest.mark.parametrize("filename", SUPPORTED_RASTER)
def test_supported_raster_base64(tmp_path, filename):
    """
    Ensure Base64Converter successfully encodes supported raster images to Base64.
    """
    converter = Base64Converter()
    src = DATA_DIR / filename
    dst = tmp_path / f"{Path(filename).stem}.b64"

    # Perform conversion
    converter.convert(src, dst)

    # Verify output exists
    assert dst.exists(), f"Base64 output not found for {filename}"

    # Read Base64 string and decode
    b64_str = dst.read_text(encoding="utf-8")
    assert b64_str.strip(), f"Empty Base64 output for {filename}"

    decoded = base64.b64decode(b64_str)
    original = src.read_bytes()
    assert decoded == original, f"Decoded bytes do not match original for {filename}"


def test_svg_base64(tmp_path):
    """
    Ensure Base64Converter can encode SVG files to Base64.
    """
    svg_content = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">'
        '<rect width="10" height="10" fill="red"/>'
        "</svg>"
    )
    svg_file = tmp_path / "test.svg"
    svg_file.write_text(svg_content, encoding="utf-8")
    dst = tmp_path / "test.b64"

    converter = Base64Converter()
    converter.convert(svg_file, dst)

    assert dst.exists(), "Base64 output not found for SVG"
    b64_str = dst.read_text(encoding="utf-8")
    decoded = base64.b64decode(b64_str).decode("utf-8")
    assert decoded == svg_content, "Decoded SVG content does not match original"


@pytest.mark.parametrize("filename", UNSUPPORTED_FILES)
def test_unsupported_files(tmp_path, filename):
    """
    Ensure Base64Converter raises ConversionError for unsupported file types.
    """
    converter = Base64Converter()
    src = DATA_DIR / filename
    dst = tmp_path / f"{Path(filename).stem}.b64"

    with pytest.raises(ConversionError):
        converter.convert(src, dst)
