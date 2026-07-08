# XMIP API Contract Freeze v0.1

Date: 2026-07-07

Validated branch: `feat/api-contract-freeze`

Base commit on `main`: `438b830` (`Merge pull request #13 from ferkuellar/feat/production-hardening`)

Validation environment:

- Local VPS-like stack: `docker compose -f docker-compose.vps.yml up -d --build postgres api frontend caddy`
- Direct API: `http://127.0.0.1:8000`
- Reverse proxy: `https://127.0.0.1`
- API key used for smoke: `local-staging-smoke-key`
- Actor role used for RBAC smoke: `system` and `admin`

This document freezes the MVP v0.1 contract surface as observed from the live backend and OpenAPI served by the running stack. Do not change these contracts without a deliberate versioned API decision.

## Platform

| Method | Path | Notes |
| --- | --- | --- |
| GET | `/health` | Public. Returns service metadata. |
| GET | `/live` | Public. Liveness only. |
| GET | `/ready` | Public. Validates deployed-environment config and DB health when enabled. |
| GET | `/openapi.json` | Public OpenAPI document at the root path. |

## News

| Method | Path | Auth | Notes |
| --- | --- | --- | --- |
| GET | `/api/v1/news` | No | Public list endpoint. Supports filters and pagination. |
| GET | `/api/v1/news/{news_id}` | No | Public detail endpoint. |
| PATCH | `/api/v1/news/{news_id}/status` | Yes | API key required. |
| POST | `/api/v1/news/intake` | Yes | API key required. |
| GET | `/api/v1/news/{news_id}/verification-records` | No | Public read-model list. |
| GET | `/api/v1/news/{news_id}/risk-reviews` | No | Public read-model list. |
| GET | `/api/v1/news/{news_id}/content-pieces` | No | Exists in OpenAPI, not part of the frontend MVP core surface. |
| GET | `/api/v1/news/{news_id}/publication-records` | No | Exists in OpenAPI, not part of the frontend MVP core surface. |
| GET | `/api/v1/news/{news_id}/tasks` | No | Exists in OpenAPI, not part of the frontend MVP core surface. |
| GET | `/api/v1/news/{news_id}/metric-snapshots` | No | Exists in OpenAPI, not part of the frontend MVP core surface. |
| GET | `/api/v1/news/{news_id}/memory-items` | No | Exists in OpenAPI, not part of the frontend MVP core surface. |
| GET | `/api/v1/news/{news_id}/workflow` | No | Returns latest workflow run for a news item. |

`GET /api/v1/news` query parameters confirmed in code and smoke:

- `status`
- `q`
- `category`
- `priority`
- `source`
- `created_from`
- `created_to`
- `limit`
- `offset`

Observed behavior:

- `X-Total-Count` is present on `GET /api/v1/news`.
- `X-Correlation-ID` is present on successful and error responses.
- `Access-Control-Expose-Headers: X-Total-Count, X-Correlation-ID` is configured globally.
- Invalid `status` and `priority` return `400` with the normalized error envelope.
- Missing `news_id` returns `404` with the normalized error envelope.

## Editorial Readiness

| Method | Path | Auth | Notes |
| --- | --- | --- | --- |
| GET | `/api/v1/editorial-readiness/news/{news_id}/latest` | No | Latest readiness read model. |
| POST | `/api/v1/editorial-readiness/news/{news_id}/calculate` | Yes | Requires permission `readiness.calculate`. Returns `201`. |
| GET | `/api/v1/editorial-readiness/news/{news_id}/explain` | No | Exists in OpenAPI. |
| GET | `/api/v1/editorial-readiness` | No | List endpoint. |
| GET | `/api/v1/editorial-readiness/{score_id}` | No | Detail endpoint. |

Important: `calculate` is `POST`, not `GET`.

## Intake

| Method | Path | Auth | Notes |
| --- | --- | --- | --- |
| GET | `/api/v1/intake/signals` | No | Public read-model list. |
| GET | `/api/v1/intake/signals/{signal_id}` | No | Public detail. |
| POST | `/api/v1/intake/signals` | Yes | API key required. |
| POST | `/api/v1/intake/signals/{signal_id}/dedupe` | Yes | API key required. |
| PATCH | `/api/v1/intake/signals/{signal_id}/reject` | Yes | API key required. |
| PATCH | `/api/v1/intake/signals/{signal_id}/archive` | Yes | API key required. |
| POST | `/api/v1/intake/signals/{signal_id}/promote` | Yes | Requires permission `intake.promote`. |
| GET | `/api/v1/intake/adapter-runs` | No | Public list endpoint. |
| POST | `/api/v1/intake/adapter-runs` | Yes | API key required. |
| GET | `/api/v1/intake/adapter-runs/{adapter_run_id}` | No | Public detail endpoint. |

## Sources

| Method | Path | Auth | Notes |
| --- | --- | --- | --- |
| GET | `/api/v1/sources` | No | Public list endpoint. |
| GET | `/api/v1/sources/{source_id}` | No | Public detail endpoint. |
| POST | `/api/v1/sources` | Yes | API key required. |

