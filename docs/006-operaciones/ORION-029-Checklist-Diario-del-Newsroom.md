# ORION-029 — Checklist Diario del Newsroom

**Nivel documental:** L4 — Operations
**Volumen:** 006-operaciones
**Proyecto:** ORION / XCripto / XMIP
**Versión:** 1.0
**Estado:** Draft
**Owner:** Fernando Cuellar
**Última actualización:** 2026-07-02
**Ruta sugerida:** `docs/006-operaciones/ORION-029-Checklist-Diario-del-Newsroom.md`

---

## 1. Propósito

Este documento define el checklist diario operativo del newsroom de XCripto.

Su propósito es consolidar en una lista ejecutable las actividades mínimas que deben realizarse cada día para abrir, operar, producir, verificar, publicar, distribuir, medir y cerrar la operación editorial.

ORION-029 responde a la pregunta:

> ¿Qué debe revisar y ejecutar XCripto todos los días para operar como agencia de noticias cripto con disciplina, trazabilidad y control editorial?

Este documento convierte los procesos operativos de `006-operaciones` en una rutina diaria verificable.

---

## 2. Alcance

Este checklist cubre:

* Apertura diaria del newsroom.
* Revisión de contexto.
* Monitoreo de fuentes.
* Intake de noticias.
* Validación editorial.
* Priorización.
* Producción de contenido.
* Operación de agentes.
* Revisión y aprobación.
* Publicación.
* Distribución multicanal.
* Métricas.
* Incidentes.
* Memoria editorial.
* Cierre diario.
* Preparación del día siguiente.

Este documento no reemplaza:

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
* ORION-028 — Operación de Agentes Editoriales.

Este documento es la lista diaria de ejecución.

---

## 3. Principio rector

El checklist diario de XCripto sigue este principio:

```text
Abrir con contexto.
Operar con fuentes.
Publicar con verificación.
Distribuir con trazabilidad.
Cerrar con aprendizaje.
```

Una jornada editorial no se considera completa solo porque se publicó contenido.

Se considera completa cuando:

* Las fuentes fueron revisadas.
* Las noticias importantes fueron priorizadas.
* Las piezas publicadas fueron verificadas.
* Las publicaciones quedaron registradas.
* Las métricas fueron capturadas.
* Los incidentes fueron atendidos.
* La memoria útil fue evaluada.
* El día siguiente quedó preparado.

---

## 4. Definición de día operativo completo

Un día operativo completo de XCripto debe cubrir este flujo:

```text
apertura
→ monitoreo
→ intake
→ verificación
→ priorización
→ producción
→ revisión
→ publicación
→ distribución
→ métricas
→ incidentes
→ memoria
→ cierre
```

Si alguna etapa crítica queda incompleta, debe registrarse como pendiente.

---

## 5. Roles responsables

| Rol                      | Responsabilidad diaria                                                                   |
| ------------------------ | ---------------------------------------------------------------------------------------- |
| Owner / Editor Principal | Aprobar prioridades, temas sensibles, incidentes y decisiones críticas                  |
| Operador de Newsroom     | Ejecutar checklist, mover estados, coordinar pipeline                                    |
| Revisor Editorial        | Validar precisión, tono, fuente, riesgo y aprobación                                   |
| Productor de Contenido   | Crear piezas, guiones, clips, captions y adaptaciones                                    |
| Agentes XMIP             | Apoyar detección, validación, producción, riesgo, distribución, memoria y auditoría |

---

## 6. Agentes involucrados

| Agente               | Uso diario                              |
| -------------------- | --------------------------------------- |
| NewsScoutAgent       | Detectar señales y noticias candidatas |
| SourceValidatorAgent | Revisar fuentes                         |
| MarketImpactAgent    | Clasificar impacto y prioridad          |
| EditorialAgent       | Crear briefs y borradores               |
| ScriptAgent          | Crear guiones                           |
| SocialClipAgent      | Crear variantes para redes              |
| DistributionAgent    | Proponer distribución                  |
| RiskAgent            | Detectar riesgos                        |
| AuditAgent           | Validar trazabilidad                    |
| MemoryAgent          | Proponer memoria útil                  |
| KnowledgeAgent       | Relacionar entidades                    |
| CalendarAgent        | Revisar calendario                      |
| MetricsAgent         | Analizar desempeño cuando aplique      |

