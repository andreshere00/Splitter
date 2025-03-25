from markitdown import MarkItDown

from src.reader.base_reader import BaseReader


class MarkItDownConverter(BaseReader):
    def __init__(self, llm_client=None, llm_model=None):
        self.md = MarkItDown(llm_client=llm_client, llm_model=llm_model)

    def convert(self, file_path: str) -> str:
        return self.md.convert(file_path).text_content
