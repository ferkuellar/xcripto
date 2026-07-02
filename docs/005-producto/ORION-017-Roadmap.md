
# ORION-017 — Roadmap

**Nivel documental:** L3 — Product
**Volumen:** 005-producto
**Proyecto:** ORION / XMIP
**Versión:** 1.0
**Estado:** Draft
**Owner:** Fernando Cuellar
**Última actualización:** 2026-07-01
**Ruta sugerida:** `docs/005-producto/ORION-017-roadmap.md`
**Ruta equivalente por nivel:** `docs/L3-product/ORION-017-roadmap.md`

---

## 1. Propósito

Este documento define el roadmap de producto de XMIP.

Su propósito es ordenar la evolución del producto desde el MVP hasta una plataforma multiagente operable, trazable y preparada para implementación técnica por sprints.

ORION-017 responde a la pregunta:

> ¿En qué orden debe evolucionar XMIP para entregar valor real sin perder arquitectura, trazabilidad ni control?

Este roadmap no es una promesa comercial ni un calendario rígido.
Es una secuencia de madurez producto-arquitectura para construir XMIP con disciplina.

---

## 2. Alcance

Este documento cubre:

* Enfoque general del roadmap.
* Fases de producto.
* Releases principales.
* Capacidades por fase.
* Dependencias arquitectónicas.
* Criterios de avance.
* Gates de validación.
* Métricas de éxito.
* Riesgos por fase.
* Relación con MVP.
* Relación con sprints.
* Próximos documentos de producto.

Este documento no cubre:

* Fechas contractuales.
* Estimaciones de esfuerzo definitivas.
* Asignación de recursos.
* Diseño visual final.
* Historias de usuario detalladas.
* Implementación técnica específica.
* Costeo.
* Go-to-market.
* Pricing.
* Roadmap comercial.

---

## 3. Documentos base

Este documento se apoya en:

* ORION-008 — Guía de Estilo.
* ORION-009 — Principios de Arquitectura Empresarial.
* ORION-010 — Arquitectura Empresarial.
* ORION-011 — Arquitectura del Sistema.
* ORION-012 — Grafo de Conocimiento.
* ORION-013 — Modelo de Datos.
* ORION-014 — Arquitectura de Agentes.
* ORION-015 — Visión de Producto.
* ORION-016 — Definición del MVP.

Este documento alimenta directamente:

* ORION-018 — Casos de Uso.
* ORION-019 — Requerimientos de Producto.
* ORION-020 — Backlog Inicial.
* L5 — Sprints de implementación.

---

## 4. Contexto

XMIP ya tiene una base conceptual y arquitectónica suficientemente clara:

```text
Arquitectura empresarial
→ Arquitectura del sistema
→ Grafo de conocimiento
→ Modelo de datos
→ Arquitectura de agentes
→ Visión de producto
→ Definición del MVP
```

El siguiente riesgo es construir sin orden.

El roadmap evita tres errores clásicos:

1. Construir una demo visual sin profundidad operativa.
2. Implementar demasiada arquitectura antes de entregar valor.
3. Agregar agentes, memoria y grafo sin un flujo de producto que los justifique.

XMIP debe evolucionar por capacidades verificables, no por ocurrencias.

---

## 5. Principio rector del roadmap

El roadmap de XMIP sigue este principio:

```text
Primero flujo útil.
Luego trazabilidad.
Luego memoria.
Luego conocimiento.
Luego operación multiagente avanzada.
```

La secuencia correcta es:

```text
Workspace → Documentos → Agentes → Workflows → Memoria → Conocimiento → Auditoría → Backlog → Operación
```

XMIP debe avanzar por madurez, no por ansiedad técnica.

---

## 6. Objetivos del roadmap

El roadmap busca cumplir estos objetivos:

1. Entregar valor útil desde el MVP.
2. Validar el flujo documental ORION/XMIP.
3. Habilitar agentes especializados de forma controlada.
4. Convertir documentos en activos versionados.
5. Registrar memoria útil sin contaminar contexto.
6. Conectar documentos, decisiones, agentes y workflows.
7. Derivar backlog desde arquitectura.
8. Preparar ejecución técnica por sprints.
9. Agregar observabilidad y auditoría progresivamente.
10. Evitar sobreconstrucción prematura.

---

## 7. Modelo de evolución

XMIP evoluciona en seis fases principales.

