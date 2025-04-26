import openai

from src.application.api.config import settings
from src.infrastructure.analyzer.analyzers.base_client import BaseLLMClient


class AzureOpenAIClient(BaseLLMClient):
    """
    Client for interacting with Azure OpenAI.

    Environment variables required:
    - AZURE_OPENAI_API_KEY
    - AZURE_OPENAI_API_VERSION
    - AZURE_OPENAI_ENDPOINT
    - AZURE_OPENAI_DEPLOYMENT
    """

    def __init__(self):
        self.client = openai.AzureOpenAI(
            api_key=settings.azure_openai_api_key,
            api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint,
        )
        self.model = settings.azure_openai_deployment

    def get_client(self) -> object:
        return self.client

    def get_model(self) -> str:
        return self.model
