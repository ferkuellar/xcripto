from app.core.config import get_settings

CONNECTOR_PAYLOAD = {
    "connector_name": "Example RSS",
    "connector_type": "rss_feed",
    "connector_status": "dry_run_only",
    "provider": "example",
    "base_url": "https://example.com/feed.xml",
    "description": "Example RSS connector contract.",
    "capabilities": ["ingest_signals"],
    "configuration": {"feed_path": "/feed.xml"},
    "auth_type": "none",
    "enabled": False,
    "dry_run_only": True,
}


def enable_auth(monkeypatch) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")


def auth_headers(role: str = "admin") -> dict[str, str]:
    return {"X-API-Key": "dev-secret", "X-Actor-Role": role}


async def create_connector(client, **overrides) -> dict:
    response = await client.post("/api/v1/connectors", json={**CONNECTOR_PAYLOAD, **overrides})
    assert response.status_code == 201
    return response.json()


async def test_create_external_connector_valid(client):
    connector = await create_connector(client)

    assert connector["connector_name"] == "Example RSS"
    assert connector["connector_type"] == "rss_feed"
    assert connector["dry_run_only"] is True


async def test_block_invalid_connector_type(client):
    response = await client.post(
        "/api/v1/connectors",
        json={**CONNECTOR_PAYLOAD, "connector_type": "real_scraper"},
    )

    assert response.status_code == 422


async def test_block_invalid_connector_status(client):
    response = await client.post(
        "/api/v1/connectors",
        json={**CONNECTOR_PAYLOAD, "connector_status": "live"},
    )

    assert response.status_code == 422


async def test_block_invalid_auth_type(client):
    response = await client.post(
        "/api/v1/connectors",
        json={**CONNECTOR_PAYLOAD, "auth_type": "plain_secret"},
    )

    assert response.status_code == 422


async def test_block_invalid_capability(client):
    response = await client.post(
        "/api/v1/connectors",
        json={**CONNECTOR_PAYLOAD, "capabilities": ["scrape_everything"]},
    )

    assert response.status_code == 422


async def test_block_configuration_with_api_key(client):
    response = await client.post(
        "/api/v1/connectors",
        json={**CONNECTOR_PAYLOAD, "configuration": {"api_key": "secret-value"}},
    )

    assert response.status_code == 400
    assert "must not contain secrets" in str(response.json())


async def test_block_configuration_with_nested_token(client):
    response = await client.post(
        "/api/v1/connectors",
        json={**CONNECTOR_PAYLOAD, "configuration": {"headers": {"token": "secret"}}},
    )

    assert response.status_code == 400


async def test_allow_secret_ref(client):
    connector = await create_connector(
        client,
        auth_type="api_key_ref",
        secret_ref="vault://xmip/rss/example",
    )

    assert connector["secret_ref"] == "vault://xmip/rss/example"


async def test_list_connectors(client):
    await create_connector(client)

    response = await client.get("/api/v1/connectors")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_filter_connectors_by_type(client):
    await create_connector(client)
    await create_connector(
        client,
        connector_name="Example Market",
        connector_type="market_data",
        capabilities=["fetch_market_context"],
    )

    response = await client.get("/api/v1/connectors", params={"connector_type": "market_data"})

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["connector_type"] == "market_data"