---

# 7. Checklist 1 — Apertura del newsroom

## 7.1 Objetivo

Iniciar la operación diaria con contexto, foco y prioridades.

## 7.2 Checklist

* [ ] Confirmar fecha operativa.
* [ ] Confirmar responsable del día.
* [ ] Revisar calendario editorial.
* [ ] Revisar piezas programadas para hoy.
* [ ] Revisar pendientes del día anterior.
* [ ] Revisar noticias en estado `monitoring`.
* [ ] Revisar incidentes abiertos.
* [ ] Revisar fuentes en watchlist/restricted.
* [ ] Revisar eventos macro, regulatorios o cripto programados.
* [ ] Revisar narrativa principal del mercado.
* [ ] Definir foco editorial del día.
* [ ] Crear o actualizar `Daily Editorial Context`.

## 7.3 Salida esperada

```text
Daily Editorial Context
```

## 7.4 Criterios de aceptación

* [ ] El día tiene foco editorial.
* [ ] Los pendientes están identificados.
* [ ] Los eventos relevantes están visibles.
* [ ] Los riesgos del día están marcados.
* [ ] El calendario fue revisado.

---

# 8. Checklist 2 — Revisión de fuentes

## 8.1 Objetivo

Confirmar que las fuentes críticas están disponibles, clasificadas y sin alertas relevantes.

## 8.2 Checklist

* [ ] Revisar fuentes primarias prioritarias.
* [ ] Revisar medios cripto confiables.
* [ ] Revisar fuentes regulatorias relevantes.
* [ ] Revisar fuentes on-chain si aplica.
* [ ] Revisar fuentes de mercado.
* [ ] Revisar fuentes sociales oficiales.
* [ ] Revisar fuentes en watchlist.
* [ ] Confirmar que no se usen fuentes bloqueadas.
* [ ] Registrar fuentes nuevas detectadas.
* [ ] Clasificar fuentes nuevas.
* [ ] Marcar fuentes dudosas para revisión.
* [ ] Crear `SourceReview` cuando aplique.

## 8.3 Salida esperada

```text
Source Review Summary
```

## 8.4 Criterios de aceptación

* [ ] Toda fuente nueva tiene registro.
* [ ] Toda fuente usada tiene tipo asignado.
* [ ] No hay fuente bloqueada en uso.
* [ ] Fuentes sensibles fueron revisadas.
* [ ] Fuentes dudosas quedaron en watchlist/restricted.

---

# 9. Checklist 3 — Intake de noticias

## 9.1 Objetivo

Detectar, registrar y ordenar señales informativas relevantes.

## 9.2 Checklist

* [ ] Ejecutar o revisar señales de NewsScoutAgent.
* [ ] Registrar señales relevantes.
* [ ] Crear `NewsItem` para cada señal útil.
* [ ] Asignar título preliminar.
* [ ] Asignar categoría preliminar.
* [ ] Asignar fuente inicial.
* [ ] Asignar estado `detected`.
* [ ] Crear `correlation_id`.
* [ ] Detectar duplicados.
* [ ] Descartar ruido evidente.
* [ ] Marcar posibles P0/P1.
* [ ] Marcar posibles rumores.
* [ ] Marcar noticias que requieren seguimiento.

## 9.3 Salida esperada

```text
Candidate News Queue
```

## 9.4 Criterios de aceptación

* [ ] Toda señal útil tiene `NewsItem`.
* [ ] Todo `NewsItem` tiene fuente inicial.
* [ ] Todo `NewsItem` tiene categoría preliminar.
* [ ] Todo `NewsItem` tiene `correlation_id`.
* [ ] Duplicados fueron revisados.
* [ ] Rumores fueron marcados como tal.

---

# 10. Checklist 4 — Clasificación y prioridad

## 10.1 Objetivo

Clasificar noticias por categoría, riesgo, prioridad y formato potencial.

## 10.2 Checklist

* [ ] Ejecutar MarketImpactAgent si aplica.
* [ ] Asignar categoría editorial.
* [ ] Asignar prioridad P0-P4.
* [ ] Asignar tipo editorial.
* [ ] Identificar activos, proyectos o entidades relacionadas.
* [ ] Identificar riesgo preliminar.
* [ ] Identificar si requiere escalamiento.
* [ ] Marcar lead story candidata.
* [ ] Crear lista preliminar de Top 5 noticias.
* [ ] Registrar motivo de prioridad.
* [ ] Actualizar estado del `NewsItem`.

