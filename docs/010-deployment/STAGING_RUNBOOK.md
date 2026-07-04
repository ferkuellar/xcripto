# XMIP Staging Runbook

> Checklist operativo para desplegar y validar staging. Comandos genéricos: sustituir
> `<domain>` y `<key>`. No ejecutar hasta aprobación explícita; no commitear secretos.

## 1. Preflight
- [ ] `main` verde en CI, tag `v0.1.0-rc1` presente.
- [ ] Proveedores elegidos (ver `STAGING_DEPLOYMENT_PLAN.md` §18) y cuentas listas.
- [ ] Dominios `api-staging.<domain>` / `admin-staging.<domain>` disponibles.
- [ ] Secretos de staging generados (API key) y guardados en el secret store.

## 2. Crear DB
- [ ] Provisionar PostgreSQL gestionado (Render PG / Neon), misma región que el backend.
- [ ] Obtener `DATABASE_URL` con `ssl=require`; habilitar backups automáticos.
- [ ] Restringir acceso de red (solo backend / IP allowlist).

## 3. Configurar env vars
- [ ] Cargar todas las variables de `STAGING_ENVIRONMENT_VARIABLES.md` (backend) en el
      secret store del proveedor. `AUTH_ENABLED=true`, `AUTO_CREATE_TABLES=false`.

## 4. Deploy backend
- [ ] Conectar el repo, apuntar al `backend/Dockerfile`.
- [ ] Comando de arranque: `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000`.
- [ ] Healthcheck del proveedor → `GET /ready`. Una sola instancia para la migración.

## 5. Correr Alembic upgrade head
- [ ] Verificar en logs la cadena hasta `20260702_0011`. Si el proveedor usa release
      command, ejecutar `alembic upgrade head` allí.

## 6-8. Validar health
```bash
curl https://api-staging.<domain>/health   # {"status":"ok",...}
curl https://api-staging.<domain>/live     # {"status":"alive",...}
curl https://api-staging.<domain>/ready    # {"status":"ready","checks":{"database":"ok",...}}
```

## 9. Exportar OpenAPI
```bash
curl https://api-staging.<domain>/openapi.json -o openapi-staging.json   # sanity del contrato
```

## 10. Deploy frontend
- [ ] Configurar `VITE_*` en el host de frontend; build `npm ci && npm run build`.
- [ ] Publicar `dist/` en `admin-staging.<domain>`; fallback SPA a `index.html`.
- [ ] Activar acceso restringido (password/IP allowlist) por la key incrustada.

## 11. Validar CORS
```bash
curl -s -D - -o /dev/null -X OPTIONS https://api-staging.<domain>/api/v1/admin/dashboard/overview \
  -H "Origin: https://admin-staging.<domain>" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: x-api-key,x-actor-role,x-actor-id"
# Esperado: 200 + access-control-allow-origin: https://admin-staging.<domain>
```

## 12-14. Smoke tests remotos
```bash
cd backend
python scripts/smoke_test.py --base-url https://api-staging.<domain> --api-key <key>
python scripts/admin_contract_smoke.py --base-url https://api-staging.<domain> --api-key <key> --actor-role admin
python scripts/local_newsroom_qa.py --base-url https://api-staging.<domain> --api-key <key> --actor-role admin
```
Esperado: `Smoke test passed.`, `Admin contract smoke test passed.`, `RESULTADO: PASS`.

## 15. Revisar logs
- [ ] Sin errores 5xx ni tracebacks; ver correlación por `X-Correlation-ID`.

## 16. Revisar OperationalAuditLog
```bash
curl https://api-staging.<domain>/api/v1/admin/audit/summary \
  -H "X-API-Key: <key>" -H "X-Actor-Role: admin"
```
- [ ] Eventos de auth/rbac/editorial registrados con actor y decisión.

## 17. GO / NO-GO staging
GO si: migraciones en head, health/ready verdes, los 3 smoke tests PASS, CORS correcto,
logs limpios y audit log poblado. NO-GO → aplicar `STAGING_ROLLBACK_PLAN.md`.
