from pathlib import Path
from typing import Optional, Union

from markitdown import MarkItDown

from src.infrastructure.converter.base_converter import BaseConverter, ConversionError


class MarkdownConverter(BaseConverter):
    """
    Converter for various document types to Markdown using MarkItDown or built-in logic.

    Supports:
    - .txt : plain text pass-through (non-empty)
    - .pdf, .html, .xlsx : conversion via MarkItDown
    - .xml : vanilla text passthrough (non-empty)
    """

    def __init__(
        self, llm_client: Optional[object] = None, llm_model: Optional[str] = None
    ):
        """
        Initialize the MarkItDown instance.

        :param llm_client: Optional LLM client for image descriptions.
        :param llm_model: Optional model name for image descriptions.
        """
        self.md = MarkItDown(llm_client=llm_client, llm_model=llm_model)

    def convert(
        self, input_source: Union[str, Path], output_target: Union[str, Path]
    ) -> None:
        """
        Convert supported files to Markdown and write to output.

        Delegates to the appropriate helper based on file extension.

        :param input_source: Path to the source file.
        :param output_target: Path where the Markdown file will be saved.
        :raises ConversionError: if conversion fails or extension unsupported.
        """
        src = Path(input_source)
        dst = Path(output_target)
        suffix = src.suffix.lower()

        handlers = {
            ".txt": self._convert_txt,
            ".pdf": self._convert_with_markitdown,
            ".html": self._convert_with_markitdown,
            ".xlsx": self._convert_with_markitdown,
            ".xml": self._convert_txt,
        }

        handler = handlers.get(suffix)
        if handler is None:
            raise ConversionError(f"Unsupported extension: {suffix}")

        handler(src, dst)

    def _convert_txt(self, src: Path, dst: Path) -> None:
        """
        Copy plain text or XML files directly to the destination, ensuring non-empty content.

        :param src: Path to the .txt or .xml file.
        :param dst: Path where the Markdown file will be saved.
        :raises ConversionError: if file is empty.
        """
        text = src.read_text(encoding="utf-8")
        if not text.strip():
            raise ConversionError(f"Source file is empty: {src}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text, encoding="utf-8")

    def _convert_with_markitdown(self, src: Path, dst: Path) -> None:
        """
        Use MarkItDown to convert documents to Markdown.

        Supports PDF, HTML, XLSX formats.

        :param src: Path to the source file.
        :param dst: Path where the Markdown file will be saved.
        :raises ConversionError: if MarkItDown conversion fails.
        """
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            result = self.md.convert(str(src))
        except Exception as e:
            raise ConversionError(f"MarkItDown conversion failed: {e}")

        try:
            dst.write_text(result.text_content, encoding="utf-8")
        except Exception as e:
            raise ConversionError(f"Failed to write output file: {e}")
