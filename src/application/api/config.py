from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Azure OpenAI config
    azure_openai_api_key: str
    azure_openai_api_version: str
    azure_openai_endpoint: str
    azure_openai_deployment: str

    # OpenAI config
    openai_api_key: str
    openai_model: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra fields not explicitly defined in Settings


settings = Settings()
