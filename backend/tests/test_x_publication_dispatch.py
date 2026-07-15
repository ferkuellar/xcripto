from __future__ import annotations

import json

from app.core.config import get_settings
from app.db.session import AsyncSessionLocal
from app.integrations.x_client import XPublishError, XPublishResult, build_x_post, publish_x_post
from app.models import PublicationRecord
from app.services.publication_dispatch_service import dispatch_publication_record

NEWS_PAYLOAD = {
    "title": "X validation - Bitcoin ETF sees record inflows",
    "summary": "Institutional inflows into spot BTC ETFs reached a new daily record.",
    "category": "markets",
    "priority": "P1",
    "source_url": "https://example.com/etf-inflows",
    "source_name": "Example Wire",
}


def _content_piece_payload(news_id: str, **overrides) -> dict:
    payload = {
        "news_item_id": news_id,
        "content_type": "news_article",
        "title": "X validation - Bitcoin ETF inflows hit new record",
        "summary": "A concise editorial summary of the inflow signal.",
        "body": "Institutional inflows into spot BTC ETFs reached a new daily record.",
        "status": "approved",
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


def _distribution_plan_payload(news_id: str, content_piece_id: str, **overrides) -> dict:
    payload = {
        "content_piece_id": content_piece_id,
        "news_item_id": news_id,
        "primary_channel": "X",
        "secondary_channels": [],
        "distribution_type": "primary_publication",
        "status": "scheduled",
        "owner": "distribution-desk",
        "dependencies": ["editorial approval"],
        "metric_plan": {"primary_metric": "views"},
        "risk_level": "medium",
        "publication_readiness": "ready",
    }
    return {**payload, **overrides}


def _publication_record_payload(
    news_id: str,
    content_piece_id: str,
    distribution_plan_id: str,
    **overrides,
) -> dict:
    payload = {
        "content_piece_id": content_piece_id,
        "distribution_plan_id": distribution_plan_id,
        "news_item_id": news_id,
        "channel": "X",
        "publication_status": "scheduled",
        "owner": "publisher",
        "notes": "Scheduled through editorial desk.",
    }
    return {**payload, **overrides}


async def _create_x_publication_chain(client, **overrides) -> dict:
    news = (await client.post("/api/v1/news/intake", json=NEWS_PAYLOAD)).json()
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
            json=_publication_record_payload(news["id"], piece["id"], plan["id"], **overrides),
        )
    ).json()
    return {"news": news, "piece": piece, "plan": plan, "publication": publication}


def test_build_x_post_truncates_summary_and_preserves_canonical_url():
    canonical_url = "https://xcripto.test/news/bitcoin-etf-inflows-hit-new-record"
    text = build_x_post(
        title="Bitcoin ETF inflows hit new record",
        summary=" ".join(["Detailed market context"] * 40),
        canonical_url=canonical_url,
    )

    assert len(text) <= 280
    assert text.endswith(canonical_url)
    assert "Bitcoin ETF inflows hit new record" in text
    assert "Detailed market context" in text
    assert text.count(canonical_url) == 1


def test_publish_x_post_uses_oauth1_and_parses_response(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "x_api_key", "consumer-key")
    monkeypatch.setattr(settings, "x_api_secret", "consumer-secret")
    monkeypatch.setattr(settings, "x_access_token", "access-token")
    monkeypatch.setattr(settings, "x_access_token_secret", "access-token-secret")

    captured: dict[str, object] = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return json.dumps({"data": {"id": "987654321"}}).encode("utf-8")

    def fake_urlopen(request, timeout):  # noqa: ANN001
        captured["url"] = request.full_url
        captured["headers"] = dict(request.header_items())
        captured["body"] = request.data.decode("utf-8") if request.data else ""
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr("app.integrations.x_client.urllib.request.urlopen", fake_urlopen)

    result = publish_x_post("X test post")

    assert result.post_id == "987654321"
    assert result.post_url == "https://x.com/i/web/status/987654321"
    assert captured["url"] == "https://api.x.com/2/tweets"
    assert captured["body"] == json.dumps({"text": "X test post"})
    assert "OAuth" in captured["headers"]["Authorization"]
    assert "oauth_consumer_key=\"consumer-key\"" in captured["headers"]["Authorization"]
    assert "oauth_signature=" in captured["headers"]["Authorization"]