## Agents

| Method | Path | Auth | Notes |
| --- | --- | --- | --- |
| GET | `/api/v1/agents/executions` | No | Public list endpoint. |
| GET | `/api/v1/agents/executions/{execution_id}` | No | Public detail endpoint. |
| POST | `/api/v1/agents/executions` | Yes | API key required. |

## Audit Checks

| Method | Path | Auth | Notes |
| --- | --- | --- | --- |
| GET | `/api/v1/audit/checks` | No | Public list endpoint. |
| GET | `/api/v1/audit/checks/{audit_check_id}` | No | Public detail endpoint. |
| POST | `/api/v1/audit/checks` | Yes | Requires permission `audit.create`. |

## Operational Audit

| Method | Path | Auth | Notes |
| --- | --- | --- | --- |
| GET | `/api/v1/operational-audit/events` | Yes | Requires permission `operational_audit.read`. |
| POST | `/api/v1/operational-audit/events` | Yes | Requires permission `operational_audit.create`. |
| GET | `/api/v1/operational-audit/events/{event_id}` | Yes | Requires permission `operational_audit.read`. |
| GET | `/api/v1/operational-audit/correlation/{correlation_id}` | Yes | Requires permission `operational_audit.read`. |
| GET | `/api/v1/operational-audit/actors/{actor_id}` | Yes | Requires permission `operational_audit.read`. |
| GET | `/api/v1/operational-audit/entity/{entity_type}/{entity_id}` | Yes | Requires permission `operational_audit.read`. |

Smoke-confirmed behavior:

- Missing API key returns `401`.
- Invalid actor role returns `403`.
- Valid key + valid role returns `200`.

## Admin / Read Models

The live backend does not expose the phase-brief names `admin/dashboard/summary`, `admin/news/summary`, `admin/intake/summary`, or `admin/agents/summary`.

Actual admin routes in OpenAPI:

| Method | Path | Auth |
| --- | --- | --- |
| GET | `/api/v1/admin/dashboard/overview` | Yes |
| GET | `/api/v1/admin/dashboard/newsroom-health` | Yes |
| GET | `/api/v1/admin/intake/queue` | Yes |
| GET | `/api/v1/admin/editorial/work-queue` | Yes |
| GET | `/api/v1/admin/blockers` | Yes |
| GET | `/api/v1/admin/readiness/board` | Yes |
| GET | `/api/v1/admin/tasks/board` | Yes |
| GET | `/api/v1/admin/publications/board` | Yes |
| GET | `/api/v1/admin/ownership/board` | Yes |
| GET | `/api/v1/admin/gaps` | Yes |
| GET | `/api/v1/admin/audit/summary` | Yes |
| GET | `/api/v1/admin/agent-runner/summary` | Yes |
| GET | `/api/v1/admin/connectors/summary` | Yes |
| GET | `/api/v1/admin/frontend/config` | Yes |
| GET | `/api/v1/admin/frontend/route-map` | Yes |

## Auth Matrix

| Endpoint group | Auth required | Required header | Required role if applicable | Missing key | Invalid role / permission |
| --- | --- | --- | --- | --- | --- |
| Health/platform | No | None | None | N/A | N/A |
| News list/detail | No | None | None | N/A | N/A |
| News mutations | Yes | `X-API-Key` | None for API-key-only operations | `401` | `403` if key invalid |
| Intake mutations | Yes | `X-API-Key` | `X-Actor-Role` for promote / permissioned actions | `401` | `403` |
| Sources create | Yes | `X-API-Key` | None | `401` | `403` if key invalid |
| Agents executions create | Yes | `X-API-Key` | None | `401` | `403` if key invalid |
| Audit checks create | Yes | `X-API-Key` | `X-Actor-Role` for permissioned actions | `401` | `403` |
| Editorial readiness calculate | Yes | `X-API-Key` | `X-Actor-Role` for permissioned actions | `401` | `403` |
| Operational audit | Yes | `X-API-Key` | `X-Actor-Role` required for RBAC routes | `401` | `403` |
| Admin read models | Yes | `X-API-Key` | `X-Actor-Role` required for RBAC routes | `401` | `403` |

Smoke-confirmed auth examples:

- `GET /api/v1/operational-audit/events` without API key -> `401`.
- `GET /api/v1/admin/dashboard/overview` with invalid actor role -> `403`.
- `GET /api/v1/admin/dashboard/overview` with `viewer` role -> `200`.

## Error Envelope

The backend normalizes HTTP exceptions into:

```json
{
  "success": false,
  "error": "message",
  "correlation_id": "corr_..."
}
```

Validation errors normalize into:

```json
{
  "success": false,
  "error": "Request validation failed",
  "details": [],
  "correlation_id": "corr_..."
}
```

Observed and code-backed status handling:

- `400` domain validation errors
- `401` missing API key
- `403` invalid API key, invalid role, insufficient permission
- `404` not found
- `409` conflict
- `422` request validation
- `500` unhandled exceptions, with tracebacks hidden when `DEBUG=false`

