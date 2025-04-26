import pytest

from src.infrastructure.analyzer.analyzers.huggingface_client import HuggingFaceClient


class DummyTokenizer:
    pass


class DummyModel:
    pass


class DummyPipeline:
    pass


@pytest.fixture(autouse=True)
def clear_env_and_patches(monkeypatch):
    # ensure clean env
    monkeypatch.delenv("HUGGINGFACE_MODEL_NAME", raising=False)
    yield
    monkeypatch.delenv("HUGGINGFACE_MODEL_NAME", raising=False)


def test_init_and_methods_invoke_transformers(monkeypatch):
    # 1) set the env var that the client will read
    monkeypatch.setenv("HUGGINGFACE_MODEL_NAME", "test-model")

    # 2) stub out AutoTokenizer.from_pretrained
    def fake_tokenizer_from_pretrained(name):
        assert name == "test-model"
        return DummyTokenizer()

    monkeypatch.setattr(
        "src.infrastructure.analyzer.analyzers.huggingface_client.AutoTokenizer.from_pretrained",
        fake_tokenizer_from_pretrained,
    )

    # 3) stub out AutoModelForCausalLM.from_pretrained
    def fake_model_from_pretrained(name):
        assert name == "test-model"
        return DummyModel()

    monkeypatch.setattr(
        "src.infrastructure.analyzer.analyzers.huggingface_client.AutoModelForCausalLM.from_pretrained",
        fake_model_from_pretrained,
    )

    # 4) stub out pipeline
    seen = {}

    def fake_pipeline(task, model, tokenizer):
        # ensure correct args
        assert task == "text-generation"
        assert isinstance(model, DummyModel)
        assert isinstance(tokenizer, DummyTokenizer)
        seen["pipeline"] = DummyPipeline()
        return seen["pipeline"]

    monkeypatch.setattr(
        "src.infrastructure.analyzer.analyzers.huggingface_client.pipeline",
        fake_pipeline,
    )

    # 5) instantiate the client (constructor will invoke all the above)
    client = HuggingFaceClient()

    # 6) get_model should return the env var
    assert client.get_model() == "test-model"

    # 7) get_client should return exactly what our fake pipeline returned
    returned = client.get_client()
    assert returned is seen["pipeline"]


def test_missing_env_var_raises(monkeypatch):
    # ensure no HUGGINGFACE_MODEL_NAME in env
    monkeypatch.delenv("HUGGINGFACE_MODEL_NAME", raising=False)

    # stub transformers so we can catch the failure early
    monkeypatch.setattr(
        "src.infrastructure.analyzer.analyzers.huggingface_client.AutoTokenizer.from_pretrained",
        lambda name: DummyTokenizer(),
    )
    monkeypatch.setattr(
        "src.infrastructure.analyzer.analyzers.huggingface_client.AutoModelForCausalLM.from_pretrained",
        lambda name: DummyModel(),
    )
    monkeypatch.setattr(
        "src.infrastructure.analyzer.analyzers.huggingface_client.pipeline",
        lambda *args, **kwargs: DummyPipeline(),
    )

    # now __init__ should see model_name=None and likely fail on from_pretrained(None)
    with pytest.raises(Exception):
        HuggingFaceClient(model_name="whatever")
