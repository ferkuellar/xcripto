# Production Deploy Smoke — v0.1.0-rc1

## Status

NO-GO

## Release candidate

Tag: `v0.1.0-rc1`  
Commit: `ed62d8e8852cd0cbab7fa465be0d939b69eed18c`  
Date: `2026-07-09`  
Operator: `Codex`

## Environment

Frontend domain: not provisioned
API domain: not provisioned
Reverse proxy: not deployed
Database: not provisioned
TLS: not validated

## Configuration

- `ENVIRONMENT=production`
- `DEBUG=false`
- `AUTH_ENABLED=true`
- `AUTO_CREATE_TABLES=false`
- `CORS_ALLOWED_ORIGINS` not set for a real production origin
- `CONNECTORS_ENABLED=false`
- `RSS_CONNECTOR_ENABLED=false`
- `CONNECTOR_AUTO_PROMOTE=false`

Secrets are not stored in the repository.

## Backend smoke

- `/health`: not executed against a production or public production-like target
- `/live`: not executed against a production or public production-like target
- `/ready`: not executed against a production or public production-like target
- `/openapi.json`: not executed against a production or public production-like target
- `/api/v1/news`: not executed against a production or public production-like target
- `/api/v1/operational-audit/events`: not executed against a production or public production-like target

## Frontend smoke

Routes tested:

- `/`
- `/news`
- `/news/:id`
- Intake
- Sources
- Agents
- Audit
- Operational Audit

Result: not executed against a production or public production-like target

## Auth

- API key valid: not validated
- Missing API key: not validated
- Invalid role if tested: not validated

## CORS and headers

- `Access-Control-Allow-Origin`: not validated
- `Access-Control-Expose-Headers`: not validated
- `X-Correlation-ID`: not validated
- `X-Total-Count`: not validated

## Logs

- Secrets leaked: not assessed in a production runtime
- Stack traces: not assessed in a production runtime
- Correlation IDs: not assessed in a production runtime

## Connectors

- `CONNECTORS_ENABLED=false`
- `RSS_CONNECTOR_ENABLED=false`
- `CONNECTOR_AUTO_PROMOTE=false`
- Auto-runs observed: not validated in a production runtime

## Restart validation

- API restart: not executed
- Stack restart: not executed

## Backup

- Backup created: not created
- Backup path: not available

## Rollback

Rollback target: previous stable tag or commit before `v0.1.0-rc1`
Rollback procedure confirmed: yes

## Issues found

- No real production target was available in this workspace.
- No `.env.production` or `.env.vps` with real `APP_DOMAIN`, `API_DOMAIN`, and `ACME_EMAIL` was available.
- The only local production-like reference env present in `backend/.env` uses `dev-secret`, which is explicitly disallowed for this smoke.
- Public-domain TLS / ACME, CORS, API smoke, and browser smoke could not be executed without real deployment inputs.

## Fixes applied

- None. No code or tag changes were made.

## Residual risks

- Production smoke remains unverified on a real public target.
- TLS and CORS behavior on the intended production domains remain unknown.
- Backend/API/browser smoke remain unexecuted against the intended deployment.

## Final decision

NO-GO
