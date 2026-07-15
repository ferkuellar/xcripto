from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.core.config import Settings
from app.services.public_news_service import normalize_public_base_url, public_news_url


def test_normalize_public_base_url_preserves_localhost_for_local_runtime():
    assert normalize_public_base_url("http://localhost:3000/", "http://127.0.0.1:8000") == (
        "http://localhost:3000"
    )


def test_normalize_public_base_url_defaults_to_https_for_domain_names():
    assert normalize_public_base_url("xcripto.com/", "http://127.0.0.1:8000") == (
        "https://xcripto.com"
    )


def test_public_news_url_trims_slashes_and_preserves_slug():
    assert public_news_url("https://xcripto.com/", "bitcoin-etf-sees-record-inflows") == (
        "https://xcripto.com/news/bitcoin-etf-sees-record-inflows"
    )


def test_settings_accepts_public_web_base_url_field():
    settings = Settings(public_web_base_url="https://xcripto.com")

    assert settings.public_web_base_url == "https://xcripto.com"


def test_deployed_environment_rejects_localhost_public_base_url():
    with pytest.raises(ValidationError, match="PUBLIC_WEB_BASE_URL must not use localhost"):
        Settings(
            environment="production",
            auth_enabled=True,
            api_key="prod-secret",
            database_url="postgresql+asyncpg://xmip:xmip@db:5432/xmip",
            cors_allowed_origins="https://xcripto.com,https://admin.xcripto.com",
            public_web_base_url="http://localhost:3000",
        )
