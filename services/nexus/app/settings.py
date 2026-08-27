from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "OpenFDE Nexus"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://openfde:openfde@localhost:5432/openfde"
    nexus_api_key: SecretStr = Field(min_length=12)


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
