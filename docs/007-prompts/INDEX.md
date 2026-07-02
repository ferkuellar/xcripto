# INDEX — Prompts Operativos XMIP

**Nivel documental:** L4 — Operations / Prompts
**Volumen:** 007-prompts
**Proyecto:** ORION / XCripto / XMIP
**Versión:** 1.0
**Estado:** Draft
**Owner:** Fernando Cuellar
**Última actualización:** 2026-07-02
**Ruta sugerida:** `docs/007-prompts/INDEX.md`

---

## 1. Propósito

Este índice organiza el volumen **007-prompts** del proyecto ORION / XCripto / XMIP.

El objetivo de este volumen es centralizar los prompts operativos, editoriales, técnicos y de ejecución utilizados por los modelos de inteligencia artificial que apoyan la operación de XCripto como agencia de noticias, análisis y contenido cripto.

Este volumen define:

* Prompts canónicos de agentes.
* Prompts maestros por modelo.
* Prompts de operación del newsroom.
* Prompts para producción editorial.
* Prompts para análisis, distribución, memoria, auditoría y métricas.
* Prompts para ejecución técnica o asistida por agentes.

---

## 2. Alcance

Este volumen cubre prompts para:

```text
GPT
Claude
Hermes
```

Cada carpeta tiene una función distinta dentro de XMIP.

---

## 3. Principio rector

```text
GPT define agentes.
Claude desarrolla pensamiento, contenido y arquitectura.
Hermes ejecuta operación compacta y flujos.
```

Regla principal:

```text
No duplicar prompts entre modelos sin una razón operativa.
Cada modelo debe tener prompts adaptados a su fortaleza.
```

---

## 4. Estructura del volumen

```text
docs/007-prompts
│   INDEX.md
│   README.md
│
├───gpt
│       Prompt-NewsScoutAgent.md
│       Prompt-SourceValidatorAgent.md
│       Prompt-RiskAgent.md
│       Prompt-EditorialAgent.md
│       Prompt-ScriptAgent.md
│       Prompt-SocialClipAgent.md
│       Prompt-DistributionAgent.md
│       Prompt-AuditAgent.md
│       Prompt-MemoryAgent.md
│       Prompt-MarketImpactAgent.md
│       Prompt-KnowledgeAgent.md
│       Prompt-CalendarAgent.md
│       Prompt-MetricsAgent.md
│
├───claude
│       README.md
│       Claude-Newsroom-MasterPrompt.md
│       Claude-Editorial-Workbench.md
│       Claude-Script-Studio.md
│       Claude-Social-Distribution.md
│       Claude-Code-XMIP-Builder.md
│
└───hermes
        README.md
        Hermes-System-Prompt.md
        Hermes-Agent-Router.md
        Hermes-Newsroom-Workflow.md
        Hermes-Operational-Commands.md
```

---

## 5. Uso por modelo

## 5.1 GPT

La carpeta `gpt/` contiene los prompts formales de agentes digitales de XMIP.

GPT se usa como base para:

* Agentes estructurados.
* Clasificación.
* Revisión.
* Validación.
* Auditoría.
* Ruteo.
* Salidas JSON.
* Control de estados.
* Procesamiento operativo del pipeline.

GPT debe operar con instrucciones estrictas, esquemas claros y reglas de bloqueo.

---

## 5.2 Claude

La carpeta `claude/` contiene prompts para trabajo editorial, creativo, analítico, documental y arquitectónico de mayor profundidad.

Claude se usa para:

* Guiones largos.
* Documentación estratégica.
* Revisión editorial extensa.
* Análisis narrativo.
* Diseño de producto.
* Claude Code.
* Claude Design.
* Landing pages.
* Documentación técnica.
* Redacción premium.
* Explicaciones largas.
* Workbenches editoriales.

Claude no reemplaza las reglas formales de los agentes GPT; las consume como marco de trabajo.

---

## 5.3 Hermes

