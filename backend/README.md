# XMIP Backend

Backend API de la plataforma multiagente **XMIP** (newsroom de **XCripto**, bajo gobierno **ORION**).

Estado actual: MVP backend funcional con FastAPI, SQLAlchemy async, trazabilidad por
`X-Correlation-ID`, migración Alembic inicial y máquina de estados editorial para `NewsItem`.

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

| Variable | Default | Descripción |
| --- | --- | --- |
| `DATABASE_URL` | `sqlite+aiosqlite:///./xmip.db` | URL async de SQLAlchemy. Para PostgreSQL: `postgresql+asyncpg://user:pass@host:5432/xmip` |
| `AUTO_CREATE_TABLES` | `true` | Crea tablas al arrancar solo en local/dev/test cuando no se usan migraciones |
| `ENVIRONMENT` | `local` | `local` / `dev` / `staging` / `prod` / `test` |
| `CORS_ORIGINS` | `["http://localhost:5173"]` | Orígenes permitidos |
| `LOG_LEVEL` | `INFO` | Nivel de logging |

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

## Arquitectura

```text
app/
├── api/v1/endpoints/   # Routers HTTP, sin lógica de negocio
├── core/               # Config, constantes, errores, middleware, state machine
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

## Trazabilidad y reglas editoriales ORION

- Nada se publica sin fuente: `source_url` y `source_name` son obligatorios en news intake.
- Nada sensible se publica sin verificación: `published` solo se alcanza desde `scheduled`.
- Nada crítico se publica sin aprobación: `scheduled` solo se alcanza desde `approved`.
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

- Autenticación/autorización para agentes y humanos.
- Roles y permisos editoriales (`ADMIN`, `EDITOR`, `VIEWER`, etc.).
- Endpoints de workflows, memoria editorial, métricas y calendario.
- Auditorías que bloqueen transiciones críticas con evidencia insuficiente.
- Pipeline CI con tests, lint y migraciones.
