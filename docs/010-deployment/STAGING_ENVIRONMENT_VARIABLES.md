# XMIP Staging Environment Variables

> **Sin valores secretos reales.** Los placeholders `<...>` se resuelven en el secret
> store del proveedor (Render/Railway/Vercel), nunca en un `.env` commiteado.

## Backend (FastAPI) — secret store del proveedor

```env
APP_NAME=XMIP Backend
APP_VERSION=0.1.0-rc1
ENVIRONMENT=staging
# APP_ENV=staging is also accepted if the provider reserves ENVIRONMENT.
DEBUG=false
LOG_LEVEL=INFO

# PostgreSQL gestionado (asyncpg + TLS). No exponer la DB públicamente.
DATABASE_URL=<managed-postgres-url>   # postgresql+asyncpg://user:pass@host:5432/db?ssl=require
AUTO_CREATE_TABLES=false
DB_HEALTHCHECK_ENABLED=true

# Auth MVP por API key + RBAC por headers.
AUTH_ENABLED=true
API_KEY=<staging-api-key-secret>
API_KEY_HEADER_NAME=X-API-Key

# CORS restringido al SPA de staging (sin comodines, sin cookies).
CORS_ALLOWED_ORIGINS=https://admin-staging.<domain>
CORS_ALLOW_CREDENTIALS=false
CORS_ALLOWED_METHODS=GET,POST,PATCH,DELETE,OPTIONS
CORS_ALLOWED_HEADERS=Content-Type,X-API-Key,X-Actor-Role,X-Actor-Id,X-Correlation-ID

# Logging / auditoría.
REQUEST_LOGGING_ENABLED=true
REQUEST_BODY_LOGGING_ENABLED=false
RESPONSE_BODY_LOGGING_ENABLED=false
REQUEST_TIMEOUT_SECONDS=30
OPERATIONAL_AUDIT_ENABLED=true

# Conectores reales (P9). OFF por defecto; kill switches. Nunca publican; el ingest crea
# IntakeSignals. CONNECTOR_AUTO_PROMOTE debe quedar en false en staging.
CONNECTORS_ENABLED=false
RSS_CONNECTOR_ENABLED=false
RSS_CONNECTOR_MAX_ITEMS=20
RSS_CONNECTOR_TIMEOUT_SECONDS=10
RSS_CONNECTOR_ALLOWED_DOMAINS=coindesk.com,cointelegraph.com,decrypt.co,theblock.co
CONNECTOR_AUDIT_ENABLED=true
CONNECTOR_REQUIRE_SOURCE_REFERENCE=true
CONNECTOR_AUTO_PROMOTE=false
```

## Frontend (Vite) — build-time del proveedor de frontend

```env
VITE_API_BASE_URL=https://api-staging.<domain>
VITE_API_KEY=<staging-admin-key>
VITE_ACTOR_ROLE=admin
VITE_ACTOR_ID=staging-admin
```

## Notas de seguridad
- `staging`, `production` y `prod` fallan configuración si usan SQLite, CORS wildcard,
  `AUTH_ENABLED=false`, `API_KEY` vacío o placeholders como `dev-secret`.
- `AUTO_CREATE_TABLES` debe quedar en `false`; migraciones siempre por Alembic.
- **`VITE_API_KEY` se incrusta en el bundle y es público** para cualquiera que acceda
  al SPA. No es una solución productiva. Para **staging interno** es temporalmente
  aceptable **si** el frontend está tras acceso restringido (protección por contraseña
  del host o IP allowlist) y la key es exclusiva de staging.
- **P10 reemplazará esto con autenticación real** (JWT/OAuth + sesión); no promover el
  patrón de key incrustada a producción.
- `API_KEY` (backend) y `VITE_API_KEY` (frontend) deben ser el **mismo** secreto de
  staging, distinto de dev (`dev-secret`) y de cualquier futuro de producción.
- Rotar la key de staging si se filtra; los secretos viven solo en el proveedor.

## Diferencias vs local (`.env.local.production.example`)
| Variable | Local | Staging |
| --- | --- | --- |
| `ENVIRONMENT` | production | staging |
| `DATABASE_URL` | `postgresql+asyncpg://xmip:xmip@postgres:5432/xmip` | managed + `ssl=require` |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:5173` | `https://admin-staging.<domain>` |
| `API_KEY` | `dev-secret` | secreto de staging (secret store) |
| `VITE_API_BASE_URL` | `http://127.0.0.1:8010` | `https://api-staging.<domain>` |
