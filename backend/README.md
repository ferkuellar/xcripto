# XMIP Backend

Backend API de la plataforma multiagente **XMIP** (newsroom de **XCripto**, bajo gobierno **ORION**).

> **Release candidate local actual: `v0.1.0-rc1`** — ver
> `docs/RELEASE_NOTES_v0.1.0-rc1.md` y `docs/LOCAL_RC_v0.1.0-rc1_REPORT.md`.
> Correr tests: `pytest` (sin un `.env.local` con `AUTH_ENABLED=true`, que rompería el suite).
> Correr Docker/PostgreSQL: `API_PORT=8010 POSTGRES_PORT=55432 docker compose up --build`.

Estado actual: MVP backend funcional con FastAPI, SQLAlchemy async, trazabilidad por
`X-Correlation-ID`, migración Alembic inicial, máquina de estados editorial para
`NewsItem`, autorización mínima por API key, editorial gates basados en `AuditCheck`
y almacenamiento auditable de `AgentOutput`.
También incluye scoring determinístico de readiness editorial por `NewsItem`.
Fase 10 agrega intake, normalización y deduplicación de señales candidatas antes de
promoverlas a noticias.
Fase 11 agrega usuarios internos, roles mínimos, ownership operativo y permisos por
headers para acciones críticas.
Fase 12 agrega read models administrativos para el futuro dashboard operativo.
Fase 13 agrega `OperationalAuditLog` para trazabilidad operativa persistente de
acciones críticas, actores, permisos, decisiones, resultados y `correlation_id`.
Fase 14 endurece configuración, CORS, logging estructurado, health/readiness,
Docker, smoke tests y documentación operativa para deploy del MVP.
Fase 15 agrega un Internal Agent Runner síncrono y determinístico para ejecutar
`WorkflowTask` elegibles sin modelos reales ni integraciones externas.
Fase 16 agrega External Connector Interfaces para registrar contratos de conectores
futuros, validar configuración segura y ejecutar dry-runs locales sin llamadas externas.

## Stack

- FastAPI + Pydantic v2
- SQLAlchemy 2 async
- SQLite local/dev por defecto
- PostgreSQL 16 vía Docker Compose o `DATABASE_URL`
- Alembic para migraciones formales
- pytest + httpx para tests
- Ruff para lint básico

## Ejecutar en local con SQLite

### Windows PowerShell

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

### Linux / macOS

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

La API queda en `http://127.0.0.1:8000` y la documentación interactiva en `/docs`.

## Ejecutar con PostgreSQL / Docker

```bash
cd backend
docker compose up --build
```

Docker Compose levanta PostgreSQL 16 y la API en `http://localhost:8000`.
Para entornos persistentes, usa `AUTO_CREATE_TABLES=false` y aplica migraciones Alembic.
El servicio API ejecuta `alembic upgrade head` antes de iniciar Uvicorn.

Los puertos del host son configurables (útil si `:8000`/`:5432` ya están ocupados):

```bash
API_PORT=8010 POSTGRES_PORT=55432 docker compose up --build
```

Para una corrida production-like local, copia `.env.local.production.example` a
`.env.local` (gitignored) y usa `PUBLIC_WEB_BASE_URL=http://localhost:3000`,
`AUTH_ENABLED=true`, `API_KEY=dev-secret` y `DATABASE_URL=sqlite+aiosqlite:///./xmip_local_prod.db`.
Para el contrato real de producción usa `.env.production.example` como plantilla:
`ENVIRONMENT=production`, `DEBUG=false`, `DATABASE_URL=postgresql+asyncpg://...`,
`PUBLIC_WEB_BASE_URL=https://xcripto.com.mx`, `CORS_ALLOWED_ORIGINS=https://xcripto.com.mx,https://www.xcripto.com.mx,https://admin.xcripto.com.mx`.
Ver `docs/LOCAL_DOCKER_POSTGRES_E2E_REPORT.md` para el flujo E2E validado
(Alembic, smoke tests, newsroom QA y persistencia).

## Migraciones Alembic

La migración inicial crea:

- `news_items`
- `source_references`
- `agent_executions`
- `audit_checks`

Comandos principales:

```bash
cd backend
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
alembic downgrade -1
```

Alembic lee `DATABASE_URL` desde la configuración del backend. El archivo `alembic.ini`
incluye un fallback local SQLite, pero en entornos reales la configuración debe venir
del entorno de despliegue, no de un `.env` compartido.

`AUTO_CREATE_TABLES` se conserva solo como ayuda de desarrollo/test. Para staging/prod,
configura:

```env
AUTO_CREATE_TABLES=false
```

## Tests y lint

```bash
cd backend
pytest
ruff check .
```

Los tests usan SQLite en memoria y no requieren base externa.

## Configuración

Copia `.env.example` a `.env.local`. Variables principales:

| Variable               | Default                           | Descripción                                                                               |
| ---------------------- | --------------------------------- | ------------------------------------------------------------------------------------------ |
| `APP_NAME`           | `XMIP Backend`                  | Nombre mostrado por OpenAPI                                                               |
| `APP_VERSION`        | `0.1.0`                         | Versión operativa expuesta en healthchecks                                                |
| `DATABASE_URL`       | `sqlite+aiosqlite:///./xmip.db` | URL async de SQLAlchemy. Para PostgreSQL:`postgresql+asyncpg://user:pass@host:5432/xmip` |
| `AUTO_CREATE_TABLES` | `false`                         | Debe quedar `false` en staging/prod; usa Alembic para crear esquema                       |
| `ENVIRONMENT`        | `development`                   | `development` / `staging` / `production` / `test`; `APP_ENV` también se acepta como alias |
| `DEBUG`              | `false`                         | Evita exponer internals en producción                                                     |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000,http://localhost:5173` | Orígenes frontend/admin permitidos                                          |
| `PUBLIC_WEB_BASE_URL` | `http://localhost:3000`        | Base canónica del sitio público; en producción debe ser `https://xcripto.com.mx`           |
| `CORS_ALLOW_CREDENTIALS` | `false`                    | Credenciales CORS                                                                         |
| `CORS_ALLOWED_METHODS` | `GET,POST,PATCH,PUT,DELETE,OPTIONS` | Métodos CORS permitidos                                                           |
| `CORS_ALLOWED_HEADERS` | `Authorization,Content-Type,X-API-Key,X-Correlation-ID,X-Actor-Id,X-Actor-Role,X-Actor-Display` | Headers CORS |
| `LOG_LEVEL`          | `INFO`                          | Nivel de logging                                                                           |
| `AUTH_ENABLED`       | `false`                         | Activa API key auth para endpoints de escritura                                            |
| `API_KEY`            | `null`                          | Secreto esperado cuando `AUTH_ENABLED=true`                                                |
| `API_KEY_HEADER_NAME` | `X-API-Key`                    | Header usado para enviar la API key                                                        |
| `REQUEST_LOGGING_ENABLED` | `true`                    | Activa logs estructurados por request                                                       |
| `REQUEST_BODY_LOGGING_ENABLED` | `false`             | Mantener `false` salvo diagnóstico controlado                                              |
| `RESPONSE_BODY_LOGGING_ENABLED` | `false`            | Mantener `false` salvo diagnóstico controlado                                              |
| `REQUEST_TIMEOUT_SECONDS` | `30`                    | Timeout operativo global para clientes/scripts que lo adopten                              |
| `OPERATIONAL_AUDIT_ENABLED` | `true`                | Habilita bitácora operacional                                                              |
| `DB_HEALTHCHECK_ENABLED` | `true`                    | `/ready` valida DB con `SELECT 1`                                                          |

En `ENVIRONMENT=staging`, `production` o `prod`, la configuración falla si usa SQLite,
`AUTH_ENABLED=false`, `API_KEY` vacío o placeholder, `AUTO_CREATE_TABLES=true`,
`DEBUG=true`, `CORS_ALLOWED_ORIGINS=*`, orígenes localhost, o `PUBLIC_WEB_BASE_URL`
apuntando a localhost. Configura explícitamente el origen del frontend/admin,
usa PostgreSQL y publica con un dominio HTTPS real:

```env
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/xmip
AUTH_ENABLED=true
API_KEY=<secret-from-secret-manager>
CORS_ALLOWED_ORIGINS=https://admin.xcripto.example
PUBLIC_WEB_BASE_URL=https://xcripto.com.mx
```

## Autorización mínima

Por defecto `AUTH_ENABLED=false` para mantener simple el desarrollo local y los tests.
Cuando `AUTH_ENABLED=true`, estos endpoints de escritura requieren API key:

