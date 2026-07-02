# ORION-025 — Distribución Multicanal

**Nivel documental:** L4 — Operations
**Volumen:** 006-operaciones
**Proyecto:** ORION / XCripto / XMIP
**Versión:** 1.0
**Estado:** Draft
**Owner:** Fernando Cuellar
**Última actualización:** 2026-07-02
**Ruta sugerida:** `docs/006-operaciones/ORION-025-Distribucion-Multicanal.md`

---

## 1. Propósito

Este documento define el modelo operativo de distribución multicanal de XCripto.

Su propósito es establecer cómo una pieza editorial aprobada se adapta, publica, distribuye, mide y archiva en diferentes canales sin perder coherencia editorial, trazabilidad, fuente, contexto ni control de riesgo.

ORION-025 responde a la pregunta:

> ¿Cómo distribuye XCripto una noticia, análisis, guion o alerta en múltiples canales de forma consistente, útil y trazable?

La distribución multicanal no significa copiar y pegar el mismo contenido en todos lados.
Significa adaptar una misma unidad editorial al lenguaje, formato, profundidad y ritmo de cada canal.

---

## 2. Alcance

Este documento cubre:

* Principios de distribución.
* Canales oficiales de XCripto.
* Adaptación por canal.
* Formatos por canal.
* Reglas para YouTube.
* Reglas para YouTube Shorts.
* Reglas para TikTok.
* Reglas para Instagram Reels.
* Reglas para X / Twitter.
* Reglas para LinkedIn.
* Reglas para newsletter.
* Reglas para blog / web.
* Reglas para Telegram / Discord.
* Reglas de reutilización de contenido.
* Trazabilidad multicanal.
* Estados de distribución.
* Responsables.
* Agentes involucrados.
* Datos mínimos en XMIP.
* Métricas.
* Riesgos.
* Checklist operativo.

Este documento no cubre en detalle:

* Producción inicial de noticias.
* Verificación editorial.
* Calendario editorial.
* Métricas avanzadas.
* Gestión de incidentes.
* Operación detallada de agentes.

Esos temas se desarrollan en:

* ORION-020 — Runbook de Producción de Noticias.
* ORION-022 — Protocolo de Verificación Editorial.
* ORION-024 — Calendario Editorial.
* ORION-026 — Métricas Operativas.
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

Este documento gobierna directamente:

* ORION-026 — Métricas Operativas.
* ORION-027 — Gestión de Incidentes Editoriales.
* ORION-028 — Operación de Agentes Editoriales.
* ORION-029 — Checklist Diario del Newsroom.

---

## 4. Contexto operativo

XCripto produce contenido cripto en un entorno donde la audiencia consume información en distintos formatos:

* Video largo.
* Video corto.
* Posts rápidos.
* Hilos.
* Newsletter.
* Artículos.
* Alertas comunitarias.
* Clips derivados.
* Resúmenes ejecutivos.

Cada canal tiene una lógica distinta.

Un error común es pensar que distribuir significa publicar el mismo texto en todas partes. Eso degrada el contenido, reduce valor y rompe la experiencia de audiencia.

XCripto debe operar bajo esta lógica:

```text
pieza editorial aprobada
→ versión principal
→ variantes por canal
→ publicación
→ distribución secundaria
→ medición
→ aprendizaje
```

---

## 5. Principio rector de distribución

La distribución multicanal de XCripto sigue este principio:

```text
Una fuente editorial, múltiples formatos, una sola trazabilidad.
```

Esto significa:

* La noticia base debe conservar su fuente.
* Cada canal debe tener adaptación propia.
* El mensaje debe ser consistente.
* El nivel de evidencia no debe cambiar por canal.
* El riesgo editorial debe viajar con la pieza.
* Las métricas deben regresar al mismo registro editorial.

---

## 6. Objetivos de la distribución multicanal

La distribución multicanal busca:

1. Ampliar alcance sin perder precisión.
2. Adaptar contenido a cada audiencia.
3. Reutilizar piezas sin duplicar ruido.
4. Convertir guiones largos en clips útiles.
5. Convertir noticias en posts rápidos.
6. Convertir análisis en contenido profesional.
7. Convertir resúmenes en newsletter.
8. Mantener trazabilidad por canal.
9. Medir desempeño comparativo.
10. Alimentar memoria editorial sobre qué funciona.

---

## 7. Canales oficiales

### 7.1 Canales principales

