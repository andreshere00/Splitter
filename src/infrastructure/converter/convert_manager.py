import logging
import shutil
from pathlib import Path
from typing import Optional, Union

from src.infrastructure.converter.converters import (
    Base64Converter,
    HTMLConverter,
    JSONConverter,
    MarkdownConverter,
    PDFConverter,
    PNGConverter,
)
from src.infrastructure.helpers.config_loader import load_config

from .base_converter import BaseConverter, ConversionError


class ConvertManager:
    """
    Look at a file’s extension, consult the YAML config,
    and dispatch to the correct BaseConverter subclass (or skip).
    """

    # map the “conversion name” in your YAML to the actual class
    _CREATORS = {
        "pdf": PDFConverter,
        "markdown": MarkdownConverter,
        "json": JSONConverter,
        "html": HTMLConverter,
        "png": PNGConverter,
        "base64": Base64Converter,
    }

    def __init__(self, config_path: Union[str, Path]):
        cfg = load_config(config_path)
        conv_cfg = cfg["converter"]
        self._default = conv_cfg["default"]  # e.g. “none”
        self._overrides = {
            ext.lower(): conv_name
            for ext, conv_name in (conv_cfg.get("override") or {}).items()
        }

    def _get_conversion_name(self, ext: str) -> str:
        # strip leading “.” and down-case
        e = ext.lower().lstrip(".")
        return self._overrides.get(e, self._default)

    def _make_converter(self, conv_name: str) -> Optional[BaseConverter]:
        if conv_name == "none":
            return None
        cls = self._CREATORS.get(conv_name)
        if not cls:
            raise ConversionError(f"No converter registered for '{conv_name}'")
        return cls()

    def convert_file(
        self, src: Union[str, Path], dst_folder: Union[str, Path]
    ) -> Optional[Path]:
        src = Path(src)
        dst_folder = Path(dst_folder)
        dst_folder.mkdir(parents=True, exist_ok=True)

        conv_name = self._get_conversion_name(src.suffix)
        converter = self._make_converter(conv_name)

        if converter is None:
            # no conversion needed → just copy through
            dst = dst_folder / src.name
            shutil.copy(src, dst)
            logging.debug(f"Skipped conversion of {src}, copied to {dst}")
            return dst

        # build the output filename with the new extension
        out_name = src.with_suffix(f".{conv_name}").name
        dst = dst_folder / out_name

        try:
            converter.convert(src, dst)
            logging.info(
                f"Converted {src} → {dst} using {converter.__class__.__name__}"
            )
            return dst
        except ConversionError as e:
            logging.error(f"Conversion failed for {src}: {e}")
            raise

    def convert_folder(
        self, src_folder: Union[str, Path], dst_folder: Union[str, Path]
    ):
        for p in Path(src_folder).iterdir():
            if not p.is_file():
                continue
            self.convert_file(p, dst_folder)