La carpeta `hermes/` contiene prompts compactos para operación desde agente, terminal, CLI o flujos de ejecución.

Hermes se usa para:

* Ruteo operativo.
* Comandos compactos.
* Ejecución de workflows.
* Resúmenes de estado.
* Operación de newsroom.
* Coordinación de agentes.
* Procesos repetibles.
* Ejecución con contexto limitado.

Hermes no debe cargar documentos largos innecesariamente. Debe operar con prompts breves, explícitos y orientados a acción.

---

## 6. Prompts GPT

Los prompts GPT son la base canónica de los agentes digitales de XMIP.

| Archivo                                | Agente               | Función                                                   | Estado |
| -------------------------------------- | -------------------- | ---------------------------------------------------------- | ------ |
| `gpt/Prompt-NewsScoutAgent.md`       | NewsScoutAgent       | Detecta señales y noticias candidatas                     | Listo  |
| `gpt/Prompt-SourceValidatorAgent.md` | SourceValidatorAgent | Evalúa fuentes, evidencia y estado de verificación       | Listo  |
| `gpt/Prompt-RiskAgent.md`            | RiskAgent            | Detecta riesgo editorial, legal, reputacional y financiero | Listo  |
| `gpt/Prompt-EditorialAgent.md`       | EditorialAgent       | Convierte información validada en contenido editorial     | Listo  |
| `gpt/Prompt-ScriptAgent.md`          | ScriptAgent          | Convierte briefs y piezas en guiones audiovisuales         | Listo  |
| `gpt/Prompt-SocialClipAgent.md`      | SocialClipAgent      | Crea variantes sociales, hooks, captions y clips           | Listo  |
| `gpt/Prompt-DistributionAgent.md`    | DistributionAgent    | Planea distribución multicanal trazable                   | Listo  |
| `gpt/Prompt-AuditAgent.md`           | AuditAgent           | Valida trazabilidad, registros, bloqueos y readiness       | Listo  |
| `gpt/Prompt-MemoryAgent.md`          | MemoryAgent          | Propone memoria editorial y operativa reutilizable         | Listo  |
| `gpt/Prompt-MarketImpactAgent.md`    | MarketImpactAgent    | Clasifica impacto sin predecir precios                     | Listo  |
| `gpt/Prompt-KnowledgeAgent.md`       | KnowledgeAgent       | Propone nodos y relaciones del grafo de conocimiento       | Listo  |
| `gpt/Prompt-CalendarAgent.md`        | CalendarAgent        | Coordina agenda editorial y programación                  | Listo  |
| `gpt/Prompt-MetricsAgent.md`         | MetricsAgent         | Analiza métricas operativas, editoriales y de audiencia   | Listo  |

---

## 7. Flujo operativo de agentes GPT

Flujo recomendado:

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

Este flujo puede variar según el tipo de noticia, nivel de riesgo, prioridad y canal.

---

## 8. Flujo para breaking news

```text
NewsScoutAgent
→ SourceValidatorAgent
→ RiskAgent
→ MarketImpactAgent
→ EditorialAgent
→ AuditAgent
→ DistributionAgent
→ CalendarAgent
→ MetricsAgent
→ MemoryAgent
→ KnowledgeAgent
```

Regla:

```text
Breaking news no elimina verificación.
La urgencia no reemplaza fuente, riesgo, auditoría ni aprobación.
```

---

