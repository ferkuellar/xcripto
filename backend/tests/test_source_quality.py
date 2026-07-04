"""SOURCE_QUALITY_POLICY enforcement (niveles S1-S5).

Cubre la política pura (`app.core.source_quality`) y su integración en el gate de
publicación (`news_service.update_news_status`) y en el readiness editorial.
"""

from types import SimpleNamespace

from app.core.source_quality import (
    evaluate_publication_source_gate,
    is_disqualified,
    is_strong_verification,
    readiness_score_for_source,
    source_level_for,
)

# --- Fakes ligeros (el módulo es duck-typed y no toca la base de datos) ---


def _source(trust_level="T1", source_status="active", source_name="Example Wire"):
    return SimpleNamespace(
        trust_level=trust_level,
        source_status=source_status,
        source_name=source_name,
    )


def _verification(
    verification_status="verified",
    evidence_level="E3",
    source_refs=("a", "b"),
    contradictions=(),
):
    return SimpleNamespace(
        verification_status=verification_status,
        evidence_level=evidence_level,
        source_refs=list(source_refs),
        contradictions=list(contradictions),
    )


# --- Política pura: mapeo de niveles ---


def test_trust_level_maps_to_source_level():
    assert source_level_for(_source(trust_level="T0")) == "S1"
    assert source_level_for(_source(trust_level="T1")) == "S2"
    assert source_level_for(_source(trust_level="T2")) == "S3"
    assert source_level_for(_source(trust_level="T3")) == "S4"


def test_unknown_trust_level_fails_closed_to_s5():
    assert source_level_for(_source(trust_level="T9")) == "S5"


def test_blocked_and_restricted_sources_are_disqualified():
    assert is_disqualified(_source(source_status="blocked")) is True
    assert is_disqualified(_source(source_status="restricted")) is True
    assert is_disqualified(_source(source_status="active")) is False


def test_readiness_score_scales_with_level():
    assert readiness_score_for_source(_source(trust_level="T0")) == 10.0
    assert readiness_score_for_source(_source(trust_level="T1")) == 9.0
    assert readiness_score_for_source(_source(trust_level="T2")) == 7.0
    assert readiness_score_for_source(_source(trust_level="T3")) == 3.0


def test_disqualified_source_scores_zero_regardless_of_level():
    assert readiness_score_for_source(_source(trust_level="T0", source_status="blocked")) == 0.0


# --- Política pura: verificación fuerte ---


def test_strong_verification_requires_verified_status():
    assert is_strong_verification(None) is False
    assert is_strong_verification(_verification(verification_status="partially_verified")) is False


def test_strong_verification_needs_evidence_or_multiple_sources():
    strong_evidence = _verification(evidence_level="E3", source_refs=())
    multiple_sources = _verification(evidence_level="E1", source_refs=("a", "b"))
    weak = _verification(evidence_level="E1", source_refs=("a",))
    assert is_strong_verification(strong_evidence) is True
    assert is_strong_verification(multiple_sources) is True
    assert is_strong_verification(weak) is False


def test_contradictions_break_strong_verification():
    assert is_strong_verification(_verification(contradictions=("price mismatch",))) is False


# --- Política pura: gate de publicación ---


def test_gate_allows_missing_source_reference():
    # Sin fuente registrada delega en el gate de AuditCheck; no bloquea aquí.
    assert evaluate_publication_source_gate(None, verification_strong=False) == []


def test_gate_allows_primary_and_trusted_sources():
    for trust_level in ("T0", "T1"):  # S1, S2
        gate = evaluate_publication_source_gate(
            _source(trust_level=trust_level), verification_strong=False
        )
        assert gate == []


def test_gate_blocks_disqualified_source():
    reasons = evaluate_publication_source_gate(
        _source(trust_level="T0", source_status="blocked"), verification_strong=True
    )
    assert reasons and "blocked" in reasons[0]


def test_gate_blocks_s5_source_unconditionally():
    reasons = evaluate_publication_source_gate(
        _source(trust_level="T9"), verification_strong=True
    )
    assert reasons and "S5" in reasons[0]


def test_gate_blocks_s4_without_strong_verification():
    reasons = evaluate_publication_source_gate(
        _source(trust_level="T3"), verification_strong=False
    )
    assert reasons and "S4" in reasons[0]


def test_gate_allows_s4_with_strong_verification():
    gate = evaluate_publication_source_gate(_source(trust_level="T3"), verification_strong=True)
    assert gate == []


def test_gate_blocks_s3_without_strong_verification():
    reasons = evaluate_publication_source_gate(
        _source(trust_level="T2"), verification_strong=False
    )
    assert reasons and "S3" in reasons[0]


# --- Integración: gate de publicación en update_news_status ---

NEWS_PAYLOAD = {
    "title": "Bitcoin ETF sees record inflows",
    "summary": "Institutional inflows into spot BTC ETFs reached a new daily record.",
    "category": "markets",
    "priority": "P1",
    "source_url": "https://example.com/etf-inflows",
    "source_name": "Example Wire",
}

VALID_AUDIT_PAYLOAD = {
    "entity_type": "news_item",
    "entity_id": "placeholder",
    "audit_status": "passed",
    "severity": "medium",
    "decision_recommendation": "allow_to_continue",
    "ready_to_advance": True,
    "publication_block_recommended": False,
    "missing_requirements": [],
    "audit_flags": [],
}


