# ORION-028 — Operación de Agentes Editoriales

**Nivel documental:** L4 — Operations
**Volumen:** 006-operaciones
**Proyecto:** ORION / XCripto / XMIP
**Versión:** 1.0
**Estado:** Draft
**Owner:** Fernando Cuellar
**Última actualización:** 2026-07-02
**Ruta sugerida:** `docs/006-operaciones/ORION-028-Operacion-de-Agentes-Editoriales.md`

---

## 1. Propósito

Este documento define el modelo operativo para ejecutar, supervisar, limitar, auditar y mejorar los agentes editoriales de XCripto dentro de XMIP.

Su propósito es establecer cómo deben trabajar los agentes dentro del newsroom sin reemplazar el criterio editorial humano, sin publicar información no verificada, sin contaminar memoria, sin alterar el nivel de evidencia y sin operar fuera de sus límites.

ORION-028 responde a la pregunta:

> ¿Cómo operan los agentes editoriales de XCripto de forma útil, controlada, trazable y segura?

Los agentes no son el newsroom.
Los agentes son capacidades operativas al servicio del newsroom.

---

## 2. Alcance

Este documento cubre:

* Principios de operación de agentes editoriales.
* Catálogo operativo de agentes.
* Responsabilidades por agente.
* Límites por agente.
* Entradas y salidas permitidas.
* Niveles de autonomía.
* Flujos de ejecución.
* Supervisión humana.
* Validación de outputs.
* Auditoría.
* Gestión de errores.
* Memoria usada por agentes.
* Métricas de agentes.
* Reglas de seguridad editorial.
* Playbooks de operación.
* Criterios de aceptación.

Este documento no cubre en detalle:

* Arquitectura interna completa de agentes.
* Protocolo técnico de comunicación entre agentes.
* Modelo de datos general del sistema.
* Pipeline completo del newsroom.
* Gestión completa de incidentes.
* Métricas generales del newsroom.

Esos temas se desarrollan en:

* ORION-014 — Arquitectura de Agentes.
* ORION-014A — Protocolo de Comunicación entre Agentes.
* ORION-014B — Especificación de Agentes Digitales.
* ORION-023 — Pipeline del Newsroom.
* ORION-026 — Métricas Operativas.
* ORION-027 — Gestión de Incidentes Editoriales.

---

## 3. Documentos base

Este documento se apoya en:

* ORION-005 — Constitución Editorial.
* ORION-006 — Estándares Editoriales.
* ORION-007 — Flujo Editorial.
* ORION-014 — Arquitectura de Agentes.
* ORION-014A — Protocolo de Comunicación entre Agentes.
* ORION-014B — Especificación de Agentes Digitales.
* ORION-018 — Operaciones Diarias.
* ORION-019 — Flujo de Publicación.
* ORION-020 — Runbook de Producción de Noticias.
* ORION-021 — Gestión de Fuentes.
* ORION-022 — Protocolo de Verificación Editorial.
* ORION-023 — Pipeline del Newsroom.
* ORION-024 — Calendario Editorial.
* ORION-025 — Distribución Multicanal.
* ORION-026 — Métricas Operativas.
* ORION-027 — Gestión de Incidentes Editoriales.

Este documento gobierna directamente:

* ORION-029 — Checklist Diario del Newsroom.
* Futuros workflows de ejecución editorial en XMIP.
* Backlog técnico de agentes editoriales.
* Políticas de revisión humana.

---

## 4. Contexto operativo

XCripto usará agentes editoriales para acelerar tareas repetibles del newsroom:

```text
detectar noticias
validar fuentes
clasificar impacto
crear briefs
redactar borradores
generar guiones
crear variantes por canal
detectar riesgos
auditar trazabilidad
proponer memoria
medir resultados
```

Pero el ecosistema cripto es sensible:

* Hay rumores.
* Hay manipulación.
* Hay fuentes interesadas.
* Hay scams.
* Hay movimientos de mercado.
* Hay información legal compleja.
* Hay datos on-chain fáciles de malinterpretar.
* Hay riesgo reputacional.

Por eso, los agentes deben operar bajo límites estrictos.

El principio operativo es:

```text
Agentes aceleran.
Humanos aprueban.
XMIP audita.
ORION gobierna.
```

---

## 5. Principio rector

La operación de agentes editoriales de XCripto sigue este principio:

```text
Ningún agente publica, confirma, acusa, recomienda o escala confianza por sí solo.
```

Los agentes pueden:

* Proponer.
* Resumir.
* Clasificar.
* Comparar.
* Detectar.
* Redactar borradores.
* Adaptar formatos.
* Alertar riesgos.
* Preparar checklists.
* Crear registros.

Los agentes no pueden:

* Publicar directamente contenido sensible.
* Convertir rumor en hecho.
* Inventar fuentes.
* Aprobar verificación crítica.
* Retirar contenido por sí solos.
* Guardar memoria permanente sin aprobación.
* Modificar política editorial.
* Saltarse revisión humana.
* Dar recomendaciones financieras.

---

## 6. Objetivos operativos

Los agentes editoriales deben ayudar a:

1. Reducir tiempo de monitoreo.
2. Mejorar detección de noticias.
3. Filtrar ruido.
4. Estandarizar briefs.
5. Mejorar consistencia editorial.
6. Detectar riesgos antes de publicar.
7. Adaptar contenido por canal.
8. Mantener trazabilidad.
9. Proponer memoria útil.
10. Medir outputs.
11. Identificar incidentes.
12. Aumentar capacidad del newsroom sin perder control.

---

## 7. Catálogo de agentes editoriales

