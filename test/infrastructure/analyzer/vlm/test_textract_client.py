from unittest.mock import MagicMock, patch

import pytest

from src.infrastructure.analyzer.vlm.textract_client import TextractClient


@patch("src.infrastructure.analyzer.vlm.textract_client.os.getenv")
@patch("src.infrastructure.analyzer.vlm.textract_client.boto3.client")
def test_initialize_textract_client(mock_boto_client, mock_getenv):
    """
    Test that environment variables are passed to boto3.client when initializing TextractClient.
    """
    fake_client = MagicMock()
    mock_boto_client.return_value = fake_client

    # Simulate environment variables
    def getenv_side_effect(key, default=None):
        env = {
            "AWS_ACCESS_KEY_ID": "fake-access-key",
            "AWS_SECRET_ACCESS_KEY": "fake-secret-key",
            "AWS_SESSION_TOKEN": "fake-session-token",
            "AWS_REGION": "us-west-2",
        }
        return env.get(key, default)

    mock_getenv.side_effect = getenv_side_effect

    client = TextractClient()

    mock_boto_client.assert_called_once_with(
        "textract",
        aws_access_key_id="fake-access-key",
        aws_secret_access_key="fake-secret-key",
        aws_session_token="fake-session-token",
        region_name="us-west-2",
    )

    assert client.client == fake_client
    assert client.model is None


@patch("src.infrastructure.analyzer.vlm.textract_client.boto3.client")
def test_get_client_returns_boto3_client(mock_boto_client):
    """
    Test that get_client returns the boto3 textract client.
    """
    fake_client = MagicMock()
    mock_boto_client.return_value = fake_client

    client = TextractClient()
    assert client.get_client() == fake_client


@patch("src.infrastructure.analyzer.vlm.textract_client.boto3.client")
def test_get_model_returns_none_by_default(mock_boto_client):
    """
    Test that get_model returns None by default.
    """
    mock_boto_client.return_value = MagicMock()
    client = TextractClient()
    assert client.get_model() is None
