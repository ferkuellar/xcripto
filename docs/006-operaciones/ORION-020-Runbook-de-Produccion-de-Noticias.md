
# ORION-020 — Runbook de Producción de Noticias

**Nivel documental:** L4 — Operations
**Volumen:** 006-operaciones
**Proyecto:** ORION / XCripto / XMIP
**Versión:** 1.0
**Estado:** Draft
**Owner:** Fernando Cuellar
**Última actualización:** 2026-07-02
**Ruta sugerida:** `docs/006-operaciones/ORION-020-Runbook-de-Produccion-de-Noticias.md`

---

## 1. Propósito

Este documento define el runbook operativo para producir noticias dentro de XCripto.

Su propósito es establecer el procedimiento paso a paso para convertir una señal informativa en una pieza editorial validada, redactada, revisada, publicada, distribuida y registrada dentro de XMIP.

ORION-020 responde a la pregunta:

> ¿Qué pasos exactos debe seguir XCripto para producir una noticia cripto desde su detección hasta su publicación y cierre operativo?

Este documento convierte las operaciones diarias y el flujo de publicación en una guía ejecutable.

---

## 2. Alcance

Este runbook cubre:

* Producción de noticias individuales.
* Producción de notas breves.
* Producción de alertas.
* Producción de guiones para video.
* Producción de piezas para redes.
* Validación mínima de fuentes.
* Clasificación de prioridad.
* Revisión editorial.
* Publicación.
* Registro operativo.
* Métricas iniciales.
* Memoria editorial.
* Auditoría.

Este runbook no cubre en detalle:

* Gestión avanzada de fuentes.
* Verificación editorial profunda.
* Distribución multicanal avanzada.
* Gestión de incidentes.
* Calendario editorial.
* Operación detallada de cada agente.

Esos temas se desarrollan en documentos relacionados:

* ORION-021 — Gestión de Fuentes.
* ORION-022 — Protocolo de Verificación Editorial.
* ORION-023 — Pipeline del Newsroom.
* ORION-024 — Calendario Editorial.
* ORION-025 — Distribución Multicanal.
* ORION-027 — Gestión de Incidentes Editoriales.
* ORION-028 — Operación de Agentes Editoriales.

---

## 3. Contexto operativo

XCripto opera en un ecosistema donde la información se mueve rápido, los rumores se amplifican fácil y los errores pueden afectar la confianza de la audiencia.

Por eso, la producción de noticias debe seguir un procedimiento claro.

El objetivo no es ser el primero en publicar cualquier cosa.
El objetivo es publicar contenido útil, verificable, oportuno y con contexto.

El flujo base de producción es:

```text
detectar
→ registrar
→ clasificar
→ validar
→ priorizar
→ redactar
→ revisar
→ aprobar
→ publicar
→ distribuir
→ medir
→ archivar
→ guardar memoria
```

---

## 4. Principios del runbook

### 4.1 Toda noticia empieza como señal, no como hecho

Una noticia detectada aún no es publicable.

Debe pasar por registro, validación y clasificación.

### 4.2 Ninguna fuente social es suficiente por sí sola para temas sensibles

Publicaciones en X, Telegram, Discord, Reddit o foros pueden disparar investigación, pero no deben convertirse automáticamente en noticia confirmada.

### 4.3 El titular debe seguir al hecho

El titular puede ser atractivo, pero no debe exagerar ni cambiar el sentido de la información.

### 4.4 La producción debe dejar rastro

Cada noticia debe tener fuente, responsable, estado, agente involucrado, validación y registro de publicación.

### 4.5 Los agentes preparan; el humano decide en temas críticos

Los agentes pueden acelerar el trabajo, pero las piezas sensibles requieren revisión humana.

### 4.6 El cierre importa

Una noticia no termina cuando se publica.
Debe medirse, archivarse y conectarse con memoria editorial si deja aprendizaje útil.

---

## 5. Roles responsables

### 5.1 Owner / Editor Principal

Responsable de:

* Aprobar noticias sensibles.
* Decidir publicación de piezas P0.
* Autorizar correcciones materiales.
* Autorizar retiro de contenido.
* Definir postura editorial cuando exista ambigüedad.

### 5.2 Operador de Newsroom

Responsable de:

* Ejecutar este runbook.
* Registrar noticias.
* Activar agentes.
* Coordinar revisión.
* Publicar o programar contenido.
* Registrar URLs.
* Cerrar la operación.

### 5.3 Revisor Editorial

Responsable de:

* Revisar precisión.
* Revisar tono.
* Verificar fuente.
* Separar hecho, análisis y opinión.
* Marcar riesgos editoriales.

### 5.4 Productor de Contenido

Responsable de:

