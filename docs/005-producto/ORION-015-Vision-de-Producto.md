
# ORION-015 — Visión de Producto

**Nivel documental:** L3 — Product
**Volumen:** 005-producto
**Proyecto:** ORION / XMIP
**Versión:** 1.0
**Estado:** Draft
**Owner:** Fernando Cuellar
**Última actualización:** 2026-07-01
**Ruta sugerida:** `docs/005-producto/ORION-015-vision-de-producto.md`
**Ruta equivalente por nivel:** `docs/L3-product/ORION-015-vision-de-producto.md`

---

## 1. Propósito

Este documento define la visión de producto de XMIP dentro del marco ORION.

Su propósito es traducir la arquitectura empresarial, técnica, de datos, conocimiento y agentes en una visión clara de producto: qué problema resuelve XMIP, para quién existe, qué valor entrega, qué capacidades debe ofrecer y qué límites debe respetar.

ORION-015 responde a la pregunta:

> ¿Qué producto estamos construyendo con XMIP y por qué debe existir?

Este documento marca el inicio formal del volumen **005-producto**.

---

## 2. Alcance

Este documento cubre:

* Visión de producto.
* Problema principal.
* Usuarios objetivo.
* Propuesta de valor.
* Principios de producto.
* Capacidades producto.
* Casos de uso principales.
* Experiencia esperada.
* Diferenciadores.
* Límites del producto.
* MVP recomendado.
* Métricas de éxito.
* Riesgos de producto.
* Relación con arquitectura.
* Próximos documentos de producto.

Este documento no cubre:

* Diseño visual detallado.
* Wireframes finales.
* Backlog granular.
* Historias de usuario completas.
* Pricing.
* Go-to-market.
* Roadmap comercial.
* Implementación técnica.
* Sprints específicos.

---

## 3. Contexto

XMIP ya cuenta con una base arquitectónica documentada:

* ORION-008 — Guía de Estilo.
* ORION-009 — Principios de Arquitectura Empresarial.
* ORION-010 — Arquitectura Empresarial.
* ORION-011 — Arquitectura del Sistema.
* ORION-012 — Grafo de Conocimiento.
* ORION-013 — Modelo de Datos.
* ORION-014 — Arquitectura de Agentes.

Con esos documentos, XMIP ya no debe pensarse como una idea suelta ni como un conjunto de prompts.

A partir de ORION-015, XMIP debe entenderse como producto.

Esto significa definir:

* Qué experiencia entrega.
* Qué usuario atiende.
* Qué trabajo ayuda a realizar.
* Qué resultados produce.
* Qué valor genera.
* Qué problemas decide no resolver.
* Qué capacidades deben construirse primero.

---

## 4. Definición de producto

XMIP es una plataforma operativa multiagente para estructurar, documentar, coordinar y ejecutar trabajo estratégico, técnico y operativo con asistencia de agentes digitales gobernados.

XMIP convierte:

```text
intención + contexto + conocimiento + agentes + workflows
```

en:

```text
decisiones + documentos + análisis + ejecución trazable + memoria reutilizable
```

XMIP no es solo un chatbot.

XMIP es un sistema de trabajo asistido por agentes, diseñado para producir resultados consistentes, auditables y reutilizables.

---

## 5. Visión de producto

La visión de producto de XMIP es:

> Convertirse en una plataforma de operación intelectual aumentada, donde usuarios y agentes digitales colaboran para convertir ideas, decisiones, conocimiento y procesos en entregables estructurados, trazables y accionables.

XMIP debe permitir que una persona o equipo trabaje con una red de agentes especializados sin perder control, contexto, trazabilidad ni calidad.

La visión no es reemplazar al usuario.

La visión es darle al usuario una capa operativa de inteligencia estructurada para trabajar mejor, decidir mejor y ejecutar con menos improvisación.

---

## 6. Problema principal

El problema que XMIP resuelve es la fragmentación del trabajo intelectual y operativo.

En proyectos complejos, el conocimiento suele quedar disperso en:

* Conversaciones.
* Documentos sueltos.
* Prompts.
* Notas.
* Decisiones no registradas.
* Archivos sin gobierno.
* Herramientas desconectadas.
* Memoria humana.
* Tareas improvisadas.
* Contexto perdido entre sesiones.

Esto produce:

* Repetición de trabajo.
* Pérdida de contexto.
* Decisiones sin trazabilidad.
* Documentación inconsistente.
* Automatización frágil.
* Agentes mal definidos.
* Sprints desconectados de arquitectura.
* Dependencia excesiva de memoria personal.
* Dificultad para escalar operación.

XMIP existe para resolver ese caos.

---

## 7. Usuario objetivo

### 7.1 Usuario primario

El usuario primario de XMIP es un operador estratégico-técnico que necesita convertir ideas complejas en arquitectura, documentos, decisiones, sistemas y ejecución.

Perfil:

* Arquitecto.
* Consultor.
* Founder.
* Product Owner técnico.
* Líder de plataforma.
* Estratega de negocio.
* Operador de proyectos complejos.
* Profesional que usa IA como multiplicador de trabajo.

Este usuario no necesita otro chatbot.
Necesita un sistema que organice trabajo serio.

---

### 7.2 Usuarios secundarios

| Usuario          | Necesidad                                       |
| ---------------- | ----------------------------------------------- |
| Arquitecto       | Diseñar sistemas trazables y documentados      |
| Product Owner    | Convertir visión en funcionalidades y roadmap  |
| Consultor        | Producir entregables consistentes para clientes |
| Operador         | Ejecutar workflows repetibles                   |
| Revisor          | Validar decisiones, documentos y riesgos        |
| Desarrollador    | Implementar desde arquitectura clara            |
| Auditor          | Reconstruir decisiones, eventos y cambios       |
| Equipo ejecutivo | Entender avances, riesgos y resultados          |

---

## 8. Jobs to Be Done

XMIP debe ayudar al usuario a realizar estos trabajos.

### 8.1 Convertir ideas en documentos

Cuando el usuario tenga una idea o necesidad, XMIP debe ayudar a convertirla en un documento estructurado, versionado y alineado al marco ORION.

Ejemplo:

```text
Necesito definir la arquitectura de agentes.
→ XMIP genera ORION-014 con estructura, decisiones, riesgos y criterios.
```

---

### 8.2 Convertir arquitectura en implementación

Cuando exista arquitectura documentada, XMIP debe ayudar a derivar sprints, tareas, modelos y entregables técnicos.

Ejemplo:

```text
ORION-011 define Agent Runtime.
→ XMIP deriva SPRINT de implementación para Agent Runtime.
```

---

### 8.3 Mantener contexto entre sesiones

Cuando el usuario retome un proyecto, XMIP debe recordar decisiones, documentos, restricciones y próximos pasos relevantes.

Ejemplo:

```text
Continuemos con producto.
→ XMIP sabe que arquitectura ya está documentada y que sigue L3 Product.
```

---

### 8.4 Coordinar agentes especializados

Cuando una tarea requiera análisis, documentación, validación o revisión, XMIP debe asignar el trabajo al agente adecuado.

Ejemplo:

```text
Generar visión de producto.
→ ProductAgent usa ORION-010, ORION-011, ORION-014 y genera ORION-015.
```

---

### 8.5 Auditar decisiones

Cuando se revise un resultado, XMIP debe permitir entender qué documentos, agentes, reglas y contexto lo soportaron.

Ejemplo:

```text
¿Por qué el modelo de datos usa PostgreSQL al inicio?
→ XMIP conecta ORION-013 con la decisión arquitectónica y su justificación.
```

---

## 9. Propuesta de valor

XMIP entrega valor en cinco dimensiones.

### 9.1 Claridad

XMIP convierte ideas ambiguas en estructuras claras.

### 9.2 Continuidad

XMIP conserva contexto de proyecto, decisiones y arquitectura.

### 9.3 Trazabilidad

XMIP permite reconstruir qué se decidió, cuándo, por qué y con base en qué documentos.

### 9.4 Velocidad controlada

XMIP acelera producción de entregables sin sacrificar gobierno.

### 9.5 Escalabilidad operativa