- `POST /api/v1/news/intake`
- `PATCH /api/v1/news/{news_id}/status`
- `POST /api/v1/sources`
- `POST /api/v1/agents/executions`
- `POST /api/v1/audit/checks`
- `POST /api/v1/verification-records`
- `POST /api/v1/risk-reviews`
- `POST /api/v1/content-pieces`
- `PATCH /api/v1/content-pieces/{content_piece_id}/status`
- `POST /api/v1/distribution-plans`
- `PATCH /api/v1/distribution-plans/{distribution_plan_id}/status`
- `POST /api/v1/publication-records`
- `PATCH /api/v1/publication-records/{publication_record_id}/status`
- `POST /api/v1/workflows/news/{news_id}/start`
- `POST /api/v1/workflows/{workflow_run_id}/recalculate`
- `POST /api/v1/workflows/{workflow_run_id}/advance`
- `POST /api/v1/agent-outputs`
- `PATCH /api/v1/agent-outputs/{agent_output_id}/accept`
- `PATCH /api/v1/agent-outputs/{agent_output_id}/reject`
- `PATCH /api/v1/agent-outputs/{agent_output_id}/supersede`
- `POST /api/v1/editorial-readiness/news/{news_id}/calculate`
- `POST /api/v1/intake/signals`
- `POST /api/v1/intake/signals/{signal_id}/dedupe`
- `POST /api/v1/intake/signals/{signal_id}/promote`
- `PATCH /api/v1/intake/signals/{signal_id}/reject`
- `PATCH /api/v1/intake/signals/{signal_id}/archive`
- `POST /api/v1/intake/adapter-runs`
- `POST /api/v1/users`
- `PATCH /api/v1/users/{user_id}`
- `PATCH /api/v1/users/{user_id}/activate`
- `PATCH /api/v1/users/{user_id}/deactivate`
- `POST /api/v1/ownership/assign`
- `PATCH /api/v1/ownership/{ownership_id}/release`
- `PATCH /api/v1/ownership/{ownership_id}/transfer`
- `POST /api/v1/operational-audit/events`
- `POST /api/v1/connectors`
- `PATCH /api/v1/connectors/{connector_id}`
- `PATCH /api/v1/connectors/{connector_id}/enable`
- `PATCH /api/v1/connectors/{connector_id}/disable`
- `PATCH /api/v1/connectors/{connector_id}/archive`
- `POST /api/v1/connectors/{connector_id}/validate`
- `POST /api/v1/connectors/{connector_id}/dry-run`

Los endpoints `GET`, incluido `GET /health`, quedan públicos por ahora.

Ejemplo:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/news/intake \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{
    "title": "Bitcoin ETF sees record inflows",
    "summary": "Institutional inflows reached a new daily record.",
    "category": "markets",
    "priority": "P1",
    "source_url": "https://example.com/etf-inflows",
    "source_name": "Example Wire"
  }'
```

Respuestas esperadas con auth activa:

- Sin header: HTTP 401, `Missing API key`
- Header incorrecto: HTTP 403, `Invalid API key`
- `AUTH_ENABLED=true` sin `API_KEY`: HTTP 500 controlado de configuración

## RBAC mínimo

Fase 11 agrega `UserAccount`, `OwnershipAssignment` y permisos estáticos por rol.
No implementa login, passwords, JWT, OAuth ni sesiones. La API key sigue siendo la
base de protección para escrituras cuando `AUTH_ENABLED=true`.

Headers opcionales:

```text
X-Actor-Id
X-Actor-Role
```

Comportamiento:

- `AUTH_ENABLED=false`: no bloquea por API key ni por actor, para mantener DX local.
- `AUTH_ENABLED=true`: la API key sigue siendo obligatoria.
- Si viene `X-Actor-Role`, se valida contra permisos.
- Si no viene actor con auth activa, se usa `system` para compatibilidad interna.

Roles permitidos:

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

Acciones protegidas principales:

```text
intake.promote
readiness.calculate
audit.create
publication.create
publication.update_status
agent_output.accept
agent_output.reject
memory.approve
memory.invalidate
user.create
user.update
ownership.assign
ownership.release
operational_audit.read
operational_audit.create
```

`owner`, `admin` y `system` tienen permisos completos. `viewer` es de solo lectura.
Los demás roles tienen permisos acotados a su área editorial u operativa.
`operational_audit.read` queda disponible para `owner`, `admin`, `system`,
`editor_in_chief`, `analyst` y `reviewer`; `viewer` no puede leer el audit log
operacional por defecto.

### UserAccount

`UserAccount` identifica actores internos para ownership, trazabilidad y permisos
mínimos. No implica sesión autenticada todavía.

Endpoints:

- `POST /api/v1/users`
- `GET /api/v1/users` - filtros `role`, `status`, `is_active`, `email`, `handle`, `limit`, `offset`
- `GET /api/v1/users/{user_id}`
- `PATCH /api/v1/users/{user_id}`
- `PATCH /api/v1/users/{user_id}/activate`
- `PATCH /api/v1/users/{user_id}/deactivate`

Crear usuario:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin" \
  -d '{
    "display_name": "Fernando Cuellar",
    "email": "fercuellar@example.com",
    "handle": "fercuellar",
    "role": "owner"
  }'
```

### OwnershipAssignment

`OwnershipAssignment` registra responsabilidad operativa sobre una entidad editorial
o de workflow. El ownership formal vive en esta tabla; `WorkflowTask.assigned_to`
continúa como string compatible con el modelo existente.

Tipos:

```text
owner
assignee
reviewer
approver
publisher
watcher
backup
escalation_owner
```

Estados:

```text
active
released
transferred
cancelled
archived
```

Endpoints:

- `POST /api/v1/ownership/assign`
- `GET /api/v1/ownership`
- `GET /api/v1/ownership/{ownership_id}`
- `GET /api/v1/users/{user_id}/ownership`
- `GET /api/v1/ownership/entity/{entity_type}/{entity_id}`
- `PATCH /api/v1/ownership/{ownership_id}/release`
- `PATCH /api/v1/ownership/{ownership_id}/transfer`

Asignar ownership:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/ownership/assign \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin" \
  -d '{
    "user_id": "USER_ID",
    "entity_type": "NewsItem",
    "entity_id": "NEWS_ID",
    "ownership_type": "owner",
    "assigned_by": "operator"
  }'
```

Probar permiso suficiente:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/intake/signals/SIGNAL_ID/promote \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: editor" \
  -d '{"create_workflow": false}'
```

Probar permiso insuficiente:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/intake/signals/SIGNAL_ID/promote \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: viewer" \
  -d '{"create_workflow": false}'
