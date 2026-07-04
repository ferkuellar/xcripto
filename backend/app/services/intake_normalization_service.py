from hashlib import sha256
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

TRACKING_QUERY_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
}


def normalize_text(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = " ".join(value.strip().split())
    return normalized or None


def normalize_comparison_text(value: str | None) -> str:
    normalized = normalize_text(value)
    return normalized.lower() if normalized else ""


def canonicalize_url(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    if not stripped:
        return None
    parsed = urlsplit(stripped)
    query = [
        (key, val)
        for key, val in parse_qsl(parsed.query, keep_blank_values=True)
        if key.lower() not in TRACKING_QUERY_PARAMS
    ]
    path = parsed.path.rstrip("/") or "/"
    canonical = urlunsplit(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            path,
            urlencode(query, doseq=True),
            "",
        )
    )
    return canonical.rstrip("/") if canonical.endswith("/") and path == "/" else canonical


def normalize_list(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        normalized = normalize_text(value)
        if normalized and normalized not in result:
            result.append(normalized)
    return result


def normalize_symbol_list(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        normalized = normalize_text(value)
        if normalized:
            symbol = normalized.upper()
            if symbol not in result:
                result.append(symbol)
    return result


def build_content_hash(
    normalized_title: str | None,
    normalized_summary: str | None,
    raw_content: str | None,
    url_canonical: str | None,
) -> str:
    material = "|".join(
        [
            normalize_comparison_text(normalized_title),
            normalize_comparison_text(normalized_summary),
            normalize_comparison_text(raw_content),
        ]
    )
    return sha256(material.encode("utf-8")).hexdigest()


def build_dedupe_key(
    normalized_title: str | None,
    topic: str | None,
    source_name: str | None,
) -> str:
    title = normalize_comparison_text(normalized_title)
    topic_key = normalize_comparison_text(topic)
    source_key = normalize_comparison_text(source_name)
    return "|".join([title, topic_key, source_key]).strip("|")


def normalize_signal_payload(data: dict) -> dict:
    normalized_title = normalize_text(data.get("normalized_title") or data.get("raw_title"))
    normalized_summary = normalize_text(data.get("normalized_summary") or data.get("raw_summary"))
    raw_content = normalize_text(data.get("raw_content"))
    source_url = normalize_text(data.get("source_url"))
    url_canonical = canonicalize_url(data.get("url_canonical") or source_url)
    asset_symbols = normalize_symbol_list(data.get("asset_symbols") or [])
    entities = normalize_list(data.get("entities") or [])
    keywords = normalize_list(data.get("keywords") or [])
    topic = normalize_text(data.get("topic")) or "general"
    language = normalize_text(data.get("language")) or "en"
    source_name = normalize_text(data.get("source_name"))

    normalized_payload = {
        "normalized_title": normalized_title,
        "normalized_summary": normalized_summary,
        "language": language,
        "topic": topic,
        "asset_symbols": asset_symbols,
        "entities": entities,
        "keywords": keywords,
        "url_canonical": url_canonical,
    }
    content_hash = build_content_hash(
        normalized_title,
        normalized_summary,
        raw_content,
        url_canonical,
    )
    dedupe_key = build_dedupe_key(normalized_title, topic, source_name)

    data.update(
        {
            "source_name": source_name,
            "source_url": source_url,
            "raw_title": normalize_text(data.get("raw_title")),
            "raw_summary": normalize_text(data.get("raw_summary")),
            "raw_content": raw_content,
            "normalized_title": normalized_title,
            "normalized_summary": normalized_summary,
            "language": language,
            "topic": topic,
            "asset_symbols": asset_symbols,
            "entities": entities,
            "keywords": keywords,
            "url_canonical": url_canonical,
            "content_hash": content_hash,
            "dedupe_key": dedupe_key,
            "normalized_payload": normalized_payload,
        }
    )
    return data
