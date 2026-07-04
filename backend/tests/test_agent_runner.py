from app.core.config import get_settings

NEWS_PAYLOAD = {
    "title": "Runner test news",
    "summary": "A deterministic runner test item.",
    "category": "ops",
    "priority": "P2",
    "source_url": "https://example.com/runner",
    "source_name": "Runner Source",
}


async def create_news(client, **overrides) -> dict:
    response = await client.post("/api/v1/news/intake", json={**NEWS_PAYLOAD, **overrides})
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
        "task_type": "source_validation",
        "task_status": "queued",
        "priority": "P2",
        "assigned_agent": "SourceValidatorAgent",
        "title": "Validate sources",
        "description": "Validate source evidence.",
    }
    payload.update(overrides)
    response = await client.post("/api/v1/workflow-tasks", json=payload)
    assert response.status_code == 201
    return response.json()


async def create_workflow_task_chain(client, **task_overrides) -> tuple[dict, dict, dict]:
    news = await create_news(client)
    workflow = await create_workflow(client, news["id"])
    task = await create_task(client, workflow["id"], news["id"], **task_overrides)
    return news, workflow, task


async def test_capabilities_returns_supported_agents(client):
    response = await client.get("/api/v1/agent-runner/capabilities")

    assert response.status_code == 200
    agents = {item["agent_name"] for item in response.json()}
    assert "SourceValidatorAgent" in agents
    assert "RiskAgent" in agents


async def test_capabilities_are_internal_only(client):
    response = await client.get("/api/v1/agent-runner/capabilities")

    assert response.status_code == 200
    assert all(item["internal_only"] is True for item in response.json())


async def test_capabilities_do_not_expose_external_integrations(client):
    response = await client.get("/api/v1/agent-runner/capabilities")

    assert response.status_code == 200
    assert all(item["external_integrations"] is False for item in response.json())


async def test_dry_run_valid_task_returns_eligible(client):
    _, _, task = await create_workflow_task_chain(client)

    response = await client.post(f"/api/v1/agent-runner/tasks/{task['id']}/dry-run")

    assert response.status_code == 200
    body = response.json()
    assert body["eligible"] is True
    assert body["recommended_agent"] == "SourceValidatorAgent"
    assert body["output_type"] == "source_review"


async def test_dry_run_does_not_create_agent_execution(client):
    _, _, task = await create_workflow_task_chain(client)

    response = await client.post(f"/api/v1/agent-runner/tasks/{task['id']}/dry-run")
    executions = await client.get("/api/v1/agents/executions")

    assert response.status_code == 200
    assert executions.json() == []


async def test_dry_run_does_not_create_agent_output(client):
    _, _, task = await create_workflow_task_chain(client)

    response = await client.post(f"/api/v1/agent-runner/tasks/{task['id']}/dry-run")
    outputs = await client.get("/api/v1/agent-outputs")

    assert response.status_code == 200
    assert outputs.json() == []


async def test_dry_run_does_not_modify_workflow_task(client):
    _, _, task = await create_workflow_task_chain(client)

    response = await client.post(f"/api/v1/agent-runner/tasks/{task['id']}/dry-run")
    task_after = await client.get(f"/api/v1/workflow-tasks/{task['id']}")

    assert response.status_code == 200
    assert task_after.json()["task_status"] == "queued"
    assert task_after.json()["agent_output_id"] is None


async def test_dry_run_missing_task_returns_404(client):
    response = await client.post("/api/v1/agent-runner/tasks/missing-task/dry-run")

    assert response.status_code == 404


async def test_run_task_creates_agent_execution(client):
    _, _, task = await create_workflow_task_chain(client)

    response = await client.post(f"/api/v1/agent-runner/tasks/{task['id']}/run", json={})

    assert response.status_code == 200
    execution = response.json()["execution"]
    assert execution["agent_name"] == "SourceValidatorAgent"
    assert execution["agent_version"] == "internal-runner-v1"
    assert execution["status"] == "completed"


async def test_run_task_creates_agent_output(client):
    _, _, task = await create_workflow_task_chain(client)

    response = await client.post(f"/api/v1/agent-runner/tasks/{task['id']}/run", json={})

    assert response.status_code == 200
    output = response.json()["output"]
    assert output["output_type"] == "source_review"
    assert output["entity_type"] == "WorkflowTask"
    assert output["entity_id"] == task["id"]


