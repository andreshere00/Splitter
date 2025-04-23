from pathlib import Path

import pytest
from PIL import Image

from src.infrastructure.converter.base_converter import ConversionError
from src.infrastructure.converter.converters.png_converter import PNGConverter

# Directory containing test input files
DATA_DIR = Path(__file__).parents[4] / "data" / "test" / "input"

# Supported raster formats and their filenames in DATA_DIR
SUPPORTED_FILES = ["test_1.jpg", "test_1.bmp", "test_1.gif", "test_1.tiff"]

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
    "test_1.xlsx",
    "test_1.xml",
    "test_1.yaml",
]


@pytest.mark.parametrize("filename", SUPPORTED_FILES)
def test_supported_raster_conversion(tmp_path, filename):
    """
    Ensure PNGConverter successfully converts supported raster image formats to PNG.
    """
    converter = PNGConverter()
    input_file = DATA_DIR / filename
    output_file = tmp_path / f"{Path(filename).stem}.png"

    # Perform conversion
    converter.convert(str(input_file), str(output_file))

    # Verify output exists and is a valid PNG
    assert output_file.exists(), f"Output PNG not found for {filename}"
    img = Image.open(output_file)
    assert img.format == "PNG", f"Expected PNG format, got {img.format}"
    assert img.width > 0 and img.height > 0, "Output image has invalid dimensions"


@pytest.mark.parametrize("filename", UNSUPPORTED_FILES)
def test_unsupported_conversion(tmp_path, filename):
    """
    Ensure PNGConverter raises ConversionError for unsupported file types.
    """
    converter = PNGConverter()
    input_file = DATA_DIR / filename
    output_file = tmp_path / f"{Path(filename).stem}.png"

    with pytest.raises(ConversionError):
        converter.convert(str(input_file), str(output_file))


def test_svg_conversion(tmp_path):
    """
    Ensure PNGConverter can convert SVG images via PDF intermediate.
    """
    # Create a minimal SVG file
    svg_content = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">'
        '<rect width="10" height="10" fill="blue"/>'
        "</svg>"
    )
    svg_file = tmp_path / "test.svg"
    svg_file.write_text(svg_content, encoding="utf-8")
    output_file = tmp_path / "test.png"

    converter = PNGConverter()
    converter.convert(str(svg_file), str(output_file))

    assert output_file.exists(), "SVG to PNG conversion did not produce output"
    img = Image.open(output_file)
    assert img.format == "PNG", f"Expected PNG format, got {img.format}"
    assert img.width > 0 and img.height > 0, "SVG output image has invalid dimensions"
