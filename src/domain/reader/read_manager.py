import logging
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from fastapi import UploadFile

from src.domain.reader.readers import (
    DoclingReader,
    MarkItDownReader,
    PandasReader,
    PDFPlumberReader,
    TextractReader,
)
from src.infrastructure.analyzer.analyze_manager import AnalyzeManager
from src.infrastructure.converter.convert_manager import ConvertManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d - %H:%M:%S",
)


class ReadManager:
    """
    1) Convert incoming file → standardized extension
    2) Ask AnalyzeManager which LLM client & model to use
    3) Pick the right Reader, feed it the client+model
    4) Return the markdown text
    """

    def __init__(
        self,
        config: Optional[Dict] = None,
        *,
        input_path: Optional[str] = None,
        config_path: str = "config.yaml",
    ) -> None:
        # --- load config & defaults
        if config is None:
            input_path = input_path or "data/input"
            config = {"file_io": {"input_path": input_path}}
        self.config = config
        self.input_path = self.config["file_io"]["input_path"]

        # managers
        self.converter = ConvertManager(config_path)
        self.analyzer = AnalyzeManager(config_path)

        # reader method (e.g. "markitdown")
        self.reader_method: str = self.config.get("reader", {}).get(
            "method", "markitdown"
        )

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"{now} | ReadManager initialized | Config: {self.config}")

    def read_file(self, file_path: str) -> str:
        # 1) resolve path
        if not os.path.isabs(file_path):
            file_path = os.path.join(self.input_path, file_path)
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(file_path)
        if p.stat().st_size == 0:
            raise ValueError(f"{file_path} is empty")

        # 2) convert into a temp folder
        with tempfile.TemporaryDirectory() as tmpdir:
            converted = self.converter.convert_file(p, tmpdir)
            # converted is a Path to the (maybe new-ext) file

            # 3) pick analyzer client + model
            client, model_name = self.analyzer.get_analyzer(converted.suffix)

            # 4) instantiate the reader
            reader = self._make_reader(client, model_name)

            # 5) run conversion → markdown text
            try:
                text = reader.convert(str(converted))
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logging.info(
                    f"{now} | read_file finished | {converted.name} | "
                    f"{reader.__class__.__name__}"
                )
                return text
            except Exception as e:
                logging.error(f"Reader failed on {converted}: {e}")
                raise RuntimeError("Failed to read file")

    def read_file_object(self, file: UploadFile) -> str:
        # same trick for an UploadFile
        suffix = "." + file.filename.rsplit(".", 1)[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name

        try:
            return self.read_file(tmp_path)
        finally:
            os.remove(tmp_path)

    def _make_reader(self, client, model_name: Optional[str]):
        """
        Pass client + model_name into the Reader constructor.
        client may be None (if analyzer == 'none').
        model_name may be None too.
        """
        if self.reader_method == "markitdown":
            return MarkItDownReader(client, model_name)
        elif self.reader_method == "docling":
            return DoclingReader()  # TODO: Add support to models
        elif self.reader_method == "pdfplumber":
            return PDFPlumberReader()  # TODO: Add support to models
        elif self.reader_method == "textract":
            return TextractReader(client, model_name)
        elif self.reader_method == "pandas":
            return PandasReader()

        raise ValueError(f"Unsupported reader method: {self.reader_method}")
