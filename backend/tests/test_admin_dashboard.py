from app.core.config import get_settings

NEWS_PAYLOAD = {
    "title": "Bitcoin ETF sees record inflows",
    "summary": "Institutional inflows into spot BTC ETFs reached a new daily record.",
    "category": "markets",
    "priority": "P1",
    "source_url": "https://example.com/etf-inflows",
    "source_name": "Example Wire",
}


def enable_auth(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")


def auth_headers(role: str = "admin") -> dict[str, str]:
    return {"X-API-Key": "dev-secret", "X-Actor-Role": role}


async def create_news(client, **overrides) -> dict:
    response = await client.post("/api/v1/news/intake", json={**NEWS_PAYLOAD, **overrides})
    assert response.status_code == 201
    return response.json()


async def create_signal(client, **overrides) -> dict:
    payload = {
        "signal_type": "manual",
        "source_name": "Example Wire",
        "source_url": "https://example.com/signal",
        "raw_title": "Signal pending",
        "raw_summary": "Signal summary",
        "topic": "markets",
        "priority": "P1",
        **overrides,
    }
    response = await client.post("/api/v1/intake/signals", json=payload)
    assert response.status_code == 201
    return response.json()


async def create_workflow(client, news_id: str) -> dict:
    response = await client.post(
        f"/api/v1/workflows/news/{news_id}/start",
        json={"workflow_type": "editorial_pipeline"},
    )
    assert response.status_code == 201
    return response.json()


async def create_task(client, workflow_id: str, news_id: str, **overrides) -> dict:
    payload = {
        "workflow_run_id": workflow_id,
        "news_item_id": news_id,
        "task_type": "manual_review",
        "task_status": "queued",
        "priority": "P1",
        "assigned_agent": "HumanEditor",
        "title": "Review item",
        "description": "Review editorial state.",
        **overrides,
    }
    response = await client.post("/api/v1/workflow-tasks", json=payload)
    assert response.status_code == 201
    return response.json()


async def create_user(client, **overrides) -> dict:
    payload = {
        "email": "admin-board@example.com",
        "display_name": "Admin Board",
        "handle": "admin_board",
        "role": "editor",
        **overrides,
    }
    response = await client.post("/api/v1/users", json=payload)
    assert response.status_code == 201
    return response.json()


async def create_content_and_plan(client, news_id: str) -> tuple[dict, dict]:
    piece = await client.post(
        "/api/v1/content-pieces",
        json={
            "news_item_id": news_id,
            "content_type": "news_article",
            "title": "Publication item",
            "summary": "Summary",
            "body": "Body",
            "status": "approved",
            "category": "markets",
            "priority": "P1",
            "verification_status": "verified",
            "risk_level": "medium",
            "source_refs": ["https://example.com/etf-inflows"],
        },
    )
    assert piece.status_code == 201
    plan = await client.post(
        "/api/v1/distribution-plans",
        json={
            "content_piece_id": piece.json()["id"],
            "news_item_id": news_id,
            "primary_channel": "Blog / Web",
            "secondary_channels": [],
            "distribution_type": "primary_publication",
            "status": "scheduled",
            "dependencies": [],
            "metric_plan": {"primary_metric": "views"},
            "risk_level": "medium",
            "publication_readiness": "ready",
        },
    )
    assert plan.status_code == 201
    return piece.json(), plan.json()


async def test_overview_counts_intake_signals(client):
    await create_signal(client)

    response = await client.get("/api/v1/admin/dashboard/overview")

    assert response.status_code == 200
    assert response.json()["total_intake_signals"] == 1


async def test_overview_counts_workflow_tasks(client):
    news = await create_news(client)
    workflow = await create_workflow(client, news["id"])
    await create_task(client, workflow["id"], news["id"])

    response = await client.get("/api/v1/admin/dashboard/overview")

    assert response.status_code == 200
    assert response.json()["pending_tasks"] == 1


async def test_overview_counts_readiness_scores(client):
    news = await create_news(client)
    await client.post(f"/api/v1/editorial-readiness/news/{news['id']}/calculate")

    response = await client.get("/api/v1/admin/dashboard/overview")

    assert response.status_code == 200
    assert response.json()["latest_readiness_count"] == 1


async def test_newsroom_health_healthy_without_blockers(client):
    response = await client.get("/api/v1/admin/dashboard/newsroom-health")

    assert response.status_code == 200
    assert response.json()["health_status"] == "healthy"


async def test_newsroom_health_degraded_with_blocked_task(client):
    news = await create_news(client)
    workflow = await create_workflow(client, news["id"])
    await create_task(
        client,
        workflow["id"],
        news["id"],
        task_status="blocked",
        blocking=True,
        blocking_reason="Needs owner",
    )

    response = await client.get("/api/v1/admin/dashboard/newsroom-health")

    assert response.status_code == 200
    assert response.json()["health_status"] == "degraded"


async def test_newsroom_health_critical_with_risk_critical(client):
    news = await create_news(client)
    response = await client.post(
        "/api/v1/risk-reviews",
        json={
            "news_item_id": news["id"],
            "entity_type": "news_item",
            "entity_id": news["id"],
            "risk_level": "critical",
            "severity": "R-SEV-4",
            "decision_recommendation": "block_publication",
            "risk_flags": ["critical"],
            "summary": "Critical risk.",
            "required_disclaimers": [],
            "language_restrictions": [],
            "publication_block_recommended": True,
        },
    )
    assert response.status_code == 201

    health = await client.get("/api/v1/admin/dashboard/newsroom-health")

    assert health.status_code == 200
    assert health.json()["health_status"] == "critical"


async def test_intake_queue_lists_pending_signals(client):
    signal = await create_signal(client)

    response = await client.get("/api/v1/admin/intake/queue")

    assert response.status_code == 200
    assert response.json()[0]["signal_id"] == signal["id"]


async def test_intake_queue_filters_by_dedupe_status(client):
    signal = await create_signal(client)

    response = await client.get(
        "/api/v1/admin/intake/queue",
        params={"dedupe_status": signal["dedupe_status"]},
    )

    assert response.status_code == 200
    assert response.json()[0]["dedupe_status"] == signal["dedupe_status"]


async def test_work_queue_detects_missing_verification(client):
    news = await create_news(client)

    response = await client.get("/api/v1/admin/editorial/work-queue")

    assert response.status_code == 200
    item = response.json()[0]
    assert item["news_item_id"] == news["id"]
    assert "VerificationRecord" in item["missing_requirements"]


async def test_work_queue_detects_missing_risk_review(client):
    news = await create_news(client)
    verification = await client.post(
        "/api/v1/verification-records",
        json={
            "news_item_id": news["id"],
            "verification_status": "verified",
            "evidence_level": "E3",
            "confidence_level": "C4",
            "summary": "Verified.",
        },
    )
    assert verification.status_code == 201

    response = await client.get("/api/v1/admin/editorial/work-queue")

    assert "RiskReview" in response.json()[0]["missing_requirements"]


async def test_work_queue_includes_latest_readiness(client):
    news = await create_news(client)
    score = await client.post(f"/api/v1/editorial-readiness/news/{news['id']}/calculate")
    assert score.status_code == 201

    response = await client.get("/api/v1/admin/editorial/work-queue")

    assert response.json()[0]["score"] == score.json()["score"]


async def test_work_queue_includes_pending_task_count(client):
    news = await create_news(client)
    workflow = await create_workflow(client, news["id"])
    await create_task(client, workflow["id"], news["id"])

    response = await client.get("/api/v1/admin/editorial/work-queue")

    assert response.json()[0]["pending_task_count"] == 1


async def test_blockers_detects_blocked_task(client):
    news = await create_news(client)
    workflow = await create_workflow(client, news["id"])
    task = await create_task(
        client,
        workflow["id"],
        news["id"],
        task_status="blocked",
        blocking=True,
        blocking_reason="Blocked",
    )

    response = await client.get("/api/v1/admin/blockers")

    assert response.status_code == 200
    assert any(item["entity_id"] == task["id"] for item in response.json())


async def test_blockers_detects_critical_risk(client):
    news = await create_news(client)
    risk = await client.post(
        "/api/v1/risk-reviews",
        json={
            "news_item_id": news["id"],
            "entity_type": "news_item",
            "entity_id": news["id"],
            "risk_level": "critical",
            "severity": "R-SEV-4",
            "decision_recommendation": "block_publication",
            "summary": "Critical risk.",
        },
    )
    assert risk.status_code == 201

    response = await client.get("/api/v1/admin/blockers")

    assert any(item["entity_id"] == risk.json()["id"] for item in response.json())


async def test_blockers_detects_blocking_audit_check(client):
    news = await create_news(client)
    audit = await client.post(
        "/api/v1/audit/checks",
        json={
            "entity_type": "news_item",
            "entity_id": news["id"],
            "audit_status": "failed",
            "severity": "high",
            "publication_block_recommended": True,
            "ready_to_advance": False,
            "missing_requirements": ["source"],
            "audit_flags": ["blocked"],
        },
    )
    assert audit.status_code == 201

    response = await client.get("/api/v1/admin/blockers")

    assert any(item["entity_id"] == audit.json()["id"] for item in response.json())


async def test_readiness_board_uses_latest_score_by_news(client):
    news = await create_news(client)
    first = await client.post(f"/api/v1/editorial-readiness/news/{news['id']}/calculate")
    second = await client.post(f"/api/v1/editorial-readiness/news/{news['id']}/calculate")
    assert first.status_code == 201
    assert second.status_code == 201

    response = await client.get("/api/v1/admin/readiness/board")

    assert len(response.json()) == 1
    assert response.json()[0]["calculated_at"] == second.json()["created_at"]


async def test_readiness_board_filters_by_score_band(client):
    news = await create_news(client)
    score = await client.post(f"/api/v1/editorial-readiness/news/{news['id']}/calculate")

    response = await client.get(
        "/api/v1/admin/readiness/board",
        params={"score_band": score.json()["score_band"]},
    )

    assert response.status_code == 200
    assert response.json()[0]["score_band"] == score.json()["score_band"]


async def test_task_board_lists_tasks(client):
    news = await create_news(client)
    workflow = await create_workflow(client, news["id"])
    task = await create_task(client, workflow["id"], news["id"])

    response = await client.get("/api/v1/admin/tasks/board")

    assert response.status_code == 200
    assert response.json()[0]["task_id"] == task["id"]


async def test_task_board_filters_by_assigned_agent(client):
    news = await create_news(client)
    workflow = await create_workflow(client, news["id"])
    await create_task(client, workflow["id"], news["id"], assigned_agent="RiskAgent")

    response = await client.get(
        "/api/v1/admin/tasks/board",
        params={"assigned_agent": "RiskAgent"},
    )

    assert response.json()[0]["assigned_agent"] == "RiskAgent"


async def test_task_board_filters_by_blocking(client):
    news = await create_news(client)
    workflow = await create_workflow(client, news["id"])
    await create_task(client, workflow["id"], news["id"], blocking=True)

    response = await client.get("/api/v1/admin/tasks/board", params={"blocking": True})

    assert response.json()[0]["blocking"] is True


async def test_publication_board_lists_publications(client):
    news = await create_news(client)
    piece, plan = await create_content_and_plan(client, news["id"])
    publication = await client.post(
        "/api/v1/publication-records",
        json={
            "content_piece_id": piece["id"],
            "distribution_plan_id": plan["id"],
            "news_item_id": news["id"],
            "channel": "Blog / Web",
            "publication_status": "scheduled",
        },
    )
    assert publication.status_code == 201

    response = await client.get("/api/v1/admin/publications/board")

    assert response.json()[0]["publication_record_id"] == publication.json()["id"]


async def test_ownership_board_detects_unassigned_news(client):
    news = await create_news(client)

    response = await client.get("/api/v1/admin/ownership/board")

    assert news["id"] in response.json()["unassigned_news"]


async def test_ownership_board_counts_assignments_by_user(client):
    user = await create_user(client)
    await client.post(
        "/api/v1/ownership/assign",
        json={
            "user_id": user["id"],
            "entity_type": "NewsItem",
            "entity_id": "news-1",
            "ownership_type": "owner",
        },
    )

    response = await client.get("/api/v1/admin/ownership/board")

    assert response.json()["users"][0]["active_assignment_count"] == 1


async def test_user_workload_returns_tasks_and_assignments(client):
    user = await create_user(client)
    news = await create_news(client)
    workflow = await create_workflow(client, news["id"])
    await create_task(client, workflow["id"], news["id"], assigned_to=user["id"])
    await client.post(
        "/api/v1/ownership/assign",
        json={
            "user_id": user["id"],
            "entity_type": "NewsItem",
            "entity_id": news["id"],
            "ownership_type": "owner",
        },
    )

    response = await client.get(f"/api/v1/admin/users/{user['id']}/workload")

    assert response.status_code == 200
    assert response.json()["summary_counts"]["workflow_tasks"] == 1
    assert response.json()["summary_counts"]["ownership_assignments"] == 1


async def test_gaps_detects_news_without_verification(client):
    await create_news(client)

    response = await client.get("/api/v1/admin/gaps")

    gap = next(item for item in response.json() if item["gap_type"] == "news_without_verification")
    assert gap["count"] == 1


async def test_gaps_detects_published_without_metrics(client):
    news = await create_news(client)
    piece, plan = await create_content_and_plan(client, news["id"])
    publication = await client.post(
        "/api/v1/publication-records",
        json={
            "content_piece_id": piece["id"],
            "distribution_plan_id": plan["id"],
            "news_item_id": news["id"],
            "channel": "Blog / Web",
            "publication_status": "published",
            "published_url": "https://example.com/published",
        },
    )
    assert publication.status_code == 201

    response = await client.get("/api/v1/admin/gaps")

    gap = next(item for item in response.json() if item["gap_type"] == "published_without_metrics")
    assert gap["count"] == 1


async def test_gaps_detects_agent_outputs_pending_review(client):
    response = await client.post(
        "/api/v1/agent-outputs",
        json={
            "agent_name": "RiskAgent",
            "output_type": "risk_review",
            "entity_type": "news_item",
            "entity_id": "news-1",
            "summary": "Needs review",
            "payload": {"risk": "critical"},
            "risk_flags": ["critical_risk"],
        },
    )
    assert response.status_code == 201

    gaps = await client.get("/api/v1/admin/gaps")

    gap = next(item for item in gaps.json() if item["gap_type"] == "agent_outputs_pending_review")
    assert gap["count"] == 1


async def test_admin_dashboard_allows_viewer_when_auth_enabled(client, monkeypatch):
    enable_auth(monkeypatch)

    response = await client.get(
        "/api/v1/admin/dashboard/overview",
        headers=auth_headers("viewer"),
    )

    assert response.status_code == 200


async def test_admin_dashboard_blocks_invalid_role(client, monkeypatch):
    enable_auth(monkeypatch)

    response = await client.get(
        "/api/v1/admin/dashboard/overview",
        headers=auth_headers("external"),
    )

    assert response.status_code == 403


async def test_admin_dashboard_requires_api_key_when_auth_enabled(client, monkeypatch):
    enable_auth(monkeypatch)

    response = await client.get(
        "/api/v1/admin/dashboard/overview",
        headers={"X-Actor-Role": "admin"},
    )

    assert response.status_code == 401


async def test_admin_dashboard_compatible_when_auth_disabled(client):
    response = await client.get("/api/v1/admin/dashboard/overview")

    assert response.status_code == 200