|   Fase | Nombre                      | Objetivo                                           |
| -----: | --------------------------- | -------------------------------------------------- |
| Fase 0 | Foundation Documental       | Tener la base ORION documentada                    |
| Fase 1 | MVP Documental              | Generar y registrar documentos útiles             |
| Fase 2 | Producto Guiado por Agentes | Usar agentes especializados con control            |
| Fase 3 | Workflows y Memoria         | Convertir tareas repetibles en flujos persistentes |
| Fase 4 | Conocimiento y Trazabilidad | Conectar documentos, decisiones, memoria y agentes |
| Fase 5 | Backlog y Ejecución        | Derivar sprints desde arquitectura y producto      |
| Fase 6 | Operación Multiagente      | Operar XMIP como plataforma gobernada              |

---

## 8. Fase 0 — Foundation Documental

### 8.1 Objetivo

Establecer la base documental, estratégica y arquitectónica de XMIP antes de construir producto.

### 8.2 Estado esperado

Esta fase se considera prácticamente completada cuando existen los documentos base:

```text
ORION-008 — Guía de Estilo
ORION-009 — Principios de Arquitectura Empresarial
ORION-010 — Arquitectura Empresarial
ORION-011 — Arquitectura del Sistema
ORION-012 — Grafo de Conocimiento
ORION-013 — Modelo de Datos
ORION-014 — Arquitectura de Agentes
ORION-015 — Visión de Producto
ORION-016 — Definición del MVP
ORION-017 — Roadmap
```

### 8.3 Capacidades habilitadas

| Capacidad           | Descripción                                    |
| ------------------- | ----------------------------------------------- |
| Gobierno documental | Estructura y estilo de documentos               |
| Arquitectura base   | Empresa, sistema, datos, conocimiento y agentes |
| Visión de producto | Dirección funcional del producto               |
| MVP scope           | Alcance inicial definido                        |
| Roadmap             | Orden de evolución                             |

### 8.4 Criterios de salida

* [ ] Documentos base creados.
* [ ] Secuencia documental clara.
* [ ] Arquitectura base no contradice producto.
* [ ] MVP definido.
* [ ] Roadmap inicial aprobado.

---

## 9. Fase 1 — MVP Documental

### 9.1 Objetivo

Construir el primer flujo útil de XMIP:

```text
Proyecto → Documento → Agente → Markdown → Registro → Exportación
```

El objetivo de esta fase no es construir toda la plataforma.
El objetivo es demostrar que XMIP puede producir entregables estructurados y reutilizables.

### 9.2 Capacidades incluidas

| ID         | Capacidad                       | Prioridad |
| ---------- | ------------------------------- | --------- |
| F1-CAP-001 | Project Workspace básico       | Alta      |
| F1-CAP-002 | Document Registry               | Alta      |
| F1-CAP-003 | Document Generator              | Alta      |
| F1-CAP-004 | Markdown Export                 | Alta      |
| F1-CAP-005 | Estado documental               | Alta      |
| F1-CAP-006 | Siguiente documento recomendado | Alta      |
| F1-CAP-007 | Audit Log básico               | Alta      |

### 9.3 Entregables

* Workspace básico del proyecto.
* Registro de documentos.
* Generador de documentos Markdown.
* Exportación `.md`.
* Historial básico de actividad.
* Estado documental.
* Recomendación del próximo documento.

### 9.4 Flujo validado

```text
Abrir proyecto
→ ver documentos existentes
→ seleccionar siguiente documento
→ generar Markdown
→ revisar contenido
→ registrar documento
→ exportar archivo
```

### 9.5 Criterios de salida

* [ ] El usuario puede crear o seleccionar proyecto.
* [ ] El usuario puede ver documentos existentes.
* [ ] XMIP recomienda el siguiente documento.
* [ ] XMIP genera documento Markdown completo.
* [ ] El documento tiene metadata estándar.
* [ ] El documento puede exportarse limpio.
* [ ] La generación queda registrada.
* [ ] El flujo completo funciona sin intervención manual fuera del sistema.

---

## 10. Fase 2 — Producto Guiado por Agentes

### 10.1 Objetivo

Incorporar agentes especializados como entidades visibles y controladas dentro del producto.

El usuario debe saber:

* Qué agente está trabajando.
* Qué responsabilidad tiene.
* Qué documento produce.
* Qué límite tiene.
* Qué salida generó.