XMIP permite pasar de trabajo individual asistido por IA a operación multiagente gobernada.

---

## 10. Declaración de posicionamiento

Para arquitectos, consultores, founders y operadores técnicos que necesitan convertir ideas complejas en sistemas, documentos y ejecución, XMIP es una plataforma multiagente gobernada que organiza contexto, agentes, conocimiento, memoria y workflows para producir entregables trazables y accionables.

A diferencia de un chatbot genérico, XMIP opera con arquitectura, documentación, memoria gobernada, agentes especializados, auditoría y control humano sobre decisiones críticas.

---

## 11. Principios de producto

### 11.1 Producto antes que herramienta

XMIP no debe sentirse como una colección de utilidades.
Debe sentirse como una plataforma coherente.

### 11.2 Resultado antes que conversación

La conversación es un medio.
El resultado es el entregable, la decisión, el documento, el workflow o la acción.

### 11.3 Trazabilidad antes que magia

El usuario debe poder entender de dónde salió un resultado.

### 11.4 Control humano en puntos críticos

XMIP puede recomendar y preparar, pero el usuario conserva control sobre decisiones críticas.

### 11.5 Documentación viva

Los documentos no son archivos muertos.
Son activos que gobiernan implementación, agentes, workflows y decisiones.

### 11.6 Agentes con límites claros

Cada agente debe tener propósito, permisos y responsabilidades definidas.

### 11.7 Memoria útil, no memoria infinita

XMIP debe recordar lo importante, no acumular basura contextual.

### 11.8 Simplicidad operativa

La experiencia debe ocultar complejidad innecesaria sin eliminar trazabilidad.

---

## 12. Capacidades de producto

### 12.1 Mapa de capacidades producto

| ID       | Capacidad                        | Descripción                                                | Prioridad |
| -------- | -------------------------------- | ----------------------------------------------------------- | --------- |
| PROD-001 | Workspace de proyecto            | Espacio central para operar proyectos ORION/XMIP            | Alta      |
| PROD-002 | Gestión documental              | Crear, editar, versionar y revisar documentos               | Alta      |
| PROD-003 | Asistencia multiagente           | Usar agentes especializados por tarea                       | Alta      |
| PROD-004 | Generación de entregables       | Crear documentos, análisis, reportes y planes              | Alta      |
| PROD-005 | Memoria de proyecto              | Mantener contexto estable del proyecto                      | Alta      |
| PROD-006 | Grafo de conocimiento visible    | Consultar relaciones entre documentos, agentes y decisiones | Media     |
| PROD-007 | Workflow execution               | Ejecutar flujos definidos con estados                       | Alta      |
| PROD-008 | Revisión y aprobación          | Aprobar documentos, decisiones y acciones críticas         | Alta      |
| PROD-009 | Auditoría de resultados         | Ver evidencia y trazabilidad de ejecuciones                 | Alta      |
| PROD-010 | Backlog derivado de arquitectura | Convertir arquitectura en tareas y sprints                  | Alta      |
| PROD-011 | Panel de agentes                 | Consultar agentes disponibles, roles y permisos             | Media     |
| PROD-012 | Panel de riesgos                 | Consultar riesgos, controles y mitigaciones                 | Media     |
| PROD-013 | Observabilidad de producto       | Ver uso, errores, costos y actividad                        | Media     |
| PROD-014 | Integración con repositorio     | Exportar y sincronizar documentos con Git                   | Alta      |
| PROD-015 | Búsqueda contextual             | Encontrar documentos, decisiones y memorias                 | Alta      |

---

## 13. Experiencia esperada

XMIP debe ofrecer una experiencia basada en trabajo guiado, no en improvisación.

### 13.1 El usuario debe poder

* Crear un proyecto.
* Consultar documentos existentes.
* Pedir un nuevo documento ORION.
* Ejecutar un workflow.
* Seleccionar o aceptar un agente recomendado.
* Ver qué contexto se usó.
* Revisar resultado.
* Aprobar o rechazar salida.
* Guardar memoria relevante.
* Registrar decisión.
* Derivar backlog.
* Exportar a Git.
* Consultar auditoría.

### 13.2 El usuario no debe tener que

