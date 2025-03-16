import logging
from typing import Any, Dict

import yaml


class ConfigLoader:
    def load_config(config_path: str) -> Dict[str, Any]:
        """Load configuration from a YAML file."""
        try:
            with open(config_path, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)
                return config or {}
        except (FileNotFoundError, yaml.YAMLError) as e:
            logging.error(f"Error loading config: {e}")
            return {}
