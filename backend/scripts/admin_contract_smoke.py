from __future__ import annotations

import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ADMIN_CONTRACT_ENDPOINTS = [
    "/health",
    "/live",
    "/ready",
    "/api/v1/admin/dashboard/overview",
    "/api/v1/admin/dashboard/newsroom-health",
    "/api/v1/admin/intake/queue",
    "/api/v1/admin/editorial/work-queue",
    "/api/v1/admin/blockers",
    "/api/v1/admin/readiness/board",
    "/api/v1/admin/tasks/board",
    "/api/v1/admin/publications/board",
    "/api/v1/admin/ownership/board",
    "/api/v1/admin/gaps",
    "/api/v1/admin/agent-runner/summary",
    "/api/v1/admin/connectors/summary",
    "/api/v1/admin/audit/summary",
]


def request_json(
    base_url: str,
    path: str,
    api_key: str | None = None,
    actor_role: str | None = None,
) -> tuple[int, dict]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key
    if actor_role:
        headers["X-Actor-Role"] = actor_role
    request = Request(f"{base_url.rstrip('/')}{path}", headers=headers, method="GET")
    try:
        with urlopen(request, timeout=5) as response:
            data = response.read().decode("utf-8")
            return response.status, json.loads(data) if data else {}
    except HTTPError as exc:
        data = exc.read().decode("utf-8")
        return exc.code, json.loads(data) if data else {}
    except URLError as exc:
        raise RuntimeError(f"Request to {path} failed: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="XMIP admin dashboard contract smoke test")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--actor-role", default=None)
    args = parser.parse_args()

    failures: list[str] = []
    for path in ADMIN_CONTRACT_ENDPOINTS:
        status, payload = request_json(
            args.base_url,
            path,
            api_key=args.api_key,
            actor_role=args.actor_role,
        )
        print(f"{status} {path}")
        if status >= 400:
            failures.append(f"{path} returned HTTP {status}: {payload}")

    if failures:
        raise RuntimeError("; ".join(failures))
    print("Admin contract smoke test passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"Admin contract smoke test failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
