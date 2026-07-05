"""Integration tests for the controlled RSS connector rollout (P9), fetch mocked."""

import socket

import pytest
from sqlalchemy import func, select

from app.core.config import Settings, get_settings
from app.db.session import AsyncSessionLocal
from app.models import IntakeSignal, NewsItem, OperationalAuditLog, SourceReference
from app.services import connector_service

FEED = b"""<?xml version="1.0"?>
<rss version="2.0"><channel>
<item><title>CoinDesk item</title><link>https://www.coindesk.com/markets/a1</link>
<description>Reserve report.</description><guid>cd-a1</guid>
<pubDate>Mon, 05 Jul 2026 10:00:00 +0000</pubDate></item>
<item><title>CoinDesk second item</title><link>https://coindesk.com/markets/a2</link>
<description>Second.</description><guid>ct-a2</guid></item>
<item><title>Unknown blog item</title><link>https://randomblog.example/x</link>
<description>Not allowed.</description><guid>rb-x</guid></item>
</channel></rss>"""

SPOOFED_FEED = b"""<?xml version="1.0"?>
<rss version="2.0"><channel>
<item><title>Spoofed trusted link</title><link>https://cointelegraph.com/news/spoof</link>
<description>Should not inherit trust from an arbitrary item link.</description>
<guid>spoof</guid></item>
</channel></rss>"""


def enable(monkeypatch, allowed="coindesk.com,cointelegraph.com", max_items=20):
    s = get_settings()
    monkeypatch.setattr(s, "connectors_enabled", True)
    monkeypatch.setattr(s, "rss_connector_enabled", True)
    monkeypatch.setattr(s, "rss_connector_allowed_domains", allowed)
    monkeypatch.setattr(s, "rss_connector_max_items", max_items)


def feed_fetch(_url):
    return FEED


async def run(**kwargs):
    async with AsyncSessionLocal() as session:
        return await connector_service.run_rss_connector(
            session, "https://www.coindesk.com/feed", fetch=feed_fetch, **kwargs
        )


async def count(model, **where) -> int:
    async with AsyncSessionLocal() as session:
        stmt = select(func.count()).select_from(model)
        for k, v in where.items():
            stmt = stmt.where(getattr(model, k) == v)
        return int((await session.execute(stmt)).scalar_one())


async def test_disabled_connector_does_not_ingest(client):
    # Kill switch off by default -> no signals, no adapter run.
    result = await run()
    assert result.disabled is True
    assert result.reason == "connectors disabled"
    assert await count(IntakeSignal) == 0
    assert await count(OperationalAuditLog, event_type="connector_event") == 0


async def test_allowed_domain_item_is_ingested(client, monkeypatch):
    enable(monkeypatch)
    result = await run()
    assert result.accepted_count == 2  # coindesk + cointelegraph
    assert result.rejected_count == 1  # unknown blog
    assert await count(IntakeSignal, signal_type="rss") == 2


async def test_disallowed_domain_is_rejected(client, monkeypatch):
    enable(monkeypatch, allowed="coindesk.com")  # cointelegraph now disallowed too
    result = await run()
    assert result.accepted_count == 2
    assert result.rejected_count == 1


async def test_max_items_is_respected(client, monkeypatch):
    enable(monkeypatch)
    result = await run(max_items=1)
    assert result.fetched_count == 3
    assert result.accepted_count + result.rejected_count == 1


async def test_zero_max_items_ingests_nothing(client, monkeypatch):
    enable(monkeypatch)
    result = await run(max_items=0)
    assert result.accepted_count == 0
    assert await count(IntakeSignal) == 0


async def test_fetch_error_is_recorded_and_does_not_crash(client, monkeypatch):
    enable(monkeypatch)

    def boom(_url):
        raise TimeoutError("feed timed out")

    async with AsyncSessionLocal() as session:
        result = await connector_service.run_rss_connector(
            session, "https://coindesk.com/feed", fetch=boom
        )
    assert result.errors
    assert await count(OperationalAuditLog, event_type="connector_event", outcome="failed") >= 1


async def test_duplicate_item_is_flagged_on_second_run(client, monkeypatch):
    enable(monkeypatch)
    await run()
    second = await run()
    assert second.duplicate_count >= 1
    assert await count(OperationalAuditLog, action="connector.item.duplicate") >= 1


async def test_ingested_item_creates_audit_event(client, monkeypatch):
    enable(monkeypatch)
    await run()
    assert await count(OperationalAuditLog, action="connector.item.ingested") == 2
    assert await count(OperationalAuditLog, action="connector.run.started") == 1
    assert await count(OperationalAuditLog, action="connector.run.completed") == 1


