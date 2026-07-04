# XMIP Staging Rollback Plan

> Reglas: **no** hacer downgrade destructivo sin backup; **no** borrar la DB de staging
> salvo confirmación explícita; **preferir** redeploy de la versión anterior antes que
> tocar datos.

## 1. Cuándo hacer rollback
- `/ready` en rojo (DB o configuración) sostenido tras el deploy.
- Smoke/admin/newsroom QA fallando por regresión introducida en el release.
- Errores 5xx generalizados o migración fallida/parcial.
- CORS/health rotos que impiden el uso del admin.

## 2. Rollback backend
- **Preferido:** redeploy de la imagen/commit anterior desde el panel del proveedor
  (Render/Railway guardan deploys previos → "rollback to this deploy").
- Confirmar que la versión anterior es compatible con el esquema actual de la DB
  (ver §5 antes de revertir código si hubo migración).

## 3. Rollback frontend
- Redeploy instantáneo de la build anterior en Vercel/Netlify (historial de deploys).
- Sin estado propio; el rollback es inmediato y seguro.

## 4. Rollback database
- **No borrar la DB.** Si una migración corrompió datos: restaurar desde el backup más
  reciente (§6) a una instancia nueva y repuntar `DATABASE_URL`.
- Borrado/reset de la DB de staging **solo** con confirmación explícita del owner.

## 5. Alembic downgrade policy
- Solo `alembic downgrade -1` (un paso) y **solo con backup previo** (§6).
- Validar el downgrade equivalente en local/DB temporal antes de aplicarlo en staging.
- Si el downgrade es destructivo (drop de columnas/tablas con datos), preferir
  restaurar backup en lugar de degradar.
- Tras estabilizar, volver a `alembic upgrade head`.

## 6. Backup antes de migración
- Tomar snapshot/backup de la DB gestionada **antes** de cada `upgrade head` en staging.
- Render PG / Neon ofrecen backups automáticos + snapshots manuales; Neon además
  permite *branching* (rama de DB desechable para probar la migración).
- Registrar el id/label del backup en el canal de coordinación.

## 7. Recovery checklist
- [ ] Identificar el deploy/commit bueno conocido (last-known-good).
- [ ] Redeploy backend a esa versión.
- [ ] Redeploy frontend a esa build.
- [ ] Verificar compatibilidad de esquema; restaurar backup si la migración fue el problema.
- [ ] `/health` `/live` `/ready` verdes.
- [ ] Re-correr smoke/admin/newsroom QA.
- [ ] Revisar `OperationalAuditLog` y logs.
- [ ] Registrar causa raíz y follow-up.

## 8. Comunicación interna
- Avisar al owner (Fernando) al inicio y al cierre del rollback.
- Documentar: qué falló, versión revertida, backup usado, estado final, acciones
  pendientes. Staging es interno: sin comunicación pública.
