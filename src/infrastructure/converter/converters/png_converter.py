import os
from pathlib import Path
from typing import Union

from pdf2image import convert_from_path
from PIL import Image
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

from src.infrastructure.converter.base_converter import BaseConverter, ConversionError


class PNGConverter(BaseConverter):
    """
    Converter for images to PNG format.

    Supports raster formats via Pillow:
    - .jpg, .jpeg, .png, .bmp, .gif, .tiff

    Supports vector SVG by converting via PDF intermediate:
    - .svg
    """

    def convert(
        self, input_source: Union[str, Path], output_target: Union[str, Path]
    ) -> None:
        """
        Convert an image file to PNG and save to the specified path.

        :param input_source: Path to the source image file.
        :param output_target: Path where the PNG file will be saved.
        :raises ConversionError: if conversion fails or format unsupported.
        """
        src = Path(input_source)
        dst = Path(output_target)
        suffix = src.suffix.lower()

        handlers = {
            ".jpg": self._convert_raster,
            ".jpeg": self._convert_raster,
            ".png": self._convert_raster,
            ".bmp": self._convert_raster,
            ".gif": self._convert_raster,
            ".tiff": self._convert_raster,
            ".svg": self._convert_svg,
        }

        handler = handlers.get(suffix)
        if handler is None:
            raise ConversionError(f"Unsupported extension for PNG conversion: {suffix}")

        handler(src, dst)

    def _convert_raster(self, src: Path, dst: Path) -> None:
        """
        Convert raster images to PNG using Pillow.

        :param src: Path to a raster image file.
        :param dst: Path where the PNG file will be saved.
        :raises ConversionError: on read or write failures.
        """
        try:
            img = Image.open(src)
            img = img.convert("RGBA")
        except Exception as e:
            raise ConversionError(f"Failed to open raster image: {e}")

        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            img.save(dst, format="PNG")
        except Exception as e:
            raise ConversionError(f"Failed to save PNG image: {e}")

    def _convert_svg(self, src: Path, dst: Path) -> None:
        """
        Convert an SVG file to PNG by first converting it to PDF and then to PNG.

        :param src: Path to the .svg file.
        :param dst: Path where the PNG file will be saved.
        :raises ConversionError: if conversion fails.
        """
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            # Intermediate PDF path
            pdf_file = dst.with_suffix(".pdf")

            # SVG -> PDF
            drawing = svg2rlg(str(src))
            renderPDF.drawToFile(drawing, str(pdf_file))

            # PDF -> PNG
            images = convert_from_path(str(pdf_file), dpi=300)
            if not images:
                raise ConversionError(
                    f"PDF to PNG conversion produced no images for {src}"
                )
            images[0].save(str(dst), format="PNG")

            # Clean up
            os.remove(str(pdf_file))
        except Exception as e:
            raise ConversionError(f"Failed to convert SVG to PNG: {e}")
