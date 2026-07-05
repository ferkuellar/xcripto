"""Unit tests for the dependency-free RSS/Atom parser (no network)."""

import pytest

from app.connectors.base import ConnectorSecurityError, fetch_url
from app.connectors.rss_connector import FeedParseError, parse_feed

RSS = b"""<?xml version="1.0"?>
<rss version="2.0"><channel>
<title>Feed</title>
<item>
  <title>BTC reserve report published</title>
  <link>https://www.coindesk.com/markets/a1</link>
  <description>An exchange published its reserve report.</description>
  <guid>coindesk-a1</guid>
  <pubDate>Mon, 05 Jul 2026 10:00:00 +0000</pubDate>
</item>
<item>
  <title>Second item</title>
  <link>https://cointelegraph.com/news/a2</link>
  <description>Second summary.</description>
</item>
</channel></rss>"""

ATOM = b"""<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
<title>Atom Feed</title>
<entry>
  <title>Atom entry one</title>
  <link href="https://decrypt.co/a1" rel="alternate"/>
  <summary>Atom summary.</summary>
  <id>atom-a1</id>
  <updated>2026-07-05T10:00:00+00:00</updated>
</entry>
</feed>"""


def test_parse_rss_extracts_normalized_items():
    items = parse_feed(RSS)
    assert len(items) == 2
    first = items[0]
    assert first.title == "BTC reserve report published"
    assert first.url == "https://www.coindesk.com/markets/a1"
    assert first.source_domain == "coindesk.com"  # www stripped
    assert first.external_id == "coindesk-a1"
    assert first.published_at is not None
    assert first.raw_payload_hash


def test_parse_atom_extracts_link_href_and_domain():
    items = parse_feed(ATOM)
    assert len(items) == 1
    assert items[0].url == "https://decrypt.co/a1"
    assert items[0].source_domain == "decrypt.co"
    assert items[0].summary == "Atom summary."


def test_parse_invalid_xml_raises_feed_parse_error():
    with pytest.raises(FeedParseError):
        parse_feed(b"this is not xml <<<")


def test_parse_rejects_dtd_and_entity_payload():
    payload = b"""<?xml version="1.0"?>
    <!DOCTYPE rss [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
    <rss version="2.0"><channel><item><title>&xxe;</title>
    <link>https://coindesk.com/a</link></item></channel></rss>"""
    with pytest.raises(FeedParseError, match="DTD/ENTITY"):
        parse_feed(payload)


def test_parse_skips_items_without_title_or_link():
    feed = b"""<?xml version="1.0"?><rss version="2.0"><channel>
    <item><description>no title no link</description></item>
    <item><title>Has title</title><link>https://coindesk.com/ok</link></item>
    </channel></rss>"""
    items = parse_feed(feed)
    assert len(items) == 1
    assert items[0].title == "Has title"


def test_fetch_url_rejects_non_http_scheme():
    with pytest.raises(ConnectorSecurityError, match="http or https"):
        fetch_url(
            "file:///tmp/feed.xml",
            timeout=1,
            user_agent="test",
            allowed_domains={"coindesk.com"},
        )