## 10.3 Prioridades

```text
P0 — Breaking / alto impacto
P1 — Principal del día
P2 — Relevante secundaria
P3 — Seguimiento
P4 — Ruido / descarte
```

## 10.4 Salida esperada

```text
Classified News Queue
```

## 10.5 Criterios de aceptación

* [ ] Toda noticia candidata tiene categoría.
* [ ] Toda noticia candidata tiene prioridad.
* [ ] Toda P0/P1 tiene responsable.
* [ ] Toda noticia sensible tiene riesgo preliminar.
* [ ] Toda noticia descartada tiene motivo.

---

# 11. Checklist 5 — Verificación editorial

## 11.1 Objetivo

Determinar qué noticias pueden publicarse como hecho, cuáles requieren lenguaje condicionado, cuáles quedan en monitoreo y cuáles deben descartarse.

## 11.2 Checklist

* [ ] Ejecutar SourceValidatorAgent.
* [ ] Buscar fuente primaria.
* [ ] Confirmar fecha.
* [ ] Revisar si es noticia vieja reciclada.
* [ ] Revisar fuentes secundarias confiables.
* [ ] Revisar información contradictoria.
* [ ] Asignar nivel de evidencia E0-E5.
* [ ] Asignar nivel de confianza C0-C5.
* [ ] Asignar estado de verificación.
* [ ] Ejecutar RiskAgent para temas sensibles.
* [ ] Crear `VerificationRecord`.
* [ ] Escalar si corresponde.
* [ ] Bloquear publicación si la verificación es insuficiente.

## 11.3 Estados permitidos

```text
unverified
validating
verified
partially_verified
rumor
contradicted
rejected
escalated
monitoring
outdated
```

## 11.4 Salida esperada

```text
Verification Records
```

## 11.5 Criterios de aceptación

* [ ] Toda noticia publicable tiene `VerificationRecord`.
* [ ] Ningún rumor pasa como hecho.
* [ ] Toda noticia sensible fue escalada si corresponde.
* [ ] Toda noticia tiene nivel de evidencia.
* [ ] Toda noticia tiene nivel de confianza.
* [ ] AuditAgent puede reconstruir la verificación.

---

# 12. Checklist 6 — Priorización editorial final

## 12.1 Objetivo

Definir qué se produce hoy y qué queda en monitoreo.

## 12.2 Checklist

* [ ] Revisar noticias verificadas.
* [ ] Revisar noticias parcialmente verificadas.
* [ ] Revisar P0/P1.
* [ ] Definir lead story.
* [ ] Definir Top 5 noticias.
* [ ] Definir noticias secundarias.
* [ ] Definir alertas.
* [ ] Definir notas de seguimiento.
* [ ] Definir piezas evergreen si hay espacio.
* [ ] Definir formato por noticia.
* [ ] Definir canal principal.
* [ ] Asignar responsables.
* [ ] Actualizar calendario editorial.

## 12.3 Salida esperada

```text
Daily Editorial Priority List
```

## 12.4 Criterios de aceptación

* [ ] Lead story definida o explícitamente descartada.
* [ ] Top 5 definido.
* [ ] Cada pieza tiene responsable.
* [ ] Cada pieza tiene formato sugerido.
* [ ] Cada pieza tiene estado actualizado.
* [ ] Noticias no publicables quedaron en monitoring/rejected.

---

# 13. Checklist 7 — Producción de contenido

## 13.1 Objetivo

Convertir noticias priorizadas en briefs, guiones, posts, clips o piezas editoriales.

## 13.2 Checklist

* [ ] Crear brief editorial para cada noticia principal.
* [ ] Ejecutar EditorialAgent.
* [ ] Crear titular preliminar.
* [ ] Crear resumen.
* [ ] Separar hechos de análisis.
* [ ] Incluir fuentes.
* [ ] Incluir riesgos.
* [ ] Crear pieza base.
* [ ] Crear guion si aplica.
* [ ] Ejecutar ScriptAgent para video.
* [ ] Ejecutar SocialClipAgent para clips.
* [ ] Crear variantes por canal si aplica.
* [ ] Incluir disclaimers cuando aplique.
* [ ] Crear `ContentPiece`.
* [ ] Registrar outputs de agentes.

