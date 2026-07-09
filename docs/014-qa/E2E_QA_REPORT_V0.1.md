# E2E QA Report — XMIP MVP v0.1

> Validación de punta a punta (backend + frontend + PostgreSQL + Docker + Auth/CORS)
> para decidir GO / NO-GO del release candidate `v0.1.0-rc1`.
> No se agregaron features, no se rediseñó el frontend, no se cambiaron contratos API.

---

## 1. Fecha

2026-07-09 (ejecutado 2026-07-08/09, TZ local).

## 2. Rama

`test/e2e-qa-v0.1`

## 3. Commit / base

- Base (main): `6136498348dd81c3a7bceb369feddef989d42c11`
  (`Merge pull request #15 — Fase 17 Frontend Production Integration`)
- Gate Fase 0 verificado en `main`:
  - `06c16d2` feat(frontend): align production integration with API contract freeze v0.1 — **Fase 17** ✅
  - `2b092f6` docs(api): freeze MVP API contract for v0.1 — **Fase 16** ✅
  - `bae83ff` feat(hardening): enforce production-ready backend configuration — **Fase 14** ✅
  - `14b6e27` feat(connectors): add hardened RSS connector rollout — **Fase 15 / connectors** ✅

## 4. Stack usado

Se documenta el método exacto (el plan lo permite cuando no se usa el compose VPS íntegro).

- **Backend + PostgreSQL:** `backend/docker-compose.yml` (stack tipo prod: `postgres:16-alpine` + API con
  `alembic upgrade head`, `AUTO_CREATE_TABLES=false`, healthcheck sobre `/ready`).
  - `postgres` → `localhost:5432` (healthy)
  - `api` → `localhost:8000` (healthy)
  - Levantado con: `docker compose -f backend/docker-compose.yml --env-file <qa.env> -p xmip-qa up -d --build`
  - DB de QA **limpia** (volumen nuevo `xmip-qa_xmip_pgdata`); datos generados vía el flujo real de intake.
- **Frontend:** Vite dev server en `localhost:5173`, `--mode qa` (env de mayor precedencia
  `frontend/.env.qa.local`, para no tocar el `.env.local` del usuario). Apunta a `http://localhost:8000`.
- **Docker:** Docker Desktop 29.6.1 / Compose v5.3.0. Plataforma Windows 11.

> **Por qué no `docker-compose.vps.yml`:** ese compose está diseñado para VPS real con TLS —
> sólo expone Caddy en 80/443, construye el frontend con `https://${API_DOMAIN}` y fija CORS a
> `https://${APP_DOMAIN}`; requiere dominios + certs ACME. Es incompatible con el plan de QA local
> basado en `http://localhost:8000` / `http://localhost:5173`. Se revisó su estructura (misma imagen
> `api`, migraciones alembic, wiring de CORS con `X-API-Key/X-Actor-*/X-Correlation-ID`) y es coherente.
> Ver **Riesgos residuales**.

## 5. Config backend usada (sin secretos)

```env
ENVIRONMENT=staging
DEBUG=false
AUTH_ENABLED=true
API_KEY=<local-staging-smoke-key · redactada>
API_KEY_HEADER_NAME=X-API-Key
AUTO_CREATE_TABLES=false
DATABASE_URL=postgresql+asyncpg://xmip:***@postgres:5432/xmip
CORS_ALLOWED_ORIGINS=http://localhost:5173
CORS_ALLOW_CREDENTIALS=false
OPERATIONAL_AUDIT_ENABLED=true
DB_HEALTHCHECK_ENABLED=true
CONNECTORS_ENABLED=false
RSS_CONNECTOR_ENABLED=false
CONNECTOR_AUTO_PROMOTE=false
CONNECTOR_RUN_MODE=manual
APP_VERSION=0.1.0-rc1
```

Config runtime confirmada dentro del container `xmip-qa-api-1`.

## 6. Config frontend usada (sin secretos)

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_API_KEY=<local-staging-smoke-key · redactada>
VITE_ACTOR_ROLE=system
VITE_ACTOR_ID=qa-e2e
```

> `system` cubre todos los permisos requeridos (writes + `operational_audit.read` + `admin.dashboard.read`).
> `frontend/.env.qa.local` está gitignored; el `.env.local` del usuario (`:8010`) **no se tocó**.

## 7. Backend smoke — PASS ✅

| Endpoint | Resultado |
|---|---|
| `GET /health` | 200 · `x-correlation-id` presente |
| `GET /live` | 200 |
| `GET /ready` | 200 · `checks.configuration=ok` · `checks.database=ok` |
| `GET /openapi.json` | 200 (233 KB) · `x-correlation-id` |

Sin stack traces. `X-Correlation-ID` en todas las respuestas.

**API smoke:**

| Caso | Resultado |
|---|---|
| `GET /api/v1/news` (key+role) | 200 · `X-Total-Count` · `X-Correlation-ID` |
| `GET /api/v1/operational-audit/events` (con key) | 200 |
| `GET /api/v1/operational-audit/events` (**sin key**) | **401** · `{"success":false,"error":"Missing API key","correlation_id":...}` |
| `GET /api/v1/operational-audit/events` (**role inválido**) | **403** · `{"success":false,"error":"Invalid actor role",...}` |

Errores normalizados (envelope `success/error/correlation_id`).

## 8. Frontend build / lint / test — PASS ✅

| Comando | Resultado |
|---|---|
| `npm install` | up to date |
| `npm run build` (`tsc -b && vite build`) | **OK** |
| `npm run lint` (oxlint) | **OK** (sólo warnings preexistentes `only-export-components`) |
| `npm test` (vitest run) | **19 passed** (3 files) |

## 9. Rutas probadas (navegador, dev server real → backend real)

`/` (Command Center), `#/news`, `#/news?q=Ethereum`, `#/news/:id`, `#/intake`, `#/sources`,
`#/agents`, `#/audit` (Audit Checks + Operational Audit), `#/admin` (read models).

