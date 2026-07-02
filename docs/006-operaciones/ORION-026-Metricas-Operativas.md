# ORION-026 — Métricas Operativas

**Nivel documental:** L4 — Operations
**Volumen:** 006-operaciones
**Proyecto:** ORION / XCripto / XMIP
**Versión:** 1.0
**Estado:** Draft
**Owner:** Fernando Cuellar
**Última actualización:** 2026-07-02
**Ruta sugerida:** `docs/006-operaciones/ORION-026-Metricas-Operativas.md`

---

## 1. Propósito

Este documento define el modelo de métricas operativas de XCripto.

Su propósito es establecer cómo medir el desempeño del newsroom, la calidad editorial, la velocidad de producción, la confiabilidad de fuentes, la verificación, la publicación, la distribución multicanal, el aprendizaje editorial y la operación de agentes dentro de XMIP.

ORION-026 responde a la pregunta:

> ¿Cómo sabe XCripto si su operación editorial está funcionando bien?

Las métricas operativas no existen para inflar dashboards.
Existen para tomar mejores decisiones, detectar fallas, mejorar calidad y operar el newsroom con disciplina.

---

## 2. Alcance

Este documento cubre:

* Principios de medición.
* Categorías de métricas.
* Métricas de intake.
* Métricas de fuentes.
* Métricas de verificación.
* Métricas de producción.
* Métricas de publicación.
* Métricas de distribución.
* Métricas de audiencia.
* Métricas de calidad editorial.
* Métricas de agentes.
* Métricas de memoria.
* Métricas de incidentes.
* Métricas de calendario.
* Métricas ejecutivas.
* Datos mínimos en XMIP.
* Eventos.
* Dashboards recomendados.
* Alertas operativas.
* Riesgos.
* Criterios de aceptación.

Este documento no cubre en detalle:

* Flujo completo de producción.
* Gestión de fuentes.
* Verificación editorial.
* Distribución multicanal.
* Gestión de incidentes.
* Operación específica de agentes.

Esos temas se desarrollan en:

* ORION-020 — Runbook de Producción de Noticias.
* ORION-021 — Gestión de Fuentes.
* ORION-022 — Protocolo de Verificación Editorial.
* ORION-023 — Pipeline del Newsroom.
* ORION-024 — Calendario Editorial.
* ORION-025 — Distribución Multicanal.
* ORION-027 — Gestión de Incidentes Editoriales.
* ORION-028 — Operación de Agentes Editoriales.

---

## 3. Documentos base

Este documento se apoya en:

* ORION-005 — Constitución Editorial.
* ORION-006 — Estándares Editoriales.
* ORION-007 — Flujo Editorial.
* ORION-018 — Operaciones Diarias.
* ORION-019 — Flujo de Publicación.
* ORION-020 — Runbook de Producción de Noticias.
* ORION-021 — Gestión de Fuentes.
* ORION-022 — Protocolo de Verificación Editorial.
* ORION-023 — Pipeline del Newsroom.
* ORION-024 — Calendario Editorial.
* ORION-025 — Distribución Multicanal.

Este documento gobierna directamente:

* ORION-027 — Gestión de Incidentes Editoriales.
* ORION-028 — Operación de Agentes Editoriales.
* ORION-029 — Checklist Diario del Newsroom.

---

## 4. Contexto operativo

XCripto necesita medir su operación para evitar que el newsroom funcione por percepción.

Sin métricas, el equipo puede creer que está publicando bien solo porque publica mucho.

Pero una agencia de noticias cripto debe medir más que volumen.

Debe medir:

```text
calidad
velocidad
precisión
fuentes
verificación
riesgo
alcance
retención
distribución
aprendizaje
incidentes
agentes
```

El objetivo no es perseguir vanity metrics.

El objetivo es construir una operación editorial confiable.

---

## 5. Principio rector de métricas

Las métricas operativas de XCripto siguen este principio:

```text
Medir lo que mejora confianza, calidad, velocidad y aprendizaje editorial.
```

Las métricas deben ayudar a responder:

* ¿Estamos detectando buenas noticias?
* ¿Estamos filtrando ruido?
* ¿Estamos verificando correctamente?
* ¿Estamos publicando a tiempo?
* ¿Estamos cometiendo errores?
* ¿Qué canales funcionan?
* ¿Qué fuentes son confiables?
* ¿Qué agentes ayudan realmente?
* ¿Qué piezas generan valor?
* ¿Qué debemos dejar de hacer?

---

## 6. Objetivos de medición

El sistema de métricas debe permitir:

