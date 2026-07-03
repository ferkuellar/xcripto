# XMIP Backend

Backend API de la plataforma multiagente **XMIP** (newsroom de **XCripto**, bajo gobierno **ORION**).

Estado actual: MVP backend funcional con FastAPI, SQLAlchemy async, trazabilidad por
`X-Correlation-ID`, migración Alembic inicial, máquina de estados editorial para
`NewsItem`, autorización mínima por API key, editorial gates basados en `AuditCheck`
y almacenamiento auditable de `AgentOutput`.

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
incluye un fallback local SQLite, pero en entornos reales debe usarse `.env`.

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

Copia `.env.example` a `.env`. Variables principales:

| Variable               | Default                           | Descripción                                                                               |
| ---------------------- | --------------------------------- | ------------------------------------------------------------------------------------------ |
| `DATABASE_URL`       | `sqlite+aiosqlite:///./xmip.db` | URL async de SQLAlchemy. Para PostgreSQL:`postgresql+asyncpg://user:pass@host:5432/xmip` |
| `AUTO_CREATE_TABLES` | `true`                          | Crea tablas al arrancar solo en local/dev/test cuando no se usan migraciones               |
| `ENVIRONMENT`        | `local`                         | `local` / `dev` / `staging` / `prod` / `test`                                    |
| `CORS_ORIGINS`       | `["http://localhost:5173"]`     | Orígenes permitidos                                                                       |
| `LOG_LEVEL`          | `INFO`                          | Nivel de logging                                                                           |
| `AUTH_ENABLED`       | `false`                         | Activa API key auth para endpoints de escritura                                            |
| `API_KEY`            | `null`                          | Secreto esperado cuando `AUTH_ENABLED=true`                                                |
| `API_KEY_HEADER_NAME` | `X-API-Key`                    | Header usado para enviar la API key                                                        |

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

## Endpoints actuales

### Health

- `GET /health`

### News Intake (`/api/v1/news`)

- `POST /api/v1/news/intake` - registra una noticia candidata
- `GET /api/v1/news` - lista noticias, con filtros `status`, `limit`, `offset`
- `GET /api/v1/news/{news_id}`
- `PATCH /api/v1/news/{news_id}/status` - cambia estado con máquina de estados

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
└── main.py             # App FastAPI, middleware, handlers, /health
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
- Roles y permisos editoriales (`ADMIN`, `EDITOR`, `VIEWER`, etc.).
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
