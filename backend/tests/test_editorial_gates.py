NEWS_PAYLOAD = {
    "title": "Bitcoin ETF sees record inflows",
    "summary": "Institutional inflows into spot BTC ETFs reached a new daily record.",
    "category": "markets",
    "priority": "P1",
    "source_url": "https://example.com/etf-inflows",
    "source_name": "Example Wire",
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


async def create_news_item(client) -> dict:
    response = await client.post("/api/v1/news/intake", json=NEWS_PAYLOAD)
    assert response.status_code == 201
    return response.json()


async def update_status(client, news_id: str, status: str):
    return await client.patch(f"/api/v1/news/{news_id}/status", json={"status": status})


async def move_to_reviewing(client, news_id: str) -> None:
    for status in [
        "registered",
        "classified",
        "validating",
        "verified",
        "prioritized",
        "drafting",
        "reviewing",
    ]:
        response = await update_status(client, news_id, status)
        assert response.status_code == 200


async def create_audit_check(client, news_id: str, **overrides) -> dict:
    payload = {**VALID_AUDIT_PAYLOAD, "entity_id": news_id, **overrides}
    response = await client.post("/api/v1/audit/checks", json=payload)
    assert response.status_code == 201
    return response.json()


async def approve_news_item(client, news_id: str) -> None:
    await move_to_reviewing(client, news_id)
    await create_audit_check(client, news_id)
    response = await update_status(client, news_id, "approved")
    assert response.status_code == 200


async def schedule_news_item(client, news_id: str) -> None:
    await approve_news_item(client, news_id)
    response = await update_status(client, news_id, "scheduled")
    assert response.status_code == 200


async def test_reviewing_to_approved_without_passing_audit_check_fails(client):
    news = await create_news_item(client)
    await move_to_reviewing(client, news["id"])

    response = await update_status(client, news["id"], "approved")

    assert response.status_code == 409
    assert (
        response.json()["error"]
        == "NewsItem cannot transition to approved without a passing AuditCheck"
    )


async def test_reviewing_to_approved_with_passing_audit_check_passes(client):
    news = await create_news_item(client)
    await move_to_reviewing(client, news["id"])
    await create_audit_check(client, news["id"])

    response = await update_status(client, news["id"], "approved")

    assert response.status_code == 200
    assert response.json()["status"] == "approved"


async def test_approved_to_scheduled_without_current_passing_audit_check_fails(client):
    news = await create_news_item(client)
    await approve_news_item(client, news["id"])
    await create_audit_check(client, news["id"], ready_to_advance=False)

    response = await update_status(client, news["id"], "scheduled")

    assert response.status_code == 409
    assert (
        response.json()["error"]
        == "NewsItem cannot transition to scheduled without a passing AuditCheck"
    )


async def test_scheduled_to_published_without_current_passing_audit_check_fails(client):
    news = await create_news_item(client)
    await schedule_news_item(client, news["id"])
    await create_audit_check(client, news["id"], ready_to_advance=False)

    response = await update_status(client, news["id"], "published")

    assert response.status_code == 409
    assert (
        response.json()["error"]
        == "NewsItem cannot transition to published without a passing AuditCheck"
    )


async def test_scheduled_to_published_with_passing_audit_check_passes(client):
    news = await create_news_item(client)
    await schedule_news_item(client, news["id"])

    response = await update_status(client, news["id"], "published")

    assert response.status_code == 200
    assert response.json()["status"] == "published"


async def test_audit_check_with_publication_block_recommended_blocks(client):
    news = await create_news_item(client)
    await move_to_reviewing(client, news["id"])
    await create_audit_check(client, news["id"], publication_block_recommended=True)

    response = await update_status(client, news["id"], "approved")

    assert response.status_code == 409


async def test_audit_check_with_ready_to_advance_false_blocks(client):
    news = await create_news_item(client)
    await move_to_reviewing(client, news["id"])
    await create_audit_check(client, news["id"], ready_to_advance=False)

    response = await update_status(client, news["id"], "approved")

    assert response.status_code == 409


async def test_audit_check_with_failed_status_blocks(client):
    news = await create_news_item(client)
    await move_to_reviewing(client, news["id"])
    await create_audit_check(client, news["id"], audit_status="failed")

    response = await update_status(client, news["id"], "approved")

    assert response.status_code == 409
