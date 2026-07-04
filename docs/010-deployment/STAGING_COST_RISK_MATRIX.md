# XMIP Staging Cost / Risk Matrix

> Costos y complejidad **cualitativos** (low/medium/high). No se consultó pricing en
> vivo; verificar tarifas y límites oficiales vigentes antes de aprovisionar.

## Backend API

| Provider | Deploy Docker | Rollback | Ops complexity | Secrets | Logs | Custom domain | Costo | Recomendado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Render** | nativo (Dockerfile) | 1-click deploy previo | low | secret store | sí | sí | low–med | ✅ principal |
| **Railway** | nativo | 1-click | low | secret store | sí | sí | low–med | ✅ alternativa |
| **Fly.io** | nativo (fly.toml) | releases | medium | secrets CLI | sí | sí | low–med | ◻ viable |
| **VPS + Docker** | manual | redeploy manual | high | a mano | a mano | manual (TLS propio) | low fijo | ◻ control |
| **AWS App Runner/Lightsail** | sí | media | medium–high | Secrets Mgr | CloudWatch | sí | med | ◻ a futuro |

## PostgreSQL

| Provider | Gestionado | Backups | Branching | TLS | Ops | Costo | Recomendado |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Render Postgres** | sí | automáticos | no | sí | low | low–med | ✅ (mismo proveedor) |
| **Neon** | sí (serverless) | sí | **sí** | sí | low | low (free tier) | ✅ (branching staging) |
| **Railway Postgres** | sí | sí | no | sí | low | low–med | ✅ (si backend en Railway) |
| **Supabase** | sí | sí | no | sí | low | low–med | ◻ (trae extras no usados) |
| **AWS RDS** | sí | sí | no | sí | high | med–high | ◻ solo producción futura |

## Frontend

| Provider | SPA estático | Rollback | Preview deploys | Acceso restringido | Custom domain | Costo | Recomendado |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Vercel** | sí | instantáneo | sí | password/allowlist | sí | low (hobby) | ✅ principal |
| **Netlify** | sí | instantáneo | sí | password/allowlist | sí | low (free) | ✅ alternativa |

## Riesgos por opción
- **Render/Railway/Neon/Vercel (free/hobby):** cold starts / sleep en inactividad y
  límites de horas/almacenamiento → aceptable para staging interno de baja carga.
- **VPS:** costo fijo y control, pero TLS, backups y parches son responsabilidad propia
  (ops high).
- **AWS:** máxima capacidad pero complejidad y costo altos; sobredimensionado para
  staging. Reservar para producción.
- **Transversal:** `VITE_API_KEY` incrustado en el bundle (mitigar con acceso
  restringido; resolver en P10). Pricing/limits pueden cambiar → verificar.

## Decisión recomendada
**Principal:** Render (backend Docker + Render Postgres) + Vercel (frontend) — mejor
balance simplicidad / costo (low) / rollback (1-click) / operación (low) para XMIP, que
ya trae Dockerfile.
**Alternativa DB:** Neon (branching para resetear staging sin borrar la base).
**Alternativa de control:** VPS + Docker Compose si se prioriza costo fijo y control total.