## 13.3 Salidas posibles

```text
EditorialBrief
ContentPiece
VideoScript
ShortScript
SocialPost
NewsletterItem
ArticleDraft
ChannelVariant
```

## 13.4 Criterios de aceptación

* [ ] Toda pieza tiene fuente.
* [ ] Toda pieza tiene estado.
* [ ] Toda pieza tiene responsable.
* [ ] Toda pieza conserva nivel de verificación.
* [ ] Toda salida de agente fue registrada.
* [ ] Ninguna pieza sensible queda sin revisión.

---

# 14. Checklist 8 — Revisión editorial

## 14.1 Objetivo

Evitar errores antes de aprobación y publicación.

## 14.2 Checklist

* [ ] Revisar titular.
* [ ] Revisar fuente.
* [ ] Revisar fecha.
* [ ] Revisar contexto.
* [ ] Revisar separación hecho/análisis/opinión.
* [ ] Revisar lenguaje de certeza.
* [ ] Revisar si hay recomendación financiera implícita.
* [ ] Revisar disclaimers.
* [ ] Ejecutar RiskAgent.
* [ ] Ejecutar AuditAgent.
* [ ] Corregir inconsistencias.
* [ ] Escalar si el riesgo es alto.
* [ ] Aprobar, regresar, rechazar o mantener en hold.
* [ ] Crear `ApprovalRecord` si se aprueba.

## 14.3 Decisiones posibles

```text
approve
revise
reject
hold
escalate
```

## 14.4 Criterios de aceptación

* [ ] Toda pieza aprobada tiene `ApprovalRecord`.
* [ ] Toda pieza sensible tiene revisión humana.
* [ ] Todo riesgo fue evaluado.
* [ ] AuditAgent no detecta faltantes críticos.
* [ ] El estado fue actualizado.

---

# 15. Checklist 9 — Publicación

## 15.1 Objetivo

Publicar o programar piezas aprobadas con trazabilidad completa.

## 15.2 Checklist

* [ ] Confirmar que la pieza está aprobada.
* [ ] Confirmar canal principal.
* [ ] Confirmar metadata.
* [ ] Confirmar assets.
* [ ] Confirmar descripción/caption.
* [ ] Confirmar disclaimer.
* [ ] Confirmar horario de publicación.
* [ ] Publicar o programar.
* [ ] Capturar URL o ID de publicación.
* [ ] Crear `PublicationRecord`.
* [ ] Actualizar estado a `published` o `scheduled`.
* [ ] Generar evento de auditoría.

## 15.3 Canales posibles

```text
YouTube
YouTube Shorts
TikTok
Instagram Reels
X / Twitter
LinkedIn
Newsletter
Blog / Web
Telegram
Discord
```

## 15.4 Criterios de aceptación

* [ ] Toda publicación tiene URL o ID.
* [ ] Toda publicación tiene canal.
* [ ] Toda publicación tiene responsable.
* [ ] Toda publicación tiene `PublicationRecord`.
* [ ] Toda publicación tiene `correlation_id`.
* [ ] Ninguna pieza se publicó sin aprobación.

---

# 16. Checklist 10 — Distribución multicanal

## 16.1 Objetivo

Adaptar y distribuir contenido sin perder coherencia, fuente ni nivel de evidencia.

## 16.2 Checklist

* [ ] Crear o revisar `DistributionPlan`.
* [ ] Definir canal principal.
* [ ] Definir canales secundarios.
* [ ] Crear variantes por canal.
* [ ] Revisar que cada variante conserve el sentido original.
* [ ] Revisar que cada variante conserve nivel de certeza.
* [ ] Revisar hooks.
* [ ] Revisar captions.
* [ ] Revisar links.
* [ ] Revisar disclaimers.
* [ ] Publicar o programar variantes.
* [ ] Registrar URLs.
* [ ] Crear `DistributionRecord`.
* [ ] Programar métricas por canal.

## 16.3 Criterios de aceptación

