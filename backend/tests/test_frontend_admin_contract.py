from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from app.core.config import get_settings

BACKEND_ROOT = Path(__file__).resolve().parents[1]


def load_script_module(name: str, relative_path: str):
    path = BACKEND_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def enable_auth(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")


def test_frontend_admin_api_contract_exists():
    assert (BACKEND_ROOT / "docs" / "FRONTEND_ADMIN_API_CONTRACT.md").exists()


def test_frontend_admin_integration_guide_exists():
    assert (BACKEND_ROOT / "docs" / "FRONTEND_ADMIN_INTEGRATION_GUIDE.md").exists()


def test_api_error_contract_exists():
    assert (BACKEND_ROOT / "docs" / "API_ERROR_CONTRACT.md").exists()


def test_api_auth_rbac_contract_exists():
    assert (BACKEND_ROOT / "docs" / "API_AUTH_RBAC_CONTRACT.md").exists()


def test_export_openapi_script_exists():
    assert (BACKEND_ROOT / "scripts" / "export_openapi.py").exists()


def test_export_openapi_script_generates_json(tmp_path):
    module = load_script_module("export_openapi_script", "scripts/export_openapi.py")
    output = tmp_path / "openapi.json"

    generated = module.export_openapi(output)

    assert generated == output
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["info"]["title"] == "XMIP Backend"
    assert "/api/v1/admin/frontend/config" in payload["paths"]


def test_admin_contract_smoke_script_exists():
    assert (BACKEND_ROOT / "scripts" / "admin_contract_smoke.py").exists()


def test_admin_contract_smoke_defines_critical_admin_endpoints():
    module = load_script_module("admin_contract_smoke_script", "scripts/admin_contract_smoke.py")

    endpoints = set(module.ADMIN_CONTRACT_ENDPOINTS)

    assert "/api/v1/admin/dashboard/overview" in endpoints
    assert "/api/v1/admin/editorial/work-queue" in endpoints
    assert "/api/v1/admin/agent-runner/summary" in endpoints
    assert "/api/v1/admin/connectors/summary" in endpoints
    assert "/api/v1/admin/audit/summary" in endpoints


async def test_frontend_config_no_api_key_or_database_url(client):
    response = await client.get("/api/v1/admin/frontend/config")

    assert response.status_code == 200
    body = response.json()
    serialized = json.dumps(body).lower()
    assert "api_key" not in serialized
    assert "database_url" not in serialized
    assert "dev-secret" not in serialized
    assert "sqlite" not in serialized


async def test_frontend_config_returns_expected_features(client):
    response = await client.get("/api/v1/admin/frontend/config")

    assert response.status_code == 200
    body = response.json()
    assert body["app_name"] == "XMIP Backend"
    assert body["rbac_enabled"] is True
    assert body["features"]["admin_dashboard"] is True
    assert body["features"]["agent_runner"] is True
    assert body["features"]["connectors"] is True
    assert body["features"]["operational_audit"] is True
    assert body["features"]["readiness_scoring"] is True


async def test_frontend_config_respects_api_key_when_auth_enabled(client, monkeypatch):
    enable_auth(monkeypatch)

    response = await client.get(
        "/api/v1/admin/frontend/config",
        headers={"X-Actor-Role": "admin"},
    )

    assert response.status_code == 401


async def test_frontend_config_blocks_invalid_role_when_auth_enabled(client, monkeypatch):
    enable_auth(monkeypatch)

    response = await client.get(
        "/api/v1/admin/frontend/config",
        headers={"X-API-Key": "dev-secret", "X-Actor-Role": "external"},
    )

    assert response.status_code == 403


async def test_frontend_route_map_returns_groups(client):
    response = await client.get("/api/v1/admin/frontend/route-map")

    assert response.status_code == 200
    groups = {item["group"] for item in response.json()}
    assert {
        "health",
        "dashboard",
        "intake",
        "workflow",
        "tasks",
        "readiness",
        "agent_runner",
        "connectors",
        "audit",
        "ownership",
        "users",
    }.issubset(groups)


async def test_frontend_route_map_respects_api_key_when_auth_enabled(client, monkeypatch):
    enable_auth(monkeypatch)

    response = await client.get(
        "/api/v1/admin/frontend/route-map",
        headers={"X-Actor-Role": "admin"},
    )

    assert response.status_code == 401


async def test_frontend_route_map_does_not_expose_secrets(client):
    response = await client.get("/api/v1/admin/frontend/route-map")

    assert response.status_code == 200
    serialized = json.dumps(response.json()).lower()
    assert "api_key" not in serialized
    assert "database_url" not in serialized
    assert "secret" not in serialized


def test_readme_mentions_frontend_admin_integration():
    readme = (BACKEND_ROOT / "README.md").read_text(encoding="utf-8")

    assert "Frontend/Admin Integration" in readme
    assert "scripts/export_openapi.py" in readme
    assert "scripts/admin_contract_smoke.py" in readme
