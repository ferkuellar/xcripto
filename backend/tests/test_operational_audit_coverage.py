"""P8.1: OperationalAuditLog coverage for NewsItem status transitions and
SourceReference registration (gap detected by the P8 controlled newsroom pilot)."""

NEWS_PAYLOAD = {
    "title": "Audit coverage news",
    "summary": "Synthetic item for audit coverage.",
    "category": "markets",
    "priority": "P2",
    "source_url": "https://example.com/audit-coverage",
    "source_name": "Audit Coverage Wire",
}

VALID_AUDIT_PAYLOAD = {
    "entity_type": "news_item",
    "entity_id": "placeholder",
    "audit_status": "passed",
    "severity": "medium",
    "decision_recommendation": "allow_to_continue",
    "ready_to_advance": True,
    "publication_block_recommended": False,
    "missing_requirements": [],
    "audit_flags": [],
}


async def create_news(client, **overrides) -> dict:
    response = await client.post("/api/v1/news/intake", json={**NEWS_PAYLOAD, **overrides})
    assert response.status_code == 201
    return response.json()


async def register_source(client, *, source_url, source_name, trust_level="T1",
                          source_status="active") -> dict:
    response = await client.post(
        "/api/v1/sources",
        json={
            "source_name": source_name,
            "source_url": source_url,
            "source_type": "news_outlet",
            "source_status": source_status,
            "trust_level": trust_level,
        },
    )
    assert response.status_code == 201
    return response.json()


async def set_status(client, news_id, status, **headers):
    return await client.patch(
        f"/api/v1/news/{news_id}/status", json={"status": status}, headers=headers or None
    )


async def move_to_reviewing(client, news_id):
    for st in ["registered", "classified", "validating", "verified",
               "prioritized", "drafting", "reviewing"]:
        assert (await set_status(client, news_id, st)).status_code == 200


async def pass_audit(client, news_id):
    payload = {**VALID_AUDIT_PAYLOAD, "entity_id": news_id}
    assert (await client.post("/api/v1/audit/checks", json=payload)).status_code == 201


async def events(client, **params):
    response = await client.get("/api/v1/operational-audit/events", params=params)
    assert response.status_code == 200
    return response.json()


# --- NewsItem status transitions ---


async def test_successful_transition_is_audited(client):
    news = await create_news(client)

    assert (await set_status(client, news["id"], "registered")).status_code == 200

    evs = await events(client, news_item_id=news["id"], action="news.status.transition")
    assert len(evs) == 1
    ev = evs[0]
    assert ev["event_type"] == "news_event"
    assert ev["outcome"] == "succeeded"
    assert ev["decision"] == "updated"
    assert ev["before_state"] == {"status": "detected"}
    assert ev["after_state"] == {"status": "registered"}
    assert ev["metadata"]["previous_status"] == "detected"
    assert ev["metadata"]["new_status"] == "registered"


async def test_gate_blocked_transition_is_audited(client):
    news = await create_news(client)
    # S4 source (T3) without strong verification -> source-quality gate blocks approve.
    await register_source(
        client, source_url=NEWS_PAYLOAD["source_url"],
        source_name=NEWS_PAYLOAD["source_name"], trust_level="T3",
    )
    await move_to_reviewing(client, news["id"])
    await pass_audit(client, news["id"])

    blocked = await set_status(client, news["id"], "approved")
    assert blocked.status_code == 409

    evs = await events(client, news_item_id=news["id"], decision="blocked")
    assert len(evs) == 1
    ev = evs[0]
    assert ev["outcome"] == "blocked"
    assert ev["metadata"]["blocked_by_gate"] is True
    assert ev["metadata"]["attempted_status"] == "approved"
    assert ev["reason"]  # gate reason recorded


async def test_invalid_transition_is_audited_as_failed(client):
    news = await create_news(client)

    invalid = await set_status(client, news["id"], "verified")  # detected -> verified is invalid
    assert invalid.status_code == 400

    evs = await events(client, news_item_id=news["id"], outcome="failed")
    assert len(evs) == 1
    assert evs[0]["decision"] == "deny"
    assert evs[0]["metadata"]["attempted_status"] == "verified"


# --- SourceReference registration ---


async def test_source_registration_is_audited_with_quality(client):
    source = await register_source(
        client, source_url="https://sec.gov/filing", source_name="SEC",
        trust_level="T0", source_status="active",
    )

    evs = await events(client, entity_id=source["id"], event_type="source_event")
    assert len(evs) == 1
    md = evs[0]["metadata"]
    assert evs[0]["decision"] == "created"
    assert md["trust_level"] == "T0"
    assert md["source_status"] == "active"
    assert md["quality_level"] == "S1"
    assert md["allowed_for_fact_publication"] is True
    assert md["requires_strong_verification"] is False
    assert md["disqualified"] is False


async def test_blocked_source_registration_is_audited_as_disqualified(client):
    source = await register_source(
        client, source_url="https://rumor.example/blocked", source_name="Blocked Src",
        trust_level="T0", source_status="blocked",
    )

    evs = await events(client, entity_id=source["id"], event_type="source_event")
    md = evs[0]["metadata"]
    assert md["disqualified"] is True
    assert md["allowed_for_fact_publication"] is False


# --- Propagation + secret hygiene ---


async def test_correlation_and_actor_role_propagate_to_audit(client):
    news = await create_news(client)

    response = await set_status(
        client, news["id"], "registered",
        **{"X-Correlation-ID": "corr-audit-cov-1", "X-Actor-Role": "editor"},
    )
    assert response.status_code == 200

    evs = await events(client, correlation_id="corr-audit-cov-1")
    assert len(evs) == 1
    assert evs[0]["actor_role"] == "editor"
    assert evs[0]["correlation_id"] == "corr-audit-cov-1"


async def test_audit_payload_redacts_url_query_and_leaks_no_api_key(client):
    source = await register_source(
        client,
        source_url="https://src.example/path?token=SECRET123&x=1",
        source_name="Redacted Src",
    )

    evs = await events(client, entity_id=source["id"], event_type="source_event")
    ev = evs[0]
    # Query string (possible token) stripped; path preserved.
    assert ev["metadata"]["source_url"] == "https://src.example/path"
    assert "SECRET123" not in str(ev)
    # No API key material anywhere in the audit record.
    for blob in (str(ev.get("metadata")), str(ev.get("before_state")), str(ev.get("after_state"))):
        assert "dev-secret" not in blob
        assert "X-API-Key" not in blob
