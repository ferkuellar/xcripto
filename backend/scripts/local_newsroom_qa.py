"""Local newsroom QA: end-to-end editorial flow against a local XMIP backend.

Exercises the minimum professional-newsroom path without external APIs:
health checks -> manual IntakeSignal -> dedupe -> promote to NewsItem with
workflow -> admin overview / work queue / readiness board / audit summary.

Usage:
    python scripts/local_newsroom_qa.py --base-url http://127.0.0.1:8000 \
        --api-key dev-secret --actor-role admin

Creates a small amount of clearly-labeled QA data (titles prefixed with
"[QA]"). Never publishes anything and never calls external services.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
import uuid

FAILURES: list[str] = []
RESULTS: list[str] = []


def log(line: str) -> None:
    print(line, flush=True)
    RESULTS.append(line)


def request(
    base_url: str,
    method: str,
    path: str,
    *,
    api_key: str | None,
    actor_role: str | None,
    payload: dict | None = None,
    expected: tuple[int, ...] = (200,),
) -> tuple[int, dict | list | None]:
    url = f"{base_url.rstrip('/')}{path}"
    headers = {"Accept": "application/json"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    if api_key:
        headers["X-API-Key"] = api_key
    if actor_role:
        headers["X-Actor-Role"] = actor_role
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            body = json.loads(response.read() or b"null")
            status = response.status
    except urllib.error.HTTPError as exc:
        status = exc.code
        try:
            body = json.loads(exc.read() or b"null")
        except json.JSONDecodeError:
            body = None
    except (urllib.error.URLError, TimeoutError) as exc:
        FAILURES.append(f"{method} {path}: unreachable ({exc})")
        log(f"[FAIL] {method} {path}: unreachable ({exc})")
        return 0, None

    if status in expected:
        log(f"[ OK ] {method} {path} -> {status}")
    else:
        FAILURES.append(f"{method} {path}: expected {expected}, got {status} body={body}")
        log(f"[FAIL] {method} {path}: expected {expected}, got {status}")
    return status, body


def main() -> int:
    parser = argparse.ArgumentParser(description="XMIP local newsroom QA flow")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--actor-role", default=None)
    args = parser.parse_args()

    auth = {"api_key": args.api_key, "actor_role": args.actor_role}
    run_tag = uuid.uuid4().hex[:8]
    log(f"== XMIP local newsroom QA :: run {run_tag} :: {args.base_url} ==")

    # 1. Health surface
    request(args.base_url, "GET", "/health", **auth)
    request(args.base_url, "GET", "/live", **auth)
    request(args.base_url, "GET", "/ready", **auth)

    # 2. Manual intake signal with a clear, verifiable source
    _, signal = request(
        args.base_url,
        "POST",
        "/api/v1/intake/signals",
        **auth,
        payload={
            "signal_type": "manual",
            "source_name": "Example Primary Source",
            "source_url": "https://example.com/official-announcement",
            "raw_title": f"[QA] Exchange announces reserve transparency report ({run_tag})",
            "raw_summary": "The company published an updated reserve transparency report.",
            "topic": "exchanges",
            "priority": "P1",
            "confidence_level": "IC2",
        },
        expected=(201,),
    )
    signal_id = signal.get("id") if isinstance(signal, dict) else None
    if not signal_id:
        log("[FAIL] no signal id; aborting flow steps")
        return report()
    log(f"       IntakeSignal id={signal_id} dedupe={signal.get('dedupe_status')} "
        f"hash={str(signal.get('content_hash'))[:12]}")

    # 3. Dedupe recalculation
    _, deduped = request(
        args.base_url, "POST", f"/api/v1/intake/signals/{signal_id}/dedupe", **auth
    )
    if isinstance(deduped, dict):
        log(f"       dedupe_status={deduped.get('dedupe_status')} "
            f"dedupe_key={str(deduped.get('dedupe_key'))[:16]} "
            f"duplicate_of={deduped.get('duplicate_of_signal_id')}")

    # 4. Promote to NewsItem with workflow
    _, promoted = request(
        args.base_url,
        "POST",
        f"/api/v1/intake/signals/{signal_id}/promote",
        **auth,
        payload={"create_workflow": True, "workflow_type": "editorial_pipeline"},
    )
    news_id = promoted.get("promoted_news_item_id") if isinstance(promoted, dict) else None
    if news_id:
        log(f"       NewsItem id={news_id}")
    else:
        FAILURES.append("promote did not return promoted_news_item_id")
        log("[FAIL] promote did not return promoted_news_item_id")

    if news_id:
        request(args.base_url, "GET", f"/api/v1/news/{news_id}", **auth)

    # 5. Admin surface (RBAC)
    _, overview = request(args.base_url, "GET", "/api/v1/admin/dashboard/overview", **auth)
    request(args.base_url, "GET", "/api/v1/admin/editorial/work-queue", **auth)
    request(args.base_url, "GET", "/api/v1/admin/readiness/board", **auth)
    request(args.base_url, "GET", "/api/v1/admin/audit/summary", **auth)

    if isinstance(overview, dict):
        keys = ", ".join(sorted(overview.keys())[:8])
        log(f"       overview keys: {keys}")

    return report(created_ids={"intake_signal": signal_id, "news_item": news_id})


def report(created_ids: dict | None = None) -> int:
    log("== resumen ==")
    if created_ids:
        for name, value in created_ids.items():
            log(f"   creado {name}: {value}")
    if FAILURES:
        log(f"RESULTADO: FAIL ({len(FAILURES)} problemas)")
        for failure in FAILURES:
            log(f"   - {failure}")
        return 1
    log("RESULTADO: PASS — flujo editorial local completo")
    return 0


if __name__ == "__main__":
    sys.exit(main())
