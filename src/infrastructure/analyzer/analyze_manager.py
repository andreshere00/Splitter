import logging
from pathlib import Path
from typing import Optional, Tuple, Union

from src.infrastructure.analyzer.analyzers import (
    AzureOpenAIClient,
    BaseLLMClient,
    HuggingFaceClient,
    OpenAIClient,
    TextractClient,
)
from src.infrastructure.helpers.config_loader import load_config


class AnalyzeManager:
    """
    Factory for selecting an analyzer based on file extension + YAML config.
    get_analyzer(ext) → (client_instance or None, analyzer_name)
    """

    _CREATORS = {
        "openai": OpenAIClient,
        "azure-openai": AzureOpenAIClient,
        "huggingface": HuggingFaceClient,
        "textract": TextractClient,
    }

    def __init__(self, config_path: Union[str, Path]):
        cfg = load_config(config_path)
        anl = cfg.get("analyzer", {})
        self._default = anl.get("default", "none")
        # e.g. {"png": "azure-openai", "base64": "azure-openai"}
        self._overrides = {
            ext.lower(): name for ext, name in anl.get("override", {}).items()
        }

    def _get_analyzer_name(self, ext: str) -> str:
        """
        Strip leading dot, lowercase, then check overrides/default.
        """
        e = ext.lower().lstrip(".")
        return self._overrides.get(e, self._default)

    def _make_client(self, name: str) -> Optional[BaseLLMClient]:
        """
        Instantiate the client class for `name`, or return None if name == "none".
        """
        if name == "none":
            return None

        cls = self._CREATORS.get(name)
        if cls is None:
            raise ValueError(f"No analyzer registered for '{name}'")
        return cls()

    def get_analyzer(self, file_ext: str) -> Tuple[Optional[BaseLLMClient], str]:
        """
        Public API → pass in a suffix (e.g. ".png" or "pdf")
        Returns:
          client: BaseLLMClient | None
          name:   the analyzer key from the config (e.g. "azure-openai", "none")
        """
        name = self._get_analyzer_name(file_ext)
        client = self._make_client(name)
        logging.debug(f"AnalyzerManager: '{file_ext}' → '{name}' → {client!r}")
        return client, name