* Adaptar la noticia al formato.
* Preparar guion, copy, caption o descripción.
* Preparar assets editoriales.
* Ajustar contenido por canal.

### 5.5 Agentes XMIP

Responsables de apoyar el proceso mediante:

* Detección.
* Resumen.
* Validación preliminar.
* Clasificación.
* Redacción.
* Adaptación.
* Revisión de riesgo.
* Auditoría.
* Memoria.

---

## 6. Agentes involucrados

### 6.1 NewsScoutAgent

Detecta señales informativas y propone noticias candidatas.

### 6.2 SourceValidatorAgent

Evalúa confiabilidad, fuente primaria, fecha, duplicados y riesgo de rumor.

### 6.3 MarketImpactAgent

Clasifica impacto por mercado, sector, activo o narrativa.

### 6.4 EditorialAgent

Convierte la noticia validada en pieza editorial clara.

### 6.5 ScriptAgent

Convierte la noticia en guion para video o bloque de noticiero.

### 6.6 SocialClipAgent

Adapta la noticia a formato corto para redes.

### 6.7 RiskAgent

Detecta riesgos editoriales, lenguaje especulativo, hype o falta de evidencia.

### 6.8 AuditAgent

Valida que la pieza tenga trazabilidad mínima.

### 6.9 MemoryAgent

Propone memoria editorial cuando la noticia deja aprendizaje reutilizable.

---

## 7. Entradas del runbook

Una producción de noticia puede iniciar desde:

* Fuente oficial.
* Medio confiable.
* Red social.
* Alerta de mercado.
* Evento on-chain.
* Comunicado regulatorio.
* Blog de proyecto.
* Reporte institucional.
* Hack / exploit.
* Rumor que requiere seguimiento.
* Evento programado del calendario editorial.

Entrada mínima:

```text
raw_signal
source_name
source_url
detected_at
detected_by
initial_category
initial_priority
notes
```

---

## 8. Salidas del runbook

El runbook puede producir una o varias salidas:

* NewsItem registrado.
* Nota editorial.
* Alerta.
* Guion de video.
* Post para redes.
* Hilo.
* Newsletter brief.
* Registro de publicación.
* Registro de descarte.
* Memoria editorial.
* Evento de auditoría.

Salida mínima para una noticia publicada:

```text
news_id
content_id
publication_id
title
summary
source_refs
status
priority
channel
published_url
published_at
correlation_id
```

---

## 9. Estados de una noticia

| Estado             | Descripción                     |
| ------------------ | -------------------------------- |
| detected           | Señal detectada                 |
| registered         | Señal registrada                |
| classified         | Categoría y prioridad asignadas |
| validating         | En validación                   |
| verified           | Validada                         |
| partially_verified | Validación parcial              |
| rumor              | Rumor no confirmado              |
| rejected           | Descartada                       |
| monitoring         | En seguimiento                   |
| prioritized        | Priorizada para producción      |
| drafting           | En redacción                    |
| reviewing          | En revisión                     |
| approved           | Aprobada                         |
| scheduled          | Programada                       |
| published          | Publicada                        |
| corrected          | Corregida                        |
| archived           | Archivada                        |
| escalated          | Escalada a revisión humana      |

---

## 10. Prioridades operativas

| Prioridad | Uso                          | Tiempo de respuesta esperado    |
| --------- | ---------------------------- | ------------------------------- |
| P0        | Breaking news / alto impacto | Inmediato, con revisión humana |
| P1        | Noticia principal del día   | Mismo bloque operativo          |
| P2        | Noticia relevante secundaria | Durante el día                 |
| P3        | Seguimiento o contexto       | Cuando haya espacio editorial   |
| P4        | Ruido o baja relevancia      | Descartar o archivar            |

---

## 11. Categorías editoriales

| Categoría    | Descripción                            |
| ------------- | --------------------------------------- |
| Bitcoin       | BTC, ETF, minería, adopción           |
| Ethereum      | ETH, L2, staking, ecosistema            |
| Altcoins      | Tokens y proyectos relevantes           |
| Exchanges     | Binance, Coinbase, Kraken, Bybit, etc.  |
| Regulation    | Regulación, leyes, demandas, sanciones |
| DeFi          | Protocolos, TVL, gobernanza, exploits   |
| Stablecoins   | USDT, USDC, DAI, pagos, regulación     |
| Security      | Hacks, exploits, vulnerabilidades       |
| Institutional | Bancos, fondos, empresas públicas      |
| Macro         | Tasas, inflación, dólar, liquidez     |
| On-chain      | Métricas blockchain relevantes         |
| AI + Crypto   | Intersección IA y cripto               |
| Scam / Fraud  | Fraudes, phishing, alertas              |
| Education     | Explicadores y contexto                 |
| Market        | Narrativa general de mercado            |

