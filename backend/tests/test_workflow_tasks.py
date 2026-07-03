import pytest

from app.core.config import get_settings

NEWS_PAYLOAD = {
    "title": "Task queue news",
    "summary": "Workflow task queue integration coverage.",
    "category": "markets",
    "content": "Workflow task queue integration coverage.",
    "source_url": "https://example.com/workflow-task-queue",
    "source_name": "Example Wire",
}


def workflow_task_payload(workflow_id: str, news_id: str, **overrides):
    payload = {
        "workflow_run_id": workflow_id,
        "news_item_id": news_id,
        "task_type": "source_validation",
        "task_status": "queued",
        "priority": "P3",
        "assigned_agent": "SourceValidatorAgent",
        "assigned_to": None,
        "title": "Validate sources",
        "description": "Validate sources before drafting.",
        "input_payload": {"evidence": ["wire"]},
        "output_ref": None,
        "agent_execution_id": None,
        "agent_output_id": None,
        "blocking": False,
        "blocking_reason": None,
        "attempt_count": 0,
        "max_attempts": 3,
        "due_at": None,
        "started_at": None,
        "completed_at": None,
        "failed_at": None,
        "cancelled_at": None,
    }
    payload.update(overrides)
    return payload


async def create_news_item(client, **overrides):
    response = await client.post("/api/v1/news/intake", json={**NEWS_PAYLOAD, **overrides})
    assert response.status_code == 201
    return response.json()


async def create_workflow(client, news_id: str):
    response = await client.post(
        f"/api/v1/workflows/news/{news_id}/start",
        json={"workflow_type": "editorial_pipeline"},
    )
    assert response.status_code == 201
    return response.json()


async def create_task(client, workflow_id: str, news_id: str, **overrides):
    response = await client.post(
        "/api/v1/workflow-tasks",
        json=workflow_task_payload(workflow_id, news_id, **overrides),
    )
    assert response.status_code == 201
    return response.json()


async def create_agent_output(client, news_id: str, workflow_id: str, **overrides):
    payload = {
        "agent_name": "SourceValidatorAgent",
        "agent_version": "1.0.0",
        "output_type": "source_review",
        "status": "stored",
        "entity_type": "news_item",
        "entity_id": news_id,
        "news_item_id": news_id,
        "workflow_run_id": workflow_id,
        "workflow_step_id": None,
        "summary": "Validated sources for workflow task queue tests.",
        "payload": {"sources": [{"title": "wire", "confidence": "medium"}]},
        "risk_flags": [],
        "missing_requirements": [],
        "next_agent": "RiskAgent",
        "human_review_required": False,
    }
    payload.update(overrides)
    response = await client.post("/api/v1/agent-outputs", json=payload)
    assert response.status_code == 201
    return response.json()


async def test_create_workflow_task_valid(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])

    task = await create_task(client, workflow["id"], news["id"])

    assert task["workflow_run_id"] == workflow["id"]
    assert task["news_item_id"] == news["id"]
    assert task["task_status"] == "queued"
    assert task["task_type"] == "source_validation"


async def test_create_workflow_task_blocks_invalid_task_type(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])

    response = await client.post(
        "/api/v1/workflow-tasks",
        json=workflow_task_payload(workflow["id"], news["id"], task_type="unknown_task"),
    )

    assert response.status_code == 422


async def test_create_workflow_task_blocks_invalid_status(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])

    response = await client.post(
        "/api/v1/workflow-tasks",
        json=workflow_task_payload(workflow["id"], news["id"], task_status="sleeping"),
    )

    assert response.status_code == 422


async def test_create_workflow_task_blocks_invalid_priority(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])

    response = await client.post(
        "/api/v1/workflow-tasks",
        json=workflow_task_payload(workflow["id"], news["id"], priority="P9"),
    )

    assert response.status_code == 422


async def test_create_workflow_task_blocks_invalid_assigned_agent(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])

    response = await client.post(
        "/api/v1/workflow-tasks",
        json=workflow_task_payload(workflow["id"], news["id"], assigned_agent="RobotEditor"),
    )

    assert response.status_code == 422


async def test_create_workflow_task_blocks_empty_payload(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])

    response = await client.post(
        "/api/v1/workflow-tasks",
        json=workflow_task_payload(workflow["id"], news["id"], input_payload={}),
    )

    assert response.status_code == 422


