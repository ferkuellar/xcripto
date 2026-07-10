from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import secrets
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Final

from app.core.config import get_settings
from app.core.errors import DomainValidationError

logger = logging.getLogger(__name__)

X_API_BASE_URL: Final = "https://api.x.com"
X_POST_LIMIT: Final = 280


@dataclass(slots=True)
class XPublishResult:
    post_id: str
    post_url: str
    raw_response: dict


class XPublishError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        retryable: bool,
        status_code: int | None = None,
        error_type: str | None = None,
    ) -> None:
        super().__init__(message)
        self.retryable = retryable
        self.status_code = status_code
        self.error_type = error_type


def build_x_post(
    title: str,
    summary: str | None,
    canonical_url: str,
    *,
    max_length: int = X_POST_LIMIT,
) -> str:
    cleaned_title = _normalize_text(title)
    cleaned_summary = _normalize_text(summary or "")
    cleaned_url = canonical_url.strip()
    if not cleaned_url:
        raise DomainValidationError("canonical_url is required for X publication")
    if len(cleaned_url) > max_length:
        raise DomainValidationError("canonical_url exceeds the X post length limit")

    separator = "\n\n"
    if cleaned_summary:
        text = separator.join([cleaned_title, cleaned_summary, cleaned_url])
        if len(text) <= max_length:
            return text
        summary_budget = max_length - len(cleaned_title) - len(cleaned_url) - len(separator) * 2
        if summary_budget > 0:
            trimmed_summary = _trim_text(cleaned_summary, summary_budget)
            text = separator.join([cleaned_title, trimmed_summary, cleaned_url])
            if len(text) <= max_length:
                return text

    title_budget = max_length - len(cleaned_url) - len(separator)
    if title_budget <= 0:
        raise DomainValidationError("canonical_url leaves no room for X post text")
    trimmed_title = _trim_text(cleaned_title, title_budget)
    text = separator.join([trimmed_title, cleaned_url])
    if len(text) > max_length:
        raise DomainValidationError("X post exceeds the length limit")
    return text


def publish_x_post(text: str) -> XPublishResult:
    settings = get_settings()
    credentials = _x_credentials(settings)
    if credentials is None:
        raise XPublishError("X credentials are required", retryable=False)

    url = f"{X_API_BASE_URL}/2/tweets"
    payload = {"text": text}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": _build_oauth1_header(
            method="POST",
            url=url,
            consumer_key=credentials["consumer_key"],
            consumer_secret=credentials["consumer_secret"],
            token=credentials["access_token"],
            token_secret=credentials["access_token_secret"],
        ),
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(  # noqa: S310 - validated X API endpoint
            request,
            timeout=settings.request_timeout_seconds,
        ) as response:
            raw = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = _safe_error_body(exc)
        raise _x_error_from_http(exc.code, body) from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise XPublishError("X request failed", retryable=True) from exc

    result = raw.get("data") if isinstance(raw, dict) else None
    if not isinstance(result, dict):
        raise XPublishError("X response missing data", retryable=True)
    post_id = str(result.get("id") or "")
    if not post_id:
        raise XPublishError("X response missing post id", retryable=True)
    post_url = f"https://x.com/i/web/status/{post_id}"
    return XPublishResult(post_id=post_id, post_url=post_url, raw_response=raw)


def _x_credentials(settings) -> dict[str, str] | None:
    if not (
        settings.x_api_key
        and settings.x_api_secret
        and settings.x_access_token
        and settings.x_access_token_secret
    ):
        return None
    return {
        "consumer_key": settings.x_api_key,
        "consumer_secret": settings.x_api_secret,
        "access_token": settings.x_access_token,
        "access_token_secret": settings.x_access_token_secret,
    }


def _build_oauth1_header(
    *,
    method: str,
    url: str,
    consumer_key: str,
    consumer_secret: str,
    token: str,
    token_secret: str,
) -> str:
    nonce = secrets.token_hex(16)
    timestamp = str(int(time.time()))
    parsed = urllib.parse.urlsplit(url)
    normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    oauth_params = {
        "oauth_consumer_key": consumer_key,
        "oauth_nonce": nonce,
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": timestamp,
        "oauth_token": token,
        "oauth_version": "1.0",
    }
    param_string = _normalized_param_string(oauth_params)
    base_string = "&".join(
        [
            _oauth_encode(method.upper()),
            _oauth_encode(normalized_url),
            _oauth_encode(param_string),
        ]
    )
    signing_key = f"{_oauth_encode(consumer_secret)}&{_oauth_encode(token_secret)}"
    signature = base64.b64encode(
        hmac.new(signing_key.encode("utf-8"), base_string.encode("utf-8"), hashlib.sha1).digest()
    ).decode("ascii")
    oauth_params["oauth_signature"] = signature
    header_params = ", ".join(
        f'{key}="{_oauth_encode(value)}"' for key, value in sorted(oauth_params.items())
    )
    return f"OAuth {header_params}"


def _normalized_param_string(params: dict[str, str]) -> str:
    pairs = sorted((_oauth_encode(key), _oauth_encode(value)) for key, value in params.items())
    return "&".join(f"{key}={value}" for key, value in pairs)


def _oauth_encode(value: str) -> str:
    return urllib.parse.quote(str(value), safe="~")


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


def _safe_error_body(exc: urllib.error.HTTPError) -> str:
    try:
        raw = exc.read().decode("utf-8", errors="replace")
    except Exception:
        return ""
    if len(raw) > 240:
        return raw[:240] + "..."
    return raw


def _x_error_from_http(status_code: int, body: str) -> XPublishError:
    body_lower = body.lower()
    if status_code == 402:
        return XPublishError(
            "X API access requires paid entitlement",
            retryable=False,
            status_code=status_code,
        )
    if status_code in {401, 403}:
        return XPublishError(
            "X rejected credentials or access",
            retryable=False,
            status_code=status_code,
        )
    if status_code == 429:
        return XPublishError("X rate limit exceeded", retryable=True, status_code=status_code)
    if status_code in {400, 422} and ("duplicate" in body_lower or "already" in body_lower):
        return XPublishError(
            "X rejected duplicate content",
            retryable=False,
            status_code=status_code,
        )
    if status_code in {400, 422}:
        return XPublishError(
            "X rejected content",
            retryable=False,
            status_code=status_code,
        )
    if 500 <= status_code <= 599:
        return XPublishError(
            "X temporary upstream failure",
            retryable=True,
            status_code=status_code,
        )
    return XPublishError("X request failed", retryable=True, status_code=status_code)
