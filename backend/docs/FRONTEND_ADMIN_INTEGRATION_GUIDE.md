# XMIP Frontend/Admin Integration Guide

This guide explains how a future React/Vite admin app should call the XMIP
backend. It does not create or modify frontend files.

## Environment Variables

Development-only example:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_API_KEY=dev-secret
VITE_ACTOR_ROLE=admin
```

Do not expose a production API key in a public browser app. The current API key
auth is an MVP internal control. A future production frontend should use
proper login plus JWT/OAuth/session auth.

## Headers

Recommended headers:

```text
X-API-Key: development API key when AUTH_ENABLED=true
X-Actor-Role: admin
X-Actor-Id: optional user id
X-Correlation-ID: generated per user action
Content-Type: application/json
```

## Minimal TypeScript Fetch Helper

```ts
export async function apiGet<T>(path: string): Promise<T> {
  const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}${path}`, {
    headers: {
      "X-API-Key": import.meta.env.VITE_API_KEY,
      "X-Actor-Role": "admin",
    },
  });

  if (!response.ok) {
    throw await response.json();
  }

  return response.json() as Promise<T>;
}
```

For write calls, include `Content-Type: application/json`, method and a JSON
body. Always preserve and display `correlation_id` when the backend returns or
logs one.

## Status Handling

| Status | Frontend behavior |
| --- | --- |
| 401 | Show "API key missing" or force internal reconfiguration |
| 403 | Show permission denied and current actor role |
| 404 | Show empty/detail not found state |
| 409 | Show blocked workflow/editorial gate/state conflict |
| 422 | Show field-level validation errors |
| 503 | Show backend not ready and retry after readiness recovers |

## Bootstrapping The Admin App

1. Fetch `/health`, `/live` or `/ready` for environment status.
2. Fetch `/api/v1/admin/frontend/config` to discover feature flags.
3. Fetch `/api/v1/admin/frontend/route-map` to map sections to permissions.
4. Fetch `/api/v1/admin/dashboard/overview` for initial dashboard cards.
5. Load boards lazily per tab to avoid unnecessary query load.

## Dashboard Screens

### Overview

Use:

```text
GET /api/v1/admin/dashboard/overview
GET /api/v1/admin/dashboard/newsroom-health
```

Render KPI cards, health status, critical blockers and recommended actions.

### Intake Queue

Use:

```text
GET /api/v1/admin/intake/queue?dedupe_status=unique&limit=50&offset=0
```

Show signal title, source, priority, dedupe status and promoted news id. Do not
display full raw payloads by default.

### Editorial Work Queue

Use:

```text
GET /api/v1/admin/editorial/work-queue
```

Show `missing_requirements`, `blocking_reasons`, `next_agent`, owner and task
counts. Link to news detail and workflow detail.

### Blockers

Use:

```text
GET /api/v1/admin/blockers
```

Group by `blocker_type` and severity. Show recommended actions.

### Readiness Board

Use:

```text
GET /api/v1/admin/readiness/board?readiness_status=blocked
```

Use the latest score per news item only. Do not treat readiness score as
approval or publication permission.

### Task Board

Use:

```text
GET /api/v1/admin/tasks/board?blocking=true
```

Show assignment, status, priority, attempts and blocking reason.

### Publications

Use:

```text
GET /api/v1/admin/publications/board?publication_status=scheduled
```

Show scheduled/published status, URL, external id, owner and content links.

### Ownership

Use:

```text
GET /api/v1/admin/ownership/board
GET /api/v1/admin/users/{user_id}/workload
```

Show unassigned news/tasks/content and per-user workload.

### Agent Runner

Use:

```text
GET /api/v1/admin/agent-runner/summary
GET /api/v1/agent-runner/capabilities
```

Run actions are protected by `agent_runner.run`. Agent outputs are auxiliary and
must not be treated as factual verification.

### Connectors

Use:

```text
GET /api/v1/admin/connectors/summary
GET /api/v1/connectors
```

Connectors are dry-run interfaces only. Never ask users to paste secrets into
`configuration`; use `secret_ref`.

### Operational Audit

Use:

```text
GET /api/v1/admin/audit/summary
GET /api/v1/operational-audit/events?correlation_id=...
```

Show recent actions, outcomes, actor role and entity references. Do not expose
audit data to public users.

## CORS

Set backend `CORS_ALLOWED_ORIGINS` to include the Vite dev origin, usually:

```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

Production must use explicit origins. Wildcard CORS is rejected in production
when `AUTH_ENABLED=true`.

## Contract Validation

Export OpenAPI:

```bash
cd backend
python scripts/export_openapi.py --output docs/openapi.json
```

Run admin contract smoke against a running backend:

```bash
python scripts/admin_contract_smoke.py \
  --base-url http://127.0.0.1:8000 \
  --api-key dev-secret \
  --actor-role admin
```

