EXECUTION_PAYLOAD = {
    "agent_name": "news-scout",
    "agent_version": "0.1.0",
    "input_ref": "news:abc123",
    "status": "queued",
}


async def test_create_execution(client):
    response = await client.post("/api/v1/agents/executions", json=EXECUTION_PAYLOAD)

    assert response.status_code == 201
    body = response.json()
    assert body["agent_name"] == "news-scout"
    assert body["status"] == "queued"
    assert body["id"]


async def test_create_execution_rejects_invalid_status(client):
    response = await client.post(
        "/api/v1/agents/executions", json={**EXECUTION_PAYLOAD, "status": "sleeping"}
    )

    assert response.status_code == 422


async def test_list_executions_filtered_by_agent(client):
    await client.post("/api/v1/agents/executions", json=EXECUTION_PAYLOAD)
    await client.post(
        "/api/v1/agents/executions", json={**EXECUTION_PAYLOAD, "agent_name": "risk-reviewer"}
    )

    response = await client.get("/api/v1/agents/executions", params={"agent_name": "news-scout"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["agent_name"] == "news-scout"


async def test_get_execution_by_id(client):
    created = (await client.post("/api/v1/agents/executions", json=EXECUTION_PAYLOAD)).json()

    response = await client.get(f"/api/v1/agents/executions/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
