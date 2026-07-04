# Controlled Newsroom Trial Plan

| Campo | Valor |
| --- | --- |
| Proyecto | ORION / XCripto / XMIP |
| Tipo | Plan de pilot editorial controlado |
| Entorno | Local production-like (Docker + PostgreSQL 16 + auth) — equivalente a staging |
| Base | `v0.1.0-rc1` / main `6c95b4c` |
| Fecha | 2026-07-04 |

> **Nota de entorno:** el proyecto se opera **localmente** (no hay staging cloud
> desplegado; se eligió VPS para más adelante). El pilot corre contra el stack
> `docker compose` con PostgreSQL 16 y auth activada — mismo binario y esquema que
> iría al VPS. No se publica nada; todos los datos son sintéticos y neutrales.

## 1. Objetivo
Simular operación de newsroom con un lote controlado de casos que ejercen la matriz de
calidad de fuente **S1–S5**, los gates editoriales fail-closed, el readiness scoring, la
deduplicación y la trazabilidad, verificando el **resultado esperado** de cada caso.

## 2. Regla de oro (fail-closed)
Un caso que **debe** bloquearse (S3/S4 sin verificación fuerte, S5, fuente
blocked/restricted, riesgo crítico) **nunca** debe poder avanzar a `approved`. Si eso
ocurre, el pilot FALLA (marca `CRIT`).

## 3. Mapeo S1–S5 (doc SOURCE_QUALITY_POLICY §4)
`trust_level`: T0=S1 (primaria oficial), T1=S2 (medio reconocido), T2=S3 (analista
identificado), T3=S4 (social sin confirmar); `source_status` blocked/restricted
descalifica; nivel desconocido → S5 (fail-closed).

## 4. Dataset piloto (13 casos sintéticos)

**Gate de publicación** (crear noticia + fuente registrada → llevar a `reviewing` con
AuditCheck aprobatorio → intentar `approved`):

| # | Caso | Fuente | Verificación | Esperado |
| --- | --- | --- | --- | --- |
| C1 | Primaria oficial | S1 (T0) active | — | avanza (200) |
| C2 | Medio reconocido | S2 (T1) active | — | avanza (200) |
| C3 | Analista + confirmación | S3 (T2) active | fuerte | avanza (200) |
| C4 | Analista sin confirmar | S3 (T2) active | ninguna | **BLOQUEADO (409)** |
| C5 | Social sin confirmar | S4 (T3) active | ninguna | **BLOQUEADO (409)** |
| C6 | Social + verificación fuerte | S4 (T3) active | fuerte | avanza (200) |
| C7 | Fuente bloqueada | S1 (T0) **blocked** | fuerte | **BLOQUEADO (409)** |
| C8 | Fuente restringida | S2 (T1) **restricted** | fuerte | **BLOQUEADO (409)** |

**Readiness / trazabilidad**:

| # | Caso | Esperado |
| --- | --- | --- |
| C9 | Readiness de fuente débil S4 | `source_score ≤ 3` (refleja debilidad) |
| C10 | Contradicción entre fuentes | `human_review_required` + warning de conflicto |
| C11 | Falta de evidencia | `VerificationRecord` en missing + `score < 40` |
| C12 | Riesgo crítico | `readiness_status = blocked` + `publication_block_recommended` |
| C13 | Señal duplicada | `dedupe_status ∈ {exact_duplicate, probable_duplicate}` |

**Verificación fuerte** = `VerificationRecord` `verified`, sin contradicciones, con
evidencia E3+ **o** ≥2 `source_refs` (una fuente débil nunca es confirmación única).

## 5. Ejecución
```bash
cd backend
python scripts/controlled_newsroom_pilot.py \
  --base-url http://127.0.0.1:8010 --api-key dev-secret --actor-role admin
```
El script imprime PASS/FAIL/CRIT por caso y sale con código ≠ 0 si algún gate quedó
abierto. Resultados en `CONTROLLED_NEWSROOM_TRIAL_REPORT.md`.

## 6. Reglas de seguridad del pilot
Sin publicación real, sin redes, sin conectores/LLM reales, sin datos personales, sin
secretos en git. Títulos con prefijo `[PILOT <run>]` y URLs `pilot.example`.