async def test_run_task_completes_workflow_task(client):
    _, _, task = await create_workflow_task_chain(client)

    response = await client.post(f"/api/v1/agent-runner/tasks/{task['id']}/run", json={})

    assert response.status_code == 200
    completed_task = response.json()["task"]
    assert completed_task["task_status"] == "completed"
    assert completed_task["agent_output_id"] == response.json()["output"]["id"]


async def test_run_task_persists_correlation_id(client):
    _, _, task = await create_workflow_task_chain(client)

    response = await client.post(
        f"/api/v1/agent-runner/tasks/{task['id']}/run",
        json={},
        headers={"X-Correlation-ID": "runner-correlation"},
    )

    assert response.status_code == 200
    assert response.json()["execution"]["correlation_id"] == "runner-correlation"
    assert response.json()["output"]["correlation_id"] == "runner-correlation"


async def test_run_source_validator_produces_source_review(client):
    _, _, task = await create_workflow_task_chain(client)

    response = await client.post(f"/api/v1/agent-runner/tasks/{task['id']}/run", json={})

    assert response.status_code == 200
    output = response.json()["output"]
    assert output["output_type"] == "source_review"
    assert "VerificationRecord" in output["missing_requirements"]


async def test_run_risk_agent_marks_human_review_required(client):
    _, workflow, _task = await create_workflow_task_chain(client)
    risk_task = await create_task(
        client,
        workflow["id"],
        workflow["news_item_id"],
        task_type="risk_review",
        assigned_agent="RiskAgent",
    )

    response = await client.post(f"/api/v1/agent-runner/tasks/{risk_task['id']}/run", json={})

    assert response.status_code == 200
    output = response.json()["output"]
    assert output["output_type"] == "risk_review"
    assert output["human_review_required"] is True
    assert response.json()["task"]["task_status"] == "completed_with_warnings"


async def test_run_task_blocks_completed_task(client):
    _, _, task = await create_workflow_task_chain(client, task_status="completed")

    response = await client.post(f"/api/v1/agent-runner/tasks/{task['id']}/run", json={})

    assert response.status_code == 409


async def test_run_task_blocks_human_editor_without_force(client):
    _, _, task = await create_workflow_task_chain(
        client,
        task_type="manual_review",
        assigned_agent="HumanEditor",
    )

    response = await client.post(f"/api/v1/agent-runner/tasks/{task['id']}/run", json={})

    assert response.status_code == 409


async def test_run_task_blocked_without_force_blocks(client):
    _, _, task = await create_workflow_task_chain(
        client,
        task_status="blocked",
        blocking=True,
        blocking_reason="Waiting for operator",
    )

    response = await client.post(f"/api/v1/agent-runner/tasks/{task['id']}/run", json={})

    assert response.status_code == 409


async def test_run_task_blocked_with_force_allows_supported_agent(client):
    _, _, task = await create_workflow_task_chain(
        client,
        task_status="blocked",
        blocking=True,
        blocking_reason="Waiting for operator",
    )

    response = await client.post(
        f"/api/v1/agent-runner/tasks/{task['id']}/run",
        json={"force": True},
    )

    assert response.status_code == 200
    assert response.json()["task"]["task_status"] == "completed"


async def test_run_task_registers_operational_audit(client):
    _, _, task = await create_workflow_task_chain(client)

    response = await client.post(f"/api/v1/agent-runner/tasks/{task['id']}/run", json={})
    audit = await client.get(
        "/api/v1/operational-audit/events",
        params={"action": "agent_runner.run_task"},
    )

    assert response.status_code == 200
    assert audit.status_code == 200
    assert audit.json()[0]["workflow_task_id"] == task["id"]


async def test_run_next_executes_p0_before_p3(client):
    news = await create_news(client)
    workflow = await create_workflow(client, news["id"])
    p3 = await create_task(client, workflow["id"], news["id"], priority="P3")
    p0 = await create_task(client, workflow["id"], news["id"], priority="P0")

    response = await client.post(
        f"/api/v1/agent-runner/workflows/{workflow['id']}/run-next",
        json={},
    )

    assert response.status_code == 200
    assert response.json()["result"]["task"]["id"] == p0["id"]
    assert response.json()["result"]["task"]["id"] != p3["id"]


async def test_run_next_ignores_completed_cancelled_archived(client):
    news = await create_news(client)
    workflow = await create_workflow(client, news["id"])
    await create_task(client, workflow["id"], news["id"], task_status="completed")
    await create_task(client, workflow["id"], news["id"], task_status="cancelled")
    await create_task(client, workflow["id"], news["id"], task_status="archived")
    runnable = await create_task(client, workflow["id"], news["id"], task_status="queued")

    response = await client.post(
        f"/api/v1/agent-runner/workflows/{workflow['id']}/run-next",
        json={},
    )

    assert response.status_code == 200
    assert response.json()["result"]["task"]["id"] == runnable["id"]


