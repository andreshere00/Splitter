from langchain.text_splitter import RecursiveCharacterTextSplitter

class RecursiveSplitter:
    """
    RecursiveSplitter uses LangChain's RecursiveCharacterTextSplitter to split text
    recursively using a list of separators. It takes a chunk size and an overlap value.
    
    Attributes:
        size (int): The target number of characters per chunk.
        overlap (int): The number of characters to overlap between chunks.
    """
    
    def __init__(self, size=500, overlap=50):
        """
        Initialize the RecursiveSplitter with a fixed chunk size and overlap.
        
        Args:
            size (int): The desired number of characters per chunk.
            overlap (int): The overlapping characters between chunks.
        """
        self.size = size
        self.overlap = overlap
        self.splitter = RecursiveCharacterTextSplitter(
            separators=[
                "\n\n",
                "\n",
                " ",
                ".",
                ",",
                "\u200b",  # Zero-width space
                "\uff0c",  # Fullwidth comma
                "\u3001",  # Ideographic comma
                "\uff0e",  # Fullwidth full stop
                "\u3002",  # Ideographic full stop
                "",
            ],
            chunk_size=self.size,
            chunk_overlap=self.overlap
        )
    
    def split(self, text):
        """
        Splits the input text using the recursive character splitter.
        
        Args:
            text (str): The text to be split.
        
        Returns:
            List[str]: A list of text chunks.
        """
        return self.splitter.split_text(text)
