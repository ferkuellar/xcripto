# XMIP Backend

Backend API de la plataforma multiagente **XMIP** (newsroom de **XCripto**, bajo gobierno **ORION**).

## Stack

- FastAPI + Pydantic v2
- SQLAlchemy 2 async (SQLite local por defecto, PostgreSQL vía `DATABASE_URL`)
- pytest + httpx para tests
- Docker / Docker Compose (API + PostgreSQL)

## Ejecutar en local

### Windows (PowerShell)

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

La API queda en `http://127.0.0.1:8000` (docs interactivas en `/docs`).

## Tests

```bash
cd backend
pytest
```

Los tests usan SQLite en memoria; no requieren base de datos externa.

## Configuración

Copia `.env.example` a `.env`. Variables principales:

| Variable | Default | Descripción |
| --- | --- | --- |
| `DATABASE_URL` | `sqlite+aiosqlite:///./xmip.db` | URL async de SQLAlchemy. Para PostgreSQL: `postgresql+asyncpg://user:pass@host:5432/xmip` |
| `AUTO_CREATE_TABLES` | `true` | Crea tablas al arrancar (modo local; desactivar cuando existan migraciones Alembic) |
| `ENVIRONMENT` | `local` | `local` / `dev` / `staging` / `prod` / `test` |
| `CORS_ORIGINS` | `["http://localhost:5173"]` | Orígenes permitidos |

## Docker

```bash
cd backend
docker compose up --build
```

Levanta PostgreSQL 16 y la API en `http://localhost:8000`.

## Endpoints

### Health

- `GET /health` → `{"status": "ok", "service": "xmip-backend", "version": "0.1.0"}`

### News Intake (`/api/v1/news`)

- `POST /api/v1/news/intake` — registra una noticia candidata (status inicial `detected`)
- `GET /api/v1/news` — lista (filtros: `status`, `limit`, `offset`)
- `GET /api/v1/news/{news_id}`
- `PATCH /api/v1/news/{news_id}/status` — transición de estado editorial

### Source References (`/api/v1/sources`)

- `POST /api/v1/sources`
- `GET /api/v1/sources` (filtros: `source_status`, `limit`, `offset`)
- `GET /api/v1/sources/{source_id}`

### Agent Executions (`/api/v1/agents/executions`)

- `POST /api/v1/agents/executions`
- `GET /api/v1/agents/executions` (filtros: `agent_name`, `status`, `limit`, `offset`)
- `GET /api/v1/agents/executions/{execution_id}`

### Audit Checks (`/api/v1/audit/checks`)

- `POST /api/v1/audit/checks`
- `GET /api/v1/audit/checks` (filtros: `entity_type`, `entity_id`, `limit`, `offset`)
- `GET /api/v1/audit/checks/{audit_check_id}`

## Arquitectura

```text
app/
├── api/v1/endpoints/   # Routers HTTP (sin lógica de negocio)
├── core/               # Config, constantes de dominio, errores, middleware
├── db/                 # Engine, sesión async, init de tablas
├── models/             # Entidades SQLAlchemy
├── schemas/            # Pydantic (request/response, validación de estados)
├── services/           # Lógica de negocio y persistencia
└── main.py             # App FastAPI, middleware, handlers, /health
```

Reglas: los endpoints solo orquestan; los estados permitidos viven en `app/core/constants.py`
(estados editoriales de ORION, estados de ejecución de agentes, niveles de confianza de fuentes).
Cada request recibe/propaga `X-Correlation-ID` (middleware) y las entidades lo persisten para
trazabilidad de auditoría.

## Trazabilidad y reglas editoriales

El backend da soporte a las reglas de ORION:

- Toda noticia registra `source_url` / `source_name` obligatorios (nada sin fuente).
- Los `audit_checks` registran bloqueos de publicación (`publication_block_recommended`) y
  requisitos faltantes antes de avanzar de estado.
- Las ejecuciones de agentes quedan registradas con estado, tiempos y `correlation_id`.
- Ningún endpoint publica contenido; solo gestiona estados del pipeline editorial.

## Pendientes

- Migraciones Alembic (hoy se usa `create_all` en local; al pasar a PostgreSQL estable,
  generar migración inicial y poner `AUTO_CREATE_TABLES=false`).
- Máquina de estados con transiciones válidas (hoy se valida pertenencia al catálogo,
  no la transición concreta).
- Autenticación/autorización de agentes y humanos.
- Endpoints de workflows, telemetría y memoria editorial.
