import os
import logging
from typing import List
from src.splitter.split_manager import SplitManager
from src.utils.splitter import load_config

class ChunkManager:
    def __init__(self, config_path: str = "src/config.yaml") -> None:
        """
        Initialize the ChunkManager with configuration and a SplitManager instance.
        Reads file I/O paths from the configuration.
        
        Args:
            config_path: Path to the configuration file.
        """
        self.config = load_config(config_path)
        self.output_path = self.config.get("file_io", {}).get("output_path", "data/output")
        os.makedirs(self.output_path, exist_ok=True)
        self.split_manager = SplitManager(config_path=config_path)

    def save_chunks(self, chunks: List[str], base_filename: str) -> List[str]:
        """
        Save each chunk in markdown format to the output directory.
        
        Args:
            chunks: A list of text chunks.
            base_filename: Base name used to construct each output file's name.
        
        Returns:
            A list of file paths where the chunks have been saved.
        """
        saved_files = []
        for i, chunk in enumerate(chunks, start=1):
            filename = f"{base_filename}_chunk_{i}.md"  # Use markdown file extension
            filepath = os.path.join(self.output_path, filename)
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(chunk)
                saved_files.append(filepath)
                logging.info(f"Chunk {i} saved to {filepath}")
            except Exception as e:
                logging.error(f"Error saving chunk {i} to {filepath}: {e}")
        return saved_files

    def process_file(self, input_file: str) -> List[str]:
        """
        Read the contents of an input file, split the text using SplitManager,
        and save the resulting chunks in markdown format.
        
        Args:
            input_file: Path to the input file to be processed.
        
        Returns:
            A list of file paths where the chunks have been saved.
        """
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            logging.error(f"Error reading file {input_file}: {e}")
            return []
        
        base_filename = os.path.splitext(os.path.basename(input_file))[0]
        # Use the SplitManager to obtain a list of chunks
        chunks = self.split_manager.split_text(text)
        return self.save_chunks(chunks, base_filename)
