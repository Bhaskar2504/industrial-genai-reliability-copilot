from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_provider: str = "mock"
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.6-luna"
    app_env: str = "development"
    trace_to_stdout: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