### 7.1 Agentes principales

| Agente               | Función principal                      | Nivel de riesgo |
| -------------------- | --------------------------------------- | --------------- |
| NewsScoutAgent       | Detectar señales y noticias candidatas | Medio           |
| SourceValidatorAgent | Validar fuentes y confiabilidad         | Alto            |
| MarketImpactAgent    | Clasificar impacto y categoría         | Medio           |
| EditorialAgent       | Crear briefs y piezas editoriales       | Alto            |
| ScriptAgent          | Crear guiones audiovisuales             | Medio           |
| SocialClipAgent      | Crear variantes cortas por canal        | Alto            |
| DistributionAgent    | Proponer distribución multicanal       | Medio           |
| RiskAgent            | Detectar riesgos editoriales            | Alto            |
| AuditAgent           | Validar trazabilidad y cumplimiento     | Alto            |
| MemoryAgent          | Proponer memoria editorial              | Medio           |
| KnowledgeAgent       | Crear relaciones semánticas            | Medio           |
| CalendarAgent        | Coordinar agenda editorial              | Bajo / Medio    |
| MetricsAgent         | Analizar desempeño operativo           | Bajo / Medio    |

---

## 8. Niveles de autonomía

### 8.1 Escala de autonomía

| Nivel | Nombre                 | Descripción                                 | Permitido en MVP |
| ----- | ---------------------- | -------------------------------------------- | ---------------- |
| A0    | Sin autonomía         | Solo responde a instrucción directa         | Sí              |
| A1    | Asistencia             | Propone salida, humano decide                | Sí              |
| A2    | Preparación           | Prepara registros o borradores               | Sí              |
| A3    | Ejecución supervisada | Ejecuta tareas no críticas con revisión    | Limitado         |
| A4    | Ejecución controlada  | Ejecuta acciones con políticas automáticas | Futuro           |
| A5    | Autonomía completa    | Decide y actúa sin humano                   | No permitido     |

### 8.2 Regla general

Para el MVP editorial de XCripto, los agentes deben operar principalmente en:

```text
A1 — Asistencia
A2 — Preparación
A3 — Ejecución supervisada limitada
```

El nivel A5 queda prohibido para decisiones editoriales críticas.

---

## 9. Responsabilidades por agente

## 9.1 NewsScoutAgent

### Propósito

Detectar señales informativas relevantes para el newsroom.

### Puede hacer

* Revisar fuentes configuradas.
* Identificar noticias candidatas.
* Agrupar señales similares.
* Detectar temas emergentes.
* Proponer categoría preliminar.
* Crear registros `detected`.
* Alertar posibles P0/P1.

### No puede hacer

* Confirmar noticia como verificada.
* Publicar alertas.
* Decidir prioridad final.
* Usar fuentes bloqueadas como válidas.
* Convertir rumor en hecho.

### Entradas

```text
source_feeds
social_signals
market_alerts
editorial_calendar
watchlists
```

### Salidas

```text
DetectedSignal
CandidateNewsItem
IntakeSummary
```

### Revisión humana requerida

* Cuando marque P0.
* Cuando la fuente sea social no verificada.
* Cuando el tema sea hack, exchange, regulación, fraude o insolvencia.

---

## 9.2 SourceValidatorAgent

### Propósito

Evaluar fuentes, detectar confiabilidad y apoyar verificación preliminar.

### Puede hacer

* Clasificar tipo de fuente.
* Revisar si existe en Source Registry.
* Detectar fuente primaria.
* Comparar fuentes.
* Revisar fecha.
* Marcar fuente débil.
* Proponer trust level.
* Proponer estado: `active`, `watchlist`, `restricted`, `blocked`.

### No puede hacer

* Aprobar fuente crítica sin humano.
* Rehabilitar fuente bloqueada.
* Ignorar contradicciones.
* Confirmar acusaciones sensibles.
* Sustituir verificación humana en temas críticos.

### Entradas

```text
source_url
source_metadata
source_history
news_item
verification_context
```

### Salidas

```text
SourceReview
SourceRiskFlag
SourceTrustRecommendation
VerificationInput
```

### Revisión humana requerida

* Cambio a `trusted`.
* Cambio a `blocked`.
* Rehabilitación de fuente.
* Fuente anónima.
* Fuente social usada en P0/P1.
* Fuente relacionada con acusaciones o riesgos legales.

---

## 9.3 MarketImpactAgent

### Propósito

Clasificar impacto editorial y de mercado sin hacer predicciones.

### Puede hacer

* Clasificar noticia por categoría.
* Identificar activos relacionados.
* Identificar narrativa.
* Separar impacto inmediato, medio y bajo.
* Marcar si requiere explicación.
* Proponer prioridad editorial.

### No puede hacer

* Predecir precio.
* Recomendar compra o venta.
* Afirmar causalidad sin evidencia.
* Presentar correlación como causa.
* Generar señales de trading.

### Entradas

```text
news_item
market_context
asset_list
category_taxonomy
historical_narratives
```

### Salidas

```text
MarketImpactAssessment
CategoryRecommendation
PriorityRecommendation
```

### Revisión humana requerida

* P0.
* Alta sensibilidad de mercado.
* Noticias sobre BTC, ETH, ETFs, exchanges o regulación con posible impacto fuerte.

---

## 9.4 EditorialAgent

### Propósito

Convertir noticias verificadas o parcialmente verificadas en briefs y borradores editoriales.

### Puede hacer

* Crear brief editorial.
* Redactar borrador de noticia.
* Proponer titular.
* Separar hechos de análisis.
* Sugerir estructura.
* Preparar texto para blog, newsletter o LinkedIn.
* Aplicar guía de estilo.

