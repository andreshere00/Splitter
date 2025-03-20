import logging
import os
from typing import Any, Dict, Optional

from markitdown import MarkItDown

from src.utils.logging_manager import LoggingManager


class ReadManager:
    """
    Manages the process of reading files from a specified input directory
    and converting them into Markdown format.

    This class is responsible for:
    - Configuring logging based on the provided configuration.
    - Reading files from a configured input directory.
    - Converting files (TXT, MD, DOCX, PDF) into Markdown format.

    Attributes:
        config (Dict[str, Any]): A dictionary containing configuration settings.
        input_path (str): The directory path where input files are stored.
        md (Any): The Markdown converter instance used for file conversion.
    """

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        *,
        input_path: Optional[str] = None,
        markdown_converter: Any = None,
    ) -> None:
        """
        Initializes the ReadManager with a configuration dictionary or with provided arguments.

        If no configuration dictionary is provided, it builds one using the provided arguments.

        Args:
            config (Optional[Dict[str, Any]]): A dictionary containing configuration settings.
            input_path (Optional[str]): The directory path where input files are stored.
            markdown_converter (Any, optional): An instance of a Markdown converter.
                                                Defaults to `MarkItDown`.
        """
        if config is None:
            if input_path is None:
                input_path = "data/input"
            config = {"file_io": {"input_path": input_path}}
        self.config = config
        self.logging = LoggingManager.configure_logging(self.config)
        file_io_config = self.config.get("file_io", {})
        self.input_path = file_io_config.get("input_path", "data/input")
        # Use dependency injection for the Markdown converter.
        self.md = markdown_converter if markdown_converter is not None else MarkItDown()

    def read_file(self, file_name: str) -> str:
        """
        Reads and converts a file to Markdown format.

        The file is retrieved from the configured input directory.
        Only files with extensions `.txt`, `.md`, `.docx`, and `.pdf` are supported.
        The converted text is returned as a Markdown string.

        Args:
            file_name (str): The name of the file to be read and converted.

        Returns:
            str: The Markdown text content of the converted file.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is empty or has an unsupported extension.
            RuntimeError: If an error occurs during file conversion.
        """
        file_path = os.path.join(self.input_path, file_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if os.path.getsize(file_path) == 0:
            raise ValueError("File is empty")

        if not file_name.lower().endswith((".txt", ".md", ".docx", ".pdf")):
            raise ValueError("Invalid file extension")

        try:
            markdown_text = self.md.convert(file_path)
            return markdown_text.text_content
        except Exception as e:
            logging.error(f"Error converting file {file_path} using markitdown: {e}")
            raise RuntimeError("Failed to convert file")
