from app.core.config import get_settings

NEWS_PAYLOAD = {
    "title": "Bitcoin ETF sees record inflows",
    "summary": "Institutional inflows into spot BTC ETFs reached a new daily record.",
    "category": "markets",
    "priority": "P1",
    "source_url": "https://example.com/etf-inflows",
    "source_name": "Example Wire",
}


async def create_news_item(client) -> dict:
    response = await client.post("/api/v1/news/intake", json=NEWS_PAYLOAD)
    assert response.status_code == 201
    return response.json()


async def create_workflow(client, news_id: str) -> dict:
    response = await client.post(
        f"/api/v1/workflows/news/{news_id}/start",
        json={"workflow_type": "editorial_pipeline"},
    )
    assert response.status_code == 201
    return response.json()


def agent_output_payload(news_id: str, **overrides) -> dict:
    payload = {
        "agent_name": "NewsScoutAgent",
        "agent_version": "0.1.0",
        "output_type": "news_scout_report",
        "status": "stored",
        "news_item_id": news_id,
        "summary": "Scout report for ETF inflow signal.",
        "payload": {"signals": [{"title": "ETF inflows", "confidence": "medium"}]},
        "risk_flags": [],
        "missing_requirements": [],
        "next_agent": "SourceValidatorAgent",
    }
    return {**payload, **overrides}


async def create_agent_output(client, news_id: str, **overrides) -> dict:
    response = await client.post(
        "/api/v1/agent-outputs",
        json=agent_output_payload(news_id, **overrides),
    )
    assert response.status_code == 201
    return response.json()


async def test_create_agent_output_with_valid_news_item(client):
    news = await create_news_item(client)

    output = await create_agent_output(client, news["id"])

    assert output["news_item_id"] == news["id"]
    assert output["agent_name"] == "NewsScoutAgent"
    assert output["status"] == "stored"


async def test_create_agent_output_blocks_missing_relation(client):
    response = await client.post(
        "/api/v1/agent-outputs",
        json={
            "agent_name": "NewsScoutAgent",
            "output_type": "news_scout_report",
            "summary": "No relation.",
            "payload": {"signals": ["orphan"]},
        },
    )

    assert response.status_code == 400


async def test_create_agent_output_blocks_missing_news_item(client):
    response = await client.post(
        "/api/v1/agent-outputs",
        json=agent_output_payload("missing-news"),
    )

    assert response.status_code == 404


async def test_create_agent_output_blocks_invalid_agent_name(client):
    news = await create_news_item(client)

    response = await client.post(
        "/api/v1/agent-outputs",
        json=agent_output_payload(news["id"], agent_name="UnknownAgent"),
    )

    assert response.status_code == 422


async def test_create_agent_output_blocks_invalid_output_type(client):
    news = await create_news_item(client)

    response = await client.post(
        "/api/v1/agent-outputs",
        json=agent_output_payload(news["id"], output_type="not-a-real-output"),
    )

    assert response.status_code == 422


async def test_create_agent_output_blocks_empty_payload(client):
    news = await create_news_item(client)

    response = await client.post(
        "/api/v1/agent-outputs",
        json=agent_output_payload(news["id"], payload={}),
    )

    assert response.status_code == 422