1. Medir productividad editorial.
2. Medir calidad de fuentes.
3. Medir eficacia de verificación.
4. Medir velocidad del pipeline.
5. Medir cumplimiento del calendario.
6. Medir desempeño por canal.
7. Medir engagement de audiencia.
8. Medir errores y correcciones.
9. Medir incidentes editoriales.
10. Medir operación de agentes.
11. Medir aprendizaje editorial.
12. Detectar cuellos de botella.
13. Alimentar decisiones de roadmap.
14. Mejorar el newsroom de forma continua.

---

## 7. Categorías de métricas

Las métricas se organizan en 12 categorías.

| Categoría        | Propósito                            |
| ----------------- | ------------------------------------- |
| Intake            | Medir señales y noticias detectadas  |
| Fuentes           | Medir confiabilidad y uso de fuentes  |
| Verificación     | Medir rigor editorial                 |
| Producción       | Medir creación de contenido          |
| Publicación      | Medir salida real                     |
| Distribución     | Medir adaptación multicanal          |
| Audiencia         | Medir respuesta del público          |
| Calidad editorial | Medir precisión y consistencia       |
| Calendario        | Medir cumplimiento de agenda          |
| Agentes           | Medir desempeño operativo de agentes |
| Memoria           | Medir aprendizaje reutilizable        |
| Incidentes        | Medir fallas y riesgos                |

---

# 8. Métricas de intake

## 8.1 Objetivo

Medir la capacidad del newsroom para detectar señales relevantes y convertirlas en noticias candidatas.

## 8.2 Métricas principales

| Métrica                        | Definición                     | Uso                                   |
| ------------------------------- | ------------------------------- | ------------------------------------- |
| `signals_detected`            | Señales detectadas             | Medir volumen de monitoreo            |
| `news_items_created`          | Noticias registradas            | Medir conversión de señal a noticia |
| `signals_rejected`            | Señales descartadas            | Medir ruido                           |
| `duplicate_signals`           | Señales duplicadas             | Medir eficiencia de intake            |
| `signals_by_category`         | Señales por categoría         | Detectar concentración temática     |
| `signals_by_source_type`      | Señales por tipo de fuente     | Medir exposición a fuentes           |
| `intake_to_registration_time` | Tiempo de detección a registro | Medir velocidad de captura            |

## 8.3 Metas iniciales

| Métrica                           | Meta inicial |
| ---------------------------------- | -----------: |
| Señales con fuente registrada     |         100% |
| Señales con categoría preliminar |         100% |
| Señales duplicadas no detectadas  |  0 críticas |
| Señales sin correlation_id        |            0 |

---

# 9. Métricas de fuentes

## 9.1 Objetivo

Medir calidad, confiabilidad, uso y riesgo de las fuentes del newsroom.

## 9.2 Métricas principales

| Métrica                          | Definición                            | Uso                           |
| --------------------------------- | -------------------------------------- | ----------------------------- |
| `sources_registered`            | Fuentes registradas                    | Medir catálogo de fuentes    |
| `trusted_sources_count`         | Fuentes trusted                        | Medir base confiable          |
| `watchlist_sources_count`       | Fuentes en observación                | Medir riesgo                  |
| `blocked_sources_count`         | Fuentes bloqueadas                     | Medir higiene                 |
| `source_usage_count`            | Uso por fuente                         | Detectar dependencia excesiva |
| `primary_source_usage_rate`     | % piezas con fuente primaria           | Medir fortaleza editorial     |
| `social_source_dependency_rate` | % piezas dependientes de fuente social | Medir exposición a ruido     |
| `corrections_by_source`         | Correcciones asociadas a fuente        | Medir precisión              |
| `rumors_by_source`              | Rumores originados por fuente          | Detectar fuentes débiles     |
| `blocked_source_usage_attempts` | Intentos de uso de fuente bloqueada    | Detectar fallas de control    |

## 9.3 Metas iniciales

| Métrica                                           | Meta inicial |
| -------------------------------------------------- | -----------: |
| Piezas publicadas con fuente registrada            |         100% |
| Piezas sensibles con fuente primaria o equivalente |         100% |
| Uso de fuentes bloqueadas                          |            0 |
| Noticias P0 con fuente social como única fuente   |            0 |
| Fuentes sin tipo asignado                          |            0 |

---

# 10. Métricas de verificación

## 10.1 Objetivo

Medir si las noticias publicadas cuentan con evidencia, confianza y verificación suficiente.

## 10.2 Métricas principales