async def _create_news(client) -> dict:
    response = await client.post("/api/v1/news/intake", json=NEWS_PAYLOAD)
    assert response.status_code == 201
    return response.json()


async def _register_source(client, *, trust_level="T1", source_status="active") -> dict:
    response = await client.post(
        "/api/v1/sources",
        json={
            "source_name": NEWS_PAYLOAD["source_name"],
            "source_url": NEWS_PAYLOAD["source_url"],
            "source_type": "news_outlet",
            "source_status": source_status,
            "trust_level": trust_level,
        },
    )
    assert response.status_code == 201
    return response.json()


async def _create_verification(client, news_id: str) -> dict:
    response = await client.post(
        "/api/v1/verification-records",
        json={
            "news_item_id": news_id,
            "verification_status": "verified",
            "evidence_level": "E4",
            "confidence_level": "C4",
            "summary": "Corroborated against two independent primary sources.",
            "verified_claims": ["ETF inflows increased"],
            "unverified_claims": [],
            "contradictions": [],
            "source_refs": [
                "https://example.com/etf-inflows",
                "https://sec.gov/filing",
            ],
        },
    )
    assert response.status_code == 201
    return response.json()


async def _move_to_reviewing(client, news_id: str) -> None:
    for status in [
        "registered",
        "classified",
        "validating",
        "verified",
        "prioritized",
        "drafting",
        "reviewing",
    ]:
        response = await client.patch(
            f"/api/v1/news/{news_id}/status", json={"status": status}
        )
        assert response.status_code == 200


async def _pass_audit(client, news_id: str) -> None:
    payload = {**VALID_AUDIT_PAYLOAD, "entity_id": news_id}
    response = await client.post("/api/v1/audit/checks", json=payload)
    assert response.status_code == 201


async def _approve(client, news_id: str):
    return await client.patch(f"/api/v1/news/{news_id}/status", json={"status": "approved"})


async def test_approve_blocked_by_s4_source_without_verification(client):
    news = await _create_news(client)
    await _register_source(client, trust_level="T3")  # S4
    await _move_to_reviewing(client, news["id"])
    await _pass_audit(client, news["id"])

    response = await _approve(client, news["id"])

    assert response.status_code == 409
    assert "level S4" in response.json()["error"]
    assert "SOURCE_QUALITY_POLICY" in response.json()["error"]


async def test_approve_allowed_for_s4_source_with_strong_verification(client):
    news = await _create_news(client)
    await _register_source(client, trust_level="T3")  # S4
    await _create_verification(client, news["id"])  # verified + 2 refs => strong
    await _move_to_reviewing(client, news["id"])
    await _pass_audit(client, news["id"])

    response = await _approve(client, news["id"])

    assert response.status_code == 200
    assert response.json()["status"] == "approved"


async def test_approve_blocked_by_blocked_source(client):
    news = await _create_news(client)
    await _register_source(client, trust_level="T0", source_status="blocked")
    await _move_to_reviewing(client, news["id"])
    await _pass_audit(client, news["id"])

    response = await _approve(client, news["id"])

    assert response.status_code == 409
    assert "blocked" in response.json()["error"]


async def test_approve_allowed_for_primary_source(client):
    news = await _create_news(client)
    await _register_source(client, trust_level="T0")  # S1
    await _move_to_reviewing(client, news["id"])
    await _pass_audit(client, news["id"])

    response = await _approve(client, news["id"])

    assert response.status_code == 200
    assert response.json()["status"] == "approved"


async def test_approve_allowed_without_registered_source(client):
    # Comportamiento heredado: sin SourceReference registrada, gobierna el audit.
    news = await _create_news(client)
    await _move_to_reviewing(client, news["id"])
    await _pass_audit(client, news["id"])

    response = await _approve(client, news["id"])

    assert response.status_code == 200


# --- Integración: calidad de fuente visible en el readiness ---


async def _calculate(client, news_id: str) -> dict:
    response = await client.post(
        f"/api/v1/editorial-readiness/news/{news_id}/calculate"
    )
    assert response.status_code == 201
    return response.json()


async def test_readiness_surfaces_source_level(client):
    news = await _create_news(client)
    await _register_source(client, trust_level="T0")  # S1

    score = await _calculate(client, news["id"])

    assert score["source_score"] == 10
    assert score["score_payload"]["components"]["source"]["source_level"] == "S1"


async def test_readiness_blocks_on_disqualified_source(client):
    news = await _create_news(client)
    await _register_source(client, trust_level="T0", source_status="blocked")

    score = await _calculate(client, news["id"])

    assert score["score_band"] == "blocked"
    assert score["readiness_status"] == "blocked"
    assert score["publication_block_recommended"] is True


async def test_readiness_warns_on_source_contradictions(client):
    news = await _create_news(client)
    response = await client.post(
        "/api/v1/verification-records",
        json={
            "news_item_id": news["id"],
            "verification_status": "verified",
            "evidence_level": "E3",
            "confidence_level": "C3",
            "summary": "Verified but sources disagree on the amount.",
            "verified_claims": ["A hack occurred"],
            "unverified_claims": [],
            "contradictions": ["Source A says $10M, source B says $2M"],
            "source_refs": ["https://example.com/etf-inflows"],
        },
    )
    assert response.status_code == 201

    score = await _calculate(client, news["id"])

    assert any("conflict" in w for w in score["warnings"])
    assert score["human_review_required"] is True
