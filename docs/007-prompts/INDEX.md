# INDEX — Runtime Prompts XMIP

**Nivel documental:** L4 — Operaciones / Runtime Execution
**Volumen:** 007-prompts
**Proyecto:** Project ORION / XCripto / XMIP
**Versión:** 2.0
**Estado:** Draft Implementable
**Owner:** Fernando Cuellar
**Última actualización:** 2026-07-02
**Ruta:** `docs/007-prompts/INDEX.md`

---

## 1. Propósito

Este índice organiza el volumen **007-prompts**: la capa de prompts runtime de XMIP — XCripto Media Intelligence Platform.

El volumen centraliza los contratos compartidos y los adaptadores de ejecución que permiten operar los agentes ORION sobre los runtimes disponibles: GPT, Claude y Hermes.

Regla central del volumen:

```text
El agente pertenece a ORION.
El prompt pertenece al runtime.
La ejecución pertenece a XMIP.
```

---

## 2. Modelo de capas

```text
docs/004-agentes/            = definición oficial del agente (ORION)
docs/007-prompts/000-shared/ = contratos y guardrails compartidos
docs/007-prompts/<runtime>/  = adaptación del agente a un runtime
backend/ (XMIP)              = ejecución, persistencia, trazabilidad
```

Un adaptador nunca redefine al agente. Solo lo traduce a las reglas de ejecución de su runtime.

---

## 3. Estructura real del volumen

```text
docs/007-prompts/
├── INDEX.md
├── README.md
├── 000-shared/
│   ├── agent-base-contract.md
│   ├── agent-output-standards.md
│   └── editorial-guardrails.md
├── claude/
│   ├── README.md
│   ├── 00-claude-global-system.md
│   ├── Claude-Agent-Execution-Contract.md
│   └── Claude-<AgentName>.md   (13 adaptadores)
├── gpt/
│   ├── README.md
│   ├── 00-gpt-global-system.md
│   ├── GPT-Agent-Execution-Contract.md
│   └── GPT-<AgentName>.md      (13 adaptadores)
└── hermes/
    ├── README.md
    ├── 00-hermes-global-system.md
    ├── Hermes-Agent-Execution-Contract.md
    ├── Hermes-<AgentName>.md   (13 adaptadores)
    ├── Hermes-DocsMaintenanceAgent.md
    └── Hermes-RepositoryOperator.md
```

---

## 4. Estado por carpeta

| Carpeta        | Rol                                   | Docs | Estado    |
| -------------- | ------------------------------------- | ---: | --------- |
| `000-shared/` | Contratos compartidos                 |    3 | Completo  |
| `gpt/`        | Runtime cognitivo general             |   16 | Completo  |
| `claude/`     | Runtime cognitivo y editorial         |   16 | Completo  |
| `hermes/`     | Runtime operador local                |   18 | Completo  |

Nota: `hermes/` incluye dos agentes operativos propios del runtime (`Hermes-DocsMaintenanceAgent.md`, `Hermes-RepositoryOperator.md`) que no tienen espejo en los runtimes cognitivos, porque corresponden a operación local de repositorio.

---

## 5. Roles por runtime

```text
GPT    = runtime cognitivo general: clasificación, estructuración, validación,
         procesamiento del pipeline, salidas JSON estrictas.
Claude = runtime cognitivo y editorial: razonamiento editorial, redacción
         estructurada, análisis documental de contexto largo, revisión de
         consistencia, planeación de handoffs, generación de prompts y documentos.
Hermes = operador local de ejecución: repositorio, archivos, validaciones,
         estructura documental, flujos controlados. No es motor cognitivo.
```

Regla operativa:

```text
GPT / Claude = motores cognitivos
Hermes = operador de ejecución
```

---

## 6. Agentes espejo (13)

Cada runtime tiene un adaptador por cada agente oficial:

| Agente               | GPT                             | Claude                             | Hermes                             |
| -------------------- | ------------------------------- | ---------------------------------- | ---------------------------------- |
| NewsScoutAgent       | `GPT-NewsScoutAgent.md`       | `Claude-NewsScoutAgent.md`       | `Hermes-NewsScoutAgent.md`       |
| SourceValidatorAgent | `GPT-SourceValidatorAgent.md` | `Claude-SourceValidatorAgent.md` | `Hermes-SourceValidatorAgent.md` |
| EditorialAgent       | `GPT-EditorialAgent.md`       | `Claude-EditorialAgent.md`       | `Hermes-EditorialAgent.md`       |
| MarketImpactAgent    | `GPT-MarketImpactAgent.md`    | `Claude-MarketImpactAgent.md`    | `Hermes-MarketImpactAgent.md`    |
| ScriptAgent          | `GPT-ScriptAgent.md`          | `Claude-ScriptAgent.md`          | `Hermes-ScriptAgent.md`          |
| RiskAgent            | `GPT-RiskAgent.md`            | `Claude-RiskAgent.md`            | `Hermes-RiskAgent.md`            |
| AuditAgent           | `GPT-AuditAgent.md`           | `Claude-AuditAgent.md`           | `Hermes-AuditAgent.md`           |
| KnowledgeAgent       | `GPT-KnowledgeAgent.md`       | `Claude-KnowledgeAgent.md`       | `Hermes-KnowledgeAgent.md`       |
| DistributionAgent    | `GPT-DistributionAgent.md`    | `Claude-DistributionAgent.md`    | `Hermes-DistributionAgent.md`    |
| SocialClipAgent      | `GPT-SocialClipAgent.md`      | `Claude-SocialClipAgent.md`      | `Hermes-SocialClipAgent.md`      |
| MemoryAgent          | `GPT-MemoryAgent.md`          | `Claude-MemoryAgent.md`          | `Hermes-MemoryAgent.md`          |
| MetricsAgent         | `GPT-MetricsAgent.md`         | `Claude-MetricsAgent.md`         | `Hermes-MetricsAgent.md`         |
| CalendarAgent        | `GPT-CalendarAgent.md`        | `Claude-CalendarAgent.md`        | `Hermes-CalendarAgent.md`        |

---

## 7. Naming convention

```text
Global system:         00-<runtime>-global-system.md
Execution contract:    <Runtime>-Agent-Execution-Contract.md
Adaptador de agente:   <Runtime>-<AgentName>.md
Contratos compartidos: kebab-case descriptivo (solo 000-shared/)
```

Convención legacy retirada:

```text
Prompt-<AgentName>.md
```

Los archivos con ese patrón fueron renombrados a `GPT-<AgentName>.md`. No deben crearse archivos nuevos con la convención legacy.

---

## 8. Orden de carga por ejecución

Para ejecutar un agente en cualquier runtime, el contexto mínimo es:

```text
1. docs/004-agentes/<AgentName>.md
2. docs/007-prompts/000-shared/agent-base-contract.md
3. docs/007-prompts/000-shared/agent-output-standards.md
4. docs/007-prompts/000-shared/editorial-guardrails.md
5. docs/007-prompts/<runtime>/00-<runtime>-global-system.md
6. docs/007-prompts/<runtime>/<Runtime>-Agent-Execution-Contract.md
7. docs/007-prompts/<runtime>/<Runtime>-<AgentName>.md
```

Si falta un documento crítico, el runtime debe declararlo y bloquear en lugar de improvisar.

---

## 9. Flujo operativo de agentes

Flujo editorial estándar:

```text
NewsScoutAgent
→ SourceValidatorAgent
→ MarketImpactAgent
→ RiskAgent
→ EditorialAgent
→ ScriptAgent
→ SocialClipAgent
→ DistributionAgent
→ AuditAgent
→ CalendarAgent
→ MetricsAgent
→ MemoryAgent
→ KnowledgeAgent
```

Regla para breaking news:

```text
Breaking news no elimina verificación.
La urgencia no reemplaza fuente, riesgo, auditoría ni aprobación.
```

Regla para variantes sociales:

```text
Una variante social no puede cambiar el nivel de certeza de la pieza original.
```

Regla para memoria y conocimiento:

```text
La memoria no es fuente factual.
El conocimiento conecta contexto, no confirma hechos por sí solo.
```

---

## 10. Handoff entre runtimes

