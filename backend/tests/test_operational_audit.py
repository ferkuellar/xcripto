import pytest

from app.core.config import get_settings

NEWS_PAYLOAD = {
    "title": "Operational audit news",
    "summary": "Audit log coverage signal.",
    "category": "markets",
    "priority": "P1",
    "source_url": "https://example.com/operational-audit",
    "source_name": "Example Wire",
}


def enable_auth(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")


def auth_headers(role: str = "admin", actor_id: str = "actor-1") -> dict[str, str]:
    return {"X-API-Key": "dev-secret", "X-Actor-Role": role, "X-Actor-Id": actor_id}


def manual_event_payload(**overrides) -> dict:
    payload = {
        "event_type": "system_event",
        "action": "system.manual_note",
        "permission": "operational_audit.create",
        "actor_id": "operator-1",
        "actor_role": "admin",
        "actor_source": "header",
        "entity_type": "System",
        "entity_id": "manual-1",
        "outcome": "succeeded",
        "decision": "created",
        "metadata": {"note": "manual audit event"},
    }
    payload.update(overrides)
    return payload


async def create_manual_event(client, **overrides) -> dict:
    response = await client.post(
        "/api/v1/operational-audit/events",
        json=manual_event_payload(**overrides),
    )
    assert response.status_code == 201
    return response.json()


async def create_news(client, **overrides) -> dict:
    response = await client.post("/api/v1/news/intake", json={**NEWS_PAYLOAD, **overrides})
    assert response.status_code == 201
    return response.json()


async def create_signal(client) -> dict:
    response = await client.post(
        "/api/v1/intake/signals",
        json={
            "signal_type": "manual",
            "source_name": "Example Wire",
            "source_url": "https://example.com/audit-signal",
            "raw_title": "Operational audit signal",
            "raw_summary": "Signal summary",
            "topic": "markets",
        },
    )
    assert response.status_code == 201
    return response.json()


async def create_agent_output(client, news_id: str | None = None) -> dict:
    payload = {
        "agent_name": "RiskAgent",
        "output_type": "risk_review",
        "summary": "Risk output",
        "payload": {"risk_level": "medium"},
        "entity_type": "news_item",
        "entity_id": news_id or "manual-news",
    }
    if news_id:
        payload["news_item_id"] = news_id
    response = await client.post("/api/v1/agent-outputs", json=payload)
    assert response.status_code == 201
    return response.json()


async def create_memory_item(client, news_id: str) -> dict:
    response = await client.post(
        "/api/v1/memory-items",
        json={
            "memory_type": "editorial_memory",
            "memory_status": "proposed",
            "title": "Audit memory",
            "memory_statement": "Keep audit traces for critical actions.",
            "source_or_origin": "operator note",
            "news_item_id": news_id,
            "confidence_level": "MC3",
            "persistence_level": "M2",
            "scope": "project_wide",
            "expiration_recommendation": "review_quarterly",
        },
    )
    assert response.status_code == 201
    return response.json()


async def create_user(client, **overrides) -> dict:
    payload = {
        "email": "audit-user@example.com",
        "display_name": "Audit User",
        "handle": "audit_user",
        "role": "editor",
        "status": "active",
        **overrides,
    }
    response = await client.post("/api/v1/users", json=payload)
    assert response.status_code == 201
    return response.json()


async def create_ownership(client, user_id: str, **overrides) -> dict:
    payload = {
        "user_id": user_id,
        "entity_type": "NewsItem",
        "entity_id": "news-1",
        "ownership_type": "owner",
        "assigned_by": "operator",
        **overrides,
    }
    response = await client.post("/api/v1/ownership/assign", json=payload)
    assert response.status_code == 201
    return response.json()


async def create_publishable_chain(client) -> tuple[dict, dict, dict]:
    news = await create_news(client)
    piece = (
        await client.post(
            "/api/v1/content-pieces",
            json={
                "news_item_id": news["id"],
                "content_type": "news_article",
                "title": "Audit publication",
                "summary": "Summary",
                "body": "Body",
                "status": "approved",
                "category": "markets",
                "priority": "P1",
                "verification_status": "verified",
                "risk_level": "medium",
                "source_refs": ["https://example.com/operational-audit"],
            },
        )
    )
    assert piece.status_code == 201
    plan = (
        await client.post(
            "/api/v1/distribution-plans",
            json={
                "content_piece_id": piece.json()["id"],
                "news_item_id": news["id"],
                "primary_channel": "Blog / Web",
                "secondary_channels": [],
                "distribution_type": "primary_publication",
                "status": "scheduled",
                "dependencies": [],
                "metric_plan": {"primary_metric": "views"},
                "risk_level": "medium",
                "publication_readiness": "ready",
            },
        )
    )
    assert plan.status_code == 201
    return news, piece.json(), plan.json()


async def create_workflow_task(client) -> dict:
    news = await create_news(client)
    workflow = await client.post(
        f"/api/v1/workflows/news/{news['id']}/start",
        json={"workflow_type": "editorial_pipeline"},
    )
    assert workflow.status_code == 201
    response = await client.post(
        "/api/v1/workflow-tasks",
        json={
            "workflow_run_id": workflow.json()["id"],
            "news_item_id": news["id"],
            "task_type": "source_validation",
            "task_status": "queued",
            "priority": "P3",
            "assigned_agent": "SourceValidatorAgent",
            "title": "Validate source",
            "description": "Validate the initial source signal.",
            "input_payload": {"source": "wire"},
        },
    )
    assert response.status_code == 201
    return response.json()


async def latest_event(client, action: str) -> dict:
    response = await client.get("/api/v1/operational-audit/events", params={"action": action})
    assert response.status_code == 200
    assert response.json()
    return response.json()[0]


async def test_create_operational_audit_log_manual_valid(client):
    event = await create_manual_event(client)

    assert event["event_type"] == "system_event"
    assert event["metadata"]["note"] == "manual audit event"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("event_type", "bad_event"),
        ("outcome", "maybe"),
        ("decision", "maybe"),
    ],
)
async def test_block_invalid_operational_audit_catalog_values(client, field, value):
    response = await client.post(
        "/api/v1/operational-audit/events",
        json=manual_event_payload(**{field: value}),
    )

    assert response.status_code == 422


