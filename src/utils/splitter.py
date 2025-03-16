import logging
import os
from typing import Any, Dict

import yaml

from src.splitter.base_splitter import BaseSplitter
from src.splitter.splitters import (  # SemanticSplitter,; PagedSplitter,; RowColumnSplitter,; SchemaBasedSplitter,; AutoSplitter, # noqa: E501
    FixedSplitter,
    ParagraphSplitter,
    RecursiveSplitter,
    SentenceSplitter,
    WordSplitter,
)


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from a YAML file."""
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
            return config or {}
    except (FileNotFoundError, yaml.YAMLError) as e:
        logging.error(f"Error loading config: {e}")
        return {}


def configure_logging(config: Dict[str, Any]) -> None:
    """Configure logging based on the provided configuration."""
    log_config = config.get("logging", {})
    if not log_config.get("enabled", True):
        logging.disable(logging.CRITICAL)
        return

    log_level = log_config.get("level", "ERROR").upper()
    log_format = log_config.get("format", "%(asctime)s - %(levelname)s - %(message)s")
    logging.basicConfig(level=log_level, format=log_format)

    logger = logging.getLogger()
    logger.handlers.clear()  # Remove default handlers

    for handler_cfg in log_config.get("handlers", []):
        if handler_cfg["type"] == "stream":
            handler = logging.StreamHandler()
        elif handler_cfg["type"] == "file":
            filename = handler_cfg.get("filename", "app.log")
            mode = handler_cfg.get("mode", "a")
            log_dir = os.path.dirname(filename)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
            handler = logging.FileHandler(filename, mode=mode)
        else:
            continue
        handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(handler)


def create_splitter(config: Dict[str, Any]) -> BaseSplitter:
    """
    Factory method to instantiate the desired splitter from configuration.
    Loads all the parameters for the selected method from the configuration at once.

    Args:
        config: The configuration dictionary.

    Returns:
        An instance of a class that conforms to the Splitter protocol.
    """
    splitter_config = config.get("splitter", {})
    method = splitter_config.get("method", "auto")

    splitter_mapping = {
        "word": WordSplitter,
        "sentence": SentenceSplitter,
        "paragraph": ParagraphSplitter,
        # "semantic": SemanticSplitter,
        "fixed": FixedSplitter,
        "recursive": RecursiveSplitter,
        # "paged": PagedSplitter,
        # "row-column": RowColumnSplitter,
        # "schema-based": SchemaBasedSplitter,
        # "auto": AutoSplitter,
    }

    splitter_class = splitter_mapping.get(method)
    # if not splitter_class:
    #     logging.error(f"Invalid splitting method: {method}. Defaulting to 'auto'.")
    #     splitter_class = AutoSplitter
    #     params = splitter_config.get("auto", {})
    # else:
    #     params = splitter_config.get(method, {})
    params = splitter_config.get(method, {})

    return splitter_class(**params)
