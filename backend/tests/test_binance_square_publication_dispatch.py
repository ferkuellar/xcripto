from __future__ import annotations

import io
import json
import urllib.error

from app.core.config import get_settings
from app.db.session import AsyncSessionLocal
from app.integrations.binance_square_client import (
    BinanceSquareClient,
    BinanceSquarePublishError,
    BinanceSquarePublishResult,
    build_binance_square_post,
)
from app.models import PublicationRecord
from app.services.publication_dispatch_service import dispatch_publication_record

NEWS_PAYLOAD = {
    "title": "Binance Square validation - Bitcoin ETF sees record inflows",
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
        "title": "Binance Square validation - Bitcoin ETF inflows hit new record",
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
        "primary_channel": "BINANCE_SQUARE",
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
        "channel": "BINANCE_SQUARE",
        "publication_status": "scheduled",
        "owner": "publisher",
        "notes": "Scheduled through editorial desk.",
    }
    return {**payload, **overrides}


async def _create_binance_publication_chain(client, **overrides) -> dict:
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


def test_build_binance_square_post_preserves_url_and_trims_summary():
    canonical_url = "https://xcripto.test/news/bitcoin-etf-inflows-hit-new-record"
    text = build_binance_square_post(
        title="Bitcoin ETF inflows hit new record",
        summary=" ".join(["Detailed market context"] * 40),
        canonical_url=canonical_url,
        max_length=180,
    )

    assert len(text) <= 180
    assert text.endswith(canonical_url)
    assert "Bitcoin ETF inflows hit new record" in text
    assert "Detailed market context" in text
    assert text.count(canonical_url) == 1


def test_binance_square_client_uses_official_contract(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "binance_square_openapi_key", "square-key")

    captured: dict[str, object] = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return json.dumps(
                {"code": "000000", "data": {"id": "987", "shareLink": "https://sq.example/987"}}
            ).encode("utf-8")

    def fake_urlopen(request, timeout):  # noqa: ANN001
        captured["url"] = request.full_url
        captured["headers"] = {k.lower(): v for k, v in request.header_items()}
        captured["body"] = json.loads(request.data.decode("utf-8")) if request.data else {}
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(
        "app.integrations.binance_square_client.urllib.request.urlopen",
        fake_urlopen,
    )

    client = BinanceSquareClient(settings=settings)
    result = client.publish_short_post("Binance Square test post")

    assert result.external_id == "987"
    assert result.published_url == "https://sq.example/987"
    assert captured["url"] == (
        "https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add"
    )
    assert captured["body"] == {
        "contentType": 1,
        "bodyTextOnly": "Binance Square test post",
    }
    assert captured["timeout"] == settings.request_timeout_seconds
    assert captured["headers"]["x-square-openapi-key"] == "square-key"
    assert captured["headers"]["content-type"] == "application/json"
    assert captured["headers"]["clienttype"] == "binanceSkill"
    assert "square-key" not in json.dumps(result.raw_response)


def test_binance_square_client_sanitizes_provider_and_transport_errors(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "binance_square_openapi_key", "square-key")

    def fake_http_error(status_code: int, body: str):
        return urllib.error.HTTPError(
            url="https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add",
            code=status_code,
            msg="error",
            hdrs=None,
            fp=io.BytesIO(body.encode("utf-8")),
        )

    for status_code, body, expected_error_type, retryable in [
        (401, '{"message": "invalid api key square-key"}', "authentication_rejected", False),
        (400, '{"message": "invalid payload"}', "invalid_payload", False),
        (500, '{"message": "upstream error"}', "upstream_failure", True),
        (504, "", "ambiguous_timeout", False),
    ]:
        client = BinanceSquareClient(settings=settings)
        current_status_code = status_code
        current_body = body

        def fake_urlopen(  # noqa: ANN001
            *args,
            status_code=current_status_code,
            body_text=current_body,
            **kwargs,
        ):
            raise fake_http_error(status_code, body_text)

        monkeypatch.setattr(
            "app.integrations.binance_square_client.urllib.request.urlopen",
            fake_urlopen,
        )

        try:
            client.publish_short_post("Binance Square test post")
        except BinanceSquarePublishError as exc:
            assert exc.error_type == expected_error_type
            assert exc.retryable is retryable
            assert "square-key" not in str(exc)
            if status_code == 504:
                assert exc.ambiguous_outcome is True
        else:  # pragma: no cover - defensive
            raise AssertionError("Expected BinanceSquarePublishError")


