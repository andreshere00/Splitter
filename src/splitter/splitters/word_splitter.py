from typing import List

from src.splitter.base_splitter import BaseSplitter


class WordSplitter(BaseSplitter):
    """
    Splits the input text into individual words.

    This class tokenizes the text into words using whitespace and punctuation as delimiters.
    It is particularly useful for further processing that requires analysis at the word level.
    """

    def __init__(self, num_words: int = 10) -> None:
        """
        Initialize the splitter with the number of words per chunk.

        Args:
            num_words (int): The desired number of words per chunk.
                             Must be greater than 0.
        """
        if num_words <= 0:
            raise ValueError("num_words must be greater than 0")
        self.num_words = num_words

    def split(self, text: str) -> List[str]:
        """
        Split the text into chunks of words.

        Args:
            text (str): The input text.

        Returns:
            List[str]: A list of text chunks.
        """
        words = text.split()
        groups = []
        for i in range(0, len(words), self.num_words):
            group = " ".join(words[i : i + self.num_words])
            groups.append(group)
        return groups