| Métrica                                | Definición                           | Uso                          |
| --------------------------------------- | ------------------------------------- | ---------------------------- |
| `verification_records_created`        | Registros de verificación creados    | Medir disciplina             |
| `verified_news_count`                 | Noticias verificadas                  | Medir volumen publicable     |
| `partially_verified_news_count`       | Noticias parcialmente verificadas     | Medir incertidumbre          |
| `rumor_count`                         | Noticias marcadas como rumor          | Medir ruido                  |
| `rejected_verification_count`         | Noticias rechazadas por verificación | Medir filtro                 |
| `escalated_verification_count`        | Noticias escaladas                    | Medir sensibilidad           |
| `average_verification_time`           | Tiempo promedio de verificación      | Medir eficiencia             |
| `evidence_level_distribution`         | Distribución E0-E5                   | Medir fortaleza de evidencia |
| `confidence_level_distribution`       | Distribución C0-C5                   | Medir confianza editorial    |
| `publication_blocked_by_verification` | Publicaciones bloqueadas              | Medir control                |

## 10.3 Metas iniciales

| Métrica                              | Meta inicial |
| ------------------------------------- | -----------: |
| Publicaciones con VerificationRecord  |         100% |
| Piezas sensibles con revisión humana |         100% |
| Rumores publicados como hechos        |            0 |
| Publicaciones sin nivel de evidencia  |            0 |
| Publicaciones sin nivel de confianza  |            0 |

---

# 11. Métricas de producción

## 11.1 Objetivo

Medir la capacidad del newsroom para producir contenido editorial útil y consistente.

## 11.2 Métricas principales

| Métrica                     | Definición                   | Uso                         |
| ---------------------------- | ----------------------------- | --------------------------- |
| `content_pieces_created`   | Piezas creadas                | Medir producción total     |
| `briefs_created`           | Briefs editoriales creados    | Medir preparación          |
| `scripts_created`          | Guiones creados               | Medir capacidad audiovisual |
| `short_scripts_created`    | Guiones cortos creados        | Medir clips                 |
| `articles_created`         | Artículos creados            | Medir contenido web         |
| `newsletter_items_created` | Bloques newsletter creados    | Medir curaduría            |
| `content_by_format`        | Contenido por formato         | Ver balance                 |
| `content_by_category`      | Contenido por categoría      | Ver foco editorial          |
| `average_draft_time`       | Tiempo promedio de redacción | Medir eficiencia            |
| `revision_count_per_piece` | Revisiones por pieza          | Medir calidad inicial       |

## 11.3 Metas iniciales

| Métrica                          | Meta inicial |
| --------------------------------- | -----------: |
| Piezas con brief previo           |         80%+ |
| Piezas sensibles con brief previo |         100% |
| Piezas con fuente conservada      |         100% |
| Piezas sin responsable            |            0 |
| Piezas sin estado                 |            0 |

---

# 12. Métricas de publicación

## 12.1 Objetivo

Medir la salida real del newsroom.

## 12.2 Métricas principales

| Métrica                          | Definición                          | Uso                 |
| --------------------------------- | ------------------------------------ | ------------------- |
| `publications_created`          | Publicaciones registradas            | Medir salida total  |
| `published_content_count`       | Piezas publicadas                    | Medir ejecución    |
| `scheduled_content_count`       | Piezas programadas                   | Medir planeación   |
| `failed_publications_count`     | Publicaciones fallidas               | Detectar fricción  |
| `publication_by_channel`        | Publicaciones por canal              | Medir distribución |
| `approval_to_publication_time`  | Tiempo de aprobación a publicación | Medir velocidad     |
| `published_url_capture_rate`    | % publicaciones con URL              | Medir trazabilidad  |
| `publication_corrections_count` | Correcciones posteriores             | Medir calidad       |
| `retractions_count`             | Retiradas                            | Medir riesgo grave  |

## 12.3 Metas iniciales

| Métrica                                    | Meta inicial |
| ------------------------------------------- | -----------: |
| Publicaciones con URL registrada            |         100% |
| Publicaciones con responsable               |         100% |
| Publicaciones con PublicationRecord         |         100% |
| Publicaciones fallidas sin causa registrada |            0 |
| Correcciones materiales sin registro        |            0 |

---

# 13. Métricas de distribución

## 13.1 Objetivo

Medir cómo se adapta y distribuye el contenido en múltiples canales.

## 13.2 Métricas principales

| Métrica                         | Definición                      | Uso                          |
| -------------------------------- | -------------------------------- | ---------------------------- |
| `distribution_plans_created`   | Planes de distribución creados  | Medir planeación            |
| `channel_variants_created`     | Variantes por canal              | Medir adaptación            |
| `variants_per_content_piece`   | Variantes por pieza base         | Medir reutilización         |
| `distribution_records_created` | Registros de distribución       | Medir trazabilidad           |
| `distribution_by_channel`      | Distribución por canal          | Ver balance                  |
| `distribution_failure_rate`    | Fallas de distribución          | Detectar problemas           |
| `variant_rejection_rate`       | Variantes rechazadas             | Medir calidad de adaptación |
| `cross_channel_performance`    | Desempeño comparativo por canal | Optimizar canal              |
| `unmeasured_distributions`     | Distribuciones sin métricas     | Detectar cierre incompleto   |

