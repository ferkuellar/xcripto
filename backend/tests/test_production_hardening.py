import logging
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.core.config import Settings, get_settings
from app.core.logging import JsonFormatter, sanitize_headers
from app.db import health as db_health
from app.main import db_health as main_db_health
from app.main import settings as app_settings


async def test_live_returns_alive_without_database_dependency(client, monkeypatch):
    async def fail_if_called() -> None:
        raise AssertionError("live endpoint must not check the database")

    monkeypatch.setattr(main_db_health, "check_database_health", fail_if_called)

    response = await client.get("/live")

    assert response.status_code == 200
    assert response.json() == {
        "status": "alive",
        "service": "xmip-backend",
        "version": "0.1.0",
    }


async def test_ready_returns_ready_when_database_ok(client):
    response = await client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"
    assert response.json()["checks"]["configuration"] == "ok"
    assert response.json()["checks"]["database"] == "ok"


async def test_ready_returns_503_when_database_fails(client, monkeypatch):
    async def fail_database_check() -> None:
        raise RuntimeError("database unavailable")

    monkeypatch.setattr(main_db_health, "check_database_health", fail_database_check)

    response = await client.get("/ready")

    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"
    assert response.json()["checks"]["database"] == "failed"


async def test_ready_skips_database_when_disabled(client, monkeypatch):
    monkeypatch.setattr(app_settings, "db_healthcheck_enabled", False)

    response = await client.get("/ready")

    assert response.status_code == 200
    assert response.json()["checks"]["database"] == "skipped"


async def test_ready_returns_503_when_configuration_is_invalid(client, monkeypatch):
    monkeypatch.setattr(app_settings, "environment", "staging")
    monkeypatch.setattr(app_settings, "auth_enabled", False)

    response = await client.get("/ready")

    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"
    assert response.json()["checks"]["configuration"] == "failed"
    assert "AUTH_ENABLED must be true" in " ".join(
        response.json()["checks"]["configuration_errors"]
    )


async def test_health_still_returns_ok(client):
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


async def test_validation_errors_include_correlation_id(client):
    response = await client.post(
        "/api/v1/news/intake",
        json={},
        headers={"X-Correlation-ID": "phase14-validation"},
    )

    assert response.status_code == 422
    assert response.json()["correlation_id"] == "phase14-validation"


