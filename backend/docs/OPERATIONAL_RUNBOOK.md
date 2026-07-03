# XMIP Backend Operational Runbook

## Local Startup

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload
```

## Docker Startup

```bash
cd backend
docker compose up --build
```

The API service waits for PostgreSQL health and runs `alembic upgrade head`.

## Readiness

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/live
curl http://127.0.0.1:8000/ready
```

- `/health`: basic service response.
- `/live`: process liveness, no database dependency.
- `/ready`: configuration and database readiness.

## Common Problems

### Database Does Not Connect

- Check `DATABASE_URL`.
- Verify PostgreSQL is reachable.
- Run `alembic current`.
- Check `/ready`; a DB failure returns HTTP 503.

### CORS Blocked

- Confirm `CORS_ALLOWED_ORIGINS` includes the frontend/admin origin.
- Do not use wildcard CORS in production with `AUTH_ENABLED=true`.
- Re-run a browser preflight or curl OPTIONS check.

### API Key Invalid

- Confirm `AUTH_ENABLED=true`.
- Confirm `API_KEY` is set in runtime env.
- Send `X-API-Key`.
- Do not log or paste real API keys into issue tickets.

### RBAC 403

- Send a valid `X-Actor-Role`.
- Check the permission catalog in `app/core/permissions.py`.
- `viewer` is read-only and cannot perform critical writes.

### Alembic Out of Sync

```bash
cd backend
alembic current
alembic upgrade head
```

If a rollback is needed, coordinate data impact before `alembic downgrade -1`.

## Operational Audit

Query recent operational actions:

```bash
curl http://127.0.0.1:8000/api/v1/operational-audit/events \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin"
```

Query by correlation:

```bash
curl http://127.0.0.1:8000/api/v1/operational-audit/correlation/CORRELATION_ID \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin"
```

## Admin Dashboard Overview

```bash
curl http://127.0.0.1:8000/api/v1/admin/dashboard/overview \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin"
```

## Internal Agent Runner

El Internal Agent Runner ejecuta tareas de agente de forma local y determinística.
No llama modelos reales, no publica y no aprueba contenido. Crea `AgentExecution`,
`AgentOutput`, actualiza `WorkflowTask` y registra `OperationalAuditLog`.

Consultar capacidades:

```bash
curl http://127.0.0.1:8000/api/v1/agent-runner/capabilities \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: agent_operator"
```

Dry-run sin modificar estado:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/agent-runner/tasks/TASK_ID/dry-run \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: agent_operator"
```

Ejecutar una tarea:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/agent-runner/tasks/TASK_ID/run \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: agent_operator" \
  -d '{"force":false,"runner":"internal"}'
```

Ejecutar la siguiente tarea elegible de un workflow:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/agent-runner/workflows/WORKFLOW_ID/run-next \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: agent_operator" \
  -d '{"force":false,"runner":"internal"}'
```

Revisar ejecuciones recientes y summary operativo:

```bash
curl http://127.0.0.1:8000/api/v1/agent-runner/runs \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: agent_operator"

curl http://127.0.0.1:8000/api/v1/admin/agent-runner/summary \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: agent_operator"
```

Problemas comunes:

- HTTP 403: usar `X-Actor-Role: agent_operator`, `admin`, `owner` o `editor_in_chief`.
- `WorkflowTask is not eligible`: revisar `task_status`, `task_type` y `assigned_agent`.
- `blocked` con `force=false`: revisar `blocking_reason`; usar `force=true` solo con criterio operativo.
- Output en `pending_review`: revisar `AgentOutput`; no usarlo como fuente factual ni aprobación.

## Smoke Test

```bash
python scripts/smoke_test.py --base-url http://127.0.0.1:8000
```

If write auth is enabled:

```bash
python scripts/smoke_test.py \
  --base-url http://127.0.0.1:8000 \
  --api-key dev-secret \
  --create-intake-signal
```

## Logging

Request logs are JSON lines and include:

- `timestamp`
- `level`
- `logger`
- `message`
- `correlation_id`
- `request_method`
- `request_path`
- `status_code`
- `duration_ms`
- `actor_role`

Request and response bodies are not logged by default. API keys and authorization
headers must never be logged.