async def test_list_and_filter_operational_audit_events(client):
    event = await create_manual_event(
        client,
        event_type="publication_event",
        actor_role="publisher",
        entity_type="PublicationRecord",
        entity_id="pub-1",
        correlation_id="corr-audit-filter",
    )

    filters = {
        "event_type": "publication_event",
        "actor_role": "publisher",
        "entity_type": "PublicationRecord",
        "entity_id": "pub-1",
        "correlation_id": "corr-audit-filter",
    }
    response = await client.get("/api/v1/operational-audit/events", params=filters)

    assert response.status_code == 200
    assert response.json()[0]["id"] == event["id"]


@pytest.mark.parametrize(
    ("filter_name", "filter_value"),
    [
        ("action", "publication.manual"),
        ("permission", "publication.create"),
        ("news_item_id", "news-filter-1"),
        ("workflow_run_id", "workflow-filter-1"),
        ("workflow_task_id", "task-filter-1"),
        ("agent_output_id", "output-filter-1"),
        ("outcome", "succeeded"),
        ("decision", "created"),
    ],
)
async def test_operational_audit_list_filters_for_critical_dimensions(
    client,
    filter_name,
    filter_value,
):
    event = await create_manual_event(
        client,
        event_type="publication_event",
        action="publication.manual",
        permission="publication.create",
        news_item_id="news-filter-1",
        workflow_run_id="workflow-filter-1",
        workflow_task_id="task-filter-1",
        agent_output_id="output-filter-1",
        outcome="succeeded",
        decision="created",
    )

    response = await client.get(
        "/api/v1/operational-audit/events",
        params={filter_name: filter_value},
    )

    assert response.status_code == 200
    assert response.json()[0]["id"] == event["id"]


