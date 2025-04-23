import os
from typing import Optional

import boto3

from src.infrastructure.analyzer.vlm.base_client import BaseLLMClient


class TextractClient(BaseLLMClient):
    """
    Client for interacting with AWS Textract using environment-based credentials.

    Environment variables required:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_SESSION_TOKEN (optional)
    - AWS_REGION (e.g. 'us-east-1')
    """

    def __init__(self):
        self.client = boto3.client(
            "textract",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=os.getenv("AWS_SESSION_TOKEN"),  # optional
            region_name=os.getenv("AWS_REGION", "us-east-1"),  # fallback region
        )
        self.model = None

    def get_client(self) -> object:
        return self.client

    def get_model(self) -> Optional[str]:
        return self.model
