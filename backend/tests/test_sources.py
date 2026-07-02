SOURCE_PAYLOAD = {
    "source_name": "Example Wire",
    "source_url": "https://example.com",
    "source_type": "news_outlet",
    "source_status": "active",
    "trust_level": "T1",
    "notes": "Primary market data source.",
}


async def test_create_source(client):
    response = await client.post("/api/v1/sources", json=SOURCE_PAYLOAD)

    assert response.status_code == 201
    body = response.json()
    assert body["source_name"] == SOURCE_PAYLOAD["source_name"]
    assert body["trust_level"] == "T1"
    assert body["id"]


async def test_create_source_rejects_invalid_trust_level(client):
    response = await client.post(
        "/api/v1/sources", json={**SOURCE_PAYLOAD, "trust_level": "T9"}
    )

    assert response.status_code == 422


async def test_list_sources(client):
    await client.post("/api/v1/sources", json=SOURCE_PAYLOAD)

    response = await client.get("/api/v1/sources")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_source_by_id(client):
    created = (await client.post("/api/v1/sources", json=SOURCE_PAYLOAD)).json()

    response = await client.get(f"/api/v1/sources/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
