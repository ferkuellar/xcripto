"""Controlled newsroom pilot: synthetic editorial trial against a running XMIP backend.

Exercises the source-quality matrix (S1-S5), the fail-closed publication gate, the
readiness scoring and deduplication, asserting the *expected* editorial outcome of each
case. Uses only synthetic, neutral data; never publishes anything and never calls
external services.

Fail-closed guarantees enforced here (the run FAILS if any is violated):
  - A source-quality-blocked case (S3/S4 without strong verification, S5, or a
    blocked/restricted source) must NOT be allowed to advance to `approved`.
  - An S1/S2 (or strongly verified S3/S4) case must be allowed to advance.
  - Readiness must reflect weak sources (low source component + warning).
  - A critical-risk case must be blocked in readiness.

Usage:
    python scripts/controlled_newsroom_pilot.py \
        --base-url http://127.0.0.1:8010 --api-key dev-secret --actor-role admin
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
import uuid

# S-level → SourceReference.trust_level (doc SOURCE_QUALITY_POLICY §4).
TRUST = {"S1": "T0", "S2": "T1", "S3": "T2", "S4": "T3"}

RESULTS: list[dict] = []


def request(
    base_url: str,
    method: str,
    path: str,
    *,
    api_key: str | None,
    actor_role: str | None,
    actor_id: str = "pilot",
    payload: dict | None = None,
) -> tuple[int, dict | list | None]:
    url = f"{base_url.rstrip('/')}{path}"
    headers = {"Accept": "application/json"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    if api_key:
        headers["X-API-Key"] = api_key
    if actor_role:
        headers["X-Actor-Role"] = actor_role
    if actor_id:
        headers["X-Actor-Id"] = actor_id
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return response.status, json.loads(response.read() or b"null")
    except urllib.error.HTTPError as exc:
        try:
            body = json.loads(exc.read() or b"null")
        except json.JSONDecodeError:
            body = None
        return exc.code, body
    except (urllib.error.URLError, TimeoutError) as exc:
        return 0, {"error": f"unreachable: {exc}"}


class Client:
    def __init__(self, base_url: str, api_key: str | None, actor_role: str | None, tag: str):
        self.base_url = base_url
        self.auth = {"api_key": api_key, "actor_role": actor_role}
        self.tag = tag

    def _req(self, method, path, payload=None):
        return request(self.base_url, method, path, payload=payload, **self.auth)

    def create_news(self, idx: int, title: str) -> str | None:
        status, body = self._req(
            "POST",
            "/api/v1/news/intake",
            {
                "title": f"[PILOT {self.tag}] {title}",
                "summary": "Synthetic pilot item — neutral, not for publication.",
                "category": "markets",
                "priority": "P2",
                "source_url": f"https://pilot.example/{self.tag}/{idx}",
                "source_name": f"Pilot Source {self.tag}-{idx}",
            },
        )
        return body.get("id") if status == 201 and isinstance(body, dict) else None

    def register_source(self, idx: int, s_level: str, source_status: str = "active") -> int:
        trust = TRUST.get(s_level, "T3")
        status, _ = self._req(
            "POST",
            "/api/v1/sources",
            {
                "source_name": f"Pilot Source {self.tag}-{idx}",
                "source_url": f"https://pilot.example/{self.tag}/{idx}",
                "source_type": "news_outlet",
                "source_status": source_status,
                "trust_level": trust,
            },
        )
        return status

    def strong_verification(self, news_id: str, idx: int) -> int:
        status, _ = self._req(
            "POST",
            "/api/v1/verification-records",
            {
                "news_item_id": news_id,
                "verification_status": "verified",
                "evidence_level": "E4",
                "confidence_level": "C4",
                "summary": "Corroborated against two independent primary sources.",
                "verified_claims": ["synthetic claim"],
                "unverified_claims": [],
                "contradictions": [],
                "source_refs": [
                    f"https://pilot.example/{self.tag}/{idx}",
                    f"https://pilot.example/{self.tag}/{idx}-b",
                ],
            },
        )
        return status

    def contradicted_verification(self, news_id: str) -> int:
        status, _ = self._req(
            "POST",
            "/api/v1/verification-records",
            {
                "news_item_id": news_id,
                "verification_status": "verified",
                "evidence_level": "E3",
                "confidence_level": "C3",
                "summary": "Sources disagree on the reported figure.",
                "verified_claims": ["an event occurred"],
                "unverified_claims": [],
                "contradictions": ["Source A says X, source B says Y"],
                "source_refs": ["https://pilot.example/single"],
            },
        )
        return status

    def critical_risk(self, news_id: str) -> int:
        status, _ = self._req(
            "POST",
            "/api/v1/risk-reviews",
            {
                "news_item_id": news_id,
                "entity_type": "news_item",
                "entity_id": news_id,
                "risk_level": "critical",
                "severity": "R-SEV-3",
                "decision_recommendation": "block_publication",
                "risk_flags": ["critical_risk"],
                "summary": "Critical editorial/legal risk.",
                "required_disclaimers": [],
                "language_restrictions": [],
                "human_review_required": True,
                "publication_block_recommended": True,
            },
        )
        return status

    def passing_audit(self, news_id: str) -> int:
        status, _ = self._req(
            "POST",
            "/api/v1/audit/checks",
            {
                "entity_type": "news_item",
                "entity_id": news_id,
                "audit_status": "passed",
                "severity": "medium",
                "decision_recommendation": "allow_to_continue",
                "ready_to_advance": True,
                "publication_block_recommended": False,
                "missing_requirements": [],
                "audit_flags": [],
            },
        )
        return status

    def move_to_reviewing(self, news_id: str) -> bool:
        for st in [
            "registered", "classified", "validating", "verified",
            "prioritized", "drafting", "reviewing",
        ]:
            status, _ = self._req("PATCH", f"/api/v1/news/{news_id}/status", {"status": st})
            if status != 200:
                return False
        return True

    def try_approve(self, news_id: str) -> int:
        status, _ = self._req("PATCH", f"/api/v1/news/{news_id}/status", {"status": "approved"})
        return status

    def calculate_readiness(self, news_id: str) -> dict | None:
        status, body = self._req(
            "POST", f"/api/v1/editorial-readiness/news/{news_id}/calculate"
        )
        return body if status == 201 and isinstance(body, dict) else None


def record(name: str, expected: str, actual: str, ok: bool, critical: bool = False) -> None:
    tag = "CRIT" if (critical and not ok) else ("PASS" if ok else "FAIL")
    RESULTS.append({"name": name, "expected": expected, "actual": actual, "ok": ok})
    print(f"[{tag:4}] {name}", flush=True)
    print(f"         expected: {expected}", flush=True)
    print(f"         actual:   {actual}", flush=True)


def gate_case(c: Client, idx: int, name: str, s_level: str, *, verified: bool,
              source_status: str, expect_approved: bool) -> None:
    """Create a news item + registered source, drive it to reviewing with a passing
    audit, then attempt to approve. expect_approved=False means it MUST be blocked."""
    news_id = c.create_news(idx, name)
    if not news_id:
        record(name, "created", "news intake failed", False, critical=True)
        return
    c.register_source(idx, s_level, source_status)
    if verified:
        c.strong_verification(news_id, idx)
    if not c.move_to_reviewing(news_id):
        record(name, "reach reviewing", "state transition failed", False)
        return
    c.passing_audit(news_id)
    status = c.try_approve(news_id)
    advanced = status == 200
    blocked = status == 409
    ok = advanced if expect_approved else blocked
    exp = "advance to approved (200)" if expect_approved else "BLOCKED at approve (409)"
    act = f"HTTP {status} ({'advanced' if advanced else 'blocked' if blocked else 'unexpected'})"
    # A blocked-expected case that advanced is a fail-closed violation (critical).
    record(name, exp, act, ok, critical=not expect_approved)


def main() -> int:
    parser = argparse.ArgumentParser(description="XMIP controlled newsroom pilot")
    parser.add_argument("--base-url", default="http://127.0.0.1:8010")
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--actor-role", default="admin")
    args = parser.parse_args()

    tag = uuid.uuid4().hex[:6]
    c = Client(args.base_url, args.api_key, args.actor_role, tag)
    print(f"== XMIP controlled newsroom pilot :: run {tag} :: {args.base_url} ==\n", flush=True)

    # --- Publication gate matrix (approve must succeed or be blocked, fail-closed) ---
    gate_case(c, 1, "C1 S1 primary source + audit -> advances", "S1",
              verified=False, source_status="active", expect_approved=True)
    gate_case(c, 2, "C2 S2 trusted media + audit -> advances", "S2",
              verified=False, source_status="active", expect_approved=True)
    gate_case(c, 3, "C3 S3 analyst + STRONG verification -> advances", "S3",
              verified=True, source_status="active", expect_approved=True)
    gate_case(c, 4, "C4 S3 analyst WITHOUT verification -> BLOCKED", "S3",
              verified=False, source_status="active", expect_approved=False)
    gate_case(c, 5, "C5 S4 social unconfirmed -> BLOCKED", "S4",
              verified=False, source_status="active", expect_approved=False)
    gate_case(c, 6, "C6 S4 social + STRONG verification -> advances", "S4",
              verified=True, source_status="active", expect_approved=True)
    gate_case(c, 7, "C7 blocked source -> BLOCKED", "S1",
              verified=True, source_status="blocked", expect_approved=False)
    gate_case(c, 8, "C8 restricted source -> BLOCKED", "S2",
              verified=True, source_status="restricted", expect_approved=False)

    # --- Readiness reflects source quality / conflicts / risk ---
    n9 = c.create_news(9, "C9 S4 weak source readiness")
    if n9:
        c.register_source(9, "S4", "active")
        r = c.calculate_readiness(n9)
        score = r.get("source_score") if r else None
        weak_reflected = r is not None and score is not None and score <= 3
        record("C9 readiness reflects weak S4 source (source_score<=3)",
               "source_score<=3 for S4", f"source_score={score}", weak_reflected, critical=True)

    n10 = c.create_news(10, "C10 contradiction between sources")
    if n10:
        c.contradicted_verification(n10)
        r = c.calculate_readiness(n10)
        warns = " ".join(r.get("warnings", [])) if r else ""
        hr = r.get("human_review_required") if r else None
        ok = r is not None and hr is True and "conflict" in warns
        record("C10 contradictions -> human review + warning",
               "human_review_required + conflict warning",
               f"human_review={hr}, warnings={warns[:50]}", ok)

    n11 = c.create_news(11, "C11 missing evidence")
    if n11:
        r = c.calculate_readiness(n11)
        missing = r.get("missing_requirements", []) if r else []
        score = r.get("score") if r else None
        ok = r is not None and "VerificationRecord" in missing and (score or 100) < 40
        record("C11 no verification -> low readiness + missing VerificationRecord",
               "VerificationRecord missing + score<40",
               f"missing={'VerificationRecord' in missing}, score={score}", ok)

    n12 = c.create_news(12, "C12 critical risk must stay blocked")
    if n12:
        c.critical_risk(n12)
        r = c.calculate_readiness(n12)
        ok = (r is not None and r.get("readiness_status") == "blocked"
              and r.get("publication_block_recommended") is True)
        record("C12 critical risk -> readiness blocked",
               "readiness_status=blocked + publication_block_recommended",
               f"status={r.get('readiness_status') if r else None}, "
               f"block={r.get('publication_block_recommended') if r else None}", ok, critical=True)

    # --- Deduplication ---
    dup_payload = {
        "signal_type": "manual",
        "source_name": f"Pilot Dedup {tag}",
        "source_url": f"https://pilot.example/{tag}/dup",
        "raw_title": f"[PILOT {tag}] Identical synthetic headline for dedup",
        "raw_summary": "Same content submitted twice to exercise deduplication.",
        "topic": "markets",
        "priority": "P3",
        "confidence_level": "IC2",
    }
    c._req("POST", "/api/v1/intake/signals", dup_payload)
    status2, body2 = c._req("POST", "/api/v1/intake/signals", dup_payload)
    dedupe = body2.get("dedupe_status") if isinstance(body2, dict) else None
    ok = dedupe in {"exact_duplicate", "probable_duplicate"}
    record("C13 duplicate signal flagged by dedup",
           "dedupe_status in {exact_duplicate, probable_duplicate}",
           f"dedupe_status={dedupe}", ok)

    # --- Operational audit coverage (P8.1): transitions + source registration ---
    _, trans = c._req(
        "GET", "/api/v1/operational-audit/events?action=news.status.transition&limit=200"
    )
    n_trans = len(trans) if isinstance(trans, list) else -1
    record("C14 audit log covers NewsItem status transitions",
           "news.status.transition events >= 8", f"count={n_trans}", n_trans >= 8)
    _, srcs = c._req(
        "GET", "/api/v1/operational-audit/events?action=source.register&limit=200"
    )
    n_srcs = len(srcs) if isinstance(srcs, list) else -1
    record("C15 audit log covers SourceReference registration",
           "source.register events >= 8", f"count={n_srcs}", n_srcs >= 8)

    # --- Summary ---
    total = len(RESULTS)
    passed = sum(1 for r in RESULTS if r["ok"])
    failed = total - passed
    print(f"\n== resumen :: {passed}/{total} PASS, {failed} FAIL ==", flush=True)
    if failed:
        print("RESULTADO: FAIL — casos FAIL/CRIT (posible gate abierto)", flush=True)
        return 1
    print("RESULTADO: PASS — todos los casos piloto se comportaron fail-closed", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