```

Respuesta esperada: HTTP 403 `Insufficient permission`.

## Endpoints actuales

### Health

- `GET /health`
- `GET /live` - liveness del proceso, no depende de DB
- `GET /ready` - readiness operacional; valida DB si `DB_HEALTHCHECK_ENABLED=true`

Ejemplo de readiness saludable:

```json
{
  "status": "ready",
  "service": "xmip-backend",
  "version": "0.1.0",
  "checks": {
    "configuration": "ok",
    "database": "ok"
  }
}
```

Si la DB no responde, `/ready` devuelve HTTP 503 con `status=not_ready`.

### News Intake (`/api/v1/news`)

- `POST /api/v1/news/intake` - registra una noticia candidata
- `GET /api/v1/news` - lista noticias, con filtros `status`, `limit`, `offset`
- `GET /api/v1/news/{news_id}`
- `PATCH /api/v1/news/{news_id}/status` - cambia estado con máquina de estados

### Intake Signals

- `POST /api/v1/intake/signals`
- `GET /api/v1/intake/signals` - filtros `signal_type`, `signal_status`, `dedupe_status`, `source_name`, `source_type`, `topic`, `priority`, `linked_news_item_id`, `promoted_news_item_id`, `limit`, `offset`
- `GET /api/v1/intake/signals/{signal_id}`
- `POST /api/v1/intake/signals/{signal_id}/dedupe`
- `POST /api/v1/intake/signals/{signal_id}/promote`
- `PATCH /api/v1/intake/signals/{signal_id}/reject`
- `PATCH /api/v1/intake/signals/{signal_id}/archive`
- `POST /api/v1/intake/adapter-runs`
- `GET /api/v1/intake/adapter-runs` - filtros `adapter_name`, `adapter_type`, `status`, `limit`, `offset`
- `GET /api/v1/intake/adapter-runs/{adapter_run_id}`

### Source References (`/api/v1/sources`)

- `POST /api/v1/sources`
- `GET /api/v1/sources` - filtros `source_status`, `limit`, `offset`
- `GET /api/v1/sources/{source_id}`

### Agent Executions (`/api/v1/agents/executions`)

- `POST /api/v1/agents/executions`
- `GET /api/v1/agents/executions` - filtros `agent_name`, `status`, `limit`, `offset`
- `GET /api/v1/agents/executions/{execution_id}`

### Agent Outputs

- `POST /api/v1/agent-outputs`
- `GET /api/v1/agent-outputs` - filtros `agent_name`, `output_type`, `status`, `entity_type`, `entity_id`, `news_item_id`, `workflow_run_id`, `agent_execution_id`, `human_review_required`, `accepted`, `limit`, `offset`
- `GET /api/v1/agent-outputs/{agent_output_id}`
- `GET /api/v1/news/{news_id}/agent-outputs`
- `GET /api/v1/workflows/{workflow_run_id}/agent-outputs`
- `PATCH /api/v1/agent-outputs/{agent_output_id}/accept`
- `PATCH /api/v1/agent-outputs/{agent_output_id}/reject`
- `PATCH /api/v1/agent-outputs/{agent_output_id}/supersede`

### Audit Checks (`/api/v1/audit/checks`)

- `POST /api/v1/audit/checks`
- `GET /api/v1/audit/checks` - filtros `entity_type`, `entity_id`, `limit`, `offset`
- `GET /api/v1/audit/checks/{audit_check_id}`

### Verification Records

- `POST /api/v1/verification-records`
- `GET /api/v1/verification-records` - filtros `news_item_id`, `limit`, `offset`
- `GET /api/v1/verification-records/{verification_record_id}`
- `GET /api/v1/news/{news_id}/verification-records`

### Risk Reviews

- `POST /api/v1/risk-reviews`
- `GET /api/v1/risk-reviews` - filtros `news_item_id`, `entity_type`, `entity_id`, `limit`, `offset`
- `GET /api/v1/risk-reviews/{risk_review_id}`
- `GET /api/v1/news/{news_id}/risk-reviews`

### Content Pieces

- `POST /api/v1/content-pieces`
- `GET /api/v1/content-pieces` - filtros `news_item_id`, `status`, `limit`, `offset`
- `GET /api/v1/content-pieces/{content_piece_id}`
- `GET /api/v1/news/{news_id}/content-pieces`
- `PATCH /api/v1/content-pieces/{content_piece_id}/status`

### Distribution Plans

- `POST /api/v1/distribution-plans`
- `GET /api/v1/distribution-plans` - filtros `content_piece_id`, `news_item_id`, `status`, `limit`, `offset`
- `GET /api/v1/distribution-plans/{distribution_plan_id}`
- `GET /api/v1/content-pieces/{content_piece_id}/distribution-plans`
- `PATCH /api/v1/distribution-plans/{distribution_plan_id}/status`

### Publication Records

- `POST /api/v1/publication-records`
- `GET /api/v1/publication-records` - filtros `content_piece_id`, `news_item_id`, `limit`, `offset`
- `GET /api/v1/publication-records/{publication_record_id}`
- `GET /api/v1/content-pieces/{content_piece_id}/publication-records`
- `GET /api/v1/news/{news_id}/publication-records`
- `PATCH /api/v1/publication-records/{publication_record_id}/status`

### Workflows

- `POST /api/v1/workflows/news/{news_id}/start`
- `GET /api/v1/workflows` - filtros `news_item_id`, `status`, `workflow_type`, `current_step`, `limit`, `offset`
- `GET /api/v1/workflows/{workflow_run_id}`
- `GET /api/v1/news/{news_id}/workflow`
- `POST /api/v1/workflows/{workflow_run_id}/recalculate`
- `POST /api/v1/workflows/{workflow_run_id}/advance`

### Editorial Readiness

- `POST /api/v1/editorial-readiness/news/{news_id}/calculate`
- `GET /api/v1/editorial-readiness/news/{news_id}/latest`
- `GET /api/v1/editorial-readiness/news/{news_id}/explain`
- `GET /api/v1/editorial-readiness`
- `GET /api/v1/editorial-readiness/{score_id}`

### Admin Dashboard

- `GET /api/v1/admin/dashboard/overview`
- `GET /api/v1/admin/dashboard/newsroom-health`
- `GET /api/v1/admin/intake/queue`
- `GET /api/v1/admin/editorial/work-queue`
- `GET /api/v1/admin/blockers`
- `GET /api/v1/admin/readiness/board`
- `GET /api/v1/admin/tasks/board`
- `GET /api/v1/admin/publications/board`
- `GET /api/v1/admin/ownership/board`
- `GET /api/v1/admin/users/{user_id}/workload`
- `GET /api/v1/admin/gaps`
- `GET /api/v1/admin/audit/summary`
- `GET /api/v1/admin/connectors/summary`

### Operational Audit Log

- `POST /api/v1/operational-audit/events`
- `GET /api/v1/operational-audit/events` - filtros `event_type`, `action`, `permission`, `actor_id`, `actor_role`, `entity_type`, `entity_id`, `news_item_id`, `workflow_run_id`, `workflow_task_id`, `agent_output_id`, `outcome`, `decision`, `correlation_id`, `limit`, `offset`
- `GET /api/v1/operational-audit/events/{event_id}`
- `GET /api/v1/operational-audit/correlation/{correlation_id}`
- `GET /api/v1/operational-audit/actors/{actor_id}`
- `GET /api/v1/operational-audit/entity/{entity_type}/{entity_id}`

## Admin Read Models

Fase 12 agrega una API de dashboard operativo bajo `/api/v1/admin`. Estos endpoints
no duplican datos ni crean tablas nuevas: calculan vistas de lectura desde entidades
existentes como `NewsItem`, `IntakeSignal`, `WorkflowRun`, `WorkflowTask`,
`EditorialReadinessScore`, `PublicationRecord`, `OwnershipAssignment`, `AgentOutput`,
`MemoryItem` y `MetricSnapshot`.

Los endpoints admin usan el permiso `admin.dashboard.read`. `viewer` puede leer estos
dashboards porque se interpreta como rol interno read-only. Si `AUTH_ENABLED=true`, la
API key sigue siendo obligatoria y `X-Actor-Role` debe ser un rol válido.

### Overview

`GET /api/v1/admin/dashboard/overview` devuelve conteos operativos:

- noticias e intake signals.
- workflows activos y bloqueados.
- tasks pendientes, bloqueadas y completadas.
- readiness latest, ready-to-advance y bloqueado.
- publicaciones scheduled/published.
- agent outputs pendientes de revisión.
- usuarios activos y trabajo sin asignar.

```bash
curl http://127.0.0.1:8000/api/v1/admin/dashboard/overview \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin"
```

### Newsroom Health

`GET /api/v1/admin/dashboard/newsroom-health` devuelve:

- `health_status`: `healthy`, `degraded` o `critical`.
- `health_score`.
- blockers críticos, warnings y acciones recomendadas.
- conteos por estado de news, workflow, task y readiness.

### Boards

- Intake queue: señales pendientes, duplicadas o únicas, sin incluir `raw_payload`.
- Editorial work queue: noticias con brechas editoriales, tareas pendientes o readiness bajo.
- Blockers: tareas bloqueadas, risks críticos, auditorías bloqueantes y readiness bloqueado.
- Readiness board: último score por noticia, sin duplicar scores viejos.
- Task board: tareas operativas con filtros por estado, agente, assignee, prioridad y bloqueo.
- Publication board: publicaciones scheduled/published por canal y estado.
- Ownership board: usuarios, asignaciones activas y trabajo sin owner.
- User workload: asignaciones, tasks, noticias owned y revisiones por usuario.
- Operational gaps: brechas como noticias sin verificación, publicaciones sin métricas,
  agent outputs pendientes y tareas sin owner.
- Audit summary: conteos por tipo, outcome, decision y eventos recientes del
  `OperationalAuditLog`.

Ejemplos:

```bash
curl "http://127.0.0.1:8000/api/v1/admin/editorial/work-queue" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: editor"
```

```bash
curl "http://127.0.0.1:8000/api/v1/admin/blockers" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: reviewer"
```

```bash
curl "http://127.0.0.1:8000/api/v1/admin/readiness/board?score_band=blocked" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: analyst"
```

```bash
curl "http://127.0.0.1:8000/api/v1/admin/ownership/board" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin"
```

```bash
curl "http://127.0.0.1:8000/api/v1/admin/audit/summary" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin"
```

## Operational Audit Log

Fase 13 agrega `OperationalAuditLog`, una bitácora operacional persistente para
acciones críticas de XMIP. Registra actor, rol, permiso evaluado, acción, entidad,
decisión, outcome, metadata mínima y `correlation_id`.

No reemplaza `AuditCheck`: `AuditCheck` gobierna revisión editorial de contenido.
`OperationalAuditLog` solo registra trazabilidad operativa. No aprueba, no publica,
no ejecuta acciones y no debe guardar secretos, API keys ni payloads sensibles completos.

Campos principales:

- `event_type`
- `action`
- `permission`
- `actor_id`, `actor_role`, `actor_display`, `actor_source`
- `request_method`, `request_path`
- `entity_type`, `entity_id`
- referencias opcionales a `news_item_id`, `workflow_run_id`, `workflow_task_id`,
  `agent_output_id`, `ownership_id` y `user_id`
- `outcome`, `decision`, `reason`
- `before_state`, `after_state`, `metadata`
- `error_code`, `error_message`
- `correlation_id`

Tipos de evento:

```text
auth_event
rbac_event
intake_event
news_event
source_event
verification_event
risk_event
content_event
audit_event
distribution_event
publication_event
workflow_event
workflow_task_event
agent_output_event
memory_event
knowledge_event
readiness_event
user_event
ownership_event
admin_event
system_event
```

Outcomes:

```text
allowed
denied
succeeded
failed
blocked
skipped
cancelled
```

Decisiones:

```text
allow
deny
created
updated
deleted
accepted
rejected
approved
invalidated
archived
promoted
calculated
assigned
released
transferred
started
completed
failed
blocked
cancelled
retried
no_op
error
```

Acciones críticas auditadas:

- promover señal a noticia.
- calcular readiness.
- crear `AuditCheck`.
- crear `PublicationRecord`.
- cambiar estado de publicación.
- aceptar o rechazar `AgentOutput`.
- aprobar o invalidar `MemoryItem`.
- crear o actualizar `UserAccount`.
- asignar, liberar o transferir ownership.
- iniciar, completar, fallar, bloquear, cancelar o reintentar `WorkflowTask`.

Crear evento manual o de sistema:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/operational-audit/events \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin" \
  -d '{
    "event_type": "system_event",
    "action": "system.manual_note",
    "permission": "operational_audit.create",
    "actor_role": "admin",
    "entity_type": "System",
    "entity_id": "manual-1",
    "outcome": "succeeded",
    "decision": "created",
    "metadata": {"note": "Manual audit event without secrets."}
  }'
```

