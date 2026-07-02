# XMIP Backend

Backend API de la plataforma multiagente **XMIP** (newsroom de **XCripto**, bajo gobierno **ORION**).

Estado actual: MVP backend funcional con FastAPI, SQLAlchemy async, trazabilidad por
`X-Correlation-ID`, migración Alembic inicial, máquina de estados editorial para
`NewsItem`, autorización mínima por API key y editorial gates basados en `AuditCheck`.

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