---

# 12. Procedimiento estándar

## 12.1 Paso 1 — Detectar señal

### Objetivo

Identificar una posible noticia relevante.

### Responsable

* NewsScoutAgent.
* Operador de Newsroom.

### Actividades

1. Revisar fuentes asignadas.
2. Detectar evento, anuncio, movimiento o narrativa.
3. Capturar URL o referencia.
4. Registrar hora de detección.
5. Identificar fuente original si existe.
6. Crear entrada preliminar.

### Criterios de aceptación

* [ ] La señal tiene fuente.
* [ ] La señal tiene fecha/hora.
* [ ] La señal tiene categoría preliminar.
* [ ] La señal tiene responsable o agente detector.
* [ ] La señal fue registrada en XMIP.

### Salida

```text
Detected Signal
```

---

## 12.2 Paso 2 — Registrar NewsItem

### Objetivo

Crear el registro operativo de la noticia.

### Responsable

* Operador de Newsroom.
* AuditAgent.

### Campos mínimos

```text
news_id
title_preliminary
source_url
source_name
source_type
detected_at
detected_by
category
priority
status
correlation_id
```

### Regla

Toda noticia debe tener `correlation_id`.

### Criterios de aceptación

* [ ] `news_id` creado.
* [ ] `correlation_id` asignado.
* [ ] Fuente registrada.
* [ ] Estado inicial asignado.
* [ ] Categoría preliminar asignada.

### Salida

```text
Registered NewsItem
```

---

## 12.3 Paso 3 — Clasificar noticia

### Objetivo

Asignar categoría, prioridad y tipo editorial.

### Responsable

* MarketImpactAgent.
* Operador de Newsroom.

### Actividades

1. Identificar categoría editorial.
2. Determinar impacto potencial.
3. Asignar prioridad P0-P4.
4. Determinar tipo de pieza recomendada.
5. Marcar si requiere revisión humana.

### Tipo editorial

| Tipo           | Uso                 |
| -------------- | ------------------- |
| alert          | Alerta rápida      |
| brief          | Nota breve          |
| lead_story     | Historia principal  |
| explainer      | Explicación        |
| follow_up      | Seguimiento         |
| market_context | Contexto de mercado |
| risk_warning   | Advertencia         |
| educational    | Educativo           |

### Criterios de aceptación

* [ ] Categoría asignada.
* [ ] Prioridad asignada.
* [ ] Tipo editorial asignado.
* [ ] Riesgo preliminar identificado.
* [ ] P0 o alto riesgo marcado para revisión humana.

### Salida

```text
Classified NewsItem
```

---

## 12.4 Paso 4 — Validar fuente

### Objetivo

Determinar si la noticia puede trabajarse como hecho, seguimiento, rumor o descarte.

### Responsable

* SourceValidatorAgent.
* Revisor Editorial.

### Actividades

1. Confirmar que la fuente existe.
2. Revisar fecha y hora.
3. Buscar fuente primaria.
4. Buscar fuente secundaria confiable.
5. Detectar duplicados.
6. Detectar si es noticia vieja reciclada.
7. Evaluar confiabilidad.
8. Marcar estado de validación.

### Estados de validación

| Estado             | Uso                                |
| ------------------ | ---------------------------------- |
| verified           | Confirmada                         |
| partially_verified | Hay evidencia, falta confirmación |
| rumor              | No confirmada                      |
| monitoring         | Seguir observando                  |
| rejected           | Descartada                         |
| escalated          | Requiere revisión humana          |

### Criterios de aceptación

* [ ] Fuente primaria identificada o justificación de ausencia.
* [ ] Fecha validada.
* [ ] Duplicados revisados.
* [ ] Estado de validación asignado.
* [ ] Nivel de confianza asignado.

### Salida

```text
Validation Record
```

---

## 12.5 Paso 5 — Decidir continuar, monitorear o descartar

### Objetivo

Evitar producir contenido sobre noticias débiles o irrelevantes.

### Responsable

* Operador de Newsroom.
* Editor Principal para casos sensibles.

### Decisiones posibles

| Decisión | Acción                        |
| --------- | ------------------------------ |
| continue  | Pasar a producción            |
| monitor   | Mantener en seguimiento        |
| reject    | Descartar                      |
| escalate  | Enviar a revisión humana      |
| breaking  | Activar flujo de breaking news |

### Reglas

* `rumor` no puede pasar a publicación como hecho.
* `partially_verified` puede usarse solo con lenguaje condicionado.
* `P0` debe escalarse.
* `rejected` debe registrar motivo.

### Criterios de aceptación

