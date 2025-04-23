import base64
from pathlib import Path
from typing import Union

from src.infrastructure.converter.base_converter import BaseConverter, ConversionError


class Base64Converter(BaseConverter):
    """
    Converter for encoding image files to Base64 strings.

    Supports common raster and vector formats:
    - .png, .jpg, .jpeg, .bmp, .gif, .tiff, .svg

    The output is a UTF-8 text file containing the Base64 representation of the image.
    """

    def convert(
        self, input_source: Union[str, Path], output_target: Union[str, Path]
    ) -> None:
        """
        Read the input image, encode its bytes to Base64, and write the result to output.

        :param input_source: Path to the source image file.
        :param output_target: Path where the Base64 text file will be saved.
        :raises ConversionError: if file I/O or encoding fails, or extension unsupported.
        """
        src = Path(input_source)
        dst = Path(output_target)
        suffix = src.suffix.lower()

        supported_exts = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".svg"}
        if suffix not in supported_exts:
            raise ConversionError(
                f"Unsupported extension for Base64 conversion: {suffix}"
            )

        # Read raw bytes
        try:
            raw = src.read_bytes()
        except Exception as e:
            raise ConversionError(f"Failed to read file: {e}")

        # Encode to Base64
        try:
            b64 = base64.b64encode(raw).decode("utf-8")
        except Exception as e:
            raise ConversionError(f"Failed to encode to Base64: {e}")

        # Write Base64 string to output
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            dst.write_text(b64, encoding="utf-8")
        except Exception as e:
            raise ConversionError(f"Failed to write Base64 output: {e}")
