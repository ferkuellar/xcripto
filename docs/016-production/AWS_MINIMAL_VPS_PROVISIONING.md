# AWS Minimal VPS Provisioning

Plan operativo mínimo para preparar un EC2 Ubuntu LTS como target de producción
o production-like para `v0.1.0-rc1`.

This document is infrastructure planning only. It does not change code, tags, or
release artifacts.

## Objective

Provision a single-host stack that can run:

- Caddy for TLS and reverse proxy
- frontend container
- API container
- PostgreSQL container with persistent storage

## Minimal architecture

- 1x EC2 Ubuntu LTS instance
- 1x Elastic IP
- 1x Security Group
- 1x EBS gp3 volume for the OS and runtime
- 1x persistent volume or mounted directory for PostgreSQL data
- 2 public DNS records:
  - `app.xcripto.com`
  - `api.xcripto.com`

Both DNS records should resolve to the same Elastic IP.

## EC2 recommendation

- OS: Ubuntu LTS
- CPU: 2 vCPU minimum
- Memory: 4 GB recommended
- Storage: 30-50 GB gp3 recommended
- Instance class: choose a burstable or general-purpose size that satisfies the
  memory target

## Security Group

- `22/tcp` only from the operator IP range
- `80/tcp` public
- `443/tcp` public
- No public PostgreSQL port
- No public backend API port unless a separate smoke decision explicitly requires it

## Elastic IP

- Allocate a static Elastic IP
- Associate it with the EC2 instance
- Point DNS A records to that Elastic IP

## DNS

- `app.xcripto.com` -> Elastic IP
- `api.xcripto.com` -> Elastic IP
- Wait for propagation before first Caddy start

## Software required on the server

- Docker
- Docker Compose
- Git
- cURL
- a shell capable of running the deployment commands

## Server directories

Recommended layout:

- `/srv/xmip` for the repository checkout
- `/srv/xmip/.env.production` for production env vars
- `/srv/xmip/backups/` for database backups
- `/var/lib/docker` or the Docker-managed volume path for runtime data

## `.env.production`

Create the environment file outside the repository and set permissions to `600`.
Never commit the file or print its contents in logs.

Required values:

- `APP_DOMAIN=app.xcripto.com`
- `API_DOMAIN=api.xcripto.com`
- `ACME_EMAIL=<real-email>`
- `POSTGRES_USER=xmip`
- `POSTGRES_PASSWORD=<strong-secret>`
- `POSTGRES_DB=xmip`
- `API_KEY=<strong-secret>`
- `VITE_API_KEY=<authorized-public-key-or-same-secret>`
- `ENVIRONMENT=production`
- `APP_ENV=production`
- `DEBUG=false`
- `AUTH_ENABLED=true`
- `AUTO_CREATE_TABLES=false`
- `CORS_ALLOWED_ORIGINS=https://app.xcripto.com`
- `CORS_ALLOW_CREDENTIALS=false`
- `CONNECTORS_ENABLED=false`
- `RSS_CONNECTOR_ENABLED=false`
- `CONNECTOR_AUTO_PROMOTE=false`

## Docker Compose

- Use `docker-compose.vps.yml`
- Load values from `/srv/xmip/.env.production`
- Keep PostgreSQL on the internal network only
- Keep API and frontend behind Caddy
- Do not expose the backend or PostgreSQL as public services

## Backup

Before first production smoke and before any upgrade with data:

- create a Postgres dump
- store it in `/srv/xmip/backups/`
- verify the file exists and is readable

Suggested file name:

- `backup_before_v0.1.0-rc1.sql`

## Rollback

Rollback should restore the previous stable tag or commit and re-run the compose
stack with the same env file.

Minimum steps:

1. Stop the stack.
2. Checkout the previous stable tag or commit.
3. Restart the stack with the same production env file.
4. Verify `/health` and `/ready`.

## Risks

- DNS propagation delay
- TLS issuance failure if the domain does not resolve
- Port 80/443 blocked by firewall or cloud networking
- Missing or incorrect production secrets
- PostgreSQL data loss if backups are not taken first
- Incorrect CORS origin if the frontend domain is changed later
- `VITE_API_KEY` exposure in the frontend bundle

## GO / NO-GO checklist

- [ ] EC2 provisioned
- [ ] Elastic IP associated
- [ ] DNS resolves to the Elastic IP
- [ ] Security Group allows only the required ports
- [ ] Docker installed
- [ ] Docker Compose installed
- [ ] Git installed
- [ ] Repository cloned
- [ ] `/srv/xmip/.env.production` created outside the repo
- [ ] Permissions set to `600`
- [ ] PostgreSQL backup path exists
- [ ] `v0.1.0-rc1` checked out
- [ ] Compose stack starts cleanly
- [ ] TLS validates
- [ ] Backend smoke passes
- [ ] Auth smoke passes
- [ ] CORS smoke passes
- [ ] Frontend smoke passes
- [ ] Logs are clean
- [ ] Restart validation passes
- [ ] Backup exists
- [ ] Rollback procedure confirmed

If any unchecked item remains, the production smoke stays `NO-GO`.