| Canal           | Uso principal                                     |
| --------------- | ------------------------------------------------- |
| YouTube         | Noticiero, análisis, explicadores                |
| YouTube Shorts  | Clips rápidos, alertas, educativos cortos        |
| TikTok          | Clips rápidos, educación ligera, hooks fuertes  |
| Instagram Reels | Clips visuales, educativos, awareness             |
| X / Twitter     | Alertas, titulares, hilos, seguimiento            |
| LinkedIn        | Análisis profesional, regulación, institucional |
| Newsletter      | Curaduría, resumen, seguimiento                  |
| Blog / Web      | Archivo, SEO, artículos, análisis               |
| Telegram        | Alertas y comunidad                               |
| Discord         | Comunidad y seguimiento                           |

---

### 7.2 Canal principal por tipo de contenido

| Tipo de contenido   | Canal principal sugerido     |
| ------------------- | ---------------------------- |
| Noticiero           | YouTube                      |
| Breaking news       | X / Telegram                 |
| Alerta breve        | X / Telegram / Shorts        |
| Análisis largo     | YouTube / Blog / LinkedIn    |
| Explicador          | YouTube / Blog               |
| Clip educativo      | Shorts / TikTok / Reels      |
| Resumen semanal     | Newsletter / YouTube         |
| Regulación         | LinkedIn / Blog / Newsletter |
| Seguridad / hack    | X / Blog / YouTube           |
| Opinión editorial  | LinkedIn / YouTube / Blog    |
| Seguimiento de tema | X / Newsletter / Blog        |

---

## 8. Modelo de distribución

La distribución inicia solo cuando existe una pieza aprobada.

Flujo estándar:

```text
ContentPiece approved
→ Channel Strategy
→ Channel Variant
→ Channel Validation
→ Publication
→ Secondary Distribution
→ Metrics Capture
→ Memory Evaluation
```

---

## 9. Estados de distribución

| Estado      | Descripción                    |
| ----------- | ------------------------------- |
| pending     | Distribución pendiente         |
| adapting    | Adaptando al canal              |
| ready       | Variante lista                  |
| scheduled   | Programada                      |
| published   | Publicada                       |
| distributed | Distribuida en canal secundario |
| failed      | Falló publicación             |
| corrected   | Corregida                       |
| cancelled   | Cancelada                       |
| archived    | Archivada                       |

---

## 10. Reglas generales de distribución

### 10.1 No copiar y pegar sin adaptar

Cada canal requiere:

* Longitud distinta.
* Ritmo distinto.
* Profundidad distinta.
* CTA distinto.
* Nivel de contexto distinto.
* Formato visual distinto.

---

### 10.2 No cambiar el nivel de certeza

Si la noticia base está parcialmente verificada, ningún canal puede publicarla como confirmada.

Ejemplo incorrecto:

```text
Base: información preliminar.
Short: “Confirmado: hackean protocolo.”
```

Ejemplo correcto:

```text
Base: información preliminar.
Short: “Información preliminar apunta a posible incidente; aún falta confirmación oficial.”
```

---

### 10.3 No amplificar riesgo innecesario

Canales cortos tienden a exagerar.
El hook debe atraer sin distorsionar.

---

### 10.4 Cada variante debe conservar fuente interna

Aunque no siempre se muestre públicamente toda la fuente, XMIP debe registrar la fuente base.

---

### 10.5 Cada publicación debe regresar al mismo registro

Todas las variantes deben conectarse con:

```text
NewsItem
ContentPiece
SourceReference
VerificationRecord
PublicationRecord
MetricSnapshot
```

---

## 11. Adaptación por canal

### 11.1 YouTube

Uso:

* Noticiero.
* Análisis.
* Explicadores.
* Coberturas especiales.
* Resúmenes semanales.

Formato recomendado:

```text
8 a 15 minutos para noticiero
5 a 12 minutos para análisis
3 a 8 minutos para explicadores
```

Estructura recomendada:

```text
hook
contexto
noticia principal
impacto
bloques secundarios
explicación
cierre
disclaimer
```

Elementos obligatorios:

* Título.
* Descripción.
* Guion.
* Thumbnail brief.
* Fuentes internas.
* Capítulos si aplica.
* Disclaimer si aplica.
* Tags.
* Categoría.

Reglas:

* No prometer predicciones.
* No exagerar thumbnails.
* No usar lenguaje de compra/venta.
* Separar noticia de análisis.
* Incluir contexto suficiente.

---

### 11.2 YouTube Shorts

Uso:

* Clips derivados.
* Una noticia rápida.
* Concepto educativo.
* Alerta breve.
* Dato relevante.

