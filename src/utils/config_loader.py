from typing import Dict, Optional

import yaml


def load_config_file(path: str = "src/config.yaml") -> Dict:
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}  # Return empty if config file doesn't exist


def merge_config(
    base_config: Optional[Dict] = None,
    input_path: Optional[str] = None,
    output_path: Optional[str] = None,
    split_method: Optional[str] = None,
) -> Dict:
    """
    Merges user-provided values with defaults and base config.

    Args:
        base_config: Original config from YAML or elsewhere.
        input_path: Override for file_io.input_path
        output_path: Override for file_io.output_path
        split_method: Override for splitter.method

    Returns:
        Merged dictionary.
    """
    config = base_config.copy() if base_config else {}

    file_io = config.setdefault("file_io", {})
    splitter = config.setdefault("splitter", {})

    if input_path:
        file_io["input_path"] = input_path
    if output_path:
        file_io["output_path"] = output_path
    if split_method:
        splitter["method"] = split_method

    return config
