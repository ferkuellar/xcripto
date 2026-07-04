# ORION — Índice Maestro de Documentación

**Proyecto:** ORION / XCripto / XMIP
**Documento:** Índice maestro de documentación
**Versión:** 1.0
**Estado:** Draft
**Owner:** Fernando Cuellar
**Última actualización:** 2026-07-02
**Ruta:** `docs/INDEX.md`

---

## 1. Propósito

Este documento funciona como el índice maestro de la documentación del proyecto ORION / XCripto / XMIP.

Su propósito es servir como punto central de navegación para todos los documentos estratégicos, editoriales, arquitectónicos, operativos, técnicos y de ejecución del proyecto.

ORION es el sistema de gobierno documental y arquitectónico.
XCripto es la agencia / medio cripto.
XMIP es la plataforma interna multiagente que opera el newsroom, la inteligencia editorial y los flujos de producción.

---

## 2. Definición del proyecto

```text
ORION = Gobierno, arquitectura, doctrina y documentación del sistema.
XCripto = Medio, agencia de noticias, análisis y contenido cripto.
XMIP = XCripto Media Intelligence Platform, plataforma interna multiagente para operar la agencia.
```

Definición operativa:

> XCripto será una agencia de noticias, análisis y contenido cripto operada por XMIP, una plataforma multiagente de inteligencia editorial gobernada por ORION.

---

## 3. Estructura general del repositorio

```text
.
├── apps/
├── backend/
├── docs/
│   ├── INDEX.md
│   ├── 000-fundacion/
│   ├── 001-estrategia/
│   ├── 002-editorial/
│   ├── 003-arquitectura/
│   ├── 004-agentes/
│   ├── 005-producto/
│   ├── 006-operaciones/
│   ├── 007-prompts/
│   ├── 008-decisiones/   ← no existe en el working tree actual
│   └── 009-sprints/      ← no existe en el working tree actual
├── frontend/
└── newsroom/
```

> ⚠️ **Nota (2026-07-02):** `apps/` y `newsroom/` existen pero están vacías, y `docs/008-decisiones/` y `docs/009-sprints/` fueron removidas del working tree sin commit. Las cuatro rutas están en estado: candidate for archive/delete pending reference cleanup.

---

## 4. Mapa documental

| Volumen              | Nombre       | Propósito                                                          |
| -------------------- | ------------ | ------------------------------------------------------------------- |
| `000-fundacion`    | Fundación   | Define identidad, doctrina, lenguaje y base conceptual del proyecto |
| `001-estrategia`   | Estrategia   | Define propósito, visión, principios y modelo de negocio          |
| `002-editorial`    | Editorial    | Define cómo piensa, escribe y publica XCripto                      |
| `003-arquitectura` | Arquitectura | Define arquitectura empresarial, sistema, datos y conocimiento      |
| `004-agentes`      | Agentes      | Define arquitectura y especificación de agentes digitales          |
| `005-producto`     | Producto     | Define visión, MVP y roadmap de XMIP                               |
| `006-operaciones`  | Operaciones  | Define operación diaria del newsroom y flujos editoriales          |
| `007-prompts`      | Prompts      | Contendrá prompts operativos para agentes y modelos                |
| `008-decisiones`   | Decisiones   | Contendrá ADRs y decisiones arquitectónicas                       |
| `009-sprints`      | Sprints      | Contendrá ejecución incremental del proyecto                      |

---

## 5. Niveles documentales

| Nivel | Nombre       | Propósito                   | Frecuencia de cambio |
| ----- | ------------ | ---------------------------- | -------------------- |
| L0    | Constitution | Constitución del proyecto   | Muy baja             |
| L1    | Strategy     | Estrategia y fundamentos     | Baja                 |
| L2    | Architecture | Arquitectura del sistema     | Baja / media         |
| L3    | Product      | Producto, MVP y roadmap      | Media                |
| L4    | Operations   | Operación diaria y runbooks | Alta                 |
| L5    | Sprints      | Ejecución incremental       | Muy alta             |

