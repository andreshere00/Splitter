import openai

from src.infrastructure.analyzer.analyzers.openai_client import OpenAIClient


def test_openai_client(monkeypatch):
    # Dummy environment values.
    dummy_api_key = "dummy_api_key"
    dummy_model = "dummy_model"

    # Set environment variables using monkeypatch.
    monkeypatch.setenv("OPENAI_API_KEY", dummy_api_key)
    monkeypatch.setenv("OPENAI_MODEL", dummy_model)

    # Define a dummy OpenAI class that just stores the api_key.
    class DummyOpenAI:
        def __init__(self, api_key):
            self.api_key = api_key

    # Replace openai.OpenAI with DummyOpenAI.
    monkeypatch.setattr(openai, "OpenAI", DummyOpenAI)

    # Instantiate the OpenAIClient.
    client_instance = OpenAIClient()

    # Verify that get_model returns the dummy model.
    assert client_instance.get_model() == dummy_model

    # Verify that get_client returns an instance of DummyOpenAI with the dummy api_key.
    client_obj = client_instance.get_client()
    assert isinstance(client_obj, DummyOpenAI)
    assert client_obj.api_key == dummy_api_key