Estructura recomendada:

```text
hook de 1 a 3 segundos
dato central
contexto mínimo
impacto
cierre
```

Reglas:

* Una sola idea por short.
* No meter demasiadas noticias.
* No exagerar incertidumbre.
* No publicar rumores como hechos.
* Evitar “se va a disparar”, “colapsó”, “garantizado”.

---

### 11.3 TikTok

Uso:

* Contenido educativo corto.
* Resumen rápido.
* Explicación simple.
* Noticia con hook fuerte.

Reglas:

* Lenguaje claro.
* Ritmo rápido.
* Hook visual o verbal fuerte.
* No sacrificar precisión.
* Evitar clickbait financiero.
* Agregar contexto en caption si es necesario.

---

### 11.4 Instagram Reels

Uso:

* Clips educativos.
* Awareness.
* Resumen visual.
* Contenido de marca.
* Piezas ligeras derivadas del noticiero.

Reglas:

* Cuidar visual.
* Mensaje simple.
* Hook claro.
* Caption útil.
* No saturar de datos.
* Mantener tono confiable.

---

### 11.5 X / Twitter

Uso:

* Alertas.
* Titulares.
* Hilos.
* Seguimiento de breaking news.
* Opinión editorial marcada.
* Distribución de links.

Formatos:

```text
alerta
post corto
hilo
seguimiento
comentario editorial
link post
```

Formato de alerta:

```text
ALERTA XCRIPTO:

[Hecho confirmado o información preliminar]

Contexto:
[1-2 líneas]

Impacto:
[1 línea]

Fuente:
[referencia si aplica]
```

Reglas:

* Incluir fuente cuando sea posible.
* Marcar rumor o información preliminar.
* No afirmar causalidad de mercado sin evidencia.
* No usar tono alarmista.
* Usar hilos para explicar temas complejos.

---

### 11.6 LinkedIn

Uso:

* Análisis profesional.
* Regulación.
* Institucional.
* Seguridad.
* Tendencias.
* Reflexiones de industria.
* Contexto ejecutivo.

Estructura recomendada:

```text
contexto
hecho principal
por qué importa
implicaciones
riesgos
pregunta abierta o cierre editorial
```

Reglas:

* Tono profesional.
* Menos hype.
* Más contexto.
* Evitar slang excesivo.
* Separar hecho y análisis.
* No publicar como si fuera señal de trading.

---

### 11.7 Newsletter

Uso:

* Curaduría.
* Resumen diario o semanal.
* Seguimiento de narrativas.
* Top noticias.
* Tema a vigilar.

Estructura recomendada:

```text
asunto
resumen ejecutivo
top noticias
impacto por noticia
tema a vigilar
links
cierre
disclaimer
```

Reglas:

* No saturar.
* Priorizar claridad.
* Mantener jerarquía.
* Incluir links.
* Evitar titulares engañosos.
* Diferenciar noticia, análisis y opinión.

---

### 11.8 Blog / Web

Uso:

* Archivo.
* Artículos.
* SEO.
* Explicadores.
* Reportes.
* Análisis evergreen.
* Páginas de referencia.

Estructura recomendada:

```text
título
slug
resumen
cuerpo
fuentes
categoría
tags
autor
fecha
disclaimer
```

Reglas:

* URL limpia.
* Fuente clara.
* Fecha visible.
* Posibilidad de actualización.
* Correcciones registradas.
* SEO sin sacrificar precisión.

---

### 11.9 Telegram

Uso:

* Alertas.
* Resúmenes.
* Links.
* Comunidad.
* Seguimiento rápido.

Reglas:

* Breve.
* Claro.
* Sin saturar.
* Evitar pánico.
* Fuente o link si aplica.
* Marcar información preliminar.

---

### 11.10 Discord

Uso:

* Comunidad.
* Discusión.
* Seguimiento.
* Feedback.
* Preguntas y respuestas.

Reglas:

* Evitar afirmaciones improvisadas.
* Moderar discusiones sensibles.
* Vincular a pieza completa.
* Marcar fuentes.
* No convertir conversación en publicación oficial sin pasar por pipeline.

---

## 12. Matriz de adaptación

