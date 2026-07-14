from app.core.config import get_settings

NEWS_PAYLOAD = {
    "title": "Bitcoin ETF sees record inflows",
    "summary": "Institutional inflows into spot BTC ETFs reached a new daily record.",
    "category": "markets",
    "priority": "P1",
    "source_url": "https://example.com/etf-inflows",
    "source_name": "Example Wire",
}


async def create_news_item(client) -> dict:
    response = await client.post("/api/v1/news/intake", json=NEWS_PAYLOAD)
    assert response.status_code == 201
    return response.json()


def verification_payload(news_id: str) -> dict:
    return {
        "news_item_id": news_id,
        "verification_status": "verified",
        "evidence_level": "E3",
        "confidence_level": "C4",
        "summary": "Confirmed against primary and secondary sources.",
        "verified_claims": ["ETF inflows increased"],
        "unverified_claims": [],
        "contradictions": [],
        "source_refs": ["https://example.com/etf-inflows"],
        "human_review_required": False,
        "reviewer": "editorial-desk",
    }


def risk_review_payload(news_id: str) -> dict:
    return {
        "news_item_id": news_id,
        "entity_type": "news_item",
        "entity_id": news_id,
        "risk_level": "medium",
        "severity": "R-SEV-1",
        "decision_recommendation": "allow_with_minor_edits",
        "risk_flags": ["market_sensitive"],
        "summary": "Market-sensitive but publishable with neutral language.",
        "required_disclaimers": ["Not financial advice."],
        "language_restrictions": ["avoid price prediction"],
        "human_review_required": True,
        "publication_block_recommended": False,
        "reviewer": "risk-editor",
    }


def content_piece_payload(news_id: str, **overrides) -> dict:
    payload = {
        "news_item_id": news_id,
        "content_type": "news_article",
        "title": "Bitcoin ETF inflows hit new record",
        "summary": "A concise editorial summary of the inflow signal.",
        "body": "Institutional inflows into spot BTC ETFs reached a new daily record.",
        "status": "drafting",
        "category": "markets",
        "priority": "P1",
        "verification_status": "verified",
        "risk_level": "medium",
        "source_refs": ["https://example.com/etf-inflows"],
        "disclaimer_required": True,
        "human_review_required": True,
        "owner": "editorial-desk",
    }
    return {**payload, **overrides}


async def create_content_piece(client, news_id: str, **overrides) -> dict:
    response = await client.post(
        "/api/v1/content-pieces",
        json=content_piece_payload(news_id, **overrides),
    )
    assert response.status_code == 201
    return response.json()


def distribution_plan_payload(news_id: str, content_piece_id: str, **overrides) -> dict:
    payload = {
        "content_piece_id": content_piece_id,
        "news_item_id": news_id,
        "primary_channel": "Blog / Web",
        "secondary_channels": ["LinkedIn", "X / Twitter"],
        "distribution_type": "primary_publication",
        "status": "ready_for_review",
        "owner": "distribution-desk",
        "dependencies": ["editorial approval"],
        "metric_plan": {"primary_metric": "views"},
        "risk_level": "medium",
        "publication_readiness": "ready",
    }
    return {**payload, **overrides}


async def create_distribution_plan(
    client,
    news_id: str,
    content_piece_id: str,
    **overrides,
) -> dict:
    response = await client.post(
        "/api/v1/distribution-plans",
        json=distribution_plan_payload(news_id, content_piece_id, **overrides),
    )
    assert response.status_code == 201
    return response.json()


def publication_record_payload(
    news_id: str,
    content_piece_id: str,
    distribution_plan_id: str,
    **overrides,
) -> dict:
    payload = {
        "content_piece_id": content_piece_id,
        "distribution_plan_id": distribution_plan_id,
        "news_item_id": news_id,
        "channel": "Blog / Web",
        "publication_status": "scheduled",
        "owner": "publisher",
        "notes": "Scheduled through editorial desk.",
    }
    return {**payload, **overrides}


async def create_publishable_chain(client) -> tuple[dict, dict, dict]:
    news = await create_news_item(client)
    piece = await create_content_piece(client, news["id"], status="approved")
    plan = await create_distribution_plan(client, news["id"], piece["id"], status="scheduled")
    return news, piece, plan


async def test_create_verification_record(client):
    news = await create_news_item(client)

    response = await client.post(
        "/api/v1/verification-records",
        json=verification_payload(news["id"]),
    )

    assert response.status_code == 201
    assert response.json()["news_item_id"] == news["id"]


