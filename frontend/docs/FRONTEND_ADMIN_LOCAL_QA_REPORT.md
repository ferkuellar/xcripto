# Frontend Admin Local QA Report

## 1. Fecha
2026-07-04 (Hard Phase P2 — Frontend Admin Local QA).

## 2. Rama
`qa/frontend-admin-local` (desde `main` = `1d4628b`, con branch protection + CI verde).

## 3. Backend base URL
`http://127.0.0.1:8010` (production-like con auth + RBAC). El puerto 8000 estaba
ocupado por un proceso local del operador, así que se usó 8010 y se apuntó
`VITE_API_BASE_URL` a ese puerto. El default documentado sigue siendo 8000.

## 4. Variables usadas (frontend/.env.local, gitignored)
```env
VITE_API_BASE_URL=http://127.0.0.1:8010
VITE_API_KEY=dev-secret
VITE_ACTOR_ROLE=admin
VITE_ACTOR_ID=local-admin
```
`dev-secret` es solo local. El cliente admin (`src/lib/xmipAdminApi.ts`) lee estas
variables Vite, envía `X-API-Key`, `X-Actor-Role`, `X-Actor-Id` y un
`X-Correlation-ID` por request. No hardcodea la key, no la imprime, no usa
localStorage.

## 5. Secciones validadas (ruta `#/admin`)
Todas renderizadas contra el backend real con datos sembrados:
- `/ready` banner (Backend ready, checks configuration/database ok)
- Config banner (auth habilitado, RBAC activo, 29 rutas admin)
- Overview stat cards (noticias, intake, tareas bloqueadas, readiness,
  publicaciones, agentes, conectores, audit events)
- Newsroom health (degraded 70, blocked_readiness_scores: 1)
- Operational gaps (news_without_verification, _risk_review, _content, etc.)
- Ownership board (usuarios / news sin owner / tasks sin owner)
- Intake queue (señal con dedupe `unique`)
- Editorial work queue (noticia `blocked` + missing requirements chips)
- Blockers ("AgentOutput has critical unaccepted risk flags", severity high)
- Readiness board (score 67, `blocked`)
- Task board (5 tareas: completed / completed_with_warnings)
- Publication board (empty state "Sin elementos operativos")
- Agent runner / Connectors / Operational audit summaries

Cada sección tiene loading skeleton, success, empty state y error state
independientes. El fallo de una sección no tumba la pantalla.

## 6. Errores 401/403/503 validados (en navegador)
| Escenario | Config | Resultado UI |
| --- | --- | --- |
| 401 Missing key | `VITE_API_KEY=` | "API key requerida" + "Missing API key" + corr id + retry, por sección |
| 403 Invalid role | `VITE_ACTOR_ROLE=guest` | "Rol sin permiso" + "Invalid actor role"; `/ready` sigue verde (público) |
| Backend offline | backend apagado | "Backend no disponible" en todas las secciones + Topbar "XMIP sin conexión"; sin loading infinito |
| 503 not ready | — | code-verified (AdminErrorState mapea 503 → "Backend no listo"); no simulado en navegador (requiere romper la DB en caliente) |

Ninguno imprime stacktrace ni la API key. Hallazgo de contrato: **una API key
incorrecta devuelve 403** (no 401); el backend usa 401 solo para key ausente y
403 para key inválida / rol inválido / permiso insuficiente. La UI mapea ambos
de forma clara.

## 7. Bugs encontrados
1. `AdminDashboardPage.toneForStatus` no reconocía valores canónicos
   (`ready_to_advance`, `completed_with_warnings`, `passed`, `allow_to_continue`,
   etc.) → caían a badge neutral. **Visible**: `completed_with_warnings` salía gris
   en lugar de amarillo.
2. `api-types.ts` `AuditCheckRead.audit_status` tipado con el catálogo legacy
   `'pass' | 'fail' | 'warning' | 'pending'` (el backend ya rechaza `pass`/`fail`
   con 422 y produce `passed`/`failed`/...).
