import os
import logging
import datetime
from typing import List
from src.splitter.split_manager import SplitManager
from src.utils.splitter import load_config

class ChunkManager:
    def __init__(self, config_path: str = "src/config.yaml") -> None:
        """
        Initialize the ChunkManager with configuration and a SplitManager instance.
        Reads file I/O paths from the configuration.
        """
        self.config = load_config(config_path)
        self.output_path = self.config.get("file_io", {}).get("output_path", "data/output")
        os.makedirs(self.output_path, exist_ok=True)
        self.split_manager = SplitManager(config_path=config_path)

    def save_chunks(self, chunks: List[str], base_filename: str, original_extension: str, splitter_method: str) -> List[str]:
        """
        Save each chunk in markdown format into a subfolder with the following structure:
        {file_name}_{original_extension}_{date}_{time}_{splitter_method}.
        Chunks are saved as {file_name}_chunk_{number}.md.

        Args:
            chunks: A list of text chunks.
            base_filename: Base name used to construct output folder and chunk file names.
            original_extension: The extension of the original file (e.g., ".md").
            splitter_method: The splitting method used (e.g., "fixed").

        Returns:
            A list of file paths where the chunks have been saved.
        """
        # Get current date and time for folder naming.
        now = datetime.datetime.now()
        date_str = now.strftime("%Y%m%d")
        time_str = now.strftime("%H%M%S")
        
        # Build the folder name.
        folder_name = f"{base_filename}_{original_extension.strip('.')}_{date_str}_{time_str}_{splitter_method}"
        folder_path = os.path.join(self.output_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        saved_files = []
        for i, chunk in enumerate(chunks, start=1):
            chunk_filename = f"{base_filename}_chunk_{i}.md"
            filepath = os.path.join(folder_path, chunk_filename)
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(chunk)
                saved_files.append(filepath)
                logging.info(f"Chunk {i} saved to {filepath}")
            except Exception as e:
                logging.error(f"Error saving chunk {i} to {filepath}: {e}")
        return saved_files