- **0 pantallas blancas**, **0 errores de consola** (sesión completa con backend online).
- Health badge visible ("XMIP online · 0.1.0-rc1"). Auth/API key operando.
- Correlation ID visible en errores técnicos.
- Los read models admin (`/api/v1/admin/*`) respondieron 200.

## 10. E2E News Feed — PASS ✅

- Listado backend real (2 items sembrados vía intake).
- Búsqueda backend-side y **URL-shareable**: `#/news?q=Ethereum` → `GET /api/v1/news?q=Ethereum&limit=50&offset=0`
  → sólo el item Ethereum (oculta SEC).
- Filtros verificados a nivel API: `status=detected`→2, `priority=P1`→1, `priority=P4`→0.
- Paginación real (`limit`/`offset`). Sin mocks ocultos en los datos del feed.

## 11. E2E News Detail — PASS ✅

`#/news/390be61e-…` (item "SEC charges crypto firm"). Endpoints disparados y OK:

| Endpoint | Resultado |
|---|---|
| `GET /news/{id}` | 200 |
| `GET /news/{id}/verification-records` | 200 (empty state) |
| `GET /news/{id}/risk-reviews` | 200 (empty state) |
| `GET /editorial-readiness/news/{id}/latest` | 404 antes de calcular → 200 después (empty state correcto) |
| `POST /editorial-readiness/news/{id}/calculate` | **201** (botón "Recalcular" en UI) |
| `GET /audit/checks?entity_type=news_item&entity_id=…` | 200 |
| `GET /intake/signals?promoted_news_item_id=…` | 200 (trazabilidad) |

- Readiness visible: `score=9 · very_low · not_ready`, desglose por componente, `falta: VerificationRecord/RiskReview/AuditCheck/…`.
- **404 manejado** (`{"success":false,"error":"News item not found",...}`).
- Calculate funciona desde UI (write con API key). Score explícito: "no aprueba publicación".

## 12. E2E Intake → News — PASS ✅

Flujo completo ejercitado vía API + verificado en UI:

1. `POST /sources` → fuente "SEC Press Office" (`trust_level=T1`).
2. `POST /intake/signals` ×3 (SEC, Ethereum, Stablecoin).
3. `POST /intake/signals/{id}/dedupe` → `dedupe_status=unique`.
4. `POST /intake/signals/{id}/promote` → `signal_status=promoted`, `promoted_news_item_id` seteado.
5. Noticia creada visible en `/news` y `/news/:id`; trazabilidad vía `intake/signals?promoted_news_item_id`.

- **Promote NO publica**: las news quedan en `status=detected` (no `published`). ✅
- Acciones usan API key + `X-Actor-Role`. Errores 401/403/422 normalizados.
- UI de Intake muestra las 3 señales con estado dedupe/promoted + botón "Registrar señal".

## 13. E2E Sources — PASS ✅

- Lista fuentes reales del backend ("SEC Press Office" con trust tier + status).
- Botón "Registrar fuente" (`POST /api/v1/sources`) real. Sin botones falsos sin backend.

## 14. E2E Agents — PASS ✅

- Lista executions reales vía `GET /api/v1/agents/executions`.
- **Empty state correcto**: "Sin ejecuciones de agentes registradas"; cada agente ORION con "0 ejecuciones · sin actividad".
- **No simula ejecución** (nota explícita: aparecerán con `POST /api/v1/agents/executions`).

## 15. E2E Audit Checks vs Operational Audit — PASS ✅

Separación clara y etiquetada:

- **Audit Checks** → `GET /api/v1/audit/checks` (público). Empty state correcto.
  (El bloque "Alertas de integridad" está badgeado **DEMO — pendiente de endpoint**.)
- **Operational Audit** → `GET /api/v1/operational-audit/events` (cliente admin, `X-API-Key + X-Actor-Role`).
  - Con key válida (`system`): 200, muestra eventos RBAC reales de las escrituras QA
    (`readiness.calculate`, `intake.promote` → `succeeded`, con `permiso`, `actor: system · qa-e2e`, `corr:`).
  - Sin key → 401; role inválido → 403 (backend). En UI, error controlado con correlation ID.

## 16. Offline / retry — PASS ✅

