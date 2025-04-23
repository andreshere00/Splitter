import json
from pathlib import Path
from typing import Union

import pandas as pd
import xmltodict
import yaml

from src.infrastructure.converter.base_converter import BaseConverter, ConversionError


class JSONConverter(BaseConverter):
    """
    Converter for XML, YAML, and Excel files to JSON format.

    Supports:
    - .xml   : parsed via xmltodict
    - .yaml, .yml : parsed via PyYAML
    - .xlsx, .xls : parsed via pandas
    """

    def convert(
        self, input_source: Union[str, Path], output_target: Union[str, Path]
    ) -> None:
        """
        Convert a supported file type to JSON and write to the specified path.

        :param input_source: Path to the source file (.xml, .yaml/.yml, .xlsx/.xls).
        :param output_target: Path where the JSON output will be saved.
        :raises ConversionError: if conversion fails or extension unsupported.
        """
        src = Path(input_source)
        dst = Path(output_target)
        suffix = src.suffix.lower()

        # map extensions to handlers
        handlers = {
            ".xml": self._convert_xml,
            ".yaml": self._convert_yaml,
            ".yml": self._convert_yaml,
            ".xlsx": self._convert_excel,
            ".xls": self._convert_excel,
        }

        handler = handlers.get(suffix)
        if handler is None:
            raise ConversionError(
                f"Unsupported extension for JSON conversion: {suffix}"
            )

        handler(src, dst)

    def _convert_xml(self, src: Path, dst: Path) -> None:
        """
        Parse an XML file into a Python dict via xmltodict and write as JSON.

        :param src: Path to the .xml file.
        :param dst: Path where the JSON file will be saved.
        :raises ConversionError: on parsing or writing errors.
        """
        try:
            content = src.read_text(encoding="utf-8")
            data = xmltodict.parse(content)
        except Exception as e:
            raise ConversionError(f"Failed to parse XML: {e}")

        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(dst, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise ConversionError(f"Failed to write JSON file: {e}")

    def _convert_yaml(self, src: Path, dst: Path) -> None:
        """
        Parse a YAML file into a Python object via PyYAML and write as JSON.

        :param src: Path to the .yaml or .yml file.
        :param dst: Path where the JSON file will be saved.
        :raises ConversionError: on parsing or writing errors.
        """
        try:
            content = src.read_text(encoding="utf-8")
            data = yaml.safe_load(content)
        except Exception as e:
            raise ConversionError(f"Failed to parse YAML: {e}")

        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(dst, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise ConversionError(f"Failed to write JSON file: {e}")

    def _convert_excel(self, src: Path, dst: Path) -> None:
        """
        Read an Excel workbook via pandas and write each sheet as JSON.

        If multiple sheets exist, output is a dict mapping sheet names
        to list-of-records, else a single list-of-records.

        :param src: Path to the .xlsx or .xls file.
        :param dst: Path where the JSON file will be saved.
        :raises ConversionError: on reading or writing errors.
        """
        try:
            sheets = pd.read_excel(src, sheet_name=None)
        except Exception as e:
            raise ConversionError(f"Failed to read Excel file: {e}")

        # if single-sheet, unwrap
        if len(sheets) == 1:
            _, df = next(iter(sheets.items()))
            data = df.to_dict(orient="records")
        else:
            data = {sheet: df.to_dict(orient="records") for sheet, df in sheets.items()}

        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(dst, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise ConversionError(f"Failed to write JSON file: {e}")
