# XMIP v0.1.0-rc1 Release Notes

**XCripto Media Intelligence Platform — Local Release Candidate 1**
Fecha: 2026-07-04 · Commit base: `257cd72` (main)

## Scope

Primer *release candidate* **local** de XMIP: backend editorial multiagente + admin
frontend + stack Docker/PostgreSQL, validado end-to-end en un entorno local tipo
producción. No incluye despliegue cloud, autenticación de usuarios ni integraciones
externas reales (ver *Known Limitations*).

## Major Capabilities

- **Pipeline editorial**: intake de señales → deduplicación → promoción a NewsItem →
  workflow orquestado → agent runner interno → entidades canónicas (verificación,
  riesgo, contenido, auditoría, distribución, publicación) → readiness editorial.
- **Máquina de estados editorial** con transiciones válidas y gates fail-closed.
- **Admin API + dashboard** (overview, work-queue, blockers, readiness board, tasks,
  publications, ownership, gaps, agent-runner, connectors, audit summary).
- **RBAC** por `X-API-Key` / `X-Actor-Role` / `X-Actor-Id` (401 sin key, 403 rol/permiso).
- **Operational audit log** para trazabilidad.

## Editorial Safety

- **Source Quality Enforcement (S1–S5)**: gate de publicación que bloquea
  `approved/scheduled/published` cuando la fuente registrada es blocked/restricted, S5
  (rumor/opaca) o S3/S4 sin verificación independiente fuerte; calidad de fuente visible
  en el readiness. Fail-closed.
- **Audit gate**: sin `AuditCheck` aprobatorio no se avanza a estados protegidos.
- **Risk gate**: riesgo crítico o bloqueo recomendado detiene la publicación.
- **Conflicto entre fuentes**: contradicciones en la verificación fuerzan revisión humana.
- Rumor-como-hecho y predicción de precios señalados vía `risk_flags` sensibles en
  AgentOutput.

## Backend

- FastAPI + SQLAlchemy async + Pydantic v2 + Alembic. Python 3.12.
- Migraciones Alembic hasta `20260702_0011`. Health surface `/health`, `/live`, `/ready`.
- 522 pruebas (pytest) verdes; ruff limpio.

## Frontend Admin

- React 19 + TypeScript + Vite + Tailwind (HashRouter). Code-splitting.
- Cliente API endurecido: headers desde env, sin API key hardcodeada, manejo de
  401/403/offline, correlation id.
- **Regression tests (Vitest + Testing Library)**: 19 pruebas (API client, badges
  canónicos de audit, KPI de bloqueos, empty/error states).

## Docker/PostgreSQL

- `docker compose` con **PostgreSQL 16** + api (build local, `alembic upgrade head` al
  arrancar, healthcheck `/ready`). Puertos de host configurables (`API_PORT`,
  `POSTGRES_PORT`). Volumen persistente `xmip_pgdata`.
- Validado E2E: migraciones contra Postgres, smoke/admin/newsroom QA, persistencia tras
  reinicio del contenedor api, conectividad CORS del frontend.

## Testing

| Suite | Resultado |
| --- | --- |
| Backend pytest | 522 passed |
| Backend ruff | clean |
| Alembic upgrade/downgrade/upgrade | head `20260702_0011` |
| Frontend Vitest | 19 passed |
| Frontend build / lint | OK / 0 errores |
| Docker smoke_test | PASS |
| Docker admin_contract_smoke | PASS (11 endpoints) |
| Docker local_newsroom_qa | PASS |
| Persistencia tras restart api | confirmada |

## Known Limitations

- Sin login / JWT / OAuth. La `API_KEY` es un secreto local/admin interno (`dev-secret`).
- Sin conectores externos reales, sin LLM real, sin scraping, sin publicación automática.
- Sin staging/cloud.
- **Source quality enforcement** solo gradúa calidad cuando existe una `SourceReference`
  registrada; noticias con fuente solo denormalizada quedan gobernadas por el gate de
  `AuditCheck`.
- Un `backend/.env` local con `AUTH_ENABLED=true` rompe el pytest local (pydantic lo lee
  vía `env_file`); ejecutar tests sin ese `.env` o con `AUTH_ENABLED=false`.
- El frontend admin es funcional, no diseño premium final.

## Not Included

Despliegue cloud, colas (Redis/Celery), auth de usuarios real, publicación/trading real,
integraciones LLM/exchange/regulador en vivo.

## Upgrade/Run Instructions

**Backend local (SQLite, rápido):**
```bash
cd backend && pip install -e ".[dev]" && uvicorn app.main:app --reload
```

**Docker + PostgreSQL (production-like):**
```bash
cd backend
API_PORT=8010 POSTGRES_PORT=55432 docker compose up --build
# auth production-like: copiar .env.local.production.example a .env (gitignored),
# AUTH_ENABLED=true, API_KEY=dev-secret, DATABASE_URL=postgresql+asyncpg://xmip:xmip@postgres:5432/xmip
```

**Frontend:**
```bash
cd frontend && npm install && npm run dev   # VITE_API_BASE_URL en .env.local
```

Ver `docs/LOCAL_DOCKER_POSTGRES_E2E_REPORT.md` y `docs/LOCAL_RC_v0.1.0-rc1_REPORT.md`.
