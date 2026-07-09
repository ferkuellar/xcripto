# Production Environment Template

This file is a template only. Do not commit secrets.

Use it as the source of truth for the variables that must exist outside the repo
before attempting `Production Deploy Smoke — v0.1.0-rc1`.

## Required variables

```env
APP_DOMAIN=<frontend-domain>
API_DOMAIN=<api-domain>
ACME_EMAIL=<real-email>

POSTGRES_USER=xmip
POSTGRES_PASSWORD=<strong-secret>
POSTGRES_DB=xmip

API_KEY=<strong-secret>
VITE_API_KEY=<same-or-authorized-public-key>

ENVIRONMENT=production
APP_ENV=production
DEBUG=false
AUTH_ENABLED=true
AUTO_CREATE_TABLES=false
CORS_ALLOWED_ORIGINS=https://<frontend-domain>
CORS_ALLOW_CREDENTIALS=false
CONNECTORS_ENABLED=false
RSS_CONNECTOR_ENABLED=false
CONNECTOR_AUTO_PROMOTE=false
```

## Notes

- `APP_DOMAIN` and `API_DOMAIN` must be real DNS names that already resolve to the
  target VPS before the first Caddy start.
- `CORS_ALLOWED_ORIGINS` must be an exact allowlist value, not a wildcard.
- `API_KEY` and `VITE_API_KEY` must not be placeholders.
- `VITE_API_KEY` is embedded into the frontend bundle, so treat it as public
  exposure and restrict access to the frontend accordingly.
- The production smoke must not use `dev-secret`.
- Keep this file out of git if you turn it into a live env file.

## Compose-derived requirements

These values are required by `docker-compose.vps.yml` even if they are not all
declared in the env template above:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `API_KEY`
- `VITE_API_KEY`
- `APP_DOMAIN`
- `API_DOMAIN`
- `ACME_EMAIL`

The compose file also hardcodes these runtime values:

- `APP_VERSION=0.1.0-rc1`
- `API_KEY_HEADER_NAME=X-API-Key`
- `VITE_ACTOR_ROLE=admin`
- `VITE_ACTOR_ID=vps-admin`
- `CORS_ALLOWED_METHODS=GET,POST,PATCH,DELETE,OPTIONS`
- `CORS_ALLOWED_HEADERS=Content-Type,X-API-Key,X-Actor-Role,X-Actor-Id,X-Correlation-ID`
- `OPERATIONAL_AUDIT_ENABLED=true`
- `DB_HEALTHCHECK_ENABLED=true`
- `DEBUG=false`
- `AUTO_CREATE_TABLES=false`
- `AUTH_ENABLED=true`

## Deployment file location

Use a production env file outside the repository, for example:

- `/opt/xmip/.env.production`
- `/srv/xmip/.env.production`

The exact path can vary by host, but it must not be versioned.