## 13.3 Metas iniciales

| Métrica                               | Meta inicial |
| -------------------------------------- | -----------: |
| Variantes con fuente interna           |         100% |
| Variantes con correlation_id           |         100% |
| Variantes que exceden evidencia        |            0 |
| Distribuciones con URL o ID registrado |         100% |
| Distribuciones con métricas 24h       |         90%+ |

---

# 14. Métricas de audiencia

## 14.1 Objetivo

Medir respuesta de audiencia sin confundir popularidad con calidad.

## 14.2 Métricas por canal

### YouTube

| Métrica                  | Uso                           |
| ------------------------- | ----------------------------- |
| `views`                 | Alcance                       |
| `watch_time`            | Profundidad de consumo        |
| `average_view_duration` | Calidad de retención         |
| `retention_rate`        | Interés sostenido            |
| `ctr`                   | Efectividad título/thumbnail |
| `comments`              | Conversación                 |
| `subscribers_gained`    | Crecimiento                   |

### Shorts / TikTok / Reels

| Métrica              | Uso                      |
| --------------------- | ------------------------ |
| `views`             | Alcance                  |
| `completion_rate`   | Calidad del clip         |
| `shares`            | Valor percibido          |
| `saves`             | Utilidad                 |
| `comments`          | Interacción             |
| `follows_generated` | Conversión de audiencia |

### X / Twitter

| Métrica           | Uso                           |
| ------------------ | ----------------------------- |
| `impressions`    | Alcance                       |
| `reposts`        | Amplificación                |
| `replies`        | Conversación                 |
| `clicks`         | Tráfico                      |
| `profile_visits` | Interés                      |
| `bookmarks`      | Valor percibido si disponible |

### LinkedIn

| Métrica           | Uso                  |
| ------------------ | -------------------- |
| `impressions`    | Alcance profesional  |
| `reactions`      | Respuesta            |
| `comments`       | Conversación        |
| `shares`         | Relevancia           |
| `profile_visits` | Interés profesional |
| `link_clicks`    | Tráfico             |

### Newsletter

| Métrica             | Uso                     |
| -------------------- | ----------------------- |
| `open_rate`        | Interés inicial        |
| `click_rate`       | Valor del contenido     |
| `unsubscribe_rate` | Fatiga o desalineación |
| `reply_rate`       | Calidad de relación    |
| `bounce_rate`      | Higiene de lista        |

### Blog / Web

| Métrica           | Uso             |
| ------------------ | --------------- |
| `pageviews`      | Alcance         |
| `time_on_page`   | Profundidad     |
| `scroll_depth`   | Consumo real    |
| `search_traffic` | Valor evergreen |
| `referrals`      | Distribución   |
| `cta_clicks`     | Conversión     |

---

# 15. Métricas de calidad editorial

## 15.1 Objetivo

Medir precisión, consistencia, responsabilidad y calidad del contenido publicado.

## 15.2 Métricas principales

| Métrica                             | Definición                     | Uso                   |
| ------------------------------------ | ------------------------------- | --------------------- |
| `corrections_count`                | Correcciones totales            | Medir errores         |
| `material_corrections_count`       | Correcciones materiales         | Medir riesgo          |
| `retractions_count`                | Retiradas                       | Medir fallas graves   |
| `source_missing_count`             | Piezas sin fuente               | Debe ser 0            |
| `disclaimer_missing_count`         | Disclaimers omitidos            | Medir riesgo          |
| `headline_mismatch_count`          | Titulares que exceden evidencia | Medir clickbait       |
| `fact_opinion_mixing_count`        | Mezcla hecho/opinión           | Medir claridad        |
| `rumor_misclassification_count`    | Rumores mal clasificados        | Medir falla editorial |
| `sensitive_content_without_review` | Piezas sensibles sin revisión  | Debe ser 0            |

## 15.3 Metas iniciales

| Métrica                               | Meta inicial |
| -------------------------------------- | -----------: |
| Piezas sin fuente                      |            0 |
| Rumores publicados como hechos         |            0 |
| Piezas sensibles sin revisión humana  |            0 |
| Correcciones materiales no registradas |            0 |
| Retiradas por error editorial          |   0 objetivo |

---

# 16. Métricas de calendario editorial

## 16.1 Objetivo

Medir cumplimiento, consistencia y carga de producción calendarizada.

## 16.2 Métricas principales

