import logging
import os
from typing import Dict, Optional

from src.model.llm_client import LLMClient
from src.reader.readers.markitdown_reader import MarkItDownConverter


class ReadManager:
    """
    Manages reading and converting files into text using format-specific converters.
    """

    def __init__(
        self, config: Optional[Dict] = None, *, input_path: Optional[str] = None
    ) -> None:
        """
        Initializes ReadManager with a configuration or a default input path.

        Args:
            config (dict, optional): Configuration dictionary.
            input_path (str, optional): Path to the input directory.
        """
        if config is None:
            input_path = input_path or "data/input"
            config = {"file_io": {"input_path": input_path}}
        self.config: Dict = config
        self.input_path: str = self.config.get("file_io", {}).get(
            "input_path", "data/input"
        )
        self.llm: LLMClient = LLMClient(
            self.config.get("ocr", {}).get("method", "none")
        )

    def read_file(self, file_name: str) -> str:
        """
        Reads and converts a file to text based on its extension.

        Args:
            file_name (str): Name of the file to read.

        Returns:
            str: Converted text content.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            ValueError: If the file is empty or unsupported.
            RuntimeError: If conversion fails.
        """
        file_path: str = os.path.join(self.input_path, file_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        if os.path.getsize(file_path) == 0:
            raise ValueError("File is empty")

        ext: str = file_name.lower().split(".")[-1]
        converter: Optional[MarkItDownConverter] = self._get_converter_for_extension(
            ext
        )
        if converter is None:
            raise ValueError("Unsupported file extension")

        try:
            return converter.convert(file_path)
        except Exception as e:
            logging.error(
                f"Error converting file {file_path} using {converter.__class__.__name__}: {e}"
            )
            raise RuntimeError("Failed to convert file")

    def _get_converter_for_extension(self, ext: str) -> Optional[MarkItDownConverter]:
        """
        Returns the appropriate converter based on file extension.

        Args:
            ext (str): File extension.

        Returns:
            Optional[MarkItDownConverter]: Converter instance or None if unsupported.
        """
        client = self.llm.get_client()
        model = self.llm.get_model()

        mapping: Dict[str, MarkItDownConverter] = {
            "txt": MarkItDownConverter(),
            "md": MarkItDownConverter(),
            "docx": MarkItDownConverter(client, model),
            "xlsx": MarkItDownConverter(),
            "pptx": MarkItDownConverter(client, model),
            "pdf": MarkItDownConverter(client, model),
            "png": MarkItDownConverter(client, model),
            "jpg": MarkItDownConverter(client, model),
        }
        return mapping.get(ext)