The body shape is not the FastAPI default `detail` wrapper for handled exceptions; frontend clients should use `success`, `error`, `details` when present, and `correlation_id`.

## Headers

Confirmed headers:

- `X-Correlation-ID` is emitted by the backend middleware.
- `X-Total-Count` is emitted by `GET /api/v1/news`.
- `Access-Control-Expose-Headers: X-Total-Count, X-Correlation-ID` is configured globally.
- `Access-Control-Allow-Origin` echoes the allowed origin, not `*`.
- `Vary: Origin` is present on CORS-enabled responses.

## Pagination

Confirmed list endpoints accept `limit` and `offset`:

- `GET /api/v1/news`
- `GET /api/v1/news/{news_id}/verification-records`
- `GET /api/v1/news/{news_id}/risk-reviews`
- `GET /api/v1/editorial-readiness`
- `GET /api/v1/intake/signals`
- `GET /api/v1/intake/adapter-runs`
- `GET /api/v1/sources`
- `GET /api/v1/agents/executions`
- `GET /api/v1/audit/checks`
- `GET /api/v1/operational-audit/events`
- admin list endpoints under `/api/v1/admin/*`

Current contract reality:

- `GET /api/v1/news` returns a plain array plus `X-Total-Count`.
- The other list endpoints return plain arrays and do not set `X-Total-Count`.

## Enums and Catalogs

Canonical backend catalogs live in `backend/app/core/constants.py`.

Relevant MVP catalog values:

- `NEWS_STATUSES`
- `NEWS_PRIORITIES`
- `SOURCE_STATUSES`
- `TRUST_LEVELS`
- `VERIFICATION_STATUSES`
- `EVIDENCE_LEVELS`
- `CONFIDENCE_LEVELS`
- `RISK_LEVELS`
- `RISK_SEVERITIES`
- `RISK_DECISION_RECOMMENDATIONS`
- `AUDIT_STATUSES`
- `AUDIT_SEVERITIES`
- `AUDIT_DECISION_RECOMMENDATIONS`
- `EDITORIAL_READINESS_SCORE_BANDS`
- `EDITORIAL_READINESS_STATUSES`
- `INTAKE_SIGNAL_TYPES`
- `INTAKE_SIGNAL_STATUSES`
- `INTAKE_DEDUPE_STATUSES`
- `INTAKE_ADAPTER_TYPES`
- `INTAKE_ADAPTER_RUN_STATUSES`
- `AGENT_EXECUTION_STATUSES`
- `OPERATIONAL_AUDIT_EVENT_TYPES`
- `OPERATIONAL_AUDIT_OUTCOMES`
- `OPERATIONAL_AUDIT_DECISIONS`

These values are enforced by Pydantic validators and appear in OpenAPI enums where applicable.

## Frontend Dependencies

Observed frontend consumers:

- Command Center: `/api/v1/news`, `/api/v1/intake/signals`, `/api/v1/agents/executions`, `/api/v1/audit/checks`
- News Feed: `/api/v1/news`
- News Detail: `/api/v1/news/{id}`, `/api/v1/news/{id}/verification-records`, `/api/v1/news/{id}/risk-reviews`, `/api/v1/editorial-readiness/news/{id}/latest`, `/api/v1/editorial-readiness/news/{id}/calculate`, `/api/v1/audit/checks?entity_type=news_item&entity_id=...`, `/api/v1/intake/signals?promoted_news_item_id=...`
- Sources: `/api/v1/sources`
- Agents: `/api/v1/agents/executions`
- Audit: `/api/v1/audit/checks`
- Admin shell: `/api/v1/admin/frontend/config`, `/api/v1/admin/frontend/route-map`, `/api/v1/admin/dashboard/overview`, `/api/v1/admin/dashboard/newsroom-health`, `/api/v1/admin/intake/queue`, `/api/v1/admin/editorial/work-queue`, `/api/v1/admin/blockers`, `/api/v1/admin/readiness/board`, `/api/v1/admin/tasks/board`, `/api/v1/admin/publications/board`, `/api/v1/admin/ownership/board`, `/api/v1/admin/gaps`, `/api/v1/admin/agent-runner/summary`, `/api/v1/admin/connectors/summary`, `/api/v1/admin/audit/summary`

## Known Gaps

- There is no `/api/v1/admin/dashboard/summary`; the real route is `/api/v1/admin/dashboard/overview`.
- There is no `/api/v1/admin/news/summary`.
- There is no `/api/v1/admin/intake/summary`.
- There is no `/api/v1/admin/agents/summary`; the real route is `/api/v1/admin/agent-runner/summary`.
- `GET /api/v1/editorial-readiness/news/{news_id}/calculate` is invalid; use `POST`.
- Only `GET /api/v1/news` emits `X-Total-Count`.
- Public read-model endpoints exist for MVP support; do not add new auth requirements without a versioned contract decision.

## Freeze Rule

This contract is frozen for frontend integration against v0.1.0 unless a blocking bug is found in one of the validated paths above.

