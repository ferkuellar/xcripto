# Operational Audit Coverage Report

| Campo | Valor |
| --- | --- |
| Fase | P8.1 — Operational Audit Coverage Hardening |
| Fecha | 2026-07-04 |
| Base | main `9e7d29f` (post-P8) |
| Entorno de validación | Local production-like (Docker + PostgreSQL 16 + auth) |

## 1. Contexto
El pilot P8 confirmó que los gates editoriales son fail-closed, pero detectó un gap de
**trazabilidad**: no todas las acciones críticas quedaban en `OperationalAuditLog`.

## 2. Gap detectado en P8
`OperationalAuditLog` cubría audit checks (`audit_event`), readiness (`readiness_event`)
e intake (`intake_event`), **pero no** las transiciones de estado de `NewsItem` ni el
registro de `SourceReference`. No se podía responder de forma auditable "quién cambió una
noticia de estado, de qué estado a qué estado, y si un gate la bloqueó".

## 3. Eventos agregados
| Evento | event_type | action | decision | outcome |
| --- | --- | --- | --- | --- |
| Transición exitosa de NewsItem | `news_event` | `news.status.transition` | `updated` | `succeeded` |
| Transición bloqueada por gate | `news_event` | `news.status.transition` | `blocked` | `blocked` |
| Transición inválida (state machine) | `news_event` | `news.status.transition` | `deny` | `failed` |
| Registro de SourceReference | `source_event` | `source.register` | `created` | `succeeded` |

Valores dentro de la taxonomía canónica existente (`OPERATIONAL_AUDIT_EVENT_TYPES` /
`_OUTCOMES` / `_DECISIONS`); **sin romper compatibilidad**. La evaluación de calidad de
fuente se registra como metadata del evento de registro (es determinística a partir de la
fuente registrada; no hay un paso de evaluación separado que inventar).

## 4. NewsItem status transitions
Integradas en el endpoint `PATCH /api/v1/news/{id}/status` (`app/api/v1/endpoints/news.py`).
Se captura el estado previo (como string inmutable, antes de la transición), se intenta la
transición y:
- **éxito** → evento `succeeded/updated` con `before_state`/`after_state` (`{status}`) y
  metadata `previous_status`/`new_status`.
- **bloqueo por gate editorial** (`ConflictError`, 409) → evento `blocked/blocked` con
  `blocked_by_gate=true`, `attempted_status` y `reason` del gate; **luego re-lanza** (el
  gate sigue fallando cerrado — la semántica no cambia).
- **transición inválida** (`DomainValidationError`, 400) → evento `failed/deny`.

No se alteró qué transiciones son válidas ni ningún gate; solo se auditan.

## 5. SourceReference registration
Integrada en `POST /api/v1/sources` (`app/api/v1/endpoints/sources.py`). Cada registro
emite `source_event/source.register` con la evaluación de calidad.

## 6. Metadata capturada
- NewsItem: `previous_status`, `new_status`/`attempted_status`, `blocked_by_gate`, `reason`,
  `news_item_id`, `entity_type=NewsItem`, `actor_role`, `actor_id`, `correlation_id`,
  `request_method`/`request_path`.
- SourceReference: `source_reference_id`, `source_name`, `source_url` (redactado),
  `trust_level`, `source_status`, `quality_level` (S1–S5), `disqualified`,
  `allowed_for_fact_publication`, `requires_strong_verification`, `actor_role`,
  `correlation_id`.

## 7. Secret redaction
`operational_audit_service.redact_url()` elimina query string y fragmento de las URLs
antes de auditarlas (las URLs de fuente no son secretos, pero un query param podría cargar
un token). Ninguna API key ni header de auth entra al payload de audit. Test dedicado
verifica que `?token=...` se elimina y que `dev-secret` no aparece en el registro.

## 8. Tests agregados
`backend/tests/test_operational_audit_coverage.py` (7 tests): transición exitosa auditada,
transición bloqueada por gate auditada (blocked + reason + blocked_by_gate), transición
inválida auditada como failed/deny, registro de fuente auditado con calidad, fuente
`blocked` auditada como descalificada, propagación de `correlation_id` + `actor_role`,
redacción de URL + ausencia de API key. **Suite total: 529 pytest verdes** (522 + 7).

## 9. Pilot validation
`controlled_newsroom_pilot.py` ampliado con C14/C15. Corrida contra el stack local:
**15/15 PASS**. `admin/audit/summary` tras el pilot:
`events_by_type = {audit_event: 8, readiness_event: 4, source_event: 9, news_event: 64}`,
`events_by_outcome = {succeeded: 81, blocked: 4}`. Los 4 `blocked` corresponden a las
transiciones a `approved` detenidas por el gate de calidad de fuente (C4, C5, C7, C8).

## 10. Riesgos restantes
- Las fuentes creadas automáticamente durante `intake.promote` se cubren hoy por el
  `intake_event` de la promoción; el evento `source.register` cubre el registro explícito
  vía `POST /sources`. Ampliar a la creación implícita queda como follow-up menor.
- El logging sigue el patrón existente (no fail-closed sobre el audit log): si el registro
  del evento fallara, la operación principal ya está commiteada. Consistente con el resto.

## 11. GO / NO-GO
**GO.** El gap de P8 queda cerrado: transiciones de estado (incl. bloqueos por gate) y
registro de fuentes son ahora auditables, con actor/correlation propagados y sin secretos.
