from app.core.config import get_settings

NEWS_PAYLOAD = {
    "title": "Bitcoin ETF sees record inflows",
    "summary": "Institutional inflows into spot BTC ETFs reached a new daily record.",
    "category": "markets",
    "priority": "P1",
    "source_url": "https://example.com/etf-inflows",
    "source_name": "Example Wire",
}


async def test_auth_disabled_allows_post_without_api_key(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", False)

    response = await client.post("/api/v1/news/intake", json=NEWS_PAYLOAD)

    assert response.status_code == 201


async def test_auth_enabled_blocks_post_without_api_key(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.post("/api/v1/news/intake", json=NEWS_PAYLOAD)

    assert response.status_code == 401
    assert response.json()["error"] == "Missing API key"


async def test_auth_enabled_blocks_incorrect_api_key(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.post(
        "/api/v1/news/intake",
        json=NEWS_PAYLOAD,
        headers={"X-API-Key": "wrong-secret"},
    )

    assert response.status_code == 403
    assert response.json()["error"] == "Invalid API key"


async def test_auth_enabled_allows_correct_api_key(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.post(
        "/api/v1/news/intake",
        json=NEWS_PAYLOAD,
        headers={"X-API-Key": "dev-secret"},
    )

    assert response.status_code == 201


async def test_health_never_requires_api_key(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.get("/health")

    assert response.status_code == 200
