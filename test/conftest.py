import os

_DUMMY_ENV = {
    "AZURE_OPENAI_API_KEY": "dummy",
    "AZURE_OPENAI_API_VERSION": "2024-04-15",
    "AZURE_OPENAI_ENDPOINT": "https://example.com",
    "AZURE_OPENAI_DEPLOYMENT": "dummy-deployment",
    "OPENAI_API_KEY": "dummy",
    "OPENAI_MODEL": "dummy-model",
}


def pytest_sessionstart(session):
    """Populate required env-vars before any project code is imported."""
    for k, v in _DUMMY_ENV.items():
        os.environ.setdefault(k, v)