| Pieza base       | YouTube             | Shorts/TikTok/Reels | X                | LinkedIn                  | Newsletter         | Blog                  |
| ---------------- | ------------------- | ------------------- | ---------------- | ------------------------- | ------------------ | --------------------- |
| Breaking news    | Cobertura posterior | Alerta breve        | Alerta principal | Solo si requiere contexto | Resumen            | Artículo actualizado |
| Noticia diaria   | Bloque de noticiero | Clip                | Post             | Breve si es profesional   | Top news           | Nota                  |
| Análisis        | Video               | Clip insight        | Hilo             | Post principal            | Resumen            | Artículo largo       |
| Educativo        | Video explicador    | Clip educativo      | Mini hilo        | Post conceptual           | Recurso            | Guía evergreen       |
| Regulación      | Video contexto      | Clip resumen        | Hilo             | Post principal            | Sección destacada | Artículo             |
| Hack / seguridad | Video explicativo   | Alerta controlada   | Alerta/hilo      | Análisis riesgo          | Resumen            | Reporte               |
| Newsletter       | Video resumen       | Clips               | Top tweets       | Extracto                  | Canal principal    | Archivo               |

---

## 13. Proceso operativo de distribución

### 13.1 Paso 1 — Confirmar pieza aprobada

Antes de distribuir, validar:

* ContentPiece aprobado.
* Fuente registrada.
* VerificationRecord existente.
* RiskReview completo.
* Canal principal definido.
* Disclaimers definidos si aplica.

Salida:

```text
Distribution Ready Content
```

---

### 13.2 Paso 2 — Definir estrategia de canal

Determinar:

* Canal principal.
* Canales secundarios.
* Formatos derivados.
* Prioridad.
* Timing.
* Riesgo por canal.
* Responsable.

Salida:

```text
Channel Distribution Plan
```

---

### 13.3 Paso 3 — Crear variantes por canal

Crear una variante específica para cada canal.

Campos mínimos:

```text
channel
format
title_or_hook
body_or_script
caption
cta
source_refs
risk_level
status
```

Salida:

```text
Channel Variants
```

---

### 13.4 Paso 4 — Validar variantes

Validar que cada variante:

* Respeta evidencia.
* No exagera.
* Conserva sentido.
* Tiene canal correcto.
* Tiene fuente interna.
* Tiene disclaimer si aplica.

Salida:

```text
Validated Channel Variants
```

---

### 13.5 Paso 5 — Publicar o programar

Publicar según calendario o urgencia.

Registrar:

```text
channel
published_url
published_at
published_by
status
correlation_id
```

Salida:

```text
PublicationRecord
```

---

### 13.6 Paso 6 — Registrar distribución

Cada variante debe quedar conectada con la pieza base.

Salida:

```text
DistributionRecord
```

---

### 13.7 Paso 7 — Medir desempeño

Registrar métricas por canal en ventanas mínimas:

```text
1 hora
24 horas
7 días
```

Salida:

```text
MetricSnapshot
```

---

### 13.8 Paso 8 — Guardar aprendizaje

Evaluar si la distribución deja memoria útil.

Ejemplos:

* Un hook funcionó.
* Un canal no respondió.
* Un formato generó confusión.
* Una audiencia pidió explicación.
* Un tema requiere seguimiento.

Salida:

```text
Distribution Memory
```

---

## 14. Reutilización de contenido

### 14.1 Reglas de reutilización

Una pieza puede reutilizarse si:

* Sigue vigente.
* No perdió contexto.
* La fuente sigue siendo válida.
* No hubo corrección posterior que cambie sentido.
* Se adapta al nuevo canal.
* Se registra como derivado.

---

### 14.2 Tipos de reutilización

| Tipo                 | Descripción                          |
| -------------------- | ------------------------------------- |
| clip_from_video      | Clip derivado de video largo          |
| thread_from_article  | Hilo derivado de artículo            |
| newsletter_from_news | Resumen en newsletter                 |
| short_from_analysis  | Insight corto derivado de análisis   |
| post_from_script     | Post derivado de guion                |
| evergreen_refresh    | Actualización de contenido evergreen |

---

### 14.3 Regla crítica

No reutilizar contenido viejo como si fuera noticia nueva.

Si es contenido actualizado, marcarlo como:

```text
actualización
seguimiento
contexto
recordatorio
evergreen
```

---

## 15. Trazabilidad multicanal

Toda distribución debe mantener relación con la pieza original.

Modelo mínimo:

```text
NewsItem
→ ContentPiece
→ ChannelVariant
→ PublicationRecord
→ DistributionRecord
→ MetricSnapshot
→ EditorialMemory
```

Cada canal debe conservar:

* Fuente.
* Estado de verificación.
* Riesgo.
* Responsable.
* Correlation ID.
* URL.
* Métricas.

---

## 16. Datos mínimos en XMIP

### 16.1 Channel

