# Production Deploy Smoke Checklist — v0.1

Use this checklist immediately before and during the production smoke for
`v0.1.0-rc1`.

## Preflight

- [ ] `v0.1.0-rc1` exists
- [ ] `v0.1.0-rc1` points to `ed62d8e8852cd0cbab7fa465be0d939b69eed18c`
- [ ] EC2 created
- [ ] Elastic IP associated
- [ ] DNS `app.xcripto.com` resolves to Elastic IP
- [ ] DNS `api.xcripto.com` resolves to Elastic IP
- [ ] Ports `80/443` open
- [ ] SSH restricted to operator IP
- [ ] Docker installed
- [ ] Docker Compose installed
- [ ] Git installed
- [ ] Repo cloned on the server
- [ ] `v0.1.0-rc1` checked out on the server

## Environment

- [ ] `.env.production` created outside the repo
- [ ] `.env.production` permissions set to `600`
- [ ] `APP_DOMAIN` set
- [ ] `API_DOMAIN` set
- [ ] `ACME_EMAIL` set
- [ ] `POSTGRES_USER` set
- [ ] `POSTGRES_PASSWORD` set
- [ ] `POSTGRES_DB` set
- [ ] `API_KEY` set
- [ ] `VITE_API_KEY` set
- [ ] `ENVIRONMENT=production`
- [ ] `APP_ENV=production`
- [ ] `DEBUG=false`
- [ ] `AUTH_ENABLED=true`
- [ ] `AUTO_CREATE_TABLES=false`
- [ ] `CORS_ALLOWED_ORIGINS` set to the exact frontend production origin
- [ ] `CORS_ALLOW_CREDENTIALS=false`
- [ ] `CONNECTORS_ENABLED=false`
- [ ] `RSS_CONNECTOR_ENABLED=false`
- [ ] `CONNECTOR_AUTO_PROMOTE=false`

## Stack

- [ ] PostgreSQL healthy
- [ ] API healthy
- [ ] Frontend up
- [ ] Caddy up
- [ ] No public PostgreSQL port
- [ ] No direct public backend port unless explicitly documented

## TLS and health

- [ ] TLS valid
- [ ] `/health` returns 200
- [ ] `/live` returns 200
- [ ] `/ready` returns 200
- [ ] `/openapi.json` returns 200

## API smoke

- [ ] `/news` returns 200
- [ ] `/news` includes `X-Total-Count`
- [ ] `/news` includes `X-Correlation-ID`
- [ ] `operational-audit` with API key returns 200
- [ ] `operational-audit` without API key returns 401

## CORS and headers

- [ ] CORS allows only the production frontend origin
- [ ] `Access-Control-Allow-Origin` is exact
- [ ] No wildcard origin is present
- [ ] `Access-Control-Expose-Headers` includes `X-Total-Count, X-Correlation-ID`
- [ ] `X-Correlation-ID` is present

## Frontend

- [ ] Frontend loads
- [ ] No blank screen
- [ ] No critical console errors
- [ ] Health badge online
- [ ] Empty states render correctly
- [ ] Protected actions use the API key

## Operations

- [ ] Logs contain no secrets
- [ ] Logs contain no unexpected stack traces
- [ ] Connectors remain disabled
- [ ] API restart passes
- [ ] Backup created
- [ ] Rollback documented

## Final decision

- [ ] GO
- [ ] NO-GO

Only mark `GO` if every required checkbox is complete and the runtime checks
match the expected outputs.
