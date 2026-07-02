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
        f"/api/v1/news/{created['id']}/status", json={"status": "verified"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "verified"


async def test_update_news_status_rejects_unknown_status(client):
    created = (await client.post("/api/v1/news/intake", json=NEWS_PAYLOAD)).json()

    response = await client.patch(
        f"/api/v1/news/{created['id']}/status", json={"status": "not-a-status"}
    )

    assert response.status_code == 422
