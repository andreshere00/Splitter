from src.utils.file_reader import (
    TextFileReader,
    MarkdownFileReader,
    PdfFileReader,
    WordFileReader,
    ExcelFileReader,
    CsvFileReader,
    ImageFileReader,
    SvgFileReader
)

import logging
import yaml
import os


class ReadManager:
    def __init__(self, config_path="config.yaml"):
        """Initialize ReadManager with configurations and logging."""
        self.config = self.load_config(config_path)
        self.readers = self._initialize_readers()
        self._configure_logging()

    def load_config(self, config_path):
        """Load configuration from a YAML file."""
        with open(config_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    def _initialize_readers(self):
        """Dynamically load all available file readers."""
        return {
            ".txt": TextFileReader(),
            ".md": MarkdownFileReader(),
            ".pdf": PdfFileReader(),
            ".docx": WordFileReader(),
            ".xlsx": ExcelFileReader(),
            ".csv": CsvFileReader(),
            ".png": ImageFileReader(),
            ".svg": SvgFileReader(),
        }

    def _configure_logging(self):
        """Set up logging configuration based on config file."""
        log_config = self.config.get('logging', {})
        log_level = log_config.get('level', 'ERROR').upper()
        log_format = log_config.get('format', '%(asctime)s - %(levelname)s - %(message)s')
        
        logging.basicConfig(level=log_level, format=log_format)

        # Add handlers from the config (stream and file)
        for handler_config in log_config.get('handlers', []):
            if handler_config['type'] == 'stream':
                stream_handler = logging.StreamHandler()
                logging.getLogger().addHandler(stream_handler)
            elif handler_config['type'] == 'file':
                file_handler = logging.FileHandler(handler_config['filename'], mode=handler_config.get('mode', 'a'))
                logging.getLogger().addHandler(file_handler)

    def read_file(self, file_path):
        """Determine the file type and call the appropriate reader."""
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            return ""
        
        ext = os.path.splitext(file_path)[1].lower()
        reader = self.readers.get(ext)

        if not reader:
            logging.error(f"Unsupported file type: {ext} for file {file_path}")
            return ""

        return reader.read(file_path)