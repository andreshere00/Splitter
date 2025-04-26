import pytest

import src.infrastructure.analyzer.analyze_manager as mgr_mod
from src.infrastructure.analyzer.analyze_manager import AnalyzeManager


# Dummy client classes to stand in for real LLM clients
class DummyOpenAI:
    pass


class DummyAzure:
    pass


class DummyHF:
    pass


def make_config(default, override=None):
    """
    Return a minimal config-dict for AnalyzeManager.
    """
    cfg = {"analyzer": {"default": default}}
    if override is not None:
        cfg["analyzer"]["override"] = override
    return cfg


@pytest.mark.parametrize(
    "ext, default, override, creators, exp_name, exp_cls",
    [
        # 1) no override, default "none"  → skip analysis
        (".txt", "none", None, {}, "none", None),
        # 2) override for png → azure-openai
        (
            "png",
            "none",
            {"png": "azure-openai"},
            {"azure-openai": DummyAzure},
            "azure-openai",
            DummyAzure,
        ),
        # 3) uppercase / no-dot ext, default openai
        ("PDF", "openai", None, {"openai": DummyOpenAI}, "openai", DummyOpenAI),
        # 4) override for hf, default none
        (
            ".md",
            "none",
            {"md": "huggingface"},
            {"huggingface": DummyHF},
            "huggingface",
            DummyHF,
        ),
    ],
)
def test_get_analyzer_returns_expected_client_and_name(
    monkeypatch, ext, default, override, creators, exp_name, exp_cls
):
    # 1) Monkeypatch load_config to return our fake config
    fake_cfg = make_config(default, override)
    monkeypatch.setattr(mgr_mod, "load_config", lambda path: fake_cfg)

    # 2) Monkeypatch the _CREATORS mapping on the class
    monkeypatch.setattr(AnalyzeManager, "_CREATORS", creators, raising=True)

    # 3) Instantiate manager (config_path is irrelevant here)
    am = AnalyzeManager(config_path="dummy-path.yaml")

    # 4) Call get_analyzer
    if exp_cls is None:
        client, name = am.get_analyzer(ext)
        assert client is None
        assert name == exp_name
    else:
        client, name = am.get_analyzer(ext)
        assert isinstance(
            client, exp_cls
        ), f"Expected client of type {exp_cls.__name__}, got {type(client)}"
        assert name == exp_name


def test_unknown_analyzer_name_raises(monkeypatch):
    # default is a non-"none" name that isn't in _CREATORS
    fake_cfg = make_config("nonexistent", None)
    monkeypatch.setattr(mgr_mod, "load_config", lambda path: fake_cfg)
    # ensure no mapping for "nonexistent"
    monkeypatch.setattr(AnalyzeManager, "_CREATORS", {}, raising=True)

    am = AnalyzeManager(config_path="dummy")
    with pytest.raises(ValueError) as exc:
        am.get_analyzer(".anything")
    assert "No analyzer registered for 'nonexistent'" in str(exc.value)
