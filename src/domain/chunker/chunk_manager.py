import datetime
import logging
import os
from typing import Dict, List, Optional

from src.domain.splitter.split_manager import SplitManager


class ChunkManager:
    """
    ChunkManager handles the storage and management of text chunks generated by the SplitManager.

    It is responsible for tasks such as saving chunks to an output directory, aggregating related
    chunks, and optionally converting them into Markdown format.

    Attributes:
        input_path (str): Directory where the original files are located.
        output_path (str): Directory where the resulting chunks will be saved.
        split_method (str): The method used for splitting the text.

    Methods:
        save_chunks(chunks: List[str], file_name: str, extension: str, split_method: str) -> None:
            Saves each chunk to the output directory, naming them based on the original file name
            and chunk index.
    """

    def __init__(
        self,
        config: Optional[Dict] = None,
        *,
        input_path: Optional[str] = None,
        output_path: Optional[str] = None,
        split_method: Optional[str] = None,
    ) -> None:
        """
        Initializes the ChunkManager with a configuration dictionary or with provided arguments.

        If no configuration dictionary is provided, it builds one using the provided arguments.
        The output_path defaults to "<input_path>/output" if not explicitly provided.

        Args:
            config (Optional[dict]): A dictionary containing configuration settings.
            input_path (Optional[str]): The directory path where input files are stored.
            output_path (Optional[str]): The directory path where the chunk files will be saved.
            split_method (Optional[str]): The method used for splitting the text.
        """
        if config is None:
            # Use defaults if not provided.
            if input_path is None:
                input_path = "data/input"
            if output_path is None:
                output_path = os.path.join(input_path, "output")
            if split_method is None:
                split_method = "auto"
            config = {
                "file_io": {
                    "input_path": input_path,
                    "output_path": output_path,
                },
                "splitter": {"method": split_method},
            }
        self.config = config
        self.output_path = self.config.get("file_io", {}).get(
            "output_path", "data/output"
        )
        os.makedirs(self.output_path, exist_ok=True)
        # Initialize the SplitManager with the provided configuration.
        self.split_manager = SplitManager(config=self.config)

    def save_chunks(
        self,
        chunks: List[str],
        base_filename: str,
        original_extension: str,
        splitter_method: str,
    ) -> List[str]:
        """
        Saves the given text chunks into markdown files in a uniquely named directory.

        The directory is created based on the base filename, original file extension,
        current date and time, and the splitter method used. Each chunk is saved in a separate
        markdown file following the naming convention:
        `{base_filename}_{original_extension}_{date}_{time}_chunk_{i}.md`.

        Args:
            chunks (List[str]): A list of text chunks to be saved.
            base_filename (str): The base name of the original file used to construct output
                filenames.
            original_extension (str): The file extension of the original file (e.g., ".md").
            splitter_method (str): The method used for splitting the text (e.g., "fixed").

        Returns:
            List[str]: A list of file paths where the chunks have been saved.
        """
        now = datetime.datetime.now()
        date_str = now.strftime("%Y%m%d")
        time_str = now.strftime("%H%M%S")
        folder_name = f"{base_filename}_{original_extension.strip('.')}_{date_str}_{time_str}_{splitter_method}"  # noqa: E501
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