### No puede hacer

* Publicar.
* Aprobar su propio contenido.
* Inventar fuente.
* Ocultar incertidumbre.
* Cambiar estado de verificación.
* Redactar acusaciones no sustentadas.
* Convertir análisis en recomendación financiera.

### Entradas

```text
verified_news_item
verification_record
source_refs
editorial_context
style_guide
```

### Salidas

```text
EditorialBrief
ContentDraft
HeadlineOptions
Summary
```

### Revisión humana requerida

* Toda pieza sensible.
* Todo contenido legal, regulatorio, hack, exploit, fraude o exchange.
* Todo titular de alto impacto.
* Todo contenido que pueda inducir acción financiera.

---

## 9.5 ScriptAgent

### Propósito

Convertir briefs y noticias priorizadas en guiones para video.

### Puede hacer

* Crear guion de noticiero.
* Crear estructura de video.
* Crear hooks.
* Proponer transiciones.
* Dividir bloques.
* Sugerir cierres.
* Sugerir clips derivados.

### No puede hacer

* Cambiar nivel de certeza.
* Agregar hechos no verificados.
* Exagerar para retención.
* Crear promesas de precio.
* Eliminar disclaimers necesarios.

### Entradas

```text
editorial_brief
content_piece
format_requirements
video_duration
channel_rules
```

### Salidas

```text
VideoScript
NewscastSegment
ClipSuggestions
HookOptions
```

### Revisión humana requerida

* Guion final de noticiero.
* Hooks de temas sensibles.
* Videos sobre mercado, hacks, regulación o exchanges.

---

## 9.6 SocialClipAgent

### Propósito

Adaptar contenido a formatos cortos y redes sociales.

### Puede hacer

* Crear hooks cortos.
* Crear captions.
* Proponer posts para X.
* Crear guiones para Shorts, TikTok y Reels.
* Crear hilos.
* Sugerir CTAs.
* Crear variantes por canal.

### No puede hacer

* Exagerar evidencia.
* Quitar incertidumbre.
* Publicar directamente.
* Usar lenguaje de recomendación financiera.
* Convertir rumor en alerta.
* Crear clickbait engañoso.

### Entradas

```text
approved_content_piece
verification_record
channel_rules
distribution_plan
```

### Salidas

```text
ChannelVariant
ShortScript
SocialCaption
XThread
HookOptions
```

### Revisión humana requerida

* Temas sensibles.
* Hooks fuertes.
* Contenido con información preliminar.
* Cualquier variante que reduzca contexto crítico.

---

## 9.7 DistributionAgent

### Propósito

Crear y coordinar planes de distribución multicanal.

### Puede hacer

* Sugerir canal principal.
* Sugerir canales secundarios.
* Crear DistributionPlan.
* Detectar saturación de canal.
* Marcar contenido reutilizable.
* Recomendar horario.

### No puede hacer

* Publicar sin aprobación.
* Saltarse calendario.
* Distribuir contenido rechazado.
* Programar contenido desactualizado.
* Cambiar prioridad editorial por sí solo.

### Entradas

```text
approved_content_piece
calendar_items
channel_strategy
metric_history
```

### Salidas

```text
DistributionPlan
ChannelScheduleRecommendation
DistributionChecklist
```

### Revisión humana requerida

* Campañas especiales.
* Breaking news.
* Piezas sensibles.
* Cambios de prioridad P0/P1.

---

## 9.8 RiskAgent

### Propósito

Detectar riesgos editoriales, reputacionales, financieros, legales o de confianza.

### Puede hacer

* Evaluar lenguaje.
* Detectar afirmaciones no verificadas.
* Detectar hype.
* Detectar falta de disclaimer.
* Marcar necesidad de escalamiento.
* Recomendar bloqueo de publicación.
* Detectar riesgo por canal.

### No puede hacer

* Aprobar publicación.
* Resolver incidente solo.
* Cambiar política editorial.
* Hacer juicio legal definitivo.
* Descartar riesgo sin evidencia.

### Entradas

```text
content_piece
headline
verification_record
source_refs
channel_variant
risk_policy
```

### Salidas

```text
RiskReview
EscalationRecommendation
PolicyViolationFlag
DisclaimerRecommendation
```

### Revisión humana requerida

* SEV-0 / SEV-1.
* Riesgo alto o crítico.
* Bloqueo de publicación sensible.
* Recomendación de retiro.

---

## 9.9 AuditAgent

### Propósito

Verificar que cada operación tenga trazabilidad, estados y evidencia mínima.

### Puede hacer

* Revisar si existe SourceReference.
* Revisar VerificationRecord.
* Revisar ApprovalRecord.
* Revisar correlation_id.
* Revisar PublicationRecord.
* Detectar faltantes.
* Crear audit flags.
* Bloquear flujo si falta requisito crítico.

### No puede hacer

* Aprobar editorialmente.
* Corregir contenido por sí solo.
* Modificar fuente.
* Modificar memoria.
* Cambiar política.

### Entradas

```text
workflow_run
news_item
content_piece
publication_record
audit_policy
```

### Salidas

```text
AuditCheck
AuditEvent
MissingRequirementFlag
PublicationBlockRecommendation
```

### Revisión humana requerida

* Cuando detecte bloqueo crítico.
* Cuando falten evidencias en publicación ya realizada.
* Cuando se detecte manipulación o bypass de proceso.

---

## 9.10 MemoryAgent

### Propósito

Proponer memoria editorial útil para mejorar continuidad y aprendizaje.

### Puede hacer

