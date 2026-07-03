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
- `OPERATIONAL_AUDIT_ENABLED=true`
- `DB_HEALTHCHECK_ENABLED=true`

Do not use wildcard CORS origins in production when `AUTH_ENABLED=true`.

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
`DB_HEALTHCHECK_ENABLED=true` and returns HTTP 503 if the backend is not ready.

## CORS

Verify the admin/frontend origin is present in `CORS_ALLOWED_ORIGINS`.

```bash
curl -i -X OPTIONS http://127.0.0.1:8000/health \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: GET"
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

## Smoke Test

```bash
cd backend
python scripts/smoke_test.py --base-url http://127.0.0.1:8000
```

Optional write smoke:

```bash
python scripts/smoke_test.py \
  --base-url http://127.0.0.1:8000 \
  --api-key dev-secret \
  --create-intake-signal
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
