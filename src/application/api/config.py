from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Azure OpenAI
    azure_openai_api_key: str
    azure_openai_api_version: str
    azure_openai_endpoint: str
    azure_openai_deployment: str

    # OpenAI
    openai_api_key: str
    openai_model: str

    model_config = dict(extra="ignore")


settings = Settings()