async def test_cors_allows_localhost_development_origin(client):
    response = await client.options(
        "/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_cors_wildcard_blocked_in_production_when_auth_enabled():
    with pytest.raises(ValidationError):
        Settings(
            environment="production",
            auth_enabled=True,
            cors_allowed_origins="*",
            database_url="postgresql+asyncpg://xmip:xmip@db:5432/xmip",
            public_web_base_url="https://xcripto.com",
            cors_allow_credentials=True,
            session_cookie_secure=True,
        )


def test_cors_wildcard_allowed_in_development():
    settings = Settings(
        environment="development",
        auth_enabled=False,
        cors_allowed_origins="*",
    )

    assert settings.cors_origins == ["*"]


def test_cors_wildcard_blocked_in_staging_even_without_auth():
    with pytest.raises(ValidationError):
        Settings(
            environment="staging",
            auth_enabled=False,
            cors_allowed_origins="*",
            database_url="postgresql+asyncpg://xmip:xmip@db:5432/xmip",
            public_web_base_url="https://xcripto.com",
            cors_allow_credentials=True,
            session_cookie_secure=True,
        )


def test_cors_json_list_backwards_compatible():
    settings = Settings(cors_allowed_origins='["http://localhost:5173"]')

    assert settings.cors_origins == ["http://localhost:5173"]


def test_cors_methods_and_headers_parse_from_csv():
    settings = Settings(
        cors_allowed_methods="GET,POST",
        cors_allowed_headers="Content-Type,X-Correlation-ID",
    )

    assert settings.cors_methods == ["GET", "POST"]
    assert settings.cors_headers == ["Content-Type", "X-Correlation-ID"]


def test_settings_defaults_are_development_safe():
    settings = Settings()

    assert settings.debug is False
    assert settings.auto_create_tables is False
    assert settings.request_body_logging_enabled is False
    assert settings.response_body_logging_enabled is False


def test_app_env_alias_is_supported_for_deployed_environment():
    settings = Settings(
        APP_ENV="staging",
        auth_enabled=True,
        api_key="staging-secret",
        database_url="postgresql+asyncpg://xmip:xmip@db:5432/xmip",
        cors_allowed_origins="https://admin-staging.example.com",
        public_web_base_url="https://xcripto-staging.example.com",
        cors_allow_credentials=True,
        session_cookie_secure=True,
    )

    assert settings.environment == "staging"


def test_deployed_environment_requires_cookie_security_and_postgres():
    with pytest.raises(ValidationError) as exc:
        Settings(
            environment="production",
            public_web_base_url="https://xcripto.com",
            cors_allowed_origins="https://xcripto.com,https://admin.xcripto.com",
            cors_allow_credentials=False,
            session_cookie_secure=False,
        )

    message = str(exc.value)
    assert "AUTH_ENABLED must be true" in message
    assert "CORS_ALLOW_CREDENTIALS must be true" in message
    assert "SESSION_COOKIE_SECURE must be true" in message
    assert "DATABASE_URL must use PostgreSQL" in message


def test_deployed_environment_rejects_debug_mode():
    with pytest.raises(ValidationError):
        Settings(
            environment="staging",
            debug=True,
            auth_enabled=True,
            cors_allow_credentials=True,
            session_cookie_secure=True,
            database_url="postgresql+asyncpg://xmip:xmip@db:5432/xmip",
            cors_allowed_origins="https://admin-staging.example.com",
            public_web_base_url="https://xcripto-staging.example.com",
        )


def test_deployed_environment_requires_public_web_base_url():
    with pytest.raises(ValidationError, match="PUBLIC_WEB_BASE_URL is required"):
        Settings(
            environment="production",
            auth_enabled=True,
            database_url="postgresql+asyncpg://xmip:xmip@db:5432/xmip",
            cors_allowed_origins="https://xcripto.com,https://admin.xcripto.com",
            cors_allow_credentials=True,
            session_cookie_secure=True,
        )


def test_deployed_environment_rejects_localhost_public_web_base_url():
    with pytest.raises(ValidationError, match="PUBLIC_WEB_BASE_URL must not use localhost"):
        Settings(
            environment="production",
            auth_enabled=True,
            database_url="postgresql+asyncpg://xmip:xmip@db:5432/xmip",
            cors_allowed_origins="https://xcripto.com,https://admin.xcripto.com",
            cors_allow_credentials=True,
            session_cookie_secure=True,
            public_web_base_url="http://localhost:3000",
        )


def test_request_timeout_setting_accepts_legacy_alias():
    settings = Settings(REQUEST_TIMEOUT=45)

    assert settings.request_timeout_seconds == 45


def test_default_cors_origins_include_local_development_frontends():
    settings = Settings()

    assert "http://localhost:3000" in settings.cors_origins
    assert "http://localhost:5173" in settings.cors_origins


def test_request_logging_settings_default_to_safe_body_logging_disabled():
    settings = Settings()

    assert settings.request_logging_enabled is True
    assert settings.request_body_logging_enabled is False
    assert settings.response_body_logging_enabled is False


async def test_request_logging_does_not_break_requests(client, caplog):
    caplog.set_level(logging.INFO, logger="xmip.request")

    response = await client.get("/api/v1/news")

    assert response.status_code == 200
    assert any(
        getattr(record, "request_path", None) == "/api/v1/news"
        for record in caplog.records
    )


async def test_request_logging_does_not_include_api_key_value(client, caplog):
    caplog.set_level(logging.INFO, logger="xmip.request")

    response = await client.get(
        "/api/v1/news",
        headers={"X-API-Key": "phase14-secret-value"},
    )

    assert response.status_code == 200
    assert "phase14-secret-value" not in caplog.text


async def test_request_logging_skips_health_noise(client, caplog):
    caplog.set_level(logging.INFO, logger="xmip.request")

    response = await client.get("/health")

    assert response.status_code == 200
    assert not any(
        getattr(record, "request_path", None) == "/health" for record in caplog.records
    )


def test_sanitize_headers_redacts_sensitive_headers():
    sanitized = sanitize_headers(
        {
            "X-API-Key": "secret",
            "Authorization": "Bearer secret",
            "Content-Type": "application/json",
        }
    )

    assert sanitized["X-API-Key"] == "[REDACTED]"
    assert sanitized["Authorization"] == "[REDACTED]"
    assert sanitized["Content-Type"] == "application/json"


def test_json_formatter_includes_structured_fields():
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="xmip.request",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="request completed",
        args=(),
        exc_info=None,
    )
    record.correlation_id = "cid-1"
    record.request_method = "GET"
    record.request_path = "/api/v1/news"
    record.status_code = 200
    record.duration_ms = 1.5

    formatted = formatter.format(record)

    assert '"correlation_id": "cid-1"' in formatted
    assert '"request_path": "/api/v1/news"' in formatted


async def test_database_health_executes_select_one():
    result = await db_health.check_database_health()

    assert result is None


def test_get_settings_uses_production_safe_defaults():
    settings = get_settings()

    assert settings.debug is False
    assert settings.auto_create_tables is False


def test_smoke_test_script_exists():
    assert Path("scripts/smoke_test.py").is_file()


def test_deployment_checklist_exists():
    assert Path("docs/DEPLOYMENT_CHECKLIST.md").is_file()


def test_operational_runbook_exists():
    assert Path("docs/OPERATIONAL_RUNBOOK.md").is_file()


def test_dockerfile_contains_uvicorn_app_command_and_healthcheck():
    content = Path("Dockerfile").read_text(encoding="utf-8")

    assert "app.main:app" in content
    assert "HEALTHCHECK" in content
    assert "alembic.ini" in content


def test_docker_compose_defines_api_and_postgres_services():
    content = Path("docker-compose.yml").read_text(encoding="utf-8")

    assert "api:" in content
    assert "postgres:" in content
    assert "alembic upgrade head" in content


def test_env_example_documents_hardening_settings():
    content = Path(".env.example").read_text(encoding="utf-8")

    assert "CORS_ALLOWED_ORIGINS" in content
    assert "REQUEST_LOGGING_ENABLED" in content
    assert "DB_HEALTHCHECK_ENABLED" in content
