# Local Docker PostgreSQL E2E Report

## 1. Fecha
2026-07-04

## 2. Rama
`qa/docker-postgres-e2e` (desde `main` @ `f968d04`).

## 3. Puertos usados
| Servicio | Host | Contenedor | Motivo |
| --- | --- | --- | --- |
| api | **8010** | 8000 | `:8000` ocupado por el `uvicorn` dev del usuario (PID vivo, no se tocó) |
| postgres | **55432** | 5432 | evitar choque con cualquier PostgreSQL local |

Configurables vía `API_PORT` / `POSTGRES_PORT` (nuevo, ver §4). Defaults siguen en 8000/5432.

## 4. Compose config/build
`docker-compose.yml` ya traía `postgres:16-alpine` (healthcheck + volumen `xmip_pgdata`) y
`api` (build local, `alembic upgrade head` en el arranque, `depends_on: postgres healthy`,
healthcheck a `/ready`). **Fix mínimo aplicado:** los puertos estaban hardcodeados
(`5432:5432`, `8000:8000`); se parametrizaron a `${POSTGRES_PORT:-5432}` / `${API_PORT:-8000}`
para poder correr en puertos libres sin editar el compose.

- `docker compose config` → válido, puertos resueltos a `8010→8000` y `55432→5432`.
- `docker compose build` → imagen `backend-api` construida (python:3.12-slim, `pip install .`).
- Variables production-like inyectadas vía `backend/.env` **local y gitignored** (`AUTH_ENABLED=true`,
  `API_KEY=dev-secret`, `AUTO_CREATE_TABLES=false`, `DATABASE_URL=postgresql+asyncpg://xmip:xmip@postgres:5432/xmip`).
  `dev-secret` es solo local; ningún secreto real se commitea.

## 5. PostgreSQL health
`backend-postgres-1` → `Up (healthy)` (`pg_isready`). Volumen `backend_xmip_pgdata` creado.
Base **PostgreSQL 16**, no SQLite.

## 6. Alembic contra PostgreSQL
El contenedor `api` corrió la cadena completa en el arranque:
`... -> 20260702_0001 (initial schema) -> ... -> 20260702_0011 (external connector interfaces)`.
`docker compose exec api alembic current` → **`20260702_0011 (head)`**. Migraciones reales
contra Postgres (transactional DDL), sin SQLite.

## 7. Health/live/ready
```
/health       → {"status":"ok",...}
/live         → {"status":"alive",...}
/ready        → {"status":"ready","checks":{"configuration":"ok","database":"ok"}}
/openapi.json → XMIP Backend 0.1.0
```
`database: ok` confirma conectividad real api → Postgres.

## 8. Smoke tests
- `smoke_test.py --base-url http://127.0.0.1:8010 --api-key dev-secret` → **Smoke test passed.**
- `admin_contract_smoke.py --base-url ... --api-key dev-secret --actor-role admin` → **passed**
  (11 endpoints admin en 200: intake/queue, work-queue, blockers, readiness/board, tasks/board,
  publications/board, ownership/board, gaps, agent-runner/summary, connectors/summary, audit/summary).

## 9. local_newsroom_qa
`local_newsroom_qa.py --base-url http://127.0.0.1:8010 --api-key dev-secret --actor-role admin`
→ **RESULTADO: PASS — flujo editorial local completo.** Flujo: health → IntakeSignal manual
(`dedupe=unique`) → recálculo dedupe → promote a NewsItem (`5ed261d2-…`) → ficha `/news/{id}` →
superficies admin (overview/work-queue/readiness/audit). Todo contra Postgres.

## 10. Persistencia tras restart API
`docker compose restart api` (solo API, Postgres intacto). Tras el reinicio (ready en ~1s):
- `GET /api/v1/news/5ed261d2-…` → mismo NewsItem `[QA] Exchange announces reserve transpar…`.
- `X-Total-Count` de `/api/v1/news` → `1` (igual que antes del restart).
- `admin_contract_smoke` → passed.

Los datos viven en el volumen Postgres, no en el contenedor api. **Persistencia confirmada.**

## 11. Frontend apuntando a Compose
`frontend/.env.local` (gitignored) → `VITE_API_BASE_URL=http://127.0.0.1:8010` + `dev-secret` +
actor admin. Contrato de conectividad verificado por HTTP (sin sesión de navegador):
- Preflight `OPTIONS` desde `Origin: http://localhost:5173` → 200 con
  `access-control-allow-origin: http://localhost:5173` y `allow-headers` incluyendo
  `X-API-Key, X-Actor-Id, X-Actor-Role, X-Correlation-ID`.
- `GET /api/v1/admin/dashboard/overview` con los headers reales del frontend → 200 (19 claves).

Para validación visual: `cd frontend && npm run dev` → `http://localhost:5173/#/admin`
(el backend Compose debe estar arriba en :8010).

## 12. Bugs encontrados
Ninguno funcional/editorial. Único hallazgo de infra: puertos del compose hardcodeados
(impedían correr junto a un `:8000`/`:5432` ya ocupado).

## 13. Bugs corregidos
`docker-compose.yml`: puertos parametrizados (`API_PORT` / `POSTGRES_PORT`), sin cambio de
comportamiento por defecto.

## 14. Riesgos restantes
- `backend/.env` local (gitignored) es necesario para la corrida production-like; el default del
  compose deja `AUTH_ENABLED=false` (dev). Documentado.
- Fallback dev con SQLite sigue soportado (`.env.example`), pero P4 valida **solo Postgres**.
- El `uvicorn` dev del usuario en `:8000` sigue vivo y sirve una base SQLite distinta; no
  interfiere con el stack Compose (:8010 / :55432).

## 15. GO / NO-GO
**GO.** XMIP corre en un entorno local tipo producción con Docker Compose + PostgreSQL 16:
migraciones Alembic reales, health/ready verdes, smoke + admin contract + newsroom QA en verde,
persistencia confirmada y frontend con conectividad/CORS validada contra el stack Compose.
