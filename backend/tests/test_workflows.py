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


async def start_workflow(client, news_id: str, **headers) -> dict:
    response = await client.post(
        f"/api/v1/workflows/news/{news_id}/start",
        json={"workflow_type": "editorial_pipeline"},
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()


async def create_verification_record(client, news_id: str, status: str = "verified") -> dict:
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
            "decision_recommendation": "block_publication"
            if publication_block_recommended
            else "allow_with_minor_edits",
            "risk_flags": [],
            "summary": "Risk reviewed.",
            "required_disclaimers": [],
            "language_restrictions": [],
            "publication_block_recommended": publication_block_recommended,
        },
    )
    assert response.status_code == 201
    return response.json()


async def create_content_piece(client, news_id: str, status: str = "drafting") -> dict:
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


async def create_audit_check(client, news_id: str, publication_block: bool = False) -> dict:
    response = await client.post(
        "/api/v1/audit/checks",
        json={
            "entity_type": "news_item",
            "entity_id": news_id,
            "audit_status": "passed",
            "severity": "medium",
            "decision_recommendation": "allow_to_continue",
            "ready_to_advance": not publication_block,
            "publication_block_recommended": publication_block,
            "missing_requirements": [],
            "audit_flags": [],
        },
    )
    assert response.status_code == 201
    return response.json()


