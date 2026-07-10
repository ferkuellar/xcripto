from __future__ import annotations

from app.core.config import get_settings
from app.db.session import AsyncSessionLocal
from app.models import PublicationRecord
from app.services.publication_dispatch_service import dispatch_publication_record

NEWS_PAYLOAD = {
    "title": "Bitcoin ETF sees record inflows",
    "summary": "Institutional inflows into spot BTC ETFs reached a new daily record.",
    "category": "markets",
    "priority": "P1",
    "source_url": "https://example.com/etf-inflows",
    "source_name": "Example Wire",
}


def _content_piece_payload(news_id: str) -> dict:
    return {
        "news_item_id": news_id,
        "content_type": "news_article",
        "title": "Bitcoin ETF inflows hit new record",
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


def _distribution_plan_payload(news_id: str, content_piece_id: str) -> dict:
    return {
        "content_piece_id": content_piece_id,
        "news_item_id": news_id,
        "primary_channel": "Telegram",
        "secondary_channels": [],
        "distribution_type": "primary_publication",
        "status": "scheduled",
        "owner": "distribution-desk",
        "dependencies": ["editorial approval"],
        "metric_plan": {"primary_metric": "views"},
        "risk_level": "medium",
        "publication_readiness": "ready",
    }


def _publication_record_payload(
    news_id: str,
    content_piece_id: str,
    distribution_plan_id: str,
) -> dict:
    return {
        "content_piece_id": content_piece_id,
        "distribution_plan_id": distribution_plan_id,
        "news_item_id": news_id,
        "channel": "Telegram",
        "publication_status": "scheduled",
        "owner": "publisher",
        "notes": "Scheduled through editorial desk.",
    }


async def _create_telegram_publication_chain(client) -> dict:
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
            json=_publication_record_payload(news["id"], piece["id"], plan["id"]),
        )
    ).json()
    return {"news": news, "piece": piece, "plan": plan, "publication": publication}


async def test_telegram_dispatch_dry_run_returns_preview(client):
    chain = await _create_telegram_publication_chain(client)

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
    assert "Bitcoin ETF inflows hit new record" in result.message
    assert "news/bitcoin-etf-inflows-hit-new-record" in result.message
    assert record.publication_status == "scheduled"
    assert record.external_id is None


async def test_published_telegram_record_gets_dispatched_and_is_idempotent(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "public_site_url", "https://xcripto.test")
    monkeypatch.setattr(settings, "telegram_bot_token", "telegram-token")
    monkeypatch.setattr(settings, "telegram_channel_id", "@xcripto_news")

    calls: list[str] = []

    async def fake_send_telegram_message(text: str) -> dict:
        calls.append(text)
        return {"ok": True, "result": {"message_id": 77}}

    monkeypatch.setattr(
        "app.services.publication_dispatch_service._send_telegram_message",
        fake_send_telegram_message,
    )

    chain = await _create_telegram_publication_chain(client)
    publication_id = chain["publication"]["id"]

    response = await client.patch(
        f"/api/v1/publication-records/{publication_id}/status",
        json={"publication_status": "published"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["publication_status"] == "published"
    assert body["external_id"] == "77"
    assert body["published_url"] == "https://t.me/xcripto_news/77"
    assert len(calls) == 1

    second = await client.patch(
        f"/api/v1/publication-records/{publication_id}/status",
        json={"publication_status": "published"},
    )

    assert second.status_code == 200
    assert second.json()["external_id"] == "77"
    assert len(calls) == 1


async def test_telegram_dispatch_failure_marks_record_failed(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "public_site_url", "https://xcripto.test")
    monkeypatch.setattr(settings, "telegram_bot_token", "telegram-token")
    monkeypatch.setattr(settings, "telegram_channel_id", "@xcripto_news")

    async def failing_send_telegram_message(text: str) -> dict:
        raise OSError("telegram offline")

    monkeypatch.setattr(
        "app.services.publication_dispatch_service._send_telegram_message",
        failing_send_telegram_message,
    )

    chain = await _create_telegram_publication_chain(client)
    publication_id = chain["publication"]["id"]

    response = await client.patch(
        f"/api/v1/publication-records/{publication_id}/status",
        json={"publication_status": "published"},
    )

    assert response.status_code == 409
    assert "Telegram publication failed" in response.json()["error"]

    async with AsyncSessionLocal() as session:
        record = await session.get(PublicationRecord, publication_id)

    assert record.publication_status == "failed"