### 10.2 Capacidades incluidas

| ID         | Capacidad                          | Prioridad |
| ---------- | ---------------------------------- | --------- |
| F2-CAP-001 | Agent Registry MVP                 | Alta      |
| F2-CAP-002 | ProductAgent                       | Alta      |
| F2-CAP-003 | DocumentationAgent                 | Alta      |
| F2-CAP-004 | ArchitectureAgent                  | Alta      |
| F2-CAP-005 | Agent Execution Log                | Alta      |
| F2-CAP-006 | Prompt version básico             | Media     |
| F2-CAP-007 | Selección de agente por documento | Alta      |

### 10.3 Agentes iniciales

| Agente             | Uso                              |
| ------------------ | -------------------------------- |
| ProductAgent       | Documentos L3 de producto        |
| DocumentationAgent | Estilo, estructura y formato     |
| ArchitectureAgent  | Consistencia con L2 Architecture |
| MemoryAgent        | Propuesta de memoria             |
| KnowledgeAgent     | Relaciones documentales básicas |

### 10.4 Entregables

* Catálogo de agentes.
* Vista básica de agente.
* Ejecución registrada por agente.
* Asignación de agente por tipo de documento.
* Versionado básico de prompt o plantilla.
* Registro de salida por agente.

### 10.5 Criterios de salida

* [ ] Cada generación registra agente usado.
* [ ] Cada agente tiene propósito visible.
* [ ] Cada agente tiene versión.
* [ ] Cada agente tiene límites básicos.
* [ ] ProductAgent puede generar documentos L3.
* [ ] DocumentationAgent aplica estructura ORION.
* [ ] ArchitectureAgent detecta contradicciones básicas.
* [ ] El usuario puede ver historial de ejecuciones por agente.

---

## 11. Fase 3 — Workflows y Memoria

### 11.1 Objetivo

Convertir acciones repetibles en workflows y permitir continuidad básica mediante memoria gobernada.

El producto debe dejar de ser solo generación puntual y comenzar a operar como sistema.

### 11.2 Capacidades incluidas

| ID         | Capacidad              | Prioridad |
| ---------- | ---------------------- | --------- |
| F3-CAP-001 | Workflow Run MVP       | Alta      |
| F3-CAP-002 | Workflow status        | Alta      |
| F3-CAP-003 | Workflow step tracking | Media     |
| F3-CAP-004 | Project Memory MVP     | Alta      |
| F3-CAP-005 | Memory approval        | Alta      |
| F3-CAP-006 | Memory invalidation    | Media     |
| F3-CAP-007 | Context reuse          | Alta      |

### 11.3 Workflows iniciales

```text
wf_generate_orion_document
wf_register_document
wf_save_project_memory
wf_export_markdown_document
wf_update_document_status
```

### 11.4 Memoria inicial

Tipos de memoria permitidos:

```text
project_memory
document_memory
architecture_memory
product_memory
```

### 11.5 Entregables

* Workflows con estado.
* Historial de workflow runs.
* Memoria de proyecto.
* Aprobación manual de memoria.
* Reutilización de contexto en nuevas generaciones.
* Registro de memoria usada.

### 11.6 Criterios de salida

* [ ] Toda generación ocurre dentro de un workflow.
* [ ] Todo workflow tiene estado.
* [ ] Todo workflow tiene correlation_id.
* [ ] El usuario puede guardar memoria útil.
* [ ] Toda memoria tiene fuente.
* [ ] El usuario puede invalidar memoria.
* [ ] Nuevos documentos pueden usar memoria aprobada.
* [ ] Se registra qué memoria fue usada.

---

## 12. Fase 4 — Conocimiento y Trazabilidad

### 12.1 Objetivo

Activar el grafo lógico de conocimiento para conectar documentos, decisiones, agentes, memoria y workflows.

En esta fase XMIP empieza a “entender” relaciones, no solo a almacenar archivos.

### 12.2 Capacidades incluidas

| ID         | Capacidad               | Prioridad |
| ---------- | ----------------------- | --------- |
| F4-CAP-001 | Knowledge Nodes MVP     | Alta      |
| F4-CAP-002 | Knowledge Edges MVP     | Alta      |
| F4-CAP-003 | Document relationships  | Alta      |
| F4-CAP-004 | Impact analysis básico | Media     |
| F4-CAP-005 | Decision registry       | Alta      |
| F4-CAP-006 | Risk-control links      | Media     |
| F4-CAP-007 | Knowledge query básico | Media     |

