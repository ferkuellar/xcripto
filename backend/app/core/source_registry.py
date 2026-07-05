"""Source connector registry: maps approved feed providers to source identity.

Quality classification for connector-ingested sources. Reputation is documented in
``docs/012-connectors/SOURCE_CONNECTOR_REGISTRY.md`` and mapped to the S1-S5 policy via
``trust_level`` (T0=S1, T1=S2, T2=S3, T3=S4). Connector feeds fail closed unless the
feed URL belongs to an explicit provider entry. Item links must also match that
provider's allowed item domains.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.connectors.base import domain_matches, domain_of


@dataclass(frozen=True)
class RegistryEntry:
    domain: str
    source_name: str
    trust_level: str  # T0-T3 (see SOURCE_QUALITY_POLICY §4)
    rationale: str


@dataclass(frozen=True)
class FeedProviderEntry:
    provider_key: str
    feed_domains: frozenset[str]
    item_domains: frozenset[str]
    source_name: str
    trust_level: str
    rationale: str

    @property
    def canonical_domain(self) -> str:
        return sorted(self.feed_domains)[0]


# Known reputable crypto news outlets with an editorial process (S2/S3).
SOURCE_REGISTRY: dict[str, RegistryEntry] = {
    "coindesk.com": RegistryEntry(
        "coindesk.com", "CoinDesk", "T1", "Established crypto outlet with editorial process (S2)."
    ),
    "cointelegraph.com": RegistryEntry(
        "cointelegraph.com", "Cointelegraph", "T2", "Recognized outlet; treat as S3 pending policy."
    ),
    "decrypt.co": RegistryEntry(
        "decrypt.co", "Decrypt", "T2", "Recognized outlet; treat as S3 pending policy."
    ),
    "theblock.co": RegistryEntry(
        "theblock.co", "The Block", "T1", "Institutional-grade crypto news, editorial process (S2)."
    ),
}

FEED_PROVIDER_REGISTRY: dict[str, FeedProviderEntry] = {
    "coindesk": FeedProviderEntry(
        provider_key="coindesk",
        feed_domains=frozenset({"coindesk.com"}),
        item_domains=frozenset({"coindesk.com"}),
        source_name="CoinDesk",
        trust_level="T1",
        rationale="CoinDesk RSS feed; item links must remain on coindesk.com.",
    ),
    "cointelegraph": FeedProviderEntry(
        provider_key="cointelegraph",
        feed_domains=frozenset({"cointelegraph.com"}),
        item_domains=frozenset({"cointelegraph.com"}),
        source_name="Cointelegraph",
        trust_level="T2",
        rationale="Cointelegraph RSS feed; item links must remain on cointelegraph.com.",
    ),
    "decrypt": FeedProviderEntry(
        provider_key="decrypt",
        feed_domains=frozenset({"decrypt.co"}),
        item_domains=frozenset({"decrypt.co"}),
        source_name="Decrypt",
        trust_level="T2",
        rationale="Decrypt RSS feed; item links must remain on decrypt.co.",
    ),
    "theblock": FeedProviderEntry(
        provider_key="theblock",
        feed_domains=frozenset({"theblock.co"}),
        item_domains=frozenset({"theblock.co"}),
        source_name="The Block",
        trust_level="T1",
        rationale="The Block RSS feed; item links must remain on theblock.co.",
    ),
}

# Legacy helper fallback for non-connector callers. RSS providers themselves fail closed.
DEFAULT_UNKNOWN_TRUST_LEVEL = "T3"


def normalize_domain(domain: str | None) -> str:
    if not domain:
        return ""
    domain = domain.strip().lower()
    return domain[4:] if domain.startswith("www.") else domain


def lookup(domain: str | None) -> RegistryEntry | None:
    return SOURCE_REGISTRY.get(normalize_domain(domain))


def trust_level_for_domain(domain: str | None) -> str:
    entry = lookup(domain)
    return entry.trust_level if entry else DEFAULT_UNKNOWN_TRUST_LEVEL


def source_name_for_domain(domain: str | None, fallback: str | None = None) -> str:
    entry = lookup(domain)
    if entry:
        return entry.source_name
    return fallback or normalize_domain(domain) or "unknown"


def provider_for_feed_url(
    feed_url: str,
    allowed_domains: set[str],
) -> FeedProviderEntry:
    feed_domain = domain_of(feed_url)
    for provider in FEED_PROVIDER_REGISTRY.values():
        provider_allowed = any(
            any(domain_matches(feed_domain, domain) for domain in provider.feed_domains)
            and domain in allowed_domains
            for domain in provider.feed_domains
        )
        if provider_allowed:
            return provider
    raise ValueError("feed_url does not match an allowed feed provider")


def provider_allows_item(provider: FeedProviderEntry, item_url: str) -> bool:
    item_domain = domain_of(item_url)
    return any(domain_matches(item_domain, domain) for domain in provider.item_domains)
