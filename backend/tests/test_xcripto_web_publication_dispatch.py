from __future__ import annotations

import pytest

from app.core.config import get_settings
from app.core.errors import ConflictError
from app.db.session import AsyncSessionLocal
from app.models import ContentPiece, PublicationRecord
from app.services.publication_dispatch_service import dispatch_publication_record

NEWS_PAYLOAD = {
    "title": "Bitcoin ETF sees record inflows",
    "summary": "Institutional inflows into spot BTC ETFs reached a new daily record.",
    "category": "markets",
    "priority": "P1",
    "source_url": "https://example.com/etf-inflows",
    "source_name": "Example Wire",
}

SECOND_NEWS_PAYLOAD = {
    "title": "Bitcoin ETF sees record inflows",
    "summary": "A follow-up market note with the same editorial title.",
    "category": "markets",
    "priority": "P1",
    "source_url": "https://example.com/etf-inflows-2",
    "source_name": "Example Wire 2",
}


def _content_piece_payload(news_id: str, **overrides: object) -> dict:
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
    payload.update(overrides)
    return payload


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


async def _create_web_publication_chain(client, news_payload: dict) -> dict:
    news = (await client.post("/api/v1/news/intake", json=news_payload)).json()
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


async def test_xcripto_web_dry_run_returns_canonical_url(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "public_web_base_url", "https://xcripto.test")

    chain = await _create_web_publication_chain(client, NEWS_PAYLOAD)

    async with AsyncSessionLocal() as session:
        result = await dispatch_publication_record(
            session,
            chain["publication"]["id"],
            dry_run=True,
        )
        record = await session.get(PublicationRecord, chain["publication"]["id"])

    assert result.dry_run is True
    assert result.dispatched is False
    assert result.reason == "dry_run"
    assert result.message == "https://xcripto.test/news/bitcoin-etf-sees-record-inflows"
    assert record.publication_status == "scheduled"
    assert record.canonical_slug is None
    assert record.published_url is None


async def test_xcripto_web_dispatch_publishes_and_is_idempotent(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "public_web_base_url", "https://xcripto.test")

    chain = await _create_web_publication_chain(client, NEWS_PAYLOAD)
    publication_id = chain["publication"]["id"]

    async with AsyncSessionLocal() as session:
        record = await session.get(PublicationRecord, publication_id)
        record.publication_status = "published"
        await session.commit()
        result = await dispatch_publication_record(session, publication_id)
        await session.refresh(record)

        assert result.dispatched is True
        assert result.idempotent is False
        assert result.external_id == chain["news"]["id"]
        assert result.published_url == "https://xcripto.test/news/bitcoin-etf-sees-record-inflows"
        assert record.publication_status == "published"
        assert record.external_id == chain["news"]["id"]
        assert record.published_url == "https://xcripto.test/news/bitcoin-etf-sees-record-inflows"
        assert record.canonical_slug == "bitcoin-etf-sees-record-inflows"
        assert record.published_at is not None

        second = await dispatch_publication_record(session, publication_id)

    assert second.idempotent is True
    assert second.external_id == chain["news"]["id"]
    assert second.published_url == "https://xcripto.test/news/bitcoin-etf-sees-record-inflows"


async def test_xcripto_web_slug_collision_uses_deterministic_suffix(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "public_web_base_url", "https://xcripto.test")

    first_chain = await _create_web_publication_chain(client, NEWS_PAYLOAD)
    second_chain = await _create_web_publication_chain(client, SECOND_NEWS_PAYLOAD)

    async with AsyncSessionLocal() as session:
        first = await session.get(PublicationRecord, first_chain["publication"]["id"])
        first.publication_status = "published"
        await session.commit()
        await dispatch_publication_record(session, first.id)

        second = await session.get(PublicationRecord, second_chain["publication"]["id"])
        second.publication_status = "published"
        await session.commit()
        result = await dispatch_publication_record(session, second.id)
        await session.refresh(second)

    assert result.dispatched is True
    assert second.canonical_slug
    assert second.canonical_slug != first.canonical_slug
    assert second.canonical_slug.startswith("bitcoin-etf-sees-record-inflows-")
    assert result.published_url == f"https://xcripto.test/news/{second.canonical_slug}"


async def test_xcripto_web_failure_marks_record_failed_and_retry_succeeds(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "public_web_base_url", "https://xcripto.test")

    chain = await _create_web_publication_chain(client, NEWS_PAYLOAD)

    async with AsyncSessionLocal() as session:
        record = await session.get(PublicationRecord, chain["publication"]["id"])
        piece = await session.get(ContentPiece, chain["piece"]["id"])
        record.publication_status = "published"
        piece.body = ""
        await session.commit()

        with pytest.raises(ConflictError):
            await dispatch_publication_record(session, record.id)

        await session.refresh(record)
        assert record.publication_status == "failed"
        assert record.external_id is None
        assert record.published_url is None
        assert "body unavailable" in (record.notes or "")

        piece.body = "Institutional inflows reached a record."
        record.publication_status = "published"
        await session.commit()

        retry = await dispatch_publication_record(session, record.id)
        await session.refresh(record)

    assert retry.dispatched is True
    assert retry.idempotent is False
    assert record.publication_status == "published"
    assert record.published_url == "https://xcripto.test/news/bitcoin-etf-sees-record-inflows"
