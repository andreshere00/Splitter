import xml.dom.minidom
from pathlib import Path
from typing import Union

import pandas as pd

from src.infrastructure.converter.base_converter import BaseConverter, ConversionError


class HTMLConverter(BaseConverter):
    """
    Converter for SVG, XML, and Excel files to HTML format.

    Supports:
    - .svg   : wraps raw SVG content in an HTML document
    - .xml   : pretty-prints XML inside <pre> in an HTML document
    - .xlsx, .xls : reads Excel sheets and outputs HTML tables
    """

    def convert(
        self, input_source: Union[str, Path], output_target: Union[str, Path]
    ) -> None:
        """
        Convert a supported file type to HTML and write to the specified path.

        :param input_source: Path to the source file (.svg, .xml, .xlsx, .xls)
        :param output_target: Path where the HTML output will be saved.
        :raises ConversionError: if conversion fails or extension unsupported.
        """
        src = Path(input_source)
        dst = Path(output_target)
        suffix = src.suffix.lower()

        handlers = {
            ".svg": self._convert_svg,
            ".xml": self._convert_xml,
            ".xlsx": self._convert_excel,
            ".xls": self._convert_excel,
        }

        handler = handlers.get(suffix)
        if handler is None:
            raise ConversionError(
                f"Unsupported extension for HTML conversion: {suffix}"
            )

        handler(src, dst)

    def _convert_svg(self, src: Path, dst: Path) -> None:
        """
        Wrap raw SVG content in a basic HTML document.

        :param src: Path to the .svg file.
        :param dst: Path where the HTML file will be saved.
        :raises ConversionError: on read/write errors.
        """
        try:
            svg_content = src.read_text(encoding="utf-8")
        except Exception as e:
            raise ConversionError(f"Failed to read SVG file: {e}")

        html = f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <title>{src.name}</title>
</head>
<body>
{svg_content}
</body>
</html>
""".strip()

        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            dst.write_text(html, encoding="utf-8")
        except Exception as e:
            raise ConversionError(f"Failed to write HTML file: {e}")

    def _convert_xml(self, src: Path, dst: Path) -> None:
        """
        Pretty-print XML content inside a <pre> tag in an HTML document.

        :param src: Path to the .xml file.
        :param dst: Path where the HTML file will be saved.
        :raises ConversionError: on parse or write errors.
        """
        try:
            dom = xml.dom.minidom.parse(str(src))
            pretty_xml = dom.toprettyxml()
        except Exception as e:
            raise ConversionError(f"Failed to parse XML: {e}")

        html = f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <title>{src.name}</title>
</head>
<body>
<pre>
{pretty_xml}
</pre>
</body>
</html>
""".strip()

        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            dst.write_text(html, encoding="utf-8")
        except Exception as e:
            raise ConversionError(f"Failed to write HTML file: {e}")

    def _convert_excel(self, src: Path, dst: Path) -> None:
        """
        Read Excel workbook via pandas and write each sheet as an HTML table.

        If multiple sheets exist, concatenates tables with headers.

        :param src: Path to the .xlsx or .xls file.
        :param dst: Path where the HTML file will be saved.
        :raises ConversionError: on read or write errors.
        """
        try:
            sheets = pd.read_excel(src, sheet_name=None)
        except Exception as e:
            raise ConversionError(f"Failed to read Excel file: {e}")

        parts = [
            """<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <title>{0}</title>
</head>
<body>""".format(
                src.name
            )
        ]

        for name, df in sheets.items():
            parts.append(f"<h2>Sheet: {name}</h2>")
            try:
                parts.append(df.to_html(index=False, escape=False))
            except Exception as e:
                raise ConversionError(f"Failed to convert sheet '{name}' to HTML: {e}")

        parts.append("</body></html>")
        html = "\n".join(parts)

        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            dst.write_text(html, encoding="utf-8")
        except Exception as e:
            raise ConversionError(f"Failed to write HTML file: {e}")
