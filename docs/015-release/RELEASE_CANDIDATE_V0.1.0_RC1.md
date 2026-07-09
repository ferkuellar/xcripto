# XCripto/XMIP Release Candidate v0.1.0-rc1

## Status

Release Candidate (pre-release).

- Date: 2026-07-09
- Branch: `release/v0.1.0-rc1`
- Base commit: `03d94e0` (main, includes Fases 14–19)
- Runtime version reported by backend (staging/VPS): `0.1.0-rc1` (`APP_VERSION` in `docker-compose.vps.yml`).
  Python package base version in `backend/pyproject.toml` stays `0.1.0`; the RC is marked by the git tag.

## Scope

- Backend XMIP MVP
- Frontend XMIP MVP
- PostgreSQL-backed deployment
- Hardened configuration
- API key auth
- CORS explicit allowlist
- API contract freeze
- E2E QA validated
- Minimal CI enabled

## Included phases

- Fase 14 — Production Hardening / Deploy Readiness
- Fase 15 — Staging Deployment Validation
- Fase 16 — API Contract Freeze v0.1
- Fase 17 — Frontend Production Integration
- Fase 18 — E2E QA Backend + Frontend
- Fase 19 — Minimal CI Pipeline

## Backend validation

Local (`backend/.venv`, `XMIP_DISABLE_DOTENV=1`):

- pytest result: **557 passed** (0 failed)
- ruff result: **All checks passed**

Docker/VPS-like smoke (`docker-compose.vps.yml`, api reachable on `:8000`):

- /health: **200** (`{"status":"ok","version":"0.1.0-rc1"}`)
- /live: **200**
- /ready: **200** — `checks.configuration=ok`, `checks.database=ok`
- /openapi.json: **200**
- /api/v1/news: **200**, `X-Total-Count` present, `X-Correlation-ID` present
- /api/v1/operational-audit/events: **200** with API key · **401** without key (normalized `{"success":false,"error":"Missing API key","correlation_id":...}`)

## Frontend validation

Local:

- build (`tsc -b && vite build`): **passed**
- lint (oxlint): **passed** (only pre-existing `only-export-components` warnings; exit 0)
- tests (vitest): **19 passed** (3 files)

Browser smoke (dev server → api on `:8000`, Playwright):

- Routes: `/` (Command Center), `/news`, `/news?q=SEC`, `/news/:id`, `/intake`, `/sources`, `/agents`, `/audit` (Audit Checks + Operational Audit).
- **0 console errors**, no white screens, health badge `online`, real data + correct empty states, correlation IDs visible in technical errors, protected actions use the API key.

## Docker / VPS-like full-stack smoke

Full production compose `docker-compose.vps.yml` (postgres + api + frontend nginx + caddy) built and booted (project `xmip-rc`, `*.localhost` domains, api port published for curls):

- All 4 containers up: `postgres` (healthy), `api` (healthy), `frontend` (nginx), `caddy`.
- Caddy edge over internal TLS reverse-proxies correctly:
  - `caddy → api` (SNI `api.localhost`) → **200** (`version 0.1.0-rc1`)
  - `caddy → frontend` (SNI `app.localhost`) → **200** (SPA served)
- Frontend nginx serves the SPA (`<title>XMIP — XCripto Media Intelligence Platform</title>`).

## Auth / CORS / headers

- Auth positive (API key + role): 200. Auth negative (no key): **401** normalized with `correlation_id`; invalid role: **403**.
- CORS explicit allowlist confirmed against the VPS config (`CORS_ALLOWED_ORIGINS=https://app.localhost`):
  - Allowed origin `https://app.localhost` → `Access-Control-Allow-Origin: https://app.localhost`, `Access-Control-Expose-Headers: X-Total-Count, X-Correlation-ID`, `Vary: Origin`.
  - Disallowed origin (`https://evil.com`) → **no** `Access-Control-Allow-Origin` (no wildcard).
  - `CORS_ALLOW_CREDENTIALS=false`.

## Logs

- Secret scan across `api`, `frontend`, `caddy` logs: **0 leaks** (no API keys / passwords / secrets printed).
- **0 unexpected stack traces**. `correlation_id` visible in api logs. No connector auto-runs.

## Security posture (runtime-confirmed in the VPS stack)

- `ENVIRONMENT=staging`
- `AUTH_ENABLED=true`
- `DEBUG=false`
- `AUTO_CREATE_TABLES=false`
- CORS wildcard forbidden (explicit allowlist only)
- SQLite forbidden in staging/production (PostgreSQL-backed; config-hardening test enforces this)
- `CONNECTORS_ENABLED=false`, `RSS_CONNECTOR_ENABLED=false`, `CONNECTOR_AUTO_PROMOTE=false`
- Connectors disabled by default (no env override needed; app defaults are disabled)

## Connector guardrails

Effective runtime config in the VPS api container:

```
connectors_enabled = False
rss_connector_enabled = False
connector_auto_promote = False
```

Result: no connector auto-runs, no autopromote, no automatic ingest.

## Known limitations

- RC is validated on local / VPS-like smoke, not on the final public production domain with a
  publicly-trusted TLS certificate. Caddy TLS was validated locally with an internal (self-signed)
  CA for `*.localhost`; **public-domain ACME/TLS must be validated during production deploy**.
- Connectors remain disabled by default.
- Production secrets are not stored in the repo (CI/smoke use throwaway values only).

## Rollback

Rollback target: previous stable `main` commit before the `v0.1.0-rc1` tag (`03d94e0`).

Rollback procedure:

1. Stop current stack (`docker compose -f docker-compose.vps.yml down`).
2. Checkout the previous stable commit or tag.
3. Restore previous environment variables (`.env.vps`).
4. Restart stack (`docker compose -f docker-compose.vps.yml up -d --build`).
5. Validate `/health` and `/ready`.
6. Verify frontend loads.
7. Review logs.

## Go / No-Go

**GO** for tag `v0.1.0-rc1`.

All gates satisfied:

- CI green (backend + frontend + docker smoke) — verified on the release PR.
- Backend tests pass (557) and ruff clean.
- Frontend build/lint pass; 19 tests pass.
- Docker/VPS-like full-stack smoke passes (incl. Caddy TLS edge).
- Auth positive/negative pass.
- CORS/headers pass (explicit allowlist, no wildcard).
- Logs do not leak secrets.
- No critical UI console errors.
- Connectors disabled by default.

Residual (non-blocking): public-domain TLS/ACME validation to be completed during production deploy.