| Métrica                     | Definición            | Uso                        |
| ---------------------------- | ---------------------- | -------------------------- |
| `calendar_items_created`   | Ítems creados         | Medir planeación          |
| `calendar_items_published` | Ítems publicados      | Medir cumplimiento         |
| `calendar_items_postponed` | Ítems pospuestos      | Detectar fricción         |
| `calendar_items_cancelled` | Ítems cancelados      | Medir sobreplaneación     |
| `calendar_items_replaced`  | Ítems reemplazados    | Medir impacto de coyuntura |
| `on_time_publication_rate` | % publicado a tiempo   | Medir disciplina           |
| `calendar_completion_rate` | % completado           | Medir ejecución           |
| `overdue_items_count`      | Ítems atrasados       | Detectar cuello de botella |
| `items_without_owner`      | Ítems sin responsable | Debe ser 0                 |

---

# 17. Métricas de agentes

## 17.1 Objetivo

Medir si los agentes realmente aportan valor operativo.

## 17.2 Métricas principales

| Métrica                         | Definición                  | Uso                    |
| -------------------------------- | ---------------------------- | ---------------------- |
| `agent_executions_count`       | Ejecuciones por agente       | Medir uso              |
| `agent_success_rate`           | % ejecuciones exitosas       | Medir estabilidad      |
| `agent_failure_rate`           | % fallas                     | Detectar problemas     |
| `average_agent_latency`        | Tiempo promedio de respuesta | Medir eficiencia       |
| `agent_output_acceptance_rate` | % salidas aceptadas          | Medir utilidad         |
| `agent_output_revision_rate`   | % salidas corregidas         | Medir calidad          |
| `agent_escalation_count`       | Escalamientos generados      | Medir riesgo detectado |
| `agent_policy_violation_count` | Violaciones de política     | Debe ser bajo/cero     |
| `agent_cost_estimate`          | Costo por agente             | Medir sostenibilidad   |
| `agent_memory_usage_count`     | Uso de memoria               | Medir contexto         |

## 17.3 Metas iniciales

| Métrica                                | Meta inicial |
| --------------------------------------- | -----------: |
| Ejecuciones con correlation_id          |         100% |
| Ejecuciones con agente identificado     |         100% |
| Salidas aceptadas sin edición crítica |         70%+ |
| Violaciones de política editorial      |  0 críticas |
| Agentes sin registro de ejecución      |            0 |

---

# 18. Métricas de memoria editorial

## 18.1 Objetivo

Medir si la memoria editorial mejora la operación o solo acumula ruido.

## 18.2 Métricas principales

| Métrica                        | Definición           | Uso                         |
| ------------------------------- | --------------------- | --------------------------- |
| `memory_items_proposed`       | Memorias propuestas   | Medir aprendizaje potencial |
| `memory_items_approved`       | Memorias aprobadas    | Medir utilidad              |
| `memory_items_rejected`       | Memorias rechazadas   | Medir ruido                 |
| `memory_items_invalidated`    | Memorias invalidadas  | Medir higiene               |
| `memory_reuse_count`          | Memorias reutilizadas | Medir valor real            |
| `memory_by_type`              | Memoria por tipo      | Analizar composición       |
| `memory_without_source_count` | Memorias sin fuente   | Debe ser 0                  |
| `memory_conflict_count`       | Memorias en conflicto | Detectar inconsistencia     |

## 18.3 Tipos de memoria

```text
source_memory
editorial_memory
distribution_memory
verification_memory
incident_memory
audience_memory
calendar_memory
agent_memory
```

## 18.4 Metas iniciales

| Métrica                         | Meta inicial |
| -------------------------------- | -----------: |
| Memorias con fuente              |         100% |
| Memorias aprobadas manualmente   |         100% |
| Memorias reutilizadas por semana |           5+ |
| Memorias sin fuente              |            0 |
| Memorias invalidadas sin motivo  |            0 |

---

# 19. Métricas de incidentes

## 19.1 Objetivo

Medir errores, fallas, riesgos y eventos que requieren corrección o escalamiento.

## 19.2 Métricas principales

| Métrica                          | Definición                | Uso                       |
| --------------------------------- | -------------------------- | ------------------------- |
| `editorial_incidents_count`     | Incidentes editoriales     | Medir riesgo              |
| `incident_by_severity`          | Incidentes por severidad   | Priorizar                 |
| `incident_by_type`              | Incidentes por tipo        | Detectar patrón          |
| `mean_time_to_detect_incident`  | Tiempo de detección       | Medir vigilancia          |
| `mean_time_to_resolve_incident` | Tiempo de resolución      | Medir respuesta           |
| `corrections_after_incident`    | Correcciones por incidente | Medir impacto             |
| `retractions_after_incident`    | Retiradas por incidente    | Medir gravedad            |
| `repeat_incidents_count`        | Incidentes repetidos       | Detectar falla sistémica |