---

# 6. Volumen 000 — Fundación

## 6.1 Propósito

Define la base conceptual del proyecto: qué es ORION, qué es XCripto, qué es XMIP, qué lenguaje se usa y qué doctrina guía el sistema.

## 6.2 Documentos

| Código    | Documento             | Ruta                                                       | Estado |
| ---------- | --------------------- | ---------------------------------------------------------- | ------ |
| ORION-000  | Project Charter       | `docs/000-fundacion/ORION-000-Project-Charter.md`        | Draft  |
| ORION-000A | Glosario del Proyecto | `docs/000-fundacion/ORION-000A-Glosario-del-Proyecto.md` | Draft  |
| ORION-000B | Doctrina XCripto      | `docs/000-fundacion/ORION-000B-Doctrina-XCripto.md`      | Draft  |

---

# 7. Volumen 001 — Estrategia

## 7.1 Propósito

Define por qué existe el proyecto, qué problema resuelve, cómo compite, cómo opera como negocio y qué principios estratégicos lo gobiernan.

## 7.2 Documentos

| Código   | Documento               | Ruta                                                        | Estado |
| --------- | ----------------------- | ----------------------------------------------------------- | ------ |
| ORION-001 | Fundamento Estratégico | `docs/001-estrategia/ORION-001-Fundamento-Estrategico.md` | Draft  |
| ORION-002 | Manifiesto XCripto      | `docs/001-estrategia/ORION-002-Manifiesto-XCripto.md`     | Draft  |
| ORION-003 | Principios Operativos   | `docs/001-estrategia/ORION-003-Principios-Operativos.md`  | Draft  |
| ORION-004 | Modelo de Negocio       | `docs/001-estrategia/ORION-004-Modelo-de-Negocio.md`      | Draft  |

---

# 8. Volumen 002 — Editorial

## 8.1 Propósito

Define cómo piensa, escribe, verifica, estructura y publica XCripto como agencia de noticias, análisis y contenido cripto.

## 8.2 Documentos

| Código   | Documento               | Ruta                                                       | Estado |
| --------- | ----------------------- | ---------------------------------------------------------- | ------ |
| ORION-005 | Constitución Editorial | `docs/002-editorial/ORION-005-Constitucion-Editorial.md` | Draft  |
| ORION-006 | Estándares Editoriales | `docs/002-editorial/ORION-006-Estandares-Editoriales.md` | Draft  |
| ORION-007 | Flujo Editorial         | `docs/002-editorial/ORION-007-Flujo-Editorial.md`        | Draft  |
| ORION-008 | Guía de Estilo         | `docs/002-editorial/ORION-008-Guia-de-Estilo.md`         | Draft  |

---

# 9. Volumen 003 — Arquitectura

## 9.1 Propósito

Define cómo se diseña XMIP desde una perspectiva empresarial, lógica, técnica, de datos y conocimiento.

## 9.2 Documentos

| Código   | Documento                              | Ruta                                                                          | Estado |
| --------- | -------------------------------------- | ----------------------------------------------------------------------------- | ------ |
| ORION-009 | Principios de Arquitectura Empresarial | `docs/003-arquitectura/ORION-009-Principios-de-Arquitectura-Empresarial.md` | Draft  |
| ORION-010 | Arquitectura Empresarial               | `docs/003-arquitectura/ORION-010-Arquitectura-Empresarial.md`               | Draft  |
| ORION-011 | Arquitectura del Sistema               | `docs/003-arquitectura/ORION-011-Arquitectura-del-Sistema.md`               | Draft  |
| ORION-012 | Grafo de Conocimiento                  | `docs/003-arquitectura/ORION-012-Grafo-de-Conocimiento.md`                  | Draft  |
| ORION-013 | Modelo de Datos                        | `docs/003-arquitectura/ORION-013-Modelo-de-Datos.md`                        | Draft  |

