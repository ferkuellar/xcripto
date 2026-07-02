NEWS_PAYLOAD = {
    "title": "Bitcoin ETF sees record inflows",
    "summary": "Institutional inflows into spot BTC ETFs reached a new daily record.",
    "category": "markets",
    "priority": "P1",
    "source_url": "https://example.com/etf-inflows",
    "source_name": "Example Wire",
}


async def test_intake_news(client):
    response = await client.post("/api/v1/news/intake", json=NEWS_PAYLOAD)

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == NEWS_PAYLOAD["title"]
    assert body["status"] == "detected"
    assert body["priority"] == "P1"
    assert body["id"]
    assert body["correlation_id"]  # filled from middleware when not provided


async def test_intake_news_persists_header_correlation_id(client):
    response = await client.post(
        "/api/v1/news/intake",
        json=NEWS_PAYLOAD,
        headers={"X-Correlation-ID": "corr-test-news-001"},
    )

    assert response.status_code == 201
    assert response.headers["X-Correlation-ID"] == "corr-test-news-001"
    assert response.json()["correlation_id"] == "corr-test-news-001"


async def test_intake_rejects_invalid_priority(client):
    response = await client.post(
        "/api/v1/news/intake", json={**NEWS_PAYLOAD, "priority": "P9"}
    )

    assert response.status_code == 422
    assert response.json()["success"] is False


async def test_list_news(client):
    await client.post("/api/v1/news/intake", json=NEWS_PAYLOAD)
    await client.post("/api/v1/news/intake", json={**NEWS_PAYLOAD, "title": "Second item"})

    response = await client.get("/api/v1/news")

    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_news_by_id(client):
    created = (await client.post("/api/v1/news/intake", json=NEWS_PAYLOAD)).json()

    response = await client.get(f"/api/v1/news/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


async def test_get_news_not_found(client):
    response = await client.get("/api/v1/news/does-not-exist")

    assert response.status_code == 404


async def test_update_news_status(client):
    created = (await client.post("/api/v1/news/intake", json=NEWS_PAYLOAD)).json()

    response = await client.patch(
        f"/api/v1/news/{created['id']}/status", json={"status": "registered"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "registered"


async def test_update_news_status_blocks_detected_to_verified(client):
    created = (await client.post("/api/v1/news/intake", json=NEWS_PAYLOAD)).json()

    response = await client.patch(
        f"/api/v1/news/{created['id']}/status", json={"status": "verified"}
    )

    assert response.status_code == 400
    assert response.json()["success"] is False
    assert response.json()["error"] == "Invalid status transition from detected to verified"


async def test_update_news_status_blocks_rumor_to_published(client):
    created = (
        await client.post("/api/v1/news/intake", json={**NEWS_PAYLOAD, "status": "rumor"})
    ).json()

    response = await client.patch(
        f"/api/v1/news/{created['id']}/status", json={"status": "published"}
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Invalid status transition from rumor to published"


async def test_update_news_status_allows_published_to_corrected(client):
    created = (
        await client.post("/api/v1/news/intake", json={**NEWS_PAYLOAD, "status": "published"})
    ).json()

    response = await client.patch(
        f"/api/v1/news/{created['id']}/status", json={"status": "corrected"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "corrected"


async def test_update_news_status_allows_published_to_retracted(client):
    created = (
        await client.post("/api/v1/news/intake", json={**NEWS_PAYLOAD, "status": "published"})
    ).json()

    response = await client.patch(
        f"/api/v1/news/{created['id']}/status", json={"status": "retracted"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "retracted"


async def test_update_news_status_rejects_unknown_status(client):
    created = (await client.post("/api/v1/news/intake", json=NEWS_PAYLOAD)).json()

    response = await client.patch(
        f"/api/v1/news/{created['id']}/status", json={"status": "not-a-status"}
    )

    assert response.status_code == 422
