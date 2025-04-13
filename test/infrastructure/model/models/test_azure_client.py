import openai

from src.infrastructure.model.models.azure_client import AzureOpenAIClient


def test_azure_client(monkeypatch):
    # Dummy values for settings.
    dummy_api_key = "dummy_api_key"
    dummy_api_version = "dummy_api_version"
    dummy_endpoint = "dummy_endpoint"
    dummy_deployment = "dummy_deployment"

    # Create a dummy AzureOpenAI class to replace openai.AzureOpenAI.
    class DummyAzureOpenAI:
        def __init__(self, api_key, api_version, azure_endpoint):
            self.api_key = api_key
            self.api_version = api_version
            self.azure_endpoint = azure_endpoint

    # Monkeypatch openai.AzureOpenAI to our dummy implementation.
    monkeypatch.setattr(openai, "AzureOpenAI", DummyAzureOpenAI)

    # Monkeypatch the settings values.
    from src.application.api.config import settings

    monkeypatch.setattr(settings, "azure_openai_api_key", dummy_api_key)
    monkeypatch.setattr(settings, "azure_openai_api_version", dummy_api_version)
    monkeypatch.setattr(settings, "azure_openai_endpoint", dummy_endpoint)
    monkeypatch.setattr(settings, "azure_openai_deployment", dummy_deployment)

    # Instantiate the AzureOpenAIClient.
    client_instance = AzureOpenAIClient()

    # Verify that get_model returns the dummy deployment.
    assert client_instance.get_model() == dummy_deployment

    # Verify that the client attribute is an instance of DummyAzureOpenAI and has correct values.
    azure_client_obj = client_instance.get_client()
    assert isinstance(azure_client_obj, DummyAzureOpenAI)
    assert azure_client_obj.api_key == dummy_api_key
    assert azure_client_obj.api_version == dummy_api_version
    assert azure_client_obj.azure_endpoint == dummy_endpoint