* Proponer memoria.
* Relacionar memoria con fuente, noticia o incidente.
* Detectar patrones.
* Sugerir invalidación.
* Identificar narrativas recurrentes.

### No puede hacer

* Guardar memoria permanente sin aprobación.
* Guardar rumor como hecho.
* Guardar información sensible sin fuente.
* Rehabilitar memoria inválida.
* Sobrescribir memoria aprobada sin revisión.

### Entradas

```text
news_item
incident_record
metric_snapshot
source_review
editorial_decision
```

### Salidas

```text
MemoryProposal
MemoryInvalidationSuggestion
NarrativeMemoryCandidate
```

### Revisión humana requerida

* Toda memoria persistente.
* Memoria derivada de incidentes.
* Memoria sobre fuentes.
* Memoria que afecte decisiones futuras.

---

## 9.11 KnowledgeAgent

### Propósito

Conectar noticias, fuentes, documentos, agentes, decisiones, métricas e incidentes dentro del grafo de conocimiento.

### Puede hacer

* Crear relaciones propuestas.
* Detectar nodos huérfanos.
* Relacionar fuente con noticia.
* Relacionar incidente con causa.
* Relacionar pieza con métrica.
* Proponer impacto en documentos.

### No puede hacer

* Aprobar relaciones críticas sin revisión.
* Inventar relaciones.
* Convertir correlación en causalidad.
* Eliminar nodos auditables.

### Entradas

```text
news_item
source_reference
content_piece
publication_record
incident_record
metric_snapshot
memory_item
```

### Salidas

```text
KnowledgeNodeProposal
KnowledgeEdgeProposal
ImpactAnalysis
RelationshipWarnings
```

### Revisión humana requerida

* Relaciones de causalidad.
* Relaciones con incidentes SEV-0/SEV-1.
* Relaciones que afecten fuente, política o riesgo.

---

## 9.12 CalendarAgent

### Propósito

Coordinar calendario editorial y detectar conflictos de agenda.

### Puede hacer

* Proponer agenda semanal.
* Detectar piezas atrasadas.
* Sugerir reprogramación.
* Relacionar eventos externos con calendario.
* Sugerir contenido evergreen.

### No puede hacer

* Cancelar P0/P1 sin humano.
* Publicar contenido programado.
* Revalidar noticia por sí solo.
* Ignorar cambio de contexto.

### Entradas

```text
calendar_items
editorial_events
pipeline_status
content_schedule
```

### Salidas

```text
CalendarRecommendation
RescheduleSuggestion
EditorialAgendaDraft
```

### Revisión humana requerida

* Cambios de prioridad.
* Reprogramación de contenido sensible.
* Coberturas especiales.

---

## 9.13 MetricsAgent

### Propósito

Analizar desempeño operativo y sugerir mejoras.

### Puede hacer

* Analizar métricas por canal.
* Detectar anomalías.
* Sugerir horarios.
* Detectar piezas sin métricas.
* Identificar formatos con mejor rendimiento.
* Proponer aprendizajes.

### No puede hacer

* Cambiar estrategia por sí solo.
* Optimizar hacia clickbait.
* Ignorar calidad editorial.
* Priorizar views sobre confianza.

### Entradas

```text
metric_snapshots
publication_records
distribution_records
calendar_items
agent_executions
```

### Salidas

```text
MetricInsight
PerformanceSummary
OperationalRecommendation
MetricAlert
```

### Revisión humana requerida

* Cambios de calendario basados en métricas.
* Decisiones estratégicas.
* Reglas nuevas de distribución.

---

## 10. Flujos operativos de agentes

## 10.1 Flujo: detección de noticia

```text
NewsScoutAgent
→ CandidateNewsItem
→ SourceValidatorAgent
→ SourceReview
→ MarketImpactAgent
→ PriorityRecommendation
→ Operador decide
```

Criterios:

* NewsScoutAgent no confirma.
* SourceValidatorAgent no aprueba temas críticos solo.
* Operador decide si entra al pipeline.

---

## 10.2 Flujo: verificación

```text
SourceValidatorAgent
→ VerificationInput
→ RiskAgent
→ RiskReview
→ AuditAgent
→ VerificationCompletenessCheck
→ Revisor / Editor decide
```

Criterios:

* La verificación final en temas sensibles es humana.
* AuditAgent bloquea si falta fuente, evidencia o correlation_id.

---

## 10.3 Flujo: producción editorial

```text
EditorialAgent
→ EditorialBrief
→ EditorialAgent / ScriptAgent
→ ContentDraft
→ RiskAgent
→ RiskReview
→ Revisor Editorial
```

Criterios:

* Ningún borrador va directo a publicación.
* El RiskAgent revisa antes de aprobación.
* El Revisor Editorial aprueba o regresa.

---

## 10.4 Flujo: distribución

```text
DistributionAgent
→ DistributionPlan
→ SocialClipAgent
→ ChannelVariants
→ RiskAgent
→ ChannelRiskReview
→ Operador publica/programa
→ AuditAgent verifica
```

Criterios:

* Cada variante conserva nivel de evidencia.
* Cada URL se registra.
* Cada variante queda conectada a ContentPiece.

---

## 10.5 Flujo: incidente

```text
RiskAgent / AuditAgent
→ IncidentCandidate
→ Operador registra
→ Editor clasifica severidad
→ EditorialAgent propone corrección
→ DistributionAgent identifica canales afectados
→ AuditAgent valida cierre
→ MemoryAgent propone aprendizaje
```

Criterios:

* SEV-0 y SEV-1 requieren Owner / Editor Principal.
* Postmortem obligatorio para incidentes graves.

