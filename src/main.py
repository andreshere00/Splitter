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
    Coordinates reading, splitting, and saving chunks.
    """

    def __init__(self, config: Dict[str, Any], config_path: str) -> None:
        self.config = config
        self.config_path = config_path

        setup_logging(self.config.get("logging", {}))

        # Pass the path only to ReadManager (SplitManager doesn’t need it)
        self.read_manager = ReadManager(
            config=self.config, config_path=self.config_path
        )
        self.split_manager = SplitManager(config=self.config)
        self.chunk_manager = ChunkManager(config=self.config)

    # ------------------------------------------------------------------ #
    # main workflow
    # ------------------------------------------------------------------ #

    def run(self) -> None:
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

        splitter_method = self.config.get("splitter", {}).get("default", "unknown")

        for fname in files:
            # Skip hidden/metadata files like .DS_Store
            if fname.startswith("."):
                continue

            infile = os.path.join(input_path, fname)
            if not os.path.isfile(infile):
                continue

            logging.info(f"Processing file: {infile}")
            try:
                md_text = self.read_manager.read_file(fname)
            except Exception as exc:
                logging.error(f"Error reading {infile}: {exc}")
                continue

            chunks = self.split_manager.split_text(md_text)
            logging.info(f"Generated {len(chunks)} chunks from {fname}")

            base, ext = os.path.splitext(fname)
            self.chunk_manager.save_chunks(chunks, base, ext, splitter_method)


# ---------------------------------------------------------------------- #
# CLI entry point
# ---------------------------------------------------------------------- #


def main(config_file: str = "config.yaml") -> None:
    cfg = load_config(config_file)
    Application(cfg, config_file).run()


if __name__ == "__main__":
    import sys

    main(sys.argv[1] if len(sys.argv) > 1 else "config.yaml")
