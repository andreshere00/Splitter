import logging
from typing import Dict, List, Optional

from src.splitter.base_splitter import BaseSplitter
from src.splitter.splitters.fixed_splitter import FixedSplitter
from src.splitter.splitters.paragraph_splitter import ParagraphSplitter
from src.splitter.splitters.recursive_splitter import RecursiveSplitter
from src.splitter.splitters.sentence_splitter import SentenceSplitter
from src.splitter.splitters.word_splitter import WordSplitter

# from src.splitter.splitters.semantic_splitter import SemanticSplitter
# from src.splitter.splitters.paged_splitter import PagedSplitter
# from src.splitter.splitters.row_column_splitter import RowColumnSplitter
# from src.splitter.splitters.schema_based_splitter import SchemaBasedSplitter
# from src.splitter.splitters.auto_splitter import AutoSplitter


class SplitManager:
    """
    Manages the process of splitting text into smaller chunks using a configurable splitter.

    This class utilizes a factory design pattern to instantiate the appropriate splitter based on
    the provided configuration. It then delegates the splitting of input text to the selected
    splitter.

    Attributes:
        config (dict): A dictionary containing configuration settings.
        splitter (BaseSplitter): An instance of the selected splitter.
    """

    def __init__(
        self, config: Optional[Dict] = None, *, split_method: Optional[str] = None
    ) -> None:
        """
        Initializes the SplitManager with a configuration dictionary or with provided arguments.

        If no configuration is provided, a configuration dictionary is built using the provided
        `split_method`. Defaults to `"auto"` if not specified.

        Args:
            config (Optional[dict]): A dictionary containing configuration settings.
            split_method (Optional[str]): The method used for splitting the text.
        """
        if config is None:
            if split_method is None:
                split_method = "auto"
            config = {"splitter": {"method": split_method}}
        self.config = config
        self.splitter = self._create_splitter()

    def _create_splitter(self) -> BaseSplitter:
        """
        Factory method to instantiate the desired splitter from configuration.

        This method loads all parameters for the selected splitting method from the configuration
        and instantiates the corresponding splitter class.

        Returns:
            BaseSplitter: An instance of a class that implements the splitter interface.

        Raises:
            ValueError: If the specified splitting method is not supported.
        """
        splitter_config = self.config.get("splitter", {})
        method = splitter_config.get("method", "auto")

        splitter_mapping = {
            "word": WordSplitter,
            "sentence": SentenceSplitter,
            "paragraph": ParagraphSplitter,
            "fixed": FixedSplitter,
            "recursive": RecursiveSplitter,
            # "semantic": SemanticSplitter,
            # "paged": PagedSplitter,
            # "row-column": RowColumnSplitter,
            # "schema-based": SchemaBasedSplitter,
            # "auto": AutoSplitter,
        }

        splitter_class = splitter_mapping.get(method)
        if not splitter_class:
            raise ValueError(f"Invalid splitting method: {method}")

        # Access the parameters from the nested "methods" key in the configuration.
        params = splitter_config.get("methods", {}).get(method, {})
        return splitter_class(**params)

    def split_text(self, text: str) -> List[str]:
        """
        Splits the provided text into smaller chunks using the configured splitter.

        If the text is empty or only contains whitespace, a warning is logged and an empty list
        is returned. In case of an error during splitting, an error is logged and an empty list
        is returned.

        Args:
            text (str): The text to be split.

        Returns:
            List[str]: A list of text chunks generated by the splitter.
        """
        if not text.strip():
            logging.warning("Empty text provided for splitting.")
            return []
        try:
            return self.splitter.split(text)
        except Exception as e:
            logging.error(f"Error during text splitting: {e}")
            return []