```text
channel_id
name
type
status
url
owner
content_rules
metadata
```

---

### 16.2 ChannelVariant

```text
variant_id
content_id
channel_id
format
title
body
caption
cta
status
risk_level
source_refs
created_by
reviewed_by
correlation_id
metadata
```

---

### 16.3 DistributionPlan

```text
distribution_plan_id
content_id
primary_channel
secondary_channels
priority
scheduled_at
owner
status
risk_level
correlation_id
metadata
```

---

### 16.4 DistributionRecord

```text
distribution_id
distribution_plan_id
variant_id
channel_id
published_url
published_at
status
published_by
correlation_id
metadata
```

---

### 16.5 MetricSnapshot

```text
metric_snapshot_id
distribution_id
publication_id
channel_id
window
metric_name
metric_value
recorded_at
source
metadata
```

---

## 17. Relaciones de conocimiento

Relaciones mínimas:

```text
ContentPiece adapted_as ChannelVariant
ChannelVariant published_to Channel
ChannelVariant derived_from ContentPiece
DistributionRecord distributes ChannelVariant
MetricSnapshot measures DistributionRecord
EditorialMemory derived_from MetricSnapshot
ChannelVariant uses SourceReference
ChannelVariant governed_by VerificationRecord
```

Ejemplo:

```text
BitcoinETFNews adapted_as YouTubeScript
BitcoinETFNews adapted_as XThread
BitcoinETFNews adapted_as LinkedInPost
YouTubeScript published_to YouTube
XThread published_to X
LinkedInPost published_to LinkedIn
```

---

## 18. Responsables

### 18.1 Owner / Editor Principal

Responsabilidades:

* Aprobar distribución de piezas sensibles.
* Definir postura editorial.
* Validar canales prioritarios.
* Autorizar campañas especiales.
* Aprobar correcciones de alto impacto.

---

### 18.2 Operador de Newsroom

Responsabilidades:

* Ejecutar distribución.
* Registrar publicaciones.
* Capturar URLs.
* Actualizar estados.
* Coordinar métricas.
* Cerrar registros.

---

### 18.3 Productor de Contenido

Responsabilidades:

* Adaptar contenido por canal.
* Crear hooks.
* Preparar captions.
* Ajustar duración.
* Preparar assets.
* Revisar formato.

---

### 18.4 Revisor Editorial

Responsabilidades:

* Validar precisión.
* Revisar tono.
* Revisar riesgo.
* Confirmar que el canal no altere el sentido.
* Aprobar variantes sensibles.

---

### 18.5 Agentes XMIP

Responsabilidades:

* Proponer variantes.
* Adaptar contenido.
* Detectar riesgos.
* Medir desempeño.
* Proponer memoria.
* Mantener trazabilidad.

---

## 19. Agentes involucrados

### 19.1 DistributionAgent

Responsabilidad:

* Crear plan de distribución.
* Recomendar canales.
* Coordinar variantes.
* Detectar duplicación excesiva.

---

### 19.2 SocialClipAgent

Responsabilidad:

* Crear hooks.
* Crear clips.
* Adaptar a Shorts, TikTok, Reels y X.
* Proponer captions.

---

### 19.3 EditorialAgent

Responsabilidad:

* Mantener coherencia editorial.
* Adaptar tono.
* Preparar LinkedIn, newsletter y blog.
* Separar hecho de análisis.

---

### 19.4 ScriptAgent

Responsabilidad:

* Convertir piezas en guion para YouTube.
* Crear bloques de noticiero.
* Proponer cortes para clips.

---

### 19.5 RiskAgent

Responsabilidad:

* Revisar riesgo por canal.
* Detectar exageración.
* Bloquear variantes que exceden evidencia.
* Sugerir disclaimers.

---

### 19.6 MetricsAgent

Responsabilidad futura:

* Analizar desempeño por canal.
* Recomendar horarios.
* Recomendar formatos.
* Detectar fatiga de audiencia.

---

### 19.7 MemoryAgent

Responsabilidad:

* Guardar aprendizajes de distribución.
* Detectar patrones útiles.
* Proponer temas de seguimiento.

---

### 19.8 AuditAgent

Responsabilidad:

* Confirmar trazabilidad.
* Verificar URLs.
* Registrar eventos.
* Detectar publicaciones sin fuente o sin aprobación.

---

## 20. Métricas por canal

### 20.1 YouTube

Métricas:

* Views.
* Watch time.
* Retention.
* CTR.
* Likes.
* Comments.
* Subscribers gained.
* Average view duration.