---

# 10. Volumen 004 — Agentes

## 10.1 Propósito

Define la arquitectura, comunicación, especificación y operación base de los agentes digitales que participan en XMIP.

## 10.2 Documentos

| Código    | Documento                                | Ruta                                                                       | Estado |
| ---------- | ---------------------------------------- | -------------------------------------------------------------------------- | ------ |
| ORION-014  | Arquitectura de Agentes                  | `docs/004-agentes/ORION-014-Arquitectura-de-Agentes.md`                  | Draft  |
| ORION-014A | Protocolo de Comunicación entre Agentes | `docs/004-agentes/ORION-014A-Protocolo-de-Comunicacion-entre-Agentes.md` | Draft  |
| ORION-014B | Especificación de Agentes Digitales     | `docs/004-agentes/ORION-014B-Especificacion-de-Agentes-Digitales.md`     | Draft  |

---

## 10.3 Nota de normalización de archivo

Si existe el archivo:

```text
docs/004-agentes/ORION-014B-Especificación de Agentes Digitales.md
```

se recomienda renombrarlo a:

```text
docs/004-agentes/ORION-014B-Especificacion-de-Agentes-Digitales.md
```

Motivo:

* Evitar acentos en rutas.
* Evitar espacios en nombres de archivo.
* Mantener consistencia con el estándar del repositorio.

---

# 11. Volumen 005 — Producto

## 11.1 Propósito

Define qué producto se está construyendo, cuál es su MVP y cómo evolucionará XMIP como plataforma interna para operar XCripto.

## 11.2 Documentos

| Código   | Documento           | Ruta                                                  | Estado |
| --------- | ------------------- | ----------------------------------------------------- | ------ |
| ORION-015 | Visión de Producto | `docs/005-producto/ORION-015-Vision-de-Producto.md` | Draft  |
| ORION-016 | Definición del MVP | `docs/005-producto/ORION-016-Definicion-del-MVP.md` | Draft  |
| ORION-017 | Roadmap             | `docs/005-producto/ORION-017-Roadmap.md`            | Draft  |

---

## 11.3 Nota de alineación de producto

El producto debe mantenerse alineado con la definición operativa actual:

```text
XCripto = agencia / medio cripto.
XMIP = plataforma interna para operar el newsroom.
ORION = gobierno documental y arquitectónico.
```

El MVP real debe validar el flujo:

```text
fuente
→ noticia
→ validación
→ priorización
→ pieza editorial
→ guion / post / newsletter
→ publicación
→ memoria
→ auditoría
```

---

# 12. Volumen 006 — Operaciones

## 12.1 Propósito

Define cómo opera XCripto día a día como newsroom cripto, desde la detección de noticias hasta la publicación, distribución, métricas, incidentes, agentes y cierre operativo.

## 12.2 Estado del volumen

El volumen `006-operaciones` queda completo en su primera versión operativa.

## 12.3 Documentos

