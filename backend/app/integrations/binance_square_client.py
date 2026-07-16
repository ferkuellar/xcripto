from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Final

from app.core.config import Settings, get_settings
from app.core.errors import DomainValidationError

BINANCE_SQUARE_BASE_URL_V1: Final = (
    "https://www.binance.com/bapi/composite/v1/public/pgc/openApi"
)
BINANCE_SQUARE_ENDPOINT: Final = "/content/add"
BINANCE_SQUARE_CLIENT_TYPE: Final = "binanceSkill"


@dataclass(slots=True)
class BinanceSquarePublishResult:
    external_id: str | None
    published_url: str | None
    provider_code: str | None
    raw_response: dict


class BinanceSquarePublishError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        retryable: bool,
        status_code: int | None = None,
        error_type: str | None = None,
        ambiguous_outcome: bool = False,
    ) -> None:
        super().__init__(message)
        self.retryable = retryable
        self.status_code = status_code
        self.error_type = error_type
        self.ambiguous_outcome = ambiguous_outcome


def build_binance_square_post(
    title: str,
    summary: str | None,
    canonical_url: str,
    *,
    max_length: int | None = None,
) -> str:
    cleaned_title = _normalize_text(title)
    cleaned_summary = _normalize_text(summary or "")
    cleaned_url = canonical_url.strip()
    if not cleaned_url:
        raise DomainValidationError("canonical_url is required for Binance Square publication")
    if max_length is not None and len(cleaned_url) > max_length:
        raise DomainValidationError(
            "canonical_url exceeds the Binance Square post length limit"
        )

    parts = [cleaned_title]
    if cleaned_summary:
        parts.extend(["", cleaned_summary])
    parts.extend(["", cleaned_url])
    text = "\n".join(parts).strip()
    if max_length is None or len(text) <= max_length:
        return text

    if cleaned_summary:
        summary_budget = max_length - len(cleaned_title) - len(cleaned_url) - 4
        if summary_budget > 0:
            trimmed_summary = _trim_text(cleaned_summary, summary_budget)
            text = "\n".join([cleaned_title, "", trimmed_summary, "", cleaned_url]).strip()
            if len(text) <= max_length:
                return text

    title_budget = max_length - len(cleaned_url) - 2
    if title_budget <= 0:
        raise DomainValidationError(
            "canonical_url leaves no room for Binance Square post text"
        )

    trimmed_title = _trim_text(cleaned_title, title_budget)
    if cleaned_summary:
        text = "\n".join([trimmed_title, "", cleaned_summary, "", cleaned_url]).strip()
        if len(text) <= max_length:
            return text

    text = "\n".join([trimmed_title, "", cleaned_url]).strip()
    if len(text) > max_length:
        raise DomainValidationError("Binance Square post exceeds the length limit")
    return text


def publish_binance_square_post(
    text: str,
    *,
    settings: Settings | None = None,
) -> BinanceSquarePublishResult:
    client = BinanceSquareClient(settings=settings)
    return client.publish_short_post(text)