* Reexplicar todo el proyecto cada vez.
* Copiar contexto manualmente entre sesiones.
* Recordar qué documento sigue.
* Inventar estructura documental.
* Buscar decisiones en conversaciones viejas.
* Confiar ciegamente en una respuesta.
* Crear sprints sin arquitectura base.
* Adivinar qué agente debe usar.

---

## 14. Experiencia narrativa del producto

La experiencia ideal de XMIP debe sentirse así:

```text
El usuario entra a XMIP.
XMIP sabe qué proyecto está activo.
XMIP muestra el estado documental.
XMIP identifica el siguiente documento recomendado.
XMIP propone el agente correcto.
XMIP genera el entregable siguiendo la guía de estilo.
XMIP relaciona el documento con arquitectura previa.
XMIP registra la decisión o salida.
XMIP propone siguientes pasos.
XMIP permite exportar a Git.
```

El usuario no está “chateando con IA”.
Está operando una plataforma de trabajo estructurado con agentes.

---

## 15. Casos de uso principales

### 15.1 Crear documento ORION

**Actor:** Owner / Architect
**Objetivo:** Crear un documento formal alineado al marco ORION.

Flujo:

1. Usuario solicita documento.
2. XMIP identifica nivel documental.
3. XMIP consulta guía de estilo.
4. XMIP consulta documentos relacionados.
5. XMIP asigna agente adecuado.
6. XMIP genera borrador.
7. Usuario revisa.
8. Documento queda listo para Git.

Resultado:

* Documento Markdown formal.
* Metadata completa.
* Relación con documentos previos.
* Criterios de aceptación.

---

### 15.2 Derivar sprint desde arquitectura

**Actor:** Architect / Operator
**Objetivo:** Convertir arquitectura aprobada en sprint ejecutable.

Flujo:

1. Usuario selecciona documento base.
2. XMIP identifica capacidades y componentes.
3. XMIP propone sprint.
4. XMIP define objetivos, tareas y criterios.
5. Usuario aprueba.
6. Sprint queda registrado.

Resultado:

* Sprint alineado a arquitectura.
* Tareas concretas.
* Criterios verificables.
* Riesgos identificados.

---

### 15.3 Consultar impacto de cambio

**Actor:** Architect / Reviewer
**Objetivo:** Saber qué documentos o componentes se afectan por un cambio.

Flujo:

1. Usuario indica posible cambio.
2. XMIP consulta grafo de conocimiento.
3. XMIP identifica dependencias.
4. XMIP lista documentos afectados.
5. XMIP propone orden de actualización.

Resultado:

* Análisis de impacto.
* Riesgos documentados.
* Plan de actualización.

---

### 15.4 Registrar decisión

**Actor:** Owner / Architect
**Objetivo:** Guardar una decisión importante con trazabilidad.

Flujo:

1. Usuario plantea decisión.
2. XMIP estructura contexto.
3. XMIP lista opciones.
4. XMIP registra decisión tomada.
5. XMIP relaciona decisión con documentos, riesgos y componentes.

Resultado:

* Decisión trazable.
* Alternativas consideradas.
* Impacto documentado.
* Relación con arquitectura.

---

### 15.5 Usar memoria de proyecto

**Actor:** Usuario / Agente
**Objetivo:** Recuperar contexto relevante.

Flujo:

1. Usuario solicita continuidad.
2. XMIP consulta memoria.
3. XMIP identifica contexto útil.
4. XMIP excluye memoria obsoleta o no autorizada.
5. XMIP responde con continuidad.

Resultado:

* Menos repetición.
* Mejor precisión.
* Continuidad operativa.

---

## 16. MVP de producto

El MVP de XMIP debe enfocarse en una cosa:

> Convertir trabajo documental y arquitectónico en entregables trazables, usando agentes especializados y memoria de proyecto.

### 16.1 MVP incluido

El MVP debe incluir:

* Workspace de proyecto.
* Registro de documentos ORION.
* Generación de documentos Markdown.
* ProductAgent / DocumentationAgent / ArchitectureAgent básicos.
* Memoria de proyecto básica.
* Grafo lógico mínimo.
* Workflow de generación documental.
* Auditoría mínima.
* Exportación manual a Git.
* Estado documental.
* Siguiente documento recomendado.

