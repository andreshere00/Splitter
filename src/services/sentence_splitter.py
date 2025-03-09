import re

class SentenceSplitter:
    def __init__(self, num_sentences=5):
        """
        Initialize the splitter with the number of sentences per group.
        :param num_sentences: Number of sentences to group together.
        """
        if num_sentences <= 0:
            raise ValueError("num_sentences must be greater than 0")
        self.num_sentences = num_sentences

    def split(self, text):
        """
        Split the markdown text into groups of sentences.
        :param text: The markdown text to split.
        :return: A list of sentence groups.
        """
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        groups = []
        for i in range(0, len(sentences), self.num_sentences):
            group = " ".join(sentences[i:i + self.num_sentences])
            groups.append(group)
        return groups
