import logging

import yaml


def load_config(config_file: str) -> dict:
    """
    Loads the YAML configuration file and returns its content as a dictionary.
    """
    try:
        with open(config_file, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    except FileNotFoundError as e:
        logging.error(f"Configuration file not found: {config_file}")
        raise e
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML configuration: {e}")
        raise e
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        raise e
