import json
import logging
from typing import List

import yaml
from langchain_text_splitters import RecursiveJsonSplitter

from src.domain.splitter.base_splitter import BaseSplitter


class SchemaBasedSplitter(BaseSplitter):
    """
    Splits a hierarchical-schema based document into chunks based on document type.

    The splitter works as follows:

      - If the document is structured (i.e. valid JSON or YAML):
          1. For JSON, loads and normalizes the data (re-dumps it as a JSON string).
          2. For YAML, loads the data and converts it to JSON format.
          3. If the normalized JSON is small (length ≤ max_chunk_size), returns it as a single chunk.
          4. Otherwise, uses LangChain’s RecursiveJsonSplitter to recursively split the JSON string
             into chunks that do not exceed max_chunk_size characters.

      - If the document is unstructured (e.g. CSV-like plaintext):
          Splits the text by newline. The first header_lines lines are treated as header and are
          pre-pended to each chunk, while the remaining rows are grouped into batches of
          max_num_rows rows.

    Args:
        max_num_rows (int): Maximum number of data rows (registers) per chunk for CSV mode.
        header_lines (int): Number of header lines to preserve in CSV mode. Defaults to 1.
        max_chunk_size (int): Maximum number of characters per chunk in JSON mode.
        chunk_overlap (int): Optional number of overlapping characters between JSON chunks.
    """

    def __init__(
        self,
        max_num_rows: int,
        header_lines: int = 1,
        max_chunk_size: int = 300,
        chunk_overlap: int = 0,
    ):
        self.max_num_rows = max_num_rows
        self.header_lines = header_lines
        self.max_chunk_size = max_chunk_size
        self.chunk_overlap = chunk_overlap
        self.json_splitter = RecursiveJsonSplitter(max_chunk_size=self.max_chunk_size)

    def _fix_incomplete_json(self, text: str) -> str:
        """
        Appends a closing bracket if the JSON text appears incomplete.
        Uses a simple heuristic: if text starts with "{" or "[" but does not end with the
        corresponding "}" or "]", it appends the missing character.

        Args:
            text (str): The original JSON text.

        Returns:
            str: A potentially corrected JSON string.
        """
        text_stripped = text.strip()
        if (
            text_stripped  # noqa: W503
            and text_stripped[0] in ("{", "[")  # noqa: W503
            and text_stripped[-1] not in ("}", "]")  # noqa: W503
        ):  # noqa: W503
            closing = "}" if text_stripped[0] == "{" else "]"
            logging.info("JSON appears incomplete; appending closing bracket.")
            return text_stripped + closing
        return text_stripped

    def _parse_structured(self, text: str):
        """
        Attempts to parse the input text as JSON or YAML.

        Tries JSON first; if that fails, it tries YAML.

        Args:
            text (str): The input document text.

        Returns:
            A tuple (data, was_json) where data is the parsed object and was_json
            is a boolean that is True if JSON parsing succeeded, False otherwise.

        Raises:
            ValueError: If the text cannot be parsed as either JSON or YAML.
        """
        fixed_text = self._fix_incomplete_json(text)
        try:
            data = json.loads(fixed_text)
            return data, True
        except Exception:
            try:
                data = yaml.safe_load(text)
                return data, False
            except Exception as e:
                raise ValueError(
                    "Input data is not recognized as valid JSON or YAML"
                ) from e

    def split(self, text: str) -> List[str]:
        """
        Splits the input document text into chunks.

        For structured data (JSON or YAML):
          1. Parses the text as JSON (or YAML if JSON fails).
          2. Normalizes the data by converting it into a JSON string.
          3. If the normalized JSON is short (≤ max_chunk_size characters),
            returns it as a single chunk.
          4. Otherwise, applies RecursiveJsonSplitter to split the JSON.

        For unstructured data (CSV-like plaintext):
          1. Splits on newline.
          2. Preserves the first header_lines lines.
          3. Groups the remaining lines in batches of max_num_rows rows, pre-pending
            the header.

        Args:
            text (str): The full text content of the document.

        Returns:
            List[str]: A list of document chunks.
        """
        structured = False
        data = None
        try:
            data, was_json = self._parse_structured(text)
            structured = True
        except ValueError:
            structured = False

        if structured and isinstance(data, (dict, list)):
            normalized_json = json.dumps(data)
            if len(normalized_json) <= self.max_chunk_size:
                return [normalized_json]
            # Use RecursiveJsonSplitter to split the JSON into chunks.
            chunks = self.json_splitter.split_json(json_data=data)
            # Convert each chunk (which might be a dict) into a JSON string.
            return [
                json.dumps(chunk) if isinstance(chunk, (dict, list)) else str(chunk)
                for chunk in chunks
            ]
        else:
            # Fallback to CSV-like splitting.
            lines = text.splitlines()
            if not lines:
                logging.warning("No content to split.")
                return []
            header = lines[: self.header_lines]
            data_lines = lines[self.header_lines :]
            chunks = []
            for i in range(0, len(data_lines), self.max_num_rows):
                batch = data_lines[i : i + self.max_num_rows]
                chunk = "\n".join(header + batch)
                chunks.append(chunk)
            return chunks
