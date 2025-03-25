from typing import Optional

from src.model.base_client import BaseLLMClient
from src.model.models.azure_client import AzureOpenAIClient
from src.model.models.openai_client import OpenAIClient


class LLMClient:
    """
    Factory and wrapper for loading either an OpenAI or Azure OpenAI client based on configuration.
    """

    def __init__(self, method: str):
        """
        Initializes the LLM client.

        Args:
            method (str): Either "openai", "azure", or "none".
        """
        self.method = method.lower()
        if self.method == "openai":
            self.client_instance: Optional[BaseLLMClient] = OpenAIClient()
        elif self.method == "azure":
            self.client_instance: Optional[BaseLLMClient] = AzureOpenAIClient()
        elif self.method == "none":
            self.client_instance = None
        else:
            raise ValueError(
                f"Unsupported LLM method: '{self.method}'. Only 'openai', 'azure', \
                    or 'none' are allowed."
            )

    def get_client(self) -> Optional[object]:
        """
        Returns the underlying LLM client.
        """
        if self.client_instance is None:
            return None
        return self.client_instance.get_client()

    def get_model(self) -> Optional[str]:
        """
        Returns the model name to be used with the LLM client.
        """
        if self.client_instance is None:
            return None
        return self.client_instance.get_model()

    def is_enabled(self) -> bool:
        """
        Returns True if a valid LLM client is initialized.
        """
        return self.client_instance is not None and self.client_instance.is_enabled()
