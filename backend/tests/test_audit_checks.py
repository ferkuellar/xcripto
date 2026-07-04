AUDIT_PAYLOAD = {
    "entity_type": "news_item",
    "entity_id": "news-123",
    "audit_status": "warning",
    "severity": "high",
    "decision_recommendation": "needs_revision",
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


# --- Regression: canonical audit catalog unified with editorial gates (P1 fix #2) ---


async def test_accepts_canonical_passing_values(client):
    response = await client.post(
        "/api/v1/audit/checks",
        json={
            **AUDIT_PAYLOAD,
            "audit_status": "passed",
            "decision_recommendation": "allow_to_continue",
            "ready_to_advance": True,
            "publication_block_recommended": False,
            "missing_requirements": [],
            "audit_flags": [],
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["audit_status"] == "passed"
    assert body["decision_recommendation"] == "allow_to_continue"


async def test_rejects_legacy_pass_status(client):
    response = await client.post(
        "/api/v1/audit/checks", json={**AUDIT_PAYLOAD, "audit_status": "pass"}
    )

    assert response.status_code == 422
    details = str(response.json())
    assert "passed" in details  # el mensaje debe guiar al valor canonico


async def test_rejects_legacy_fail_status(client):
    response = await client.post(
        "/api/v1/audit/checks", json={**AUDIT_PAYLOAD, "audit_status": "fail"}
    )

    assert response.status_code == 422


async def test_rejects_free_text_decision_recommendation(client):
    response = await client.post(
        "/api/v1/audit/checks",
        json={**AUDIT_PAYLOAD, "decision_recommendation": "Needs a second independent source."},
    )

    assert response.status_code == 422
    assert "allow_to_continue" in str(response.json())


async def test_decision_recommendation_is_optional(client):
    payload = {**AUDIT_PAYLOAD}
    payload.pop("decision_recommendation")

    response = await client.post("/api/v1/audit/checks", json=payload)

    assert response.status_code == 201
    assert response.json()["decision_recommendation"] is None
