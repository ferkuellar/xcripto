from app.core.config import get_settings

SIGNAL_PAYLOAD = {
    "signal_type": "manual",
    "source_name": "Example Wire",
    "source_url": "https://example.com/news/btc-etf/?utm_source=x&utm_campaign=y",
    "source_type": "wire",
    "raw_title": "  Bitcoin   ETF sees record inflows  ",
    "raw_summary": "  Institutional  inflows increased. ",
    "raw_content": "Institutional inflows into spot BTC ETFs reached a new record.",
    "language": "en",
    "topic": "markets",
    "asset_symbols": ["btc", " BTC "],
    "entities": ["BlackRock", " BlackRock "],
    "keywords": ["ETF", " inflows "],
    "priority": "P1",
    "confidence_level": "IC3",
}


async def create_signal(client, **overrides) -> dict:
    payload = {**SIGNAL_PAYLOAD, **overrides}
    response = await client.post("/api/v1/intake/signals", json=payload)
    assert response.status_code == 201
    return response.json()


async def create_adapter_run(client, **overrides) -> dict:
    payload = {
        "adapter_name": "manual-intake",
        "adapter_type": "manual",
        "status": "completed",
        "input_payload": {"count": 1},
        "result_payload": {"signals_created": 1},
        **overrides,
    }
    response = await client.post("/api/v1/intake/adapter-runs", json=payload)
    assert response.status_code == 201
    return response.json()


async def test_create_manual_intake_signal_valid(client):
    signal = await create_signal(client)

    assert signal["signal_type"] == "manual"
    assert signal["signal_status"] == "unique"
    assert signal["dedupe_status"] == "unique"


async def test_block_intake_signal_without_title_and_content(client):
    response = await client.post(
        "/api/v1/intake/signals",
        json={
            "signal_type": "manual",
            "raw_summary": "summary only",
            "source_name": "Example Wire",
            "source_url": "https://example.com/story",
        },
    )

    assert response.status_code == 422


async def test_normalizes_title_and_summary(client):
    signal = await create_signal(client)

    assert signal["normalized_title"] == "Bitcoin ETF sees record inflows"
    assert signal["normalized_summary"] == "Institutional inflows increased."
    assert signal["asset_symbols"] == ["BTC"]
    assert signal["entities"] == ["BlackRock"]
    assert signal["keywords"] == ["ETF", "inflows"]


async def test_canonicalizes_url_removing_utm_params(client):
    signal = await create_signal(client)

    assert signal["url_canonical"] == "https://example.com/news/btc-etf"


async def test_generates_content_hash(client):
    signal = await create_signal(client)

    assert len(signal["content_hash"]) == 64


async def test_generates_dedupe_key(client):
    signal = await create_signal(client)

    assert signal["dedupe_key"] == "bitcoin etf sees record inflows|markets|example wire"


async def test_detects_exact_duplicate_by_content_hash(client):
    original = await create_signal(client, source_url="https://example.com/a")
    duplicate = await create_signal(client, source_url="https://example.com/b")

    assert duplicate["dedupe_status"] == "exact_duplicate"
    assert duplicate["duplicate_of_signal_id"] == original["id"]


async def test_detects_exact_duplicate_by_url_canonical(client):
    original = await create_signal(client, raw_title="BTC ETF inflows", raw_content="first")
    duplicate = await create_signal(
        client,
        raw_title="Different title",
        raw_content="different content",
    )

    assert duplicate["dedupe_status"] == "exact_duplicate"
    assert duplicate["duplicate_of_signal_id"] == original["id"]


async def test_detects_probable_duplicate_by_similar_title(client):
    original = await create_signal(
        client,
        source_url="https://example.com/original",
        raw_title="Bitcoin ETF sees record inflows",
        topic="markets",
        source_name="Example Wire",
    )
    duplicate = await create_signal(
        client,
        source_url="https://example.com/related",
        raw_title="Bitcoin ETF sees record inflow",
        raw_content="A similar but not identical report.",
        topic="crypto",
        source_name="Other Wire",
    )

    assert duplicate["dedupe_status"] == "probable_duplicate"
    assert duplicate["duplicate_of_signal_id"] == original["id"]
    assert duplicate["dedupe_score"] >= 0.88


async def test_marks_signal_unique_when_no_duplicate(client):
    signal = await create_signal(
        client,
        raw_title="Ethereum staking queue grows",
        raw_content="A different signal.",
        source_url="https://example.com/eth",
    )

    assert signal["dedupe_status"] == "unique"


async def test_list_intake_signals(client):
    signal = await create_signal(client)

    response = await client.get("/api/v1/intake/signals")

    assert response.status_code == 200
    assert response.json()[0]["id"] == signal["id"]


async def test_filter_intake_signals_by_signal_status(client):
    signal = await create_signal(client)

    response = await client.get(
        "/api/v1/intake/signals",
        params={"signal_status": "unique"},
    )

    assert response.status_code == 200
    assert response.json()[0]["id"] == signal["id"]


async def test_filter_intake_signals_by_dedupe_status(client):
    signal = await create_signal(client)

    response = await client.get(
        "/api/v1/intake/signals",
        params={"dedupe_status": "unique"},
    )

    assert response.status_code == 200
    assert response.json()[0]["id"] == signal["id"]


