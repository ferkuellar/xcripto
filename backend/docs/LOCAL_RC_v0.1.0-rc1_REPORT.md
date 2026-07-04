# XMIP Local Release Candidate Report — v0.1.0-rc1

## 1. Fecha
2026-07-04

## 2. Commit base
`257cd72` (main) — incluye P1–P4: source quality enforcement (#2), workspace hygiene (#3),
frontend regression tests (#4), docker postgres e2e (#5). Rama de release por encima.

## 3. Rama
`release/v0.1.0-rc1` (desde `main`).

## 4. Backend validation
- `ruff check app tests scripts` → **All checks passed!**
- `pytest -q` → **522 passed** (con entorno limpio, sin `.env` de auth local).
- `python -c "from app.main import app"` → **XMIP Backend**.
- Alembic `upgrade head → downgrade -1 → upgrade head` → **`20260702_0011 (head)`** (DB temporal).
- `scripts/export_openapi.py` → `docs/openapi.json` **sin cambios** (ya al día).

## 5. Frontend validation
- `npm run test` → **19 passed** (3 archivos: API client, audit badges/KPI, empty/error states).
- `npm run build` → **OK** (~3.5s).
- `npm run lint` → **exit 0** (solo warnings preexistentes de fast-refresh).

## 6. Docker/PostgreSQL validation
- `docker compose config` válido; puertos host `8010→8000` / `55432→5432`.
- `docker compose build` OK; **PostgreSQL 16** `Up (healthy)`, api `Up (healthy)`.
- `alembic current` en contenedor → **`20260702_0011 (head)`** contra Postgres.
- `/health`, `/live`, `/ready` (`database: ok`) verdes.

## 7. Smoke tests
`smoke_test.py --base-url http://127.0.0.1:8010 --api-key dev-secret` → **Smoke test passed.**

## 8. Admin contract smoke
`admin_contract_smoke.py ... --actor-role admin` → **passed** (11 endpoints admin en 200).

## 9. Newsroom QA
`local_newsroom_qa.py ...` → **PASS — flujo editorial local completo** (intake → dedupe
`unique` → promote → NewsItem `82e1dbea…` → superficies admin), contra Postgres.

## 10. Source quality enforcement
Activo (P3): gate de publicación S1–S5 fail-closed + calidad de fuente en readiness +
detección de conflicto entre fuentes. Cubierto por `tests/test_source_quality.py` (parte de
las 522). Limitación: solo gradúa con `SourceReference` registrada.

## 11. Operational audit
`OperationalAuditLog` presente y ejercido por los flujos admin/editoriales (endpoints admin
en 200; audit summary disponible). `OPERATIONAL_AUDIT_ENABLED=true` por defecto.

## 12. Known issues
- **`backend/.env` con `AUTH_ENABLED=true` rompe el pytest local**: pydantic lee `env_file=".env"`
  y los tests que escriben sin API key reciben 401 (429 fallos observados). Mitigación: correr
  tests sin ese `.env` (renombrado a `.env.p4bak` en esta corrida) o con `AUTH_ENABLED=false`.
  CI no se ve afectada (el `.env` es gitignored). *Follow-up sugerido:* aislar el `.env` en la
  config de test (conftest) — no aplicado en el RC para no tocar backend sin bug de producto.
- Puerto `:8000` ocupado por el `uvicorn` dev del usuario → el stack Compose usa `:8010`.

## 13. Risks
- `frontend/.env.local` apuntando a `:8010` (Compose); revertir a `:8000` si se usa el uvicorn dev.
- Stack Compose puede quedar arriba tras la validación; teardown: `docker compose down -v`.
- Sin auth de usuarios ni cloud (por diseño en este RC).

## 14. GO / NO-GO
**GO** para congelar `v0.1.0-rc1` como release candidate **local**. Toda la validación
(backend, frontend, Docker/PostgreSQL, smoke/admin/newsroom, persistencia) está verde.

## 15. Next steps
Autenticación de usuarios (JWT/OAuth), staging/cloud, conectores externos reales e
integración LLM. Aislar `.env` de los tests locales. Endurecer source quality para fuentes
denormalizadas si el producto lo requiere.
