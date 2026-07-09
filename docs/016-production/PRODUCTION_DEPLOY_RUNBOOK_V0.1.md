# Production Deploy Runbook — v0.1

Operational runbook for provisioning a real production or production-like target
for `v0.1.0-rc1` before running the production smoke.

This runbook does not change code, tags, or release artifacts.

## Scope

- Provision the VPS target.
- Create a real external env file outside the repo.
- Deploy the compose stack.
- Validate TLS, backend, frontend, auth, CORS, logs, restart, and rollback.

## Related docs

- [PRODUCTION_ENV_TEMPLATE.md](./PRODUCTION_ENV_TEMPLATE.md)
- [AWS_MINIMAL_VPS_PROVISIONING.md](./AWS_MINIMAL_VPS_PROVISIONING.md)
- [PRODUCTION_DEPLOY_SMOKE_CHECKLIST_V0.1.md](./PRODUCTION_DEPLOY_SMOKE_CHECKLIST_V0.1.md)

## Variables required by the stack

See [PRODUCTION_ENV_TEMPLATE.md](./PRODUCTION_ENV_TEMPLATE.md) for the exact
variable list and safe placeholders.

## Provisioning checklist

### Host

- [ ] VPS provisioned and reachable over SSH.
- [ ] Docker installed.
- [ ] Docker Compose installed.
- [ ] Git installed.
- [ ] Sufficient disk space for images, database volume, and backups.
- [ ] Time sync enabled on the host.

### Network and firewall

- [ ] Inbound TCP 80 open.
- [ ] Inbound TCP 443 open.
- [ ] SSH restricted to the operator's access policy.
- [ ] No public exposure for PostgreSQL.

### DNS

- [ ] `APP_DOMAIN` A record points to the VPS IP.
- [ ] `API_DOMAIN` A record points to the VPS IP.
- [ ] DNS propagation verified before first Caddy start.
- [ ] No wildcard CORS origin planned.

### Reverse proxy

- [ ] Caddy or Nginx chosen and installed.
- [ ] TLS certificate automation configured.
- [ ] Reverse proxy can reach the frontend and API services on the internal network.

### Database

- [ ] PostgreSQL volume path planned.
- [ ] Backup path planned outside the database volume.
- [ ] Database credentials generated and stored outside the repo.
- [ ] Restore procedure confirmed before first production smoke.

### Environment file

- [ ] Create `.env.production` outside the repository.
- [ ] Do not commit the env file.
- [ ] Do not use `dev-secret`.
- [ ] Set `DEBUG=false`.
- [ ] Set `AUTH_ENABLED=true`.
- [ ] Set `AUTO_CREATE_TABLES=false`.
- [ ] Set `CONNECTORS_ENABLED=false`.
- [ ] Set `RSS_CONNECTOR_ENABLED=false`.
- [ ] Set `CONNECTOR_AUTO_PROMOTE=false`.
- [ ] Set `CORS_ALLOWED_ORIGINS` to the exact frontend origin.

## Deploy flow

### 1. Verify the release tag

```bash
git fetch origin --tags
git checkout main
git pull origin main
git show --no-patch --oneline v0.1.0-rc1^{}
git status --short
```

Expected:

- `v0.1.0-rc1` points to `ed62d8e8852cd0cbab7fa465be0d939b69eed18c`
- working tree is clean

### 2. Check out the release tag on the server

```bash
git fetch origin --tags
git checkout v0.1.0-rc1
git status
git rev-parse HEAD
```

Expected:

- `HEAD = ed62d8e8852cd0cbab7fa465be0d939b69eed18c`
- working tree clean

### 3. Create the env file

Create a real production env file outside the repo, for example:

```bash
cp .env.vps.example /srv/xmip/.env.production
chmod 600 /srv/xmip/.env.production
```

Then edit the file with real values for:

- `APP_DOMAIN`
- `API_DOMAIN`
- `ACME_EMAIL`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `API_KEY`
- `VITE_API_KEY`

### 4. Build and start the stack

```bash
docker compose --env-file /srv/xmip/.env.production -f docker-compose.vps.yml up -d --build postgres api frontend caddy
docker compose --env-file /srv/xmip/.env.production -f docker-compose.vps.yml ps
```

Expected:

- `postgres` healthy
- `api` healthy
- `frontend` up
- `caddy` up

### 5. Validate TLS

```bash
curl -I https://<frontend-domain>
curl -I https://<api-domain>/health
```

Expected:

- valid certificate
- frontend responds
- API responds

### 6. Backend smoke

```bash
curl -i https://<api-domain>/health
curl -i https://<api-domain>/live
curl -i https://<api-domain>/ready
curl -i https://<api-domain>/openapi.json
```

Expected:

- `/health` 200
- `/live` 200
- `/ready` 200
- `configuration=ok`
- `database=ok`
- `/openapi.json` 200
- `X-Correlation-ID` present where applicable

### 7. API smoke

```bash
curl -i \
  -H "X-API-Key: <API_KEY>" \
  -H "X-Actor-Role: system" \
  "https://<api-domain>/api/v1/news?limit=10&offset=0"

curl -i \
  -H "X-API-Key: <API_KEY>" \
  -H "X-Actor-Role: system" \
  "https://<api-domain>/api/v1/operational-audit/events?limit=10&offset=0"

curl -i \
  "https://<api-domain>/api/v1/operational-audit/events?limit=10&offset=0"
```

Expected:

- `/news` 200
- `/news` exposes `X-Total-Count`
- `/news` exposes `X-Correlation-ID`
- operational audit with key 200
- operational audit without key 401
- normalized error response

### 8. CORS smoke

```bash
curl -i \
  -H "Origin: https://<frontend-domain>" \
  "https://<api-domain>/api/v1/news?limit=10&offset=0"

curl -i \
  -H "Origin: https://<frontend-domain>" \
  -H "X-API-Key: <API_KEY>" \
  -H "X-Actor-Role: system" \
  "https://<api-domain>/api/v1/operational-audit/events?limit=10&offset=0"
```

Expected:

- `Access-Control-Allow-Origin: https://<frontend-domain>`
- `Access-Control-Expose-Headers: X-Total-Count, X-Correlation-ID`
- `X-Correlation-ID` present
- `X-Total-Count` present in `/news`
- no wildcard origin

### 9. Frontend smoke

Open:

```text
https://<frontend-domain>
```

Validate routes:

- `/`
- `/news`
- `/news?q=SEC`
- `/news/:id`
- Intake
- Sources
- Agents
- Audit
- Operational Audit

Expected:

- frontend loads
- no blank screen
- no critical console errors
- health badge online
- real data or correct empty states
- protected actions use the API key
- technical errors show correlation IDs

### 10. Restart validation

```bash
docker compose --env-file /srv/xmip/.env.production -f docker-compose.vps.yml restart api
docker compose --env-file /srv/xmip/.env.production -f docker-compose.vps.yml ps
curl -i https://<api-domain>/ready
```

Expected:

- API healthy
- `/ready` 200
- `configuration=ok`
- `database=ok`

### 11. Logs validation

```bash
docker compose --env-file /srv/xmip/.env.production -f docker-compose.vps.yml logs api --tail=250
docker compose --env-file /srv/xmip/.env.production -f docker-compose.vps.yml logs frontend --tail=100
docker compose --env-file /srv/xmip/.env.production -f docker-compose.vps.yml logs caddy --tail=100
```

Expected:

- no leaked secrets
- no unexpected stack traces
- correlation IDs visible
- no connector auto-runs

### 12. Backup

Before first production smoke or any upgrade with data:

```bash
docker compose --env-file /srv/xmip/.env.production -f docker-compose.vps.yml exec postgres \
  pg_dump -U xmip xmip > /srv/xmip/backups/backup_before_v0.1.0-rc1.sql
ls -lh /srv/xmip/backups/backup_before_v0.1.0-rc1.sql
```

Expected:

- backup file exists
- backup path is outside the repo

### 13. Rollback

Rollback target:

- previous stable tag or commit before `v0.1.0-rc1`

Rollback procedure:

```bash
docker compose --env-file /srv/xmip/.env.production -f docker-compose.vps.yml down
git checkout <previous-stable-tag-or-commit>
docker compose --env-file /srv/xmip/.env.production -f docker-compose.vps.yml up -d --build
curl -i https://<api-domain>/health
curl -i https://<api-domain>/ready
```

Expected:

- `/health` 200
- `/ready` 200

## Go / No-Go criteria

GO only if all of the following are true:

- real production or production-like target exists
- TLS validates on the real domains
- frontend responds
- API responds
- `/ready` is OK
- PostgreSQL is OK
- auth positive and negative smoke pass
- CORS is exact and no wildcard is used
- headers are present
- logs are clean
- restart validation passes
- backup exists
- rollback is confirmed
- connectors remain disabled

Otherwise the result is `NO-GO`.

## Current blocker

At the moment this environment still lacks the real production target inputs:

- no provisioned frontend/API domains
- no real `.env.production` / `.env.vps`
- no allowed production secrets

That means the runbook is ready, but the production smoke is not yet runnable.

## Local smoke note

On this workspace, the local runtime smoke completed only after overriding
`API_DOMAIN` to `api.localhost` for the compose run. The checked-in
`.env.local.production` remains the requested template, but `https://127.0.0.1`
did not complete TLS negotiation reliably for the API endpoint on this host.
