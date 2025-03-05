import logging
import yaml
import argparse
import os

from src.services.word_splitter import WordSplitter
from src.services.sentence_splitter import SentenceSplitter
from src.services.paragraph_splitter import ParagraphSplitter
from src.services.semantic_splitter import SemanticSplitter
from src.services.fixed_splitter import FixedSplitter
from src.services.paged_splitter import PagedSplitter
from src.services.recursive_splitter import RecursiveSplitter
from src.services.row_column_splitter import RowColumnSplitter
from src.services.schema_based_splitter import SchemaBasedSplitter
from src.services.auto_splitter import AutoSplitter


class SplitManager:
    def __init__(self, config_path="src/config.yaml"):
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
        """Set up logging configuration based on the config file."""
        log_config = self.config.get("logging", {})
        enabled = log_config.get("enabled", True)
        if not enabled:
            logging.disable(logging.CRITICAL)
            return

        log_level = log_config.get("level", "ERROR").upper()
        log_format = log_config.get("format", "%(asctime)s - %(levelname)s - %(message)s")

        # Set basic configuration for logging
        logging.basicConfig(level=log_level, format=log_format)
        logger = logging.getLogger()
        logger.handlers.clear()

        # Add handlers defined in the configuration
        for handler_config in log_config.get("handlers", []):
            if handler_config["type"] == "stream":
                stream_handler = logging.StreamHandler()
                stream_handler.setFormatter(logging.Formatter(log_format))
                logger.addHandler(stream_handler)
            elif handler_config["type"] == "file":
                filename = handler_config.get("filename", "app.log")
                mode = handler_config.get("mode", "a")
                # Ensure the directory exists before creating the FileHandler
                log_dir = os.path.dirname(filename)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir, exist_ok=True)
                file_handler = logging.FileHandler(filename, mode=mode)
                file_handler.setFormatter(logging.Formatter(log_format))
                logger.addHandler(file_handler)

    def _initialize_splitter(self):
        """Dynamically select the splitting strategy based on the config or console argument."""
        splitter_config = self.config.get("splitter", {})

        # Support console argument override
        parser = argparse.ArgumentParser(description="Select the splitting method.")
        parser.add_argument("--method", type=str, help="Splitting method (word, sentence, paragraph, etc.)")
        args, unknown = parser.parse_known_args()

        # Use console argument if provided, otherwise use config
        method = args.method if args.method else splitter_config.get("method", "auto")

        splitters = {
            "word": WordSplitter(num_words=splitter_config.get("word", {}).get("num_words", 100)),
            "sentence": SentenceSplitter(num_sentences=splitter_config.get("sentence", {}).get("num_sentences", 5)),
            "paragraph": ParagraphSplitter(num_paragraphs=splitter_config.get("paragraph", {}).get("num_paragraphs", 3)),
            "semantic": SemanticSplitter(
                language_model=splitter_config.get("semantic", {}).get("language_model", "bert-base-uncased"),
                overlap=splitter_config.get("semantic", {}).get("overlap", 0.2)
            ),
            "fixed": FixedSplitter(size=splitter_config.get("fixed", {}).get("size", 500)),
            "recursive": RecursiveSplitter(
                size=splitter_config.get("recursive", {}).get("size", 500),
                overlap=splitter_config.get("recursive", {}).get("overlap", 50)
            ),
            "paged": PagedSplitter(
                num_pages=splitter_config.get("paged", {}).get("num_pages", 1),
                overlap=splitter_config.get("paged", {}).get("overlap", 0.1)
            ),
            "row-column": RowColumnSplitter(
                num_columns=splitter_config.get("row-column", {}).get("num_columns", 2),
                column_names=splitter_config.get("row-column", {}).get("column_names", ["Column1", "Column2"]),
                num_rows=splitter_config.get("row-column", {}).get("num_rows", 5),
                row_names=splitter_config.get("row-column", {}).get("row_names", ["Row1", "Row2"])
            ),
            "schema-based": SchemaBasedSplitter(
                num_registers=splitter_config.get("schema-based", {}).get("num_registers", 50),
                overlap=splitter_config.get("schema-based", {}).get("overlap", 5)
            ),
            "auto": AutoSplitter(
                methods=splitter_config.get("auto", {}).get("methods", ["sentence", "semantic"]),
                fallback=splitter_config.get("auto", {}).get("fallback", "paragraph")
            ),
        }

        if method not in splitters:
            logging.error(f"Invalid splitting method: {method}. Defaulting to 'auto'.")
            return splitters["auto"]

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
