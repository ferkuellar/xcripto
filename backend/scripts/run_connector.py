"""Manual connector runner (P9). Runs a real connector in-process against the
configured database. Disabled unless CONNECTORS_ENABLED and the per-connector switch
are true. Never promotes or publishes.

Examples:
    # real feed (needs network + allowed domain):
    CONNECTORS_ENABLED=true RSS_CONNECTOR_ENABLED=true \
    RSS_CONNECTOR_ALLOWED_DOMAINS=coindesk.com \
    python scripts/run_connector.py --connector rss \
      --feed-url https://www.coindesk.com/feed --max-items 5

    # deterministic local fixture (no network):
    python scripts/run_connector.py --connector rss --feed-file sample.xml --max-items 5
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys


async def _run(args) -> int:
    from app.db.session import AsyncSessionLocal
    from app.services import connector_service

    fetch = None
    if args.feed_file:
        with open(args.feed_file, "rb") as handle:
            data = handle.read()
        fetch = lambda _url: data  # noqa: E731 — inject fixture bytes

    async with AsyncSessionLocal() as session:
        result = await connector_service.run_rss_connector(
            session,
            args.feed_url or f"file://{args.feed_file}",
            fetch=fetch,
            max_items=args.max_items,
            actor_role=args.actor_role,
        )
    print(json.dumps(result.as_dict(), indent=2), flush=True)
    if result.disabled:
        print("connector disabled (set CONNECTORS_ENABLED + RSS_CONNECTOR_ENABLED)", flush=True)
        return 0
    return 1 if result.errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="XMIP manual connector runner")
    parser.add_argument("--connector", default="rss", choices=["rss"])
    parser.add_argument("--feed-url", default=None)
    parser.add_argument("--feed-file", default=None)
    parser.add_argument("--max-items", type=int, default=None)
    parser.add_argument("--actor-role", default="system")
    args = parser.parse_args()
    if not args.feed_url and not args.feed_file:
        parser.error("provide --feed-url or --feed-file")
    return asyncio.run(_run(args))


if __name__ == "__main__":
    sys.exit(main())