```text
Procesamiento estructurado del pipeline        → GPT
Razonamiento editorial / contexto largo /
revisión profunda / generación documental      → Claude
Operación local de repositorio o archivos      → Hermes
Aprobación, decisión editorial, juicio legal   → Human
```

Todo handoff debe declarar origen, destino, razón, payload y siguiente acción. El detalle vive en cada `<Runtime>-Agent-Execution-Contract.md`.

---

## 11. Reglas obligatorias para todos los runtimes

```text
No inventar fuentes.
No inventar datos ni métricas.
No publicar directamente.
No aprobar contenido final.
No convertir rumores en hechos.
No usar memoria como fuente factual.
No predecir precios.
No recomendar compra o venta.
No reducir incertidumbre artificialmente.
No ignorar bloqueos editoriales.
No ignorar RiskAgent.
No ignorar AuditAgent.
No saltarse revisión humana cuando aplica.
```

---

## 12. Estados globales del pipeline

```text
detected
registered
classified
validating
verified
partially_verified
rumor
monitoring
rejected
prioritized
drafting
reviewing
approved
scheduled
published
distributed
measured
archived
corrected
retracted
escalated
```

---

## 13. Dependencias documentales

| Documento                                            | Relación                     |
| ---------------------------------------------------- | ----------------------------- |
| `ORION-005-Constitucion-Editorial.md`              | Define límites editoriales   |
| `ORION-006-Estandares-Editoriales.md`              | Define calidad editorial      |
| `ORION-007-Flujo-Editorial.md`                     | Define flujo base             |
| `ORION-012-Grafo-de-Conocimiento.md`               | Define relaciones semánticas |
| `ORION-013-Modelo-de-Datos.md`                     | Define entidades y registros  |
| `ORION-014-Arquitectura-de-Agentes.md`             | Define arquitectura de agentes |
| `ORION-022-Protocolo-de-Verificacion-Editorial.md` | Define verificación          |
| `ORION-023-Pipeline-del-Newsroom.md`               | Define pipeline completo      |
| `ORION-028-Operacion-de-Agentes-Editoriales.md`    | Define operación de agentes  |

---

## 14. Criterios de aceptación del volumen 007

* [X] Existe `INDEX.md` actualizado a la estructura real.
* [X] Existe `README.md` general del volumen.
* [X] Existe paquete `000-shared/` con contratos compartidos.
* [X] Existe paquete GPT completo (global system + contrato + 13 adaptadores + README).
* [X] Existe paquete Claude completo (global system + contrato + 13 adaptadores + README).
* [X] Existe paquete Hermes completo (global system + contrato + 15 agentes + README).
* [X] Los paquetes GPT usan naming `GPT-*` sin referencias legacy `Prompt-*`.
* [ ] Los cuatro paquetes están versionados en git (pendiente: hoy `.gitignore` excluye `000-shared/`, `claude/` y `hermes/`; requiere coordinación antes de editarlo).
* [ ] Revisión cruzada de consistencia semántica entre los tres runtimes por GPT/AuditAgent.

---

## 15. Notas de mantenimiento

```text
- Este índice describe la estructura real del volumen. Si un archivo se
  agrega, renombra o elimina, este índice debe actualizarse en el mismo cambio.
- La versión 1.0 de este índice describía una estructura anterior
  (Prompt-*.md en gpt/, paquetes Claude/Hermes planeados con otro modelo).
  Esa estructura quedó obsoleta y fue reemplazada por la actual.
- Las carpetas docs/008-decisiones/ y docs/009-sprints/ están referenciadas
  en docs/INDEX.md pero no existen en el working tree actual:
  candidate for archive/delete pending reference cleanup.
```

---

## 16. Historial de cambios

| Versión | Fecha      | Cambio                                                                                             | Autor            |
| -------- | ---------- | --------------------------------------------------------------------------------------------------- | ---------------- |
| 1.0      | 2026-07-02 | Índice inicial del volumen 007-prompts (estructura antigua)                                        | Fernando Cuellar |
| 2.0      | 2026-07-02 | Reescritura completa: estructura real con 000-shared, claude, gpt, hermes; retiro de naming legacy | Claude (ORION)   |
