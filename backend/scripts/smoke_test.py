from __future__ import annotations

import argparse
import json
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def request_json(
    base_url: str,
    path: str,
    method: str = "GET",
    payload: dict | None = None,
    api_key: str | None = None,
) -> tuple[int, dict]:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key
        headers["X-Actor-Role"] = "admin"
    request = Request(f"{base_url.rstrip('/')}{path}", data=body, headers=headers, method=method)
    try:
        with urlopen(request, timeout=5) as response:
            data = response.read().decode("utf-8")
            return response.status, json.loads(data) if data else {}
    except HTTPError as exc:
        data = exc.read().decode("utf-8")
        return exc.code, json.loads(data) if data else {}
    except URLError as exc:
        raise RuntimeError(f"Request to {path} failed: {exc}") from exc


def assert_status(base_url: str, path: str, expected: int = 200) -> dict:
    status, payload = request_json(base_url, path)
    if status != expected:
        raise RuntimeError(f"{path} returned HTTP {status}: {payload}")
    print(f"OK {path}: {payload.get('status', 'ok')}")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="XMIP backend production smoke test")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--create-intake-signal", action="store_true")
    args = parser.parse_args()

    assert_status(args.base_url, "/health")
    assert_status(args.base_url, "/live")
    assert_status(args.base_url, "/ready")
    assert_status(args.base_url, "/openapi.json")

    if args.create_intake_signal:
        payload = {
            "signal_type": "manual",
            "source_name": "Smoke Test",
            "source_url": f"https://example.com/smoke/{int(time.time())}",
            "raw_title": f"Smoke test signal {int(time.time())}",
            "raw_summary": "Production smoke test signal.",
            "topic": "ops",
        }
        status, response = request_json(
            args.base_url,
            "/api/v1/intake/signals",
            method="POST",
            payload=payload,
            api_key=args.api_key,
        )
        if status != 201:
            raise RuntimeError(f"intake signal smoke test returned HTTP {status}: {response}")
        print(f"OK /api/v1/intake/signals: {response['id']}")

    print("Smoke test passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"Smoke test failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
