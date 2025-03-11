from abc import ABC, abstractmethod
from typing import List

class BaseSplitter(ABC):
    @abstractmethod
    def split(self, text: str) -> List[str]:
        """
        Split the provided text into chunks.
        
        Args:
            text (str): The text to split.
            
        Returns:
            List[str]: A list of text chunks.
        """
        pass