### 12.3 Relaciones iniciales

```text
governs
depends_on
references
defines
implements
uses
produces
derived_from
mitigated_by
approved_by
```

### 12.4 Consultas mínimas

XMIP debe poder responder:

```text
¿Qué documentos dependen de ORION-015?
¿Qué documentos gobiernan ORION-016?
¿Qué agente generó este documento?
¿Qué memoria se usó?
¿Qué decisión afecta este componente?
¿Qué sprint implementa esta capacidad?
```

### 12.5 Entregables

* Nodos básicos del grafo.
* Relaciones entre documentos.
* Relaciones entre documento y agente.
* Relaciones entre documento y memoria.
* Registro de decisiones.
* Vista básica de dependencias.
* Consulta de impacto básica.

### 12.6 Criterios de salida

* [ ] Todo documento nuevo crea nodo de conocimiento.
* [ ] Todo documento nuevo tiene al menos una relación.
* [ ] Toda relación tiene fuente.
* [ ] El usuario puede ver dependencias documentales.
* [ ] El sistema puede hacer análisis de impacto básico.
* [ ] Las decisiones importantes quedan registradas.
* [ ] La auditoría puede conectarse con documentos y workflows.

---

## 13. Fase 5 — Backlog y Ejecución

### 13.1 Objetivo

Convertir arquitectura y producto en backlog implementable.

Esta fase conecta L2 Architecture y L3 Product con L5 Sprints.

### 13.2 Capacidades incluidas

| ID         | Capacidad                 | Prioridad |
| ---------- | ------------------------- | --------- |
| F5-CAP-001 | Backlog inicial           | Alta      |
| F5-CAP-002 | Épicas                   | Alta      |
| F5-CAP-003 | Historias de usuario      | Alta      |
| F5-CAP-004 | Tareas técnicas          | Alta      |
| F5-CAP-005 | Criterios de aceptación  | Alta      |
| F5-CAP-006 | Trazabilidad a documentos | Alta      |
| F5-CAP-007 | Sprint planning básico   | Alta      |
| F5-CAP-008 | Priorización             | Media     |

### 13.3 Entregables

* ORION-020 — Backlog Inicial.
* Épicas del MVP.
* Historias de usuario.
* Tareas técnicas.
* Criterios de aceptación.
* Sprints derivados.
* Relación historia-documento.
* Relación sprint-capacidad.

### 13.4 Criterios de salida

* [ ] Cada épica referencia documento base.
* [ ] Cada historia tiene criterio de aceptación.
* [ ] Cada tarea técnica se conecta con arquitectura.
* [ ] Cada sprint implementa una capacidad.
* [ ] El backlog puede ejecutarse sin reinterpretar la visión.
* [ ] El MVP puede planearse en sprints L5.

---

## 14. Fase 6 — Operación Multiagente

### 14.1 Objetivo

Evolucionar XMIP hacia una plataforma operable con agentes, workflows, memoria, conocimiento, auditoría y observabilidad.

Esta fase ya no valida solo el producto documental.
Valida la plataforma completa.

### 14.2 Capacidades incluidas

| ID         | Capacidad               | Prioridad |
| ---------- | ----------------------- | --------- |
| F6-CAP-001 | Multi-agent workflows   | Alta      |
| F6-CAP-002 | Human approval gates    | Alta      |
| F6-CAP-003 | Audit Center            | Alta      |
| F6-CAP-004 | Observability dashboard | Media     |
| F6-CAP-005 | Cost tracking           | Media     |
| F6-CAP-006 | Risk panel              | Media     |
| F6-CAP-007 | Git integration         | Alta      |
| F6-CAP-008 | Policy engine básico   | Alta      |
| F6-CAP-009 | Agent permissions       | Alta      |
| F6-CAP-010 | Knowledge UI avanzada   | Media     |

### 14.3 Entregables

* Workflows multiagente.
* Aprobaciones humanas.
* Permisos por agente.
* Audit Center.
* Cost tracking.
* Git integration.
* Panel de riesgos.
* Observabilidad básica.
* Políticas activas.
* Operación gobernada.

### 14.4 Criterios de salida