Consultar eventos:

```bash
curl "http://127.0.0.1:8000/api/v1/operational-audit/events?event_type=publication_event" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin"
```

Consultar por correlation:

```bash
curl http://127.0.0.1:8000/api/v1/operational-audit/correlation/CORRELATION_ID \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin"
```

Consultar por actor:

```bash
curl http://127.0.0.1:8000/api/v1/operational-audit/actors/ACTOR_ID \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin"
```

Consultar por entidad:

```bash
curl http://127.0.0.1:8000/api/v1/operational-audit/entity/NewsItem/NEWS_ITEM_ID \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin"
```

## Intake Adapters & Deduplication

Fase 10 agrega `IntakeSignal` e `IntakeAdapterRun` para recibir señales candidatas
antes de convertirlas en `NewsItem`. `IntakeSignal` no es noticia aprobada, no es
fuente verificada y no publica. Debe normalizarse y deduplicarse antes de promoción.

`IntakeAdapterRun` registra ejecuciones lógicas de adaptadores manuales o futuros.
No ejecuta RSS, scraping, redes sociales ni APIs externas en esta fase.

### Catálogos

`signal_type`:

```text
manual
adapter
agent_generated
imported
webhook
rss
social
market_event
calendar_event
system
```

`signal_status`:

```text
received
normalized
dedupe_pending
duplicate
probable_duplicate
unique
linked
promoted
rejected
archived
error
```

`dedupe_status`:

```text
not_checked
unique
exact_duplicate
probable_duplicate
related
needs_review
false_positive
```

`adapter_type`:

```text
manual
rss
social
market_data
calendar
webhook
file_import
agent_output
system
```

`adapter_run_status`:

```text
created
running
completed
completed_with_warnings
failed
cancelled
```

### Normalización

Al crear una señal, el backend:

- Aplica trim y normaliza espacios en título, resumen y contenido.
- Canonicaliza URL básica.
- Elimina parámetros de tracking `utm_source`, `utm_medium`, `utm_campaign`,
  `utm_term` y `utm_content`.
- Normaliza `asset_symbols`, `entities` y `keywords`.
- Genera `content_hash` determinístico desde contenido normalizado.
- Genera `dedupe_key` desde título, topic y fuente normalizados.

### Deduplicación

Reglas determinísticas:

- Duplicado exacto si coincide `content_hash` o `url_canonical`.
- Duplicado probable si coincide `dedupe_key` o si el título es similar con
  `difflib.SequenceMatcher` y umbral `>= 0.88`.
- Si no hay coincidencias, la señal queda `unique`.

No usa ML, embeddings ni base vectorial.

### Promoción

`POST /api/v1/intake/signals/{signal_id}/promote` crea un `NewsItem` solo si la
señal no está `duplicate`, `rejected`, `archived`, `error` ni ya promovida.

Mapeo principal:

```text
normalized_title -> NewsItem.title
normalized_summary/raw_content -> NewsItem.summary
topic -> NewsItem.category
priority -> NewsItem.priority
url_canonical/source_url -> NewsItem.source_url
source_name -> NewsItem.source_name
status = detected
```

Si hay `source_url` y `source_name`, se crea `SourceReference` si no existe una
equivalente. Si el body trae `create_workflow=true`, se crea `WorkflowRun` con el
`workflow_type` solicitado. No se crean tareas bootstrap automáticamente desde promote.

### Ejemplos

Crear señal manual:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/intake/signals \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{
    "signal_type": "manual",
    "source_name": "Example Wire",
    "source_url": "https://example.com/news/btc-etf?utm_source=x",
    "source_type": "wire",
    "raw_title": "Bitcoin ETF sees record inflows",
    "raw_summary": "Institutional inflows increased.",
    "raw_content": "Institutional inflows into spot BTC ETFs reached a new record.",
    "topic": "markets",
    "asset_symbols": ["BTC"],
    "priority": "P1",
    "confidence_level": "IC3"
  }'
```

Recalcular dedupe:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/intake/signals/SIGNAL_ID/dedupe \
  -H "X-API-Key: dev-secret"
```

Promover a `NewsItem` y crear workflow:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/intake/signals/SIGNAL_ID/promote \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{"create_workflow": true, "workflow_type": "editorial_pipeline"}'
```

Rechazar o archivar:

```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/intake/signals/SIGNAL_ID/reject \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{"reason": "Duplicate or low quality."}'
```

```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/intake/signals/SIGNAL_ID/archive \
  -H "X-API-Key: dev-secret"
```

Registrar adapter run manual:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/intake/adapter-runs \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{
    "adapter_name": "manual-intake",
    "adapter_type": "manual",
    "status": "completed",
    "input_payload": {"count": 1},
    "result_payload": {"signals_created": 1}
  }'
```

Flujo mínimo:

```text
1. POST /api/v1/intake/signals
2. GET /api/v1/intake/signals
3. POST /api/v1/intake/signals/{id}/dedupe
4. POST /api/v1/intake/signals/{id}/promote
5. GET /api/v1/news/{news_id}
6. POST /api/v1/workflows/news/{news_id}/start si no se creó automáticamente
```

## Agent Output Storage

Fase 6 agrega `AgentOutput` para guardar resultados estructurados de agentes editoriales.
Esto no ejecuta agentes reales ni llama APIs externas; solo persiste outputs auditables.

Reglas críticas:

- `AgentOutput` no es fuente factual.
- `AgentOutput` no es aprobación editorial.
- `AgentOutput` no publica.
- `AgentOutput` no reemplaza `VerificationRecord`, `RiskReview`, `AuditCheck`,
  `ContentPiece`, `DistributionPlan` ni `PublicationRecord`.

Relaciones posibles:

- `agent_execution_id`
- `news_item_id`
- `workflow_run_id`
- `workflow_step_id`
- `entity_type` + `entity_id`

Al crear un output debe existir al menos una relación operativa. Si se pasan IDs de
`NewsItem`, `WorkflowRun`, `WorkflowStep` o `AgentExecution`, el backend valida que existan.

Agentes permitidos:

```text
NewsScoutAgent
SourceValidatorAgent
RiskAgent
MarketImpactAgent
EditorialAgent
ScriptAgent
SocialClipAgent
DistributionAgent
AuditAgent
MemoryAgent
KnowledgeAgent
CalendarAgent
MetricsAgent
```

Tipos de output:

```text
news_scout_report
source_review
risk_review
market_impact_assessment
editorial_output
script_output
social_output
distribution_plan_output
audit_check_output
memory_proposal
knowledge_graph_proposal
calendar_recommendation
metrics_review
workflow_recommendation
generic_agent_output
```

Estados:

```text
created
stored
pending_review
accepted
rejected
superseded
blocked
failed
archived
```

Flags sensibles como `missing_source`, `rumor_as_fact`, `financial_advice_risk`,
`hallucinated_source` o `critical_risk` activan `human_review_required=true`.

Crear output:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/agent-outputs \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{
    "agent_name": "NewsScoutAgent",
    "agent_version": "0.1.0",
    "output_type": "news_scout_report",
    "news_item_id": "NEWS_ITEM_ID",
    "summary": "Scout report for ETF inflow signal.",
    "payload": {"signals": [{"title": "ETF inflows", "confidence": "medium"}]},
    "next_agent": "SourceValidatorAgent"
  }'