---

## 11. Reglas de validación de outputs

Todo output de agente debe evaluarse antes de uso operativo.

### 11.1 Validación mínima

* [ ] Tiene propósito claro.
* [ ] Está conectado a una entidad.
* [ ] Tiene fuente si afirma hechos.
* [ ] No inventa datos.
* [ ] Respeta estado de verificación.
* [ ] No excede nivel de evidencia.
* [ ] No viola política editorial.
* [ ] Tiene correlation_id.
* [ ] Registra agente y versión.
* [ ] Indica si requiere revisión humana.

---

### 11.2 Estados del output

| Estado    | Descripción                |
| --------- | --------------------------- |
| proposed  | Propuesto por agente        |
| accepted  | Aceptado                    |
| revised   | Requiere edición           |
| rejected  | Rechazado                   |
| escalated | Requiere revisión superior |
| blocked   | Bloqueado por política     |
| archived  | Archivado                   |

---

### 11.3 Regla

Un output en estado `proposed` no es publicación, decisión ni memoria aprobada.

---

## 12. Límites editoriales obligatorios

Los agentes tienen prohibido:

* Inventar fuentes.
* Simular haber revisado una fuente.
* Decir “confirmado” sin VerificationRecord.
* Usar lenguaje de predicción financiera.
* Publicar o programar contenido sensible.
* Retirar publicaciones sin aprobación.
* Aprobar memoria persistente.
* Aprobar cambios de estado críticos.
* Ignorar contradicciones.
* Reducir incertidumbre para hacer contenido más atractivo.
* Reescribir una noticia parcial como hecho cerrado.
* Crear acusaciones sin evidencia.
* Ocultar disclaimers.

---

## 13. Reglas de memoria para agentes

### 13.1 Uso permitido de memoria

Los agentes pueden usar memoria para:

* Mantener contexto del proyecto.
* Recordar lineamientos editoriales.
* Detectar narrativas recurrentes.
* Identificar fuentes confiables.
* Evitar errores repetidos.
* Relacionar incidentes previos.
* Reutilizar aprendizajes de distribución.

### 13.2 Uso prohibido de memoria

Los agentes no deben usar memoria para:

* Confirmar hechos actuales.
* Sustituir fuentes.
* Revivir información obsoleta.
* Tratar rumores como hechos.
* Contradecir VerificationRecord.
* Ignorar fuente primaria actual.
* Publicar con base en contexto viejo.

### 13.3 Regla crítica

La memoria no es evidencia.

```text
memoria editorial ≠ fuente factual
```

---

## 14. Datos mínimos en XMIP

### 14.1 AgentDefinition

```text
agent_id
agent_key
name
purpose
status
risk_level
allowed_tasks
forbidden_tasks
owner
version
metadata
```

---

### 14.2 AgentExecution

```text
agent_execution_id
agent_id
agent_version
task_type
input_ref
output_ref
status
started_at
completed_at
latency_ms
token_usage
cost_estimate
correlation_id
metadata
```

---

### 14.3 AgentOutput

```text
agent_output_id
agent_execution_id
entity_type
entity_id
output_type
content
status
review_required
reviewed_by
reviewed_at
risk_level
source_refs
correlation_id
metadata
```

---

### 14.4 AgentPolicyCheck

```text
policy_check_id
agent_execution_id
policy_key
result
severity
message
checked_at
correlation_id
metadata
```

---

### 14.5 AgentIncident

```text
agent_incident_id
agent_id
agent_execution_id
incident_type
severity
description
detected_at
status
resolution
correlation_id
metadata
```

---

### 14.6 AgentPerformanceMetric

```text
metric_id
agent_id
metric_key
value
window
recorded_at
source
correlation_id
metadata
```

---

## 15. Relaciones de conocimiento

Relaciones mínimas:

```text
AgentExecution produced AgentOutput
AgentOutput proposes ContentPiece
AgentOutput proposes SourceReview
AgentOutput proposes VerificationRecord
AgentOutput proposes MemoryItem
AgentExecution uses MemoryItem
AgentExecution uses SourceReference
AgentExecution governed_by AgentPolicy
AgentIncident affects AgentDefinition
AgentIncident caused_by AgentExecution
AgentOutput reviewed_by User
AgentOutput approved_by User
AgentOutput rejected_by User
MetricSnapshot measures AgentExecution
```

---

## 16. Eventos de auditoría

### 16.1 Eventos obligatorios

| Evento                     | Cuándo ocurre           |
| -------------------------- | ------------------------ |
| agent_execution_started    | Inicia ejecución        |
| agent_execution_completed  | Termina ejecución       |
| agent_execution_failed     | Falla ejecución         |
| agent_output_created       | Se crea output           |
| agent_output_reviewed      | Se revisa output         |
| agent_output_accepted      | Se acepta output         |
| agent_output_rejected      | Se rechaza output        |
| agent_output_blocked       | Se bloquea por política |
| agent_policy_violation     | Viola política          |
| agent_incident_created     | Se crea incidente        |
| agent_memory_used          | Usa memoria              |
| agent_source_used          | Usa fuente               |
| agent_escalation_requested | Solicita escalamiento    |

### 16.2 Evento mínimo

```json
{
  "event_type": "agent_output_created",
  "agent_id": "editorial-agent",
  "agent_execution_id": "exec_001",
  "output_type": "editorial_brief",
  "entity_type": "news_item",
  "entity_id": "news_001",
  "status": "proposed",
  "review_required": true,
  "correlation_id": "corr_20260702_xxxxxx",
  "occurred_at": "2026-07-02T00:00:00Z"
}
```

