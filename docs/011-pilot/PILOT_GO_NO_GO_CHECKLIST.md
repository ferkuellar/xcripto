# Pilot GO/NO-GO Checklist

Entorno: local production-like (Docker + PostgreSQL 16 + auth). Base: main `6c95b4c`
(`v0.1.0-rc1`). Fecha: 2026-07-04. Evidencia: `CONTROLLED_NEWSROOM_TRIAL_REPORT.md`
(pilot 13/13 PASS).

## Editorial Safety
- [x] S3/S4 sin verificación fuerte **no** avanzan (C4, C5 → 409).
- [x] Fuente blocked/restricted bloquea (C7, C8 → 409).
- [x] Riesgo crítico bloquea readiness (C12).
- [x] Gate de fuente actúa **con** AuditCheck aprobatorio (independiente del gate de audit).
- [x] 0 violaciones fail-closed (ningún caso bloqueado avanzó).

## Source Quality
- [x] S1/S2 sostienen publicación directa (C1, C2).
- [x] S3/S4 con verificación independiente fuerte avanzan (C3, C6).
- [x] Nivel S1–S5 mapeado desde `trust_level`; desconocido → S5 (fail-closed).
- [x] Readiness refleja fuente débil (C9: source_score=3/10).
- [x] Contradicciones entre fuentes elevan a revisión humana (C10).

## Auditability
- [x] `OperationalAuditLog` registra audit checks, readiness e intake (13 eventos).
- [x] `actor_role` y `correlation_id` presentes; sin secretos en la salida.
- [ ] ⚠️ Transiciones de estado de `NewsItem` y registro de `SourceReference` **no** se
      registran aún en el audit log (gap documentado — ampliar antes de producción).

## Admin Visibility
- [x] `admin_contract_smoke` passed (11 endpoints admin en 200).
- [x] Overview refleja la actividad del pilot (blocked_readiness, duplicates, readiness).
- [x] SPA `/#/admin` carga sin crashes (confirmado por el operador).
- [x] API key no expuesta en la UI.

## Reliability
- [x] Backend 522 pytest + ruff verdes.
- [x] Frontend 19 vitest + build + lint verdes.
- [x] Alembic head `20260702_0011` contra PostgreSQL.
- [x] `/health` `/live` `/ready` verdes.

## Rollback
- [x] Procedimiento documentado (`docs/010-deployment/STAGING_ROLLBACK_PLAN.md`,
      `VPS_DEPLOYMENT_RUNBOOK.md` §7): redeploy versión anterior, restaurar backup DB.
- [x] Datos del pilot son sintéticos y descartables (`docker compose down -v`).

## Security
- [x] Auth por API key activa; RBAC por headers (admin).
- [x] Sin secretos en git; `.env` gitignored; sin datos personales.
- [ ] ⚠️ Sin login de usuarios (JWT/OAuth) — bloquea exposición pública (P10).
- [ ] ⚠️ `VITE_API_KEY` incrustado en el bundle — solo interno hasta P10.

## Production Readiness
- [x] Núcleo editorial fail-closed validado end-to-end.
- [ ] Desplegar en VPS y repetir pilot remoto.
- [ ] Ampliar cobertura de OperationalAuditLog.
- [ ] Implementar auth real (P10).

## Veredicto
**GO** para pilot editorial controlado. **NO-GO** para producción pública hasta cerrar
los ítems ⚠️ (auth real, cobertura de audit, deploy VPS validado).