```

Aceptar, rechazar o supersede:

```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/agent-outputs/OUTPUT_ID/accept \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{"accepted_by": "operator"}'
```

```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/agent-outputs/OUTPUT_ID/reject \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{"rejected_reason": "Output changed certainty level without evidence."}'
```

```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/agent-outputs/OUTPUT_ID/supersede \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{"superseded_by_output_id": "REPLACEMENT_OUTPUT_ID"}'
```

Ejemplos mínimos por agente:

```json
{"agent_name":"NewsScoutAgent","output_type":"news_scout_report","payload":{"signals":[]}}
{"agent_name":"RiskAgent","output_type":"risk_review","payload":{"risk_level":"medium"}}
{"agent_name":"EditorialAgent","output_type":"editorial_output","payload":{"draft_title":"..."}}
{"agent_name":"AuditAgent","output_type":"audit_check_output","payload":{"ready_to_advance":false}}
{"agent_name":"MetricsAgent","output_type":"metrics_review","payload":{"observations":[]}}
```

## Editorial Core

Fase 4 agrega las entidades centrales para convertir una señal noticiosa en contenido
editorial trazable:

```text
NewsItem
-> VerificationRecord
-> RiskReview
-> ContentPiece
-> DistributionPlan
-> PublicationRecord
```

## Workflow Orchestration

Fase 5 agrega `WorkflowRun` y `WorkflowStep` para orquestar el flujo editorial sin
crear automáticamente entidades editoriales ni ejecutar integraciones externas.

Un workflow responde:

- En qué etapa está la noticia.
- Qué entidades editoriales ya existen.
- Qué requisitos faltan.
- Qué bloquea el avance.
- Qué acción y agente se recomiendan después.

Flujo orquestado:

```text
NewsItem
-> VerificationRecord
-> RiskReview
-> ContentPiece
-> AuditCheck
-> DistributionPlan
-> PublicationRecord
-> measurement
```

### Readiness

- `not_ready`: faltan verificación o riesgo.
- `partially_ready`: hay verificación/riesgo, pero falta contenido.
- `ready_for_review`: hay contenido, pero falta `AuditCheck`.
- `ready_to_advance`: hay `AuditCheck` válido y distribución/publicación pendiente.
- `blocked`: hay riesgo, auditoría, contenido, distribución o publicación bloqueante.
- `completed`: existe `PublicationRecord` publicado y no hay bloqueos críticos.

### Bloqueos

El workflow queda bloqueado si detecta:

- `VerificationRecord` `contradicted` o `rejected`.
- `VerificationRecord` `rumor`.
- `RiskReview.publication_block_recommended=true`.
- `RiskReview.decision_recommendation=block_publication` o `reject`.
- `RiskReview.risk_level=critical`.
- `ContentPiece.status=blocked` o `rejected`.
- `DistributionPlan.status=blocked` o `rejected`.
- `PublicationRecord.publication_status=retracted`.
- `AuditCheck.publication_block_recommended=true`.

### Flujo ejemplo

1. Crear `NewsItem`.
2. Crear workflow:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/workflows/news/NEWS_ITEM_ID/start \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{"workflow_type": "editorial_pipeline"}'
```

3. Recalcular workflow:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/workflows/WORKFLOW_RUN_ID/recalculate \
  -H "X-API-Key: dev-secret"
```

4. Crear `VerificationRecord`.
5. Crear `RiskReview`.
6. Crear `ContentPiece`.
7. Crear `AuditCheck`.
8. Crear `DistributionPlan`.
9. Crear `PublicationRecord`.
10. Recalcular workflow.
11. Consultar estado final:

```bash
curl http://127.0.0.1:8000/api/v1/workflows/WORKFLOW_RUN_ID
```

Para intentar avanzar:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/workflows/WORKFLOW_RUN_ID/advance \
  -H "X-API-Key: dev-secret"
```

Si faltan requisitos críticos o existe bloqueo editorial, responde HTTP 409.

Las entidades nuevas mantienen `correlation_id`, timestamps y relaciones mínimas por foreign key.

### Gates mínimos

`ContentPiece` no puede crearse si:

- `news_item_id` no existe.
- `verification_status = unverified`.
- `risk_level = critical`.

`DistributionPlan` no puede crearse si:

- `content_piece_id` no existe.
- `ContentPiece.status = blocked`.
- `ContentPiece.status = rejected`.

`PublicationRecord` no puede crearse si:

- `content_piece_id` no existe.
- `distribution_plan_id` no existe.
- `ContentPiece.status` no es `approved`.
- `DistributionPlan.status` no es `scheduled` o `ready_for_review`.
- `publication_status = published` y no hay `published_url` ni `external_id`.

### Flujo ejemplo

Crear verificación:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/verification-records \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{
    "news_item_id": "NEWS_ITEM_ID",
    "verification_status": "verified",
    "evidence_level": "E3",
    "confidence_level": "C4",
    "summary": "Confirmed against primary and secondary sources.",
    "verified_claims": ["ETF inflows increased"],
    "unverified_claims": [],
    "contradictions": [],
    "source_refs": ["https://example.com/etf-inflows"]
  }'
```

Crear revisión de riesgo:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/risk-reviews \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{
    "news_item_id": "NEWS_ITEM_ID",
    "entity_type": "news_item",
    "entity_id": "NEWS_ITEM_ID",
    "risk_level": "medium",
    "severity": "R-SEV-1",
    "decision_recommendation": "allow_with_minor_edits",
    "summary": "Market-sensitive but publishable with neutral language."
  }'
```

Crear pieza editorial:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/content-pieces \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{
    "news_item_id": "NEWS_ITEM_ID",
    "content_type": "news_article",
    "title": "Bitcoin ETF inflows hit new record",
    "summary": "A concise editorial summary.",
    "body": "Institutional inflows into spot BTC ETFs reached a new daily record.",
    "status": "approved",
    "category": "markets",
    "priority": "P1",
    "verification_status": "verified",
    "risk_level": "medium",
    "source_refs": ["https://example.com/etf-inflows"]
  }'
```

Crear plan de distribución:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/distribution-plans \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{
    "content_piece_id": "CONTENT_PIECE_ID",
    "news_item_id": "NEWS_ITEM_ID",
    "primary_channel": "Blog / Web",
    "secondary_channels": ["LinkedIn", "X / Twitter"],
    "distribution_type": "primary_publication",
    "status": "scheduled",
    "dependencies": [],
    "metric_plan": {"primary_metric": "views"},
    "risk_level": "medium",
    "publication_readiness": "ready"
  }'
```

Crear registro de publicación:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/publication-records \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{
    "content_piece_id": "CONTENT_PIECE_ID",
    "distribution_plan_id": "DISTRIBUTION_PLAN_ID",
    "news_item_id": "NEWS_ITEM_ID",
    "channel": "Blog / Web",
    "publication_status": "published",
    "published_url": "https://example.com/published/story"
  }'
```

## Máquina de estados editorial

Los estados válidos viven en `app/core/constants.py`. Las transiciones válidas viven en
`app/core/state_machine.py` y se aplican desde `app/services/news_service.py`.

Transiciones principales:

```text
detected -> registered
registered -> classified
classified -> validating
validating -> verified | partially_verified | rumor | rejected
verified -> prioritized
partially_verified -> prioritized
rumor -> monitoring
monitoring -> validating
prioritized -> drafting
drafting -> reviewing
reviewing -> approved | rejected
approved -> scheduled
scheduled -> published
published -> distributed | corrected | retracted
distributed -> measured
measured -> archived
any non-final state -> escalated
```

Estados finales:

```text
rejected
archived
corrected
retracted
escalated
```

Una transición inválida responde con HTTP 400 y formato de error consistente:

```json
{
  "success": false,
  "error": "Invalid status transition from detected to verified",
  "correlation_id": "corr_..."
}
```

## Editorial gates

Los estados críticos requieren el último `AuditCheck` válido de la noticia:

```text
approved
scheduled
published
```

Un `AuditCheck` válido debe cumplir:

```text
entity_type = news_item o NewsItem
entity_id = id de la noticia
ready_to_advance = true
publication_block_recommended = false
audit_status = passed o passed_with_warnings
decision_recommendation = allow_to_continue o allow_with_warnings
```

Si el último `AuditCheck` compatible no cumple esas condiciones, el cambio de estado
responde HTTP 409:

```json
{
  "success": false,
  "error": "NewsItem cannot transition to published without a passing AuditCheck",
  "correlation_id": "corr_..."
}
```

Flujo editorial protegido:

```text
reviewing -> approved -> scheduled -> published
```

Antes de avanzar a cada estado crítico debe existir un `AuditCheck` vigente y válido.
Ejemplo para habilitar `reviewing -> approved`:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/audit/checks \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{
    "entity_type": "news_item",
    "entity_id": "NEWS_ITEM_ID",
    "audit_status": "passed",
    "severity": "medium",
    "decision_recommendation": "allow_to_continue",
    "ready_to_advance": true,
    "publication_block_recommended": false,
    "missing_requirements": [],
    "audit_flags": []
  }'
```

## Arquitectura

```text
app/
├── api/v1/endpoints/   # Routers HTTP, sin lógica de negocio
├── core/               # Config, auth, gates, errores, middleware, state machine
├── db/                 # Engine, sesión async, init local/test
├── models/             # Entidades SQLAlchemy
├── schemas/            # Pydantic request/response
├── services/           # Lógica de negocio y persistencia
└── main.py             # App FastAPI, middleware, handlers, /health, /live, /ready
```

Reglas de separación:

- API no contiene lógica de negocio.
- Services no son modelos de base de datos.
- Schemas no son entidades persistentes.
- Migraciones no dependen de `AUTO_CREATE_TABLES`.
- Agentes no publican directamente.
- Auth vive como dependency reutilizable, no como lógica duplicada en routers.
- Gates editoriales viven en core/services, no en endpoints.

## Trazabilidad y reglas editoriales ORION

- Nada se publica sin fuente: `source_url` y `source_name` son obligatorios en news intake.
- Nada sensible se publica sin verificación: `published` solo se alcanza desde `scheduled`.
- Nada crítico se publica sin aprobación: `scheduled` solo se alcanza desde `approved`.
- Los estados `approved`, `scheduled` y `published` requieren `AuditCheck` vigente y válido.
- Nada publicado queda sin registro: entidades persistidas guardan `correlation_id`.
- La memoria no es fuente factual: no existe endpoint que convierta memoria en fuente.
- Un output de agente no es fuente: `AgentExecution` registra ejecución, no evidencia editorial.
- Un agente no publica directamente: no hay endpoint de publicación automática.