async def test_run_next_returns_no_eligible_task(client):
    news = await create_news(client)
    workflow = await create_workflow(client, news["id"])

    response = await client.post(
        f"/api/v1/agent-runner/workflows/{workflow['id']}/run-next",
        json={},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "no_eligible_task"


async def test_run_next_registers_operational_audit(client):
    news = await create_news(client)
    workflow = await create_workflow(client, news["id"])
    await create_task(client, workflow["id"], news["id"])

    response = await client.post(
        f"/api/v1/agent-runner/workflows/{workflow['id']}/run-next",
        json={},
    )
    audit = await client.get(
        "/api/v1/operational-audit/events",
        params={"action": "agent_runner.run_next"},
    )

    assert response.status_code == 200
    assert audit.json()[0]["workflow_run_id"] == workflow["id"]


async def test_recent_runs_lists_internal_executions(client):
    _, _, task = await create_workflow_task_chain(client)
    run = await client.post(f"/api/v1/agent-runner/tasks/{task['id']}/run", json={})

    response = await client.get("/api/v1/agent-runner/runs")

    assert run.status_code == 200
    assert response.status_code == 200
    assert response.json()[0]["agent_version"] == "internal-runner-v1"


async def test_recent_runs_filters_by_agent_name(client):
    _, _, task = await create_workflow_task_chain(client)
    await client.post(f"/api/v1/agent-runner/tasks/{task['id']}/run", json={})

    response = await client.get(
        "/api/v1/agent-runner/runs",
        params={"agent_name": "SourceValidatorAgent"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_recent_runs_filters_by_status(client):
    _, _, task = await create_workflow_task_chain(client)
    await client.post(f"/api/v1/agent-runner/tasks/{task['id']}/run", json={})

    response = await client.get("/api/v1/agent-runner/runs", params={"status": "completed"})

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_agent_operator_can_run_when_auth_enabled(client, monkeypatch):
    _, _, task = await create_workflow_task_chain(client)
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.post(
        f"/api/v1/agent-runner/tasks/{task['id']}/run",
        json={},
        headers={"X-API-Key": "dev-secret", "X-Actor-Role": "agent_operator"},
    )

    assert response.status_code == 200


async def test_viewer_cannot_run_when_auth_enabled(client, monkeypatch):
    _, _, task = await create_workflow_task_chain(client)
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.post(
        f"/api/v1/agent-runner/tasks/{task['id']}/run",
        json={},
        headers={"X-API-Key": "dev-secret", "X-Actor-Role": "viewer"},
    )

    assert response.status_code == 403


async def test_admin_can_read_capabilities_when_auth_enabled(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.get(
        "/api/v1/agent-runner/capabilities",
        headers={"X-API-Key": "dev-secret", "X-Actor-Role": "admin"},
    )

    assert response.status_code == 200


async def test_auth_enabled_requires_api_key_for_runner(client, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.get("/api/v1/agent-runner/capabilities")

    assert response.status_code == 401


async def test_auth_disabled_keeps_runner_compatible(client):
    response = await client.get("/api/v1/agent-runner/capabilities")

    assert response.status_code == 200


async def test_admin_agent_runner_summary_counts_runs(client):
    _, _, task = await create_workflow_task_chain(client)
    await client.post(f"/api/v1/agent-runner/tasks/{task['id']}/run", json={})

    response = await client.get("/api/v1/admin/agent-runner/summary")

    assert response.status_code == 200
    assert response.json()["total_internal_runs"] == 1
    assert response.json()["completed_runs"] == 1


async def test_admin_agent_runner_summary_counts_pending_review_outputs(client):
    _, workflow, _task = await create_workflow_task_chain(client)
    risk_task = await create_task(
        client,
        workflow["id"],
        workflow["news_item_id"],
        task_type="risk_review",
        assigned_agent="RiskAgent",
    )
    await client.post(f"/api/v1/agent-runner/tasks/{risk_task['id']}/run", json={})

    response = await client.get("/api/v1/admin/agent-runner/summary")

    assert response.status_code == 200
    assert response.json()["outputs_pending_review"] == 1


async def test_admin_agent_runner_summary_counts_eligible_tasks(client):
    await create_workflow_task_chain(client)

    response = await client.get("/api/v1/admin/agent-runner/summary")

    assert response.status_code == 200
    assert response.json()["tasks_eligible_for_runner"] == 1
