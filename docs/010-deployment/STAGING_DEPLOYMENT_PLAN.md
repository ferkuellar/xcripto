# XMIP Staging Deployment Plan

| Campo | Valor |
| --- | --- |
| Proyecto | ORION / XCripto / XMIP |
| Tipo | Plan de despliegue (staging) |
| Estado | Plan — sin ejecutar, sin recursos creados |
| Base | `v0.1.0-rc1` (main `6a0e534`) |
| Fecha | 2026-07-04 |

> Este documento **decide** cómo desplegar staging. No ejecuta deploy ni crea
> recursos. Los precios se expresan cualitativamente (low/medium/high); verificar
> pricing oficial vigente antes de aprovisionar.

## 1. Objetivo
Levantar un entorno **staging** de XMIP (backend API + admin frontend + PostgreSQL
gestionado) que reproduzca la validación local E2E de `v0.1.0-rc1` en la nube, con
auth por API key, CORS restringido, migraciones Alembic y smoke tests remotos.

## 2. Alcance
- Backend FastAPI (Docker) desplegado y accesible por HTTPS.
- Frontend admin (Vite SPA estático) desplegado y apuntando al backend staging.
- PostgreSQL gestionado con `alembic upgrade head`.
- Auth API key + RBAC por headers activados.
- Health (`/health`,`/live`,`/ready`), smoke/admin/newsroom QA remotos, logs y
  `OperationalAuditLog` verificados.

## 3. No incluido
Login de usuarios (JWT/OAuth), conectores externos reales, LLM real, scraping,
publicación/trading real, autoescalado, alta disponibilidad multi-región, CD
automático, observabilidad avanzada (APM/tracing), y producción. Staging es un
entorno **interno** de validación, no público.

## 4. Arquitectura recomendada
```
[navegador interno]
   │  HTTPS
   ▼
admin-staging.<domain>  ── Vercel (SPA estático, Vite build)
   │  fetch  X-API-Key + X-Actor-*
   ▼
api-staging.<domain>    ── Render (contenedor Docker FastAPI, /ready healthcheck)
   │  asyncpg (TLS)
   ▼
PostgreSQL gestionado   ── Render Postgres (o Neon)
```
Backend y DB en el mismo proveedor/región (latencia y red simples). Frontend como
estático en CDN con rollback instantáneo. Migraciones al arrancar el contenedor
(idéntico al `docker-compose` local) o como release command.

## 5. Opciones evaluadas
Ver `STAGING_COST_RISK_MATRIX.md` para la comparación completa. Resumen:

| Capa | Candidatos |
| --- | --- |
| Backend API | Render, Railway, Fly.io, VPS+Docker, AWS App Runner/Lightsail |
| PostgreSQL | Render PG, Railway PG, Neon, Supabase, (RDS a futuro) |
| Frontend | Vercel, Netlify |

## 6. Proveedor recomendado
**Opción principal — Render (backend + Postgres) + Vercel (frontend).**
Justificación (no por moda): XMIP ya trae `Dockerfile` → Render despliega el
contenedor tal cual (sin buildpacks); Postgres gestionado del mismo proveedor
minimiza red/latencia y secretos; healthcheck nativo contra `/ready`; rollback por
redeploy del commit/imagen anterior; gestión de env vars/secretos integrada; Vercel
sirve el SPA con dominios custom y rollback instantáneo.

**Alternativa — Railway (backend + Postgres) + Vercel**: aún más simple de cablear
(plantillas monorepo), buena DX; menor control fino de red que un VPS.

**Alternativa de control — VPS + Docker Compose**: máximo control y costo predecible,
pero más operación (TLS, backups, actualizaciones a mano). Ver matriz.

## 7. Backend deployment
- Deploy del `backend/Dockerfile` (python:3.12-slim, `uvicorn app.main:app`).
- Puerto interno 8000; el proveedor termina TLS y mapea a 443.
- Comando de arranque idéntico al compose: `alembic upgrade head && uvicorn ...`
  (una sola instancia en staging evita carreras de migración).
- Healthcheck del proveedor → `GET /ready` (valida configuración + DB).
- Env vars vía el secret store del proveedor (ver `STAGING_ENVIRONMENT_VARIABLES.md`).
- Sin `AUTO_CREATE_TABLES`; el esquema lo crea Alembic.