* [ ] Decisión registrada.
* [ ] Motivo documentado.
* [ ] Responsable registrado.
* [ ] Estado actualizado.

### Salida

```text
Editorial Decision
```

---

## 12.6 Paso 6 — Crear brief editorial

### Objetivo

Convertir la noticia validada en un brief claro para producción.

### Responsable

* EditorialAgent.
* Operador de Newsroom.

### Estructura del brief

```text
título preliminar
qué pasó
por qué importa
qué está confirmado
qué falta por confirmar
impacto potencial
fuentes
riesgos
formato recomendado
```

### Criterios de aceptación

* [ ] El brief separa hechos de interpretación.
* [ ] Incluye fuentes.
* [ ] Incluye impacto.
* [ ] Incluye riesgos.
* [ ] Define formato recomendado.

### Salida

```text
Editorial Brief
```

---

## 12.7 Paso 7 — Redactar pieza base

### Objetivo

Crear la pieza editorial base.

### Responsable

* EditorialAgent.
* Productor de Contenido.

### Estructura mínima

```text
titular
resumen
contexto
hechos confirmados
impacto
fuentes
riesgos
disclaimer si aplica
```

### Reglas de redacción

* No usar lenguaje de recomendación financiera.
* No afirmar más de lo que la fuente permite.
* No exagerar impacto.
* No ocultar incertidumbre.
* No mezclar opinión con hecho.
* Marcar si es seguimiento o actualización.

### Criterios de aceptación

* [ ] Titular preciso.
* [ ] Resumen claro.
* [ ] Contexto suficiente.
* [ ] Fuentes registradas.
* [ ] Riesgos identificados.
* [ ] Disclaimer incluido si aplica.

### Salida

```text
Base Content Piece
```

---

## 12.8 Paso 8 — Adaptar a formato

### Objetivo

Convertir la pieza base al canal o formato requerido.

### Responsable

* Productor de Contenido.
* ScriptAgent.
* SocialClipAgent.

### Formatos posibles

| Formato               | Agente recomendado         |
| --------------------- | -------------------------- |
| Guion de YouTube      | ScriptAgent                |
| Short / Reel / TikTok | SocialClipAgent            |
| Post X                | SocialClipAgent            |
| Hilo X                | EditorialAgent             |
| LinkedIn post         | EditorialAgent             |
| Newsletter brief      | EditorialAgent             |
| Blog article          | EditorialAgent             |
| Alerta                | EditorialAgent + RiskAgent |

### Criterios de aceptación

* [ ] El formato corresponde al canal.
* [ ] El contenido fue adaptado, no copiado sin criterio.
* [ ] El tono es adecuado.
* [ ] El riesgo fue revaluado.
* [ ] La fuente sigue registrada.

### Salida

```text
Channel-Ready Content
```

---

## 12.9 Paso 9 — Revisar riesgo editorial

### Objetivo

Detectar problemas antes de publicación.

### Responsable

* RiskAgent.
* Revisor Editorial.

### Validaciones

* ¿Hay afirmaciones sin fuente?
* ¿El titular exagera?
* ¿Se presenta rumor como hecho?
* ¿Hay lenguaje de predicción?
* ¿Parece recomendación financiera?
* ¿Falta contexto?
* ¿Hay riesgo legal o reputacional?
* ¿Requiere aprobación humana?

### Estados de riesgo

| Estado   | Acción                   |
| -------- | ------------------------- |
| low      | Puede continuar           |
| medium   | Revisión estándar       |
| high     | Aprobación humana        |
| critical | Escalar antes de publicar |

### Criterios de aceptación

* [ ] Riesgo evaluado.
* [ ] Recomendaciones registradas.
* [ ] Correcciones aplicadas.
* [ ] Escalamiento realizado si aplica.

### Salida

```text
Risk Review Record
```

---

## 12.10 Paso 10 — Revisión editorial final

### Objetivo

Aprobar o rechazar la pieza para publicación.

### Responsable

* Revisor Editorial.
* Editor Principal si aplica.

### Checklist final

* [ ] Fuente registrada.
* [ ] Fecha correcta.
* [ ] Titular preciso.
* [ ] Hechos separados de análisis.
* [ ] Sin recomendación financiera.
* [ ] Sin hype irresponsable.
* [ ] Disclaimer incluido si aplica.
* [ ] Formato correcto.
* [ ] Riesgo aceptable.
* [ ] Estado actualizado.

### Decisiones posibles

| Decisión | Acción                  |
| --------- | ------------------------ |
| approve   | Pasar a publicación     |
| revise    | Regresar a edición      |
| reject    | Descartar                |
| escalate  | Subir a Editor Principal |
| hold      | Mantener en espera       |