async def create_distribution_plan(
    client,
    news_id: str,
    content_piece_id: str,
    status: str,
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
    status: str = "scheduled",
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


async def recalculate_workflow(client, workflow_id: str) -> dict:
    response = await client.post(f"/api/v1/workflows/{workflow_id}/recalculate")
    assert response.status_code == 200
    return response.json()


async def test_create_workflow_for_existing_news_item(client):
    news = await create_news_item(client)

    workflow = await start_workflow(client, news["id"])

    assert workflow["news_item_id"] == news["id"]
    assert workflow["current_step"] == "verification"
    assert workflow["missing_requirements"] == ["VerificationRecord"]
    assert len(workflow["steps"]) == 11


async def test_start_workflow_blocks_missing_news_item(client):
    response = await client.post(
        "/api/v1/workflows/news/missing-news/start",
        json={"workflow_type": "editorial_pipeline"},
    )

    assert response.status_code == 404


async def test_list_workflows(client):
    news = await create_news_item(client)
    await start_workflow(client, news["id"])

    response = await client.get("/api/v1/workflows")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_workflow_by_id(client):
    news = await create_news_item(client)
    workflow = await start_workflow(client, news["id"])

    response = await client.get(f"/api/v1/workflows/{workflow['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == workflow["id"]


async def test_get_workflow_by_news_id(client):
    news = await create_news_item(client)
    workflow = await start_workflow(client, news["id"])

    response = await client.get(f"/api/v1/news/{news['id']}/workflow")

    assert response.status_code == 200
    assert response.json()["id"] == workflow["id"]


async def test_initial_workflow_detects_missing_verification_record(client):
    news = await create_news_item(client)
    workflow = await start_workflow(client, news["id"])

    assert workflow["current_step"] == "verification"
    assert workflow["next_agent"] == "SourceValidatorAgent"


async def test_workflow_recalculate_after_verification_detects_missing_risk_review(client):
    news = await create_news_item(client)
    workflow = await start_workflow(client, news["id"])
    await create_verification_record(client, news["id"])

    updated = await recalculate_workflow(client, workflow["id"])

    assert updated["current_step"] == "risk_review"
    assert updated["missing_requirements"] == ["RiskReview"]
    assert updated["next_agent"] == "RiskAgent"


async def test_workflow_blocks_risk_review_publication_block(client):
    news = await create_news_item(client)
    workflow = await start_workflow(client, news["id"])
    await create_verification_record(client, news["id"])
    await create_risk_review(client, news["id"], publication_block_recommended=True)

    updated = await recalculate_workflow(client, workflow["id"])

    assert updated["blocked"] is True
    assert updated["current_step"] == "risk_review"


async def test_workflow_detects_missing_content_piece(client):
    news = await create_news_item(client)
    workflow = await start_workflow(client, news["id"])
    await create_verification_record(client, news["id"])
    await create_risk_review(client, news["id"])

    updated = await recalculate_workflow(client, workflow["id"])

    assert updated["current_step"] == "content_creation"
    assert updated["missing_requirements"] == ["ContentPiece"]


async def test_workflow_detects_missing_audit_check(client):
    news = await create_news_item(client)
    workflow = await start_workflow(client, news["id"])
    await create_verification_record(client, news["id"])
    await create_risk_review(client, news["id"])
    await create_content_piece(client, news["id"])

    updated = await recalculate_workflow(client, workflow["id"])

    assert updated["current_step"] == "audit_review"
    assert updated["missing_requirements"] == ["AuditCheck"]


async def test_workflow_detects_missing_distribution_plan(client):
    news = await create_news_item(client)
    workflow = await start_workflow(client, news["id"])
    await create_verification_record(client, news["id"])
    await create_risk_review(client, news["id"])
    await create_content_piece(client, news["id"], status="approved")
    await create_audit_check(client, news["id"])

    updated = await recalculate_workflow(client, workflow["id"])

    assert updated["current_step"] == "distribution_planning"
    assert updated["missing_requirements"] == ["DistributionPlan"]


async def test_workflow_detects_missing_publication_record(client):
    news = await create_news_item(client)
    workflow = await start_workflow(client, news["id"])
    await create_verification_record(client, news["id"])
    await create_risk_review(client, news["id"])
    piece = await create_content_piece(client, news["id"], status="approved")
    await create_audit_check(client, news["id"])
    await create_distribution_plan(client, news["id"], piece["id"], status="scheduled")

    updated = await recalculate_workflow(client, workflow["id"])

    assert updated["current_step"] == "publication"
    assert updated["missing_requirements"] == ["PublicationRecord"]


async def test_workflow_reaches_measurement_when_publication_is_published(client):
    news = await create_news_item(client)
    workflow = await start_workflow(client, news["id"])
    await create_verification_record(client, news["id"])
    await create_risk_review(client, news["id"])
    piece = await create_content_piece(client, news["id"], status="approved")
    await create_audit_check(client, news["id"])
    plan = await create_distribution_plan(client, news["id"], piece["id"], status="scheduled")
    await create_publication_record(client, news["id"], piece["id"], plan["id"], status="published")

    updated = await recalculate_workflow(client, workflow["id"])

    assert updated["current_step"] == "measurement"
    assert updated["readiness_status"] == "completed"
    assert updated["next_agent"] == "MetricsAgent"


async def test_recalculate_updates_missing_requirements(client):
    news = await create_news_item(client)
    workflow = await start_workflow(client, news["id"])
    assert workflow["missing_requirements"] == ["VerificationRecord"]

    await create_verification_record(client, news["id"])
    updated = await recalculate_workflow(client, workflow["id"])

    assert updated["missing_requirements"] == ["RiskReview"]


async def test_advance_blocks_when_dependencies_are_missing(client):
    news = await create_news_item(client)
    workflow = await start_workflow(client, news["id"])

    response = await client.post(f"/api/v1/workflows/{workflow['id']}/advance")

    assert response.status_code == 409


async def test_correlation_id_persisted_from_header(client):
    news = await create_news_item(client)

    workflow = await start_workflow(
        client,
        news["id"],
        **{"X-Correlation-ID": "corr-workflow-001"},
    )

    assert workflow["correlation_id"] == "corr-workflow-001"
    assert {step["correlation_id"] for step in workflow["steps"]} == {"corr-workflow-001"}


async def test_auth_protects_workflow_start(client, monkeypatch):
    news = await create_news_item(client)
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.post(
        f"/api/v1/workflows/news/{news['id']}/start",
        json={"workflow_type": "editorial_pipeline"},
    )

    assert response.status_code == 401


async def test_auth_protects_workflow_recalculate(client, monkeypatch):
    news = await create_news_item(client)
    workflow = await start_workflow(client, news["id"])
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.post(f"/api/v1/workflows/{workflow['id']}/recalculate")

    assert response.status_code == 401


async def test_auth_protects_workflow_advance(client, monkeypatch):
    news = await create_news_item(client)
    workflow = await start_workflow(client, news["id"])
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.post(f"/api/v1/workflows/{workflow['id']}/advance")

    assert response.status_code == 401