### 16.2 MVP excluido

El MVP no debe incluir todavía:

* Marketplace de agentes.
* Automatización autónoma avanzada.
* UI compleja de grafo.
* Multiusuario empresarial completo.
* Motor avanzado de permisos.
* Integraciones externas múltiples.
* Analytics sofisticado.
* Optimización avanzada de costos.
* Motor de graph database dedicado.
* Workflow builder visual.

No hace falta construir una nave espacial para validar el motor. Primero que encienda bien.

---

## 17. Producto mínimo operable

El primer producto operable debe permitir este flujo completo:

```text
Crear proyecto
→ cargar contexto base
→ consultar documentos existentes
→ solicitar nuevo documento
→ seleccionar agente
→ generar documento
→ revisar resultado
→ registrar relación documental
→ guardar memoria relevante
→ exportar Markdown
```

Si XMIP logra esto de forma consistente, ya tiene una base real.

---

## 18. Diferenciadores

XMIP se diferencia por:

### 18.1 Documentation-first

El producto genera y mantiene documentación como activo central.

### 18.2 Architecture-aware

XMIP entiende que los documentos tienen jerarquía, dependencias y consecuencias.

### 18.3 Agent governance

Los agentes tienen límites, permisos y responsabilidades.

### 18.4 Knowledge graph

El sistema puede relacionar documentos, agentes, decisiones, riesgos y workflows.

### 18.5 Memory governance

XMIP recuerda con control, no con acumulación indiscriminada.

### 18.6 Traceability

Cada resultado puede conectarse con contexto, agente, documento y decisión.

### 18.7 Human control

El usuario mantiene control sobre cambios críticos.

---

## 19. Límites del producto

XMIP no debe intentar ser todo.

### 19.1 XMIP no es

* Un chatbot genérico.
* Un reemplazo total del usuario.
* Un sistema autónomo sin supervisión.
* Un gestor de proyectos tradicional.
* Un Notion clonado.
* Un Jira clonado.
* Un repositorio de prompts sueltos.
* Un asistente casual sin estructura.
* Una plataforma de IA sin gobierno.
* Un motor de ejecución crítica sin aprobación.

### 19.2 XMIP sí es

* Plataforma multiagente gobernada.
* Sistema de documentación viva.
* Motor de workflows intelectuales.
* Memoria estructurada de proyecto.
* Capa de trazabilidad para decisiones.
* Sistema para convertir arquitectura en ejecución.
* Herramienta de operación estratégica y técnica.

---

## 20. Experiencia por módulos

### 20.1 Project Workspace

Debe mostrar:

* Proyecto activo.
* Estado documental.
* Próximo documento recomendado.
* Workflows recientes.
* Agentes disponibles.
* Decisiones recientes.
* Riesgos abiertos.
* Memorias relevantes.

### 20.2 Document Center

Debe permitir:

* Ver documentos.
* Crear documentos.
* Revisar versiones.
* Consultar estado.
* Ver dependencias.
* Exportar Markdown.
* Cambiar estado documental.

### 20.3 Agent Center

Debe permitir:

* Ver agentes disponibles.
* Consultar propósito.
* Consultar límites.
* Consultar herramientas permitidas.
* Ejecutar agente dentro de workflow.
* Ver historial de ejecuciones.

### 20.4 Workflow Center

Debe permitir:

* Ejecutar workflows.
* Ver estado.
* Ver pasos.
* Ver errores.
* Reintentar si aplica.
* Aprobar pasos humanos.
* Consultar resultado.

### 20.5 Memory Center

Debe permitir:

* Ver memoria activa.
* Proponer nueva memoria.
* Invalidar memoria.
* Ver fuente.
* Ver sensibilidad.
* Ver relación con documentos.

### 20.6 Knowledge Center

Debe permitir:

* Consultar relaciones.
* Ver dependencias.
* Ver impacto.
* Ver nodos principales.
* Ver relaciones por documento, agente o workflow.

### 20.7 Audit Center