---

### 20.2 Shorts / TikTok / Reels

Métricas:

* Views.
* Completion rate.
* Replays.
* Shares.
* Saves.
* Comments.
* Follows generated.

---

### 20.3 X / Twitter

Métricas:

* Impressions.
* Reposts.
* Replies.
* Likes.
* Clicks.
* Bookmark rate si disponible.
* Profile visits.

---

### 20.4 LinkedIn

Métricas:

* Impressions.
* Reactions.
* Comments.
* Shares.
* Profile visits.
* Link clicks.

---

### 20.5 Newsletter

Métricas:

* Open rate.
* Click rate.
* Unsubscribe rate.
* Bounce rate.
* Replies.
* Topic clicks.

---

### 20.6 Blog / Web

Métricas:

* Pageviews.
* Time on page.
* Scroll depth.
* Search traffic.
* Referrals.
* CTA clicks.

---

### 20.7 Telegram / Discord

Métricas:

* Views.
* Reactions.
* Replies.
* Clicks.
* Community questions.
* Sentiment cualitativo.

---

## 21. Métricas operativas de distribución

| Métrica                             | Propósito                 |
| ------------------------------------ | -------------------------- |
| Variantes creadas por pieza          | Medir reutilización       |
| Canales usados por pieza             | Medir cobertura            |
| Tiempo de aprobación a publicación | Medir velocidad            |
| Publicaciones fallidas               | Medir fricción técnica   |
| URLs registradas                     | Medir trazabilidad         |
| Variantes corregidas                 | Medir calidad              |
| Piezas distribuidas sin métricas    | Detectar cierre incompleto |
| Canales con mejor desempeño         | Optimizar calendario       |
| Formatos con mejor retención        | Optimizar producción      |

Metas iniciales:

| Métrica                          | Meta |
| --------------------------------- | ---: |
| Publicaciones con URL registrada  | 100% |
| Variantes con fuente interna      | 100% |
| Piezas sensibles con revisión    | 100% |
| Publicaciones con métricas 24h   | 90%+ |
| Distribuciones sin correlation_id |    0 |
| Variantes que exceden evidencia   |    0 |

---

## 22. Reglas de riesgo por canal

### 22.1 Canales de alto riesgo

Canales con alto riesgo de simplificación o viralidad:

* Shorts.
* TikTok.
* Reels.
* X.

Requieren cuidado extra en:

* Hook.
* Titular.
* Incertidumbre.
* Rumores.
* Temas de mercado.
* Hacks.
* Regulación.

---

### 22.2 Canales de contexto

Canales adecuados para explicar:

* YouTube.
* Blog.
* Newsletter.
* LinkedIn.

Requieren:

* Mayor profundidad.
* Fuentes claras.
* Separación de hecho y análisis.
* Disclaimers.

---

### 22.3 Regla de proporcionalidad

El canal corto no permite eliminar contexto crítico.

Si el tema requiere contexto para no distorsionarse, no debe publicarse solo como clip corto.

---

## 23. Checklist general de distribución

Antes de distribuir:

* [ ] ContentPiece aprobado.
* [ ] Fuente registrada.
* [ ] VerificationRecord existente.
* [ ] Riesgo evaluado.
* [ ] Canal principal definido.
* [ ] Canales secundarios definidos.
* [ ] Variantes creadas.
* [ ] Cada variante conserva sentido original.
* [ ] Cada variante conserva nivel de certeza.
* [ ] Disclaimers incluidos si aplica.
* [ ] Responsable asignado.
* [ ] Programación definida.
* [ ] AuditAgent valida trazabilidad.

Después de distribuir:

* [ ] URL registrada.
* [ ] Estado actualizado.
* [ ] Métricas programadas.
* [ ] Distribución conectada con ContentPiece.
* [ ] Memoria evaluada.
* [ ] Cierre operativo registrado.

---

## 24. Checklist por canal

### 24.1 YouTube

* [ ] Título revisado.
* [ ] Descripción lista.
* [ ] Fuentes internas registradas.
* [ ] Thumbnail brief listo.
* [ ] Guion aprobado.
* [ ] Disclaimer incluido si aplica.
* [ ] Tags preparados.
* [ ] URL registrada.

---

### 24.2 Shorts / TikTok / Reels

* [ ] Hook no exagera.
* [ ] Una sola idea.
* [ ] Caption adaptado.
* [ ] Fuente interna registrada.
* [ ] Duración adecuada.
* [ ] Riesgo revisado.
* [ ] CTA correcto.
* [ ] URL o ID registrado.

