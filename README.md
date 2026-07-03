# Project ORION / XCripto / XMIP

**Estado del proyecto:**

```text
Not ready for production.
Candidate for internal alpha after repo hygiene fixes.
```

---

## 1. Qué es este proyecto

Este repositorio contiene tres capas de un mismo sistema:

```text
ORION   = Gobierno, arquitectura, doctrina y documentación del sistema.
XCripto = Agencia / medio de noticias, análisis y contenido cripto.
XMIP    = XCripto Media Intelligence Platform: plataforma interna
          multiagente que opera el newsroom de XCripto.
```

Definición operativa:

> XCripto será una agencia de noticias, análisis y contenido cripto operada por XMIP, una plataforma multiagente de inteligencia editorial gobernada por ORION.

Regla arquitectónica central:

```text
El agente pertenece a ORION.
El prompt pertenece al runtime.
La ejecución pertenece a XMIP.
```

---

## 2. Estructura del repositorio

```text
.
├── backend/      API de XMIP (FastAPI + SQLAlchemy async + Alembic)
├── frontend/     UI del Newsroom OS (React + Vite) — actualmente con mock data
├── docs/         Documentación ORION (fundación → operaciones → prompts)
├── apps/         Vacía — candidate for archive/delete pending reference cleanup
├── newsroom/     Vacía — candidate for archive/delete pending reference cleanup
└── README.md
```

---

## 3. Cómo navegar `docs/`

El índice maestro es `docs/INDEX.md`. Los volúmenes:

| Volumen              | Contenido                                                  |
| -------------------- | ----------------------------------------------------------- |
| `000-fundacion`    | Identidad, doctrina, glosario y charter del proyecto        |
| `001-estrategia`   | Propósito, manifiesto, principios y modelo de negocio      |
| `002-editorial`    | Constitución, estándares, flujo y guía de estilo          |
| `003-arquitectura` | Arquitectura empresarial, sistema, datos y conocimiento     |
| `004-agentes`      | Arquitectura y especificación de agentes digitales         |
| `005-producto`     | Visión de producto, MVP y roadmap de XMIP                  |
| `006-operaciones`  | Operación diaria del newsroom y flujos editoriales         |
| `007-prompts`      | Capa de prompts runtime (000-shared, claude, gpt, hermes)   |

Nota: `docs/INDEX.md` aún referencia `008-decisiones/` y `009-sprints/`, que no existen en el working tree actual — candidate for archive/delete pending reference cleanup.

---

## 4. Qué es `backend/`

API de XMIP construida con FastAPI, SQLAlchemy async, Pydantic v2 y Alembic. Cubre intake de noticias, fuentes, ejecuciones de agentes, outputs de agentes, audit checks, verificación, riesgo, piezas editoriales, distribución, publicación, workflows, métricas, memoria y conocimiento, con trazabilidad por `X-Correlation-ID`.

Documentación, comandos y endpoints: `backend/README.md`.

> ⚠️ **Coordinación de trabajo:** el backend está en desarrollo activo por Codex
> (ramas `feat/*`). No modificar `backend/` ni sus tests, migraciones o
> configuración sin coordinar primero. Los demás runtimes trabajan en `docs/`
> y capas no-backend.

---

## 5. Qué es `frontend/`

Frontend del Newsroom OS (React 19 + TypeScript + Vite + Tailwind). En su versión actual **toda la data es mock de demostración**: no hay integración con el backend, autenticación ni llamadas externas. La integración con la API de XMIP es una fase futura.

Detalles: `frontend/README.md`.

---

## 6. Qué es `docs/007-prompts/`

La capa de prompts runtime de XMIP:

```text
docs/007-prompts/
├── 000-shared/   contratos y guardrails compartidos entre runtimes
├── claude/       runtime cognitivo y editorial (Claude)
├── gpt/          runtime cognitivo general (GPT)
└── hermes/       runtime operador local (Hermes)
```

Los agentes se definen una sola vez en `docs/004-agentes/`; cada carpeta de runtime solo los adapta. Índice detallado: `docs/007-prompts/INDEX.md` y `docs/007-prompts/README.md`.

---

## 7. Estado actual

```text
Documentación ORION (000–006):  completa en primera versión
Capa de prompts (007):          completa: shared 3, gpt 16, claude 16, hermes 18
Backend XMIP:                   en desarrollo activo (Codex, ramas feat/*)
Frontend:                       demo con mock data, sin integración
Producción:                     NO — ver próximos pasos
```

---

## 8. Próximos pasos hacia internal alpha

1. **Repo hygiene (crítico):** quitar del `.gitignore` las exclusiones de `docs/007-prompts/000-shared/`, `claude/` y `hermes/` y versionar esas carpetas — requiere coordinación con el trabajo activo en backend.
2. **Backup (crítico):** configurar git remote privado y hacer push de `main` y ramas.
3. Commitear el renombre `Prompt-*` → `GPT-*` y resolver el destino de `docs/008-decisiones/` y `docs/009-sprints/` (restaurar o retirar referencias).
4. Estabilizar el backend (Codex) y agregar CI mínima (pytest + ruff).
5. Integrar frontend con la API de XMIP.
6. Revisión cruzada de consistencia de prompts entre runtimes (GPT/AuditAgent).

---

## 9. Reglas editoriales innegociables

```text
Nada se publica sin fuente.
Nada sensible se publica sin verificación.
Nada crítico se publica sin aprobación.
Nada publicado queda sin registro.
La memoria no es fuente factual.
Un agente no publica directamente.
Un output de agente no es fuente.
```
