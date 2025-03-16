import logging
import os
from typing import Any, Dict

import yaml
from markitdown import MarkItDown


class ReadManager:
    """
    ReadManager is responsible for loading configurations, setting up logging,
    and converting files to Markdown format using a Markdown converter.

    This class reads configuration settings from a YAML file, configures logging
    based on those settings, and determines the input directory for file I/O.
    It also performs file validation and conversion to Markdown format using the
    MarkItDown library (or a user-provided converter) to handle files with extensions
    such as '.txt', '.md', '.docx', and '.pdf'.

    Attributes:
        config (Dict[str, Any]): A dictionary containing configuration values loaded from
            the YAML file.
        input_path (str): The directory path where input files are stored, as specified in
            the configuration.
        md (Any): The Markdown converter instance used to convert files to Markdown.
                  Allows for dependency injection; defaults to an instance of MarkItDown.
    """

    def __init__(
        self, config_path: str = "src/config.yaml", markdown_converter: Any = None
    ) -> None:
        """
        Initialize the ReadManager with configurations, logging, and a Markdown converter.

        Args:
            config_path (str): Path to the YAML configuration file.
                               Defaults to "src/config.yaml".
            markdown_converter (Any, optional): An instance of a Markdown converter.
                                                If None, defaults to MarkItDown.
        """
        self.config = self.load_config(config_path)
        self._configure_logging()

        file_io_config = self.config.get("file_io", {})
        self.input_path = file_io_config.get("input_path", "data/input")

        # Allow dependency injection for the Markdown converter
        self.md = markdown_converter if markdown_converter is not None else MarkItDown()

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from a YAML file.

        Args:
            config_path (str): The path to the YAML configuration file.

        Returns:
            Dict[str, Any]: The configuration as a dictionary. Returns an empty
                dictionary if an error occurs.
        """
        try:
            with open(config_path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logging.error(f"Configuration file not found: {config_path}")
            return {}
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML config: {e}")
            return {}

    def _configure_logging(self) -> None:
        """
        Set up logging configuration based on the settings in the YAML configuration.

        The logging configuration is read from the 'logging' section of the configuration.
        It supports both stream and file handlers. If logging is disabled in the config,
        all logging is turned off.
        """
        log_config = self.config.get("logging", {})
        enabled = log_config.get("enabled", True)
        if not enabled:
            logging.disable(logging.CRITICAL)
            return

        log_level = log_config.get("level", "ERROR").upper()
        log_format = log_config.get(
            "format", "%(asctime)s - %(levelname)s - %(message)s"
        )

        logging.basicConfig(level=log_level, format=log_format)
        logger = logging.getLogger()
        logger.handlers.clear()

        for handler_config in log_config.get("handlers", []):
            if handler_config["type"] == "stream":
                stream_handler = logging.StreamHandler()
                stream_handler.setFormatter(logging.Formatter(log_format))
                logger.addHandler(stream_handler)
            elif handler_config["type"] == "file":
                log_file = handler_config.get("filename", "app.log")
                log_mode = handler_config.get("mode", "a")
                log_dir = os.path.dirname(log_file)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir, exist_ok=True)
                file_handler = logging.FileHandler(log_file, mode=log_mode)
                file_handler.setFormatter(logging.Formatter(log_format))
                logger.addHandler(file_handler)

    def read_file(self, file_name: str) -> str:
        """
        Convert any supported file into Markdown format using the markitdown library.

        This method constructs the full file path based on the configured input directory,
        validates that the file exists, is non-empty, and has a supported extension. It then
        converts the file to Markdown format using the provided or default Markdown converter.

        Supported file extensions are: '.txt', '.md', '.docx', and '.pdf'.

        Args:
            file_name (str): The name of the file to be read and converted.

        Returns:
            str: The Markdown text content of the converted file.

        Raises:
            FileNotFoundError: If the file does not exist at the computed path.
            ValueError: If the file is empty or the file extension is not supported.
            RuntimeError: If an error occurs during the Markdown conversion process.
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