- **Backend apagado** (`docker compose stop api`): recarga de `/news` → **no crashea, no pantalla blanca**,
  banner **"XMIP sin conexión"** + botón **Reintentar** (ErrorState profesional). Nav intacta.
- **Backend restaurado** (`start api`, ready ~3s) + clic **Reintentar** → datos vuelven, banner desaparece,
  health badge vuelve a **"online"**.

## 17. Auth negativo (frontend) — PASS ✅

- Dev server reiniciado con `VITE_API_KEY=totally-invalid-key`.
- Operational Audit → error **controlado**: "Rol sin permiso operational_audit.read" + guía de config,
  **correlation ID visible**, botón Reintentar, **sin stack trace, sin pantalla blanca**.
- Backend con key inválida → **403 "Invalid API key"** normalizado con `correlation_id`.
- Key válida restaurada → Operational Audit recupera eventos reales.

## 18. CORS / headers — PASS ✅

| Check | Resultado |
|---|---|
| `Access-Control-Allow-Origin` | `http://localhost:5173` (origin exacto, **sin wildcard**) |
| `Access-Control-Expose-Headers` | `X-Total-Count, X-Correlation-ID` |
| `Vary` | `Origin` |
| `X-Total-Count` en `/news` | presente |
| `X-Correlation-ID` | presente |
| Preflight `OPTIONS /news` | 200 · allow-methods/headers/origin correctos |

## 19. Logs — PASS ✅

`docker compose logs api --tail=250`:

- Requests visibles con `correlation_id` (78 ocurrencias).
- **0 fugas de secretos** (scan de smoke key / password / secret).
- **0 stack traces** inesperados (`Traceback` = 0).

## 20. Connectors guardrail — PASS ✅

Env runtime del container:

```
CONNECTORS_ENABLED=false
RSS_CONNECTOR_ENABLED=false
CONNECTOR_AUTO_PROMOTE=false
CONNECTOR_RUN_MODE=manual
CONNECTOR_REQUIRE_SOURCE_REFERENCE=true
```

- **0 connector auto-runs** en logs. No autopromote.

## 21. Bugs encontrados

**Ninguno de severidad bloqueante.** Observaciones menores (no bugs):

- **O1 — `net::ERR_ABORTED` en pares de requests (dev-only).** En modo dev, React StrictMode ejecuta
  los efectos dos veces; el `AbortController` cancela la primera petición y la segunda devuelve 200.
  No es un fallo: cada request aborted tiene su 200 correspondiente. No ocurre en el build de producción
  (`npm run build` verde). No hay error de consola asociado.
- **O2 — `APP_ENV` no mapeado en el compose.** El plan lista `APP_ENV=staging`, pero ni `backend/docker-compose.yml`
  ni `docker-compose.vps.yml` lo pasan; la app lee `ENVIRONMENT` (=`staging`, sí seteado). Sin impacto funcional;
  sólo nota de naming.
- **O3 — Key inválida → 403 (no 401).** El backend reserva 401 para *key faltante* y responde 403 "Invalid API key"
  para *key incorrecta*. Ambos normalizados; consistente con el contrato v0.1.

## 22. Fixes realizados

Ninguno. No se detectaron bugs críticos que justifiquen tocar backend/frontend (regla de la Fase 18).

## 23. Docs creados / modificados

- `docs/014-qa/E2E_QA_REPORT_V0.1.md` (este documento).

## 24. Riesgos residuales

- **R1 — Stack Caddy/nginx TLS no ejercitado en navegador.** La QA corrió contra `backend/docker-compose.yml`
  + Vite dev server, no contra `docker-compose.vps.yml` (Caddy TLS + frontend nginx estático), por requerir
  dominios/certs reales. El build de prod del frontend compila OK y el `Dockerfile` (nginx) es estructuralmente
  sano, pero el path servido por nginx detrás de Caddy con TLS debe recibir un smoke test en el entorno
  staging/VPS real (dominio de la Fase 15). **Recomendado antes de exponer públicamente.**
- **R2 — Datos de QA sintéticos.** El feed se pobló con 3 señales creadas en la corrida; no refleja volumen real
  ni el pipeline editorial completo (verification/risk/content/audit siguen en empty state por diseño del MVP).
- **R3 — Widgets DEMO.** Persisten bloques badgeados "DEMO / pendiente de endpoint" (Alertas de integridad en Audit,
  Command Center inferior, notificaciones Topbar, páginas secundarias). Esperado en v0.1; no confunden con datos reales.

---

## Resultado final: **GO ✅** para release candidate `v0.1.0-rc1`

Todos los criterios de cierre de la Fase 18 se cumplen: backend smoke, frontend build/lint/test,
flujos E2E principales, auth positivo/negativo, CORS, headers, logs sin secretos, connectors apagados,
offline state y recuperación, sin pantallas blancas ni errores críticos de consola.

**Condición de salida recomendada (no bloqueante):** ejecutar un smoke test del stack completo
`docker-compose.vps.yml` (Caddy + nginx + TLS) en el entorno staging/VPS antes de exponer a Internet (R1).