async def test_list_agent_outputs(client):
    news = await create_news_item(client)
    await create_agent_output(client, news["id"])

    response = await client.get("/api/v1/agent-outputs")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_filter_agent_outputs_by_agent_name(client):
    news = await create_news_item(client)
    await create_agent_output(client, news["id"])

    response = await client.get("/api/v1/agent-outputs", params={"agent_name": "NewsScoutAgent"})

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_filter_agent_outputs_by_output_type(client):
    news = await create_news_item(client)
    await create_agent_output(client, news["id"])

    response = await client.get(
        "/api/v1/agent-outputs",
        params={"output_type": "news_scout_report"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_filter_agent_outputs_by_status(client):
    news = await create_news_item(client)
    await create_agent_output(client, news["id"])

    response = await client.get("/api/v1/agent-outputs", params={"status": "stored"})

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_agent_output_by_id(client):
    news = await create_news_item(client)
    output = await create_agent_output(client, news["id"])

    response = await client.get(f"/api/v1/agent-outputs/{output['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == output["id"]


async def test_get_agent_outputs_by_news_id(client):
    news = await create_news_item(client)
    await create_agent_output(client, news["id"])

    response = await client.get(f"/api/v1/news/{news['id']}/agent-outputs")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_agent_outputs_by_workflow_run_id(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    await create_agent_output(client, news["id"], workflow_run_id=workflow["id"])

    response = await client.get(f"/api/v1/workflows/{workflow['id']}/agent-outputs")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_accept_agent_output(client):
    news = await create_news_item(client)
    output = await create_agent_output(client, news["id"])

    response = await client.patch(
        f"/api/v1/agent-outputs/{output['id']}/accept",
        json={"accepted_by": "operator"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "accepted"
    assert response.json()["accepted"] is True
    assert response.json()["accepted_by"] == "operator"


async def test_reject_agent_output(client):
    news = await create_news_item(client)
    output = await create_agent_output(client, news["id"])

    response = await client.patch(
        f"/api/v1/agent-outputs/{output['id']}/reject",
        json={"rejected_reason": "Changed certainty without evidence."},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "rejected"
    assert response.json()["accepted"] is False


async def test_supersede_agent_output_with_valid_output(client):
    news = await create_news_item(client)
    old_output = await create_agent_output(client, news["id"])
    new_output = await create_agent_output(
        client,
        news["id"],
        summary="Updated scout report.",
    )

    response = await client.patch(
        f"/api/v1/agent-outputs/{old_output['id']}/supersede",
        json={"superseded_by_output_id": new_output["id"]},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "superseded"
    assert response.json()["superseded_by_output_id"] == new_output["id"]


async def test_supersede_agent_output_blocks_self_reference(client):
    news = await create_news_item(client)
    output = await create_agent_output(client, news["id"])

    response = await client.patch(
        f"/api/v1/agent-outputs/{output['id']}/supersede",
        json={"superseded_by_output_id": output["id"]},
    )

    assert response.status_code == 400


async def test_supersede_agent_output_blocks_missing_replacement(client):
    news = await create_news_item(client)
    output = await create_agent_output(client, news["id"])

    response = await client.patch(
        f"/api/v1/agent-outputs/{output['id']}/supersede",
        json={"superseded_by_output_id": "missing-output"},
    )

    assert response.status_code == 404


async def test_human_review_required_is_enabled_by_sensitive_risk_flags(client):
    news = await create_news_item(client)

    output = await create_agent_output(
        client,
        news["id"],
        risk_flags=["financial_advice_risk"],
    )

    assert output["human_review_required"] is True
    assert output["status"] == "pending_review"


async def test_correlation_id_persisted_from_header(client):
    news = await create_news_item(client)

    response = await client.post(
        "/api/v1/agent-outputs",
        json=agent_output_payload(news["id"]),
        headers={"X-Correlation-ID": "corr-agent-output-001"},
    )

    assert response.status_code == 201
    assert response.json()["correlation_id"] == "corr-agent-output-001"


async def test_auth_protects_agent_output_post(client, monkeypatch):
    news = await create_news_item(client)
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.post("/api/v1/agent-outputs", json=agent_output_payload(news["id"]))

    assert response.status_code == 401


async def test_auth_protects_agent_output_accept(client, monkeypatch):
    news = await create_news_item(client)
    output = await create_agent_output(client, news["id"])
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.patch(
        f"/api/v1/agent-outputs/{output['id']}/accept",
        json={"accepted_by": "operator"},
    )

    assert response.status_code == 401


async def test_auth_protects_agent_output_reject(client, monkeypatch):
    news = await create_news_item(client)
    output = await create_agent_output(client, news["id"])
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.patch(
        f"/api/v1/agent-outputs/{output['id']}/reject",
        json={"rejected_reason": "Needs evidence."},
    )

    assert response.status_code == 401


async def test_auth_protects_agent_output_supersede(client, monkeypatch):
    news = await create_news_item(client)
    output = await create_agent_output(client, news["id"])
    replacement = await create_agent_output(client, news["id"], summary="Replacement.")
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.patch(
        f"/api/v1/agent-outputs/{output['id']}/supersede",
        json={"superseded_by_output_id": replacement["id"]},
    )

    assert response.status_code == 401
