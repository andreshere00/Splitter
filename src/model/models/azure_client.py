import os
from typing import Optional

import openai
from dotenv import load_dotenv

from src.model.base_client import BaseLLMClient

load_dotenv()


class AzureOpenAIClient(BaseLLMClient):
    """
    Client for interacting with Azure OpenAI.
    """

    def __init__(self):
        self.client = openai.AzureOpenAI(
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.environ.get("AZURE_OPENAI_API_ENDPOINT"),
        )
        self.model = os.environ.get("AZURE_OPENAI_API_DEPLOYMENT")

    def get_client(self) -> object:
        return self.client

    def get_model(self) -> Optional[str]:
        return self.model
