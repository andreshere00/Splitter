import boto3
from typing import Optional
from src.infrastructure.model.base_client import BaseLLMClient


class TextractClient(BaseLLMClient):
    """
    AWS Textract client that loads the underlying boto3 client.
    """

    def __init__(self, aws_region: str = "us-east-1"):
        self._client = boto3.client("textract", region_name=aws_region)

    def get_client(self) -> object:
        """
        Returns the underlying boto3 Textract client.
        """
        return self._client

    def get_model(self) -> Optional[str]:
        """
        AWS Textract does not require a model name.
        """
        return None