| Código   | Documento                            | Ruta                                                                      | Estado |
| --------- | ------------------------------------ | ------------------------------------------------------------------------- | ------ |
| ORION-018 | Operaciones Diarias                  | `docs/006-operaciones/ORION-018-Operaciones-Diarias.md`                 | Draft  |
| ORION-019 | Flujo de Publicación                | `docs/006-operaciones/ORION-019-Flujo-de-Publicacion.md`                | Draft  |
| ORION-020 | Runbook de Producción de Noticias   | `docs/006-operaciones/ORION-020-Runbook-de-Produccion-de-Noticias.md`   | Draft  |
| ORION-021 | Gestión de Fuentes                  | `docs/006-operaciones/ORION-021-Gestion-de-Fuentes.md`                  | Draft  |
| ORION-022 | Protocolo de Verificación Editorial | `docs/006-operaciones/ORION-022-Protocolo-de-Verificacion-Editorial.md` | Draft  |
| ORION-023 | Pipeline del Newsroom                | `docs/006-operaciones/ORION-023-Pipeline-del-Newsroom.md`               | Draft  |
| ORION-024 | Calendario Editorial                 | `docs/006-operaciones/ORION-024-Calendario-Editorial.md`                | Draft  |
| ORION-025 | Distribución Multicanal             | `docs/006-operaciones/ORION-025-Distribucion-Multicanal.md`             | Draft  |
| ORION-026 | Métricas Operativas                 | `docs/006-operaciones/ORION-026-Metricas-Operativas.md`                 | Draft  |
| ORION-027 | Gestión de Incidentes Editoriales   | `docs/006-operaciones/ORION-027-Gestion-de-Incidentes-Editoriales.md`   | Draft  |
| ORION-028 | Operación de Agentes Editoriales    | `docs/006-operaciones/ORION-028-Operacion-de-Agentes-Editoriales.md`    | Draft  |
| ORION-029 | Checklist Diario del Newsroom        | `docs/006-operaciones/ORION-029-Checklist-Diario-del-Newsroom.md`       | Draft  |

---

## 12.4 Flujo operativo cubierto

El volumen `006-operaciones` cubre el siguiente ciclo completo:

```text
apertura diaria
→ monitoreo de fuentes
→ intake de noticias
→ clasificación
→ verificación
→ priorización
→ producción
→ revisión
→ publicación
→ distribución
→ medición
→ incidentes
→ agentes
→ memoria
→ cierre diario
```

---

## 12.5 Relación entre documentos operativos

| Documento | Función dentro del volumen                              |
| --------- | -------------------------------------------------------- |
| ORION-018 | Define el modelo general de operación diaria            |
| ORION-019 | Define cómo se publica contenido aprobado               |
| ORION-020 | Define el runbook paso a paso para producir noticias     |
| ORION-021 | Define cómo se administran y califican fuentes          |
| ORION-022 | Define cómo se verifica una noticia antes de publicarse |
| ORION-023 | Conecta todo en un pipeline integral del newsroom        |
| ORION-024 | Organiza la agenda diaria, semanal y mensual             |
| ORION-025 | Define adaptación y distribución multicanal            |
| ORION-026 | Define cómo se mide la operación                       |
| ORION-027 | Define respuesta ante errores e incidentes               |
| ORION-028 | Define cómo operan los agentes editoriales              |
| ORION-029 | Consolida todo en checklist diario ejecutable            |

---

# 13. Volumen 007 — Prompts

## 13.1 Propósito

Contendrá prompts operativos para agentes, modelos y herramientas utilizados dentro de XMIP.

Este volumen debe transformar los documentos de estrategia, arquitectura y operación en instrucciones ejecutables para agentes digitales.

## 13.2 Estructura sugerida

```text
docs/
└── 007-prompts/
    ├── claude/
    ├── gpt/
    └── hermes/
```

---

## 13.3 Prompts recomendados

