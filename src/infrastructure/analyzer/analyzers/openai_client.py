import os
from typing import Optional

import openai
from dotenv import load_dotenv

from src.infrastructure.analyzer.analyzers.base_client import BaseLLMClient

load_dotenv()


class OpenAIClient(BaseLLMClient):
    """
    Client for interacting with OpenAI.

    Environment variables required:
    - OPENAI_API_KEY
    - OPENAI_MODEL
    """

    def __init__(self):
        self.client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = os.environ.get("OPENAI_MODEL")

    def get_client(self) -> object:
        return self.client

    def get_model(self) -> Optional[str]:
        return self.model
