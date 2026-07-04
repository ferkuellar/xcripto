# Controlled Newsroom Trial Report

## 1. Fecha
2026-07-04

## 2. Entorno
Local production-like: `docker compose` (backend FastAPI + **PostgreSQL 16**), auth
activada (`AUTH_ENABLED=true`, `X-API-Key`), API en `http://127.0.0.1:8010`. Equivalente
funcional a staging (mismo binario/esquema que iría al VPS). No hay staging cloud
desplegado por decisión del proyecto (VPS más adelante).

## 3. Commit/tag usado
main `6c95b4c` (RC `v0.1.0-rc1`).

## 4. Dataset piloto
13 casos sintéticos definidos en `CONTROLLED_NEWSROOM_TRIAL_PLAN.md`, ejecutados por
`backend/scripts/controlled_newsroom_pilot.py`. Datos neutrales (`[PILOT <run>]`,
`pilot.example`); nada publicado.

## 5. Casos ejecutados
13 casos: 8 de gate de publicación (S1–S5 + blocked/restricted) + 4 de readiness/riesgo
+ 1 de deduplicación.

## 6. Resultados por caso — **13/13 PASS**
| # | Caso | Esperado | Resultado |
| --- | --- | --- | --- |
| C1 | S1 primaria + audit | avanza (200) | ✅ 200 advanced |
| C2 | S2 medio + audit | avanza (200) | ✅ 200 advanced |
| C3 | S3 + verificación fuerte | avanza (200) | ✅ 200 advanced |
| C4 | S3 sin verificación | BLOQUEADO (409) | ✅ 409 blocked |
| C5 | S4 sin verificación | BLOQUEADO (409) | ✅ 409 blocked |
| C6 | S4 + verificación fuerte | avanza (200) | ✅ 200 advanced |
| C7 | fuente blocked | BLOQUEADO (409) | ✅ 409 blocked |
| C8 | fuente restricted | BLOQUEADO (409) | ✅ 409 blocked |
| C9 | readiness fuente débil S4 | source_score ≤ 3 | ✅ source_score=3.0 |
| C10 | contradicción entre fuentes | human review + warning | ✅ human_review=True + conflict |
| C11 | falta de evidencia | missing + score<40 | ✅ missing=True, score=5.0 |
| C12 | riesgo crítico | readiness blocked | ✅ blocked + block_recommended |
| C13 | señal duplicada | duplicate | ✅ exact_duplicate |

## 7. Editorial gates
Fail-closed confirmado: los 4 casos que debían bloquearse (C4, C5, C7, C8) devolvieron
`409` en el intento de `approved`, **con AuditCheck aprobatorio presente** — es decir, el
gate de calidad de fuente bloquea de forma independiente al gate de audit. Ningún caso
bloqueado avanzó (0 violaciones de fail-closed).

## 8. Source quality enforcement
- S1/S2 sostienen publicación directamente (C1, C2).
- S3/S4 requieren verificación independiente fuerte: sin ella → bloqueo (C4, C5); con
  ella → avanzan (C3, C6).
- Fuente `blocked`/`restricted` descalifica sin importar el nivel (C7, C8).

## 9. Readiness scoring
Refleja la calidad de fuente y el riesgo: S4 puntúa 3/10 en el componente source (C9);
contradicciones elevan a revisión humana (C10); ausencia de verificación deja
`VerificationRecord` como faltante y score bajo (C11); riesgo crítico marca readiness
`blocked` + `publication_block_recommended` (C12).

## 10. Admin dashboard
`/api/v1/admin/dashboard/overview` reflejó la actividad del pilot:
`total_news=13`, `blocked_readiness_count=1` (C12), `latest_readiness_count=4`,
`duplicate_intake_signals=1` (C13). `admin_contract_smoke` → **passed** (11 endpoints
admin en 200). La validación visual del SPA (`/#/admin`) fue confirmada por el operador
en la sesión de arranque local.

## 11. Operational audit
`/api/v1/admin/audit/summary`: `total_events=13`, `events_by_type`
{audit_event: 8, readiness_event: 4, intake_event: 1}, `events_by_outcome`
{succeeded: 13}, `events_by_decision` {created: 8, calculated: 4, promoted: 1}. Los
eventos incluyen `actor_role` y `correlation_id`; **sin secretos** en la salida.

## 12. Bugs encontrados
Ninguno funcional. **Hallazgo (gap, no bug):** el `OperationalAuditLog` registra la
creación de audit checks, los cálculos de readiness y la promoción de intake, pero **no**
las transiciones de estado de `NewsItem` ni el registro de `SourceReference`. La
trazabilidad de las decisiones de gate de publicación se apoya hoy en el
`EditorialReadinessScore` persistido y en los `ConflictError`, no en el audit log.

## 13. Bugs corregidos
N/A (no se encontraron bugs). Solo se ajustó el estilo del script nuevo (líneas ≤100).

## 14. Riesgos restantes
- Cobertura parcial del operational audit (§12) — recomendado ampliar antes de producción
  para registrar transiciones de estado y cambios de fuente.
- Entorno de pilot es local (no cloud); el comportamiento con latencia/red del VPS se
  validará al desplegar.
- Auth por API key (sin login de usuarios) — P10.

## 15. GO / NO-GO
**GO** para el pilot editorial: las salvaguardas fail-closed, la calidad de fuente, el
readiness y la deduplicación se comportaron exactamente como se espera (13/13). Ver
`PILOT_GO_NO_GO_CHECKLIST.md`.

## 16. Recomendación
Avanzar hacia producción **tras**: (1) ampliar la cobertura del OperationalAuditLog,
(2) desplegar en el VPS y repetir el pilot remoto, (3) implementar auth de usuarios (P10).
El núcleo editorial ya es sólido y auditable.
