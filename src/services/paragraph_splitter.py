class ParagraphSplitter:
    """
    ParagraphSplitter divides the input text into chunks by paragraphs.
    
    Attributes:
        num_paragraphs (int): Optional. The number of paragraphs to include in each chunk.
                              If not specified, each paragraph is returned as a separate chunk.
    """
    
    def __init__(self, num_paragraphs=None):
        """
        Initialize the ParagraphSplitter.
        
        Args:
            num_paragraphs (int, optional): Number of paragraphs per chunk. 
                                            If None, each paragraph is treated as a chunk.
        """
        self.num_paragraphs = num_paragraphs

    def split(self, text):
        """
        Splits the provided text into paragraphs.
        
        A paragraph is considered as text separated by one or more newline characters.
        
        Args:
            text (str): The text to split.
        
        Returns:
            List[str]: A list of text chunks (paragraphs or groups of paragraphs).
        """
        # Split text by newlines and filter out empty strings
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        
        if self.num_paragraphs is None or self.num_paragraphs < 1:
            return paragraphs
        
        # Group paragraphs into chunks of num_paragraphs each
        chunks = []
        for i in range(0, len(paragraphs), self.num_paragraphs):
            chunk = "\n\n".join(paragraphs[i:i+self.num_paragraphs])
            chunks.append(chunk)
        
        return chunks
