# XMIP API Auth And RBAC Contract

XMIP currently uses MVP internal API key auth plus static role-based permissions
from request headers. This is not a public-user login system.

## Runtime Settings

| Setting | Purpose |
| --- | --- |
| `AUTH_ENABLED` | Enables API key checks for protected endpoints |
| `API_KEY` | Internal secret expected in the configured API key header |
| `API_KEY_HEADER_NAME` | Defaults to `X-API-Key` |
| `CORS_ALLOWED_ORIGINS` | Frontend/admin origins allowed by CORS |

When `AUTH_ENABLED=false`, local development stays permissive. When
`AUTH_ENABLED=true`, protected writes and RBAC-protected routes require the API
key.

## Headers

| Header | Description |
| --- | --- |
| `X-API-Key` | Internal API key when auth is enabled |
| `X-Actor-Role` | Role evaluated for RBAC |
| `X-Actor-Id` | Optional internal user id for traceability |
| `X-Correlation-ID` | Optional request/action correlation |

If `X-Actor-Role` is omitted while auth is enabled, the backend treats the actor
as `system` for compatibility. Frontend/admin clients should send an explicit
role.

## Roles

```text
owner
admin
editor_in_chief
editor
analyst
reviewer
publisher
agent_operator
viewer
system
```

`owner`, `admin` and `system` have broad operational permissions. `viewer` is
read-only for dashboard-style views and must not execute sensitive actions.

## Frontend/Admin Permissions

| Permission | Typical frontend use |
| --- | --- |
| `admin.dashboard.read` | Dashboard overview, boards, gaps, frontend config and route map |
| `connector.read` | Connector list, runs and summary |
| `connector.create` | Register connector contract |
| `connector.update` | Update/enable/disable connector |
| `connector.run` | Validate and dry-run connector |
| `connector.archive` | Archive connector |
| `agent_runner.read` | Runner capabilities, dry-run preview, recent runs |
| `agent_runner.run` | Execute deterministic internal runner |
| `operational_audit.read` | Audit list, audit summary and trace views |
| `operational_audit.create` | Manual/system audit event creation |
| `intake.create` | Create/reject/archive/re-dedupe intake signals |
| `intake.promote` | Promote intake signal to `NewsItem` |
| `readiness.calculate` | Persist readiness score |
| `workflow.start` | Start workflow |
| `workflow.advance` | Recalculate or advance workflow |
| `workflow_task.*` | Create/start/complete/fail/block/cancel/retry tasks |
| `ownership.assign` | Assign or transfer ownership |
| `ownership.release` | Release ownership |
| `user.create` | Create internal user |
| `user.update` | Update/activate/deactivate user |

## Admin Dashboard Access

The dashboard endpoints under `/api/v1/admin` use `admin.dashboard.read` by
default. Some summary endpoints add narrower permissions:

| Endpoint | Additional permission |
| --- | --- |
| `/api/v1/admin/audit/summary` | `operational_audit.read` |
| `/api/v1/admin/agent-runner/summary` | `agent_runner.read` |
| `/api/v1/admin/connectors/summary` | `connector.read` |

`/api/v1/admin/frontend/config` and `/api/v1/admin/frontend/route-map` are
protected by `admin.dashboard.read`.

## Public/Read-Only Endpoints

Many `GET` endpoints remain public while `AUTH_ENABLED=false` and follow the MVP
pattern when auth is enabled. Health endpoints are public:

```text
GET /health
GET /live
GET /ready
GET /openapi.json
```

Write and critical operational endpoints require API key when auth is enabled.

## Production Security Note

Do not ship a public production frontend that embeds `API_KEY`. The current
header-based auth is appropriate for internal MVP/admin usage only. Production
user-facing access requires a future authentication phase with login,
JWT/OAuth/session management and server-side user authorization.

