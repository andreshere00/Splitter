import logging
import os
from typing import Any, Dict

from src.domain.chunker.chunk_manager import ChunkManager
from src.domain.reader.read_manager import ReadManager
from src.domain.splitter.split_manager import SplitManager
from src.infrastructure.helpers.config_loader import load_config
from src.infrastructure.helpers.logging_manager import setup_logging


class Application:
    """
    Orchestrates the document processing workflow.

    The Application class coordinates the reading, splitting, and chunk-saving process
    using the domain-layer components: ReadManager, SplitManager, and ChunkManager.
    It also configures logging based on the provided configuration.

    Attributes:
        config (Dict[str, Any]): Loaded configuration dictionary from the YAML file.
        read_manager (ReadManager): Handles document reading and conversion to text.
        split_manager (SplitManager): Splits text content into smaller chunks.
        chunk_manager (ChunkManager): Handles saving of the generated chunks.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initializes the Application with the given configuration.

        Args:
            config (Dict[str, Any]): Configuration dictionary containing settings for
                file I/O, logging, reader method, splitting strategy, etc.
        """
        self.config = config

        # Setup logging using the configuration from YAML
        setup_logging(self.config.get("logging", {}))

        self.read_manager = ReadManager(config=self.config)
        self.split_manager = SplitManager(config=self.config)
        self.chunk_manager = ChunkManager(config=self.config)

    def run(self) -> None:
        """
        Executes the main application workflow:
        - Reads all files in the input directory.
        - Converts each file to markdown text using the configured reader.
        - Splits the text into chunks based on the configured splitter.
        - Saves the resulting chunks to the output directory.

        If the input directory is missing or contains no valid files, an error is logged.
        """
        cwd = os.getcwd()
        input_path = self.config.get("file_io", {}).get("input_path", "data/input")
        if not os.path.isabs(input_path):
            input_path = os.path.join(cwd, input_path)

        try:
            files = os.listdir(input_path)
        except FileNotFoundError:
            logging.error(f"Input directory not found: {input_path}")
            return

        if not files:
            logging.error(f"No files found in input directory: {input_path}")
            return

        splitter_method = self.config.get("splitter", {}).get("method", "unknown")

        for file in files:
            input_file = os.path.join(input_path, file)
            if not os.path.isfile(input_file):
                continue

            logging.info(f"Processing file: {input_file}")
            try:
                markdown_text = self.read_manager.read_file(file)
            except Exception as e:
                logging.error(f"Error reading file {input_file}: {e}")
                continue

            chunks = self.split_manager.split_text(markdown_text)
            logging.info(f"Generated {len(chunks)} chunks from the file.")

            basename = os.path.basename(input_file)
            base_filename, original_extension = os.path.splitext(basename)
            self.chunk_manager.save_chunks(
                chunks, base_filename, original_extension, splitter_method
            )


def main(config_file: str = "config.yaml") -> None:
    """
    Entry point for the CLI or script execution.

    Loads the configuration from the given YAML file, initializes the Application,
    and runs the document processing workflow.

    Args:
        config_file (str): Path to the YAML configuration file. Defaults to "config.yaml".
    """
    config = load_config(config_file)
    app = Application(config)
    app.run()


if __name__ == "__main__":
    main()