### Salida

```text
Editorial Approval
```

---

## 12.11 Paso 11 — Publicar o programar

### Objetivo

Publicar la pieza en el canal definido.

### Responsable

* Operador de Newsroom.
* Productor de Contenido.

### Actividades

1. Seleccionar canal.
2. Cargar contenido.
3. Cargar assets.
4. Validar metadata.
5. Publicar o programar.
6. Capturar URL.
7. Actualizar estado.

### Campos mínimos

```text
channel
publication_status
published_url
published_at
published_by
scheduled_at
```

### Criterios de aceptación

* [ ] Canal correcto.
* [ ] Contenido aprobado.
* [ ] Metadata completa.
* [ ] URL registrada.
* [ ] Estado actualizado.
* [ ] Publicación auditada.

### Salida

```text
Publication Record
```

---

## 12.12 Paso 12 — Distribuir contenido

### Objetivo

Amplificar la publicación en canales secundarios.

### Responsable

* Productor de Contenido.
* SocialClipAgent.

### Actividades

1. Adaptar texto por canal.
2. Crear posts secundarios.
3. Publicar clips si aplica.
4. Compartir enlace principal.
5. Registrar distribución.

### Canales secundarios posibles

* X.
* LinkedIn.
* Telegram.
* Discord.
* Shorts.
* Reels.
* TikTok.
* Newsletter.

### Criterios de aceptación

* [ ] La distribución no duplica texto sin adaptación.
* [ ] Los links son correctos.
* [ ] La fuente base se conserva.
* [ ] Los canales quedan registrados.

### Salida

```text
Distribution Record
```

---

## 12.13 Paso 13 — Registrar métricas iniciales

### Objetivo

Medir desempeño básico de la pieza.

### Responsable

* Operador de Newsroom.
* AuditAgent.

### Ventanas mínimas

* 1 hora.
* 24 horas.
* 7 días.

### Métricas por canal

| Canal               | Métricas                             |
| ------------------- | ------------------------------------- |
| YouTube             | views, watch time, CTR, retention     |
| Shorts/Reels/TikTok | views, completion rate, shares        |
| X                   | impressions, reposts, replies, clicks |
| LinkedIn            | impressions, reactions, comments      |
| Newsletter          | open rate, click rate                 |
| Blog                | pageviews, time on page               |

### Criterios de aceptación

* [ ] Métrica inicial registrada.
* [ ] Canal identificado.
* [ ] Fecha de medición registrada.
* [ ] publication_id relacionado.

### Salida

```text
Metric Snapshot
```

---

## 12.14 Paso 14 — Archivar pieza

### Objetivo

Cerrar el ciclo documental de la noticia.

### Responsable

* Operador de Newsroom.
* AuditAgent.

### Actividades

1. Guardar estado final.
2. Registrar URL final.
3. Relacionar contenido con noticia.
4. Relacionar métricas.
5. Relacionar fuentes.
6. Marcar si requiere seguimiento.
7. Archivar evidencia.

### Criterios de aceptación

* [ ] Pieza archivada.
* [ ] Fuente vinculada.
* [ ] Publicación vinculada.
* [ ] Métricas vinculadas.
* [ ] Estado final asignado.
* [ ] Seguimiento marcado si aplica.

### Salida

```text
Archived News Record
```

---

## 12.15 Paso 15 — Evaluar memoria editorial

### Objetivo

Guardar solo conocimiento útil para futuras operaciones.

### Responsable

* MemoryAgent.
* Editor Principal u Operador.

### Preguntas

* ¿Esta noticia forma parte de una narrativa recurrente?
* ¿Esta fuente demostró ser confiable?
* ¿Hubo error que deba evitarse?
* ¿El formato funcionó especialmente bien o mal?
* ¿Debe darse seguimiento?
* ¿Hay contexto que será útil después?

### Acciones

| Evaluación | Acción                         |
| ----------- | ------------------------------- |
| Útil       | Guardar memoria                 |
| Temporal    | No guardar                      |
| Dudosa      | Proponer y revisar              |
| Incorrecta  | No guardar / marcar advertencia |
| Seguimiento | Crear pendiente                 |

### Criterios de aceptación

* [ ] Memoria con fuente.
* [ ] Memoria con tipo.
* [ ] Memoria con fecha.
* [ ] Memoria aprobada si aplica.
* [ ] Memoria relacionada con noticia o documento.

### Salida

```text
Editorial Memory Record
```

---

# 13. Flujo especial: Breaking News

## 13.1 Cuándo usar este flujo

Usar cuando la noticia sea:

* Hack importante.
* Exchange detiene retiros.
* Acción regulatoria fuerte.
* ETF aprobado/rechazado.
* Falla crítica de infraestructura.
* Pérdida importante de fondos.
* Evento con impacto fuerte en BTC/ETH.
* Noticia institucional de alto impacto.

## 13.2 Flujo acelerado

```text
detectar
→ validar fuente primaria o confiable
→ escalar
→ publicar alerta breve
→ monitorear
→ actualizar
→ producir pieza extendida
```

## 13.3 Reglas

* Publicar solo lo confirmado.
* Decir claramente qué falta confirmar.
* No especular con precio.
* Actualizar conforme haya nueva información.
* Registrar cada actualización.
* No borrar versiones sin registro.

## 13.4 Formato de alerta

```text
ALERTA XCRIPTO

Qué pasó:
[hecho confirmado]

Lo que sabemos:
- [dato 1]
- [dato 2]

Lo que falta confirmar:
- [dato pendiente]

Impacto:
[contexto breve]

Fuente:
[referencia]

Seguimiento en desarrollo.
```

## 13.5 Criterios de aceptación

* [ ] Fuente mínima fuerte.
* [ ] Escalamiento realizado.
* [ ] Alerta revisada.
* [ ] Incertidumbre explícita.
* [ ] Seguimiento activado.
* [ ] Registro de publicación creado.

---

# 14. Flujo especial: Rumor o información no confirmada

## 14.1 Cuándo usar este flujo

Usar cuando:

* La fuente no es primaria.
* La información viene de redes sociales.
* Hay versiones contradictorias.
* Falta evidencia.
* Puede afectar reputación o mercado.

## 14.2 Reglas

* No publicar como hecho.
* Marcar como rumor si se menciona.
* Preferir monitoreo antes que publicación.
* Buscar confirmación adicional.
* Escalar si el riesgo es alto.

## 14.3 Estados permitidos

```text
rumor
monitoring
escalated
rejected
```

## 14.4 Criterios de aceptación

* [ ] No se presenta como confirmado.
* [ ] Tiene estado `rumor` o `monitoring`.
* [ ] Se registró fuente original.
* [ ] Se definió seguimiento.
* [ ] No se publicó sin aprobación.

---

# 15. Flujo especial: Corrección posterior

## 15.1 Cuándo usar

Usar cuando una pieza publicada tenga:

* Error de fuente.
* Error de fecha.
* Error de interpretación.
* Titular impreciso.
* Información incompleta.
* Cambio relevante posterior.
* Confusión entre rumor y hecho.

## 15.2 Pasos

1. Detectar error.
2. Clasificar severidad.
3. Notificar al Editor Principal si es material.
4. Corregir pieza.
5. Registrar versión anterior.
6. Registrar versión corregida.
7. Publicar nota de corrección si aplica.
8. Guardar aprendizaje.

## 15.3 Tipos de corrección

| Tipo          | Descripción                        |
| ------------- | ----------------------------------- |
| minor         | Error menor                         |
| material      | Cambia precisión o interpretación |
| update        | Nueva información                  |
| clarification | Aclaración                         |
| retraction    | Retiro de contenido                 |

## 15.4 Criterios de aceptación

* [ ] Error identificado.
* [ ] Severidad clasificada.
* [ ] Corrección aprobada.
* [ ] Registro creado.
* [ ] Memoria evaluada.
* [ ] Audiencia informada si aplica.

---

# 16. Estructura de noticia estándar

Toda noticia producida debe poder expresarse en esta estructura:

```markdown
## Titular

## Resumen

## Qué pasó

## Por qué importa

## Qué está confirmado

## Qué falta por confirmar

## Impacto potencial

## Fuentes

## Riesgos editoriales

## Formatos recomendados

## Estado
```

---

# 17. Plantilla de brief editorial

```markdown
# Brief Editorial

**News ID:**  
**Fecha:**  
**Prioridad:**  
**Categoría:**  
**Estado:**  
**Responsable:**  
**Correlation ID:**  

---

## 1. Titular preliminar

## 2. Qué pasó

## 3. Por qué importa

## 4. Hechos confirmados

## 5. Información pendiente

## 6. Impacto potencial

## 7. Fuentes

## 8. Riesgo editorial

## 9. Formato recomendado

## 10. Próxima acción
```

---

# 18. Plantilla de guion rápido

```markdown
# Guion Rápido XCripto

**Tema:**  
**Duración estimada:**  
**Formato:**  
**Fecha:**  

---

## 1. Hook

## 2. Contexto

## 3. Noticia

## 4. Impacto

## 5. Qué falta por confirmar

## 6. Cierre

## 7. Disclaimer
```

---

# 19. Plantilla de post corto