def test_binance_square_client_handles_malformed_json_and_timeout(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "binance_square_openapi_key", "square-key")

    class FakeMalformedResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return b"not-json"

    def fake_urlopen_malformed(request, timeout):  # noqa: ANN001
        return FakeMalformedResponse()

    monkeypatch.setattr(
        "app.integrations.binance_square_client.urllib.request.urlopen",
        fake_urlopen_malformed,
    )
    client = BinanceSquareClient(settings=settings)

    try:
        client.publish_short_post("Binance Square test post")
    except BinanceSquarePublishError as exc:
        assert exc.error_type == "invalid_json"
        assert exc.retryable is True
    else:  # pragma: no cover - defensive
        raise AssertionError("Expected BinanceSquarePublishError")

    def fake_urlopen_timeout(request, timeout):  # noqa: ANN001
        raise TimeoutError("socket timeout")

    monkeypatch.setattr(
        "app.integrations.binance_square_client.urllib.request.urlopen",
        fake_urlopen_timeout,
    )

    try:
        client.publish_short_post("Binance Square test post")
    except BinanceSquarePublishError as exc:
        assert exc.error_type == "network_error"
        assert exc.retryable is True
    else:  # pragma: no cover - defensive
        raise AssertionError("Expected BinanceSquarePublishError")


async def test_binance_square_channel_recognition_and_dry_run(client):
    chain = await _create_binance_publication_chain(client)

    async with AsyncSessionLocal() as session:
        result = await dispatch_publication_record(
            session,
            chain["publication"]["id"],
            dry_run=True,
        )
        record = await session.get(PublicationRecord, chain["publication"]["id"])

    assert chain["publication"]["channel"] == "BINANCE_SQUARE"
    assert result.dry_run is True
    assert result.dispatched is False
    assert result.message
    assert result.message.endswith("https://localhost/news/binance-square-validation-bitcoin-etf-inflows-hit-new-record")
    assert record.publication_status == "scheduled"
    assert record.external_id is None
    assert record.published_url is None


