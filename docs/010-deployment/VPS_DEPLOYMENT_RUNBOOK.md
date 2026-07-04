# XMIP VPS Deployment Runbook

Despliegue full-stack en un VPS con Docker: **Caddy (TLS automático) + frontend
(nginx) + api (FastAPI) + PostgreSQL 16**. Un solo `docker compose`. Solo Caddy queda
expuesto (80/443); api y postgres viven en la red interna.

Archivos: `docker-compose.vps.yml`, `Caddyfile`, `.env.vps.example`,
`frontend/Dockerfile`, `frontend/nginx.conf`, `backend/Dockerfile`.

## 1. Preflight (una vez)
- [ ] VPS con Docker + Docker Compose (Ubuntu 22.04+ recomendado).
- [ ] Dos subdominios con **A records → IP del VPS** ya propagados:
      `xmip.<domain>` (admin) y `api.xmip.<domain>` (API). Caddy los necesita
      resolubles para emitir TLS.
- [ ] Puertos 80 y 443 abiertos en el firewall del VPS.
- [ ] Repo clonado en el VPS (`git clone` + `git checkout main`).

## 2. Configurar secretos
```bash
cp .env.vps.example .env.vps
# editar .env.vps: APP_DOMAIN, API_DOMAIN, ACME_EMAIL,
#   POSTGRES_PASSWORD (fuerte), API_KEY (staging), VITE_API_KEY (= API_KEY)
```
`.env.vps` está gitignored — **nunca** commitearlo.

## 3. Levantar el stack
```bash
docker compose -f docker-compose.vps.yml --env-file .env.vps up -d --build
```
- postgres arranca y pasa healthcheck.
- api corre `alembic upgrade head` (cadena hasta `20260702_0011`) y luego uvicorn.
- frontend se compila (Vite) con la URL del API incrustada y se sirve por nginx.
- Caddy obtiene certificados TLS para ambos dominios en la primera petición.

## 4. Verificar
```bash
curl https://api.<domain>/health           # {"status":"ok",...}
curl https://api.<domain>/ready            # database: ok
curl -I https://xmip.<domain>              # 200, admin SPA
```
Preflight CORS:
```bash
curl -i -X OPTIONS https://api.<domain>/api/v1/admin/dashboard/overview \
  -H "Origin: https://xmip.<domain>" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: X-API-Key,X-Actor-Role,X-Actor-Id"
# access-control-allow-origin: https://xmip.<domain>
```
Smoke remoto (desde tu máquina):
```bash
cd backend
python scripts/smoke_test.py --base-url https://api.<domain> --api-key <API_KEY>
python scripts/admin_contract_smoke.py --base-url https://api.<domain> --api-key <API_KEY> --actor-role admin
python scripts/local_newsroom_qa.py --base-url https://api.<domain> --api-key <API_KEY> --actor-role admin
```

## 5. Operación
```bash
docker compose -f docker-compose.vps.yml --env-file .env.vps logs -f api     # logs
docker compose -f docker-compose.vps.yml --env-file .env.vps ps              # estado
docker compose -f docker-compose.vps.yml --env-file .env.vps restart api     # reinicio api
```
Backup Postgres antes de cada actualización con migraciones:
```bash
docker compose -f docker-compose.vps.yml --env-file .env.vps exec postgres \
  pg_dump -U xmip xmip > backup_$(date +%F).sql
```

## 6. Actualizar (nueva versión)
```bash
git pull origin main
docker compose -f docker-compose.vps.yml --env-file .env.vps up -d --build
```
Las migraciones corren solas al reiniciar el api. Hacer backup (§5) antes si hay
migraciones nuevas.

## 7. Rollback
- Backend/frontend: `git checkout <tag/commit anterior>` + `up -d --build`.
- DB: restaurar backup (`psql`/`pg_restore`) si una migración dañó datos. No borrar el
  volumen `xmip_pgdata` sin confirmación. Ver `STAGING_ROLLBACK_PLAN.md`.

## 8. Notas de seguridad
- `VITE_API_KEY` queda **incrustado y público** en el bundle → protege el admin con
  acceso restringido (Basic Auth en Caddy o allowlist) hasta P10 (auth real).
  Basic Auth rápido en el bloque `{$APP_DOMAIN}` del `Caddyfile`:
  ```
  basic_auth { usuario <hash-bcrypt> }
  ```
  (generar hash con `docker run caddy caddy hash-password`).
- Rotar `API_KEY`/`VITE_API_KEY` si se filtran.
- La DB no se expone públicamente (sin `ports:` en postgres).
- Mantener el VPS actualizado (`apt upgrade`) y el firewall cerrado salvo 80/443/22.

## 9. Estado de validación
`docker-compose.vps.yml` valida con `docker compose config` y la imagen del frontend
compila localmente. La emisión de TLS de Caddy y el enrutado por dominio **solo se
pueden probar en el VPS real** con DNS apuntando a él — verificar en el §4 tras el
primer deploy.
