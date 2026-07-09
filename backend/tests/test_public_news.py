from __future__ import annotations

NEWS_PUBLIC_A = {
    "title": "Bitcoin ETF sees record inflows",
    "summary": "Institutional inflows into spot BTC ETFs reached a new daily record.",
    "category": "markets",
    "priority": "P1",
    "source_url": "https://example.com/etf-inflows",
    "source_name": "Example Wire",
    "status": "published",
}

NEWS_PUBLIC_B = {
    "title": "SEC opens consultation on custody rules",
    "summary": "The regulator opened a public consultation window.",
    "category": "regulation",
    "priority": "P0",
    "source_url": "https://sec.gov/consultation",
    "source_name": "SEC Newsroom",
    "status": "approved",
}

NEWS_PRIVATE = {
    "title": "Internal draft should stay private",
    "summary": "This item is not public yet.",
    "category": "internal",
    "priority": "P3",
    "source_url": "https://example.com/internal",
    "source_name": "Internal Wire",
}


def _content_piece_payload(news_id: str, **overrides):
    payload = {
        "news_item_id": news_id,
        "content_type": "news_article",
        "title": "Bitcoin ETF inflows hit new record",
        "summary": "A concise editorial summary.",
        "body": "Institutional inflows reached a record.",
        "status": "approved",
        "category": "markets",
        "priority": "P1",
        "verification_status": "verified",
        "risk_level": "medium",
        "source_refs": ["https://example.com/etf-inflows"],
        "disclaimer_required": False,
        "human_review_required": False,
        "owner": "editorial-desk",
    }
    return {**payload, **overrides}


async def _seed_public_news(client):
    public_a = (await client.post("/api/v1/news/intake", json=NEWS_PUBLIC_A)).json()
    public_b = (await client.post("/api/v1/news/intake", json=NEWS_PUBLIC_B)).json()
    private_item = (await client.post("/api/v1/news/intake", json=NEWS_PRIVATE)).json()
    return public_a, public_b, private_item


async def test_public_news_list_returns_only_public_items(client):
    public_a, public_b, private_item = await _seed_public_news(client)

    response = await client.get("/api/v1/public/news")

    assert response.status_code == 200
    body = response.json()
    ids = {item["id"] for item in body}
    assert public_a["id"] in ids
    assert public_b["id"] in ids
    assert private_item["id"] not in ids
    first = body[0]
    assert first["slug"]
    assert first["canonical_url"].endswith(f"/news/{first['slug']}")
    assert first["seo_title"] == first["title"]
    assert first["og_title"] == first["title"]
    assert first["json_ld_type"] == "NewsArticle"


async def test_public_news_detail_by_slug(client):
    created = (await client.post("/api/v1/news/intake", json=NEWS_PUBLIC_A)).json()
    await client.post("/api/v1/content-pieces", json=_content_piece_payload(created["id"]))
    slug = "bitcoin-etf-sees-record-inflows"

    response = await client.get(f"/api/v1/public/news/{slug}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == created["id"]
    assert body["slug"] == slug
    assert body["canonical_url"].endswith(f"/news/{slug}")
    assert body["body"]
    assert body["body_format"] == "markdown"
    assert body["seo_title"] == body["title"]
    assert body["author"]


async def test_public_news_detail_rejects_drafts(client):
    await client.post("/api/v1/news/intake", json=NEWS_PUBLIC_A)

    response = await client.get("/api/v1/public/news/bitcoin-etf-sees-record-inflows")

    assert response.status_code == 404
    assert response.json()["error"] == "Public article not found"


async def test_public_categories_and_search(client):
    await _seed_public_news(client)

    categories = await client.get("/api/v1/public/categories")
    search = await client.get("/api/v1/public/search", params={"q": "consultation"})

    assert categories.status_code == 200
    assert set(categories.json()) == {"markets", "regulation"}
    assert search.status_code == 200
    assert len(search.json()) == 1
    assert search.json()[0]["category"] == "regulation"


async def test_public_rss_and_sitemap(client):
    await _seed_public_news(client)

    rss = await client.get("/api/v1/public/rss.xml")
    sitemap = await client.get("/sitemap.xml")

    assert rss.status_code == 200
    assert "<rss" in rss.text
    assert "bitcoin-etf-sees-record-inflows" in rss.text
    assert sitemap.status_code == 200
    assert "<urlset" in sitemap.text
    assert "/news/bitcoin-etf-sees-record-inflows" in sitemap.text
