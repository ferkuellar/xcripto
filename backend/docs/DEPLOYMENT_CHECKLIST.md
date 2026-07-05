# XMIP Backend Deployment Checklist

## Required Environment

- `APP_NAME=XMIP Backend`
- `APP_VERSION=0.1.0`
- `ENVIRONMENT=production`
- `DEBUG=false`
- `DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST:5432/DB`
- `AUTO_CREATE_TABLES=false`
- `AUTH_ENABLED=true`
- `API_KEY=<secret from secret manager>`
- `API_KEY_HEADER_NAME=X-API-Key`
- `CORS_ALLOWED_ORIGINS=https://admin.example.com`
- `CORS_ALLOW_CREDENTIALS=false`
- `REQUEST_LOGGING_ENABLED=true`
- `REQUEST_BODY_LOGGING_ENABLED=false`
- `RESPONSE_BODY_LOGGING_ENABLED=false`
- `REQUEST_TIMEOUT_SECONDS=30`
- `OPERATIONAL_AUDIT_ENABLED=true`
- `DB_HEALTHCHECK_ENABLED=true`

`ENVIRONMENT=production`, `prod` and `staging` are treated as deployed
environments. They must use PostgreSQL, `AUTH_ENABLED=true`, a non-placeholder
`API_KEY`, explicit CORS origins, `AUTO_CREATE_TABLES=false`, and `DEBUG=false`.
`APP_ENV` is accepted as an alias for providers that reserve `ENVIRONMENT`.

## PostgreSQL

1. Create the database and user.
2. Store credentials outside Git.
3. Set `DATABASE_URL` with the async SQLAlchemy driver.
4. Confirm network access from the API runtime to PostgreSQL.

## Migrations

Run before starting production traffic:

```bash
cd backend
alembic upgrade head
```

Production must use `AUTO_CREATE_TABLES=false`. Runtime table creation is for local
development only.

## Docker

```bash
cd backend
docker compose config
docker compose build
docker compose up
```

The Compose API service runs `alembic upgrade head` before starting Uvicorn.

## Health Checks

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/live
curl http://127.0.0.1:8000/ready
```

`/live` does not depend on the database. `/ready` checks database connectivity when
`DB_HEALTHCHECK_ENABLED=true`, validates critical deployed-environment configuration,
and returns HTTP 503 if the backend is not ready.

## CORS

Verify the admin/frontend origin is present in `CORS_ALLOWED_ORIGINS`.

```bash
curl -i -X OPTIONS http://127.0.0.1:8000/health \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: GET"
```

Confirm exposed headers for frontend pagination and tracing:

```bash
curl -i -X OPTIONS http://127.0.0.1:8000/health \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: GET" | grep -i access-control-expose-headers
```

## Auth and RBAC

With `AUTH_ENABLED=true`, protected writes require:

- `X-API-Key`
- optional `X-Actor-Role` for RBAC-protected actions
- optional `X-Actor-Id` for traceability

Validate:

```bash
curl http://127.0.0.1:8000/api/v1/admin/dashboard/overview \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin"
```

## Internal Agent Runner

Validate runner read access:

```bash
curl http://127.0.0.1:8000/api/v1/agent-runner/capabilities \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: agent_operator"
```

Validate runner dashboard summary:

```bash
curl http://127.0.0.1:8000/api/v1/admin/agent-runner/summary \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: agent_operator"
```

Do not configure external AI credentials for this phase. The runner is local,
deterministic, and must not publish or approve content automatically.

## External Connector Interfaces

Validate connector read access:

```bash
curl http://127.0.0.1:8000/api/v1/connectors \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin"
```

Validate connector dashboard summary:

```bash
curl http://127.0.0.1:8000/api/v1/admin/connectors/summary \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin"
```

Before enabling connector contracts in an environment:

- Confirm no real external network calls are configured for this phase.
- Store secrets only outside the database and reference them with `secret_ref`.
- Keep `dry_run_only=true`; connectors are registered contracts, not active integrations.
- Confirm `configuration` does not include `api_key`, `token`, `secret`, `password`, `authorization`, `bearer` or private keys.
- Use `POST /api/v1/connectors/{connector_id}/validate` before dry-runs.

## Smoke Test

```bash
cd backend
python scripts/smoke_test.py --base-url http://127.0.0.1:8000
```

Manual smoke equivalents:

```bash
curl -i http://127.0.0.1:8000/health
curl -i http://127.0.0.1:8000/live
curl -i http://127.0.0.1:8000/ready
curl -i "http://127.0.0.1:8000/api/v1/news?limit=10&offset=0"
curl -i "http://127.0.0.1:8000/api/v1/operational-audit/events?limit=10&offset=0" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin"
curl -i http://127.0.0.1:8000/openapi.json
```

Optional write smoke:

```bash
python scripts/smoke_test.py \
  --base-url http://127.0.0.1:8000 \
  --api-key dev-secret \
  --create-intake-signal
```

## Frontend/Admin Contract

Export OpenAPI for frontend/admin contract review:

```bash
cd backend
python scripts/export_openapi.py --output docs/openapi.json
```

Validate the read-only admin contract against a running backend:

```bash
python scripts/admin_contract_smoke.py \
  --base-url http://127.0.0.1:8000 \
  --api-key dev-secret \
  --actor-role admin
```

Confirm these frontend-safe endpoints do not expose secrets:

```bash
curl http://127.0.0.1:8000/api/v1/admin/frontend/config \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin"

curl http://127.0.0.1:8000/api/v1/admin/frontend/route-map \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin"
```

## Tests and Lint

```bash
cd backend
pytest
ruff check .
```

## Rollback

1. Stop new traffic.
2. Restore the previous application image.
3. If the deployed revision added a migration and rollback is approved, run:

```bash
alembic downgrade -1
```

4. Validate `/ready`.

## Known Risks

- Operational audit logs are internal traces, not SIEM integration.
- API key auth is minimal and will need user/session auth in a later phase.
- No external workers, queues, AI integrations, analytics, or notification channels are enabled.
- External connectors are dry-run interfaces only; they do not fetch, publish, scrape,
  call LLMs, or create downstream canonical entities automatically.