## 19.3 Tipos de incidente

```text
wrong_source
wrong_date
rumor_published_as_fact
headline_exceeded_evidence
missing_disclaimer
sensitive_content_without_review
publication_error
distribution_error
metrics_missing
agent_error
source_failure
correction_required
retraction_required
```

---

# 20. Métricas ejecutivas

## 20.1 Objetivo

Dar una vista simple del estado del newsroom para decisión ejecutiva.

## 20.2 Métricas recomendadas

| Métrica                    | Pregunta que responde                 |
| --------------------------- | ------------------------------------- |
| Noticias publicadas         | ¿Cuánto producimos?                 |
| Piezas con fuente           | ¿Qué tan trazables somos?           |
| Correcciones materiales     | ¿Qué tan precisos somos?            |
| Tiempo promedio de pipeline | ¿Qué tan rápidos somos?            |
| Fuentes trusted usadas      | ¿Qué tan confiable es nuestra base? |
| Publicaciones por canal     | ¿Dónde estamos distribuyendo?       |
| Mejor canal por engagement  | ¿Dónde responde la audiencia?       |
| Piezas sensibles revisadas  | ¿Controlamos riesgo?                 |
| Incidentes abiertos         | ¿Qué está mal?                     |
| Memorias reutilizadas       | ¿Estamos aprendiendo?                |
| Agentes con mayor utilidad  | ¿Qué automatización funciona?      |

---

## 21. Ventanas de medición

### 21.1 Ventanas mínimas por publicación

```text
1 hora
24 horas
7 días
30 días
```

### 21.2 Ventanas operativas

| Ventana    | Uso                           |
| ---------- | ----------------------------- |
| Diario     | Operación y cierre           |
| Semanal    | Revisión editorial           |
| Mensual    | Ajustes de estrategia         |
| Trimestral | Revisión de modelo operativo |

---

## 22. Dashboards recomendados en XMIP

### 22.1 Daily Operations Dashboard

Debe mostrar:

* Señales detectadas.
* Noticias en verificación.
* Piezas en producción.
* Publicaciones del día.
* Incidentes abiertos.
* Piezas pendientes.
* Métricas iniciales.
* Checklist de cierre.

---

### 22.2 Editorial Quality Dashboard

Debe mostrar:

* Correcciones.
* Piezas sin fuente.
* Piezas sensibles revisadas.
* Rumores detectados.
* Escalamientos.
* Titulares corregidos.
* Disclaimers faltantes.
* Incidentes editoriales.

---

### 22.3 Source Reliability Dashboard

Debe mostrar:

* Fuentes trusted.
* Fuentes watchlist.
* Fuentes bloqueadas.
* Uso por fuente.
* Correcciones por fuente.
* Rumores por fuente.
* Dependencia de fuentes sociales.
* Uso de fuentes primarias.

---

### 22.4 Distribution Dashboard

Debe mostrar:

* Publicaciones por canal.
* Variantes por pieza.
* Desempeño por canal.
* Métricas 1h / 24h / 7d.
* Publicaciones fallidas.
* URLs faltantes.
* Distribuciones sin métricas.

---

### 22.5 Agent Operations Dashboard

Debe mostrar:

* Ejecuciones por agente.
* Tasa de éxito.
* Fallas.
* Salidas aceptadas.
* Salidas rechazadas.
* Costos estimados.
* Latencia.
* Violaciones de política.

---

### 22.6 Executive Dashboard

Debe mostrar:

* Producción total.
* Calidad editorial.
* Riesgo.
* Alcance.
* Engagement.
* Incidentes.
* Aprendizaje.
* Estado de operación.

---

## 23. Datos mínimos en XMIP

### 23.1 MetricDefinition

```text
metric_id
metric_key
name
description
category
unit
calculation_method
owner
status
created_at
updated_at
```

---

### 23.2 MetricSnapshot

```text
metric_snapshot_id
metric_key
entity_type
entity_id
value
unit
window
source
recorded_at
correlation_id
metadata
```

---

### 23.3 MetricTarget

```text
target_id
metric_key
target_value
comparison_operator
period
priority
owner
status
created_at
updated_at
```

---

### 23.4 MetricAlert

```text
alert_id
metric_key
entity_type
entity_id
threshold
actual_value
severity
status
triggered_at
resolved_at
owner
correlation_id
metadata
```

---

### 23.5 DashboardView

```text
dashboard_id
name
description
metrics
owner
refresh_frequency
status
metadata
```

---

## 24. Relaciones de conocimiento

Las métricas deben conectarse con el grafo de conocimiento.

Relaciones mínimas:

```text
MetricSnapshot measures PublicationRecord
MetricSnapshot measures DistributionRecord
MetricSnapshot measures AgentExecution
MetricSnapshot measures SourceUsage
MetricSnapshot measures VerificationRecord
MetricSnapshot measures CalendarItem
MetricSnapshot measures IncidentRecord
MetricSnapshot derived_from Channel
MetricSnapshot informs EditorialDecision
MetricAlert triggered_by MetricSnapshot
EditorialMemory derived_from MetricSnapshot
```

---

## 25. Eventos de auditoría

### 25.1 Eventos obligatorios

| Evento                  | Cuándo ocurre                 |
| ----------------------- | ------------------------------ |
| metric_recorded         | Se registra métrica           |
| metric_target_created   | Se crea meta                   |
| metric_alert_triggered  | Se dispara alerta              |
| metric_alert_resolved   | Se resuelve alerta             |
| dashboard_viewed        | Se consulta dashboard crítico |
| metric_anomaly_detected | Se detecta anomalía           |
| metric_missing          | Falta métrica obligatoria     |
| metric_corrected        | Se corrige métrica            |

### 25.2 Evento mínimo

```json
{
  "event_type": "metric_recorded",
  "metric_key": "published_url_capture_rate",
  "entity_type": "publication_record",
  "entity_id": "publication_001",
  "value": 1,
  "unit": "boolean",
  "window": "24h",
  "source": "xmip",
  "status": "success",
  "correlation_id": "corr_20260702_xxxxxx",
  "occurred_at": "2026-07-02T00:00:00Z"
}
```

---

## 26. Alertas operativas

### 26.1 Alertas críticas

Disparar alerta crítica si:

* Se publica una pieza sin fuente.
* Se publica una pieza sensible sin revisión.
* Se publica rumor como hecho.
* Se usa fuente bloqueada.
* Se retira contenido por error grave.
* Falta VerificationRecord en publicación.
* Falta PublicationRecord.
* Falta URL publicada.
* Se detecta incidente editorial crítico.

---

### 26.2 Alertas medias

Disparar alerta media si:

* Hay muchas piezas atrasadas.
* Hay publicaciones sin métricas 24h.
* Hay aumento de correcciones.
* Hay alta dependencia de fuentes sociales.
* Hay muchas variantes rechazadas.
* Hay baja aceptación de outputs de agentes.
* Hay métricas faltantes recurrentes.

---

### 26.3 Alertas bajas

Disparar alerta baja si:

* Hay ítems de calendario sin dueño.
* Hay memorias propuestas sin revisar.
* Hay fuentes sin revisión reciente.
* Hay piezas archivadas sin cierre completo.
* Hay dashboards sin actualizar.

---

## 27. Scorecards recomendados

### 27.1 Score editorial diario

| Dimensión             |          Peso |
| ---------------------- | ------------: |
| Piezas con fuente      |          Alto |
| Verificación completa |          Alto |
| Piezas publicadas      |         Medio |
| Correcciones           | Alto negativo |
| Incidentes             | Alto negativo |
| Métricas registradas  |         Medio |
| Memoria útil          |         Medio |

---

### 27.2 Score de fuente

| Dimensión                       |          Peso |
| -------------------------------- | ------------: |
| Historial de precisión          |          Alto |
| Uso en publicaciones verificadas |          Alto |
| Correcciones asociadas           | Alto negativo |
| Rumores originados               | Alto negativo |
| Transparencia                    |         Medio |
| Fuente primaria                  |          Alto |

---

### 27.3 Score de agente

| Dimensión                   |           Peso |
| ---------------------------- | -------------: |
| Salidas aceptadas            |           Alto |
| Fallas                       | Medio negativo |
| Violaciones de política     |  Alto negativo |
| Latencia                     |          Medio |
| Uso de memoria correcto      |          Medio |
| Contribución a publicación |           Alto |

---

## 28. Revisión operativa

### 28.1 Revisión diaria

Debe revisar:

* Publicaciones del día.
* Piezas pendientes.
* Incidentes.
* Métricas iniciales.
* Fuentes problemáticas.
* Checklist de cierre.

---

### 28.2 Revisión semanal

Debe revisar:

* Cumplimiento de calendario.
* Desempeño por canal.
* Correcciones.
* Piezas con mejor rendimiento.
* Fuentes más usadas.
* Agentes más útiles.
* Memorias reutilizadas.
* Temas que requieren seguimiento.

---

### 28.3 Revisión mensual

Debe revisar:

* Tendencias de audiencia.
* Calidad editorial.
* Eficiencia del pipeline.
* Riesgos recurrentes.
* Canales prioritarios.
* Fuentes confiables.
* Fuentes degradadas.
* Contenido evergreen.
* Roadmap operativo.

---

## 29. Riesgos de medición