class BinanceSquareClient:
    def __init__(
        self,
        settings: Settings | None = None,
        *,
        api_key: str | None = None,
        timeout_seconds: int | None = None,
    ) -> None:
        self._settings = settings or get_settings()
        self._api_key = (
            api_key
            if api_key is not None
            else self._settings.binance_square_openapi_key
        )
        self._timeout_seconds = timeout_seconds or self._settings.request_timeout_seconds

    def publish_short_post(self, text: str) -> BinanceSquarePublishResult:
        api_key = (self._api_key or "").strip()
        if not api_key:
            raise BinanceSquarePublishError(
                "BINANCE_SQUARE_OPENAPI_KEY is required",
                retryable=False,
                error_type="missing_credentials",
            )

        payload = {"contentType": 1, "bodyTextOnly": text}
        request = urllib.request.Request(
            f"{BINANCE_SQUARE_BASE_URL_V1}{BINANCE_SQUARE_ENDPOINT}",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "X-Square-OpenAPI-Key": api_key,
                "Content-Type": "application/json",
                "clienttype": BINANCE_SQUARE_CLIENT_TYPE,
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(  # noqa: S310 - fixed Binance API endpoint
                request,
                timeout=self._timeout_seconds,
            ) as response:
                raw_text = response.read().decode("utf-8")
                status_code = getattr(response, "status", None)
        except urllib.error.HTTPError as exc:
            body = _safe_error_body(exc)
            raise _publish_error_from_http(exc.code, body) from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise BinanceSquarePublishError(
                "Binance Square request failed",
                retryable=True,
                error_type="network_error",
            ) from exc

        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            raise BinanceSquarePublishError(
                "Binance Square returned non-JSON response",
                retryable=True,
                status_code=status_code if isinstance(status_code, int) else None,
                error_type="invalid_json",
            ) from exc

        if not isinstance(parsed, dict):
            raise BinanceSquarePublishError(
                "Binance Square returned invalid JSON response",
                retryable=True,
                status_code=status_code if isinstance(status_code, int) else None,
                error_type="invalid_json",
            )

        provider_code = str(parsed.get("code") or "")
        if provider_code != "000000":
            provider_message = _safe_provider_message(parsed)
            raise _publish_error_from_provider(
                provider_code,
                provider_message,
                status_code=status_code if isinstance(status_code, int) else None,
            )

        data = parsed.get("data")
        if not isinstance(data, dict):
            raise BinanceSquarePublishError(
                "Binance Square response missing data",
                retryable=True,
                status_code=status_code if isinstance(status_code, int) else None,
                error_type="missing_data",
            )

        external_id = data.get("id")
        published_url = data.get("shareLink")
        return BinanceSquarePublishResult(
            external_id=str(external_id) if external_id else None,
            published_url=str(published_url) if published_url else None,
            provider_code=provider_code,
            raw_response=parsed,
        )


def _publish_error_from_http(status_code: int, body: str) -> BinanceSquarePublishError:
    body_lower = body.lower()
    if status_code == 504:
        return BinanceSquarePublishError(
            "Binance Square provider timeout",
            retryable=False,
            status_code=status_code,
            error_type="ambiguous_timeout",
            ambiguous_outcome=True,
        )
    if status_code in {401, 403}:
        return BinanceSquarePublishError(
            "Binance Square authentication rejected",
            retryable=False,
            status_code=status_code,
            error_type="authentication_rejected",
        )
    if status_code == 402:
        return BinanceSquarePublishError(
            "Binance Square access requires the correct entitlement",
            retryable=False,
            status_code=status_code,
            error_type="access_denied",
        )
    if status_code == 429 or _looks_like_rate_limit(body_lower):
        return BinanceSquarePublishError(
            "Binance Square daily publication limit reached",
            retryable=True,
            status_code=status_code,
            error_type="rate_limited",
        )
    if status_code in {400, 413, 422}:
        return BinanceSquarePublishError(
            "Binance Square rejected the post payload",
            retryable=False,
            status_code=status_code,
            error_type="invalid_payload",
        )
    if 500 <= status_code <= 599:
        return BinanceSquarePublishError(
            "Binance Square temporary upstream failure",
            retryable=True,
            status_code=status_code,
            error_type="upstream_failure",
        )
    return BinanceSquarePublishError(
        "Binance Square request failed",
        retryable=True,
        status_code=status_code,
        error_type="request_failed",
    )


def _publish_error_from_provider(
    provider_code: str,
    message: str,
    *,
    status_code: int | None = None,
) -> BinanceSquarePublishError:
    message_lower = message.lower()
    if _looks_like_rate_limit(message_lower):
        return BinanceSquarePublishError(
            "Binance Square daily publication limit reached",
            retryable=True,
            status_code=status_code,
            error_type="rate_limited",
        )
    if "auth" in message_lower or "credential" in message_lower:
        return BinanceSquarePublishError(
            "Binance Square authentication rejected",
            retryable=False,
            status_code=status_code,
            error_type="authentication_rejected",
        )
    if "permission" in message_lower or "entitlement" in message_lower:
        return BinanceSquarePublishError(
            "Binance Square access requires the correct entitlement",
            retryable=False,
            status_code=status_code,
            error_type="access_denied",
        )
    if "timeout" in message_lower or "504" in provider_code:
        return BinanceSquarePublishError(
            "Binance Square provider timeout",
            retryable=False,
            status_code=status_code,
            error_type="ambiguous_timeout",
            ambiguous_outcome=True,
        )
    return BinanceSquarePublishError(
        "Binance Square rejected the post payload",
        retryable=False,
        status_code=status_code,
        error_type="provider_rejected",
    )


def _safe_error_body(exc: urllib.error.HTTPError) -> str:
    try:
        raw = exc.read().decode("utf-8", errors="replace")
    except Exception:
        return ""
    if len(raw) > 240:
        return raw[:240] + "..."
    return raw


def _safe_provider_message(parsed: dict) -> str:
    message = parsed.get("message")
    if isinstance(message, str):
        return message.strip()
    if isinstance(message, dict):
        return json.dumps(message, ensure_ascii=False)
    return ""


def _looks_like_rate_limit(value: str) -> bool:
    return any(token in value for token in ("rate limit", "daily limit", "quota", "too many"))


def _normalize_text(value: str) -> str:
    return " ".join(value.split()).strip()


def _trim_text(value: str, limit: int) -> str:
    if limit <= 0:
        return ""
    if len(value) <= limit:
        return value
    if limit <= 3:
        return value[:limit]
    return value[: limit - 3].rstrip() + "..."
