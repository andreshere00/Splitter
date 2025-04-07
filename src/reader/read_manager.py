import logging
import os
import tempfile
from typing import Dict, Optional

from fastapi import UploadFile

from src.model.llm_client import LLMClient
from src.reader.readers.markitdown_reader import MarkItDownReader

# from src.reader.readers.docling_reader import DoclingReader
# from src.reader.readers.pdfplumber_reader import PDFPlumberReader
# from src.reader.readers.textract_reader import TextractReader


class ReadManager:
    """
    ReadManager is responsible for reading input documents and converting them to Markdown text.
    It selects the appropriate reader based on configuration.
    """

    def __init__(
        self, config: Optional[Dict] = None, *, input_path: Optional[str] = None
    ) -> None:
        if config is None:
            input_path = input_path or "data/input"
            config = {"file_io": {"input_path": input_path}}
        self.config: Dict = config
        self.input_path: str = self.config.get("file_io", {}).get(
            "input_path", "data/input"
        )
        self.reader_method: str = self.config.get("reader", {}).get(
            "method", "markitdown"
        )
        ocr_method = self.config.get("ocr", {}).get("method", "none")
        self.llm: LLMClient = LLMClient(ocr_method)

    def read_file(self, file_path: str) -> str:
        """
        Reads a file from the specified path, converts it using the configured reader,
        and returns the resulting Markdown text.

        Args:
            file_path (str): The path to the file to be read.

        Returns:
            str: The converted Markdown text.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is empty.
            RuntimeError: If an error occurs during conversion.
        """
        if not os.path.isabs(file_path):
            file_path = os.path.join(self.input_path, file_path)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        if os.path.getsize(file_path) == 0:
            raise ValueError("File is empty")

        reader = self._get_reader()
        try:
            return reader.convert(file_path)
        except Exception as e:
            logging.error(
                f"Error converting file {file_path} using {reader.__class__.__name__}: {e}"
            )
            raise RuntimeError("Failed to convert file")

    def read_file_object(self, file: UploadFile) -> str:
        """
        Reads an uploaded file object, temporarily saves it to disk,
        converts it using the configured reader, and returns the Markdown text.

        Args:
            file (UploadFile): The uploaded file object.

        Returns:
            str: The converted Markdown text.
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

    def _get_reader(self):
        """
        Instantiates and returns the appropriate reader based on the configuration.
        Only the MarkItDown and Docling readers are provided with the client and model.

        Returns:
            An instance of the selected reader with a 'convert' method.

        Raises:
            ValueError: If an unsupported reader method is specified.
        """
        client = self.llm.get_client() if self.llm.method != "none" else None
        model = self.llm.get_model() if self.llm.method != "none" else None

        if self.reader_method == "markitdown":
            return MarkItDownReader(client, model)
        # elif self.reader_method == "docling":
        #     return DoclingReader(client, model)
        # elif self.reader_method == "pdfplumber":
        #     return PDFPlumberReader(client, model)
        # elif self.reader_method == "textract":
        #     return TextractReader(client, model)
        else:
            raise ValueError(f"Unsupported reader method: {self.reader_method}")
