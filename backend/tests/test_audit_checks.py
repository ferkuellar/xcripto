AUDIT_PAYLOAD = {
    "entity_type": "news_item",
    "entity_id": "news-123",
    "audit_status": "warning",
    "severity": "high",
    "decision_recommendation": "Needs a second independent source.",
    "ready_to_advance": False,
    "publication_block_recommended": True,
    "missing_requirements": ["second_source"],
    "audit_flags": ["single_source"],
}


async def test_create_audit_check(client):
    response = await client.post("/api/v1/audit/checks", json=AUDIT_PAYLOAD)

    assert response.status_code == 201
    body = response.json()
    assert body["entity_type"] == "news_item"
    assert body["publication_block_recommended"] is True
    assert body["missing_requirements"] == ["second_source"]
    assert body["id"]


async def test_create_audit_check_rejects_invalid_severity(client):
    response = await client.post(
        "/api/v1/audit/checks", json={**AUDIT_PAYLOAD, "severity": "catastrophic"}
    )

    assert response.status_code == 422


async def test_list_audit_checks_filtered_by_entity(client):
    await client.post("/api/v1/audit/checks", json=AUDIT_PAYLOAD)
    await client.post(
        "/api/v1/audit/checks", json={**AUDIT_PAYLOAD, "entity_id": "news-456"}
    )

    response = await client.get("/api/v1/audit/checks", params={"entity_id": "news-123"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["entity_id"] == "news-123"


async def test_get_audit_check_by_id(client):
    created = (await client.post("/api/v1/audit/checks", json=AUDIT_PAYLOAD)).json()

    response = await client.get(f"/api/v1/audit/checks/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
