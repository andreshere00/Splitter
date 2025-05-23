from markitdown import MarkItDown

from src.domain.reader.base_reader import BaseReader


class MarkItDownReader(BaseReader):
    """
    A converter that leverages the MarkItDown library to convert file contents into Markdown
    text.

    This class initializes a MarkItDown instance with optional LLM client and model parameters,
    and exposes a method to convert files to Markdown.

    Attributes:
        llm_client: Optional client for a large language model (LLM) used in conversion.
        llm_model: Optional identifier or instance of the LLM model.
        md (MarkItDown): Instance of the MarkItDown converter initialized with the provided
            LLM parameters.
    """

    def __init__(self, llm_client=None, llm_model=None) -> MarkItDown:
        """
        Initialize the MarkItDownReader with optional LLM client and model.

        Args:
            llm_client: Optional; a client instance for interacting with a large
                language model.
            llm_model: Optional; the language model or model identifier to be used
                for conversion.
        """
        self.llm_client = llm_client
        self.llm_model = llm_model
        self.md = MarkItDown(llm_client=llm_client, llm_model=llm_model)

    def convert(self, file_path: str) -> str:
        """
        Convert the contents of a file to Markdown text.

        Args:
            file_path (str): The path to the file that will be converted.

        Returns:
            str: The Markdown text content resulting from the conversion.
        """
        return self.md.convert(file_path).text_content