async def test_list_verification_records(client):
    news = await create_news_item(client)
    await client.post("/api/v1/verification-records", json=verification_payload(news["id"]))

    response = await client.get("/api/v1/verification-records")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_verification_record_by_id(client):
    news = await create_news_item(client)
    created = (
        await client.post("/api/v1/verification-records", json=verification_payload(news["id"]))
    ).json()

    response = await client.get(f"/api/v1/verification-records/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


async def test_create_risk_review(client):
    news = await create_news_item(client)

    response = await client.post("/api/v1/risk-reviews", json=risk_review_payload(news["id"]))

    assert response.status_code == 201
    assert response.json()["risk_level"] == "medium"


async def test_create_content_piece_valid(client):
    news = await create_news_item(client)

    response = await client.post(
        "/api/v1/content-pieces",
        json=content_piece_payload(news["id"]),
    )

    assert response.status_code == 201
    assert response.json()["status"] == "drafting"


async def test_create_content_piece_blocks_missing_news_item(client):
    response = await client.post(
        "/api/v1/content-pieces",
        json=content_piece_payload("missing-news-item"),
    )

    assert response.status_code == 404


async def test_create_content_piece_blocks_unverified_status(client):
    news = await create_news_item(client)

    response = await client.post(
        "/api/v1/content-pieces",
        json=content_piece_payload(news["id"], verification_status="unverified"),
    )

    assert response.status_code == 409


async def test_create_content_piece_blocks_critical_risk(client):
    news = await create_news_item(client)

    response = await client.post(
        "/api/v1/content-pieces",
        json=content_piece_payload(news["id"], risk_level="critical"),
    )

    assert response.status_code == 409


async def test_create_distribution_plan_valid(client):
    news = await create_news_item(client)
    piece = await create_content_piece(client, news["id"])

    response = await client.post(
        "/api/v1/distribution-plans",
        json=distribution_plan_payload(news["id"], piece["id"]),
    )

    assert response.status_code == 201
    assert response.json()["content_piece_id"] == piece["id"]


async def test_create_distribution_plan_blocks_blocked_content_piece(client):
    news = await create_news_item(client)
    piece = await create_content_piece(client, news["id"], status="blocked")

    response = await client.post(
        "/api/v1/distribution-plans",
        json=distribution_plan_payload(news["id"], piece["id"]),
    )

    assert response.status_code == 409


async def test_create_distribution_plan_blocks_rejected_content_piece(client):
    news = await create_news_item(client)
    piece = await create_content_piece(client, news["id"], status="rejected")

    response = await client.post(
        "/api/v1/distribution-plans",
        json=distribution_plan_payload(news["id"], piece["id"]),
    )

    assert response.status_code == 409


async def test_create_publication_record_valid(client):
    news, piece, plan = await create_publishable_chain(client)

    response = await client.post(
        "/api/v1/publication-records",
        json=publication_record_payload(news["id"], piece["id"], plan["id"]),
    )

    assert response.status_code == 201
    assert response.json()["publication_status"] == "scheduled"


async def test_create_publication_record_is_idempotent_for_published_xcripto_web(client):
    news, piece, plan = await create_publishable_chain(client)
    payload = publication_record_payload(
        news["id"],
        piece["id"],
        plan["id"],
        channel="XCRIPTO_WEB",
        publication_status="published",
    )

    first = await client.post("/api/v1/publication-records", json=payload)
    second = await client.post("/api/v1/publication-records", json=payload)
    records = await client.get("/api/v1/publication-records")

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["id"] == second.json()["id"]
    assert second.json()["publication_status"] == "published"
    assert len([record for record in records.json() if record["news_item_id"] == news["id"]]) == 1


async def test_create_publication_record_blocks_unapproved_content_piece(client):
    news = await create_news_item(client)
    piece = await create_content_piece(client, news["id"], status="reviewing")
    plan = await create_distribution_plan(client, news["id"], piece["id"], status="scheduled")

    response = await client.post(
        "/api/v1/publication-records",
        json=publication_record_payload(news["id"], piece["id"], plan["id"]),
    )

    assert response.status_code == 409


async def test_create_publication_record_blocks_published_without_external_reference(client):
    news, piece, plan = await create_publishable_chain(client)

    response = await client.post(
        "/api/v1/publication-records",
        json=publication_record_payload(
            news["id"], piece["id"], plan["id"], publication_status="published"
        ),
    )

    assert response.status_code == 400


async def test_correlation_id_persisted_in_new_entity(client):
    news = await create_news_item(client)

    response = await client.post(
        "/api/v1/verification-records",
        json=verification_payload(news["id"]),
        headers={"X-Correlation-ID": "corr-editorial-core-001"},
    )

    assert response.status_code == 201
    assert response.json()["correlation_id"] == "corr-editorial-core-001"


async def test_auth_protects_new_entity_post(client, monkeypatch):
    news = await create_news_item(client)
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.post(
        "/api/v1/verification-records",
        json=verification_payload(news["id"]),
    )

    assert response.status_code == 401


async def test_update_content_piece_status(client):
    news = await create_news_item(client)
    piece = await create_content_piece(client, news["id"])

    response = await client.patch(
        f"/api/v1/content-pieces/{piece['id']}/status",
        json={"status": "reviewing"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "reviewing"


async def test_nested_news_content_pieces(client):
    news = await create_news_item(client)
    await create_content_piece(client, news["id"])

    response = await client.get(f"/api/v1/news/{news['id']}/content-pieces")

    assert response.status_code == 200
    assert len(response.json()) == 1