async def test_binance_square_publication_success_and_idempotency(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "public_site_url", "https://xcripto.test")
    monkeypatch.setattr(settings, "binance_square_openapi_key", "square-key")

    calls: list[str] = []

    def fake_publish_binance_square_post(text: str) -> BinanceSquarePublishResult:
        calls.append(text)
        return BinanceSquarePublishResult(
            external_id="binance-987",
            published_url="https://sq.example/p/binance-987",
            provider_code="000000",
            raw_response={
                "code": "000000",
                "data": {"id": "binance-987", "shareLink": "https://sq.example/p/binance-987"},
            },
        )

    monkeypatch.setattr(
        "app.services.publication_dispatch_service.publish_binance_square_post",
        fake_publish_binance_square_post,
    )

    chain = await _create_binance_publication_chain(client)
    publication_id = chain["publication"]["id"]

    response = await client.patch(
        f"/api/v1/publication-records/{publication_id}/status",
        json={"publication_status": "published"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["publication_status"] == "published"
    assert body["external_id"] == "binance-987"
    assert body["published_url"] == "https://sq.example/p/binance-987"
    assert body["published_at"] is not None
    assert len(calls) == 1

    async with AsyncSessionLocal() as session:
        record = await session.get(PublicationRecord, publication_id)

    assert record.publication_status == "published"
    assert record.external_id == "binance-987"
    assert record.published_url == "https://sq.example/p/binance-987"
    assert record.published_at is not None

    second = await client.patch(
        f"/api/v1/publication-records/{publication_id}/status",
        json={"publication_status": "published"},
    )

    assert second.status_code == 200
    assert second.json()["external_id"] == "binance-987"
    assert len(calls) == 1


async def test_binance_square_missing_api_key_marks_failed_and_can_retry(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "binance_square_openapi_key", None)
    chain = await _create_binance_publication_chain(client)
    publication_id = chain["publication"]["id"]

    response = await client.patch(
        f"/api/v1/publication-records/{publication_id}/status",
        json={"publication_status": "published"},
    )

    assert response.status_code == 409
    assert "Binance Square publication failed" in response.json()["error"]

    async with AsyncSessionLocal() as session:
        record = await session.get(PublicationRecord, publication_id)

    assert record.publication_status == "failed"
    assert record.external_id is None
    assert record.published_url is None
    assert "binance square publish failed: BINANCE_SQUARE_OPENAPI_KEY is required" in (
        record.notes or ""
    )

    monkeypatch.setattr(settings, "binance_square_openapi_key", "square-key")

    def fake_publish_binance_square_post(text: str) -> BinanceSquarePublishResult:
        return BinanceSquarePublishResult(
            external_id="binance-222",
            published_url="https://sq.example/p/binance-222",
            provider_code="000000",
            raw_response={
                "code": "000000",
                "data": {"id": "binance-222", "shareLink": "https://sq.example/p/binance-222"},
            },
        )

    monkeypatch.setattr(
        "app.services.publication_dispatch_service.publish_binance_square_post",
        fake_publish_binance_square_post,
    )

    retry = await client.patch(
        f"/api/v1/publication-records/{publication_id}/status",
        json={"publication_status": "published"},
    )

    assert retry.status_code == 200
    assert retry.json()["external_id"] == "binance-222"
    assert retry.json()["published_url"] == "https://sq.example/p/binance-222"


async def test_binance_square_provider_errors_and_504_are_sanitized(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "binance_square_openapi_key", "square-key")

    async def create_and_publish(error: BinanceSquarePublishError):
        chain = await _create_binance_publication_chain(client)

        def raise_error(_: str) -> None:
            raise error

        monkeypatch.setattr(
            "app.services.publication_dispatch_service.publish_binance_square_post",
            raise_error,
        )
        response = await client.patch(
            f"/api/v1/publication-records/{chain['publication']['id']}/status",
            json={"publication_status": "published"},
        )
        return chain, response

    chain_rate, response_rate = await create_and_publish(
        BinanceSquarePublishError(
            "Binance Square daily publication limit reached",
            retryable=True,
            status_code=429,
            error_type="rate_limited",
        )
    )
    assert response_rate.status_code == 409
    assert "Binance Square publication failed" in response_rate.json()["error"]

    async with AsyncSessionLocal() as session:
        record = await session.get(PublicationRecord, chain_rate["publication"]["id"])
    assert record.publication_status == "failed"
    assert record.external_id is None
    assert record.published_url is None
    assert "daily publication limit reached" in (record.notes or "").lower()

    chain_504, response_504 = await create_and_publish(
        BinanceSquarePublishError(
            "Binance Square provider timeout",
            retryable=False,
            status_code=504,
            error_type="ambiguous_timeout",
            ambiguous_outcome=True,
        )
    )
    assert response_504.status_code == 409

    async with AsyncSessionLocal() as session:
        record = await session.get(PublicationRecord, chain_504["publication"]["id"])
    assert record.publication_status == "failed"
    assert "ambiguous outcome" in (record.notes or "").lower()


async def test_binance_square_and_telegram_same_news_item_are_independent(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "public_site_url", "https://xcripto.test")
    monkeypatch.setattr(settings, "telegram_bot_token", "telegram-token")
    monkeypatch.setattr(settings, "telegram_channel_id", "@xcripto_news")
    monkeypatch.setattr(settings, "binance_square_openapi_key", "square-key")

    telegram_calls: list[str] = []
    binance_calls: list[str] = []

    async def fake_send_telegram_message(text: str) -> dict:
        telegram_calls.append(text)
        return {"ok": True, "result": {"message_id": 11}}

    def fake_publish_binance_square_post(text: str) -> BinanceSquarePublishResult:
        binance_calls.append(text)
        return BinanceSquarePublishResult(
            external_id="binance-22",
            published_url="https://sq.example/p/binance-22",
            provider_code="000000",
            raw_response={
                "code": "000000",
                "data": {"id": "binance-22", "shareLink": "https://sq.example/p/binance-22"},
            },
        )

    monkeypatch.setattr(
        "app.services.publication_dispatch_service._send_telegram_message",
        fake_send_telegram_message,
    )
    monkeypatch.setattr(
        "app.services.publication_dispatch_service.publish_binance_square_post",
        fake_publish_binance_square_post,
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
    binance_plan = (
        await client.post(
            "/api/v1/distribution-plans",
            json=_distribution_plan_payload(
                news["id"],
                piece["id"],
                primary_channel="BINANCE_SQUARE",
            ),
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
    binance_publication = (
        await client.post(
            "/api/v1/publication-records",
            json=_publication_record_payload(
                news["id"],
                piece["id"],
                binance_plan["id"],
                channel="BINANCE_SQUARE",
            ),
        )
    ).json()

    telegram_response = await client.patch(
        f"/api/v1/publication-records/{telegram_publication['id']}/status",
        json={"publication_status": "published"},
    )
    binance_response = await client.patch(
        f"/api/v1/publication-records/{binance_publication['id']}/status",
        json={"publication_status": "published"},
    )

    assert telegram_response.status_code == 200
    assert binance_response.status_code == 200
    assert telegram_response.json()["external_id"] == "11"
    assert binance_response.json()["external_id"] == "binance-22"
    assert len(telegram_calls) == 1
    assert len(binance_calls) == 1
