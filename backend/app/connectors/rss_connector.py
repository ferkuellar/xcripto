"""Minimal, dependency-free RSS 2.0 / Atom parser.

Uses the stdlib XML parser (no external feedparser). The connector service caps the
fetched body size before parsing, mitigating XML-bomb inputs; ElementTree does not
resolve external entities by default (no XXE).
"""

from __future__ import annotations

from xml.etree import ElementTree

from app.connectors.base import NormalizedItem, _to_iso, domain_of, payload_hash


class FeedParseError(ValueError):
    """Raised when the feed body cannot be parsed as XML."""


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()  # strip namespace


def _find_text(item: ElementTree.Element, *names: str) -> str:
    wanted = {n.lower() for n in names}
    for child in item:
        if _local(child.tag) in wanted and child.text and child.text.strip():
            return child.text.strip()
    return ""


def _find_link(item: ElementTree.Element) -> str:
    # RSS: <link>text</link>. Atom: <link href="..."/> (prefer rel=alternate/no rel).
    fallback = ""
    for child in item:
        if _local(child.tag) != "link":
            continue
        if child.text and child.text.strip():
            return child.text.strip()
        href = child.attrib.get("href")
        if href:
            rel = child.attrib.get("rel", "alternate")
            if rel == "alternate":
                return href
            fallback = fallback or href
    return fallback


def parse_feed(content: bytes) -> list[NormalizedItem]:
    """Parse RSS/Atom bytes into normalized items. Skips malformed entries."""
    upper_content = content.upper()
    if b"<!DOCTYPE" in upper_content or b"<!ENTITY" in upper_content:
        raise FeedParseError("RSS payload contains forbidden DTD/ENTITY declarations")
    try:
        root = ElementTree.fromstring(content)
    except ElementTree.ParseError as exc:
        raise FeedParseError(str(exc)) from exc

    items: list[NormalizedItem] = []
    for element in root.iter():
        if _local(element.tag) not in {"item", "entry"}:
            continue
        title = _find_text(element, "title")
        url = _find_link(element)
        if not title or not url:
            continue  # skip entries without a title or link
        summary = _find_text(element, "description", "summary", "content")
        guid = _find_text(element, "guid", "id") or url
        published = _to_iso(_find_text(element, "pubDate", "published", "updated"))
        items.append(
            NormalizedItem(
                external_id=guid,
                title=title[:480],
                summary=summary[:2000],
                url=url[:2048],
                source_domain=domain_of(url),
                published_at=published,
                raw_payload_hash=payload_hash(guid, title, url),
            )
        )
    return items