| Prompt                      | Ruta sugerida                                           | Propósito                              |
| --------------------------- | ------------------------------------------------------- | --------------------------------------- |
| Prompt NewsScoutAgent       | `docs/007-prompts/gpt/Prompt-NewsScoutAgent.md`       | Detectar noticias candidatas            |
| Prompt SourceValidatorAgent | `docs/007-prompts/gpt/Prompt-SourceValidatorAgent.md` | Validar fuentes                         |
| Prompt MarketImpactAgent    | `docs/007-prompts/gpt/Prompt-MarketImpactAgent.md`    | Clasificar impacto sin predecir precios |
| Prompt EditorialAgent       | `docs/007-prompts/gpt/Prompt-EditorialAgent.md`       | Crear briefs y piezas editoriales       |
| Prompt ScriptAgent          | `docs/007-prompts/gpt/Prompt-ScriptAgent.md`          | Crear guiones de video                  |
| Prompt SocialClipAgent      | `docs/007-prompts/gpt/Prompt-SocialClipAgent.md`      | Crear variantes para clips y redes      |
| Prompt RiskAgent            | `docs/007-prompts/gpt/Prompt-RiskAgent.md`            | Detectar riesgos editoriales            |
| Prompt AuditAgent           | `docs/007-prompts/gpt/Prompt-AuditAgent.md`           | Validar trazabilidad                    |
| Prompt MemoryAgent          | `docs/007-prompts/gpt/Prompt-MemoryAgent.md`          | Proponer memoria editorial              |
| Prompt KnowledgeAgent       | `docs/007-prompts/gpt/Prompt-KnowledgeAgent.md`       | Crear relaciones de conocimiento        |
| Prompt DistributionAgent    | `docs/007-prompts/gpt/Prompt-DistributionAgent.md`    | Crear planes de distribución           |
| Prompt CalendarAgent        | `docs/007-prompts/gpt/Prompt-CalendarAgent.md`        | Coordinar calendario editorial          |
| Prompt MetricsAgent         | `docs/007-prompts/gpt/Prompt-MetricsAgent.md`         | Analizar métricas operativas           |

---

# 14. Volumen 008 — Decisiones

## 14.1 Propósito

Contendrá ADRs y decisiones arquitectónicas, editoriales, técnicas y operativas relevantes.

## 14.2 Documentos actuales

| Código | Documento           | Ruta                                                   | Estado |
| ------- | ------------------- | ------------------------------------------------------ | ------ |
| ADR-001 | Documentation First | `docs/008-decisiones/ADR-001-Documentation-First.md` | Draft  |

> ⚠️ **Nota (2026-07-02):** la carpeta `docs/008-decisiones/` no existe en el working tree actual (fue removida sin commit). Estado: candidate for archive/delete pending reference cleanup. Requiere decisión: restaurar ADR-001 o retirar estas referencias.

---

## 14.3 ADRs recomendados

| Código | Documento sugerido                             | Propósito                                  |
| ------- | ---------------------------------------------- | ------------------------------------------- |
| ADR-002 | XMIP como plataforma interna del newsroom      | Formalizar que XMIP opera XCripto           |
| ADR-003 | PostgreSQL como base inicial                   | Formalizar base de datos relacional inicial |
| ADR-004 | Grafo lógico sobre modelo relacional          | Formalizar estrategia de conocimiento       |
| ADR-005 | Human-in-the-loop para decisiones críticas    | Formalizar control humano                   |
| ADR-006 | Documentation-first antes de implementación   | Reforzar modelo de trabajo                  |
| ADR-007 | Agentes sin autonomía completa en MVP         | Formalizar límite A5                       |
| ADR-008 | Bloqueo de publicación sin VerificationRecord | Formalizar regla editorial crítica         |
| ADR-009 | Memoria no es fuente factual                   | Formalizar límite de memoria               |
| ADR-010 | Newsroom como dominio principal del MVP        | Evitar deriva hacia producto genérico      |

---

# 15. Volumen 009 — Sprints

## 15.1 Propósito

Contendrá la ejecución incremental del proyecto.

Cada sprint debe derivarse de documentos aprobados y producir entregables verificables.

## 15.2 Documentos actuales

| Código    | Documento  | Ruta                               | Estado |
| ---------- | ---------- | ---------------------------------- | ------ |
| Sprint-001 | Sprint 001 | `docs/009-sprints/Sprint-001.md` | Draft  |

> ⚠️ **Nota (2026-07-02):** la carpeta `docs/009-sprints/` no existe en el working tree actual (fue removida sin commit). Estado: candidate for archive/delete pending reference cleanup. Requiere decisión: restaurar Sprint-001 o retirar estas referencias.

---

## 15.3 Sprints recomendados para XMIP Newsroom

