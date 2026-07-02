from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    service_name: str = "xmip-backend"
    version: str = "0.1.0"
    environment: Literal["local", "dev", "staging", "prod", "test"] = "local"
    database_url: str = "sqlite+aiosqlite:///./xmip.db"
    auto_create_tables: bool = True
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])
    log_level: str = "INFO"
    auth_enabled: bool = False
    api_key: str | None = None
    api_key_header_name: str = "X-API-Key"


@lru_cache
def get_settings() -> Settings:
    return Settings()
