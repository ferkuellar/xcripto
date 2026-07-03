# XMIP Frontend/Admin API Contract

This contract describes the backend surface intended for the future React/Vite
admin dashboard. It is a backend contract only; no frontend files are created in
this phase.

## Base URL

Local development:

```text
http://127.0.0.1:8000
```

Docker development:

```text
http://localhost:8000
```

All versioned business endpoints live under:

```text
/api/v1
```

## Headers

| Header | Required | Purpose |
| --- | --- | --- |
| `X-API-Key` | When `AUTH_ENABLED=true` and endpoint is protected | MVP internal API key auth |
| `X-Actor-Role` | Required for RBAC checks when auth is enabled | Static role authorization |
| `X-Actor-Id` | Optional | Human/system actor traceability |
| `X-Correlation-ID` | Optional | Request correlation across logs and persisted records |
| `Content-Type: application/json` | For JSON bodies | Request body format |

Never expose production API keys to public users. The API key pattern is for
internal MVP/admin operation until JWT/OAuth is implemented.

## Pagination And Filters

List endpoints use:

```text
limit: integer, default 50, max usually 200
offset: integer, default 0
```

Some list endpoints support exact filters such as `status`, `priority`,
`agent_name`, `connector_type`, `readiness_status` or `score_band`. Date/time
values are ISO 8601 strings. Newer news list work may also expose
`X-Total-Count` for frontend pagination.

## Error Shape

FastAPI errors use:

```json
{
  "detail": "Clear error message"
}
```

Validation errors use FastAPI/Pydantic detail arrays. Many backend responses also
include or persist `correlation_id`; frontend clients should send
`X-Correlation-ID` and surface it in support/debug views.

See `API_ERROR_CONTRACT.md` for detailed examples.

## Frontend-Safe Config

| Method | Path | Auth | Permission | Use case |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/frontend/config` | API key if enabled | `admin.dashboard.read` | Discover safe UI feature flags and required headers |
| GET | `/api/v1/admin/frontend/route-map` | API key if enabled | `admin.dashboard.read` | Discover major frontend sections and permissions |

`frontend/config` never returns `API_KEY`, `DATABASE_URL` or secrets.

## Admin Dashboard Endpoints

| Method | Path | Permission | Query params | Frontend use case |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/dashboard/overview` | `admin.dashboard.read` | none | Top KPI cards |
| GET | `/api/v1/admin/dashboard/newsroom-health` | `admin.dashboard.read` | none | Health banner and warnings |
| GET | `/api/v1/admin/intake/queue` | `admin.dashboard.read` | `signal_status`, `dedupe_status`, `priority`, `topic`, `limit`, `offset` | Intake queue table |
| GET | `/api/v1/admin/editorial/work-queue` | `admin.dashboard.read` | none | Editorial work queue |
| GET | `/api/v1/admin/blockers` | `admin.dashboard.read` | none | Blockers panel |
| GET | `/api/v1/admin/readiness/board` | `admin.dashboard.read` | `score_band`, `readiness_status`, `next_agent`, `limit`, `offset` | Readiness board |
| GET | `/api/v1/admin/tasks/board` | `admin.dashboard.read` | `task_status`, `assigned_agent`, `assigned_to`, `priority`, `blocking`, `limit`, `offset` | Task board |
| GET | `/api/v1/admin/publications/board` | `admin.dashboard.read` | `publication_status`, `channel`, `limit`, `offset` | Publication board |
| GET | `/api/v1/admin/ownership/board` | `admin.dashboard.read` | none | Ownership overview |
| GET | `/api/v1/admin/users/{user_id}/workload` | `admin.dashboard.read` | none | User workload drawer/page |
| GET | `/api/v1/admin/gaps` | `admin.dashboard.read` | none | Operational gaps |
| GET | `/api/v1/admin/agent-runner/summary` | `agent_runner.read` | none | Runner summary cards |
| GET | `/api/v1/admin/connectors/summary` | `connector.read` | none | Connector summary cards |
| GET | `/api/v1/admin/audit/summary` | `operational_audit.read` | none | Audit summary cards |

## Intake