* [ ] No hay copia mecánica entre canales.
* [ ] Cada variante tiene fuente interna.
* [ ] Cada variante tiene estado.
* [ ] Cada variante tiene URL o ID si fue publicada.
* [ ] Cada variante está conectada con ContentPiece.
* [ ] Cada variante sensible fue revisada.

---

# 17. Checklist 11 — Métricas del día

## 17.1 Objetivo

Registrar desempeño operativo y señales de calidad.

## 17.2 Checklist

* [ ] Registrar publicaciones del día.
* [ ] Registrar métricas iniciales disponibles.
* [ ] Revisar métricas de 1 hora de publicaciones recientes.
* [ ] Revisar métricas de 24 horas de publicaciones previas.
* [ ] Revisar métricas de 7 días cuando aplique.
* [ ] Revisar publicaciones sin métricas.
* [ ] Revisar publicaciones sin URL.
* [ ] Revisar piezas con bajo desempeño anormal.
* [ ] Revisar comentarios relevantes.
* [ ] Registrar `MetricSnapshot`.
* [ ] Crear alertas si hay anomalías.

## 17.3 Métricas mínimas

```text
publications_created
published_url_capture_rate
verification_records_created
source_usage_count
corrections_count
distribution_by_channel
metric_snapshots_created
incident_count
```

## 17.4 Criterios de aceptación

* [ ] Métricas críticas registradas.
* [ ] Publicaciones sin URL fueron corregidas.
* [ ] Publicaciones sin métricas quedaron marcadas.
* [ ] Anomalías fueron registradas.
* [ ] Métricas se conectan con publicación/canal.

---

# 18. Checklist 12 — Revisión de incidentes

## 18.1 Objetivo

Detectar, registrar y atender errores editoriales, operativos o de agentes.

## 18.2 Checklist

* [ ] Revisar incidentes abiertos.
* [ ] Revisar alertas críticas.
* [ ] Revisar correcciones pendientes.
* [ ] Revisar publicaciones con comentarios problemáticos.
* [ ] Revisar fuentes problemáticas.
* [ ] Revisar outputs de agentes rechazados.
* [ ] Registrar nuevos IncidentRecord si aplica.
* [ ] Clasificar severidad.
* [ ] Escalar SEV-0 / SEV-1.
* [ ] Ejecutar corrección o retiro si aplica.
* [ ] Registrar acciones.
* [ ] Actualizar estado.
* [ ] Crear postmortem si aplica.

## 18.3 Severidades

```text
SEV-0 — Crítico
SEV-1 — Alto
SEV-2 — Medio
SEV-3 — Bajo
SEV-4 — Observación
```

## 18.4 Criterios de aceptación

* [ ] Todo incidente tiene estado.
* [ ] Todo incidente tiene owner.
* [ ] Todo SEV-0/SEV-1 fue escalado.
* [ ] Toda corrección material fue registrada.
* [ ] Todo retiro fue aprobado.
* [ ] Todo incidente grave tiene postmortem pendiente o completado.

---

# 19. Checklist 13 — Operación de agentes

## 19.1 Objetivo

Supervisar que los agentes operen con trazabilidad, límites y utilidad real.

## 19.2 Checklist

* [ ] Revisar ejecuciones de agentes del día.
* [ ] Revisar outputs pendientes.
* [ ] Revisar outputs rechazados.
* [ ] Revisar outputs bloqueados por política.
* [ ] Revisar posibles fuentes inventadas.
* [ ] Revisar outputs con riesgo alto.
* [ ] Revisar uso de memoria por agentes.
* [ ] Revisar costos estimados si están disponibles.
* [ ] Revisar latencias o fallas.
* [ ] Registrar AgentIncident si aplica.
* [ ] Actualizar métricas de agentes.
* [ ] Ajustar prompts o reglas si hubo fallas.

## 19.3 Criterios de aceptación

* [ ] Toda ejecución tiene `AgentExecution`.
* [ ] Todo output tiene estado.
* [ ] Todo output sensible fue revisado.
* [ ] Ningún output de agente fue publicado sin aprobación.
* [ ] Incidentes de agente fueron registrados.
* [ ] Métricas de agentes fueron actualizadas.

---

# 20. Checklist 14 — Memoria editorial

## 20.1 Objetivo

Guardar solo aprendizaje útil y evitar contaminar el contexto.

## 20.2 Checklist

