from typing import Optional

from src.model.base_client import BaseLLMClient
from src.model.models.azure_client import AzureOpenAIClient
from src.model.models.openai_client import OpenAIClient


class LLMClient:
    """
    LLMClient is a factory and wrapper class for initializing and managing large language model (LLM)
    or OCR clients based on a given configuration.

    Depending on the specified method, this class instantiates one of the following:

      - **openai**: Uses `OpenAIClient` to interface with OpenAI's API.
      - **azure**: Uses `AzureOpenAIClient` to interface with Azure OpenAI service.
      - **none**: Disables client functionality (no LLM client is instantiated).

    The class provides helper methods to:
      - Retrieve the underlying client instance.
      - Get the model name associated with the client.
      - Check if a valid client is enabled.
    """

    def __init__(self, method: str):
        """
        Initializes the LLMClient based on the specified method.

        Args:
            method (str): Specifies the client type. Must be one of:
                - "openai" to use OpenAIClient.
                - "azure" to use AzureOpenAIClient.
                - "none" for no client.

        Raises:
            ValueError: If an unsupported method is provided.
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
                f"Unsupported LLM method: '{self.method}'. Only 'openai', 'azure', or 'none' are allowed."  # noqa: E501
            )

    def get_client(self) -> Optional[object]:
        """
        Retrieves the underlying LLM client instance.

        Returns:
            Optional[object]: The client instance if available; otherwise, None.
        """
        if self.client_instance is None:
            return None
        return self.client_instance.get_client()

    def get_model(self) -> Optional[str]:
        """
        Retrieves the model name used by the LLM client.

        Returns:
            Optional[str]: The model name if the client is enabled; otherwise, None.
        """
        if self.client_instance is None:
            return None
        return self.client_instance.get_model()

    def is_enabled(self) -> bool:
        """
        Checks if a valid LLM client is enabled.

        Returns:
            bool: True if a client is instantiated and enabled; otherwise, False.
        """
        return self.client_instance is not None and self.client_instance.is_enabled()
