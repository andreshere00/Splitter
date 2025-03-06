from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

class RecursiveSplitter:
    """
    RecursiveSplitter uses LangChain's RecursiveCharacterTextSplitter to split a text
    recursively into chunks based on a defined chunk size and overlap.

    Attributes:
        size (int): The target number of characters per chunk.
        overlap (int): The number of overlapping characters between chunks.
        splitter (RecursiveCharacterTextSplitter): The underlying splitter instance.
    """
    
    def __init__(self, size: int = 500, overlap: int = 25) -> None:
        """
        Initialize the RecursiveSplitter with a specific chunk size and overlap.

        Args:
            size (int): The desired number of characters per chunk. Must be greater than 0.
            overlap (int): The number of overlapping characters between chunks. Must be greater than 0.

        Raises:
            ValueError: If either size or overlap is less than or equal to 0.
        """
        if size <= 0 or overlap <= 0:
            raise ValueError("Chunk size and overlap parameters should be greater than 0")
        self.size: int = size
        self.overlap: int = overlap
        self.splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(
            chunk_size=self.size,
            chunk_overlap=self.overlap
        )
        
    def split(self, text: str) -> List[str]:
        """
        Splits the provided text into chunks using the recursive splitting strategy.

        Args:
            text (str): The input text to split.

        Returns:
            List[str]: A list of text chunks resulting from the splitting operation.
                       Returns an empty list if the input text is empty.
        """
        if not text:
            return []
        
        chunks = self.splitter.create_documents([text])
        return chunks
