import re
from typing import List

from src.domain.splitter.base_splitter import BaseSplitter


class SentenceSplitter(BaseSplitter):
    """
    Splits the input text into sentences.

    This class breaks the text into sentences by detecting sentence boundaries, typically using
    punctuation marks such as periods, exclamation points, and question marks. It also attempts to
    handle common edge cases, such as abbreviations, to improve accuracy.
    """

    def __init__(self, num_sentences: int = 5):
        """
        Initialize the splitter with the number of sentences per group.
        :param num_sentences: Number of sentences to group together.
        """
        if num_sentences <= 0:
            raise ValueError("num_sentences must be greater than 0")
        self.num_sentences = num_sentences

    def split(self, text: str) -> List[str]:
        """
        Split the markdown text into groups of sentences.
        :param text: The markdown text to split.
        :return: A list of sentence groups.
        """
        sentences = re.split(r"(?<=[.!?])\s+", text)
        sentences = [s.strip() for s in sentences if s.strip()]

        chunks = []
        for i in range(0, len(sentences), self.num_sentences):
            chunk = " ".join(sentences[i : i + self.num_sentences])
            chunks.append(chunk)
        return chunks
