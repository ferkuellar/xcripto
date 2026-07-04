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


# --- List filters and total count (GET /api/v1/news) ---

SECOND_PAYLOAD = {
    "title": "SEC opens consultation on custody rules",
    "summary": "The regulator opened a public consultation window.",
    "category": "regulation",
    "priority": "P0",
    "source_url": "https://sec.gov/consultation",
    "source_name": "SEC Newsroom",
}


async def _seed_two_items(client):
    first = (await client.post("/api/v1/news/intake", json=NEWS_PAYLOAD)).json()
    second = (await client.post("/api/v1/news/intake", json=SECOND_PAYLOAD)).json()
    return first, second


async def test_list_news_without_filters_returns_total_header(client):
    await _seed_two_items(client)

    response = await client.get("/api/v1/news")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.headers["X-Total-Count"] == "2"


async def test_list_news_filter_by_category(client):
    await _seed_two_items(client)

    response = await client.get("/api/v1/news", params={"category": "regulation"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["category"] == "regulation"
    assert response.headers["X-Total-Count"] == "1"


async def test_list_news_filter_by_priority(client):
    await _seed_two_items(client)

    response = await client.get("/api/v1/news", params={"priority": "P0"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["priority"] == "P0"


async def test_list_news_rejects_invalid_priority_filter(client):
    response = await client.get("/api/v1/news", params={"priority": "P9"})

    assert response.status_code == 400


async def test_list_news_filter_by_source_case_insensitive(client):
    await _seed_two_items(client)

    response = await client.get("/api/v1/news", params={"source": "sec"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["source_name"] == "SEC Newsroom"


async def test_list_news_search_q_matches_title_case_insensitive(client):
    await _seed_two_items(client)

    response = await client.get("/api/v1/news", params={"q": "consultation"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert "consultation" in body[0]["title"].lower()


async def test_list_news_search_q_matches_summary(client):
    await _seed_two_items(client)

    response = await client.get("/api/v1/news", params={"q": "institutional inflows"})

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_list_news_q_escapes_like_wildcards(client):
    await _seed_two_items(client)

    response = await client.get("/api/v1/news", params={"q": "%"})

    assert response.status_code == 200
    assert response.json() == []
    assert response.headers["X-Total-Count"] == "0"


async def test_list_news_combined_filters(client):
    await _seed_two_items(client)

    response = await client.get(
        "/api/v1/news",
        params={"q": "SEC", "category": "regulation", "priority": "P0", "status": "detected"},
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == SECOND_PAYLOAD["title"]
    assert response.headers["X-Total-Count"] == "1"


async def test_list_news_limit_offset_with_total(client):
    await _seed_two_items(client)

    page_one = await client.get("/api/v1/news", params={"limit": 1, "offset": 0})
    page_two = await client.get("/api/v1/news", params={"limit": 1, "offset": 1})

    assert page_one.status_code == 200
    assert page_two.status_code == 200
    assert len(page_one.json()) == 1
    assert len(page_two.json()) == 1
    assert page_one.headers["X-Total-Count"] == "2"
    assert page_two.headers["X-Total-Count"] == "2"
    assert page_one.json()[0]["id"] != page_two.json()[0]["id"]


async def test_list_news_no_results_returns_empty_and_zero_total(client):
    await _seed_two_items(client)

    response = await client.get("/api/v1/news", params={"q": "nonexistent-term-xyz"})

    assert response.status_code == 200
    assert response.json() == []
    assert response.headers["X-Total-Count"] == "0"