| Sprint     | Nombre sugerido              | Objetivo                             |
| ---------- | ---------------------------- | ------------------------------------ |
| Sprint-001 | Project Workspace Foundation | Base del workspace                   |
| Sprint-002 | Document Registry            | Registro documental ORION            |
| Sprint-003 | News Intake MVP              | Captura de señales y noticias       |
| Sprint-004 | Source Registry MVP          | Registro y clasificación de fuentes |
| Sprint-005 | Verification Workflow MVP    | Verificación editorial básica      |
| Sprint-006 | Content Registry MVP         | Registro de piezas editoriales       |
| Sprint-007 | Agent Execution Log          | Registro de ejecución de agentes    |
| Sprint-008 | Publication Records          | Registro de publicaciones            |
| Sprint-009 | Distribution Records         | Distribución multicanal básica     |
| Sprint-010 | Metrics Snapshots            | Métricas operativas iniciales       |
| Sprint-011 | Incident Records             | Gestión básica de incidentes       |
| Sprint-012 | Memory Proposals             | Propuestas de memoria editorial      |
| Sprint-013 | Knowledge Links MVP          | Relaciones básicas de conocimiento  |
| Sprint-014 | Daily Newsroom Checklist     | Vista operativa diaria               |
| Sprint-015 | End-to-End Newsroom MVP      | Flujo completo funcional             |

---

# 16. Orden recomendado de lectura

## 16.1 Para entender el proyecto

1. ORION-000 — Project Charter.
2. ORION-000A — Glosario del Proyecto.
3. ORION-000B — Doctrina XCripto.
4. ORION-001 — Fundamento Estratégico.
5. ORION-004 — Modelo de Negocio.

---

## 16.2 Para entender la operación editorial

1. ORION-005 — Constitución Editorial.
2. ORION-006 — Estándares Editoriales.
3. ORION-007 — Flujo Editorial.
4. ORION-018 — Operaciones Diarias.
5. ORION-020 — Runbook de Producción de Noticias.
6. ORION-022 — Protocolo de Verificación Editorial.
7. ORION-023 — Pipeline del Newsroom.
8. ORION-029 — Checklist Diario del Newsroom.

---

## 16.3 Para entender la arquitectura

1. ORION-009 — Principios de Arquitectura Empresarial.
2. ORION-010 — Arquitectura Empresarial.
3. ORION-011 — Arquitectura del Sistema.
4. ORION-012 — Grafo de Conocimiento.
5. ORION-013 — Modelo de Datos.
6. ORION-014 — Arquitectura de Agentes.
7. ORION-014A — Protocolo de Comunicación entre Agentes.
8. ORION-014B — Especificación de Agentes Digitales.

---

## 16.4 Para entender el producto

1. ORION-015 — Visión de Producto.
2. ORION-016 — Definición del MVP.
3. ORION-017 — Roadmap.
4. ORION-023 — Pipeline del Newsroom.
5. ORION-029 — Checklist Diario del Newsroom.

---

## 16.5 Para implementar

1. ORION-013 — Modelo de Datos.
2. ORION-014B — Especificación de Agentes Digitales.
3. ORION-020 — Runbook de Producción de Noticias.
4. ORION-021 — Gestión de Fuentes.
5. ORION-022 — Protocolo de Verificación Editorial.
6. ORION-023 — Pipeline del Newsroom.
7. ORION-026 — Métricas Operativas.
8. ORION-028 — Operación de Agentes Editoriales.
9. ORION-029 — Checklist Diario del Newsroom.
10. Sprint-001 en adelante.

---

# 17. Estado general de avance documental

| Volumen              | Estado                    |
| -------------------- | ------------------------- |
| `000-fundacion`    | Base inicial creada       |
| `001-estrategia`   | Base inicial creada       |
| `002-editorial`    | Base inicial creada       |
| `003-arquitectura` | Base inicial creada       |
| `004-agentes`      | Base inicial creada       |
| `005-producto`     | Base inicial creada       |
| `006-operaciones`  | Primera versión completa |
| `007-prompts`      | Pendiente de desarrollo   |
| `008-decisiones`   | Parcial                   |
| `009-sprints`      | Parcial                   |

