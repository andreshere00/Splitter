import logging
import os

import yaml

from src.domain.reader.base_reader import BaseReader


class YAMLReader(BaseReader):
    """
    YAMLReader reads YAML files and converts their content into a Python dictionary.

    It expects the input file to be in valid YAML format and will raise an error if the file
    is empty or the YAML is invalid.
    """

    def convert(self, file_path: str) -> str | dict:
        """
        Reads a YAML file from the given path and returns its contents as a dictionary.

        Args:
            file_path (str): The path to the YAML file.

        Returns:
            dict: The parsed YAML data.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is empty or contains invalid YAML.
        """
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if os.path.getsize(file_path) == 0:
            raise ValueError("File is empty")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                # If the YAML file is empty, safe_load returns None. Convert that to an empty dict.
                if data is None:
                    return {}
                return data
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML file {file_path}: {e}")
            raise ValueError("Invalid YAML content") from e
