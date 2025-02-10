import logging
import yaml
import os

from src.services.word_splitter import WordSplitter
from src.services.sentence_splitter import SentenceSplitter
from src.services.paragraph_splitter import ParagraphSplitter
from src.services.semantic_splitter import SemanticSplitter
from src.services.fixed_splitter import FixedSplitter
from src.services.paged_splitter import PagedSplitter


class SplitManager:
    def __init__(self, config_path="config.yaml"):
        """Initialize SplitManager with configurations and logging."""
        self.config = self.load_config(config_path)
        self._configure_logging()
        self.splitter = self._initialize_splitter()

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
                file_handler = logging.FileHandler(handler_config["filename"], mode=handler_config.get("mode", "a"))
                file_handler.setFormatter(logging.Formatter(log_format))
                logger.addHandler(file_handler)

    def _initialize_splitter(self):
        """Dynamically select the splitting strategy based on config."""
        splitter_config = self.config.get("splitter", {})
        method = splitter_config.get("method", "paragraph")
        config = splitter_config.get("config", {})

        splitters = {
            "word": WordSplitter(),
            "sentence": SentenceSplitter(),
            "paragraph": ParagraphSplitter(),
            "semantic": SemanticSplitter(threshold=config.get("semantic", {}).get("threshold", 0.8)),
            "fixed": FixedSplitter(size=config.get("fixed", {}).get("size", 500)),
            "paged": PagedSplitter(allowed_docs=config.get("paged", {}).get("allowed_documents", ["pdf", "docx", "xlsx"])),
        }

        if method not in splitters:
            logging.error(f"Invalid splitting method: {method}. Defaulting to paragraph.")
            return ParagraphSplitter()

        return splitters[method]

    def split_text(self, text):
        """Apply the selected splitting technique to the input text."""
        if not text.strip():
            logging.warning("Empty text provided for splitting.")
            return []

        try:
            return self.splitter.split(text)
        except Exception as e:
            logging.error(f"Error during text splitting: {e}")
            return []