* [ ] Los agentes operan con permisos definidos.
* [ ] Acciones críticas requieren aprobación.
* [ ] El sistema registra auditoría completa.
* [ ] El usuario puede rastrear costo básico.
* [ ] Los documentos pueden sincronizarse con Git.
* [ ] El grafo ayuda a detectar impacto.
* [ ] Los workflows multiagente producen resultados trazables.
* [ ] El sistema puede operar más allá de generación documental.

---

## 15. Releases sugeridos

El roadmap puede agruparse en releases.

| Release | Nombre                    | Contenido principal                    |
| ------- | ------------------------- | -------------------------------------- |
| R0      | ORION Foundation          | Documentos base y arquitectura         |
| R1      | XMIP MVP Documental       | Workspace, documentos, Markdown export |
| R2      | Agent-Assisted XMIP       | Agentes visibles y ejecuciones         |
| R3      | Workflow & Memory XMIP    | Workflows, estados y memoria           |
| R4      | Knowledge XMIP            | Grafo lógico y trazabilidad           |
| R5      | Execution XMIP            | Backlog y sprints derivados            |
| R6      | Governed Multi-Agent XMIP | Operación multiagente gobernada       |

---

## 16. Roadmap resumido

```text
R0 — ORION Foundation
    ↓
R1 — MVP Documental
    ↓
R2 — Agentes visibles
    ↓
R3 — Workflows + memoria
    ↓
R4 — Grafo + trazabilidad
    ↓
R5 — Backlog + sprints
    ↓
R6 — Operación multiagente gobernada
```

La secuencia es deliberada.

No tiene sentido meter operación multiagente avanzada si todavía no existe un flujo documental estable.
No tiene sentido meter grafo visual si todavía no hay relaciones útiles.
No tiene sentido meter backlog si la arquitectura y el producto no están cerrados.

---

## 17. Dependencias principales

| Fase   | Depende de                   |
| ------ | ---------------------------- |
| Fase 1 | ORION-015, ORION-016         |
| Fase 2 | ORION-014, Fase 1            |
| Fase 3 | ORION-011, ORION-013, Fase 2 |
| Fase 4 | ORION-012, ORION-013, Fase 3 |
| Fase 5 | ORION-015, ORION-016, Fase 4 |
| Fase 6 | ORION-011, ORION-014, Fase 5 |

---

## 18. Gates de validación

Cada fase debe pasar un gate antes de avanzar.

### 18.1 Gate R1 — MVP Documental

Preguntas:

* ¿El usuario puede generar un documento útil?
* ¿El documento puede copiarse a Git?
* ¿La estructura es consistente?
* ¿El sistema registra actividad básica?
* ¿El usuario entiende cuál es el siguiente paso?

No avanzar si el producto todavía depende de copiar y pegar contexto manualmente en exceso.

---

### 18.2 Gate R2 — Agentes

Preguntas:

* ¿Cada agente tiene propósito claro?
* ¿El usuario sabe qué agente produjo qué?
* ¿Los agentes tienen límites?
* ¿Hay registro de ejecución?
* ¿La salida mejora por especialización?

No avanzar si los agentes son solo nombres bonitos encima del mismo prompt genérico.

---

### 18.3 Gate R3 — Workflows y memoria

Preguntas:

* ¿Los workflows tienen estado?
* ¿La memoria tiene fuente?
* ¿La memoria se reutiliza de forma útil?
* ¿La memoria puede invalidarse?
* ¿El usuario repite menos contexto?

No avanzar si la memoria empieza a ensuciar el sistema.

---

### 18.4 Gate R4 — Conocimiento

Preguntas:

* ¿Las relaciones ayudan a tomar decisiones?
* ¿El sistema puede mostrar dependencias?
* ¿El grafo tiene fuentes?
* ¿Hay análisis de impacto básico?
* ¿Las relaciones se conectan con documentos reales?

No avanzar si el grafo solo se ve bonito pero no sirve para operar.

---

### 18.5 Gate R5 — Backlog

Preguntas:

* ¿Cada épica deriva de arquitectura o producto?
* ¿Cada historia tiene criterio de aceptación?
* ¿Cada sprint tiene capacidad asociada?
* ¿El equipo puede implementar sin reinterpretar documentos?
* ¿Hay trazabilidad desde backlog a ORION?

No avanzar si el backlog parece lista de deseos.

---

### 18.6 Gate R6 — Operación

Preguntas:

* ¿Los agentes respetan permisos?
* ¿Las acciones críticas tienen aprobación?
* ¿Los costos son visibles?
* ¿La auditoría reconstruye ejecuciones?
* ¿El sistema puede operar con fallos controlados?

No avanzar si la plataforma es poderosa pero opaca. Eso no es madurez; es riesgo con interfaz.

---

## 19. Roadmap por capacidades

| Capacidad          |           R1 |         R2 |           R3 |             R4 |               R5 |           R6 |
| ------------------ | -----------: | ---------: | -----------: | -------------: | ---------------: | -----------: |
| Workspace          |      Básico |   Mejorado |     Mejorado |       Mejorado |         Completo |     Completo |
| Document Registry  |      Básico |   Mejorado |     Mejorado | Con relaciones |         Completo |     Completo |
| Document Generator |      Básico | Por agente | Por workflow |       Trazable |         Completo |     Completo |
| Agent Registry     |           No |    Básico |     Mejorado |    Relacionado |         Completo |    Gobernado |
| Workflows          |       Manual |    Básico | Completo MVP |    Relacionado |     Sprint-ready |  Multiagente |
| Memory             | No / mínima |  Propuesta |          MVP |    Relacionada | Usada en backlog |    Gobernada |
| Knowledge Graph    | No / mínimo |    Mínimo |      Básico |   MVP completo |   Backlog linked |     Avanzado |
| Audit              |      Básico | Por agente | Por workflow |     Semántico |    Sprint-linked |  Operacional |
| Git Export         |       Manual |     Manual |       Manual |         Manual |         Mejorado | Integración |
| Observability      |         Logs |       Logs |      Básica |        Básica |           Costos |    Dashboard |
| Backlog            |           No |         No |           No |        Inicial |         Completo |     Operable |

---

## 20. Roadmap por documentos producto

| Documento                               | Fase       | Propósito                         |
| --------------------------------------- | ---------- | ---------------------------------- |
| ORION-015 — Visión de Producto        | Fase 0     | Define dirección del producto     |
| ORION-016 — Definición del MVP        | Fase 0     | Define alcance inicial             |
| ORION-017 — Roadmap                    | Fase 0     | Define evolución                  |
| ORION-018 — Casos de Uso               | Fase 1     | Define interacciones principales   |
| ORION-019 — Requerimientos de Producto | Fase 1     | Define requerimientos verificables |
| ORION-020 — Backlog Inicial            | Fase 5     | Define trabajo implementable       |
| ORION-021 — Historias de Usuario       | Fase 5     | Detalla historias por épica       |
| ORION-022 — Criterios de Aceptación   | Fase 5     | Estandariza validación            |
| ORION-023 — UX Conceptual              | Fase 1 / 2 | Define experiencia mínima         |
| ORION-024 — Métricas de Producto      | Fase 3 / 4 | Define medición                   |

---

## 21. Sprints derivados sugeridos

El roadmap puede traducirse inicialmente en estos sprints L5.

### 21.1 Sprints para R1 — MVP Documental

```text
SPRINT-001 — Project Workspace Foundation
SPRINT-002 — Document Registry
SPRINT-003 — Markdown Document Generator
SPRINT-004 — Markdown Export
SPRINT-005 — Activity Log MVP
SPRINT-006 — MVP Documental End-to-End
```

### 21.2 Sprints para R2 — Agentes

```text
SPRINT-007 — Agent Registry MVP
SPRINT-008 — ProductAgent Integration
SPRINT-009 — DocumentationAgent Integration
SPRINT-010 — ArchitectureAgent Validation
SPRINT-011 — Agent Execution Log
```

### 21.3 Sprints para R3 — Workflows y memoria

```text
SPRINT-012 — Workflow Runtime MVP
SPRINT-013 — Workflow Status Tracking
SPRINT-014 — Project Memory MVP
SPRINT-015 — Memory Approval Flow
SPRINT-016 — Context Reuse MVP
```

### 21.4 Sprints para R4 — Conocimiento y trazabilidad

```text
SPRINT-017 — Knowledge Nodes MVP
SPRINT-018 — Knowledge Edges MVP
SPRINT-019 — Document Dependency View
SPRINT-020 — Decision Registry
SPRINT-021 — Impact Analysis MVP
```

### 21.5 Sprints para R5 — Backlog y ejecución

```text
SPRINT-022 — Epic Model
SPRINT-023 — User Story Model
SPRINT-024 — Backlog Generation
SPRINT-025 — Sprint Planning MVP
SPRINT-026 — Traceability Backlog-to-Architecture
```

