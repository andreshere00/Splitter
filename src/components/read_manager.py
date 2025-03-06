import logging
import yaml
import os
from markitdown import MarkItDown  # Hypothetical library that converts various file formats to Markdown

class ReadManager:
    def __init__(self, config_path="src/config.yaml"):
        """Initialize ReadManager with configurations and logging."""
        self.config = self.load_config(config_path)
        self._configure_logging()  # Set up logging first
        
        # Read file I/O paths from config
        file_io_config = self.config.get("file_io", {})
        self.input_path = file_io_config.get("input_path", "data/input")
        self.md = MarkItDown()
        # Optionally store output_path if needed
        # self.output_path = file_io_config.get("output_path", "data/output")

    def load_config(self, config_path):
        """Load configuration from a YAML file."""
        try:
            with open(config_path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logging.error(f"Configuration file not found: {config_path}")
            return {}
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML config: {e}")
            return {}

    def _configure_logging(self):
        """Set up logging configuration based on config.yaml."""
        log_config = self.config.get("logging", {})
        enabled = log_config.get("enabled", True)
        if not enabled:
            logging.disable(logging.CRITICAL)
            return

        log_level = log_config.get("level", "ERROR").upper()
        log_format = log_config.get("format", "%(asctime)s - %(levelname)s - %(message)s")

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

    def read_file(self, file_name):
        """
        Convert any file into Markdown using the markitdown library.
        file_name: the name of the file relative to self.input_path.
        """
        file_path = os.path.join(self.input_path, file_name)
        
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            return ""
        
        try:
            markdown_text = self.md.convert(file_path)
            return markdown_text.text_content
        except Exception as e:
            logging.error(f"Error converting file {file_path} using markitdown: {e}")
            return ""