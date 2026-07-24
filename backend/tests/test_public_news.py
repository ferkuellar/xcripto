from __future__ import annotations

from app.core.config import get_settings

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
        "title": "Bitcoin ETF sees record inflows",
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


def _distribution_plan_payload(news_id: str, content_piece_id: str) -> dict:
    return {
        "content_piece_id": content_piece_id,
        "news_item_id": news_id,
        "primary_channel": "XCRIPTO_WEB",
        "secondary_channels": [],
        "distribution_type": "primary_publication",
        "status": "scheduled",
        "owner": "distribution-desk",
        "dependencies": ["editorial approval"],
        "metric_plan": {"primary_metric": "views"},
        "risk_level": "medium",
        "publication_readiness": "ready",
    }


def _publication_record_payload(news_id: str, content_piece_id: str, plan_id: str) -> dict:
    return {
        "content_piece_id": content_piece_id,
        "distribution_plan_id": plan_id,
        "news_item_id": news_id,
        "channel": "XCRIPTO_WEB",
        "publication_status": "scheduled",
        "owner": "publisher",
        "notes": "Scheduled through editorial desk.",
    }


async def _create_canonical_publication(client, payload: dict) -> dict:
    news = (await client.post("/api/v1/news/intake", json=payload)).json()
    piece = (
        await client.post("/api/v1/content-pieces", json=_content_piece_payload(news["id"]))
    ).json()
    plan = (
        await client.post(
            "/api/v1/distribution-plans",
            json=_distribution_plan_payload(news["id"], piece["id"]),
        )
    ).json()
    publication = (
        await client.post(
            "/api/v1/publication-records",
            json={
                **_publication_record_payload(news["id"], piece["id"], plan["id"]),
                "channel": "XCRIPTO_WEB",
            },
        )
    ).json()
    publication = (
        await client.patch(
            f"/api/v1/publication-records/{publication['id']}/status",
            json={"publication_status": "published"},
        )
    ).json()
    return {"news": news, "piece": piece, "plan": plan, "publication": publication}


async def _seed_public_news(client):
    public_a = await _create_canonical_publication(client, NEWS_PUBLIC_A)
    public_b = await _create_canonical_publication(client, NEWS_PUBLIC_B)
    private_item = (await client.post("/api/v1/news/intake", json=NEWS_PRIVATE)).json()
    return public_a, public_b, private_item


async def test_public_news_list_returns_only_public_items(client):
    public_a, public_b, private_item = await _seed_public_news(client)

    response = await client.get("/api/v1/public/news")

    assert response.status_code == 200
    body = response.json()
    ids = {item["id"] for item in body}
    assert public_a["news"]["id"] in ids
    assert public_b["news"]["id"] in ids
    assert private_item["id"] not in ids
    item = next(item for item in body if item["id"] == public_a["news"]["id"])
    assert item["slug"]
    assert item["canonical_url"].endswith(f"/news/{item['slug']}")
    assert item["seo_title"] == item["title"]
    assert item["og_title"] == item["title"]
    assert item["json_ld_type"] == "NewsArticle"
    assert item["status"] == "published"


async def test_public_news_detail_by_slug(client):
    created = await _create_canonical_publication(client, NEWS_PUBLIC_A)
    slug = "bitcoin-etf-sees-record-inflows"

    response = await client.get(f"/api/v1/public/news/{slug}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == created["news"]["id"]
    assert body["slug"] == slug
    assert body["canonical_url"].endswith(f"/news/{slug}")
    assert body["body"]
    assert body["body_format"] == "markdown"
    assert body["seo_title"] == body["title"]
    assert body["author"]


async def test_public_news_exposes_cover_image_as_og_image(client):
    created = await _create_canonical_publication(client, NEWS_PUBLIC_A)
    cover_url = "https://cdn.example.com/xcripto/bitcoin-cover.png"

    update = await client.patch(
        f"/api/v1/news/{created['news']['id']}/cover-image",
        json={"cover_image_url": cover_url},
    )
    assert update.status_code == 200

    listing = await client.get("/api/v1/public/news")
    assert listing.status_code == 200
    listing_item = next(
        item for item in listing.json() if item["id"] == created["news"]["id"]
    )
    assert listing_item["cover_image_url"] == cover_url
    assert listing_item["og_image"] == cover_url

    detail = await client.get("/api/v1/public/news/bitcoin-etf-sees-record-inflows")
    assert detail.status_code == 200
    assert detail.json()["cover_image_url"] == cover_url
    assert detail.json()["og_image"] == cover_url

    clear = await client.patch(
        f"/api/v1/news/{created['news']['id']}/cover-image",
        json={"cover_image_url": None},
    )
    assert clear.status_code == 200

    listing_after_clear = await client.get("/api/v1/public/news")
    assert listing_after_clear.status_code == 200
    cleared_listing_item = next(
        item for item in listing_after_clear.json() if item["id"] == created["news"]["id"]
    )
    assert cleared_listing_item["cover_image_url"] is None
    assert cleared_listing_item["og_image"] is None

    detail_after_clear = await client.get("/api/v1/public/news/bitcoin-etf-sees-record-inflows")
    assert detail_after_clear.status_code == 200
    assert detail_after_clear.json()["cover_image_url"] is None
    assert detail_after_clear.json()["og_image"] is None


async def test_public_news_uses_configured_public_base_url(client, monkeypatch):
    created = await _create_canonical_publication(client, NEWS_PUBLIC_A)
    settings = get_settings()
    monkeypatch.setattr(settings, "public_web_base_url", "https://xcripto.com")

    response = await client.get("/api/v1/public/news")

    assert response.status_code == 200
    body = response.json()
    item = next(item for item in body if item["id"] == created["news"]["id"])
    assert item["slug"] == "bitcoin-etf-sees-record-inflows"
    assert item["canonical_url"] == "https://xcripto.com/news/bitcoin-etf-sees-record-inflows"
    assert not item["canonical_url"].startswith("http://localhost")


async def test_public_news_detail_rejects_drafts(client):
    await client.post("/api/v1/news/intake", json=NEWS_PUBLIC_A)

    response = await client.get("/api/v1/public/news/bitcoin-etf-sees-record-inflows")

    assert response.status_code == 404
    assert response.json()["error"] in {
        "Public article not found",
        "Public news item not found",
    }


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
