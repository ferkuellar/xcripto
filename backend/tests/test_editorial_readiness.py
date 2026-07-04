from app.core.config import get_settings

NEWS_PAYLOAD = {
    "title": "Bitcoin ETF sees record inflows",
    "summary": "Institutional inflows into spot BTC ETFs reached a new daily record.",
    "category": "markets",
    "priority": "P1",
    "source_url": "https://example.com/etf-inflows",
    "source_name": "Example Wire",
}


async def create_news_item(client) -> dict:
    response = await client.post("/api/v1/news/intake", json=NEWS_PAYLOAD)
    assert response.status_code == 201
    return response.json()


async def calculate_score(client, news_id: str, **headers) -> dict:
    response = await client.post(
        f"/api/v1/editorial-readiness/news/{news_id}/calculate",
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()


async def create_workflow(client, news_id: str) -> dict:
    response = await client.post(
        f"/api/v1/workflows/news/{news_id}/start",
        json={"workflow_type": "editorial_pipeline"},
    )
    assert response.status_code == 201
    return response.json()


async def create_verification(client, news_id: str, status: str = "verified") -> dict:
    response = await client.post(
        "/api/v1/verification-records",
        json={
            "news_item_id": news_id,
            "verification_status": status,
            "evidence_level": "E3",
            "confidence_level": "C4",
            "summary": "Verified against source material.",
            "verified_claims": ["ETF inflows increased"],
            "unverified_claims": [],
            "contradictions": [],
            "source_refs": ["https://example.com/etf-inflows"],
        },
    )
    assert response.status_code == 201
    return response.json()


async def create_risk_review(
    client,
    news_id: str,
    risk_level: str = "medium",
    decision_recommendation: str = "allow_with_minor_edits",
    publication_block_recommended: bool = False,
) -> dict:
    response = await client.post(
        "/api/v1/risk-reviews",
        json={
            "news_item_id": news_id,
            "entity_type": "news_item",
            "entity_id": news_id,
            "risk_level": risk_level,
            "severity": "R-SEV-1",
            "decision_recommendation": decision_recommendation,
            "risk_flags": [],
            "summary": "Risk reviewed.",
            "required_disclaimers": [],
            "language_restrictions": [],
            "human_review_required": risk_level in {"high", "critical"},
            "publication_block_recommended": publication_block_recommended,
        },
    )
    assert response.status_code == 201
    return response.json()


async def create_content_piece(client, news_id: str, status: str = "approved") -> dict:
    response = await client.post(
        "/api/v1/content-pieces",
        json={
            "news_item_id": news_id,
            "content_type": "news_article",
            "title": "Bitcoin ETF inflows hit new record",
            "summary": "A concise editorial summary.",
            "body": "Institutional inflows reached a record.",
            "status": status,
            "category": "markets",
            "priority": "P1",
            "verification_status": "verified",
            "risk_level": "medium",
            "source_refs": ["https://example.com/etf-inflows"],
        },
    )
    assert response.status_code == 201
    return response.json()


async def create_audit_check(client, news_id: str, status: str = "passed") -> dict:
    response = await client.post(
        "/api/v1/audit/checks",
        json={
            "entity_type": "news_item",
            "entity_id": news_id,
            "audit_status": status,
            "severity": "medium",
            "decision_recommendation": "allow_to_continue",
            "ready_to_advance": True,
            "publication_block_recommended": False,
            "missing_requirements": [],
            "audit_flags": [],
        },
    )
    assert response.status_code == 201
    return response.json()


async def create_distribution_plan(
    client, news_id: str, content_piece_id: str, status: str = "scheduled"
) -> dict:
    response = await client.post(
        "/api/v1/distribution-plans",
        json={
            "content_piece_id": content_piece_id,
            "news_item_id": news_id,
            "primary_channel": "Blog / Web",
            "secondary_channels": ["LinkedIn"],
            "distribution_type": "primary_publication",
            "status": status,
            "dependencies": [],
            "metric_plan": {"primary_metric": "views"},
            "risk_level": "medium",
            "publication_readiness": "ready",
        },
    )
    assert response.status_code == 201
    return response.json()


async def create_publication_record(
    client,
    news_id: str,
    content_piece_id: str,
    distribution_plan_id: str,
    status: str = "published",
) -> dict:
    payload = {
        "content_piece_id": content_piece_id,
        "distribution_plan_id": distribution_plan_id,
        "news_item_id": news_id,
        "channel": "Blog / Web",
        "publication_status": status,
    }
    if status == "published":
        payload["published_url"] = "https://example.com/published/story"
    response = await client.post("/api/v1/publication-records", json=payload)
    assert response.status_code == 201
    return response.json()


async def test_calculate_score_for_existing_news_item(client):
    news = await create_news_item(client)

    score = await calculate_score(client, news["id"])

    assert score["news_item_id"] == news["id"]
    assert score["score"] >= 0
    assert score["calculated_by"] == "system"


async def test_calculate_score_blocks_missing_news_item(client):
    response = await client.post("/api/v1/editorial-readiness/news/missing-news/calculate")

    assert response.status_code == 404


async def test_score_without_verification_is_low_and_missing_verification(client):
    news = await create_news_item(client)

    score = await calculate_score(client, news["id"])

    assert score["score"] < 40
    assert "VerificationRecord" in score["missing_requirements"]


async def test_score_with_verified_record_increases_verification_score(client):
    news = await create_news_item(client)
    await create_verification(client, news["id"])

    score = await calculate_score(client, news["id"])

    assert score["verification_score"] == 20


async def test_score_with_critical_risk_is_blocked(client):
    news = await create_news_item(client)
    await create_verification(client, news["id"])
    await create_risk_review(
        client,
        news["id"],
        risk_level="critical",
        decision_recommendation="block_publication",
        publication_block_recommended=True,
    )

    score = await calculate_score(client, news["id"])

    assert score["score_band"] == "blocked"
    assert score["readiness_status"] == "blocked"
    assert score["publication_block_recommended"] is True


async def test_score_with_valid_audit_check_increases_audit_score(client):
    news = await create_news_item(client)
    await create_audit_check(client, news["id"])

    score = await calculate_score(client, news["id"])

    assert score["audit_score"] == 15


async def test_score_with_approved_content_increases_editorial_score(client):
    news = await create_news_item(client)
    await create_content_piece(client, news["id"], status="approved")

    score = await calculate_score(client, news["id"])

    assert score["editorial_score"] == 10


async def test_score_with_scheduled_distribution_increases_distribution_score(client):
    news = await create_news_item(client)
    piece = await create_content_piece(client, news["id"], status="approved")
    await create_distribution_plan(client, news["id"], piece["id"], status="scheduled")

    score = await calculate_score(client, news["id"])

    assert score["distribution_score"] == 5


async def test_score_with_published_publication_marks_published(client):
    news = await create_news_item(client)
    piece = await create_content_piece(client, news["id"], status="approved")
    plan = await create_distribution_plan(client, news["id"], piece["id"], status="scheduled")
    await create_publication_record(client, news["id"], piece["id"], plan["id"], status="published")

    score = await calculate_score(client, news["id"])

    assert score["publication_score"] == 5
    assert score["readiness_status"] == "published"


async def test_score_with_blocking_workflow_task_is_blocked(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    task_response = await client.post(
        "/api/v1/workflow-tasks",
        json={
            "workflow_run_id": workflow["id"],
            "news_item_id": news["id"],
            "task_type": "manual_review",
            "task_status": "blocked",
            "priority": "P1",
            "assigned_agent": "HumanEditor",
            "title": "Manual review",
            "description": "Resolve verification conflict.",
            "blocking": True,
            "blocking_reason": "Verification conflict",
        },
    )
    assert task_response.status_code == 201

    score = await calculate_score(client, news["id"])

    assert score["score_band"] == "blocked"
    assert "Verification conflict" in score["blocking_reasons"]


async def test_score_with_critical_agent_output_pending_is_blocked(client):
    news = await create_news_item(client)
    response = await client.post(
        "/api/v1/agent-outputs",
        json={
            "agent_name": "RiskAgent",
            "output_type": "risk_review",
            "news_item_id": news["id"],
            "summary": "Potential financial advice risk.",
            "payload": {"risk": "financial_advice"},
            "risk_flags": ["financial_advice_risk"],
        },
    )
    assert response.status_code == 201

    score = await calculate_score(client, news["id"])

    assert score["score_band"] == "blocked"
    assert score["human_review_required"] is True


async def test_score_with_metric_snapshot_adds_metrics_score(client):
    news = await create_news_item(client)
    response = await client.post(
        "/api/v1/metric-snapshots",
        json={
            "news_item_id": news["id"],
            "metric_category": "publication_metrics",
            "measurement_window": "24h",
            "metric_name": "views",
            "metric_value": 1200,
            "source_or_origin": "manual capture",
            "data_quality": "high",
        },
    )
    assert response.status_code == 201

    score = await calculate_score(client, news["id"])

    assert score["metrics_score"] == 2


async def test_score_with_approved_memory_adds_memory_score_without_source_use(client):
    news = await create_news_item(client)
    memory = await client.post(
        "/api/v1/memory-items",
        json={
            "memory_type": "editorial_memory",
            "memory_status": "approved",
            "title": "Second source rule",
            "memory_statement": "Critical claims need a second source.",
            "source_or_origin": "editorial review",
            "news_item_id": news["id"],
            "confidence_level": "MC3",
            "persistence_level": "M2",
            "scope": "project_wide",
            "expiration_recommendation": "review_quarterly",
        },
    )
    assert memory.status_code == 201

    score = await calculate_score(client, news["id"])

    assert score["memory_score"] == 2
    assert score["source_score"] == 5


async def test_score_with_knowledge_adds_knowledge_score(client):
    news = await create_news_item(client)
    node = await client.post(
        "/api/v1/knowledge/nodes",
        json={
            "node_type": "NewsItem",
            "label": "ETF inflow signal",
            "entity_type": "news_item",
            "entity_id": news["id"],
            "confidence_level": "KC3",
            "status": "approved",
            "source_or_origin": "editorial system",
        },
    )
    assert node.status_code == 201
    other = await client.post(
        "/api/v1/knowledge/nodes",
        json={
            "node_type": "Topic",
            "label": "Bitcoin ETF",
            "confidence_level": "KC3",
            "status": "approved",
            "source_or_origin": "editorial system",
        },
    )
    assert other.status_code == 201
    edge = await client.post(
        "/api/v1/knowledge/edges",
        json={
            "source_node_id": node.json()["id"],
            "target_node_id": other.json()["id"],
            "relationship_type": "related_to",
            "scope": "editorial_context",
            "confidence_level": "KC3",
            "reason": "News item relates to ETF topic.",
            "status": "approved",
        },
    )
    assert edge.status_code == 201

    score = await calculate_score(client, news["id"])

    assert score["knowledge_score"] == 1


async def test_get_latest_returns_most_recent_score(client):
    news = await create_news_item(client)
    first = await calculate_score(client, news["id"])
    await create_verification(client, news["id"])
    second = await calculate_score(client, news["id"])

    response = await client.get(f"/api/v1/editorial-readiness/news/{news['id']}/latest")

    assert response.status_code == 200
    assert response.json()["id"] == second["id"]
    assert response.json()["id"] != first["id"]


async def test_explain_calculates_without_persisting_score(client):
    news = await create_news_item(client)
    saved = await calculate_score(client, news["id"])

    response = await client.get(f"/api/v1/editorial-readiness/news/{news['id']}/explain")
    latest = await client.get(f"/api/v1/editorial-readiness/news/{news['id']}/latest")

    assert response.status_code == 200
    assert response.json()["id"] == "not-persisted"
    assert latest.json()["id"] == saved["id"]


async def test_list_filters_by_score_band(client):
    news = await create_news_item(client)
    score = await calculate_score(client, news["id"])

    response = await client.get(
        "/api/v1/editorial-readiness",
        params={"score_band": score["score_band"]},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_list_filters_by_readiness_status(client):
    news = await create_news_item(client)
    score = await calculate_score(client, news["id"])

    response = await client.get(
        "/api/v1/editorial-readiness",
        params={"readiness_status": score["readiness_status"]},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_list_filters_by_next_agent(client):
    news = await create_news_item(client)
    score = await calculate_score(client, news["id"])

    response = await client.get(
        "/api/v1/editorial-readiness",
        params={"next_agent": score["next_agent"]},
    )

    assert response.status_code == 200
    assert response.json()[0]["next_agent"] == score["next_agent"]


async def test_list_filters_by_human_review_required(client):
    news = await create_news_item(client)
    await client.post(
        "/api/v1/agent-outputs",
        json={
            "agent_name": "RiskAgent",
            "output_type": "risk_review",
            "news_item_id": news["id"],
            "summary": "Critical risk needs review.",
            "payload": {"risk": "critical"},
            "risk_flags": ["critical_risk"],
        },
    )
    score = await calculate_score(client, news["id"])

    response = await client.get(
        "/api/v1/editorial-readiness",
        params={"human_review_required": True},
    )

    assert response.status_code == 200
    assert response.json()[0]["id"] == score["id"]


async def test_list_filters_by_publication_block_recommended(client):
    news = await create_news_item(client)
    await create_risk_review(
        client,
        news["id"],
        risk_level="critical",
        decision_recommendation="block_publication",
        publication_block_recommended=True,
    )
    score = await calculate_score(client, news["id"])

    response = await client.get(
        "/api/v1/editorial-readiness",
        params={"publication_block_recommended": True},
    )

    assert response.status_code == 200
    assert response.json()[0]["id"] == score["id"]


async def test_get_score_by_id(client):
    news = await create_news_item(client)
    score = await calculate_score(client, news["id"])

    response = await client.get(f"/api/v1/editorial-readiness/{score['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == score["id"]


async def test_correlation_id_persisted_from_header(client):
    news = await create_news_item(client)

    score = await calculate_score(client, news["id"], **{"X-Correlation-ID": "corr-ready-001"})

    assert score["correlation_id"] == "corr-ready-001"


async def test_auth_protects_calculate(client, monkeypatch):
    news = await create_news_item(client)
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.post(f"/api/v1/editorial-readiness/news/{news['id']}/calculate")

    assert response.status_code == 401


# --- Regression: calculate must not use a stale workflow snapshot (P1 fix #1) ---


async def test_calculate_refreshes_stale_workflow_requirements(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    assert "VerificationRecord" in workflow["missing_requirements"]

    await create_verification(client, news["id"])
    # Sin recalcular el workflow manualmente: calculate debe refrescarlo solo.
    score = await calculate_score(client, news["id"])

    assert "VerificationRecord" not in score["missing_requirements"]
    assert score["verification_score"] > 0


async def test_calculate_without_workflow_still_works(client):
    news = await create_news_item(client)
    await create_verification(client, news["id"])

    score = await calculate_score(client, news["id"])

    assert score["workflow_run_id"] is None
    assert "VerificationRecord" not in score["missing_requirements"]


async def test_calculate_with_blocked_workflow_keeps_real_blockers(client):
    news = await create_news_item(client)
    await create_workflow(client, news["id"])
    await create_verification(client, news["id"])
    await create_risk_review(
        client,
        news["id"],
        risk_level="critical",
        decision_recommendation="block_publication",
        publication_block_recommended=True,
    )

    score = await calculate_score(client, news["id"])

    assert score["readiness_status"] == "blocked"
    assert score["blocking_reasons"]