## Git operativo

Si el repositorio no está inicializado:

```bash
git status
git add .
git commit -m "chore: initialize ORION XMIP repository with backend MVP"
```

## Pendientes técnicos

- Autenticación completa para agentes y humanos.
- Login real, JWT/OAuth/SSO y sesiones de usuario.
- Endpoints de workflows, memoria editorial, métricas y calendario.
- Gates más específicos por severidad, categoría, fuente y riesgo editorial.
- Pipeline CI con tests, lint y migraciones.

## Workflow Task Queue

`WorkflowTask` es la cola interna de XMIP para trabajo editorial trazable. Guarda tareas,
asignaciones, bloqueos, intentos y referencias a `WorkflowRun`, `WorkflowStep`,
`NewsItem`, `AgentExecution` y `AgentOutput`. No ejecuta agentes, no publica y no
reemplaza las entidades canónicas del flujo editorial.

### Task types permitidos

- `news_intake`
- `source_validation`
- `market_impact_assessment`
- `risk_review`
- `editorial_draft`
- `script_generation`
- `social_variant_generation`
- `distribution_planning`
- `audit_check`
- `calendar_scheduling`
- `metrics_review`
- `memory_review`
- `knowledge_update`
- `workflow_recalculation`
- `manual_review`
- `publication_preparation`
- `generic_task`

### Task statuses permitidos

- `queued`
- `assigned`
- `running`
- `waiting_input`
- `waiting_review`
- `completed`
- `completed_with_warnings`
- `failed`
- `blocked`
- `cancelled`
- `retrying`
- `escalated`
- `archived`

### Assignees permitidos

- `NewsScoutAgent`
- `SourceValidatorAgent`
- `RiskAgent`
- `MarketImpactAgent`
- `EditorialAgent`
- `ScriptAgent`
- `SocialClipAgent`
- `DistributionAgent`
- `AuditAgent`
- `MemoryAgent`
- `KnowledgeAgent`
- `CalendarAgent`
- `MetricsAgent`
- `HumanEditor`
- `Operator`
- `System`
- `None`

### Endpoints

- `POST /api/v1/workflow-tasks`
- `GET /api/v1/workflow-tasks`
- `GET /api/v1/workflow-tasks/{task_id}`
- `GET /api/v1/workflows/{workflow_run_id}/tasks`
- `GET /api/v1/news/{news_id}/tasks`
- `POST /api/v1/workflows/{workflow_run_id}/tasks/bootstrap`
- `GET /api/v1/workflows/{workflow_run_id}/tasks/summary`
- `PATCH /api/v1/workflow-tasks/{task_id}/start`
- `PATCH /api/v1/workflow-tasks/{task_id}/complete`
- `PATCH /api/v1/workflow-tasks/{task_id}/fail`
- `PATCH /api/v1/workflow-tasks/{task_id}/block`
- `PATCH /api/v1/workflow-tasks/{task_id}/cancel`
- `PATCH /api/v1/workflow-tasks/{task_id}/retry`

### Auth

When `AUTH_ENABLED=true`, write endpoints require `X-API-Key`.

### Example

```bash
curl -X POST http://127.0.0.1:8000/api/v1/workflow-tasks \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{
    "workflow_run_id": "workflow-id",
    "news_item_id": "news-id",
    "task_type": "source_validation",
    "task_status": "queued",
    "priority": "P3",
    "assigned_agent": "SourceValidatorAgent",
    "title": "Validate sources",
    "description": "Validate sources before drafting.",
    "input_payload": {"evidence": ["wire"]}
  }'
```

```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/workflow-tasks/TASK_ID/start \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{"assigned_to":"operator"}'
```

```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/workflow-tasks/TASK_ID/complete \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{"output_ref":"agent-output-id"}'
```

## Metrics, Memory and Knowledge Core

Fase 8 agrega persistencia para métricas operativas, memoria editorial y relaciones
de conocimiento básicas. Esto no sustituye analítica externa, embeddings, grafo
especializado ni verificación humana.

### MetricSnapshot

`MetricSnapshot` guarda capturas de métricas vinculadas a `NewsItem`, `ContentPiece`,
`DistributionPlan`, `PublicationRecord`, `WorkflowRun`, `WorkflowTask`,
`AgentExecution` o `AgentOutput`.

Campos relevantes:

- `metric_category`
- `measurement_window`
- `metric_name`
- `metric_value`
- `snapshot_payload`
- `source_or_origin`
- `data_quality`
- `correlation_id`

Categorías permitidas:

```text
intake_metrics
source_metrics
verification_metrics
production_metrics
publication_metrics
distribution_metrics
audience_metrics
editorial_quality_metrics
calendar_metrics
agent_metrics
memory_metrics
incident_metrics
workflow_metrics
```

Ventanas permitidas:

```text
1h
24h
7d
30d
90d
custom
```

Calidad de dato:

```text
high
medium
low
insufficient
unknown
```

Endpoints:

- `POST /api/v1/metric-snapshots`
- `GET /api/v1/metric-snapshots`
- `GET /api/v1/metric-snapshots/{metric_snapshot_id}`
- `GET /api/v1/news/{news_id}/metric-snapshots`
- `GET /api/v1/publication-records/{publication_record_id}/metric-snapshots`
- `GET /api/v1/workflows/{workflow_run_id}/metric-snapshots`

### MemoryItem

`MemoryItem` guarda memoria editorial u operativa aprobable, rechazable,
invalidable o archivable. No es fuente factual ni verificación de noticia.

Campos relevantes:

- `memory_type`
- `memory_status`
- `title`
- `memory_statement`
- `source_or_origin`
- `confidence_level`
- `persistence_level`
- `scope`
- `risk_flags`
- `expiration_recommendation`
- `human_review_required`
- `approved_by`
- `invalidated_by`
- `correlation_id`

Tipos permitidos:

```text
source_memory
editorial_memory
verification_memory
distribution_memory
incident_memory
audience_memory
calendar_memory
agent_memory
workflow_memory
risk_memory
style_memory
market_context_memory
knowledge_memory
```

Estados permitidos:

```text
proposed
approved
rejected
needs_review
needs_source
needs_context
duplicate
expired
invalidated
archived
```

Endpoints:

- `POST /api/v1/memory-items`
- `GET /api/v1/memory-items`
- `GET /api/v1/memory-items/{memory_item_id}`
- `GET /api/v1/news/{news_id}/memory-items`
- `GET /api/v1/workflows/{workflow_run_id}/memory-items`
- `PATCH /api/v1/memory-items/{memory_item_id}/approve`
- `PATCH /api/v1/memory-items/{memory_item_id}/reject`
- `PATCH /api/v1/memory-items/{memory_item_id}/invalidate`
- `PATCH /api/v1/memory-items/{memory_item_id}/archive`

Reglas prácticas:

- `source_memory`, `risk_memory` e `incident_memory` activan revisión humana automática si no se envía.
- No se permite memoria sin `title`, `memory_statement` y `source_or_origin`.
- No se permite memoria sin relación operativa.
- No se puede aprobar memoria invalidada.
- No se puede invalidar memoria archivada.

### Knowledge Core

`KnowledgeNode` y `KnowledgeEdge` persisten un grafo relacional básico en PostgreSQL
o SQLite, sin grafo externo. `KnowledgeEdge` conecta contexto; no prueba causalidad.

`KnowledgeNode` campos relevantes:

- `node_type`
- `label`
- `external_ref`
- `entity_type`
- `entity_id`
- `description`
- `confidence_level`
- `status`
- `source_or_origin`
- `metadata`
- `correlation_id`

`KnowledgeEdge` campos relevantes:

- `source_node_id`
- `target_node_id`
- `relationship_type`
- `scope`
- `confidence_level`
- `reason`
- `status`
- `risk_flags`
- `metadata`
- `correlation_id`

Endpoints:

- `POST /api/v1/knowledge/nodes`
- `GET /api/v1/knowledge/nodes`
- `GET /api/v1/knowledge/nodes/{node_id}`
- `POST /api/v1/knowledge/edges`
- `GET /api/v1/knowledge/edges`
- `GET /api/v1/knowledge/edges/{edge_id}`
- `GET /api/v1/knowledge/nodes/{node_id}/edges`
- `GET /api/v1/knowledge/entity/{entity_type}/{entity_id}`

Relaciones y catálogos:

- `KnowledgeNode` admite tipos como `ContentPiece`, `MemoryItem`, `WorkflowRun`,
  `AgentOutput`, `AuditCheck` y otros definidos en `app/core/constants.py`.
- `KnowledgeEdge` admite relaciones como `derived_from`, `validated_by`,
  `derived_memory_from`, `recommends`, `blocks`, `updates`, `invalidates` y
  `related_to`.
