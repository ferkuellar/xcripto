import json
import os
from functools import lru_cache
from typing import Literal

from pydantic import AliasChoices, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Tests set XMIP_DISABLE_DOTENV=1 so local dotenv files do not leak into the suite.
# In normal local/dev runs, `.env.local` overrides `.env` so production placeholders
# in `.env` do not block startup.
_ENV_FILE = None if os.environ.get("XMIP_DISABLE_DOTENV") == "1" else (".env", ".env.local")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    app_name: str = "XMIP Backend"
    app_version: str = "0.1.0"
    service_name: str = "xmip-backend"
    version: str = "0.1.0"
    environment: Literal[
        "development", "local", "dev", "staging", "production", "prod", "test"
    ] = Field(
        default="development",
        validation_alias=AliasChoices("ENVIRONMENT", "APP_ENV"),
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
    public_site_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("APP_DOMAIN", "PUBLIC_SITE_URL"),
    )
    telegram_bot_token: str | None = Field(
        default=None,
        validation_alias=AliasChoices("TELEGRAM_BOT_TOKEN", "TELEGRAM_TOKEN"),
    )
    telegram_channel_id: str | None = Field(
        default=None,
        validation_alias=AliasChoices("TELEGRAM_CHANNEL_ID", "TELEGRAM_CHAT_ID"),
    )
    x_api_key: str | None = Field(default=None, validation_alias=AliasChoices("X_API_KEY"))
    x_api_secret: str | None = Field(
        default=None,
        validation_alias=AliasChoices("X_API_SECRET"),
    )
    x_access_token: str | None = Field(
        default=None,
        validation_alias=AliasChoices("X_ACCESS_TOKEN"),
    )
    x_access_token_secret: str | None = Field(
        default=None,
        validation_alias=AliasChoices("X_ACCESS_TOKEN_SECRET"),
    )
    binance_square_openapi_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("BINANCE_SQUARE_OPENAPI_KEY"),
    )
    request_logging_enabled: bool = True
    request_body_logging_enabled: bool = False
    response_body_logging_enabled: bool = False
    request_timeout_seconds: int = Field(
        default=30,
        validation_alias=AliasChoices("REQUEST_TIMEOUT_SECONDS", "REQUEST_TIMEOUT"),
    )
    operational_audit_enabled: bool = True
    db_healthcheck_enabled: bool = True

    # --- Real connectors (P9). Disabled by default; kill switches. ---
    connectors_enabled: bool = False
    rss_connector_enabled: bool = False
    rss_connector_max_items: int = 20
    rss_connector_timeout_seconds: int = 10
    rss_connector_user_agent: str = "XMIP-StagingBot/0.1"
    rss_connector_allowed_domains: str = ""  # CSV; empty = reject everything
    connector_run_mode: str = "manual"
    connector_audit_enabled: bool = True
    connector_require_source_reference: bool = True
    connector_auto_promote: bool = False  # MUST stay false in P9

    @property
    def is_production(self) -> bool:
        return self.environment in {"production", "prod"}

    @property
    def is_deployed_environment(self) -> bool:
        return self.environment in {"staging", "production", "prod"}

    @property
    def rss_allowed_domains(self) -> list[str]:
        return [
            d.lower().removeprefix("www.")
            for d in _split_csv(self.rss_connector_allowed_domains)
        ]

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
        if self.connector_auto_promote:
            raise ValueError("CONNECTOR_AUTO_PROMOTE must remain false in P9")
        errors = self.critical_configuration_errors()
        if errors:
            raise ValueError("; ".join(errors))
        return self

    def critical_configuration_errors(self) -> list[str]:
        errors: list[str] = []
        if self.is_deployed_environment:
            if self.debug:
                errors.append("DEBUG must be false in deployed environments")
            if self.auto_create_tables:
                errors.append("AUTO_CREATE_TABLES must be false in deployed environments")
            if not self.auth_enabled:
                errors.append("AUTH_ENABLED must be true in deployed environments")
            if not self.api_key:
                errors.append("API_KEY is required in deployed environments")
            elif self.api_key in {"dev-secret", "changeme", "change-me", "secret"}:
                errors.append("API_KEY must not use a development placeholder")
            if "*" in self.cors_origins:
                errors.append("CORS wildcard is not allowed in deployed environments")
            if self.database_url.startswith("sqlite"):
                errors.append("DATABASE_URL must use PostgreSQL in deployed environments")
        return errors


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