async def test_x_dispatch_dry_run_returns_preview(client):
    chain = await _create_x_publication_chain(client)

    async with AsyncSessionLocal() as session:
        result = await dispatch_publication_record(
            session,
            chain["publication"]["id"],
            dry_run=True,
        )
        record = await session.get(PublicationRecord, chain["publication"]["id"])

    assert result.dry_run is True
    assert result.dispatched is False
    assert result.message
    assert result.message.endswith(
        "http://localhost:3000/news/x-validation-bitcoin-etf-inflows-hit-new-record"
    )
    assert record.publication_status == "scheduled"
    assert record.external_id is None
    assert record.published_url is None


async def test_x_publication_success_and_idempotency(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "public_web_base_url", "https://xcripto.test")
    monkeypatch.setattr(settings, "x_api_key", "consumer-key")
    monkeypatch.setattr(settings, "x_api_secret", "consumer-secret")
    monkeypatch.setattr(settings, "x_access_token", "access-token")
    monkeypatch.setattr(settings, "x_access_token_secret", "access-token-secret")

    calls: list[str] = []

    def fake_publish_x_post(text: str) -> XPublishResult:
        calls.append(text)
        return XPublishResult(
            post_id="987654321",
            post_url="https://x.com/i/web/status/987654321",
            raw_response={"data": {"id": "987654321"}},
        )

    monkeypatch.setattr(
        "app.services.publication_dispatch_service.publish_x_post",
        fake_publish_x_post,
    )

    chain = await _create_x_publication_chain(client)
    publication_id = chain["publication"]["id"]

    response = await client.patch(
        f"/api/v1/publication-records/{publication_id}/status",
        json={"publication_status": "published"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["publication_status"] == "published"
    assert body["external_id"] == "987654321"
    assert body["published_url"] == "https://x.com/i/web/status/987654321"
    assert len(calls) == 1

    second = await client.patch(
        f"/api/v1/publication-records/{publication_id}/status",
        json={"publication_status": "published"},
    )

    assert second.status_code == 200
    assert second.json()["external_id"] == "987654321"
    assert len(calls) == 1


async def test_x_missing_credentials_marks_failed_and_can_retry(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "x_api_key", None)
    monkeypatch.setattr(settings, "x_api_secret", None)
    monkeypatch.setattr(settings, "x_access_token", None)
    monkeypatch.setattr(settings, "x_access_token_secret", None)
    chain = await _create_x_publication_chain(client)
    publication_id = chain["publication"]["id"]

    response = await client.patch(
        f"/api/v1/publication-records/{publication_id}/status",
        json={"publication_status": "published"},
    )

    assert response.status_code == 409
    assert "X publication failed" in response.json()["error"]

    async with AsyncSessionLocal() as session:
        record = await session.get(PublicationRecord, publication_id)

    assert record.publication_status == "failed"
    assert record.external_id is None
    assert record.published_url is None
    assert "x publish failed: X credentials are required" in (record.notes or "")

    monkeypatch.setattr(settings, "x_api_key", "consumer-key")
    monkeypatch.setattr(settings, "x_api_secret", "consumer-secret")
    monkeypatch.setattr(settings, "x_access_token", "access-token")
    monkeypatch.setattr(settings, "x_access_token_secret", "access-token-secret")

    def fake_publish_x_post(text: str) -> XPublishResult:
        return XPublishResult(
            post_id="222333444",
            post_url="https://x.com/i/web/status/222333444",
            raw_response={"data": {"id": "222333444"}},
        )

    monkeypatch.setattr(
        "app.services.publication_dispatch_service.publish_x_post",
        fake_publish_x_post,
    )

    retry = await client.patch(
        f"/api/v1/publication-records/{publication_id}/status",
        json={"publication_status": "published"},
    )

    assert retry.status_code == 200
    assert retry.json()["external_id"] == "222333444"
    assert retry.json()["published_url"] == "https://x.com/i/web/status/222333444"


async def test_x_rate_limit_and_rejected_content_mark_failed(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "x_api_key", "consumer-key")
    monkeypatch.setattr(settings, "x_api_secret", "consumer-secret")
    monkeypatch.setattr(settings, "x_access_token", "access-token")
    monkeypatch.setattr(settings, "x_access_token_secret", "access-token-secret")

    async def create_and_publish(error: XPublishError):
        chain = await _create_x_publication_chain(client)

        def raise_error(_: str) -> None:
            raise error

        monkeypatch.setattr(
            "app.services.publication_dispatch_service.publish_x_post",
            raise_error,
        )
        response = await client.patch(
            f"/api/v1/publication-records/{chain['publication']['id']}/status",
            json={"publication_status": "published"},
        )
        return chain, response

    chain_rate, response_rate = await create_and_publish(
        XPublishError("X rate limit exceeded", retryable=True, status_code=429)
    )
    assert response_rate.status_code == 409
    assert "X publication failed" in response_rate.json()["error"]

    async with AsyncSessionLocal() as session:
        record = await session.get(PublicationRecord, chain_rate["publication"]["id"])
    assert record.publication_status == "failed"
    assert record.external_id is None
    assert "rate limit" in (record.notes or "").lower()

    chain_rejected, response_rejected = await create_and_publish(
        XPublishError("X rejected content", retryable=False, status_code=422)
    )
    assert response_rejected.status_code == 409
    async with AsyncSessionLocal() as session:
        record = await session.get(PublicationRecord, chain_rejected["publication"]["id"])
    assert record.publication_status == "failed"
    assert "rejected" in (record.notes or "").lower()


async def test_x_and_telegram_same_news_item_are_independent(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "public_web_base_url", "https://xcripto.test")
    monkeypatch.setattr(settings, "telegram_bot_token", "telegram-token")
    monkeypatch.setattr(settings, "telegram_channel_id", "@xcripto_news")
    monkeypatch.setattr(settings, "x_api_key", "consumer-key")
    monkeypatch.setattr(settings, "x_api_secret", "consumer-secret")
    monkeypatch.setattr(settings, "x_access_token", "access-token")
    monkeypatch.setattr(settings, "x_access_token_secret", "access-token-secret")

    telegram_calls: list[str] = []
    x_calls: list[str] = []

    async def fake_send_telegram_message(text: str) -> dict:
        telegram_calls.append(text)
        return {"ok": True, "result": {"message_id": 11}}

    def fake_publish_x_post(text: str) -> XPublishResult:
        x_calls.append(text)
        return XPublishResult(
            post_id="22",
            post_url="https://x.com/i/web/status/22",
            raw_response={"data": {"id": "22"}},
        )

    monkeypatch.setattr(
        "app.services.publication_dispatch_service._send_telegram_message",
        fake_send_telegram_message,
    )
    monkeypatch.setattr(
        "app.services.publication_dispatch_service.publish_x_post",
        fake_publish_x_post,
    )

    news = (await client.post("/api/v1/news/intake", json=NEWS_PAYLOAD)).json()
    piece = (
        await client.post("/api/v1/content-pieces", json=_content_piece_payload(news["id"]))
    ).json()
    telegram_plan = (
        await client.post(
            "/api/v1/distribution-plans",
            json=_distribution_plan_payload(news["id"], piece["id"], primary_channel="Telegram"),
        )
    ).json()
    x_plan = (
        await client.post(
            "/api/v1/distribution-plans",
            json=_distribution_plan_payload(news["id"], piece["id"], primary_channel="X"),
        )
    ).json()
    telegram_publication = (
        await client.post(
            "/api/v1/publication-records",
            json=_publication_record_payload(
                news["id"], piece["id"], telegram_plan["id"], channel="Telegram"
            ),
        )
    ).json()
    x_publication = (
        await client.post(
            "/api/v1/publication-records",
            json=_publication_record_payload(news["id"], piece["id"], x_plan["id"], channel="X"),
        )
    ).json()

    telegram_response = await client.patch(
        f"/api/v1/publication-records/{telegram_publication['id']}/status",
        json={"publication_status": "published"},
    )
    x_response = await client.patch(
        f"/api/v1/publication-records/{x_publication['id']}/status",
        json={"publication_status": "published"},
    )

    assert telegram_response.status_code == 200
    assert x_response.status_code == 200
    assert telegram_response.json()["external_id"] == "11"
    assert x_response.json()["external_id"] == "22"
    assert len(telegram_calls) == 1
    assert len(x_calls) == 1