## 8. Frontend deployment
- Build estático: `npm ci && npm run build` → `dist/` servido por Vercel/Netlify.
- Variables `VITE_*` se **incrustan en build** (públicas) → ver nota de seguridad.
- SPA con HashRouter: no requiere rewrites de servidor, pero configurar fallback a
  `index.html` de todas formas.
- Dominio `admin-staging.<domain>`.

## 9. PostgreSQL deployment
- Instancia gestionada (Render PG o Neon), TLS obligatorio, en la misma región que el
  backend.
- `DATABASE_URL=postgresql+asyncpg://<user>:<pass>@<host>:5432/<db>?ssl=require`.
- Backups automáticos habilitados (ver `STAGING_ROLLBACK_PLAN.md` §6).
- Neon aporta *branching* de DB (útil para resetear staging sin borrar datos base).

## 10. Dominios/subdominios
| Rol | Host |
| --- | --- |
| Admin SPA | `admin-staging.<domain>` |
| API | `api-staging.<domain>` |
Ambos con TLS gestionado por el proveedor. Evitar exponer la DB públicamente
(solo acceso desde el backend / IP allowlist).

## 11. CORS
`CORS_ALLOWED_ORIGINS=https://admin-staging.<domain>` (exacto, sin `*`).
`CORS_ALLOW_CREDENTIALS=false` (auth por headers, no cookies).
Headers permitidos: `Content-Type, X-API-Key, X-Actor-Role, X-Actor-Id, X-Correlation-ID`.
Métodos: `GET, POST, PATCH, DELETE, OPTIONS`.

## 12. Seguridad
- **TLS** en API y frontend (gestionado por el proveedor).
- **API key** (`AUTH_ENABLED=true`) para endpoints de escritura + RBAC por
  `X-Actor-Role`/`X-Actor-Id`.
- ⚠️ `VITE_API_KEY` se incrusta en el bundle → **es visible para quien acceda al SPA**.
  Aceptable solo para staging **interno**; mitigar con acceso restringido al frontend
  (protección por contraseña de Vercel/Netlify o IP allowlist) y una key de staging
  distinta de cualquier futura de producción. **P10 sustituirá esto por auth real
  (JWT/OAuth)**; no promover este patrón a producción.
- Secretos solo en el secret store del proveedor; **nunca** commitear `.env` real.
- DB no expuesta públicamente; backups cifrados.
- `OPERATIONAL_AUDIT_ENABLED=true` para trazabilidad.

## 13. Alembic/migraciones
- `alembic upgrade head` al arrancar el contenedor (o como release command del
  proveedor). Head actual: `20260702_0011`.
- Una sola instancia durante la migración (evita carreras).
- Downgrade solo con backup previo (ver rollback plan).

## 14. Smoke tests
Tras el deploy, contra el dominio staging:
```bash
python scripts/smoke_test.py --base-url https://api-staging.<domain> --api-key <key>
python scripts/admin_contract_smoke.py --base-url https://api-staging.<domain> --api-key <key> --actor-role admin
python scripts/local_newsroom_qa.py --base-url https://api-staging.<domain> --api-key <key> --actor-role admin
```

## 15. Operational QA
Revisar logs del backend, respuestas de `/ready` (DB ok), y `OperationalAuditLog`
(vía `/api/v1/admin/audit/summary`) para confirmar trazabilidad. Validar CORS desde
el SPA (preflight OK) y las secciones admin sin crashes.

## 16. Costos estimados
Cualitativos (verificar pricing oficial). Render/Railway/Neon/Vercel ofrecen tiers
hobby/free adecuados para un staging interno de baja carga → **costo total: low**.
Ver `STAGING_COST_RISK_MATRIX.md`.

## 17. Riesgos
- `VITE_API_KEY` público en el bundle (mitigado con acceso restringido; resuelto en P10).
- Migración en múltiples instancias (mitigado: 1 instancia en staging).
- Cold starts / sleep de tiers free (aceptable en staging).
- Deriva entre `docker-compose` local y config del proveedor (mitigado: mismo Dockerfile).
- Pricing/limits pueden cambiar (verificar antes de aprovisionar).

## 18. Decisión final
**Principal: Render (backend Docker + Render Postgres) + Vercel (frontend).**
**Alternativa: Railway (backend + Postgres) + Vercel.**
**Control: VPS + Docker Compose** si se requiere costo fijo/control total.
DB alterna: **Neon** (serverless + branching). Ejecutar solo tras aprobación explícita;
esta fase entrega únicamente el plan.
