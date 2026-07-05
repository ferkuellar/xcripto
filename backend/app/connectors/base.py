"""Connector base contracts and a safe HTTP fetch helper."""

from __future__ import annotations

import hashlib
import ipaddress
import socket
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime
from urllib.parse import urljoin, urlsplit

# Cap the fetched body so a hostile/huge feed cannot exhaust memory or feed an XML bomb.
MAX_FETCH_BYTES = 2_000_000
METADATA_IP = ipaddress.ip_address("169.254.169.254")


class ConnectorSecurityError(ValueError):
    """Raised when a connector URL fails SSRF or provider validation."""


@dataclass
class NormalizedItem:
    external_id: str
    title: str
    summary: str
    url: str
    source_domain: str
    published_at: str | None = None
    raw_payload_hash: str = ""


@dataclass
class ConnectorRunResult:
    connector_name: str
    fetched_count: int = 0
    accepted_count: int = 0
    duplicate_count: int = 0
    rejected_count: int = 0
    errors: list[str] = field(default_factory=list)
    disabled: bool = False
    reason: str | None = None
    adapter_run_id: str | None = None

    def as_dict(self) -> dict:
        return {
            "connector_name": self.connector_name,
            "fetched_count": self.fetched_count,
            "accepted_count": self.accepted_count,
            "duplicate_count": self.duplicate_count,
            "rejected_count": self.rejected_count,
            "errors": self.errors,
            "disabled": self.disabled,
            "reason": self.reason,
            "adapter_run_id": self.adapter_run_id,
        }


def domain_of(url: str) -> str:
    host = (urlsplit(url).hostname or "").strip().lower().rstrip(".")
    return host[4:] if host.startswith("www.") else host


def domain_matches(host: str, allowed_domain: str) -> bool:
    host = domain_of(f"https://{host}") if "://" not in host else domain_of(host)
    allowed = (allowed_domain or "").strip().lower().lstrip(".")
    return bool(allowed and (host == allowed or host.endswith(f".{allowed}")))


def payload_hash(*parts: str) -> str:
    return hashlib.sha256("".join(p or "" for p in parts).encode("utf-8")).hexdigest()


def fetch_url(
    url: str,
    *,
    timeout: int,
    user_agent: str,
    allowed_domains: set[str],
) -> bytes:
    """Fetch a URL body after SSRF validation of initial, redirect and final URLs."""
    _validate_fetch_url(url, allowed_domains)
    request = urllib.request.Request(url, headers={"User-Agent": user_agent, "Accept": "*/*"})
    opener = urllib.request.build_opener(_ValidatingRedirectHandler(allowed_domains))
    with opener.open(request, timeout=timeout) as response:  # noqa: S310 (validated URL)
        final_url = response.geturl()
        _validate_fetch_url(final_url, allowed_domains)
        return response.read(MAX_FETCH_BYTES + 1)[:MAX_FETCH_BYTES]


class _ValidatingRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self, allowed_domains: set[str]) -> None:
        self.allowed_domains = allowed_domains
        super().__init__()

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        redirected_url = urljoin(req.full_url, newurl)
        _validate_fetch_url(redirected_url, self.allowed_domains)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _validate_fetch_url(url: str, allowed_domains: set[str]) -> None:
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"}:
        raise ConnectorSecurityError("feed_url must use http or https")
    if not parsed.hostname:
        raise ConnectorSecurityError("feed_url must include a hostname")
    host = parsed.hostname.strip().lower().rstrip(".")
    if not any(domain_matches(host, domain) for domain in allowed_domains):
        raise ConnectorSecurityError("feed_url host is not in the allowed connector registry")
    _resolve_public_host(host, parsed.port or (443 if parsed.scheme == "https" else 80))


def _resolve_public_host(host: str, port: int) -> None:
    try:
        addresses = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise ConnectorSecurityError(f"feed_url host could not be resolved: {host}") from exc
    if not addresses:
        raise ConnectorSecurityError(f"feed_url host could not be resolved: {host}")
    for _family, _type, _proto, _canonname, sockaddr in addresses:
        ip = ipaddress.ip_address(sockaddr[0])
        if _is_blocked_ip(ip):
            raise ConnectorSecurityError(f"feed_url resolves to blocked address: {ip}")


def _is_blocked_ip(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    return (
        ip == METADATA_IP
        or ip.is_loopback
        or ip.is_private
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_reserved
        or ip.is_unspecified
        or not ip.is_global
    )


def _to_iso(value: str | None) -> str | None:
    if not value:
        return None
    for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z", "%Y-%m-%dT%H:%M:%S%z"):
        try:
            return datetime.strptime(value.strip(), fmt).isoformat()
        except ValueError:
            continue
    return None
