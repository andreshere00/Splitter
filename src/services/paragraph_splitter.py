from typing import List

from src.services.base_splitter import BaseSplitter


class ParagraphSplitter(BaseSplitter):
    """
    ParagraphSplitter divides the input text into chunks by paragraphs.
    
    Attributes:
        num_paragraphs (int): The number of paragraphs to include in each chunk.
                              Must be greater than 0 if specified.
    """
    
    def __init__(self, num_paragraphs:int = None) -> None:
        """
        Initialize the ParagraphSplitter.
        
        Args:
            num_paragraphs (int, optional): Number of paragraphs per chunk. 
                                            If None, each paragraph is treated as a separate chunk.
        """
        if num_paragraphs is not None and num_paragraphs <= 0:
            raise ValueError("Number of paragraphs must be greater than 0")
        self.num_paragraphs = num_paragraphs

    def split(self, text: str) -> List[str]:
        """
        Splits the provided text into paragraphs.
        
        A paragraph is considered as text separated by one or more newline characters.
        
        Args:
            text (str): The text to split.
        
        Returns:
            List[str]: A list of text chunks (each chunk is either a single paragraph or a group of paragraphs).
        """
        # Split text by newlines and filter out empty strings.
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        
        # If num_paragraphs is not specified, return each paragraph separately.
        if self.num_paragraphs is None:
            return paragraphs
        
        # Group paragraphs into chunks of num_paragraphs each.
        chunks = []
        for i in range(0, len(paragraphs), self.num_paragraphs):
            chunk = "\n\n".join(paragraphs[i:i + self.num_paragraphs])
            chunks.append(chunk)
        
        return chunks
