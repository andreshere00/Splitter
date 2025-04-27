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
    1) Convert file (if needed)
    2) Select analyzer client/model
    3) Choose the correct Reader (honouring reader.override in YAML)
    4) Return markdown text
    """

    # ------------------------------------------------------------------ #
    # construction
    # ------------------------------------------------------------------ #

    def __init__(
        self,
        config: Optional[Dict] = None,
        *,
        input_path: Optional[str] = None,
        config_path: str = "config.yaml",
    ) -> None:
        self.config = config or {}

        # input_path resolution
        self.input_path = input_path or self.config.get("file_io", {}).get(
            "input_path", "data/input"
        )

        # managers
        self.converter = ConvertManager(config_path)
        self.analyzer = AnalyzeManager(config_path)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"{now} | ReadManager initialized | input_path={self.input_path}")

    # ------------------------------------------------------------------ #
    # helpers
    # ------------------------------------------------------------------ #

    def _reader_for_extension(self, ext: str) -> str:
        """
        Decide which reader to use for a given file extension,
        looking at reader.override first, then reader.default,
        finally falling back to 'markitdown'.
        """
        ext = ext.lstrip(".").lower()
        r_cfg = self.config.get("reader", {})
        return r_cfg.get("override", {}).get(
            ext,
            r_cfg.get("method", "markitdown"),
        )

    @staticmethod
    def _build_reader(method: str, client, model):
        """
        Instantiate the reader class specified by `method`.
        """
        mapping = {
            "markitdown": lambda: MarkItDownReader(client, model),
            "docling": DoclingReader,
            "pdfplumber": PDFPlumberReader,
            "textract": lambda: TextractReader(client, model),
            "pandas": PandasReader,
        }
        factory = mapping.get(method)
        if not factory:
            raise ValueError(f"Unsupported reader method: {method}")
        return factory()

    # ------------------------------------------------------------------ #
    # public API
    # ------------------------------------------------------------------ #

    def read_file(self, file_path: str) -> str:
        # resolve path
        if not os.path.isabs(file_path):
            file_path = os.path.join(self.input_path, file_path)
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(file_path)
        if p.stat().st_size == 0:
            raise ValueError(f"{file_path} is empty")

        # convert (may return same file)
        with tempfile.TemporaryDirectory() as tmpdir:
            converted = self.converter.convert_file(p, tmpdir)

            # select reader method based on final extension
            reader_method = self._reader_for_extension(converted.suffix)

            # analyzer client/model
            client, model = self.analyzer.get_analyzer(converted.suffix)

            # build reader
            reader = self._build_reader(reader_method, client, model)

            # convert to markdown
            try:
                return reader.convert(str(converted))
            except Exception as exc:
                logging.error(f"Reader failed on {converted}: {exc}")
                raise RuntimeError("Failed to read file")

    def read_file_object(self, file: UploadFile) -> str:
        suffix = "." + file.filename.rsplit(".", 1)[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name
        try:
            return self.read_file(tmp_path)
        finally:
            os.remove(tmp_path)