---

## 17. Métricas de operación de agentes

### 17.1 Métricas generales

| Métrica                         | Propósito            |
| -------------------------------- | --------------------- |
| `agent_executions_count`       | Medir uso             |
| `agent_success_rate`           | Medir estabilidad     |
| `agent_failure_rate`           | Detectar fallas       |
| `average_agent_latency`        | Medir velocidad       |
| `agent_output_acceptance_rate` | Medir utilidad        |
| `agent_output_revision_rate`   | Medir calidad inicial |
| `agent_output_rejection_rate`  | Detectar mala calidad |
| `agent_policy_violation_count` | Medir riesgo          |
| `agent_incident_count`         | Detectar problemas    |
| `agent_cost_estimate`          | Medir sostenibilidad  |
| `agent_memory_usage_count`     | Medir uso de contexto |
| `agent_escalation_count`       | Medir alertas útiles |

---

### 17.2 Métricas por agente

| Agente               | Métricas clave                                             |
| -------------------- | ----------------------------------------------------------- |
| NewsScoutAgent       | señales útiles, duplicados, falsos positivos              |
| SourceValidatorAgent | fuentes correctas, fuentes degradadas, errores de fuente    |
| MarketImpactAgent    | clasificación aceptada, revisión requerida                |
| EditorialAgent       | briefs aceptados, revisiones, errores de tono               |
| ScriptAgent          | guiones aceptados, hooks corregidos                         |
| SocialClipAgent      | variantes aceptadas, hooks rechazados                       |
| DistributionAgent    | planes aceptados, fallas de distribución                   |
| RiskAgent            | riesgos detectados, falsos positivos, incidentes prevenidos |
| AuditAgent           | faltantes detectados, bloqueos correctos                    |
| MemoryAgent          | memorias aprobadas, memorias rechazadas, reutilización     |
| KnowledgeAgent       | relaciones aceptadas, relaciones rechazadas                 |
| CalendarAgent        | recomendaciones aceptadas, conflictos detectados            |
| MetricsAgent         | insights útiles, alertas correctas                         |

---

### 17.3 Metas iniciales

| Métrica                                   | Meta |
| ------------------------------------------ | ---: |
| Ejecuciones con correlation_id             | 100% |
| Outputs con agente y versión              | 100% |
| Outputs sensibles con revisión humana     | 100% |
| Outputs publicados sin revisión           |    0 |
| Fuentes inventadas por agente              |    0 |
| Violaciones críticas de política         |    0 |
| Outputs aceptados sin corrección crítica | 70%+ |
| Memorias guardadas sin aprobación         |    0 |

---

## 18. Supervisión humana

### 18.1 Revisión humana obligatoria

Requieren revisión humana:

* Noticias P0.
* Hacks.
* Exploits.
* Fraudes.
* Exchanges.
* Regulación.
* Demandas.
* Insolvencia.
* Acusaciones.
* Contenido con impacto financiero.
* Rumores.
* Información contradictoria.
* Correcciones materiales.
* Retiros.
* Memoria persistente.
* Fuentes en watchlist/restricted.
* Outputs de agentes con riesgo alto.

---

### 18.2 Aprobación humana obligatoria

Requieren aprobación explícita:

* Publicación de contenido sensible.
* Uso de fuente débil en pieza relevante.
* Cambio de fuente a `trusted`.
* Bloqueo o rehabilitación de fuente.
* Escalamiento SEV-0/SEV-1.
* Nota pública de corrección.
* Retiro de contenido.
* Cambios a política editorial.

---

## 19. Playbooks de operación

## 19.1 Playbook: Ejecutar agente para crear brief

1. Seleccionar NewsItem.
2. Confirmar VerificationRecord.
3. Ejecutar EditorialAgent.
4. Generar EditorialBrief.
5. Ejecutar RiskAgent.
6. Revisar output.
7. Aceptar, editar o rechazar.
8. Registrar decisión.
9. Continuar a producción.

Criterios:

* No usar EditorialAgent si no existe fuente.
* No usar el brief como verificación.
* Brief en estado `proposed` hasta revisión.

---

## 19.2 Playbook: Ejecutar agente para validar fuente

1. Seleccionar SourceReference.
2. Ejecutar SourceValidatorAgent.
3. Revisar tipo de fuente.
4. Revisar trust recommendation.
5. Revisar señales de riesgo.
6. Aceptar o modificar clasificación.
7. Registrar SourceReview.
8. Escalar si es fuente sensible.

Criterios:

* El agente propone, no decide.
* Cambios críticos requieren aprobación humana.

---

## 19.3 Playbook: Ejecutar agente para clips

1. Seleccionar ContentPiece aprobado.
2. Confirmar nivel de evidencia.
3. Ejecutar SocialClipAgent.
4. Crear ChannelVariants.
5. Ejecutar RiskAgent por variante.
6. Revisar hooks.
7. Aprobar variantes.
8. Programar o publicar.

Criterios:

* No cambiar nivel de certeza.
* No quitar disclaimers si el tema lo requiere.
* No publicar directo.

---

## 19.4 Playbook: Ejecutar RiskAgent

1. Seleccionar ContentPiece o ChannelVariant.
2. Ejecutar RiskAgent.
3. Revisar riesgos detectados.
4. Clasificar severidad.
5. Ajustar contenido.
6. Escalar si aplica.
7. Registrar RiskReview.

Criterios:

* RiskAgent puede bloquear por política.
* Humano decide resolución.

---

## 19.5 Playbook: Ejecutar MemoryAgent

