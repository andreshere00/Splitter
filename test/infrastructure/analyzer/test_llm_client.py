import pytest

from src.infrastructure.analyzer.vlm.llm_client import LLMClient


def test_llm_client_none():
    """Test that when method is 'none', no client is created."""
    llm = LLMClient("none")
    assert llm.get_client() is None
    assert llm.get_model() is None


def test_llm_client_openai(monkeypatch):
    """
    Test that when method is 'openai', LLMClient instantiates an OpenAIClient
    and returns the dummy client and model.
    """
    from src.infrastructure.analyzer.vlm.openai_client import OpenAIClient

    # Monkey-patch OpenAIClient's __init__ and its methods.
    monkeypatch.setattr(OpenAIClient, "__init__", lambda self: None)
    monkeypatch.setattr(OpenAIClient, "get_client", lambda self: "dummy_openai_client")
    monkeypatch.setattr(OpenAIClient, "get_model", lambda self: "dummy_openai_model")

    llm = LLMClient("openai")
    assert llm.get_client() == "dummy_openai_client"
    assert llm.get_model() == "dummy_openai_model"


def test_llm_client_azure(monkeypatch):
    """
    Test that when method is 'azure', LLMClient instantiates an AzureOpenAIClient
    and returns the dummy client and model.
    """
    from src.infrastructure.analyzer.vlm.azure_client import AzureOpenAIClient

    # Monkey-patch AzureOpenAIClient's __init__ and its methods.
    monkeypatch.setattr(AzureOpenAIClient, "__init__", lambda self: None)
    monkeypatch.setattr(
        AzureOpenAIClient, "get_client", lambda self: "dummy_azure_client"
    )
    monkeypatch.setattr(
        AzureOpenAIClient, "get_model", lambda self: "dummy_azure_model"
    )

    llm = LLMClient("azure")
    assert llm.get_client() == "dummy_azure_client"
    assert llm.get_model() == "dummy_azure_model"


def test_llm_client_invalid():
    """Test that an invalid method raises a ValueError."""
    with pytest.raises(ValueError):
        LLMClient("invalid")