### 21.6 Sprints para R6 — Operación multiagente

```text
SPRINT-027 — Human Approval Gates
SPRINT-028 — Agent Permissions MVP
SPRINT-029 — Audit Center
SPRINT-030 — Cost Tracking MVP
SPRINT-031 — Git Integration MVP
SPRINT-032 — Governed Multi-Agent Workflow
```

---

## 22. Priorización

La priorización del roadmap sigue este orden:

1. Flujo documental útil.
2. Exportación Markdown.
3. Registro de documentos.
4. Agentes especializados.
5. Workflows con estado.
6. Memoria gobernada.
7. Relaciones de conocimiento.
8. Auditoría extendida.
9. Backlog derivado.
10. Integraciones.
11. Observabilidad avanzada.
12. Automatización multiagente avanzada.

La regla es simple:

> Lo que no mejora el flujo principal del MVP no entra primero.

---

## 23. Métricas por fase

### 23.1 Fase 1 — MVP Documental

| Métrica                         |          Meta |
| -------------------------------- | ------------: |
| Documentos generados             |           10+ |
| Documentos exportados            |          80%+ |
| Documentos con metadata completa |          100% |
| Errores críticos de generación | 0 bloqueantes |
| Tiempo contra generación manual |         Menor |

---

### 23.2 Fase 2 — Agentes

| Métrica                                 |         Meta |
| ---------------------------------------- | -----------: |
| Ejecuciones con agente registrado        |         100% |
| Agentes con propósito definido          |         100% |
| Agentes con versión                     |         100% |
| Documentos generados por agente correcto |         90%+ |
| Rechazos por inconsistencia              | Menos de 20% |

---

### 23.3 Fase 3 — Workflows y memoria

| Métrica                           |                   Meta |
| ---------------------------------- | ---------------------: |
| Workflows con estado               |                   100% |
| Workflows con correlation_id       |                   100% |
| Memorias con fuente                |                   100% |
| Memorias reutilizadas              |                     5+ |
| Memorias invalidadas correctamente | 100% de casos manuales |

---

### 23.4 Fase 4 — Conocimiento

| Métrica                           | Meta |
| ---------------------------------- | ---: |
| Documentos con relaciones          | 90%+ |
| Relaciones con fuente              | 100% |
| Nodos huérfanos críticos         |    0 |
| Consultas de impacto exitosas      | 80%+ |
| Decisiones conectadas a documentos | 80%+ |

---

### 23.5 Fase 5 — Backlog

| Métrica                                   | Meta |
| ------------------------------------------ | ---: |
| Épicas con documento base                 | 100% |
| Historias con aceptación                  | 100% |
| Sprints con capacidad asociada             | 100% |
| Tareas técnicas conectadas a arquitectura | 90%+ |
| Backlog listo para ejecución              |  Sí |

---

### 23.6 Fase 6 — Operación

| Métrica                           | Meta |
| ---------------------------------- | ---: |
| Acciones críticas con aprobación | 100% |
| Ejecuciones auditables             | 100% |
| Costos visibles por agente         | 80%+ |
| Errores con código y trazabilidad | 100% |
| Workflows multiagente exitosos     | 80%+ |

---

## 24. Riesgos del roadmap

| Riesgo                             | Impacto | Probabilidad | Mitigación                                     |
| ---------------------------------- | ------: | -----------: | ----------------------------------------------- |
| Saltar directo a agentes avanzados |    Alto |        Media | Respetar fases R1-R3                            |
| Construir UI antes de flujo        |    Alto |        Media | Validar flujo end-to-end primero                |
| Grafo sin utilidad práctica       |   Medio |        Media | Usar relaciones para impacto y dependencias     |
| Memoria contaminada                |    Alto |         Alta | Aprobación e invalidación manual              |
| Roadmap demasiado ambicioso        |   Medio |         Alta | Gates estrictos por release                     |
| Backlog sin trazabilidad           |    Alto |        Media | Conectar historias a documentos                 |
| Agentes genéricos disfrazados     |    Alto |        Media | Definir propósito y límites                   |
| Auditoría tardía                 |    Alto |        Media | Audit básico desde R1                          |
| Costos invisibles                  |   Medio |        Media | Cost tracking desde R6, medición básica antes |
| Automatización prematura          |    Alto |        Media | Human approval gates                            |