Debe permitir:

* Ver eventos.
* Filtrar por correlation_id.
* Consultar ejecución.
* Ver agente usado.
* Ver memoria consultada.
* Ver documentos generados.

---

## 21. Métricas de éxito

### 21.1 Métricas de producto

| Métrica                          | Propósito                              |
| --------------------------------- | --------------------------------------- |
| Documentos generados              | Medir producción útil                 |
| Documentos aprobados              | Medir calidad y cierre                  |
| Tiempo por documento              | Medir eficiencia                        |
| Workflows completados             | Medir ejecución real                   |
| Workflows fallidos                | Medir fricción                         |
| Memorias reutilizadas             | Medir valor de memoria                  |
| Decisiones registradas            | Medir trazabilidad                      |
| Sprints derivados de arquitectura | Medir conexión arquitectura-ejecución |
| Rechazos por calidad              | Medir precisión de agentes             |
| Exportaciones a Git               | Medir adopción documental              |

---

### 21.2 Métricas de calidad

| Métrica                                | Propósito                   |
| --------------------------------------- | ---------------------------- |
| Documentos con metadata completa        | Calidad documental           |
| Documentos con criterios de aceptación | Capacidad de implementación |
| Relaciones documentales creadas         | Trazabilidad                 |
| Resultados con fuente identificada      | Confiabilidad                |
| Memorias con fuente                     | Gobierno de memoria          |
| Agentes usados dentro de límites       | Seguridad                    |
| Aprobaciones humanas registradas        | Control                      |
| Errores auditados                       | Operabilidad                 |

---

### 21.3 Métricas de operación

| Métrica                     | Propósito          |
| ---------------------------- | ------------------- |
| Latencia por workflow        | Desempeño          |
| Costo por ejecución         | FinOps              |
| Tokens por agente            | Control de IA       |
| Errores por agente           | Calidad operativa   |
| Reintentos                   | Estabilidad         |
| Tiempo esperando aprobación | Fricción humana    |
| Consultas al grafo           | Uso de conocimiento |
| Lecturas de memoria          | Uso de contexto     |

---

## 22. Requerimientos de producto iniciales

### 22.1 Requerimientos funcionales

| ID      | Requerimiento                                                 |
| ------- | ------------------------------------------------------------- |
| PRD-001 | El usuario debe poder crear y seleccionar un proyecto         |
| PRD-002 | El usuario debe poder ver documentos ORION existentes         |
| PRD-003 | El usuario debe poder solicitar generación de documento      |
| PRD-004 | XMIP debe recomendar el siguiente documento lógico           |
| PRD-005 | XMIP debe generar documentos en Markdown                      |
| PRD-006 | XMIP debe aplicar la guía de estilo ORION-008                |
| PRD-007 | XMIP debe relacionar documentos generados con documentos base |
| PRD-008 | XMIP debe registrar eventos de generación                    |
| PRD-009 | XMIP debe permitir guardar memoria de proyecto                |
| PRD-010 | XMIP debe permitir consultar memoria relevante                |
| PRD-011 | XMIP debe registrar decisiones importantes                    |
| PRD-012 | XMIP debe permitir exportación a repositorio                 |
| PRD-013 | XMIP debe mostrar estado de workflows                         |
| PRD-014 | XMIP debe mostrar agente usado por ejecución                 |
| PRD-015 | XMIP debe permitir aprobación humana de documentos           |

---

### 22.2 Requerimientos no funcionales

| ID      | Requerimiento                                              |
| ------- | ---------------------------------------------------------- |
| NFR-001 | Toda ejecución debe tener correlation_id                  |
| NFR-002 | Toda generación documental debe auditarse                 |
| NFR-003 | Toda memoria persistente debe tener fuente                 |
| NFR-004 | Todo documento debe tener versión y estado                |
| NFR-005 | Todo agente debe tener versión                            |
| NFR-006 | Toda acción crítica debe requerir aprobación            |
| NFR-007 | El sistema debe exportar Markdown limpio                   |
| NFR-008 | Los errores deben ser visibles y auditables                |
| NFR-009 | Los costos por ejecución deben poder registrarse          |
| NFR-010 | El producto debe operar inicialmente como monolito modular |