---

### 24.3 X / Twitter

* [ ] Texto claro.
* [ ] Fuente incluida si aplica.
* [ ] Rumor marcado si aplica.
* [ ] Hilo numerado si aplica.
* [ ] No hay recomendación financiera.
* [ ] Link correcto.
* [ ] Seguimiento preparado si es breaking.

---

### 24.4 LinkedIn

* [ ] Tono profesional.
* [ ] Contexto suficiente.
* [ ] Implicaciones claras.
* [ ] Fuente registrada.
* [ ] Hecho separado de análisis.
* [ ] Cierre editorial claro.

---

### 24.5 Newsletter

* [ ] Asunto validado.
* [ ] Resumen ejecutivo.
* [ ] Links revisados.
* [ ] Top noticias priorizadas.
* [ ] Disclaimer si aplica.
* [ ] Prueba de envío si aplica.
* [ ] Métricas activas.

---

### 24.6 Blog / Web

* [ ] Slug limpio.
* [ ] Título no clickbait.
* [ ] Fecha visible.
* [ ] Categoría asignada.
* [ ] Tags definidos.
* [ ] Fuentes registradas.
* [ ] Posibilidad de actualización.
* [ ] SEO revisado sin sacrificar precisión.

---

## 25. Riesgos de distribución multicanal

| Riesgo                                   | Impacto | Probabilidad | Mitigación                       |
| ---------------------------------------- | ------: | -----------: | --------------------------------- |
| Copiar y pegar sin adaptar               |   Medio |         Alta | ChannelVariant obligatorio        |
| Exagerar hooks en clips                  |    Alto |         Alta | RiskAgent por canal               |
| Perder fuente en canales cortos          |    Alto |        Media | Source refs internas obligatorias |
| Publicar con distinto nivel de certeza   |    Alto |        Media | Validación de variante           |
| Saturar canales                          |   Medio |        Media | Calendario por canal              |
| Publicar en canal equivocado             |   Medio |        Media | DistributionPlan                  |
| No registrar URL                         |   Medio |        Media | PublicationRecord obligatorio     |
| No medir desempeño                      |   Medio |        Media | MetricSnapshot obligatorio        |
| Reutilizar noticia vieja como nueva      |    Alto |        Media | Revalidación antes de reutilizar |
| Generar confusión por falta de contexto |    Alto |        Media | Regla de proporcionalidad         |

---

## 26. Manejo de excepciones

### 26.1 Variante rechazada

Si una variante no cumple:

* Regresar a adaptación.
* Registrar motivo.
* Mantener pieza base sin afectar si está correcta.

Estado:

```text
rejected
```

---

### 26.2 Publicación fallida

Si falla publicación:

* Registrar error.
* Reintentar si procede.
* Cambiar horario si aplica.
* Notificar responsable.
* Mantener estado `failed` hasta resolución.

---

### 26.3 Error después de distribución

Si se detecta error:

* Activar flujo de corrección.
* Identificar canales afectados.
* Corregir cada variante.
* Registrar CorrectionRecord.
* Evaluar memoria.

---

### 26.4 Cambio de contexto

Si la noticia cambia antes de distribuir:

* Pausar variantes pendientes.
* Revalidar fuente.
* Actualizar contenido.
* Reprogramar si aplica.

---

## 27. Auditoría

### 27.1 Eventos obligatorios

| Evento                        | Cuándo ocurre            |
| ----------------------------- | ------------------------- |
| distribution_plan_created     | Se crea plan              |
| channel_variant_created       | Se crea variante          |
| channel_variant_reviewed      | Se revisa variante        |
| channel_variant_approved      | Se aprueba variante       |
| channel_variant_rejected      | Se rechaza variante       |
| content_published_to_channel  | Se publica en canal       |
| distribution_record_created   | Se registra distribución |
| distribution_failed           | Falla distribución       |
| distribution_corrected        | Se corrige variante       |
| distribution_metrics_recorded | Se registran métricas    |

---

### 27.2 Evento mínimo

```json
{
  "event_type": "content_published_to_channel",
  "content_id": "content_001",
  "variant_id": "variant_001",
  "channel": "youtube",
  "published_url": "https://example.com/publication",
  "actor_type": "user",
  "actor_ref": "operator",
  "status": "success",
  "correlation_id": "corr_20260702_xxxxxx",
  "occurred_at": "2026-07-02T00:00:00Z"
}
```

---

## 28. Plantilla de Distribution Plan