---

## 25. Decisiones de roadmap

### 25.1 Primero documentación, después automatización

**Decisión:** El roadmap inicia con documentación operable.

**Justificación:** XMIP es documentation-first. Automatizar antes de documentar produciría caos más rápido.

---

### 25.2 Agentes visibles antes que multiagente avanzado

**Decisión:** Primero se implementan agentes individuales con propósito visible.

**Justificación:** Un sistema multiagente sin agentes bien definidos es solo ruido coordinado.

---

### 25.3 Grafo lógico antes que visualización avanzada

**Decisión:** Primero se implementan relaciones útiles; después visualización.

**Justificación:** Un grafo bonito sin relaciones confiables no sirve.

---

### 25.4 Backlog después de producto y arquitectura

**Decisión:** El backlog se deriva después de visión, MVP y roadmap.

**Justificación:** El backlog debe ejecutar intención documentada, no sustituirla.

---

### 25.5 Operación gobernada al final del primer ciclo

**Decisión:** La operación multiagente avanzada llega después de validar flujo, agentes, memoria y conocimiento.

**Justificación:** No se gobierna bien lo que todavía no existe.

---

## 26. Antipatrones prohibidos

El roadmap debe evitar:

* Tratar fases como menú libre.
* Construir backlog antes de cerrar MVP.
* Crear UI de grafo sin datos útiles.
* Implementar agentes sin registry.
* Implementar memoria sin fuente.
* Implementar workflows sin estado.
* Generar documentos sin exportación.
* Meter Git integration antes de validar Markdown export.
* Agregar multiusuario antes de uso individual sólido.
* Construir dashboards antes de tener eventos confiables.
* Llamar MVP a una maqueta que no produce documentos reutilizables.

---

## 27. Relación con arquitectura

| Documento | Uso dentro del roadmap                  |
| --------- | --------------------------------------- |
| ORION-010 | Define capacidades empresariales        |
| ORION-011 | Define componentes técnicos por fase   |
| ORION-012 | Habilita Fase 4 de conocimiento         |
| ORION-013 | Define datos mínimos para cada release |
| ORION-014 | Habilita Fase 2 y Fase 6 de agentes     |
| ORION-015 | Define dirección producto              |
| ORION-016 | Define alcance MVP                      |

---

## 28. Relación con próximos documentos

Este roadmap deja preparado el siguiente bloque documental:

```text
ORION-018 — Casos de Uso
ORION-019 — Requerimientos de Producto
ORION-020 — Backlog Inicial
```

Secuencia recomendada:

1. **ORION-018 — Casos de Uso**
   Define cómo los usuarios interactúan con XMIP.
2. **ORION-019 — Requerimientos de Producto**
   Convierte visión, MVP y roadmap en requerimientos funcionales y no funcionales.
3. **ORION-020 — Backlog Inicial**
   Convierte requerimientos en épicas, historias y tareas.

---

## 29. Criterios de aceptación

Este documento se considera aceptado cuando:

* [ ] Define el objetivo del roadmap.
* [ ] Define fases de evolución.
* [ ] Define releases principales.
* [ ] Define capacidades por fase.
* [ ] Define entregables por fase.
* [ ] Define criterios de salida por fase.
* [ ] Define gates de validación.
* [ ] Define dependencias principales.
* [ ] Define roadmap por capacidades.
* [ ] Define roadmap por documentos.
* [ ] Define sprints derivados sugeridos.
* [ ] Define métricas por fase.
* [ ] Define riesgos y mitigaciones.
* [ ] Define decisiones de roadmap.
* [ ] Evita saltos prematuros de alcance.
* [ ] Permite derivar casos de uso, requerimientos y backlog.

---

## 30. Próximos pasos

Después de aprobar ORION-017, continuar con:

1. ORION-018 — Casos de Uso.
2. ORION-019 — Requerimientos de Producto.
3. ORION-020 — Backlog Inicial.

ORION-018 debe definir los casos de uso principales del MVP y de las siguientes fases: actores, precondiciones, flujo principal, flujos alternos, errores y criterios de aceptación.

---

## 31. Historial de cambios

| Versión | Fecha      | Cambio                                   | Autor            |
| -------- | ---------- | ---------------------------------------- | ---------------- |
| 1.0      | 2026-07-01 | Versión inicial del roadmap de producto | Fernando Cuellar |