---

## 23. Roadmap de producto inicial

### Fase 1 — Product Foundation

Objetivo: convertir XMIP en workspace documental operable.

Incluye:

* Workspace de proyecto.
* Registro documental.
* Generación Markdown.
* Exportación manual.
* Estado documental.
* Auditoría básica.

---

### Fase 2 — Agent-Assisted Product

Objetivo: operar con agentes especializados.

Incluye:

* ProductAgent.
* DocumentationAgent.
* ArchitectureAgent.
* Agent Center básico.
* Ejecuciones trazables.
* Prompt versioning básico.

---

### Fase 3 — Workflow Product

Objetivo: convertir tareas repetibles en workflows.

Incluye:

* Workflow de generación documental.
* Workflow de revisión.
* Workflow de aprobación.
* Estados de workflow.
* Historial de ejecución.

---

### Fase 4 — Memory & Knowledge Product

Objetivo: dar continuidad y contexto estructurado.

Incluye:

* Memoria de proyecto.
* Relaciones documentales.
* Grafo lógico mínimo.
* Consulta de dependencias.
* Impact analysis básico.

---

### Fase 5 — Execution Product

Objetivo: derivar implementación desde arquitectura.

Incluye:

* Backlog derivado.
* Sprints generados desde documentos.
* Tareas técnicas.
* Criterios de aceptación.
* Relación sprint-documento.

---

### Fase 6 — Operational Product

Objetivo: operar XMIP con control.

Incluye:

* Audit Center.
* Métricas de uso.
* Costo por ejecución.
* Riesgos abiertos.
* Aprobaciones.
* Reportes operativos.

---

## 24. Riesgos de producto

| Riesgo                                       | Impacto | Probabilidad | Mitigación                                             |
| -------------------------------------------- | ------: | -----------: | ------------------------------------------------------- |
| Producto se vuelve demasiado abstracto       |    Alto |        Media | MVP enfocado en generación documental y workflows      |
| Usuario lo percibe como otro chatbot         |    Alto |        Media | Workspace, documentos, agentes y trazabilidad visibles  |
| Demasiada arquitectura antes de valor usable |   Medio |        Media | Primer flujo operable completo                          |
| Agentes generan contenido inconsistente      |    Alto |        Media | Guía de estilo, prompts versionados y revisión humana |
| Memoria guarda basura                        |    Alto |         Alta | Gobierno de memoria y fuente obligatoria                |
| Grafo no aporta valor visible                |   Medio |        Media | Usarlo primero para dependencias e impacto              |
| UI demasiado compleja                        |   Medio |        Media | Empezar con módulos mínimos                           |
| Exportación a Git se vuelve frágil         |   Medio |        Media | Markdown limpio y estructura fija                       |
| Producto intenta cubrir demasiados casos     |    Alto |        Media | Mantener foco en trabajo documental-arquitectónico     |
| Falta de métricas de uso                    |   Medio |        Media | Eventos básicos desde MVP                              |

---

## 25. Decisiones de producto iniciales

### 25.1 Iniciar con documentación y arquitectura

**Decisión:** El primer caso fuerte de XMIP será producción documental y arquitectura.

**Justificación:** Es el flujo más alineado con ORION y permite validar agentes, memoria, conocimiento, workflows y auditoría.

---

### 25.2 Markdown como formato base

**Decisión:** Los entregables oficiales se generan en Markdown.

**Justificación:** Es compatible con Git, revisión, versionado, automatización y documentación técnica.

---

### 25.3 Producto guiado por documentos ORION

**Decisión:** XMIP debe recomendar próximos documentos según la estructura ORION.

**Justificación:** Reduce improvisación y mantiene continuidad.

---

### 25.4 Agentes como capacidad visible

**Decisión:** Los agentes deben ser visibles como entidades de producto, no procesos ocultos.

**Justificación:** El usuario debe saber qué agente trabaja, qué límites tiene y qué produjo.

---

### 25.5 Aprobación humana en cambios críticos

**Decisión:** Documentos aprobados, memoria crítica y decisiones arquitectónicas requieren revisión humana.