| Riesgo                                           | Impacto | Probabilidad | Mitigación                              |
| ------------------------------------------------ | ------: | -----------: | ---------------------------------------- |
| Perseguir vanity metrics                         |    Alto |         Alta | Balancear audiencia con calidad          |
| Medir mucho y decidir poco                       |   Medio |         Alta | Dashboards accionables                   |
| No medir calidad editorial                       |    Alto |        Media | Métricas de corrección y verificación |
| Datos incompletos                                |   Medio |        Media | MetricSnapshot obligatorio               |
| Métricas sin fuente                             |   Medio |        Media | Source field obligatorio                 |
| Comparar canales incorrectamente                 |   Medio |        Media | Métricas por canal                      |
| Penalizar contenido educativo por baja viralidad |   Medio |        Media | Métricas por objetivo                   |
| Ignorar incidentes                               |    Alto |        Media | Alertas críticas                        |
| Agentes optimizados por velocidad, no calidad    |    Alto |        Media | Score de aceptación y riesgo            |
| Métricas desconectadas del pipeline             |    Alto |        Media | Relaciones con XMIP                      |

---

## 30. Antipatrones prohibidos

XCripto debe evitar:

* Medir solo views.
* Celebrar alcance si hubo error editorial.
* Ignorar correcciones.
* No registrar métricas por canal.
* Comparar newsletter con TikTok como si fueran iguales.
* Medir agentes solo por cantidad de outputs.
* Medir fuentes solo por volumen.
* Ocultar incidentes.
* No revisar métricas semanalmente.
* Dejar publicaciones sin URL.
* No conectar métricas con decisiones.
* Usar métricas para justificar contenido de baja calidad.
* Optimizar hacia hype.
* Premiar velocidad sin precisión.

---

## 31. Relación con XMIP

XMIP debe soportar métricas operativas mediante:

* Metric Definitions.
* Metric Snapshots.
* Metric Targets.
* Metric Alerts.
* Dashboards.
* Agent execution logs.
* Source usage logs.
* Verification records.
* Publication records.
* Distribution records.
* Incident records.
* Memory records.
* Knowledge relationships.

Las métricas deben estar integradas al pipeline, no capturadas manualmente como actividad aislada.

---

## 32. Criterios de aceptación

Este documento se considera aceptado cuando:

* [ ] Define propósito de métricas operativas.
* [ ] Define categorías de métricas.
* [ ] Define métricas de intake.
* [ ] Define métricas de fuentes.
* [ ] Define métricas de verificación.
* [ ] Define métricas de producción.
* [ ] Define métricas de publicación.
* [ ] Define métricas de distribución.
* [ ] Define métricas de audiencia.
* [ ] Define métricas de calidad editorial.
* [ ] Define métricas de calendario.
* [ ] Define métricas de agentes.
* [ ] Define métricas de memoria.
* [ ] Define métricas de incidentes.
* [ ] Define métricas ejecutivas.
* [ ] Define ventanas de medición.
* [ ] Define dashboards recomendados.
* [ ] Define datos mínimos en XMIP.
* [ ] Define relaciones de conocimiento.
* [ ] Define eventos de auditoría.
* [ ] Define alertas operativas.
* [ ] Define scorecards.
* [ ] Define revisión diaria, semanal y mensual.
* [ ] Define riesgos y mitigaciones.
* [ ] Define antipatrones.
* [ ] Define relación con XMIP.

---

## 33. Relación con otros documentos

Este documento se apoya en:

* ORION-018 — Operaciones Diarias.
* ORION-019 — Flujo de Publicación.
* ORION-020 — Runbook de Producción de Noticias.
* ORION-021 — Gestión de Fuentes.
* ORION-022 — Protocolo de Verificación Editorial.
* ORION-023 — Pipeline del Newsroom.
* ORION-024 — Calendario Editorial.
* ORION-025 — Distribución Multicanal.

Este documento gobierna directamente:

* ORION-027 — Gestión de Incidentes Editoriales.
* ORION-028 — Operación de Agentes Editoriales.
* ORION-029 — Checklist Diario del Newsroom.

---

## 34. Próximos pasos

Después de aprobar ORION-026, continuar con:

1. ORION-027 — Gestión de Incidentes Editoriales.
2. ORION-028 — Operación de Agentes Editoriales.
3. ORION-029 — Checklist Diario del Newsroom.

ORION-027 debe definir cómo XCripto detecta, clasifica, responde, corrige, escala y aprende de errores editoriales, técnicos o de publicación.

---

## 35. Historial de cambios

| Versión | Fecha      | Cambio                                   | Autor            |
| -------- | ---------- | ---------------------------------------- | ---------------- |
| 1.0      | 2026-07-02 | Versión inicial de métricas operativas | Fernando Cuellar |