| Method | Path | Permission | Body | Frontend use case |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/intake/signals` | `intake.create` | Intake signal payload | Manual signal creation |
| GET | `/api/v1/intake/signals` | public/read-only for now | filters + pagination | Signal search/list |
| GET | `/api/v1/intake/signals/{signal_id}` | public/read-only for now | none | Signal detail |
| POST | `/api/v1/intake/signals/{signal_id}/dedupe` | `intake.create` | none | Recalculate dedupe |
| POST | `/api/v1/intake/signals/{signal_id}/promote` | `intake.promote` | `{create_workflow, workflow_type}` | Promote signal to `NewsItem` |
| PATCH | `/api/v1/intake/signals/{signal_id}/reject` | `intake.create` | `{reason}` | Reject signal |
| PATCH | `/api/v1/intake/signals/{signal_id}/archive` | `intake.create` | none | Archive signal |

## Workflow And Tasks

| Method | Path | Permission | Use case |
| --- | --- | --- | --- |
| POST | `/api/v1/workflows/news/{news_id}/start` | `workflow.start` | Start workflow for a news item |
| GET | `/api/v1/workflows` | read-only | Workflow list |
| GET | `/api/v1/workflows/{workflow_run_id}` | read-only | Workflow detail |
| GET | `/api/v1/news/{news_id}/workflow` | read-only | Active/latest workflow by news |
| POST | `/api/v1/workflows/{workflow_run_id}/recalculate` | `workflow.advance` | Recalculate workflow state |
| POST | `/api/v1/workflows/{workflow_run_id}/advance` | `workflow.advance` | Advance workflow if dependencies allow |
| POST | `/api/v1/workflow-tasks` | `workflow_task.create` | Create internal task |
| GET | `/api/v1/workflow-tasks` | read-only | Task list |
| PATCH | `/api/v1/workflow-tasks/{task_id}/start` | `workflow_task.start` | Start task |
| PATCH | `/api/v1/workflow-tasks/{task_id}/complete` | `workflow_task.complete` | Complete task |
| PATCH | `/api/v1/workflow-tasks/{task_id}/fail` | `workflow_task.fail` | Fail task |
| PATCH | `/api/v1/workflow-tasks/{task_id}/block` | `workflow_task.block` | Block task |
| PATCH | `/api/v1/workflow-tasks/{task_id}/cancel` | `workflow_task.cancel` | Cancel task |
| PATCH | `/api/v1/workflow-tasks/{task_id}/retry` | `workflow_task.retry` | Retry failed/blocked task |

## Readiness

| Method | Path | Permission | Use case |
| --- | --- | --- | --- |
| POST | `/api/v1/editorial-readiness/news/{news_id}/calculate` | `readiness.calculate` | Calculate and persist score |
| GET | `/api/v1/editorial-readiness/news/{news_id}/latest` | read-only | Latest score for news |
| GET | `/api/v1/editorial-readiness/news/{news_id}/explain` | read-only | Explain without persisting |
| GET | `/api/v1/editorial-readiness` | read-only | Filtered score list |
| GET | `/api/v1/editorial-readiness/{score_id}` | read-only | Score detail |

## Agent Runner

| Method | Path | Permission | Use case |
| --- | --- | --- | --- |
| GET | `/api/v1/agent-runner/capabilities` | `agent_runner.read` | Supported internal agents |
| POST | `/api/v1/agent-runner/tasks/{task_id}/dry-run` | `agent_runner.read` | Preview runner output |
| POST | `/api/v1/agent-runner/tasks/{task_id}/run` | `agent_runner.run` | Execute deterministic local runner |
| POST | `/api/v1/agent-runner/workflows/{workflow_run_id}/run-next` | `agent_runner.run` | Execute next eligible task |
| GET | `/api/v1/agent-runner/runs` | `agent_runner.read` | Recent internal runs |

## Connectors

| Method | Path | Permission | Use case |
| --- | --- | --- | --- |
| POST | `/api/v1/connectors` | `connector.create` | Register connector contract |
| GET | `/api/v1/connectors` | `connector.read` | Connector list |
| GET | `/api/v1/connectors/{connector_id}` | `connector.read` | Connector detail |
| PATCH | `/api/v1/connectors/{connector_id}` | `connector.update` | Update safe configuration |
| PATCH | `/api/v1/connectors/{connector_id}/enable` | `connector.update` | Enable registered/dry-run connector |
| PATCH | `/api/v1/connectors/{connector_id}/disable` | `connector.update` | Disable connector |
| PATCH | `/api/v1/connectors/{connector_id}/archive` | `connector.archive` | Archive connector |
| POST | `/api/v1/connectors/{connector_id}/validate` | `connector.run` | Validate connector contract |
| POST | `/api/v1/connectors/{connector_id}/dry-run` | `connector.run` | Dry-run without external calls |
| GET | `/api/v1/connectors/{connector_id}/runs` | `connector.read` | Connector runs |
| GET | `/api/v1/connectors/runs/{run_id}` | `connector.read` | Connector run detail |

## Operational Audit

| Method | Path | Permission | Use case |
| --- | --- | --- | --- |
| GET | `/api/v1/operational-audit/events` | `operational_audit.read` | Audit log list |
| GET | `/api/v1/operational-audit/events/{event_id}` | `operational_audit.read` | Audit event detail |
| GET | `/api/v1/operational-audit/correlation/{correlation_id}` | `operational_audit.read` | Trace by correlation |
| GET | `/api/v1/operational-audit/actors/{actor_id}` | `operational_audit.read` | Trace by actor |
| GET | `/api/v1/operational-audit/entity/{entity_type}/{entity_id}` | `operational_audit.read` | Trace by entity |

## Users And Ownership

| Method | Path | Permission | Use case |
| --- | --- | --- | --- |
| POST | `/api/v1/users` | `user.create` | Create internal user |
| GET | `/api/v1/users` | read-only | Users list |
| GET | `/api/v1/users/{user_id}` | read-only | User detail |
| PATCH | `/api/v1/users/{user_id}` | `user.update` | Update user |
| POST | `/api/v1/ownership/assign` | `ownership.assign` | Assign owner/reviewer/etc |
| GET | `/api/v1/ownership` | read-only | Ownership list |
| GET | `/api/v1/ownership/entity/{entity_type}/{entity_id}` | read-only | Ownership by entity |
| PATCH | `/api/v1/ownership/{ownership_id}/release` | `ownership.release` | Release ownership |
| PATCH | `/api/v1/ownership/{ownership_id}/transfer` | `ownership.assign` | Transfer ownership |

## Content And Publication

| Method | Path | Permission | Use case |
| --- | --- | --- | --- |
| POST | `/api/v1/content-pieces` | `content.create` | Create content piece |
| GET | `/api/v1/content-pieces` | read-only | Content list |
| PATCH | `/api/v1/content-pieces/{content_piece_id}/status` | `content.update_status` | Update content status |
| POST | `/api/v1/distribution-plans` | `distribution.create` | Create distribution plan |
| POST | `/api/v1/publication-records` | `publication.create` | Create publication record |
| PATCH | `/api/v1/publication-records/{publication_record_id}/status` | `publication.update_status` | Update publication status |