```markdown
# Post Corto

**Canal:**  
**News ID:**  
**Estado:**  

---

[Texto del post]

Fuente:
[referencia]

Nota:
[disclaimer si aplica]
```

---

# 20. Checklist operativo completo

## 20.1 Detección

* [ ] Fuente capturada.
* [ ] Fecha registrada.
* [ ] Categoría preliminar asignada.
* [ ] NewsItem creado.
* [ ] Correlation ID creado.

## 20.2 Validación

* [ ] Fuente primaria buscada.
* [ ] Fuente secundaria revisada si aplica.
* [ ] Fecha confirmada.
* [ ] Duplicados revisados.
* [ ] Estado de validación asignado.

## 20.3 Producción

* [ ] Brief creado.
* [ ] Titular revisado.
* [ ] Resumen redactado.
* [ ] Contexto incluido.
* [ ] Riesgos identificados.
* [ ] Formato seleccionado.

## 20.4 Revisión

* [ ] RiskAgent ejecutado si aplica.
* [ ] Revisor Editorial validó.
* [ ] Disclaimer incluido si aplica.
* [ ] Aprobación humana registrada si aplica.

## 20.5 Publicación

* [ ] Canal seleccionado.
* [ ] Contenido adaptado.
* [ ] Metadata completa.
* [ ] URL capturada.
* [ ] Registro de publicación creado.

## 20.6 Cierre

* [ ] Métrica inicial programada.
* [ ] Pieza archivada.
* [ ] Memoria evaluada.
* [ ] Seguimiento definido.
* [ ] Auditoría completa.

---

# 21. Datos mínimos requeridos

## 21.1 NewsItem

```text
news_id
title
summary
category
priority
status
source_refs
risk_level
detected_at
validated_at
owner
correlation_id
```

## 21.2 ContentPiece

```text
content_id
news_id
format
title
body
status
created_by
reviewed_by
approved_by
source_refs
correlation_id
```

## 21.3 PublicationRecord

```text
publication_id
content_id
channel
published_url
published_at
published_by
status
metrics_status
correction_status
correlation_id
```

## 21.4 SourceReference

```text
source_id
source_name
source_url
source_type
published_at
accessed_at
confidence
notes
```

## 21.5 EditorialMemory

```text
memory_id
memory_type
title
content
source_ref
related_news_id
status
created_at
approved_by
```

---

# 22. Auditoría mínima

Toda producción debe generar eventos de auditoría.

## 22.1 Eventos obligatorios

| Evento                  | Cuándo ocurre       |
| ----------------------- | -------------------- |
| news_detected           | Se detecta señal    |
| news_registered         | Se crea NewsItem     |
| source_validated        | Se valida fuente     |
| news_classified         | Se clasifica noticia |
| editorial_brief_created | Se crea brief        |
| content_drafted         | Se redacta contenido |
| content_reviewed        | Se revisa contenido  |
| content_approved        | Se aprueba           |
| content_published       | Se publica           |
| content_distributed     | Se distribuye        |
| metric_recorded         | Se registra métrica |
| memory_proposed         | Se propone memoria   |
| memory_approved         | Se aprueba memoria   |
| content_corrected       | Se corrige pieza     |
| content_retracted       | Se retira pieza      |

## 22.2 Formato mínimo de evento

```json
{
  "event_type": "content_published",
  "actor_type": "user",
  "actor_ref": "operator",
  "subject_type": "publication",
  "subject_ref": "publication_id",
  "action": "publish",
  "status": "success",
  "correlation_id": "corr_20260702_xxxxxx",
  "occurred_at": "2026-07-02T00:00:00Z"
}
```

---

# 23. Reglas editoriales críticas

## 23.1 Prohibido publicar como hecho

* Rumores sin fuente.
* Capturas de pantalla no verificadas.
* Supuestas filtraciones sin confirmación.
* Movimientos de precio sin contexto.
* Acusaciones sin evidencia.
* Noticias viejas recicladas.
* Traducciones dudosas sin fuente original.

## 23.2 Requiere aprobación humana

* Hacks.
* Exploits.
* Insolvencia.
* Demandas.
* Regulación.
* Riesgo para usuarios.
* Fraudes.
* Personas o empresas señaladas.
* Noticias de alto impacto de mercado.
* Cualquier pieza con riesgo reputacional.

## 23.3 Requiere disclaimer

* Contenido de mercado.
* Análisis de activos.
* Interpretación de impacto.
* Noticias que puedan inducir acción financiera.
* Guiones sobre precio, ETFs, exchanges o tokens.

Disclaimer base:

```text
Este contenido es informativo y educativo. No constituye asesoría financiera, legal ni de inversión.
```

---

# 24. Errores comunes a evitar

