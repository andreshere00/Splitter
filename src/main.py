import logging
import os
from typing import Any, Dict

import yaml

from src.chunker.chunk_manager import ChunkManager
from src.reader.read_manager import ReadManager
from src.splitter.split_manager import SplitManager


class Application:
    """
    Defines the entry point and workflow of the application.

    This class orchestrates the process of reading files, splitting their content,
    and saving the resulting chunks. It utilizes the `ReadManager`, `SplitManager`,
    and `ChunkManager` classes to perform these tasks.

    Attributes:
        config (dict): Configuration settings for file I/O, logging, and processing.
        read_manager (ReadManager): Manages file reading operations.
        split_manager (SplitManager): Manages text splitting operations.
        chunk_manager (ChunkManager): Manages chunk saving operations.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initializes the Application with the provided configuration.

        Args:
            config (dict): A dictionary containing configuration settings for
                file I/O paths, logging preferences, and processing parameters.
        """
        self.config = config
        self.read_manager = ReadManager(config=self.config)
        self.split_manager = SplitManager(config=self.config)
        self.chunk_manager = ChunkManager(config=self.config)

    def run(self) -> None:
        """
        Executes the main workflow of the application.

        This method performs the following steps:
        1. Determines the absolute input directory path.
        2. Lists all files in the input directory.
        3. For each file:
           a. Reads the file content using `ReadManager`.
           b. Splits the content into chunks using `SplitManager`.
           c. Saves the chunks using `ChunkManager`.

        If the input directory is not found or contains no files, appropriate
        messages are printed.

        Raises:
            FileNotFoundError: If the input directory does not exist.
            Exception: If an error occurs during file reading, splitting, or saving.
        """
        cwd = os.getcwd()
        input_path = self.config.get("file_io", {}).get("input_path", "data/input")
        if not os.path.isabs(input_path):
            input_path = os.path.join(cwd, input_path)

        try:
            files = os.listdir(input_path)
        except FileNotFoundError:
            print(f"Input directory not found: {input_path}")
            return

        if not files:
            print(f"No files found in input directory: {input_path}")
            return

        splitter_method = self.config.get("splitter", {}).get("method", "unknown")

        for file in files:
            input_file = os.path.join(input_path, file)
            if not os.path.isfile(input_file):
                continue

            print(f"\nProcessing file: {input_file}")
            try:
                markdown_text = self.read_manager.read_file(file)
            except Exception as e:
                print(f"Error reading file {input_file}: {e}")
                continue

            chunks = self.split_manager.split_text(markdown_text)
            print(f"Generated {len(chunks)} chunks from the file.")

            basename = os.path.basename(input_file)
            base_filename, original_extension = os.path.splitext(basename)
            saved_files = self.chunk_manager.save_chunks(
                chunks, base_filename, original_extension, splitter_method
            )

            print("Chunks saved to:")
            for f in saved_files:
                print(f)

    @classmethod
    def load_config(cls, config_file: str) -> Dict[str, Any]:
        """
        Loads the YAML configuration file and returns its content as a dictionary.

        Args:
            config_file (str): The path to the YAML configuration file.

        Returns:
            dict: The configuration settings loaded from the YAML file.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            yaml.YAMLError: If there is an error parsing the YAML file.
            Exception: If any other error occurs during file reading.
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