1. Seleccionar evento, incidente, fuente, métrica o decisión.
2. Ejecutar MemoryAgent.
3. Revisar propuesta.
4. Validar fuente.
5. Aceptar, editar o rechazar.
6. Guardar memoria aprobada.
7. Relacionar memoria con entidad.

Criterios:

* No guardar memoria sin fuente.
* No guardar rumor como hecho.
* No guardar aprendizaje sin valor futuro.

---

## 20. Manejo de errores de agentes

### 20.1 Tipos de error

| Error                     | Acción                           |
| ------------------------- | --------------------------------- |
| Fuente inventada          | Bloquear output, crear incidente  |
| Afirmación no verificada | Rechazar output                   |
| Exceso de certeza         | Editar o rechazar                 |
| Violación editorial      | Crear AgentIncident               |
| Output irrelevante        | Rechazar y registrar              |
| Error de clasificación   | Revisar manualmente               |
| Uso de memoria inválida  | Invalidar memoria, revisar agente |
| Fallo técnico            | Reintentar o escalar técnico     |
| Latencia excesiva         | Registrar métrica                |
| Costo excesivo            | Revisar configuración            |

---

### 20.2 Severidad

| Severidad | Descripción                                          |
| --------- | ----------------------------------------------------- |
| A-SEV-0   | Output causó publicación falsa o incidente crítico |
| A-SEV-1   | Output pudo causar daño si no se detecta             |
| A-SEV-2   | Output incorrecto corregible                          |
| A-SEV-3   | Output de baja calidad                                |
| A-SEV-4   | Error menor o técnico sin impacto                    |

---

### 20.3 Respuesta

Para A-SEV-0 / A-SEV-1:

* Bloquear output.
* Crear AgentIncident.
* Revisar prompt.
* Revisar memoria usada.
* Revisar fuente.
* Revisar si hubo publicación.
* Ejecutar postmortem si causó incidente editorial.
* Ajustar política o agente.

---

## 21. Reglas de seguridad editorial

### 21.1 Bloqueos automáticos recomendados

Bloquear output si:

* No tiene fuente y afirma hechos.
* Usa fuente bloqueada.
* Dice “confirmado” sin VerificationRecord.
* Recomienda comprar o vender.
* Acusa a persona o empresa sin evidencia.
* Cambia nivel de certeza.
* Omite disclaimer requerido.
* Usa memoria como fuente factual.
* Publica rumor como hecho.
* Propone retirar contenido sin escalamiento.

---

### 21.2 Advertencias automáticas recomendadas

Generar warning si:

* Fuente social es única fuente.
* Hay información preliminar.
* El contenido toca precio o inversión.
* El canal es corto y el tema requiere contexto.
* El hook tiene lenguaje fuerte.
* Hay contradicción entre fuentes.
* La noticia es vieja o posible reciclaje.
* La memoria usada está vieja.

---

## 22. Configuración operativa mínima por agente

Cada agente debe tener:

```text
agent_key
purpose
allowed_tasks
forbidden_tasks
input_schema
output_schema
required_context
review_required_rules
risk_level
default_autonomy_level
owner
version
status
```

Ejemplo:

```yaml
agent_key: editorial-agent
purpose: crear briefs y borradores editoriales
default_autonomy_level: A2
risk_level: high
allowed_tasks:
  - create_editorial_brief
  - draft_content_piece
  - propose_headlines
forbidden_tasks:
  - publish_content
  - approve_verification
  - invent_sources
  - save_memory_without_approval
review_required_rules:
  - sensitive_topic
  - high_risk
  - market_content
  - legal_or_regulatory
```

---

## 23. Vistas recomendadas en XMIP

### 23.1 Agent Operations Board

Debe mostrar:

* Agentes activos.
* Estado.
* Últimas ejecuciones.
* Fallas.
* Outputs pendientes de revisión.
* Riesgos.
* Costos estimados.

---

### 23.2 Agent Output Review Queue

Debe mostrar:

* Outputs propuestos.
* Entidad relacionada.
* Agente.
* Riesgo.
* Estado.
* Revisión requerida.
* Acciones: aceptar, editar, rechazar, escalar.

---

### 23.3 Agent Incident Board

Debe mostrar:

* Incidentes por agente.
* Severidad.
* Estado.
* Output afectado.
* Resolución.
* Postmortem si aplica.

---

### 23.4 Agent Metrics Dashboard

Debe mostrar:

* Ejecuciones.
* Tasa de éxito.
* Outputs aceptados.
* Outputs rechazados.
* Fallas.
* Latencia.
* Costo estimado.
* Violaciones de política.

---

## 24. Checklist antes de ejecutar un agente

* [ ] ¿La tarea corresponde al agente?
* [ ] ¿Existe entidad base?
* [ ] ¿Existe fuente si se trabajarán hechos?
* [ ] ¿Existe VerificationRecord si se hará contenido?
* [ ] ¿El agente tiene permisos para esta tarea?
* [ ] ¿El nivel de autonomía es adecuado?
* [ ] ¿La salida requiere revisión humana?
* [ ] ¿Hay memoria relevante y válida?
* [ ] ¿Hay riesgo editorial?
* [ ] ¿Existe correlation_id?

---

## 25. Checklist para revisar output de agente

* [ ] ¿El output responde a la tarea?
* [ ] ¿No inventa fuentes?
* [ ] ¿No agrega hechos no verificados?
* [ ] ¿Respeta nivel de evidencia?
* [ ] ¿Respeta guía de estilo?
* [ ] ¿No exagera?
* [ ] ¿No recomienda inversión?
* [ ] ¿Incluye disclaimer si aplica?
* [ ] ¿Identifica incertidumbre?
* [ ] ¿Tiene entidad relacionada?
* [ ] ¿Tiene estado correcto?
* [ ] ¿Debe aceptarse, editarse, rechazarse o escalarse?