async def test_get_operational_audit_event_by_id(client):
    event = await create_manual_event(client)

    response = await client.get(f"/api/v1/operational-audit/events/{event['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == event["id"]


async def test_get_operational_audit_by_correlation_actor_and_entity(client):
    event = await create_manual_event(
        client,
        actor_id="actor-42",
        entity_type="NewsItem",
        entity_id="news-42",
        correlation_id="corr-audit-42",
    )

    by_corr = await client.get("/api/v1/operational-audit/correlation/corr-audit-42")
    by_actor = await client.get("/api/v1/operational-audit/actors/actor-42")
    by_entity = await client.get("/api/v1/operational-audit/entity/NewsItem/news-42")

    assert by_corr.status_code == 200
    assert by_corr.json()[0]["id"] == event["id"]
    assert by_actor.json()[0]["id"] == event["id"]
    assert by_entity.json()[0]["id"] == event["id"]


async def test_operational_audit_correlation_id_persisted_from_header(client):
    response = await client.post(
        "/api/v1/operational-audit/events",
        json=manual_event_payload(correlation_id=None),
        headers={"X-Correlation-ID": "corr-operational-audit-001"},
    )

    assert response.status_code == 201
    assert response.json()["correlation_id"] == "corr-operational-audit-001"


async def test_auth_rbac_protects_operational_audit_endpoints(client, monkeypatch):
    await create_manual_event(client)
    enable_auth(monkeypatch)

    missing_key = await client.get("/api/v1/operational-audit/events")
    viewer = await client.get(
        "/api/v1/operational-audit/events",
        headers=auth_headers("viewer"),
    )
    admin = await client.get(
        "/api/v1/operational-audit/events",
        headers=auth_headers("admin"),
    )
    create_missing_key = await client.post(
        "/api/v1/operational-audit/events",
        json=manual_event_payload(),
    )

    assert missing_key.status_code == 401
    assert viewer.status_code == 403
    assert admin.status_code == 200
    assert create_missing_key.status_code == 401


async def test_auth_allows_admin_to_create_manual_operational_audit_event(client, monkeypatch):
    enable_auth(monkeypatch)

    response = await client.post(
        "/api/v1/operational-audit/events",
        json=manual_event_payload(),
        headers=auth_headers("admin"),
    )

    assert response.status_code == 201
    assert response.json()["actor_role"] == "admin"


async def test_auth_blocks_viewer_from_creating_manual_operational_audit_event(client, monkeypatch):
    enable_auth(monkeypatch)

    response = await client.post(
        "/api/v1/operational-audit/events",
        json=manual_event_payload(),
        headers=auth_headers("viewer"),
    )

    assert response.status_code == 403


async def test_intake_promote_creates_operational_audit_log(client):
    signal = await create_signal(client)

    response = await client.post(
        f"/api/v1/intake/signals/{signal['id']}/promote",
        json={"create_workflow": True},
    )
    event = await latest_event(client, "intake.promote")

    assert response.status_code == 200
    assert event["entity_id"] == signal["id"]
    assert event["decision"] == "promoted"
    assert event["metadata"]["created_workflow"] is True


async def test_readiness_calculate_creates_operational_audit_log(client):
    news = await create_news(client)

    response = await client.post(f"/api/v1/editorial-readiness/news/{news['id']}/calculate")
    event = await latest_event(client, "readiness.calculate")

    assert response.status_code == 201
    assert event["news_item_id"] == news["id"]
    assert event["decision"] == "calculated"
    assert "score" in event["metadata"]


async def test_audit_check_create_creates_operational_audit_log(client):
    news = await create_news(client)

    response = await client.post(
        "/api/v1/audit/checks",
        json={
            "entity_type": "news_item",
            "entity_id": news["id"],
            "audit_status": "passed",
            "severity": "low",
            "notes": "Passed operational audit test.",
            "ready_to_advance": True,
            "publication_block_recommended": False,
            "decision_recommendation": "allow_to_continue",
        },
    )
    event = await latest_event(client, "audit.create")

    assert response.status_code == 201
    assert event["news_item_id"] == news["id"]
    assert event["metadata"]["audit_status"] == "passed"


async def test_publication_create_and_status_update_create_operational_audit_logs(client):
    news, piece, plan = await create_publishable_chain(client)

    created = await client.post(
        "/api/v1/publication-records",
        json={
            "content_piece_id": piece["id"],
            "distribution_plan_id": plan["id"],
            "news_item_id": news["id"],
            "channel": "Blog / Web",
            "publication_status": "scheduled",
        },
    )
    updated = await client.patch(
        f"/api/v1/publication-records/{created.json()['id']}/status",
        json={"publication_status": "cancelled"},
    )
    create_event = await latest_event(client, "publication.create")
    update_event = await latest_event(client, "publication.update_status")

    assert created.status_code == 201
    assert updated.status_code == 200
    assert create_event["entity_id"] == created.json()["id"]
    assert update_event["after_state"]["publication_status"] == "cancelled"


async def test_agent_output_accept_and_reject_create_operational_audit_logs(client):
    accepted_output = await create_agent_output(client)
    rejected_output = await create_agent_output(client, news_id=None)

    accepted = await client.patch(
        f"/api/v1/agent-outputs/{accepted_output['id']}/accept",
        json={"accepted_by": "operator"},
    )
    rejected = await client.patch(
        f"/api/v1/agent-outputs/{rejected_output['id']}/reject",
        json={"rejected_reason": "Insufficient evidence."},
    )
    accept_event = await latest_event(client, "agent_output.accept")
    reject_event = await latest_event(client, "agent_output.reject")

    assert accepted.status_code == 200
    assert rejected.status_code == 200
    assert accept_event["agent_output_id"] == accepted_output["id"]
    assert reject_event["agent_output_id"] == rejected_output["id"]
    assert reject_event["reason"] == "Insufficient evidence."


async def test_memory_approve_and_invalidate_create_operational_audit_logs(client):
    news = await create_news(client)
    approve_memory = await create_memory_item(client, news["id"])
    invalidate_memory = await create_memory_item(client, news["id"])

    approved = await client.patch(
        f"/api/v1/memory-items/{approve_memory['id']}/approve",
        json={"approved_by": "reviewer"},
    )
    invalidated = await client.patch(
        f"/api/v1/memory-items/{invalidate_memory['id']}/invalidate",
        json={"invalidated_by": "reviewer", "reason": "Context changed."},
    )
    approve_event = await latest_event(client, "memory.approve")
    invalidate_event = await latest_event(client, "memory.invalidate")

    assert approved.status_code == 200
    assert invalidated.status_code == 200
    assert approve_event["entity_id"] == approve_memory["id"]
    assert invalidate_event["reason"] == "Context changed."


async def test_ownership_assign_release_transfer_create_operational_audit_logs(client):
    user = await create_user(client)
    next_user = await create_user(
        client,
        email="audit-user-2@example.com",
        handle="audit_user_2",
        role="reviewer",
    )
    assignment = await create_ownership(client, user["id"])

    released = await client.patch(
        f"/api/v1/ownership/{assignment['id']}/release",
        json={"reason": "Released for test."},
    )
    transfer_seed = await create_ownership(client, user["id"], entity_id="news-2")
    transferred = await client.patch(
        f"/api/v1/ownership/{transfer_seed['id']}/transfer",
        json={"new_user_id": next_user["id"], "assigned_by": "operator"},
    )
    assign_event = await latest_event(client, "ownership.assign")
    release_event = await latest_event(client, "ownership.release")
    transfer_event = await latest_event(client, "ownership.transfer")

    assert released.status_code == 200
    assert transferred.status_code == 200
    assert assign_event["user_id"] == user["id"]
    assert release_event["ownership_id"] == assignment["id"]
    assert transfer_event["user_id"] == next_user["id"]


async def test_user_create_and_update_create_operational_audit_logs(client):
    user = await create_user(client)

    response = await client.patch(
        f"/api/v1/users/{user['id']}",
        json={"display_name": "Updated Audit User", "role": "reviewer"},
    )
    create_event = await latest_event(client, "user.create")
    update_event = await latest_event(client, "user.update")

    assert response.status_code == 200
    assert create_event["user_id"] == user["id"]
    assert update_event["after_state"]["role"] == "reviewer"


@pytest.mark.parametrize(
    ("path_suffix", "payload", "expected_action", "expected_decision"),
    [
        ("start", {"assigned_to": "operator"}, "workflow_task.start", "started"),
        ("complete", {"output_ref": "result"}, "workflow_task.complete", "completed"),
        ("fail", {"reason": "Missing source"}, "workflow_task.fail", "failed"),
        ("block", {"reason": "Missing VerificationRecord"}, "workflow_task.block", "blocked"),
        ("cancel", {"reason": "No longer needed"}, "workflow_task.cancel", "cancelled"),
        ("retry", {}, "workflow_task.retry", "retried"),
    ],
)
async def test_workflow_task_mutations_create_operational_audit_logs(
    client,
    path_suffix,
    payload,
    expected_action,
    expected_decision,
):
    task = await create_workflow_task(client)
    if path_suffix == "complete":
        await client.patch(f"/api/v1/workflow-tasks/{task['id']}/start", json={})
    if path_suffix == "retry":
        await client.patch(
            f"/api/v1/workflow-tasks/{task['id']}/fail",
            json={"reason": "Prepare retry state."},
        )

    response = await client.patch(
        f"/api/v1/workflow-tasks/{task['id']}/{path_suffix}",
        json=payload,
    )
    event = await latest_event(client, expected_action)

    assert response.status_code == 200
    assert event["workflow_task_id"] == task["id"]
    assert event["decision"] == expected_decision


async def test_admin_audit_summary_counts_groups_and_recent_events(client):
    await create_manual_event(client, event_type="system_event", outcome="succeeded")
    await create_manual_event(
        client,
        event_type="publication_event",
        action="publication.manual",
        outcome="failed",
        decision="error",
    )

    response = await client.get("/api/v1/admin/audit/summary")

    assert response.status_code == 200
    body = response.json()
    assert body["total_events"] == 2
    assert body["events_by_type"]["system_event"] == 1
    assert body["events_by_outcome"]["failed"] == 1
    assert body["events_by_decision"]["error"] == 1
    assert len(body["recent_events"]) == 2


async def test_admin_audit_summary_requires_operational_audit_read_permission(client, monkeypatch):
    await create_manual_event(client)
    enable_auth(monkeypatch)

    viewer = await client.get("/api/v1/admin/audit/summary", headers=auth_headers("viewer"))
    admin = await client.get("/api/v1/admin/audit/summary", headers=auth_headers("admin"))

    assert viewer.status_code == 403
    assert admin.status_code == 200


async def test_operational_audit_migration_exists():
    from pathlib import Path

    migration = Path("alembic/versions/20260702_0010_add_operational_audit_log.py")

    assert migration.exists()
    assert "operational_audit_logs" in migration.read_text(encoding="utf-8")