```markdown
# Distribution Plan

**Content ID:**  
**News ID:**  
**Título base:**  
**Prioridad:**  
**Riesgo:**  
**Canal principal:**  
**Canales secundarios:**  
**Responsable:**  
**Fecha programada:**  
**Correlation ID:**  

---

## 1. Objetivo de distribución

## 2. Canal principal

## 3. Variantes requeridas

| Canal | Formato | Estado | Responsable |
|---|---|---|---|

## 4. Mensaje central

## 5. Nivel de verificación

## 6. Disclaimers requeridos

## 7. Riesgos por canal

## 8. Checklist

- [ ] Fuente registrada.
- [ ] Variantes creadas.
- [ ] Riesgo revisado.
- [ ] Publicación programada.
- [ ] Métricas programadas.
```

---

## 29. Plantilla de Channel Variant

```markdown
# Channel Variant

**Variant ID:**  
**Content ID:**  
**Canal:**  
**Formato:**  
**Estado:**  
**Riesgo:**  
**Responsable:**  

---

## 1. Hook / Título

## 2. Cuerpo / Guion / Caption

## 3. CTA

## 4. Fuente interna

## 5. Disclaimer

## 6. Notas de adaptación

## 7. Validación editorial

- [ ] Mantiene sentido original.
- [ ] Mantiene nivel de certeza.
- [ ] No exagera.
- [ ] Respeta canal.
- [ ] Fuente registrada.
```

---

## 30. Antipatrones prohibidos

XCripto debe evitar:

* Publicar el mismo texto en todos los canales.
* Quitar incertidumbre para hacer más fuerte el hook.
* Convertir análisis en recomendación financiera.
* Publicar clips sin fuente interna.
* Publicar en redes antes de aprobar la pieza base.
* Distribuir contenido sensible sin revisión.
* Crear hilos largos sin estructura.
* Reutilizar contenido viejo sin marcarlo.
* No capturar URL publicada.
* No medir desempeño.
* No conectar variantes con pieza original.
* Dejar publicaciones sin archivo.
* No registrar correcciones por canal.

---

## 31. Relación con XMIP

XMIP debe soportar distribución multicanal mediante:

* Distribution Plans.
* Channel Registry.
* Channel Variants.
* Publication Records.
* Distribution Records.
* Metric Snapshots.
* Risk checks.
* Agent execution logs.
* Audit events.
* Memory records.
* Knowledge relationships.

La distribución debe integrarse al pipeline del newsroom, no manejarse como actividad externa.

---

## 32. Criterios de aceptación

Este documento se considera aceptado cuando:

* [ ] Define propósito de distribución multicanal.
* [ ] Define canales oficiales.
* [ ] Define canal principal por tipo de contenido.
* [ ] Define modelo de distribución.
* [ ] Define estados de distribución.
* [ ] Define reglas generales.
* [ ] Define adaptación por canal.
* [ ] Define matriz de adaptación.
* [ ] Define proceso operativo.
* [ ] Define reutilización de contenido.
* [ ] Define trazabilidad multicanal.
* [ ] Define datos mínimos en XMIP.
* [ ] Define relaciones de conocimiento.
* [ ] Define responsables.
* [ ] Define agentes involucrados.
* [ ] Define métricas por canal.
* [ ] Define métricas operativas.
* [ ] Define reglas de riesgo por canal.
* [ ] Define checklists.
* [ ] Define riesgos y mitigaciones.
* [ ] Define manejo de excepciones.
* [ ] Define auditoría.
* [ ] Define plantillas operativas.
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

Este documento gobierna directamente:

* ORION-026 — Métricas Operativas.
* ORION-027 — Gestión de Incidentes Editoriales.
* ORION-028 — Operación de Agentes Editoriales.
* ORION-029 — Checklist Diario del Newsroom.

---

## 34. Próximos pasos

Después de aprobar ORION-025, continuar con:

1. ORION-026 — Métricas Operativas.
2. ORION-027 — Gestión de Incidentes Editoriales.
3. ORION-028 — Operación de Agentes Editoriales.
4. ORION-029 — Checklist Diario del Newsroom.

ORION-026 debe definir cómo XCripto mide producción, calidad, distribución, fuentes, verificación, audiencia, errores, aprendizaje editorial y desempeño operativo del newsroom.

---

## 35. Historial de cambios

| Versión | Fecha      | Cambio                                       | Autor            |
| -------- | ---------- | -------------------------------------------- | ---------------- |
| 1.0      | 2026-07-02 | Versión inicial de distribución multicanal | Fernando Cuellar |