async def test_list_workflow_tasks(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    await create_task(client, workflow["id"], news["id"])
    await create_task(
        client, workflow["id"], news["id"], task_type="risk_review", assigned_agent="RiskAgent"
    )

    response = await client.get("/api/v1/workflow-tasks")

    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_filter_workflow_tasks_by_workflow_run_id(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    await create_task(client, workflow["id"], news["id"])

    response = await client.get(
        "/api/v1/workflow-tasks", params={"workflow_run_id": workflow["id"]}
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["workflow_run_id"] == workflow["id"]


async def test_filter_workflow_tasks_by_news_item_id(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    await create_task(client, workflow["id"], news["id"])

    response = await client.get("/api/v1/workflow-tasks", params={"news_item_id": news["id"]})

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["news_item_id"] == news["id"]


async def test_filter_workflow_tasks_by_task_status(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    await create_task(client, workflow["id"], news["id"], task_status="queued")
    await create_task(
        client,
        workflow["id"],
        news["id"],
        task_type="manual_review",
        task_status="blocked",
        assigned_agent="HumanEditor",
    )

    response = await client.get("/api/v1/workflow-tasks", params={"task_status": "blocked"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["task_status"] == "blocked"


async def test_get_workflow_task_by_id(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    task = await create_task(client, workflow["id"], news["id"])

    response = await client.get(f"/api/v1/workflow-tasks/{task['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == task["id"]


async def test_get_workflow_tasks_by_workflow(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    await create_task(client, workflow["id"], news["id"])

    response = await client.get(f"/api/v1/workflows/{workflow['id']}/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_workflow_tasks_by_news(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    await create_task(client, workflow["id"], news["id"])

    response = await client.get(f"/api/v1/news/{news['id']}/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_start_workflow_task_changes_status_to_running(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    task = await create_task(client, workflow["id"], news["id"])

    response = await client.patch(
        f"/api/v1/workflow-tasks/{task['id']}/start",
        json={"assigned_to": "operator"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["task_status"] == "running"
    assert body["assigned_to"] == "operator"
    assert body["started_at"] is not None


async def test_complete_workflow_task_changes_status_to_completed(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    task = await create_task(client, workflow["id"], news["id"])
    await client.patch(f"/api/v1/workflow-tasks/{task['id']}/start", json={})

    response = await client.patch(
        f"/api/v1/workflow-tasks/{task['id']}/complete",
        json={"output_ref": "workflow-task-output-1"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["task_status"] == "completed"
    assert body["completed_at"] is not None


async def test_complete_workflow_task_with_warnings(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    task = await create_task(client, workflow["id"], news["id"])
    await client.patch(f"/api/v1/workflow-tasks/{task['id']}/start", json={})

    response = await client.patch(
        f"/api/v1/workflow-tasks/{task['id']}/complete",
        json={"completed_with_warnings": True},
    )

    assert response.status_code == 200
    assert response.json()["task_status"] == "completed_with_warnings"


async def test_complete_workflow_task_with_agent_output(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    output = await create_agent_output(client, news["id"], workflow["id"])
    task = await create_task(client, workflow["id"], news["id"])
    await client.patch(f"/api/v1/workflow-tasks/{task['id']}/start", json={})

    response = await client.patch(
        f"/api/v1/workflow-tasks/{task['id']}/complete",
        json={"agent_output_id": output["id"]},
    )

    assert response.status_code == 200
    assert response.json()["agent_output_id"] == output["id"]


async def test_fail_workflow_task_blocks_workflow(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    task = await create_task(client, workflow["id"], news["id"])

    response = await client.patch(
        f"/api/v1/workflow-tasks/{task['id']}/fail",
        json={"reason": "Missing verification"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["task_status"] == "failed"
    assert body["blocking"] is True


async def test_block_workflow_task(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    task = await create_task(client, workflow["id"], news["id"])

    response = await client.patch(
        f"/api/v1/workflow-tasks/{task['id']}/block",
        json={"reason": "Missing VerificationRecord"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["task_status"] == "blocked"
    assert body["blocking"] is True


async def test_cancel_workflow_task(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    task = await create_task(client, workflow["id"], news["id"])

    response = await client.patch(
        f"/api/v1/workflow-tasks/{task['id']}/cancel",
        json={"reason": "No longer needed"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["task_status"] == "cancelled"
    assert body["cancelled_at"] is not None


async def test_retry_workflow_task_increments_attempt_count(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    task = await create_task(client, workflow["id"], news["id"], task_status="failed")

    response = await client.patch(f"/api/v1/workflow-tasks/{task['id']}/retry", json={})

    assert response.status_code == 200
    body = response.json()
    assert body["attempt_count"] == 1
    assert body["task_status"] == "retrying"


async def test_retry_workflow_task_blocks_when_max_attempts_reached(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    task = await create_task(
        client,
        workflow["id"],
        news["id"],
        task_status="failed",
        attempt_count=1,
        max_attempts=1,
    )

    response = await client.patch(f"/api/v1/workflow-tasks/{task['id']}/retry", json={})

    assert response.status_code == 409


async def test_cannot_start_terminal_workflow_task(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    task = await create_task(client, workflow["id"], news["id"], task_status="completed")

    response = await client.patch(
        f"/api/v1/workflow-tasks/{task['id']}/start",
        json={"assigned_to": "operator"},
    )

    assert response.status_code == 409


async def test_correlation_id_persisted_from_header(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])

    response = await client.post(
        "/api/v1/workflow-tasks",
        json=workflow_task_payload(workflow["id"], news["id"]),
        headers={"X-Correlation-ID": "corr-task-queue-001"},
    )

    assert response.status_code == 201
    assert response.headers["X-Correlation-ID"] == "corr-task-queue-001"
    assert response.json()["correlation_id"] == "corr-task-queue-001"


async def test_bootstrap_workflow_tasks_creates_initial_tasks(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])

    response = await client.post(f"/api/v1/workflows/{workflow['id']}/tasks/bootstrap")

    assert response.status_code == 201
    body = response.json()
    assert {task["task_type"] for task in body} == {
        "source_validation",
        "risk_review",
        "editorial_draft",
        "audit_check",
        "distribution_planning",
    }


async def test_bootstrap_workflow_tasks_does_not_duplicate_existing_tasks(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    await client.post(f"/api/v1/workflows/{workflow['id']}/tasks/bootstrap")

    response = await client.post(f"/api/v1/workflows/{workflow['id']}/tasks/bootstrap")

    assert response.status_code == 201
    assert response.json() == []


async def test_workflow_task_summary_counts(client):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    await create_task(client, workflow["id"], news["id"])
    await create_task(
        client,
        workflow["id"],
        news["id"],
        task_status="blocked",
        task_type="manual_review",
        assigned_agent="HumanEditor",
    )
    completed = await create_task(
        client,
        workflow["id"],
        news["id"],
        task_status="completed",
        task_type="workflow_recalculation",
        assigned_agent="System",
    )

    response = await client.get(f"/api/v1/workflows/{workflow['id']}/tasks/summary")

    assert response.status_code == 200
    body = response.json()
    assert body["task_count"] == 3
    assert body["blocking_task_count"] == 1
    assert body["completed_task_count"] == 1
    assert body["pending_task_count"] == 1
    assert completed["task_status"] == "completed"


@pytest.mark.parametrize(
    ("method", "action"),
    [
        ("post", "create"),
        ("patch", "start"),
        ("patch", "complete"),
        ("patch", "fail"),
        ("patch", "block"),
        ("patch", "cancel"),
        ("patch", "retry"),
    ],
)
async def test_auth_protects_workflow_task_writes(client, monkeypatch, method, action):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    task = await create_task(client, workflow["id"], news["id"])
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    if action == "create":
        response = await client.post(
            "/api/v1/workflow-tasks",
            json=workflow_task_payload(workflow["id"], news["id"]),
        )
    elif action == "start":
        response = await client.patch(
            f"/api/v1/workflow-tasks/{task['id']}/start",
            json={"assigned_to": "operator"},
        )
    elif action == "complete":
        response = await client.patch(
            f"/api/v1/workflow-tasks/{task['id']}/complete",
            json={"output_ref": "ref"},
        )
    elif action == "fail":
        response = await client.patch(
            f"/api/v1/workflow-tasks/{task['id']}/fail",
            json={"reason": "reason"},
        )
    elif action == "block":
        response = await client.patch(
            f"/api/v1/workflow-tasks/{task['id']}/block",
            json={"reason": "reason"},
        )
    elif action == "cancel":
        response = await client.patch(
            f"/api/v1/workflow-tasks/{task['id']}/cancel",
            json={"reason": "reason"},
        )
    else:
        response = await client.patch(f"/api/v1/workflow-tasks/{task['id']}/retry", json={})

    assert response.status_code == 401


async def test_auth_allows_workflow_task_write_with_api_key(client, monkeypatch):
    news = await create_news_item(client)
    workflow = await create_workflow(client, news["id"])
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_enabled", True)
    monkeypatch.setattr(settings, "api_key", "dev-secret")

    response = await client.post(
        "/api/v1/workflow-tasks",
        json=workflow_task_payload(workflow["id"], news["id"]),
        headers={"X-API-Key": "dev-secret"},
    )

    assert response.status_code == 201
