import logging
from typing import List

from src.utils.splitter import configure_logging, create_splitter, load_config


class SplitManager:
    def __init__(self, config_path: str = "src/config.yaml") -> None:
        self.config = load_config(config_path)
        configure_logging(self.config)
        self.splitter = create_splitter(self.config)

    def split_text(self, text: str) -> List[str]:
        """Split the provided text using the selected splitter."""
        if not text.strip():
            logging.warning("Empty text provided for splitting.")
            return []
        try:
            return self.splitter.split(text)
        except Exception as e:
            logging.error(f"Error during text splitting: {e}")
            return []
