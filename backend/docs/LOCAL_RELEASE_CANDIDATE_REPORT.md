# XMIP — Local Release Candidate Report (Hard Phase P0)

| Campo | Valor |
| --- | --- |
| Fecha | 2026-07-03 |
| Rama | `hard/local-production-readiness` |
| Commit base | `052000f` (feat: connect admin frontend to backend api) |
| Commits de la fase | `8b81250` (news filters), `fca28aa` (frontend feed) + docs/scripts de este reporte |
| Autor del ciclo QA | Claude (sesión local), datos QA etiquetados `[QA]` |

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
