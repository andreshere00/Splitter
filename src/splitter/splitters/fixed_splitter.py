from typing import List

from src.splitter.base_splitter import BaseSplitter


class FixedSplitter(BaseSplitter):
    """
    Split the input text into fixed-size chunks.

    This class divides the provided text into contiguous substrings, each with a length equal to
    the specified 'chunk_size'. If the total text length is not an exact multiple of 'chunk_size',
    the final chunk will contain the remaining characters, which may be shorter than 'chunk_size'.
    """

    def __init__(self, size: int = 500) -> None:
        """
        Initialize the FixedSplitter with a specific chunk size.

        Args:
            size (int): Number of characters in each chunk.
        """
        if size <= 0:
            raise ValueError("Chunk size must be greater than 0")
        self.size = size

    def split(self, text: str) -> List[str]:
        """
        Splits the provided text into chunks, each with a fixed number of characters.
        If the chunk size is larger than the document size, the entire document is returned
            as one chunk.

        Args:
            text (str): The text to split.

        Returns:
            List[str]: A list of text chunks.
        """
        if not text:
            return []

        # Use the document length as effective size if the specified size is
        # larger.
        effective_size = self.size if self.size < len(text) else len(text)
        chunks = [
            text[i : i + effective_size] for i in range(0, len(text), effective_size)
        ]
        return chunks