- `caused_by` requiere confianza `KC3` o superior.
- `KnowledgeEdge` no puede apuntarse a sí misma.
- `KnowledgeNode` y `KnowledgeEdge` guardan `correlation_id`.

### Example flow

```text
1. Crear PublicationRecord
2. Crear MetricSnapshot
3. Crear MemoryItem derivado de la métrica
4. Aprobar MemoryItem
5. Crear KnowledgeNode para ContentPiece
6. Crear KnowledgeNode para MemoryItem
7. Crear KnowledgeEdge derived_memory_from
```

### Example curl

Crear métrica:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/metric-snapshots \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{
    "news_item_id": "NEWS_ITEM_ID",
    "metric_category": "publication_metrics",
    "measurement_window": "24h",
    "metric_name": "views",
    "metric_value": 1200,
    "snapshot_payload": {"views": 1200},
    "source_or_origin": "manual editorial capture",
    "data_quality": "high"
  }'
```

Crear memoria:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/memory-items \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{
    "memory_type": "editorial_memory",
    "title": "Second source rule",
    "memory_statement": "Critical claims need a second source.",
    "source_or_origin": "Post-publication review",
    "news_item_id": "NEWS_ITEM_ID",
    "confidence_level": "MC3",
    "persistence_level": "M2",
    "scope": "project_wide",
    "expiration_recommendation": "review_quarterly"
  }'
```

Crear nodo y edge:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/knowledge/nodes \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{
    "node_type": "MemoryItem",
    "label": "Second source rule",
    "entity_type": "memory_item",
    "entity_id": "MEMORY_ITEM_ID",
    "confidence_level": "KC3",
    "status": "approved",
    "source_or_origin": "Editorial system",
    "metadata": {"kind": "learning"}
  }'
```

```bash
curl -X POST http://127.0.0.1:8000/api/v1/knowledge/edges \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{
    "source_node_id": "SOURCE_NODE_ID",
    "target_node_id": "TARGET_NODE_ID",
    "relationship_type": "derived_memory_from",
    "scope": "memory_context",
    "confidence_level": "KC3",
    "reason": "Memory derived from the editorial artifact.",
    "status": "approved",
    "risk_flags": [],
    "metadata": {"kind": "trace"}
  }'
```

## Tests

```bash
cd backend
pytest
ruff check .
```

La suite actual valida:

- Migraciones Alembic.
- Auth mínima con API key.
- Máquina de estados y editorial gates.
- Editorial core entities.
- Workflow orchestration.
- AgentOutput storage.
- WorkflowTask queue.
- MetricSnapshot, MemoryItem, KnowledgeNode y KnowledgeEdge.
- Editorial Readiness Scoring.
- IntakeSignal, IntakeAdapterRun, normalización, deduplicación y promoción.
- UserAccount, OwnershipAssignment y RBAC mínimo por headers.
- Admin Read Models / Operational Dashboard API.
- OperationalAuditLog, endpoints de audit operacional, RBAC y acciones críticas auditadas.
- Production hardening: `/live`, `/ready`, CORS configurable, request logging,
  smoke test, Docker y documentación operativa.
- Internal Agent Runner: dry-run, ejecución local determinística, `AgentExecution`,
  `AgentOutput`, completion de `WorkflowTask` y audit operacional.
- External Connector Interfaces: `ExternalConnector`, `ExternalConnectorRun`,
  validación de contrato, dry-run local, RBAC, audit operacional y summary admin.

## Internal Agent Runner

Fase 15 agrega `/api/v1/agent-runner`, un runner interno síncrono para tomar una
`WorkflowTask`, producir un `AgentExecution`, guardar un `AgentOutput` estructurado,
completar o fallar la tarea y registrar `OperationalAuditLog`.

El runner no llama OpenAI, Anthropic, Hermes ni APIs externas. No ejecuta modelos
reales, no publica, no aprueba contenido y no crea entidades canónicas como
`VerificationRecord`, `RiskReview`, `ContentPiece` o `AuditCheck`. Sus outputs son
auxiliares y auditables; `AgentOutput` no es fuente factual.

### Agentes soportados

```text
NewsScoutAgent
SourceValidatorAgent
RiskAgent
MarketImpactAgent
EditorialAgent
ScriptAgent
SocialClipAgent
DistributionAgent
AuditAgent
MemoryAgent
KnowledgeAgent
CalendarAgent
MetricsAgent
System
```

Mapeo principal `task_type -> agent -> output_type`:

```text
news_intake -> NewsScoutAgent -> news_scout_report
source_validation -> SourceValidatorAgent -> source_review
market_impact_assessment -> MarketImpactAgent -> market_impact_assessment
risk_review -> RiskAgent -> risk_review
editorial_draft -> EditorialAgent -> editorial_output
script_generation -> ScriptAgent -> script_output
social_variant_generation -> SocialClipAgent -> social_output
distribution_planning -> DistributionAgent -> distribution_plan_output
audit_check -> AuditAgent -> audit_check_output
calendar_scheduling -> CalendarAgent -> calendar_recommendation
metrics_review -> MetricsAgent -> metrics_review
memory_review -> MemoryAgent -> memory_proposal
knowledge_update -> KnowledgeAgent -> knowledge_graph_proposal
workflow_recalculation -> System -> workflow_recommendation
generic_task -> System -> workflow_recommendation
```

`RiskAgent`, `AuditAgent`, `MemoryAgent` y `KnowledgeAgent` marcan
`human_review_required=true` por defecto.

### Endpoints

- `GET /api/v1/agent-runner/capabilities`
- `POST /api/v1/agent-runner/tasks/{task_id}/dry-run`
- `POST /api/v1/agent-runner/tasks/{task_id}/run`
- `POST /api/v1/agent-runner/workflows/{workflow_run_id}/run-next`
- `GET /api/v1/agent-runner/runs`
- `GET /api/v1/admin/agent-runner/summary`

Permisos RBAC:

```text
agent_runner.read
agent_runner.run
```

`owner`, `admin`, `editor_in_chief`, `agent_operator` y `system` pueden ejecutar.
`editor`, `analyst`, `reviewer` y `publisher` pueden leer. `viewer` no ejecuta.
Cuando `AUTH_ENABLED=false`, se mantiene compatibilidad local.

### Ejemplos curl

Capabilities:

```bash
curl http://127.0.0.1:8000/api/v1/agent-runner/capabilities \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: agent_operator"
```

Dry-run:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/agent-runner/tasks/TASK_ID/dry-run \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: agent_operator"
```

Run task:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/agent-runner/tasks/TASK_ID/run \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: agent_operator" \
  -d '{"force":false,"runner":"internal"}'
```

Run next task for a workflow:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/agent-runner/workflows/WORKFLOW_ID/run-next \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: agent_operator" \
  -d '{"force":false,"runner":"internal"}'
```

Recent runs:

```bash
curl "http://127.0.0.1:8000/api/v1/agent-runner/runs?agent_name=SourceValidatorAgent" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: agent_operator"
```

Revisar trazabilidad:

```bash
curl "http://127.0.0.1:8000/api/v1/agents/executions?agent_name=SourceValidatorAgent"
curl "http://127.0.0.1:8000/api/v1/agent-outputs?agent_name=SourceValidatorAgent"
curl "http://127.0.0.1:8000/api/v1/operational-audit/events?action=agent_runner.run_task" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin"
```

## External Connector Interfaces

Fase 16 agrega `/api/v1/connectors` para preparar integraciones futuras sin
activarlas todavía. Un `ExternalConnector` describe un contrato y configuración no
sensible; un `ExternalConnectorRun` registra un intento lógico, validación o dry-run.

Estos conectores no hacen scraping real, no llaman RSS/API/social/market data reales,
no llaman LLMs, no publican y no crean entidades canónicas automáticamente. El dry-run
solo produce `result_payload` local y auditable.

### Catálogos

`connector_type`:

```text
rss_feed
public_api
social_feed
market_data
llm_provider
publishing_channel
webhook_inbound
file_import
manual_import
system
```

`auth_type`:

```text
none
api_key_ref
bearer_token_ref
oauth_ref
basic_ref
signed_request_ref
manual
```

`capabilities`:

```text
ingest_signals
validate_sources
fetch_market_context
generate_agent_output
publish_content
schedule_content
fetch_metrics
receive_webhook
import_file
```

### Seguridad de secretos

`configuration` no puede contener claves como `api_key`, `token`, `secret`,
`password`, `authorization`, `bearer`, `private_key` ni variantes definidas en
`app/core/constants.py`. Usa `secret_ref` para apuntar a un secret manager futuro.
No se guardan secretos en claro.

### Endpoints

- `POST /api/v1/connectors`
- `GET /api/v1/connectors`
- `GET /api/v1/connectors/{connector_id}`
- `PATCH /api/v1/connectors/{connector_id}`
- `PATCH /api/v1/connectors/{connector_id}/enable`
- `PATCH /api/v1/connectors/{connector_id}/disable`
- `PATCH /api/v1/connectors/{connector_id}/archive`
- `POST /api/v1/connectors/{connector_id}/validate`
- `POST /api/v1/connectors/{connector_id}/dry-run`
- `GET /api/v1/connectors/{connector_id}/runs`
- `GET /api/v1/connectors/runs/{run_id}`
- `GET /api/v1/admin/connectors/summary`