## 9. Flujo para guion de video

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
```

---

## 10. Flujo para contenido social

```text
EditorialAgent / ScriptAgent
→ RiskAgent si aplica
→ SocialClipAgent
→ DistributionAgent
→ AuditAgent
→ CalendarAgent
→ MetricsAgent
```

Regla:

```text
Una variante social no puede cambiar el nivel de certeza de la pieza original.
```

---

## 11. Flujo para memoria y conocimiento

```text
IncidentRecord / MetricSnapshot / AuditCheck / EditorialDecision
→ MemoryAgent
→ AuditAgent
→ KnowledgeAgent
```

Regla:

```text
La memoria no es fuente factual.
El conocimiento conecta contexto, no confirma hechos por sí solo.
```

---

## 12. Prompts Claude recomendados

La carpeta `claude/` debe contener prompts orientados a trabajo profundo, redacción y arquitectura.

| Archivo                                    | Función                                                     | Estado    |
| ------------------------------------------ | ------------------------------------------------------------ | --------- |
| `claude/README.md`                       | Explica uso de Claude dentro de XMIP                         | Pendiente |
| `claude/Claude-Newsroom-MasterPrompt.md` | Prompt maestro para operar XCripto como newsroom             | Pendiente |
| `claude/Claude-Editorial-Workbench.md`   | Mesa de trabajo editorial para notas, análisis y revisiones | Pendiente |
| `claude/Claude-Script-Studio.md`         | Producción avanzada de guiones largos y noticieros          | Pendiente |
| `claude/Claude-Social-Distribution.md`   | Adaptación social premium y piezas multicanal               | Pendiente |
| `claude/Claude-Code-XMIP-Builder.md`     | Prompt para Claude Code orientado a construir XMIP           | Pendiente |

---

## 13. Uso recomendado de Claude

Claude debe utilizarse cuando se requiera:

* Razonamiento editorial largo.
* Producción de documentos extensos.
* Guiones de noticiero.
* Análisis detallado de una narrativa.
* Revisión de tono.
* Revisión de coherencia.
* Desarrollo de arquitectura.
* Creación de prompts largos.
* Diseño de UX/UI.
* Construcción asistida con Claude Code.
* Prototipos visuales con Claude Design.

Claude debe respetar los documentos ORION y los prompts GPT como marco de gobierno.

---

## 14. Prompts Hermes recomendados

La carpeta `hermes/` debe contener prompts compactos orientados a operación y ejecución.

| Archivo                                   | Función                                  | Estado    |
| ----------------------------------------- | ----------------------------------------- | --------- |
| `hermes/README.md`                      | Explica uso de Hermes dentro de XMIP      | Pendiente |
| `hermes/Hermes-System-Prompt.md`        | Prompt base del operador Hermes           | Pendiente |
| `hermes/Hermes-Agent-Router.md`         | Ruteo de tareas hacia agentes correctos   | Pendiente |
| `hermes/Hermes-Newsroom-Workflow.md`    | Flujo operativo del newsroom desde Hermes | Pendiente |
| `hermes/Hermes-Operational-Commands.md` | Comandos compactos para operación diaria | Pendiente |

---

## 15. Uso recomendado de Hermes

Hermes debe utilizarse cuando se requiera:

* Ejecutar flujos compactos.
* Operar desde terminal o CLI.
* Coordinar agentes.
* Resumir estado.
* Activar workflows.
* Hacer ruteo.
* Revisar tareas pendientes.
* Operar sin cargar contexto excesivo.
* Ejecutar comandos de newsroom.

Hermes debe ser operativo, no creativo.

---

## 16. Relación entre GPT, Claude y Hermes

| Modelo / Carpeta | Rol dentro de XMIP             | Tipo de prompt                     |
| ---------------- | ------------------------------ | ---------------------------------- |
| `gpt/`         | Agentes canónicos             | Formal, estructurado, con schemas  |
| `claude/`      | Workbench editorial y técnico | Largo, creativo, analítico        |
| `hermes/`      | Operación y ejecución        | Compacto, accionable, tipo comando |

---

## 17. Reglas de consistencia

Todos los prompts de este volumen deben respetar:

* La Constitución Editorial.
* Los Estándares Editoriales.
* El Flujo Editorial.
* El Protocolo de Verificación.
* El Pipeline del Newsroom.
* La Gestión de Incidentes.
* La Operación de Agentes.
* El principio human-in-the-loop.
* La trazabilidad por `correlation_id`.
* La separación entre fuente, memoria, análisis y publicación.

---

## 18. Reglas obligatorias para todos los modelos

Todo prompt debe respetar estas reglas:

```text
No inventar fuentes.
No inventar datos.
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
```

---

## 19. Estados globales del pipeline

Los prompts deben respetar los siguientes estados globales:

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

## 20. Agentes principales de XMIP

| Agente               | Prompt base                        | Carpeta  |
| -------------------- | ---------------------------------- | -------- |
| NewsScoutAgent       | `Prompt-NewsScoutAgent.md`       | `gpt/` |
| SourceValidatorAgent | `Prompt-SourceValidatorAgent.md` | `gpt/` |
| RiskAgent            | `Prompt-RiskAgent.md`            | `gpt/` |
| MarketImpactAgent    | `Prompt-MarketImpactAgent.md`    | `gpt/` |
| EditorialAgent       | `Prompt-EditorialAgent.md`       | `gpt/` |
| ScriptAgent          | `Prompt-ScriptAgent.md`          | `gpt/` |
| SocialClipAgent      | `Prompt-SocialClipAgent.md`      | `gpt/` |
| DistributionAgent    | `Prompt-DistributionAgent.md`    | `gpt/` |
| AuditAgent           | `Prompt-AuditAgent.md`           | `gpt/` |
| MemoryAgent          | `Prompt-MemoryAgent.md`          | `gpt/` |
| KnowledgeAgent       | `Prompt-KnowledgeAgent.md`       | `gpt/` |
| CalendarAgent        | `Prompt-CalendarAgent.md`        | `gpt/` |
| MetricsAgent         | `Prompt-MetricsAgent.md`         | `gpt/` |

---

## 21. Dependencias documentales

Este volumen depende de:

| Documento                                            | Relación                     |
| ---------------------------------------------------- | ----------------------------- |
| `ORION-005-Constitucion-Editorial.md`              | Define límites editoriales   |
| `ORION-006-Estandares-Editoriales.md`              | Define calidad editorial      |
| `ORION-007-Flujo-Editorial.md`                     | Define flujo base             |
| `ORION-012-Grafo-de-Conocimiento.md`               | Define relaciones semánticas |
| `ORION-013-Modelo-de-Datos.md`                     | Define entidades y registros  |
| `ORION-018-Operaciones-Diarias.md`                 | Define rutina diaria          |
| `ORION-019-Flujo-de-Publicacion.md`                | Define publicación           |
| `ORION-020-Runbook-de-Produccion-de-Noticias.md`   | Define producción            |
| `ORION-021-Gestion-de-Fuentes.md`                  | Define fuentes                |
| `ORION-022-Protocolo-de-Verificacion-Editorial.md` | Define verificación          |
| `ORION-023-Pipeline-del-Newsroom.md`               | Define pipeline completo      |
| `ORION-024-Calendario-Editorial.md`                | Define agenda                 |
| `ORION-025-Distribucion-Multicanal.md`             | Define canales                |
| `ORION-026-Metricas-Operativas.md`                 | Define medición              |
| `ORION-027-Gestion-de-Incidentes-Editoriales.md`   | Define incidentes             |
| `ORION-028-Operacion-de-Agentes-Editoriales.md`    | Define operación de agentes  |
| `ORION-029-Checklist-Diario-del-Newsroom.md`       | Define checklist diario       |

---

## 22. Paquete GPT actual

Estado del paquete GPT:

```text
Prompts planeados: 13
Prompts creados: 13
Prompts pendientes: 0
Estado: paquete operativo inicial completo
```

Lista:

```text
Prompt-NewsScoutAgent.md
Prompt-SourceValidatorAgent.md
Prompt-RiskAgent.md
Prompt-EditorialAgent.md
Prompt-ScriptAgent.md
Prompt-SocialClipAgent.md
Prompt-DistributionAgent.md
Prompt-AuditAgent.md
Prompt-MemoryAgent.md
Prompt-MarketImpactAgent.md
Prompt-KnowledgeAgent.md
Prompt-CalendarAgent.md
Prompt-MetricsAgent.md
```

---

## 23. Paquete Claude pendiente

Estado del paquete Claude:

```text
Prompts planeados iniciales: 6
Prompts creados: 0
Prompts pendientes: 6
Estado: pendiente de definición
```

Siguiente archivo recomendado:

```text
docs/007-prompts/claude/README.md
```

---

## 24. Paquete Hermes pendiente

Estado del paquete Hermes:

```text
Prompts planeados iniciales: 5
Prompts creados: 0
Prompts pendientes: 5
Estado: pendiente de definición
```

Siguiente archivo recomendado después de Claude:

```text
docs/007-prompts/hermes/README.md
```

---

## 25. Orden recomendado de construcción

Orden recomendado para completar el volumen 007:

```text
1. docs/007-prompts/INDEX.md
2. docs/007-prompts/README.md
3. docs/007-prompts/claude/README.md
4. docs/007-prompts/claude/Claude-Newsroom-MasterPrompt.md
5. docs/007-prompts/claude/Claude-Editorial-Workbench.md
6. docs/007-prompts/claude/Claude-Script-Studio.md
7. docs/007-prompts/claude/Claude-Social-Distribution.md
8. docs/007-prompts/claude/Claude-Code-XMIP-Builder.md
9. docs/007-prompts/hermes/README.md
10. docs/007-prompts/hermes/Hermes-System-Prompt.md
11. docs/007-prompts/hermes/Hermes-Agent-Router.md
12. docs/007-prompts/hermes/Hermes-Newsroom-Workflow.md
13. docs/007-prompts/hermes/Hermes-Operational-Commands.md
```

---

## 26. No duplicación

No se deben copiar los 13 prompts GPT directamente a Claude o Hermes.

En su lugar:

```text
GPT = definición formal del agente
Claude = uso extendido, creativo, editorial o técnico
Hermes = operación compacta y ejecución
```

Ejemplo:

```text
Prompt-EditorialAgent.md
```

no debe duplicarse como:

```text
Claude-EditorialAgent.md
```

Debe convertirse en:

```text
Claude-Editorial-Workbench.md
```

porque Claude no actúa como agente formal, sino como mesa editorial avanzada.

---

## 27. Criterios de aceptación del volumen 007

El volumen `007-prompts` se considera completo en su primera versión cuando:

* [X] Existe paquete GPT con prompts canónicos de agentes.
* [ ] Existe `README.md` general del volumen.
* [X] Existe `INDEX.md`.
* [ ] Existe README de Claude.
* [ ] Existe prompt maestro de Claude.
* [ ] Existe prompt Claude editorial.
* [ ] Existe prompt Claude para guiones.
* [ ] Existe prompt Claude para distribución social.
* [ ] Existe prompt Claude Code para XMIP.
* [ ] Existe README de Hermes.
* [ ] Existe prompt base de Hermes.
* [ ] Existe router Hermes.
* [ ] Existe workflow Hermes.
* [ ] Existe comandos Hermes.
* [ ] Los tres paquetes respetan ORION.
* [ ] Los tres paquetes diferencian claramente modelo, rol y uso.

---

## 28. Decisión operativa

La decisión actual es:

```text
Completar primero la capa de prompts canónicos GPT.
Después crear adaptadores Claude.
Finalmente crear operación Hermes.
```

Estado:

```text
GPT completado.
Claude pendiente.
Hermes pendiente.
```

---

## 29. Siguiente documento recomendado

El siguiente documento recomendado es:

```text
docs/007-prompts/README.md
```

Después:

```text
docs/007-prompts/claude/README.md
```

---

## 30. Historial de cambios

| Versión | Fecha      | Cambio                                  | Autor            |
| -------- | ---------- | --------------------------------------- | ---------------- |
| 1.0      | 2026-07-02 | Índice inicial del volumen 007-prompts | Fernando Cuellar |