* [ ] Revisar memorias propuestas por MemoryAgent.
* [ ] Revisar fuente de cada memoria.
* [ ] Rechazar memorias sin fuente.
* [ ] Rechazar rumores como memoria factual.
* [ ] Aprobar memorias útiles.
* [ ] Invalidar memorias obsoletas si aplica.
* [ ] Relacionar memoria con noticia, fuente, incidente o métrica.
* [ ] Registrar motivo de aprobación o rechazo.
* [ ] Crear relaciones de conocimiento.

## 20.3 Tipos de memoria

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

## 20.4 Criterios de aceptación

* [ ] Toda memoria aprobada tiene fuente.
* [ ] Toda memoria aprobada tiene tipo.
* [ ] Toda memoria aprobada tiene relación.
* [ ] Toda memoria rechazada tiene motivo.
* [ ] No se guardó ruido temporal.
* [ ] No se guardó rumor como hecho.

---

# 21. Checklist 15 — Cierre operativo diario

## 21.1 Objetivo

Cerrar el día con trazabilidad, pendientes claros y aprendizaje registrado.

## 21.2 Checklist

* [ ] Revisar publicaciones realizadas.
* [ ] Confirmar URLs registradas.
* [ ] Confirmar métricas iniciales.
* [ ] Revisar piezas pendientes.
* [ ] Revisar piezas programadas.
* [ ] Revisar noticias en monitoring.
* [ ] Revisar incidentes abiertos.
* [ ] Revisar memoria aprobada.
* [ ] Revisar tareas de seguimiento.
* [ ] Registrar cierre del día.
* [ ] Preparar foco preliminar para mañana.
* [ ] Actualizar calendario.
* [ ] Generar `Daily Closing Record`.

## 21.3 Salida esperada

```text
Daily Closing Record
```

## 21.4 Criterios de aceptación

* [ ] El día tiene registro de cierre.
* [ ] Publicaciones están registradas.
* [ ] Pendientes están visibles.
* [ ] Incidentes están actualizados.
* [ ] Memoria fue evaluada.
* [ ] El siguiente día tiene punto de partida.

---

# 22. Checklist rápido para día mínimo

Este checklist se usa cuando no hay capacidad para ejecutar el flujo completo, pero el newsroom debe mantener disciplina mínima.

* [ ] Revisar contexto del día.
* [ ] Detectar Top 5 noticias candidatas.
* [ ] Registrar fuentes.
* [ ] Verificar al menos noticias P0/P1.
* [ ] Producir resumen editorial.
* [ ] Publicar solo piezas aprobadas.
* [ ] Registrar URLs.
* [ ] Revisar incidentes.
* [ ] Guardar memoria útil.
* [ ] Cerrar pendientes.

Criterio:

```text
Si no hay verificación, no hay publicación sensible.
```

---

# 23. Checklist para breaking news

Usar cuando aparece una noticia P0.

* [ ] Detectar señal.
* [ ] Registrar NewsItem.
* [ ] Confirmar fuente fuerte.
* [ ] Buscar fuente primaria.
* [ ] Validar fecha.
* [ ] Asignar estado de verificación.
* [ ] Escalar al Owner / Editor Principal.
* [ ] Redactar alerta limitada.
* [ ] Marcar claramente qué está confirmado.
* [ ] Marcar qué falta por confirmar.
* [ ] Agregar fuente.
* [ ] Publicar solo si hay aprobación.
* [ ] Registrar URL.
* [ ] Abrir seguimiento.
* [ ] Actualizar conforme cambie información.
* [ ] Archivar versiones.
* [ ] Evaluar postmortem si hubo presión o error.

---

# 24. Checklist de publicación sensible

Usar para hacks, regulación, exchanges, insolvencia, fraude, demandas, mercado o acusaciones.

* [ ] Fuente primaria revisada o ausencia justificada.
* [ ] Segunda fuente revisada si aplica.
* [ ] VerificationRecord completo.
* [ ] RiskAgent ejecutado.
* [ ] Revisión humana completada.
* [ ] Disclaimer incluido.
* [ ] Titular revisado.
* [ ] Lenguaje proporcional a evidencia.
* [ ] Aprobación registrada.
* [ ] Publicación registrada.
* [ ] Métricas programadas.
* [ ] Seguimiento abierto.