3. `NewsDetailPage` y `AuditPage` mapeaban badges de audit con `pass`/`fail`
   legacy → un audit real `passed` caía a azul/neutral en vez de verde.
4. **`CommandCenter` contaba bloqueos de audit con `audit_status === 'fail'`** —
   valor que nunca coincide con el real `failed`, así que el KPI
   "Audit · bloqueos activos" subcontaba silenciosamente los audits bloqueantes
   (riesgo editorial: ocultaba bloqueos). Detectado al endurecer el tipo.

## 8. Bugs corregidos
Todos los anteriores:
- `toneForStatus` ampliado a los catálogos canónicos (readiness/audit/task/risk/
  dedupe/severity), agrupado por semántica (sano→green, bloqueo→red,
  advertencia→yellow, severidad alta→orange, en proceso→cyan).
- `AuditCheckRead.audit_status` y `decision_recommendation` retipados al catálogo
  canónico del backend.
- `auditStatusVariant` en `NewsDetailPage` y `auditStatusMap` en `AuditPage`
  actualizados a `passed/passed_with_warnings/failed/blocked/warning/pending`.
- `CommandCenter.blockingAudits` corregido a `failed`/`blocked`.

## 9. Bugs pendientes
- Ninguno bloqueante. Nota UX menor: una API key incorrecta muestra la etiqueta
  "Rol sin permiso" (por el 403), aunque el detalle real "Invalid API key" sí se
  muestra. Se deja como está: el mensaje del backend es visible y correcto.
- El componente demo `AuditPanel` (+ `data/types.ts`, `mock-operations.ts`) usa
  un catálogo `pass/fail/warning` propio del sistema DEMO (aislado, badge DEMO);
  no consume backend, se deja intacto.

## 10. Calidad editorial en UI
La UI **no oculta blockers**: el blocker "AgentOutput has critical unaccepted
risk flags" se muestra en rojo con severidad alta; la noticia con
`readiness_status=blocked` aparece con badge rojo y su score; el work queue
lista los `missing_requirements`. Una noticia bloqueada NO se presenta como lista
para publicar. Los estados `completed_with_warnings` ahora se distinguen en
amarillo (no verde), evitando falso "todo OK".

## 11. Resultado backend validation
- `pytest`: 499 passed
- `ruff check .`: All checks passed
- `python -c "from app.main import app"`: XMIP Backend
- Alembic upgrade / downgrade -1 / upgrade: OK
Backend sin cambios en P2 (solo frontend).

## 12. Resultado frontend build/lint/test
- `npm run build` (tsc -b + vite): OK
- `npm run lint` (oxlint): 0 errores
- No hay script de test en `package.json` (dev/build/lint/preview). Se documenta
  como pendiente: no se introdujo framework de test pesado en esta fase.

## 13. Resultado smoke/admin/local_newsroom_qa
Contra backend fresco (DB migrada por Alembic, puerto 8011):
- `smoke_test.py`: passed
- `admin_contract_smoke.py`: passed (16 endpoints admin en 200)
- `local_newsroom_qa.py`: PASS
Nota: en corridas repetidas sobre la MISMA DB, `local_newsroom_qa` puede fallar
en promote porque la señal repetida se marca `exact_duplicate` y el sistema
(correctamente) rehúsa promover un duplicado. Es el motor de deduplicación
funcionando, no un bug.

## 14. GO / NO-GO frontend local
**GO** para el admin frontend local. Dashboard consume el backend real, maneja
401/403/offline con claridad, no oculta blockers, badges usan el catálogo
canónico, build y lint limpios.

## 15. Siguiente paso recomendado
1. Merge del PR a `main` cuando CI pase.
2. Agregar setup de tests de frontend (Vitest + Testing Library) para el api
   client (headers, 401/403/503) y los badges canónicos — pendiente declarado.
3. Considerar afinar la etiqueta de error para distinguir "API key inválida"
   (403 con mensaje "Invalid API key") de "rol sin permiso".
