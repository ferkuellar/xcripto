from app.core.config import get_settings

USER_PAYLOAD = {
    "email": "editor@example.com",
    "display_name": "Editorial Operator",
    "handle": "editorial_operator",
    "role": "editor",
    "status": "active",
}

NEWS_PAYLOAD = {
    "title": "Bitcoin ETF sees record inflows",
    "summary": "Institutional inflows into spot BTC ETFs reached a new daily record.",
    "category": "markets",
    "priority": "P1",
    "source_url": "https://example.com/etf-inflows",
    "source_name": "Example Wire",
}


def enable_auth(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")


def auth_headers(role: str = "admin") -> dict[str, str]:
    return {"X-API-Key": "dev-secret", "X-Actor-Role": role, "X-Actor-Id": "actor-1"}


async def create_user(client, **overrides) -> dict:
    payload = {**USER_PAYLOAD, **overrides}
    response = await client.post("/api/v1/users", json=payload)
    assert response.status_code == 201
    return response.json()


async def create_news(client) -> dict:
    response = await client.post("/api/v1/news/intake", json=NEWS_PAYLOAD)
    assert response.status_code == 201
    return response.json()


async def create_signal(client) -> dict:
    response = await client.post(
        "/api/v1/intake/signals",
        json={
            "signal_type": "manual",
            "source_name": "Example Wire",
            "source_url": "https://example.com/rbac-signal",
            "raw_title": "RBAC signal",
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
            "title": "RBAC memory",
            "memory_statement": "Use clear ownership on critical edits.",
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


async def create_assignment(client, user_id: str, **overrides) -> dict:
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


async def test_create_user_account_valid(client):
    user = await create_user(client)

    assert user["display_name"] == "Editorial Operator"
    assert user["role"] == "editor"
    assert user["is_active"] is True


async def test_block_user_without_display_name(client):
    payload = {**USER_PAYLOAD}
    payload.pop("display_name")

    response = await client.post("/api/v1/users", json=payload)

    assert response.status_code == 422


async def test_block_invalid_user_role(client):
    response = await client.post("/api/v1/users", json={**USER_PAYLOAD, "role": "intern"})

    assert response.status_code == 422


async def test_block_invalid_user_status(client):
    response = await client.post("/api/v1/users", json={**USER_PAYLOAD, "status": "deleted"})

    assert response.status_code == 422


async def test_block_duplicate_user_email(client):
    await create_user(client)

    response = await client.post(
        "/api/v1/users",
        json={**USER_PAYLOAD, "handle": "other_handle"},
    )

    assert response.status_code == 409


async def test_block_duplicate_user_handle(client):
    await create_user(client)

    response = await client.post(
        "/api/v1/users",
        json={**USER_PAYLOAD, "email": "other@example.com"},
    )

    assert response.status_code == 409


async def test_list_users_and_filter_by_role(client):
    user = await create_user(client)

    response = await client.get("/api/v1/users", params={"role": "editor"})

    assert response.status_code == 200
    assert response.json()[0]["id"] == user["id"]


async def test_filter_users_by_status(client):
    user = await create_user(client, status="invited")

    response = await client.get("/api/v1/users", params={"status": "invited"})

    assert response.status_code == 200
    assert response.json()[0]["id"] == user["id"]


async def test_get_user_by_id(client):
    user = await create_user(client)

    response = await client.get(f"/api/v1/users/{user['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == user["id"]


async def test_update_user(client):
    user = await create_user(client)

    response = await client.patch(
        f"/api/v1/users/{user['id']}",
        json={"display_name": "Updated Editor", "role": "reviewer"},
    )

    assert response.status_code == 200
    assert response.json()["display_name"] == "Updated Editor"
    assert response.json()["role"] == "reviewer"


async def test_activate_user(client):
    user = await create_user(client, status="inactive", is_active=False)

    response = await client.patch(f"/api/v1/users/{user['id']}/activate")

    assert response.status_code == 200
    assert response.json()["status"] == "active"
    assert response.json()["is_active"] is True


async def test_deactivate_user(client):
    user = await create_user(client)

    response = await client.patch(f"/api/v1/users/{user['id']}/deactivate")

    assert response.status_code == 200
    assert response.json()["status"] == "inactive"
    assert response.json()["is_active"] is False


async def test_user_correlation_id_persisted_from_header(client):
    response = await client.post(
        "/api/v1/users",
        json=USER_PAYLOAD,
        headers={"X-Correlation-ID": "corr-user-001"},
    )

    assert response.status_code == 201
    assert response.json()["correlation_id"] == "corr-user-001"


async def test_auth_protects_create_user(client, monkeypatch):
    enable_auth(monkeypatch)

    response = await client.post("/api/v1/users", json=USER_PAYLOAD)

    assert response.status_code == 401


async def test_create_ownership_assignment_valid(client):
    user = await create_user(client)

    assignment = await create_assignment(client, user["id"])

    assert assignment["user_id"] == user["id"]
    assert assignment["ownership_type"] == "owner"
    assert assignment["status"] == "active"


async def test_block_ownership_with_missing_user(client):
    response = await client.post(
        "/api/v1/ownership/assign",
        json={
            "user_id": "missing",
            "entity_type": "NewsItem",
            "entity_id": "news-1",
            "ownership_type": "owner",
        },
    )

    assert response.status_code == 404


async def test_block_invalid_ownership_type(client):
    user = await create_user(client)

    response = await client.post(
        "/api/v1/ownership/assign",
        json={
            "user_id": user["id"],
            "entity_type": "NewsItem",
            "entity_id": "news-1",
            "ownership_type": "boss",
        },
    )

    assert response.status_code == 422


async def test_block_invalid_ownership_status(client):
    user = await create_user(client)

    response = await client.post(
        "/api/v1/ownership/assign",
        json={
            "user_id": user["id"],
            "entity_type": "NewsItem",
            "entity_id": "news-1",
            "ownership_type": "owner",
            "status": "open",
        },
    )

    assert response.status_code == 422


async def test_block_duplicate_active_ownership(client):
    user = await create_user(client)
    await create_assignment(client, user["id"])

    response = await client.post(
        "/api/v1/ownership/assign",
        json={
            "user_id": user["id"],
            "entity_type": "NewsItem",
            "entity_id": "news-1",
            "ownership_type": "owner",
        },
    )

    assert response.status_code == 409


async def test_list_and_filter_ownership(client):
    user = await create_user(client)
    assignment = await create_assignment(client, user["id"])

    response = await client.get(
        "/api/v1/ownership",
        params={"user_id": user["id"], "entity_type": "NewsItem", "entity_id": "news-1"},
    )

    assert response.status_code == 200
    assert response.json()[0]["id"] == assignment["id"]


async def test_get_ownership_by_id(client):
    user = await create_user(client)
    assignment = await create_assignment(client, user["id"])

    response = await client.get(f"/api/v1/ownership/{assignment['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == assignment["id"]


async def test_get_ownership_by_user(client):
    user = await create_user(client)
    assignment = await create_assignment(client, user["id"])

    response = await client.get(f"/api/v1/users/{user['id']}/ownership")

    assert response.status_code == 200
    assert response.json()[0]["id"] == assignment["id"]


async def test_get_ownership_by_entity(client):
    user = await create_user(client)
    assignment = await create_assignment(client, user["id"])

    response = await client.get("/api/v1/ownership/entity/NewsItem/news-1")

    assert response.status_code == 200
    assert response.json()[0]["id"] == assignment["id"]


async def test_release_ownership(client):
    user = await create_user(client)
    assignment = await create_assignment(client, user["id"])

    response = await client.patch(
        f"/api/v1/ownership/{assignment['id']}/release",
        json={"reason": "No longer responsible."},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "released"
    assert response.json()["released_at"] is not None


async def test_transfer_ownership(client):
    user = await create_user(client)
    next_user = await create_user(
        client,
        email="reviewer@example.com",
        handle="reviewer",
        role="reviewer",
    )
    assignment = await create_assignment(client, user["id"])

    response = await client.patch(
        f"/api/v1/ownership/{assignment['id']}/transfer",
        json={
            "new_user_id": next_user["id"],
            "assigned_by": "operator",
            "notes": "Transferred to reviewer.",
        },
    )

    assert response.status_code == 200
    assert response.json()["user_id"] == next_user["id"]
    assert response.json()["status"] == "active"


async def test_block_transfer_to_missing_user(client):
    user = await create_user(client)
    assignment = await create_assignment(client, user["id"])

    response = await client.patch(
        f"/api/v1/ownership/{assignment['id']}/transfer",
        json={"new_user_id": "missing-user"},
    )

    assert response.status_code == 404


async def test_auth_protects_ownership_mutations(client, monkeypatch):
    user = await create_user(client)
    assignment = await create_assignment(client, user["id"])
    enable_auth(monkeypatch)

    assign = await client.post(
        "/api/v1/ownership/assign",
        json={
            "user_id": user["id"],
            "entity_type": "NewsItem",
            "entity_id": "news-2",
            "ownership_type": "owner",
        },
    )
    release = await client.patch(
        f"/api/v1/ownership/{assignment['id']}/release",
        json={"reason": "No auth."},
    )
    transfer = await client.patch(
        f"/api/v1/ownership/{assignment['id']}/transfer",
        json={"new_user_id": user["id"]},
    )

    assert assign.status_code == 401
    assert release.status_code == 401
    assert transfer.status_code == 401


async def test_owner_can_execute_critical_action(client, monkeypatch):
    signal = await create_signal(client)
    enable_auth(monkeypatch)

    response = await client.post(
        f"/api/v1/intake/signals/{signal['id']}/promote",
        json={},
        headers=auth_headers("owner"),
    )

    assert response.status_code == 200


async def test_admin_can_execute_critical_action(client, monkeypatch):
    news = await create_news(client)
    enable_auth(monkeypatch)

    response = await client.post(
        f"/api/v1/editorial-readiness/news/{news['id']}/calculate",
        headers=auth_headers("admin"),
    )

    assert response.status_code == 201


async def test_viewer_cannot_promote_intake(client, monkeypatch):
    signal = await create_signal(client)
    enable_auth(monkeypatch)

    response = await client.post(
        f"/api/v1/intake/signals/{signal['id']}/promote",
        json={},
        headers=auth_headers("viewer"),
    )

    assert response.status_code == 403


async def test_viewer_cannot_approve_agent_output(client, monkeypatch):
    output = await create_agent_output(client)
    enable_auth(monkeypatch)

    response = await client.patch(
        f"/api/v1/agent-outputs/{output['id']}/accept",
        json={"accepted_by": "viewer"},
        headers=auth_headers("viewer"),
    )

    assert response.status_code == 403


async def test_viewer_cannot_approve_memory_item(client, monkeypatch):
    news = await create_news(client)
    memory = await create_memory_item(client, news["id"])
    enable_auth(monkeypatch)

    response = await client.patch(
        f"/api/v1/memory-items/{memory['id']}/approve",
        json={"approved_by": "viewer"},
        headers=auth_headers("viewer"),
    )

    assert response.status_code == 403


async def test_editor_can_promote_intake(client, monkeypatch):
    signal = await create_signal(client)
    enable_auth(monkeypatch)

    response = await client.post(
        f"/api/v1/intake/signals/{signal['id']}/promote",
        json={},
        headers=auth_headers("editor"),
    )

    assert response.status_code == 200


async def test_editor_can_update_news_cover_image(client, monkeypatch):
    news = await create_news(client)
    enable_auth(monkeypatch)

    response = await client.patch(
        f"/api/v1/news/{news['id']}/cover-image",
        json={"cover_image_url": "https://cdn.example.com/news/editor-cover.png"},
        headers=auth_headers("editor"),
    )

    assert response.status_code == 200
    assert response.json()["cover_image_url"] == "https://cdn.example.com/news/editor-cover.png"


async def test_publisher_cannot_update_news_cover_image(client, monkeypatch):
    news = await create_news(client)
    enable_auth(monkeypatch)

    response = await client.patch(
        f"/api/v1/news/{news['id']}/cover-image",
        json={"cover_image_url": "https://cdn.example.com/news/publisher-cover.png"},
        headers=auth_headers("publisher"),
    )

    assert response.status_code == 403


async def test_publisher_can_create_publication_record(client, monkeypatch):
    news = await create_news(client)
    piece = await client.post(
        "/api/v1/content-pieces",
        json={
            "news_item_id": news["id"],
            "content_type": "news_article",
            "title": "RBAC publication",
            "summary": "Summary",
            "body": "Body",
            "status": "approved",
            "category": "markets",
            "priority": "P1",
            "verification_status": "verified",
            "risk_level": "medium",
            "source_refs": ["https://example.com/etf-inflows"],
        },
    )
    assert piece.status_code == 201
    plan = await client.post(
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
    assert plan.status_code == 201
    enable_auth(monkeypatch)

    response = await client.post(
        "/api/v1/publication-records",
        json={
            "content_piece_id": piece.json()["id"],
            "distribution_plan_id": plan.json()["id"],
            "news_item_id": news["id"],
            "channel": "Blog / Web",
            "publication_status": "scheduled",
        },
        headers=auth_headers("publisher"),
    )

    assert response.status_code == 201


async def test_agent_operator_can_accept_agent_output(client, monkeypatch):
    output = await create_agent_output(client)
    enable_auth(monkeypatch)

    response = await client.patch(
        f"/api/v1/agent-outputs/{output['id']}/accept",
        json={"accepted_by": "operator"},
        headers=auth_headers("agent_operator"),
    )

    assert response.status_code == 200


async def test_without_actor_header_maintains_compatibility_when_auth_disabled(client):
    signal = await create_signal(client)

    response = await client.post(f"/api/v1/intake/signals/{signal['id']}/promote", json={})

    assert response.status_code == 200


async def test_auth_enabled_still_requires_api_key(client, monkeypatch):
    signal = await create_signal(client)
    enable_auth(monkeypatch)

    response = await client.post(
        f"/api/v1/intake/signals/{signal['id']}/promote",
        json={},
        headers={"X-Actor-Role": "owner"},
    )

    assert response.status_code == 401


async def test_insufficient_permission_returns_403(client, monkeypatch):
    news = await create_news(client)
    enable_auth(monkeypatch)

    response = await client.post(
        f"/api/v1/editorial-readiness/news/{news['id']}/calculate",
        headers=auth_headers("viewer"),
    )

    assert response.status_code == 403


async def test_readiness_calculate_respects_permission(client, monkeypatch):
    news = await create_news(client)
    enable_auth(monkeypatch)

    response = await client.post(
        f"/api/v1/editorial-readiness/news/{news['id']}/calculate",
        headers=auth_headers("analyst"),
    )

    assert response.status_code == 201


async def test_memory_approve_respects_permission(client, monkeypatch):
    news = await create_news(client)
    memory = await create_memory_item(client, news["id"])
    enable_auth(monkeypatch)

    response = await client.patch(
        f"/api/v1/memory-items/{memory['id']}/approve",
        json={"approved_by": "reviewer"},
        headers=auth_headers("reviewer"),
    )

    assert response.status_code == 200