---

# 25. Checklist de calidad editorial

Antes de publicar cualquier pieza, validar:

* [ ] ¿El titular dice lo mismo que la evidencia permite?
* [ ] ¿La fuente existe?
* [ ] ¿La fecha es correcta?
* [ ] ¿La pieza separa hecho, análisis y opinión?
* [ ] ¿Hay contexto suficiente?
* [ ] ¿Se evita recomendación financiera?
* [ ] ¿Se evita hype?
* [ ] ¿Se marca incertidumbre?
* [ ] ¿Hay disclaimer si aplica?
* [ ] ¿El canal es adecuado?
* [ ] ¿La pieza puede defenderse si alguien pregunta por la fuente?

---

# 26. Datos mínimos en XMIP

## 26.1 DailyNewsroomRun

```text
daily_run_id
date
owner
status
opening_context
closing_summary
published_count
incident_count
pending_count
memory_count
correlation_id
metadata
```

## 26.2 DailyChecklistItem

```text
checklist_item_id
daily_run_id
section
item
status
completed_by
completed_at
notes
correlation_id
```

## 26.3 DailyClosingRecord

```text
closing_record_id
daily_run_id
summary
published_items
pending_items
incidents
metrics_summary
memory_summary
next_day_focus
created_at
created_by
correlation_id
```

## 26.4 DailyEditorialContext

```text
context_id
daily_run_id
date
market_context
active_narratives
scheduled_events
editorial_focus
risks
watchlist_items
created_at
correlation_id
```

---

# 27. Eventos de auditoría

## 27.1 Eventos mínimos

| Evento                         | Cuándo ocurre              |
| ------------------------------ | --------------------------- |
| daily_newsroom_opened          | Se abre operación diaria   |
| daily_context_created          | Se crea contexto diario     |
| daily_checklist_item_completed | Se completa punto           |
| daily_priority_list_created    | Se define prioridad         |
| daily_publication_completed    | Se publica pieza            |
| daily_incident_reviewed        | Se revisa incidente         |
| daily_memory_reviewed          | Se revisa memoria           |
| daily_newsroom_closed          | Se cierra operación diaria |

## 27.2 Evento mínimo

```json
{
  "event_type": "daily_newsroom_closed",
  "daily_run_id": "daily_20260702",
  "actor_type": "user",
  "actor_ref": "operator",
  "status": "success",
  "published_count": 5,
  "incident_count": 0,
  "pending_count": 3,
  "correlation_id": "corr_20260702_daily",
  "occurred_at": "2026-07-02T23:59:00Z"
}
```

---

# 28. Métricas del checklist diario

| Métrica                            | Propósito                     |
| ----------------------------------- | ------------------------------ |
| `daily_checklist_completion_rate` | Medir disciplina diaria        |
| `daily_publications_count`        | Medir producción              |
| `daily_verified_news_count`       | Medir calidad de verificación |
| `daily_incidents_count`           | Medir riesgos                  |
| `daily_pending_items_count`       | Medir carga pendiente          |
| `daily_memory_approved_count`     | Medir aprendizaje              |
| `daily_sources_reviewed_count`    | Medir cobertura                |
| `daily_agent_outputs_reviewed`    | Medir control de agentes       |
| `daily_metrics_captured_count`    | Medir cierre operativo         |
| `daily_closing_completed`         | Confirmar cierre               |

Metas iniciales:

| Métrica                           | Meta |
| ---------------------------------- | ---: |
| Checklist crítico completado      | 100% |
| Publicaciones con fuente           | 100% |
| Publicaciones con URL              | 100% |
| Piezas sensibles con revisión     | 100% |
| Rumores publicados como hechos     |    0 |
| Cierre diario registrado           | 100% |
| Incidentes SEV-0/SEV-1 sin escalar |    0 |

---

# 29. Reglas de excepción

## 29.1 Si no hay noticias fuertes

Acción:

* Priorizar contenido educativo.
* Revisar evergreen.
* Crear análisis de contexto.
* Preparar seguimiento.
* No forzar noticia débil.

## 29.2 Si hay demasiadas noticias

Acción:

* Priorizar P0/P1.
* Limitar Top 5.
* Dejar P2/P3 en seguimiento.
* No sacrificar verificación por volumen.