---

## 26. Checklist de cierre de ejecución

* [ ] AgentExecution registrado.
* [ ] AgentOutput registrado.
* [ ] Estado asignado.
* [ ] Revisión completada si aplica.
* [ ] AuditEvent generado.
* [ ] Métricas actualizadas.
* [ ] Incidente creado si aplica.
* [ ] Memoria evaluada si aplica.
* [ ] Relaciones de conocimiento creadas si aplica.

---

## 27. Riesgos de operación de agentes

| Riesgo                             | Impacto | Probabilidad | Mitigación                  |
| ---------------------------------- | ------: | -----------: | ---------------------------- |
| Agente inventa fuente              |    Alto |        Media | SourceReference obligatorio  |
| Agente aumenta certeza             |    Alto |        Media | RiskAgent y policy check     |
| Output se publica sin revisión    |    Alto |        Media | ApprovalRecord obligatorio   |
| Memoria contamina contexto         |    Alto |        Media | Memoria con aprobación      |
| Agente usa fuente bloqueada        |    Alto |         Baja | Policy check                 |
| Agente optimiza para hype          |    Alto |        Media | Guía editorial y RiskAgent  |
| Agente clasifica mal prioridad     |   Medio |        Media | Revisión humana             |
| Agente genera muchas piezas pobres |   Medio |         Alta | Métricas de aceptación     |
| Costo operativo invisible          |   Medio |        Media | Cost estimate por ejecución |
| Dependencia excesiva del agente    |   Medio |        Media | Human-in-the-loop            |

---

## 28. Antipatrones prohibidos

XCripto debe evitar:

* Publicar outputs de agentes sin revisión.
* Tratar output de agente como fuente.
* Permitir agentes con permisos globales.
* Usar un solo agente para todo.
* Guardar toda salida como memoria.
* No versionar agentes/prompts.
* No auditar ejecuciones.
* No medir calidad de outputs.
* Culpar al agente sin revisar proceso.
* Usar agentes para saltarse verificación.
* Optimizar agentes para volumen, no calidad.
* Mezclar roles de verificación y publicación.
* Permitir que el agente decida en temas críticos.
* No registrar incidentes de agente.

---

## 29. Relación con XMIP

XMIP debe soportar la operación de agentes mediante:

* Agent Registry.
* Agent Versions.
* Agent Executions.
* Agent Outputs.
* Agent Policy Checks.
* Agent Incidents.
* Agent Metrics.
* Output Review Queue.
* Approval Records.
* Audit Events.
* Memory Usage Logs.
* Source Usage Logs.
* Knowledge Relationships.
* Cost Events.

La operación de agentes debe ser visible, trazable y gobernada.

---

## 30. Criterios de aceptación

Este documento se considera aceptado cuando:

* [ ] Define propósito de operación de agentes editoriales.
* [ ] Define catálogo operativo de agentes.
* [ ] Define responsabilidades por agente.
* [ ] Define límites por agente.
* [ ] Define niveles de autonomía.
* [ ] Define flujos operativos de agentes.
* [ ] Define reglas de validación de outputs.
* [ ] Define límites editoriales obligatorios.
* [ ] Define reglas de memoria para agentes.
* [ ] Define datos mínimos en XMIP.
* [ ] Define relaciones de conocimiento.
* [ ] Define eventos de auditoría.
* [ ] Define métricas de agentes.
* [ ] Define supervisión humana.
* [ ] Define playbooks de operación.
* [ ] Define manejo de errores.
* [ ] Define reglas de seguridad editorial.
* [ ] Define configuración mínima por agente.
* [ ] Define vistas recomendadas.
* [ ] Define checklists.
* [ ] Define riesgos y mitigaciones.
* [ ] Define antipatrones.
* [ ] Define relación con XMIP.

---

## 31. Relación con otros documentos

Este documento se apoya en:

* ORION-014 — Arquitectura de Agentes.
* ORION-014A — Protocolo de Comunicación entre Agentes.
* ORION-014B — Especificación de Agentes Digitales.
* ORION-018 — Operaciones Diarias.
* ORION-020 — Runbook de Producción de Noticias.
* ORION-022 — Protocolo de Verificación Editorial.
* ORION-023 — Pipeline del Newsroom.
* ORION-025 — Distribución Multicanal.
* ORION-026 — Métricas Operativas.
* ORION-027 — Gestión de Incidentes Editoriales.

Este documento gobierna directamente:

* ORION-029 — Checklist Diario del Newsroom.
* Workflows editoriales multiagente.
* Backlog técnico de agentes.
* Reglas de revisión humana.

---

## 32. Próximos pasos

Después de aprobar ORION-028, continuar con:

1. ORION-029 — Checklist Diario del Newsroom.
2. Definir prompts operativos en `docs/007-prompts/`.
3. Crear workflows técnicos para agentes editoriales.
4. Derivar backlog de implementación.
5. Crear pruebas de aceptación por agente.

ORION-029 debe consolidar la operación diaria en una lista ejecutable para abrir, operar, publicar, revisar y cerrar el newsroom cada día.

---

## 33. Historial de cambios

| Versión | Fecha      | Cambio                                                | Autor            |
| -------- | ---------- | ----------------------------------------------------- | ---------------- |
| 1.0      | 2026-07-02 | Versión inicial de operación de agentes editoriales | Fernando Cuellar |
