from unittest.mock import MagicMock, patch

import pytest

from src.infrastructure.model.models.textract_client import TextractClient


@patch("src.infrastructure.model.models.textract_client.boto3.client")
def test_textract_client_initialization(mock_boto_client):
    """
    Test that TextractClient initializes a boto3 client and sets model to None.
    """
    fake_client = MagicMock()
    mock_boto_client.return_value = fake_client

    client = TextractClient()

    # Assert boto3.client was called correctly
    mock_boto_client.assert_called_once_with("textract")

    # Assert the internal client is set properly
    assert client.client == fake_client

    # Assert the model attribute is None
    assert client.model is None


@patch("src.infrastructure.model.models.textract_client.boto3.client")
def test_get_client_returns_boto3_client(mock_boto_client):
    """
    Test that get_client returns the boto3 textract client.
    """
    fake_client = MagicMock()
    mock_boto_client.return_value = fake_client

    client = TextractClient()
    assert client.get_client() == fake_client


@patch("src.infrastructure.model.models.textract_client.boto3.client")
def test_get_model_returns_none_by_default(mock_boto_client):
    """
    Test that get_model returns None by default.
    """
    mock_boto_client.return_value = MagicMock()
    client = TextractClient()
    assert client.get_model() is None