## 29.3 Si falla un agente

Acción:

* Continuar manualmente.
* Registrar AgentIncident.
* No usar output dudoso.
* Revisar prompt o memoria.

## 29.4 Si falta verificación

Acción:

* No publicar como hecho.
* Marcar `monitoring` o `rumor`.
* Buscar fuente adicional.
* Escalar si es sensible.

## 29.5 Si aparece incidente durante publicación

Acción:

* Pausar distribución.
* Crear IncidentRecord.
* Escalar si aplica.
* Corregir o retirar.
* Registrar cierre.

---

# 30. Antipatrones prohibidos

XCripto debe evitar:

* Abrir el día sin contexto.
* Publicar sin fuente.
* Publicar sin VerificationRecord.
* Publicar output de agente sin revisión.
* Publicar rumor como hecho.
* Saltarse checklist por prisa.
* No registrar URL publicada.
* No revisar métricas.
* No cerrar incidentes.
* Guardar memoria sin fuente.
* Dejar piezas en limbo.
* Usar calendario como decoración.
* Confundir volumen con calidad.
* Cerrar el día sin pendientes claros.

---

# 31. Relación con XMIP

XMIP debe soportar este checklist mediante:

* Daily Newsroom Run.
* Daily Editorial Context.
* Checklist tracking.
* News Intake.
* Source Registry.
* Verification Records.
* Content Registry.
* Publication Records.
* Distribution Records.
* Metric Snapshots.
* Incident Records.
* Agent Execution Logs.
* Editorial Memory.
* Knowledge Relationships.
* Audit Events.

El checklist diario debe convertirse en una vista operativa central del newsroom.

---

# 32. Relación con otros documentos

Este documento se apoya en:

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
* ORION-028 — Operación de Agentes Editoriales.

Este documento cierra el volumen:

```text
006-operaciones
```

---

# 33. Criterios de aceptación

Este documento se considera aceptado cuando:

* [ ] Define propósito del checklist diario.
* [ ] Define día operativo completo.
* [ ] Define roles responsables.
* [ ] Define agentes involucrados.
* [ ] Define apertura del newsroom.
* [ ] Define revisión de fuentes.
* [ ] Define intake.
* [ ] Define clasificación.
* [ ] Define verificación.
* [ ] Define priorización.
* [ ] Define producción.
* [ ] Define revisión editorial.
* [ ] Define publicación.
* [ ] Define distribución.
* [ ] Define métricas.
* [ ] Define incidentes.
* [ ] Define operación de agentes.
* [ ] Define memoria editorial.
* [ ] Define cierre operativo.
* [ ] Define checklist rápido.
* [ ] Define checklist para breaking news.
* [ ] Define checklist para publicación sensible.
* [ ] Define checklist de calidad editorial.
* [ ] Define datos mínimos en XMIP.
* [ ] Define auditoría.
* [ ] Define métricas del checklist.
* [ ] Define reglas de excepción.
* [ ] Define antipatrones.
* [ ] Cierra coherentemente el volumen `006-operaciones`.

---

# 34. Próximos pasos

Después de aprobar ORION-029, continuar con:

1. Revisar consistencia completa de `006-operaciones`.
2. Actualizar `docs/INDEX.md`.
3. Crear prompts operativos en `docs/007-prompts/`.
4. Crear ADRs en `docs/008-decisiones/` si hay decisiones relevantes.
5. Derivar sprints en `docs/009-sprints/`.
6. Diseñar vistas iniciales de XMIP Newsroom.
7. Convertir checklists en workflows técnicos.

Documentos sugeridos para `007-prompts`:

```text
Prompt-NewsScoutAgent.md
Prompt-SourceValidatorAgent.md
Prompt-MarketImpactAgent.md
Prompt-EditorialAgent.md
Prompt-ScriptAgent.md
Prompt-SocialClipAgent.md
Prompt-RiskAgent.md
Prompt-AuditAgent.md
Prompt-MemoryAgent.md
Prompt-KnowledgeAgent.md
```

---

# 35. Historial de cambios

| Versión | Fecha      | Cambio                                             | Autor            |
| -------- | ---------- | -------------------------------------------------- | ---------------- |
| 1.0      | 2026-07-02 | Versión inicial del checklist diario del newsroom | Fernando Cuellar |