async def test_ingested_item_registers_source_reference_with_registry_trust(client, monkeypatch):
    enable(monkeypatch)
    await run()
    async with AsyncSessionLocal() as session:
        rows = (await session.execute(select(SourceReference))).scalars().all()
    by_name = {r.source_name: r for r in rows}
    assert set(by_name) == {"CoinDesk"}
    assert by_name["CoinDesk"].trust_level == "T1"  # S2
    assert by_name["CoinDesk"].source_url == "https://coindesk.com"


async def test_no_secret_leaks_in_audit_and_no_auto_promote(client, monkeypatch):
    enable(monkeypatch)
    await run()
    async with AsyncSessionLocal() as session:
        events = (
            await session.execute(
                select(OperationalAuditLog).where(
                    OperationalAuditLog.event_type == "connector_event"
                )
            )
        ).scalars().all()
    for ev in events:
        blob = f"{ev.event_metadata} {ev.reason} {ev.before_state} {ev.after_state}"
        assert "dev-secret" not in blob
        assert "X-API-Key" not in blob
    # P9 must never auto-promote/publish.
    assert get_settings().connector_auto_promote is False
    assert await count(NewsItem) == 0


def test_connector_auto_promote_true_is_invalid():
    with pytest.raises(ValueError, match="CONNECTOR_AUTO_PROMOTE"):
        Settings(connector_auto_promote=True)


async def test_feed_url_must_match_allowed_provider(client, monkeypatch):
    enable(monkeypatch)
    async with AsyncSessionLocal() as session:
        result = await connector_service.run_rss_connector(
            session,
            "https://evil.example/feed",
            fetch=feed_fetch,
        )
    assert result.errors == ["feed_url does not match an allowed feed provider"]
    assert await count(IntakeSignal) == 0


async def test_private_dns_resolution_is_blocked_before_fetch(client, monkeypatch):
    enable(monkeypatch)

    def fake_getaddrinfo(host, port, type=0):  # noqa: A002
        assert host == "www.coindesk.com"
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", port))]

    monkeypatch.setattr("app.connectors.base.socket.getaddrinfo", fake_getaddrinfo)
    async with AsyncSessionLocal() as session:
        result = await connector_service.run_rss_connector(session, "https://www.coindesk.com/feed")
    assert result.errors
    assert "blocked address" in result.errors[0]
    assert await count(IntakeSignal) == 0


async def test_redirect_final_url_is_validated(client, monkeypatch):
    enable(monkeypatch)

    def fake_getaddrinfo(_host, port, type=0):  # noqa: A002
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", port))]

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def geturl(self):
            return "http://127.0.0.1/latest"

        def read(self, _limit):
            return FEED

    class FakeOpener:
        def open(self, _request, timeout):
            assert timeout == get_settings().rss_connector_timeout_seconds
            return FakeResponse()

    monkeypatch.setattr("app.connectors.base.socket.getaddrinfo", fake_getaddrinfo)
    monkeypatch.setattr(
        "app.connectors.base.urllib.request.build_opener",
        lambda *_handlers: FakeOpener(),
    )

    async with AsyncSessionLocal() as session:
        result = await connector_service.run_rss_connector(session, "https://coindesk.com/feed")
    assert result.errors
    assert "allowed connector registry" in result.errors[0]
    assert await count(IntakeSignal) == 0


async def test_item_link_cannot_spoof_another_provider_trust(client, monkeypatch):
    enable(monkeypatch, allowed="coindesk.com,cointelegraph.com")
    async with AsyncSessionLocal() as session:
        result = await connector_service.run_rss_connector(
            session,
            "https://coindesk.com/feed",
            fetch=lambda _url: SPOOFED_FEED,
        )
    assert result.accepted_count == 0
    assert result.rejected_count == 1
    assert await count(IntakeSignal) == 0
    assert await count(SourceReference) == 0


async def test_source_reference_dedupes_by_canonical_url_not_name(client):
    async with AsyncSessionLocal() as session:
        await connector_service._ensure_source_reference(
            session,
            source_url="https://www.coindesk.com/",
            source_name="CoinDesk",
            trust_level="T1",
            correlation_id=None,
        )
        await connector_service._ensure_source_reference(
            session,
            source_url="https://coindesk.com",
            source_name="CoinDesk",
            trust_level="T1",
            correlation_id=None,
        )
        await connector_service._ensure_source_reference(
            session,
            source_url="https://coindesk.com/feed",
            source_name="CoinDesk",
            trust_level="T1",
            correlation_id=None,
        )
        rows = (await session.execute(select(SourceReference))).scalars().all()
    assert len(rows) == 2
    assert sorted(row.source_url for row in rows) == [
        "https://coindesk.com",
        "https://coindesk.com/feed",
    ]