Permisos RBAC:

```text
connector.read
connector.create
connector.update
connector.run
connector.archive
```

`owner`, `admin` y `system` tienen todos los permisos. `editor_in_chief` y
`agent_operator` pueden leer y ejecutar dry-runs. `analyst` y `reviewer` pueden leer.

### Ejemplos curl

Crear conector:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/connectors \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin" \
  -d '{
    "connector_name": "Example RSS",
    "connector_type": "rss_feed",
    "connector_status": "dry_run_only",
    "provider": "example",
    "base_url": "https://example.com/feed.xml",
    "capabilities": ["ingest_signals"],
    "auth_type": "none",
    "enabled": false,
    "dry_run_only": true
  }'
```

Validar contrato:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/connectors/CONNECTOR_ID/validate \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: agent_operator"
```

Dry-run:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/connectors/CONNECTOR_ID/dry-run \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: agent_operator" \
  -d '{"run_type":"dry_run"}'
```

Runs y summary:

```bash
curl http://127.0.0.1:8000/api/v1/connectors/CONNECTOR_ID/runs \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: agent_operator"

curl http://127.0.0.1:8000/api/v1/admin/connectors/summary \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin"
```

## Frontend/Admin Integration

Fase 17 deja el contrato backend/admin listo para que un dashboard React/Vite se
integre sin modificar todavía `frontend/`.

Documentos principales:

- `docs/FRONTEND_ADMIN_API_CONTRACT.md`
- `docs/FRONTEND_ADMIN_INTEGRATION_GUIDE.md`
- `docs/API_ERROR_CONTRACT.md`
- `docs/API_AUTH_RBAC_CONTRACT.md`

Base URL local:

```text
http://127.0.0.1:8000
```

Variables Vite sugeridas para desarrollo interno:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Sesión administrativa:

```text
cookie HttpOnly `xmip_session`
X-Correlation-ID
```

`VITE_*` siempre es browser-exposed. En producción no se usa para autoridad
privilegiada. El panel administrativo usa login real con cookie HttpOnly y
`credentials: include`.

Endpoints frontend-safe:

- `GET /api/v1/admin/frontend/config`
- `GET /api/v1/admin/frontend/route-map`

`frontend/config` expone solo datos seguros como nombre, versión, ambiente,
features habilitadas y headers requeridos. No devuelve `API_KEY`, `DATABASE_URL`
ni secretos.

Ejemplo:

```bash
curl http://127.0.0.1:8000/api/v1/admin/frontend/config \
  -H "X-API-Key: dev-secret" \
  -H "X-Actor-Role: admin"
```

Exportar OpenAPI sin levantar servidor:

```bash
cd backend
python scripts/export_openapi.py --output docs/openapi.json
```

Validar contrato admin contra un backend corriendo:

```bash
python scripts/admin_contract_smoke.py \
  --base-url http://127.0.0.1:8000 \
  --api-key dev-secret \
  --actor-role admin
```

Endpoints principales para el dashboard:

- `GET /api/v1/admin/dashboard/overview`
- `GET /api/v1/admin/dashboard/newsroom-health`
- `GET /api/v1/admin/intake/queue`
- `GET /api/v1/admin/editorial/work-queue`
- `GET /api/v1/admin/blockers`
- `GET /api/v1/admin/readiness/board`
- `GET /api/v1/admin/tasks/board`
- `GET /api/v1/admin/publications/board`
- `GET /api/v1/admin/ownership/board`
- `GET /api/v1/admin/agent-runner/summary`
- `GET /api/v1/admin/connectors/summary`
- `GET /api/v1/admin/audit/summary`

## Production Hardening / Deploy Readiness

Fase 14 deja el backend listo para conectarse con el futuro frontend/admin sin
cambiar la lógica editorial central.

### Healthchecks

- `/health`: compatibilidad básica del MVP.
- `/live`: liveness del proceso; no consulta DB.
- `/ready`: readiness operacional; ejecuta `SELECT 1` si `DB_HEALTHCHECK_ENABLED=true`.

### Logging

El backend usa logging JSON con campos como:

```text
timestamp
level
logger
message
correlation_id
request_method
request_path
status_code
duration_ms
actor_role
```

Por defecto no se registran cuerpos de request/response ni headers sensibles. `X-API-Key`,
`Authorization`, cookies y secretos quedan fuera de los logs operativos.

### Smoke test

Con el servidor corriendo:

```bash
cd backend
python scripts/smoke_test.py --base-url http://127.0.0.1:8000
```

El script valida `/health`, `/live`, `/ready` y `/openapi.json`. Opcionalmente puede
crear una señal de intake si se entrega API key:

```bash
python scripts/smoke_test.py \
  --base-url http://127.0.0.1:8000 \
  --api-key dev-secret \
  --create-intake-signal
```

### Docker

```bash
cd backend
docker compose config
docker compose build
docker compose up
```

`docker-compose.yml` define `api` y `postgres`. La API depende del healthcheck de
PostgreSQL, ejecuta `alembic upgrade head` y expone `/ready` como healthcheck.

### Operación

Documentos de despliegue y operación:

- `docs/DEPLOYMENT_CHECKLIST.md`
- `docs/OPERATIONAL_RUNBOOK.md`

Antes de producción:

```bash
alembic upgrade head
pytest
ruff check .
python scripts/smoke_test.py --base-url http://127.0.0.1:8000
```

Usa PostgreSQL en staging/prod. SQLite queda reservado para desarrollo y tests.

## Editorial Readiness Scoring

Fase 9 agrega `EditorialReadinessScore`, una evaluación determinística de readiness
editorial por noticia. El score informa operación; no aprueba publicación, no publica,
no reemplaza revisión humana y no reemplaza `AuditCheck`.

La tabla `editorial_readiness_scores` guarda:

- `news_item_id` y `workflow_run_id`.
- `score` total de 0 a 100.
- `score_band` y `readiness_status`.
- Scores parciales por fuente, verificación, riesgo, contenido, auditoría, workflow,
  tareas, outputs de agente, distribución, publicación, métricas, memoria y conocimiento.
- `blocking_reasons`, `missing_requirements`, `warnings` y `score_payload`.
- `recommended_next_action`, `next_agent`, `human_review_required` y
  `publication_block_recommended`.

### Fórmula

Pesos por componente:

| Componente | Peso |
| --- | ---: |
| `source_score` | 10 |
| `verification_score` | 20 |
| `risk_score` | 15 |
| `editorial_score` | 10 |
| `audit_score` | 15 |
| `workflow_score` | 5 |
| `task_score` | 5 |
| `agent_output_score` | 5 |
| `distribution_score` | 5 |
| `publication_score` | 5 |
| `metrics_score` | 2 |
| `memory_score` | 2 |
| `knowledge_score` | 1 |

Bandas:

```text
0-19    very_low
20-39   low
40-69   medium
70-89   high
90-100  ready
blocked si existe bloqueo crítico
```

Estados:

```text
not_ready
partially_ready
ready_for_review
ready_to_advance
blocked
published
archived
```

### Bloqueos críticos

El score queda `blocked` si detecta:

- `VerificationRecord` `contradicted` o `rejected`.
- `RiskReview` `critical`, `publication_block_recommended=true`,
  `block_publication` o `reject`.
- `AuditCheck` bloqueante, `failed` o `blocked`.
- `ContentPiece` `blocked` o `rejected`.
- `DistributionPlan` `blocked` o `rejected`.
- `PublicationRecord` `retracted` o `failed`.
- `WorkflowRun` bloqueado con razones críticas.
- `WorkflowTask` bloqueante en `blocked` o `failed`.
- `AgentOutput` con flags críticos pendientes de revisión.
- `NewsItem` `rejected` o `retracted`.

`AgentOutput`, `MemoryItem` y `KnowledgeEdge` son señales auxiliares. No se usan como
fuente factual, aprobación editorial ni prueba causal automática.

### Ejemplos

Calcular y guardar score:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/editorial-readiness/news/NEWS_ITEM_ID/calculate \
  -H "X-API-Key: dev-secret"
```

Consultar último score:

```bash
curl http://127.0.0.1:8000/api/v1/editorial-readiness/news/NEWS_ITEM_ID/latest
```

Explicar readiness sin guardar un nuevo registro:

```bash
curl http://127.0.0.1:8000/api/v1/editorial-readiness/news/NEWS_ITEM_ID/explain
```

Listar scores filtrados:

```bash
curl "http://127.0.0.1:8000/api/v1/editorial-readiness?score_band=blocked&limit=20"
```

Flujo recomendado:

```text
1. Crear NewsItem.
2. Crear VerificationRecord.
3. Crear RiskReview.
4. Crear ContentPiece.
5. Crear AuditCheck.
6. Crear DistributionPlan.
7. Crear PublicationRecord.
8. Crear MetricSnapshot.
9. Crear MemoryItem.
10. Crear KnowledgeNode/KnowledgeEdge.
11. POST /api/v1/editorial-readiness/news/{news_id}/calculate.
12. GET /api/v1/editorial-readiness/news/{news_id}/latest.
```
