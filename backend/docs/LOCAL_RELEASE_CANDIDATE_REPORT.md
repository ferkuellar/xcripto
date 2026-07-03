# XMIP — Local Release Candidate Report (Hard Phase P0 + P1)

| Campo | Valor |
| --- | --- |
| Fecha | 2026-07-03 (P0) · actualizado 2026-07-03 (P1) |
| Rama | `fix/local-production-readiness-p1` (sobre `hard/local-production-readiness`) |
| Commit base | `052000f` (feat: connect admin frontend to backend api) |
| Commits P0 | `8b81250` (news filters), `fca28aa` (frontend feed), `f7c76b9` (QA docs) |
| Commits P1 | `7635d09` (fix readiness stale snapshot), `7542c53` (fix audit catalog) |
| Autor del ciclo QA | Claude (sesión local), datos QA etiquetados `[QA]` |

## Actualización P1 (2026-07-03)

- **Bug #1 CORREGIDO** (`7635d09`): `calculate_editorial_readiness` recalcula el
  WorkflowRun asociado antes de puntuar; ya no reporta requisitos stale.
  `explain`/`latest`/`list` intactos (read-only). 3 tests de regresión.
- **Bug #2 CORREGIDO** (`7542c53`): catálogo único de AuditCheck alineado con los
  gates: `AUDIT_STATUSES = {passed, passed_with_warnings, failed, warning,
  pending, blocked}`; `decision_recommendation` validado contra
  `AUDIT_DECISION_RECOMMENDATIONS = {allow_to_continue, allow_with_warnings,
  needs_revision, block_publication}` (nullable). `pass`/`fail` y texto libre se
  rechazan con 422 y mensaje que apunta al valor canónico. Gates sin cambios,
  siguen fallando cerrado. 6 tests de regresión + test de consistencia
  catálogo⊇gates.
