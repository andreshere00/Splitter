from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.domain.splitter.base_splitter import BaseSplitter


class RecursiveSplitter(BaseSplitter):
    """
    Recursively split the input text into smaller chunks not exceeding a specified maximum length.

    This class applies a recursive strategy to break down the text into manageable pieces. It first
    split the text by a fixed number of characters and then further divides any resulting chunk that
    exceeds 'max_length' until all chunks satisfy the length constraint.
    """

    def __init__(self, size: int = 500, overlap: int = 25) -> None:
        """
        Initialize the RecursiveSplitter with a specific chunk size and overlap.

        Args:
            size (int): The desired number of characters per chunk. Must be greater than 0.
            overlap (int): The number of overlapping characters between chunks. Must be greater
                than 0.

        Raises:
            ValueError: If either size or overlap is less than or equal to 0.
        """
        if size <= 0 or overlap <= 0:
            raise ValueError(
                "Chunk size and overlap parameters should be greater than 0"
            )
        self.size: int = size
        self.overlap: int = overlap
        self.splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(
            chunk_size=self.size, chunk_overlap=self.overlap
        )

    def split(self, text: str) -> List[str]:
        """
        Splits the provided text into chunks using the recursive splitting strategy.
        The output from the underlying splitter is converted into a list of strings.
        If an element has a 'page_content' attribute, that attribute is used; otherwise,
        the element is assumed to be a string.

        Args:
            text (str): The input text to split.

        Returns:
            List[str]: A list of text chunks (strings) resulting from the splitting operation.
                       Returns an empty list if the input text is empty.
        """
        if not text:
            return []

        documents = self.splitter.split_text(text)
        chunks = [
            doc if isinstance(doc, str) else doc.page_content for doc in documents
        ]
        return chunks
