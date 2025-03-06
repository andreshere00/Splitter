from langchain_text_splitters import RecursiveCharacterTextSplitter

class RecursiveSplitter:
    """
    
    """

    def __init__(self, size = 500, overlap = 25):
        """

        Args:

        Returns:
        """
        if size <= 0 or overlap <= 0:
            raise ValueError("Chunk size and overlap parameters should be greater than 0")
        self.size = size
        self.overlap = overlap
        self.splitter = RecursiveCharacterTextSplitter(
                            chunk_size = self.size,
                            chunk_overlap = self.overlap
                        )
        
    def split(self, text):
        """

        Args:

        Returns:
        """

        if not text:
            return []
        
        chunks = self.splitter.create_documents([text])
        return chunks
