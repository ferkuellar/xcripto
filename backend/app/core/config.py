import json
from functools import lru_cache
from typing import Literal

from pydantic import AliasChoices, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    app_name: str = "XMIP Backend"
    app_version: str = "0.1.0"
    service_name: str = "xmip-backend"
    version: str = "0.1.0"
    environment: Literal["development", "local", "dev", "staging", "production", "prod", "test"] = (
        "development"
    )
    debug: bool = False
    database_url: str = "sqlite+aiosqlite:///./xmip.db"
    auto_create_tables: bool = False
    cors_allowed_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        validation_alias=AliasChoices("CORS_ALLOWED_ORIGINS", "CORS_ORIGINS"),
    )
    cors_allow_credentials: bool = False
    cors_allowed_methods: str = "GET,POST,PATCH,PUT,DELETE,OPTIONS"
    cors_allowed_headers: str = (
        "Authorization,Content-Type,X-API-Key,X-Correlation-ID,"
        "X-Actor-Id,X-Actor-Role,X-Actor-Display"
    )
    log_level: str = "INFO"
    auth_enabled: bool = False
    api_key: str | None = None
    api_key_header_name: str = "X-API-Key"
    request_logging_enabled: bool = True
    request_body_logging_enabled: bool = False
    response_body_logging_enabled: bool = False
    operational_audit_enabled: bool = True
    db_healthcheck_enabled: bool = True

    @property
    def is_production(self) -> bool:
        return self.environment in {"production", "prod"}

    @property
    def cors_origins(self) -> list[str]:
        return _split_csv(self.cors_allowed_origins)

    @property
    def cors_methods(self) -> list[str]:
        return _split_csv(self.cors_allowed_methods)

    @property
    def cors_headers(self) -> list[str]:
        return _split_csv(self.cors_allowed_headers)

    @model_validator(mode="after")
    def validate_production_security(self) -> "Settings":
        if self.is_production and self.auth_enabled and "*" in self.cors_origins:
            raise ValueError(
                "CORS wildcard is not allowed in production when AUTH_ENABLED=true"
            )
        return self


def _split_csv(value: str | list[str]) -> list[str]:
    if isinstance(value, list):
        return [item.strip() for item in value if item and item.strip()]
    stripped = value.strip()
    if stripped.startswith("["):
        parsed = json.loads(stripped)
        if isinstance(parsed, list):
            return [str(item).strip() for item in parsed if str(item).strip()]
    return [item.strip() for item in value.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
