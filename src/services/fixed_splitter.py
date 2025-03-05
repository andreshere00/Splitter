# src/services/fixed_splitter.py

class FixedSplitter:
    """
    FixedSplitter divides the input text into chunks of a fixed number of characters.

    Attributes:
        size (int): The number of characters per chunk.
    """
    
    def __init__(self, size=500):
        """
        Initialize the FixedSplitter with a specific chunk size.
        
        Args:
            size (int): Number of characters in each chunk.
        """
        self.size = size

    def split(self, text):
        """
        Splits the provided text into chunks, each with a fixed number of characters.
        
        Args:
            text (str): The text to split.
        
        Returns:
            List[str]: A list of text chunks.
        """
        if not text:
            return []
        
        # Create chunks of the given fixed size.
        chunks = [text[i:i+self.size] for i in range(0, len(text), self.size)]
        return chunks