async def test_filter_connectors_by_status(client):
    await create_connector(client)
    await create_connector(client, connector_status="draft", connector_name="Draft connector")

    response = await client.get(
        "/api/v1/connectors", params={"connector_status": "dry_run_only"}
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_filter_connectors_by_enabled(client):
    await create_connector(client)
    connector = await create_connector(client, connector_name="Enabled connector")
    await client.patch(f"/api/v1/connectors/{connector['id']}/enable")

    response = await client.get("/api/v1/connectors", params={"enabled": True})

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["enabled"] is True


async def test_get_connector_by_id(client):
    connector = await create_connector(client)

    response = await client.get(f"/api/v1/connectors/{connector['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == connector["id"]


async def test_update_connector(client):
    connector = await create_connector(client)

    response = await client.patch(
        f"/api/v1/connectors/{connector['id']}",
        json={
            "description": "Updated description",
            "capabilities": ["ingest_signals", "import_file"],
        },
    )

    assert response.status_code == 200
    assert response.json()["description"] == "Updated description"
    assert "import_file" in response.json()["capabilities"]


async def test_enable_connector(client):
    connector = await create_connector(client)

    response = await client.patch(f"/api/v1/connectors/{connector['id']}/enable")

    assert response.status_code == 200
    assert response.json()["enabled"] is True
    assert response.json()["connector_status"] == "dry_run_only"


async def test_disable_connector(client):
    connector = await create_connector(client)
    await client.patch(f"/api/v1/connectors/{connector['id']}/enable")

    response = await client.patch(f"/api/v1/connectors/{connector['id']}/disable")

    assert response.status_code == 200
    assert response.json()["enabled"] is False
    assert response.json()["connector_status"] == "disabled"


async def test_archive_connector(client):
    connector = await create_connector(client)

    response = await client.patch(f"/api/v1/connectors/{connector['id']}/archive")

    assert response.status_code == 200
    assert response.json()["connector_status"] == "archived"


async def test_correlation_id_persisted(client):
    response = await client.post(
        "/api/v1/connectors",
        json=CONNECTOR_PAYLOAD,
        headers={"X-Correlation-ID": "connector-correlation"},
    )

    assert response.status_code == 201
    assert response.json()["correlation_id"] == "connector-correlation"


async def test_validate_connector_valid_passes(client):
    connector = await create_connector(client)

    response = await client.post(f"/api/v1/connectors/{connector['id']}/validate")

    assert response.status_code == 200
    assert response.json()["passed"] is True


async def test_validate_connector_auth_ref_without_secret_ref_warns(client):
    connector = await create_connector(client, auth_type="api_key_ref")

    response = await client.post(f"/api/v1/connectors/{connector['id']}/validate")

    assert response.status_code == 200
    assert response.json()["passed"] is True
    assert response.json()["warnings"]


async def test_update_connector_blocks_insecure_configuration(client):
    connector = await create_connector(client)

    response = await client.patch(
        f"/api/v1/connectors/{connector['id']}",
        json={"configuration": {"password": "secret"}},
    )

    assert response.status_code == 400


async def test_dry_run_creates_connector_run(client):
    connector = await create_connector(client)

    response = await client.post(
        f"/api/v1/connectors/{connector['id']}/dry-run",
        json={"run_type": "dry_run"},
    )

    assert response.status_code == 200
    assert response.json()["run"]["connector_id"] == connector["id"]
    assert response.json()["run"]["run_status"] == "completed"


async def test_dry_run_does_not_create_intake_signal(client):
    connector = await create_connector(client)

    response = await client.post(f"/api/v1/connectors/{connector['id']}/dry-run", json={})
    signals = await client.get("/api/v1/intake/signals")

    assert response.status_code == 200
    assert signals.json() == []


async def test_dry_run_does_not_create_publication_record(client):
    connector = await create_connector(client, capabilities=["publish_content"])

    response = await client.post(f"/api/v1/connectors/{connector['id']}/dry-run", json={})
    publications = await client.get("/api/v1/publication-records")

    assert response.status_code == 200
    assert publications.json() == []


async def test_dry_run_updates_last_run_and_success(client):
    connector = await create_connector(client)

    response = await client.post(f"/api/v1/connectors/{connector['id']}/dry-run", json={})
    refreshed = await client.get(f"/api/v1/connectors/{connector['id']}")

    assert response.status_code == 200
    assert refreshed.json()["last_run_at"] is not None
    assert refreshed.json()["last_success_at"] is not None


async def test_dry_run_registers_operational_audit(client):
    connector = await create_connector(client)

    response = await client.post(f"/api/v1/connectors/{connector['id']}/dry-run", json={})
    audit = await client.get(
        "/api/v1/operational-audit/events",
        params={"action": "connector.dry_run"},
    )

    assert response.status_code == 200
    assert audit.status_code == 200
    assert audit.json()[0]["entity_id"] == connector["id"]


async def test_dry_run_blocks_archived_connector(client):
    connector = await create_connector(client)
    await client.patch(f"/api/v1/connectors/{connector['id']}/archive")

    response = await client.post(f"/api/v1/connectors/{connector['id']}/dry-run", json={})

    assert response.status_code == 409


async def test_list_connector_runs(client):
    connector = await create_connector(client)
    await client.post(f"/api/v1/connectors/{connector['id']}/dry-run", json={})

    response = await client.get(f"/api/v1/connectors/{connector['id']}/runs")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_connector_run_by_id(client):
    connector = await create_connector(client)
    dry_run = await client.post(f"/api/v1/connectors/{connector['id']}/dry-run", json={})
    run_id = dry_run.json()["run"]["id"]

    response = await client.get(f"/api/v1/connectors/runs/{run_id}")

    assert response.status_code == 200
    assert response.json()["id"] == run_id


async def test_filter_connector_runs_by_status(client):
    connector = await create_connector(client)
    await client.post(f"/api/v1/connectors/{connector['id']}/dry-run", json={})

    response = await client.get(
        f"/api/v1/connectors/{connector['id']}/runs",
        params={"run_status": "completed"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_admin_can_create_connector_when_auth_enabled(client, monkeypatch):
    enable_auth(monkeypatch)

    response = await client.post(
        "/api/v1/connectors",
        json=CONNECTOR_PAYLOAD,
        headers=auth_headers("admin"),
    )

    assert response.status_code == 201


async def test_viewer_cannot_create_connector_when_auth_enabled(client, monkeypatch):
    enable_auth(monkeypatch)

    response = await client.post(
        "/api/v1/connectors",
        json=CONNECTOR_PAYLOAD,
        headers=auth_headers("viewer"),
    )

    assert response.status_code == 403


async def test_agent_operator_can_dry_run_when_auth_enabled(client, monkeypatch):
    connector = await create_connector(client)
    enable_auth(monkeypatch)

    response = await client.post(
        f"/api/v1/connectors/{connector['id']}/dry-run",
        json={},
        headers=auth_headers("agent_operator"),
    )

    assert response.status_code == 200


async def test_viewer_cannot_dry_run_when_auth_enabled(client, monkeypatch):
    connector = await create_connector(client)
    enable_auth(monkeypatch)

    response = await client.post(
        f"/api/v1/connectors/{connector['id']}/dry-run",
        json={},
        headers=auth_headers("viewer"),
    )

    assert response.status_code == 403


async def test_auth_enabled_requires_api_key_for_connectors(client, monkeypatch):
    enable_auth(monkeypatch)

    response = await client.get("/api/v1/connectors")

    assert response.status_code == 401


async def test_auth_disabled_keeps_connectors_compatible(client):
    response = await client.get("/api/v1/connectors")

    assert response.status_code == 200


async def test_admin_connectors_summary_counts_connectors(client):
    await create_connector(client)

    response = await client.get("/api/v1/admin/connectors/summary")

    assert response.status_code == 200
    assert response.json()["total_connectors"] == 1


async def test_admin_connectors_summary_groups_by_type(client):
    await create_connector(client)

    response = await client.get("/api/v1/admin/connectors/summary")

    assert response.status_code == 200
    assert response.json()["connectors_by_type"]["rss_feed"] == 1


async def test_admin_connectors_summary_groups_by_status(client):
    await create_connector(client)

    response = await client.get("/api/v1/admin/connectors/summary")

    assert response.status_code == 200
    assert response.json()["connectors_by_status"]["dry_run_only"] == 1


async def test_admin_connectors_summary_includes_recent_runs(client):
    connector = await create_connector(client)
    await client.post(f"/api/v1/connectors/{connector['id']}/dry-run", json={})

    response = await client.get("/api/v1/admin/connectors/summary")

    assert response.status_code == 200
    assert len(response.json()["recent_connector_runs"]) == 1


async def test_external_connector_migration_exists():
    from pathlib import Path

    migration = Path("alembic/versions/20260702_0011_add_external_connector_interfaces.py")

    assert migration.exists()