- **QA post-fix:** pytest **499 passed** · ruff limpio · ciclo Alembic OK ·
  OpenAPI regenerado · smoke/admin/newsroom_qa **PASS** en server
  production-like :8010 · verificación en vivo: calculate sin recalculate
  manual ya no muestra VerificationRecord stale (fix #1) y `pass` devuelve 422
  mientras `passed/allow_to_continue` se acepta (fix #2) · docker config/build OK.
- **Remote git:** `BLOCKED: remote URL required.` Sin URL provista no se
  configuró remote ni push — sigue siendo el pendiente crítico #1.
- **Nota de datos:** filas existentes en DBs dev con `audit_status="pass"`
  permanecen (sin migración destructiva); el gate ya las trataba como
  no-aprobatorias y las nuevas escrituras quedan bloqueadas.
- **Follow-up frontend:** `frontend/src/lib/api-types.ts` y los mapas de badges
  de Audit aún tipan `pass/fail`; actualizar a los valores canónicos en la
  próxima fase de frontend (visual: valores nuevos caen a badge neutral).
- **GO/NO-GO actualizado: GO (condicionado solo por remote/push).** Las dos
  condiciones de bugs de P0 quedaron cerradas; `compose up` sigue pendiente de
  puerto libre.

---

## 1. Estado git

Working tree estabilizado al inicio de la fase: los cambios pendientes de news
(backend + frontend) se clasificaron como válidos y se integraron en dos
commits limpios. Quedan **fuera de commit por decisión humana pendiente**:
borrados de `docs/008-decisiones/` y `docs/009-sprints/`, y `.claude/` (config
local del harness, no versionable). El repo **no tiene remote** — el push a un
repositorio privado sigue siendo el pendiente crítico número 1.

## 2. Resultados de validación

| Validación | Resultado |
| --- | --- |
| `pytest` | ✅ **490 passed** (2:48) |
| `ruff check .` | ✅ All checks passed |
| `python -c "from app.main import app"` | ✅ `XMIP Backend` |
| `alembic upgrade head` (DB nueva) | ✅ 11 migraciones aplican desde cero |
| `alembic downgrade -1` → `upgrade head` | ✅ ciclo limpio, `current = 20260702_0011 (head)` |
| `docker compose config` | ✅ válido |
| `docker compose build` | ✅ imagen `backend-api` construida |
| `docker compose up` | ⚠️ OMITIDO — puerto 8000 ocupado por proceso local del operador (no se detuvo por instrucción del operador). Mitigación: server production-like validado en :8010 fuera de Docker |
| `smoke_test.py` (:8010, auth on) | ✅ health/live/ready/openapi OK |
| `admin_contract_smoke.py` (admin, RBAC) | ✅ 16 endpoints admin en 200 |
| `local_newsroom_qa.py` (nuevo) | ✅ PASS — flujo intake→dedupe→promote→admin boards |
| `export_openapi.py` | ✅ `docs/openapi.json` regenerado |

Configuración production-like usada (nuevo `backend/.env.local.production.example`):
`ENVIRONMENT=production`, `AUTH_ENABLED=true` (API key local `dev-secret`, solo
pruebas), `AUTO_CREATE_TABLES=false` (tablas vía Alembic), audit log y
healthcheck de DB activados.

## 3. Flujo editorial E2E (manual, servidor :8010)

Cadena completa ejecutada y verificada sobre una noticia QA:

```text
IntakeSignal manual (S1, IC2)            ✅ 201, dedupe unique, hash/dedupe_key
Dedupe recalculado                       ✅ unique
Promote → NewsItem + WorkflowRun         ✅ editorial_pipeline creado
Bootstrap → 5 WorkflowTasks              ✅
Agent Runner interno run-next ×5         ✅ SourceValidator/Risk/Editorial/Audit/Distribution
  → 5 AgentExecutions + 5 AgentOutputs   ✅
VerificationRecord (verified E2/C2)      ✅
RiskReview (low / allow)                 ✅ (catálogo controlado validó valores)
AuditCheck canónico (passed/allow_to_continue) ✅
ContentPiece editorial_brief → approved  ✅ (gate bloqueó PublicationRecord sin aprobación)
DistributionPlan internal → scheduled    ✅ (gate bloqueó sin plan scheduled)
PublicationRecord simulado (internal)    ✅ nada real publicado
Aceptación humana de 5 AgentOutputs      ✅ (accepted_by requerido)
Workflow recalculate                     ✅ running, sin missing
Readiness final                          ✅ score 93 · ready · ready_to_advance · 0 bloqueos
OperationalAuditLog                      ✅ 19 eventos (promote, runner ×5, accepts ×5, readiness ×5, audits, publication)
Admin dashboard                          ✅ overview/work-queue/readiness/audit reflejan el flujo
```

Progresión del readiness observada: 52 (blocked) → 88 (blocked por flags sin
aceptar) → **93 (ready)** tras aceptación humana. Los gates fallan cerrado.

## 4. Bugs encontrados

| # | Severidad | Hallazgo | Estado |
| --- | --- | --- | --- |
| 1 | P2 | El readiness `calculate` usa el snapshot `missing_requirements` del WorkflowRun sin refrescarlo: reporta requisitos ya cumplidos hasta que se llama `POST /workflows/{id}/recalculate`. Confuso para el operador. | Documentado; fix sugerido: `calculate` debería recalcular el workflow primero (o excluir el snapshot del agregado) |
| 2 | P2 | Doble catálogo de audit: el schema acepta `pass/warning`… pero el gate (`is_passing_audit_check`) solo pasa `passed/passed_with_warnings` + `decision_recommendation ∈ {allow_to_continue, allow_with_warnings}` (campo que el schema NO valida contra catálogo). Un check `pass` "válido" nunca satisface el gate, sin aviso. Falla cerrado (seguro), pero es una trampa silenciosa. | Documentado; fix sugerido: unificar catálogos y validar `decision_recommendation` de AuditCheck |
| 3 | P3 | El watcher de `uvicorn --reload` no detecta cambios sobre carpetas OneDrive (observado repetidamente); un dev server puede servir código viejo sin saberlo. | Documentado; mitigación: reiniciar manualmente o desarrollar fuera de OneDrive |
| 4 | P3 | `docker-compose.yml` publica 8000 fijo; colisiona con dev servers locales. | Documentado; sugerencia: `${API_PORT:-8000}:8000` |

**Bugs P0/P1: ninguno encontrado.** Los "errores" 4xx durante el E2E fueron
validaciones correctas de catálogos y gates editoriales haciendo su trabajo.

## 5. Bugs corregidos en esta fase

Ninguno requerido — no se encontraron fallos P0/P1. Los dos commits de
estabilización integran trabajo previo validado (filtros de news + feed).

## 6. Riesgos técnicos

1. **Sin remote git** — todo el proyecto vive en un solo disco (crítico).
2. Snapshot de workflow desincronizable (bug #1) puede confundir operación.
3. SQLite local para pruebas; el comportamiento bajo PostgreSQL se cubrió solo
   vía migraciones/compose build (compose up quedó pendiente de puerto).
4. `.env` con `dev-secret`: aceptable local, jamás en despliegue.

## 7. Riesgos editoriales

1. La trampa del catálogo de audit (bug #2) podría hacer creer a un operador
   que una noticia tiene auditoría aprobatoria cuando el gate la ignora —
   falla cerrado, pero genera fricción y desconfianza en el tablero.
2. El sistema aún permite crear NewsItems por intake directo sin señal, con
   `source_url` no verificada — la política S1–S5 es documental; su
   enforcement automático (bloquear S4/S5 como fuente única) es fase futura.
3. MetricSnapshot/MemoryItem/KnowledgeNode quedan como faltantes esperados
   pre-publicación; correcto, pero el tablero debe comunicarlo como "post-pub".

## 8. Go / No-Go local

**GO (condicionado) para operación interna local.** El backend levanta en modo
production-like con auth y RBAC, migraciones y Docker build funcionan, los
gates editoriales bloquean lo que deben bloquear, la trazabilidad de auditoría
registra la cadena completa, y el flujo editorial E2E termina en
`ready_to_advance` solo tras verificación + riesgo + auditoría + aceptación
humana. Condiciones antes de cualquier siguiente fase: (a) configurar remote y
push, (b) decidir bugs #1 y #2, (c) validar `docker compose up` completo con
PostgreSQL en un puerto libre.

## 9. Siguiente paso recomendado

1. `git remote add` + push de `hard/local-production-readiness` y `main`.
2. Fix quirúrgico del bug #1 (una llamada a recalculate dentro de
   `calculate`) con test de regresión.
3. Unificación del catálogo de audit (bug #2) con migración de datos si aplica.
4. `docker compose up` end-to-end con PostgreSQL (puerto parametrizado).
5. Enforcement automático de SOURCE_QUALITY_POLICY en intake/promote.
