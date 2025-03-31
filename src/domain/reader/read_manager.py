import logging
import os
import tempfile
from typing import Dict, Optional

from fastapi import UploadFile

from src.infrastructure.model.llm_client import LLMClient
from src.domain.reader.readers.markitdown_reader import MarkItDownReader


class ReadManager:
    """
    ReadManager is responsible for reading input documents from a specified location.

    This class supports multiple file formats such as text files (.txt, .md), Microsoft 
    Word (.docx), PDFs, PowerPoint files (.pptx), and Excel files (.xlsx). It can also 
    apply OCR processing when required.

    Attributes:
        config (dict): Configuration settings for file I/O, including input path and OCR method.

    Methods:
        read_file(file_path: str) -> str:
            Reads the file from the given path and returns its content as a string.
        read_file_object(file: UploadFile) -> str:
            Reads the content from an uploaded file object and returns it as a string.
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

    def read_file(self, file_path: str) -> str:
        """
        Reads and converts a file from the given file path to Markdown text.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Converted Markdown text.
        """
        if not os.path.isabs(file_path):
            file_path = os.path.join(self.input_path, file_path)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        if os.path.getsize(file_path) == 0:
            raise ValueError("File is empty")

        ext = file_path.lower().split(".")[-1]
        converter = self._get_converter_for_extension(ext)
        if converter is None:
            raise ValueError("Unsupported file extension")

        try:
            return converter.convert(file_path)
        except Exception as e:
            logging.error(
                f"Error converting file {file_path} using {converter.__class__.__name__}: {e}"
            )
            raise RuntimeError("Failed to convert file")

    def read_file_object(self, file: UploadFile) -> str:
        """
        Reads and converts an uploaded file object to Markdown text.
        The file is temporarily saved to disk, processed, and then deleted.

        Args:
            file (UploadFile): The uploaded file object.

        Returns:
            str: Converted Markdown text.
        """
        tmp_path = ""
        try:
            with tempfile.NamedTemporaryFile(
                delete=False, suffix="." + file.filename.split(".")[-1]
            ) as tmp:
                tmp.write(file.file.read())
                tmp_path = tmp.name
            return self.read_file(tmp_path)
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

    def _get_converter_for_extension(self, ext: str) -> Optional[MarkItDownReader]:
        """
        Returns the appropriate converter based on file extension.

        Args:
            ext (str): File extension.

        Returns:
            Optional[MarkItDownReader]: Converter instance or None if unsupported.
        """
        client = self.llm.get_client()
        model = self.llm.get_model()

        mapping: Dict[str, MarkItDownReader] = {
            "txt": MarkItDownReader(client, model),
            "md": MarkItDownReader(client, model),
            "docx": MarkItDownReader(client, model),
            "xlsx": MarkItDownReader(client, model),
            "pptx": MarkItDownReader(client, model),
            "pdf": MarkItDownReader(client, model),
            "jpg": MarkItDownReader(client, model),
            "jpeg": MarkItDownReader(client, model),
            "png": MarkItDownReader(client, model),
        }
        return mapping.get(ext)