async def test_get_intake_signal_by_id(client):
    signal = await create_signal(client)

    response = await client.get(f"/api/v1/intake/signals/{signal['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == signal["id"]


async def test_recalculate_dedupe(client):
    signal = await create_signal(client)

    response = await client.post(f"/api/v1/intake/signals/{signal['id']}/dedupe")

    assert response.status_code == 200
    assert response.json()["dedupe_status"] == "unique"


async def test_reject_signal(client):
    signal = await create_signal(client)

    response = await client.patch(
        f"/api/v1/intake/signals/{signal['id']}/reject",
        json={"reason": "Low quality."},
    )

    assert response.status_code == 200
    assert response.json()["signal_status"] == "rejected"
    assert response.json()["normalized_payload"]["rejection_reason"] == "Low quality."


async def test_archive_signal(client):
    signal = await create_signal(client)

    response = await client.patch(f"/api/v1/intake/signals/{signal['id']}/archive")

    assert response.status_code == 200
    assert response.json()["signal_status"] == "archived"


async def test_promote_unique_signal_to_news_item(client):
    signal = await create_signal(client)

    response = await client.post(f"/api/v1/intake/signals/{signal['id']}/promote", json={})

    assert response.status_code == 200
    promoted = response.json()
    assert promoted["signal_status"] == "promoted"
    assert promoted["promoted_news_item_id"] is not None


async def test_block_promotion_of_duplicate(client):
    await create_signal(client, source_url="https://example.com/a")
    duplicate = await create_signal(client, source_url="https://example.com/b")

    response = await client.post(f"/api/v1/intake/signals/{duplicate['id']}/promote", json={})

    assert response.status_code == 409


async def test_block_promotion_of_rejected(client):
    signal = await create_signal(client)
    await client.patch(
        f"/api/v1/intake/signals/{signal['id']}/reject",
        json={"reason": "Low quality."},
    )

    response = await client.post(f"/api/v1/intake/signals/{signal['id']}/promote", json={})

    assert response.status_code == 409


async def test_block_promotion_of_archived(client):
    signal = await create_signal(client)
    await client.patch(f"/api/v1/intake/signals/{signal['id']}/archive")

    response = await client.post(f"/api/v1/intake/signals/{signal['id']}/promote", json={})

    assert response.status_code == 409


async def test_block_promotion_of_already_promoted_signal(client):
    signal = await create_signal(client)
    await client.post(f"/api/v1/intake/signals/{signal['id']}/promote", json={})

    response = await client.post(f"/api/v1/intake/signals/{signal['id']}/promote", json={})

    assert response.status_code == 409


async def test_promotion_creates_news_item_with_expected_fields(client):
    signal = await create_signal(client)
    promoted = await client.post(f"/api/v1/intake/signals/{signal['id']}/promote", json={})
    news_id = promoted.json()["promoted_news_item_id"]

    response = await client.get(f"/api/v1/news/{news_id}")

    assert response.status_code == 200
    news = response.json()
    assert news["title"] == "Bitcoin ETF sees record inflows"
    assert news["category"] == "markets"
    assert news["priority"] == "P1"
    assert news["source_url"] == "https://example.com/news/btc-etf"
    assert news["status"] == "detected"


async def test_promotion_optionally_creates_workflow_run(client):
    signal = await create_signal(client)
    promoted = await client.post(
        f"/api/v1/intake/signals/{signal['id']}/promote",
        json={"create_workflow": True, "workflow_type": "editorial_pipeline"},
    )
    news_id = promoted.json()["promoted_news_item_id"]

    response = await client.get(f"/api/v1/news/{news_id}/workflow")

    assert response.status_code == 200
    assert response.json()["news_item_id"] == news_id


async def test_correlation_id_persisted_from_header(client):
    response = await client.post(
        "/api/v1/intake/signals",
        json=SIGNAL_PAYLOAD,
        headers={"X-Correlation-ID": "corr-intake-001"},
    )

    assert response.status_code == 201
    assert response.json()["correlation_id"] == "corr-intake-001"


async def test_auth_protects_create_signal(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.post("/api/v1/intake/signals", json=SIGNAL_PAYLOAD)

    assert response.status_code == 401


async def test_auth_protects_signal_mutations(client, monkeypatch):
    signal = await create_signal(client)
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    dedupe = await client.post(f"/api/v1/intake/signals/{signal['id']}/dedupe")
    promote = await client.post(f"/api/v1/intake/signals/{signal['id']}/promote", json={})
    reject = await client.patch(
        f"/api/v1/intake/signals/{signal['id']}/reject",
        json={"reason": "No auth."},
    )
    archive = await client.patch(f"/api/v1/intake/signals/{signal['id']}/archive")

    assert dedupe.status_code == 401
    assert promote.status_code == 401
    assert reject.status_code == 401
    assert archive.status_code == 401


async def test_create_intake_adapter_run_valid(client):
    run = await create_adapter_run(client)

    assert run["adapter_name"] == "manual-intake"
    assert run["adapter_type"] == "manual"
    assert run["status"] == "completed"


async def test_block_intake_adapter_run_with_invalid_adapter_type(client):
    response = await client.post(
        "/api/v1/intake/adapter-runs",
        json={"adapter_name": "bad-adapter", "adapter_type": "external_api"},
    )

    assert response.status_code == 422


async def test_list_adapter_runs(client):
    run = await create_adapter_run(client)

    response = await client.get("/api/v1/intake/adapter-runs")

    assert response.status_code == 200
    assert response.json()[0]["id"] == run["id"]


async def test_filter_adapter_runs(client):
    run = await create_adapter_run(client, adapter_name="manual-priority")

    response = await client.get(
        "/api/v1/intake/adapter-runs",
        params={"adapter_name": "manual-priority", "adapter_type": "manual"},
    )

    assert response.status_code == 200
    assert response.json()[0]["id"] == run["id"]


async def test_get_adapter_run_by_id(client):
    run = await create_adapter_run(client)

    response = await client.get(f"/api/v1/intake/adapter-runs/{run['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == run["id"]