---

# 18. Próximos pasos recomendados

## 18.1 Paso inmediato

Crear los prompts operativos del volumen:

```text
docs/007-prompts/
```

Prioridad recomendada:

1. `Prompt-NewsScoutAgent.md`
2. `Prompt-SourceValidatorAgent.md`
3. `Prompt-RiskAgent.md`
4. `Prompt-EditorialAgent.md`
5. `Prompt-AuditAgent.md`
6. `Prompt-SocialClipAgent.md`
7. `Prompt-MemoryAgent.md`

---

## 18.2 Segundo paso

Crear ADRs para decisiones críticas:

```text
docs/008-decisiones/
```

Prioridad recomendada:

1. ADR-002 — XMIP como plataforma interna del newsroom.
2. ADR-003 — Human-in-the-loop para decisiones críticas.
3. ADR-004 — Memoria no es fuente factual.
4. ADR-005 — Bloqueo de publicación sin VerificationRecord.
5. ADR-006 — Agentes sin autonomía completa en MVP.

---

## 18.3 Tercer paso

Actualizar sprints:

```text
docs/009-sprints/
```

Prioridad recomendada:

1. Sprint-001 — Project Workspace Foundation.
2. Sprint-002 — Document Registry.
3. Sprint-003 — News Intake MVP.
4. Sprint-004 — Source Registry MVP.
5. Sprint-005 — Verification Workflow MVP.

---

# 19. Reglas de mantenimiento documental

## 19.1 Convención de nombres

Usar nombres de archivo sin acentos ni espacios.

Formato recomendado:

```text
ORION-###-Nombre-del-Documento.md
```

Ejemplo:

```text
ORION-022-Protocolo-de-Verificacion-Editorial.md
```

---

## 19.2 Estados documentales

| Estado     | Uso                            |
| ---------- | ------------------------------ |
| Draft      | Documento en desarrollo        |
| Review     | Documento listo para revisión |
| Approved   | Documento aprobado             |
| Deprecated | Documento reemplazado          |
| Archived   | Documento histórico           |

---

## 19.3 Versionado

| Versión | Uso                        |
| -------- | -------------------------- |
| 0.x      | Borradores tempranos       |
| 1.0      | Primera versión funcional |
| 1.x      | Cambios menores            |
| 2.0      | Cambio estructural         |

---

## 19.4 Regla de trazabilidad

Todo documento nuevo debe indicar:

* Nivel documental.
* Volumen.
* Proyecto.
* Versión.
* Estado.
* Owner.
* Última actualización.
* Ruta sugerida.
* Relación con otros documentos.
* Historial de cambios.

---

# 20. Criterios de aceptación de este índice

Este índice se considera aceptado cuando:

* [ ] Refleja la estructura actual del repositorio.
* [ ] Lista todos los documentos ORION existentes.
* [ ] Incluye el volumen `006-operaciones` completo.
* [ ] Define próximos pasos hacia `007-prompts`.
* [ ] Define próximos pasos hacia `008-decisiones`.
* [ ] Define próximos pasos hacia `009-sprints`.
* [ ] Mantiene consistencia con ORION / XCripto / XMIP.
* [ ] Usa rutas compatibles con Git.
* [ ] Evita acentos y espacios en rutas recomendadas.
* [ ] Sirve como punto de navegación del proyecto.

---

# 21. Historial de cambios

| Versión | Fecha      | Cambio                                                           | Autor            |
| -------- | ---------- | ---------------------------------------------------------------- | ---------------- |
| 1.0      | 2026-07-02 | Índice maestro actualizado con volumen 006-operaciones completo | Fernando Cuellar |