| Error                                        | Riesgo | Prevención                   |
| -------------------------------------------- | ------ | ----------------------------- |
| Publicar primero y verificar después        | Alto   | Validación obligatoria       |
| Usar titular exagerado                       | Alto   | Revisión editorial           |
| Confundir rumor con noticia                  | Alto   | Estado`rumor`               |
| No registrar fuente                          | Alto   | SourceReference obligatorio   |
| No guardar URL publicada                     | Medio  | PublicationRecord obligatorio |
| Repetir contenido igual en todos los canales | Medio  | Adaptación por canal         |
| No corregir públicamente error material     | Alto   | Flujo de corrección          |
| Guardar ruido como memoria                   | Medio  | MemoryAgent + aprobación     |
| No medir publicación                        | Medio  | Métricas 1h / 24h / 7d       |
| No escalar tema sensible                     | Alto   | Reglas de escalamiento        |

---

# 25. Métricas del runbook

## 25.1 Métricas de ejecución

| Métrica                             | Objetivo                   |
| ------------------------------------ | -------------------------- |
| Tiempo de detección a registro      | Medir velocidad de intake  |
| Tiempo de registro a validación     | Medir eficiencia editorial |
| Tiempo de validación a publicación | Medir producción          |
| Noticias descartadas                 | Medir ruido filtrado       |
| Noticias escaladas                   | Medir riesgo operativo     |
| Correcciones posteriores             | Medir calidad              |
| Piezas con fuente completa           | Medir trazabilidad         |
| Piezas con métricas registradas     | Medir disciplina operativa |

## 25.2 Metas iniciales

| Métrica                              | Meta |
| ------------------------------------- | ---: |
| Piezas publicadas con fuente          | 100% |
| Piezas con correlation_id             | 100% |
| Piezas sensibles con revisión humana | 100% |
| Publicaciones con URL registrada      | 100% |
| Correcciones materiales registradas   | 100% |
| Memorias con fuente                   | 100% |

---

# 26. Criterios de aceptación del runbook

Este runbook se considera correctamente ejecutado cuando:

* [ ] La noticia fue detectada y registrada.
* [ ] La fuente fue validada.
* [ ] La noticia fue clasificada.
* [ ] La prioridad fue asignada.
* [ ] El riesgo fue evaluado.
* [ ] Se creó brief editorial.
* [ ] Se redactó pieza base.
* [ ] Se adaptó al canal correcto.
* [ ] Se realizó revisión editorial.
* [ ] Se aprobó o escaló según riesgo.
* [ ] Se publicó o programó correctamente.
* [ ] Se registró URL.
* [ ] Se generó auditoría.
* [ ] Se programó medición.
* [ ] Se archivó la pieza.
* [ ] Se evaluó memoria editorial.
* [ ] El ciclo puede reconstruirse con correlation_id.

---

# 27. Relación con XMIP

XMIP debe soportar este runbook mediante:

* News Intake.
* Source Registry.
* Content Registry.
* Agent Execution Log.
* Workflow Runs.
* Publication Records.
* Metric Records.
* Editorial Memory.
* Knowledge Relationships.
* Audit Events.
* Approval Records.

El runbook debe convertirse gradualmente en workflow ejecutable dentro de XMIP.

---

# 28. Relación con otros documentos

Este documento se apoya en:

* ORION-005 — Constitución Editorial.
* ORION-006 — Estándares Editoriales.
* ORION-007 — Flujo Editorial.
* ORION-014 — Arquitectura de Agentes.
* ORION-018 — Operaciones Diarias.
* ORION-019 — Flujo de Publicación.

Este documento gobierna directamente:

* ORION-021 — Gestión de Fuentes.
* ORION-022 — Protocolo de Verificación Editorial.
* ORION-023 — Pipeline del Newsroom.
* ORION-025 — Distribución Multicanal.
* ORION-027 — Gestión de Incidentes Editoriales.
* ORION-028 — Operación de Agentes Editoriales.
* ORION-029 — Checklist Diario del Newsroom.

---

# 29. Próximos pasos

Después de aprobar ORION-020, continuar con:

1. ORION-021 — Gestión de Fuentes.
2. ORION-022 — Protocolo de Verificación Editorial.
3. ORION-023 — Pipeline del Newsroom.
4. ORION-024 — Calendario Editorial.
5. ORION-025 — Distribución Multicanal.

ORION-021 debe definir cómo se clasifican, evalúan, mantienen y auditan las fuentes del newsroom.

---

# 30. Historial de cambios

| Versión | Fecha      | Cambio                                                  | Autor            |
| -------- | ---------- | ------------------------------------------------------- | ---------------- |
| 1.0      | 2026-07-02 | Versión inicial del runbook de producción de noticias | Fernando Cuellar |
