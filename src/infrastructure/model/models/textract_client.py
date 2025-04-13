from typing import Optional

import boto3

from src.infrastructure.model.base_client import BaseLLMClient


class TextractClient(BaseLLMClient):
    """
    Client for interacting with Textract.
    """

    def __init__(self):
        self.client = boto3.client("textract")
        self.model = None

    def get_client(self) -> object:
        return self.client

    def get_model(self) -> Optional[str]:
        return self.model