**Justificación:** Control y trazabilidad valen más que automatización ciega.

---

## 26. Relación con arquitectura

ORION-015 se apoya directamente en la arquitectura ya definida.

| Documento | Relación con ORION-015                               |
| --------- | ----------------------------------------------------- |
| ORION-010 | Define capacidades y dominios empresariales           |
| ORION-011 | Define componentes técnicos que soportan el producto |
| ORION-012 | Define grafo para dependencias e impacto              |
| ORION-013 | Define datos persistentes del producto                |
| ORION-014 | Define agentes que ejecutan capacidades producto      |

El producto no debe contradecir la arquitectura.

Si una funcionalidad no puede mapearse a una capacidad, dominio, agente, workflow o dato, probablemente todavía no está lista para entrar al producto.

---

## 27. Relación con agentes

ORION-015 asume que la arquitectura de agentes ya está definida.

Los agentes principales para producto son:

| Agente             | Función en producto                              |
| ------------------ | ------------------------------------------------- |
| ProductAgent       | Define visión, requerimientos, roadmap y backlog |
| DocumentationAgent | Genera documentos siguiendo ORION-008             |
| ArchitectureAgent  | Valida consistencia con arquitectura              |
| KnowledgeAgent     | Relaciona documentos, decisiones y capacidades    |
| MemoryAgent        | Sugiere memoria persistente útil                 |
| AuditAgent         | Valida trazabilidad                               |
| RiskAgent          | Identifica riesgos de producto                    |
| ExecutionAgent     | Ejecuta workflows autorizados                     |

Ningún agente debe operar fuera de los límites establecidos en ORION-014.

---

## 28. Criterios de aceptación

Este documento se considera aceptado cuando:

* [ ] Define la visión de producto de XMIP.
* [ ] Define el problema principal.
* [ ] Define usuarios objetivo.
* [ ] Define Jobs to Be Done.
* [ ] Define propuesta de valor.
* [ ] Define posicionamiento.
* [ ] Define principios de producto.
* [ ] Define capacidades de producto.
* [ ] Define experiencia esperada.
* [ ] Define casos de uso principales.
* [ ] Define MVP de producto.
* [ ] Define producto mínimo operable.
* [ ] Define diferenciadores.
* [ ] Define límites del producto.
* [ ] Define módulos de experiencia.
* [ ] Define métricas de éxito.
* [ ] Define requerimientos iniciales.
* [ ] Define roadmap de producto.
* [ ] Define riesgos de producto.
* [ ] Define decisiones de producto iniciales.
* [ ] Relaciona producto con arquitectura y agentes.
* [ ] Permite derivar PRD, backlog y sprints.

---

## 29. Relación con otros documentos

Este documento se apoya en:

* ORION-008 — Guía de Estilo.
* ORION-009 — Principios de Arquitectura Empresarial.
* ORION-010 — Arquitectura Empresarial.
* ORION-011 — Arquitectura del Sistema.
* ORION-012 — Grafo de Conocimiento.
* ORION-013 — Modelo de Datos.
* ORION-014 — Arquitectura de Agentes.

Este documento gobierna directamente:

* ORION-016 — Requerimientos de Producto.
* ORION-017 — Casos de Uso.
* ORION-018 — Roadmap de Producto.
* ORION-019 — Backlog Inicial.
* ORION-020 — MVP Scope.
* L5 — Sprints de producto e implementación.

---

## 30. Próximos pasos

Después de aprobar ORION-015, continuar con:

1. ORION-016 — Requerimientos de Producto.
2. ORION-017 — Casos de Uso.
3. ORION-018 — Roadmap de Producto.
4. ORION-019 — Backlog Inicial.
5. ORION-020 — MVP Scope.

ORION-016 debe convertir esta visión en requerimientos funcionales, no funcionales, restricciones, prioridades y criterios verificables.

---

## 31. Historial de cambios

| Versión | Fecha      | Cambio                                  | Autor            |
| -------- | ---------- | --------------------------------------- | ---------------- |
| 1.0      | 2026-07-01 | Versión inicial de visión de producto | Fernando Cuellar |
