# ORION-022 — Protocolo de Verificación Editorial

**Nivel documental:** L4 — Operations
**Volumen:** 006-operaciones
**Proyecto:** ORION / XCripto / XMIP
**Versión:** 1.0
**Estado:** Draft
**Owner:** Fernando Cuellar
**Última actualización:** 2026-07-02
**Ruta sugerida:** `docs/006-operaciones/ORION-022-Protocolo-de-Verificacion-Editorial.md`

---

## 1. Propósito

Este documento define el protocolo de verificación editorial de XCripto.

Su propósito es establecer cómo se valida una noticia antes de ser publicada, qué evidencia mínima se requiere, cómo se clasifican los niveles de confianza, cuándo se debe escalar una pieza, cuándo debe marcarse como rumor y cuándo debe rechazarse.

ORION-022 responde a la pregunta:

> ¿Cómo sabe XCripto que una noticia cripto está suficientemente verificada para publicarse?

Este protocolo protege la credibilidad del medio y reduce el riesgo de publicar rumores, información manipulada, datos incompletos o narrativas especulativas como si fueran hechos confirmados.

---

## 2. Alcance

Este documento cubre:

* Principios de verificación.
* Niveles de evidencia.
* Niveles de confianza editorial.
* Estados de verificación.
* Verificación por tipo de fuente.
* Verificación por tipo de noticia.
* Reglas para breaking news.
* Reglas para rumores.
* Reglas para hacks, exploits y seguridad.
* Reglas para regulación.
* Reglas para exchanges.
* Reglas para datos on-chain.
* Reglas para mercado y precio.
* Reglas para redes sociales.
* Escalamiento editorial.
* Uso de agentes.
* Checklist de verificación.
* Auditoría.
* Criterios de aceptación.

Este documento no cubre en detalle:

* Registro completo de fuentes.
* Producción paso a paso de una noticia.
* Publicación por canal.
* Distribución multicanal.
* Gestión de incidentes posteriores.
* Métricas operativas.

Esos temas se desarrollan en:

* ORION-019 — Flujo de Publicación.
* ORION-020 — Runbook de Producción de Noticias.
* ORION-021 — Gestión de Fuentes.
* ORION-025 — Distribución Multicanal.
* ORION-026 — Métricas Operativas.
* ORION-027 — Gestión de Incidentes Editoriales.

---

## 3. Contexto operativo

El ecosistema cripto es rápido, especulativo y vulnerable a manipulación informativa.

Una noticia puede originarse desde:

* Fuente oficial.
* Medio confiable.
* Cuenta social.
* Rumor.
* Filtración.
* Movimiento on-chain.
* Dashboard de mercado.
* Comunidad.
* Analista.
* Influencer.
* Bot.
* Documento legal.
* Publicación eliminada.
* Captura de pantalla.

No toda señal es noticia.
No toda noticia es publicable.
No toda fuente confiable elimina la necesidad de revisar.

XCripto debe operar bajo esta regla:

> Publicar tarde una noticia bien verificada es mejor que publicar rápido una mentira elegante.

---

## 4. Principios de verificación editorial

### 4.1 La carga de prueba está en la publicación

Si XCripto publica una afirmación, XCripto debe poder sostenerla con evidencia.

---

### 4.2 La velocidad no sustituye verificación

Una noticia urgente puede tener un flujo acelerado, pero nunca un flujo sin validación.

---

### 4.3 La incertidumbre debe declararse

Cuando algo no esté completamente confirmado, debe decirse claramente.

Ejemplo correcto:

```text
Hasta el momento, la información disponible indica...
```

Ejemplo incorrecto:

```text
Ya se confirmó que...
```

si todavía no existe confirmación suficiente.

---

### 4.4 La fuente primaria tiene prioridad

Cuando exista fuente primaria, debe revisarse antes de publicar.

---

### 4.5 La evidencia débil no permite lenguaje fuerte

Si la evidencia es parcial, el lenguaje debe ser parcial.

---

### 4.6 La verificación debe ser trazable

Cada publicación debe poder reconstruir:

* Fuente original.
* Fecha de consulta.
* Estado de verificación.
* Agente o humano que validó.
* Evidencia usada.
* Decisión editorial.
* Riesgo detectado.
* Correlation ID.

---

### 4.7 Los agentes no son autoridad final

Los agentes apoyan el proceso, pero no sustituyen revisión humana en temas sensibles.

---

## 5. Definiciones

### Hecho confirmado

Información respaldada por evidencia suficiente y fuente confiable.

### Hecho parcialmente confirmado

Información con evidencia razonable, pero todavía incompleta.

### Rumor

Información no confirmada, generalmente originada en fuente débil, social, anónima o contradictoria.

### Señal

Dato inicial que puede indicar una posible noticia, pero todavía no es publicable como hecho.

### Fuente primaria

Fuente que origina directamente la información.

### Fuente secundaria

Fuente que reporta o interpreta información originada por otra fuente.

### Evidencia

Elemento verificable que respalda una afirmación.

### Escalamiento

Proceso mediante el cual una noticia sensible se envía al Owner / Editor Principal para decisión.

### Retractación

Retiro formal de una pieza por error grave.

---

## 6. Estados de verificación

Toda noticia debe tener un estado de verificación.

| Estado             | Descripción                  | Acción permitida                       |
| ------------------ | ----------------------------- | --------------------------------------- |
| unverified         | No verificada                 | No publicar                             |
| validating         | En proceso de validación     | No publicar salvo alerta interna        |
| verified           | Verificada                    | Puede publicarse                        |
| partially_verified | Parcialmente verificada       | Publicar solo con lenguaje condicionado |
| rumor              | Rumor no confirmado           | No publicar como hecho                  |
| contradicted       | Información contradictoria   | Escalar o monitorear                    |
| rejected           | Rechazada                     | No publicar                             |
| escalated          | Escalada a revisión humana   | Esperar decisión                       |
| monitoring         | En seguimiento                | Observar sin publicar como hecho        |
| corrected          | Verificación corregida       | Actualizar registro                     |
| outdated           | Información vieja o superada | No publicar como noticia nueva          |

---

## 7. Niveles de evidencia

### 7.1 Nivel E0 — Sin evidencia

Descripción:

* No hay fuente clara.
* Solo existe comentario, captura o rumor.
* No hay forma de verificar.

Acción:

```text
No publicar.
```

---

### 7.2 Nivel E1 — Señal débil

Descripción:

* Fuente social no oficial.
* Comunidad.
* Captura sin origen.
* Comentario de influencer.
* Rumor en Telegram, Discord o Reddit.

Acción:

```text
Registrar como señal o monitoreo.
No publicar como hecho.
```

---

### 7.3 Nivel E2 — Evidencia secundaria

Descripción:

* Medio o analista reporta el hecho.
* La fuente cita parcialmente información.
* No se identificó fuente primaria.

Acción:

```text
Puede usarse para contexto.
Requiere confirmación adicional si el tema es sensible.
```

---

### 7.4 Nivel E3 — Evidencia secundaria confiable

Descripción:

* Medio reconocido.
* Analista confiable con historial.
* Reporte institucional.
* Fuente secundaria que enlaza evidencia primaria.

Acción:

```text
Puede apoyar publicación.
Temas sensibles requieren fuente primaria o segunda confirmación.
```

---

### 7.5 Nivel E4 — Evidencia primaria

Descripción:

* Comunicado oficial.
* Blog oficial.
* Documento regulatorio.
* Documento judicial.
* Repositorio oficial.
* Status page.
* Hash on-chain verificable.
* Declaración directa verificable.

Acción:

```text
Puede confirmar noticia.
Aun así debe revisarse contexto.
```

---

### 7.6 Nivel E5 — Evidencia primaria + confirmación independiente

Descripción:

* Fuente primaria.
* Fuente secundaria confiable.
* Evidencia técnica o documental.
* Contexto validado.

Acción:

```text
Nivel óptimo para noticias sensibles.
```

---

## 8. Niveles de confianza editorial

| Nivel | Nombre              | Descripción                                  | Publicación                   |
| ----- | ------------------- | --------------------------------------------- | ------------------------------ |
| C0    | Sin confianza       | No hay evidencia suficiente                   | No publicar                    |
| C1    | Baja confianza      | Señal débil o rumor                         | Monitorear                     |
| C2    | Confianza limitada  | Evidencia parcial                             | Publicar solo con advertencias |
| C3    | Confianza operativa | Evidencia suficiente                          | Publicable                     |
| C4    | Alta confianza      | Fuente primaria o equivalente                 | Publicable                     |
| C5    | Confianza crítica  | Fuente primaria + confirmación independiente | Publicable en temas sensibles  |

---

## 9. Matriz de decisión editorial

| Evidencia | Confianza | Estado                        | Acción                                                                 |
| --------- | --------- | ----------------------------- | ----------------------------------------------------------------------- |
| E0        | C0        | unverified                    | No publicar                                                             |
| E1        | C1        | rumor / monitoring            | Monitorear                                                              |
| E2        | C2        | partially_verified            | Publicar solo si no es sensible y con lenguaje condicionado             |
| E3        | C3        | verified / partially_verified | Publicable con revisión                                                |
| E4        | C4        | verified                      | Publicable                                                              |
| E5        | C5        | verified                      | Publicable incluso para temas sensibles, con revisión humana si aplica |

---

## 10. Verificación mínima obligatoria

Antes de publicar cualquier pieza, validar:

* [ ] Existe fuente registrada.
* [ ] La fuente tiene tipo asignado.
* [ ] La fecha fue confirmada.
* [ ] La información no es vieja reciclada.
* [ ] La afirmación principal está respaldada.
* [ ] El titular no excede la evidencia.
* [ ] El estado de verificación está asignado.
* [ ] El nivel de confianza está asignado.
* [ ] El riesgo editorial está asignado.
* [ ] Existe correlation_id.
* [ ] Se registró quién o qué agente verificó.
* [ ] Se definió si requiere aprobación humana.

---

## 11. Verificación por tipo de fuente

### 11.1 Fuente primaria

Validar:

* Dominio oficial.
* Cuenta oficial.
* Fecha.
* Autoridad emisora.
* Contexto.
* Si hay actualización posterior.
* Si aplica a la jurisdicción o entidad correcta.

Uso permitido:

* Confirmación principal.

---

### 11.2 Fuente secundaria confiable

Validar:

* Historial de la fuente.
* Si cita fuente primaria.
* Si enlaza evidencia.
* Si otros medios reportan lo mismo.
* Si hay correcciones previas.

Uso permitido:

* Apoyo editorial.
* Confirmación en noticias no sensibles.
* Contexto adicional.

---

### 11.3 Fuente social oficial

Validar:

* Que la cuenta sea oficial.
* Que no sea impersonator.
* Fecha y hora.
* Si la publicación sigue activa.
* Si coincide con otros canales oficiales.

Uso permitido:

* Confirmación si la identidad es clara.
* Aun así, temas sensibles requieren cuidado.

---

### 11.4 Fuente social no verificada

Validar:

* Identidad.
* Historial.
* Posible conflicto de interés.
* Evidencia adjunta.
* Confirmación externa.

Uso permitido:

* Señal.
* Monitoreo.
* Nunca como única confirmación en temas sensibles.

---

### 11.5 Fuente on-chain

Validar:

* Hash.
* Dirección.
* Red.
* Timestamp.
* Contrato.
* Etiqueta de wallet.
* Fuente de la etiqueta.
* Interpretación.

Uso permitido:

* Evidencia técnica.
* Debe separarse el dato de la interpretación.

---

### 11.6 Fuente regulatoria o legal

Validar:

* Autoridad emisora.
* Jurisdicción.
* Fecha.
* Número de expediente.
* Estado del documento.
* Si es propuesta, demanda, sanción, aprobación o resolución.

Uso permitido:

* Alta confianza.
* Requiere interpretación cuidadosa.

---

### 11.7 Fuente de mercado

Validar:

* Proveedor.
* Hora de consulta.
* Métrica exacta.
* Activo.
* Exchange o mercado.
* Si hay discrepancias entre proveedores.

Uso permitido:

* Contexto cuantitativo.
* No confirma causalidad por sí sola.

---

## 12. Verificación por tipo de noticia

### 12.1 Noticias de mercado

Requieren:

* Datos de mercado verificables.
* Hora de consulta.
* Activo o par.
* Contexto.
* Evitar causalidad no demostrada.

Prohibido:

```text
BTC cae por esta razón
```

si no hay evidencia clara de causalidad.

Preferible:

```text
BTC cae mientras el mercado reacciona a...
```

---

### 12.2 Hacks y exploits

Requieren:

* Fuente primaria, postmortem, investigador confiable o evidencia on-chain.
* Revisión humana.
* Claridad sobre monto si aplica.
* Claridad sobre protocolo afectado.
* Claridad sobre si el incidente está confirmado.

No publicar:

* Monto no verificado.
* Culpables sin evidencia.
* Atribuciones débiles.
* Capturas sin fuente.

Estado mínimo:

```text
verified
```

o

```text
partially_verified
```

con lenguaje muy controlado.

---

### 12.3 Regulación

Requiere:

* Documento oficial.
* Comunicado de regulador.
* Filing.
* Documento judicial.
* Fuente legal confiable.

Validar:

* Jurisdicción.
* Estado del proceso.
* Fecha.
* Entidad afectada.
* Si es propuesta o decisión final.

Toda noticia regulatoria sensible requiere revisión humana.

---

### 12.4 Exchanges

Aplica a:

* Retiros detenidos.
* Insolvencia.
* Proof of reserves.
* Listados.
* Delistings.
* Hacks.
* Demandas.
* Caídas de servicio.

Requiere:

* Comunicado oficial.
* Status page.
* Fuente secundaria confiable.
* Evidencia técnica si aplica.

Prohibido publicar como hecho:

```text
El exchange está insolvente
```

sin evidencia fuerte.

---

### 12.5 ETFs e institucional

Requiere:

* Filing.
* Documento oficial.
* Comunicado institucional.
* Fuente financiera confiable.
* Confirmación de estado: solicitado, aprobado, rechazado, diferido.

Regla:

No confundir solicitud con aprobación.

---

### 12.6 On-chain

Requiere:

* Hash o dirección.
* Red correcta.
* Fecha/hora.
* Etiqueta de wallet validada.
* Separación entre dato e interpretación.

Ejemplo correcto:

```text
Una wallet etiquetada por [proveedor] movió fondos hacia [destino].
```

Ejemplo riesgoso:

```text
Esta ballena está vendiendo todo.
```

si no hay evidencia suficiente.

---

### 12.7 Scams y fraudes

Requiere:

* Evidencia verificable.
* Revisión humana.
* Lenguaje cuidadoso.
* Evitar acusaciones directas sin respaldo.
* Documentar fuente y riesgo.

Preferir:

```text
Usuarios reportan posible fraude...
```

solo si está bien marcado y contextualizado.

---

### 12.8 Noticias educativas

Requieren:

* Fuentes base confiables.
* Claridad conceptual.
* No presentar opinión como hecho.
* No simplificar al punto de distorsionar.

---

### 12.9 Opinión y análisis

Requieren:

* Separación explícita de hechos y opinión.
* Fuente base.
* Disclaimer si toca inversión, mercado o riesgos.
* Claridad de que no es recomendación financiera.

---

## 13. Protocolo para breaking news

### 13.1 Objetivo

Publicar rápido sin sacrificar precisión.

### 13.2 Flujo

```text
detectar
→ registrar
→ validar fuente mínima fuerte
→ escalar
→ publicar alerta limitada
→ monitorear
→ actualizar
→ producir pieza extendida
```

### 13.3 Reglas

* Publicar solo lo confirmado.
* Marcar lo que falta por confirmar.
* No especular con impacto.
* No atribuir culpables sin evidencia.
* Actualizar conforme cambie la información.
* Registrar cada actualización.
* Mantener URL o hilo de seguimiento.

### 13.4 Texto base

```text
ALERTA XCRIPTO

Qué está confirmado:
[hecho confirmado]

Qué falta por confirmar:
[puntos pendientes]

Contexto:
[contexto mínimo]

Fuente:
[referencia]

Seguimiento en desarrollo.
```

### 13.5 Requisito mínimo

Breaking news debe tener al menos:

* Fuente confiable.
* Validación de fecha.
* Revisión humana si es sensible.
* Estado `verified`, `partially_verified` o `escalated`.
* Nunca `unverified`.

---

## 14. Protocolo para rumores

### 14.1 Definición

Un rumor es información no confirmada con evidencia insuficiente, contradictoria o dependiente de fuente débil.

### 14.2 Reglas

* No publicar como hecho.
* No usar titular afirmativo.
* No convertir rumor en alerta.
* No amplificar si puede causar daño innecesario.
* Mantener en estado `monitoring` o `rumor`.
* Escalar si puede afectar mercado o reputación.

### 14.3 Cuándo puede mencionarse un rumor

Solo puede mencionarse si:

* El rumor ya tiene alto impacto público.
* Es necesario aclarar que no está confirmado.
* Se aporta contexto y advertencia.
* El Editor Principal aprueba.

### 14.4 Formato permitido

```text
Circula información no confirmada sobre [tema].

Hasta ahora:
- No existe confirmación oficial.
- La fuente primaria no ha emitido postura.
- XCripto lo mantiene en seguimiento.

No debe tratarse como hecho confirmado.
```

---

## 15. Protocolo para información contradictoria

### 15.1 Cuándo aplica

Cuando dos o más fuentes confiables dicen cosas distintas.

### 15.2 Acción

* Registrar ambas fuentes.
* Identificar contradicción exacta.
* Buscar fuente primaria.
* Marcar estado `contradicted`.
* Escalar si el tema es sensible.
* No publicar conclusión definitiva.

### 15.3 Formato permitido

```text
Existen versiones contradictorias sobre [tema].

Fuente A indica:
[versión A]

Fuente B indica:
[versión B]

Por ahora, XCripto mantiene la información en seguimiento hasta contar con confirmación adicional.
```

---

## 16. Protocolo para noticia vieja reciclada

### 16.1 Señales de alerta

* Misma noticia publicada meses atrás.
* Captura sin fecha.
* Medio republica sin contexto.
* Influencer revive narrativa.
* No hay nuevo evento.

### 16.2 Validaciones

* Revisar fecha original.
* Revisar si hubo actualización real.
* Buscar fuente primaria.
* Confirmar si el hecho es nuevo o seguimiento.

### 16.3 Acción

Si no hay novedad:

```text
No publicar como noticia nueva.
```

Puede usarse como contexto histórico si se marca correctamente.

---

## 17. Protocolo para capturas de pantalla

### 17.1 Regla base

Una captura de pantalla no es evidencia suficiente por sí sola.

### 17.2 Validar

* Origen.
* URL.
* Fecha.
* Cuenta o sitio.
* Si el contenido sigue disponible.
* Si hay archivo verificable.
* Si hay manipulación visual.
* Si hay fuente alternativa.

### 17.3 Acción

* Si no se puede verificar: `rumor` o `rejected`.
* Si se verifica con fuente primaria: puede usarse.
* Si es sensible: escalar.

---

## 18. Protocolo para contenido generado por IA

### 18.1 Riesgo

Contenido generado por IA puede contener errores, inventar fuentes o resumir mal.

### 18.2 Regla

Ningún resumen generado por IA puede ser fuente primaria.

### 18.3 Uso permitido

* Apoyo de resumen.
* Organización.
* Comparación.
* Borrador.
* Clasificación.

### 18.4 Uso prohibido

* Confirmación factual.
* Cita de fuente no verificada.
* Sustituto de documento original.
* Validación legal, financiera o técnica definitiva.

---

## 19. Escalamiento editorial

### 19.1 Escalar obligatoriamente si la noticia involucra

* Hack.
* Exploit.
* Fraude.
* Insolvencia.
* Exchange importante.
* Regulador.
* Demanda.
* Persona o empresa señalada.
* Riesgo reputacional.
* Información contradictoria.
* Fuente anónima.
* Posible manipulación de mercado.
* Acusación directa.
* Impacto fuerte en BTC, ETH o mercado general.

### 19.2 Estados de escalamiento

| Estado                    | Descripción                       |
| ------------------------- | ---------------------------------- |
| escalation_required       | Debe escalarse                     |
| escalated                 | Ya fue escalada                    |
| approved_after_escalation | Aprobada después de escalamiento  |
| rejected_after_escalation | Rechazada después de escalamiento |
| held_after_escalation     | En espera                          |

### 19.3 Registro mínimo

```text
escalation_id
news_id
reason
risk_level
requested_by
approved_by
decision
decision_at
correlation_id
```

---

## 20. Rol de agentes en verificación

### 20.1 SourceValidatorAgent

Responsabilidades:

* Validar tipo de fuente.
* Buscar fuente primaria.
* Detectar duplicados.
* Revisar fecha.
* Asignar confianza preliminar.

---

### 20.2 RiskAgent

Responsabilidades:

* Detectar riesgo editorial.
* Marcar lenguaje especulativo.
* Identificar potencial de manipulación.
* Recomendar escalamiento.

---

### 20.3 MarketImpactAgent

Responsabilidades:

* Evaluar impacto potencial.
* Relacionar noticia con activos o narrativas.
* Evitar causalidad no demostrada.

---

### 20.4 AuditAgent

Responsabilidades:

* Confirmar que la verificación dejó evidencia.
* Validar correlation_id.
* Detectar publicaciones sin fuente.
* Registrar eventos.

---

### 20.5 MemoryAgent

Responsabilidades:

* Guardar aprendizajes de verificación.
* Marcar fuentes problemáticas.
* Proponer memoria editorial útil.

---

## 21. Datos mínimos de verificación en XMIP

### 21.1 VerificationRecord

```text
verification_id
news_id
status
evidence_level
confidence_level
verified_by
verified_at
source_refs
risk_level
notes
correlation_id
```

### 21.2 EvidenceRecord

```text
evidence_id
verification_id
evidence_type
source_ref
description
url
captured_at
confidence
metadata
```

### 21.3 EscalationRecord

```text
escalation_id
news_id
reason
risk_level
requested_by
decision
decided_by
decided_at
notes
correlation_id
```

### 21.4 VerificationDecision

```text
decision_id
verification_id
decision
reason
approved_for_publication
language_constraints
required_disclaimer
created_at
created_by
```

---

## 22. Lenguaje permitido según nivel de verificación

### 22.1 Verificado

Permitido:

```text
confirmó
anunció
publicó
reportó oficialmente
de acuerdo con el comunicado
según el documento oficial
```

---

### 22.2 Parcialmente verificado

Permitido:

```text
indica
apunta a
según información preliminar
hasta ahora se sabe
la información disponible muestra
```

---

### 22.3 Rumor

Permitido:

```text
circula información no confirmada
aún no existe confirmación oficial
se mantiene en seguimiento
no debe tratarse como hecho confirmado
```

---

### 22.4 Prohibido si no hay verificación fuerte

```text
se confirmó
es oficial
está demostrado
ya es un hecho
sin duda
garantizado
colapsó
quebró
hackearon
robó
fraude confirmado
```

---

## 23. Disclaimers de verificación

### 23.1 Disclaimer informativo

```text
Este contenido es informativo y educativo. No constituye asesoría financiera, legal ni de inversión.
```

### 23.2 Disclaimer de información preliminar

```text
La información está en desarrollo y puede actualizarse conforme existan nuevas fuentes o confirmaciones oficiales.
```

### 23.3 Disclaimer de rumor

```text
Esta información no está confirmada oficialmente. XCripto la mantiene en seguimiento y no debe interpretarse como hecho verificado.
```

### 23.4 Disclaimer de mercado

```text
Los movimientos de mercado pueden responder a múltiples factores. Este contenido no debe interpretarse como recomendación de compra, venta o inversión.
```

---

## 24. Checklist general de verificación

Antes de aprobar publicación:

* [ ] ¿Existe fuente registrada?
* [ ] ¿La fuente tiene tipo asignado?
* [ ] ¿La fuente no está bloqueada?
* [ ] ¿La fecha fue validada?
* [ ] ¿Existe fuente primaria?
* [ ] ¿Se consultó fuente primaria si existe?
* [ ] ¿La afirmación principal está respaldada?
* [ ] ¿Hay fuentes contradictorias?
* [ ] ¿Se asignó nivel de evidencia?
* [ ] ¿Se asignó nivel de confianza?
* [ ] ¿Se asignó estado de verificación?
* [ ] ¿Se evaluó riesgo editorial?
* [ ] ¿Requiere escalamiento?
* [ ] ¿El titular corresponde a la evidencia?
* [ ] ¿El lenguaje es proporcional al nivel de evidencia?
* [ ] ¿Se agregó disclaimer si aplica?
* [ ] ¿Se registró correlation_id?
* [ ] ¿AuditAgent puede reconstruir el proceso?

---

## 25. Checklist por tipo sensible

### 25.1 Hack / exploit

* [ ] Fuente primaria o evidencia técnica.
* [ ] Hash / dirección / reporte si aplica.
* [ ] Protocolo afectado confirmado.
* [ ] Monto confirmado o marcado como estimado.
* [ ] No hay atribución sin evidencia.
* [ ] Revisión humana completada.

---

### 25.2 Regulación

* [ ] Documento oficial.
* [ ] Jurisdicción clara.
* [ ] Fecha validada.
* [ ] Estado del proceso identificado.
* [ ] No se confunde propuesta con aprobación.
* [ ] Revisión humana completada.

---

### 25.3 Exchange

* [ ] Comunicado oficial o evidencia fuerte.
* [ ] Status page revisada si aplica.
* [ ] Segunda fuente si es sensible.
* [ ] No se afirma insolvencia sin evidencia.
* [ ] Revisión humana completada.

---

### 25.4 Mercado

* [ ] Fuente de datos registrada.
* [ ] Hora de consulta.
* [ ] No se afirma causalidad no demostrada.
* [ ] No hay recomendación financiera.
* [ ] Disclaimer incluido si aplica.

---

### 25.5 Rumor

* [ ] Estado `rumor` o `monitoring`.
* [ ] No se publica como hecho.
* [ ] Se identifica fuente original.
* [ ] Se define seguimiento.
* [ ] Escalamiento si hay riesgo alto.

---

## 26. Auditoría de verificación

### 26.1 Eventos obligatorios

| Evento                      | Cuándo ocurre                                 |
| --------------------------- | ---------------------------------------------- |
| verification_started        | Inicia verificación                           |
| source_checked              | Se revisa fuente                               |
| primary_source_checked      | Se revisa fuente primaria                      |
| evidence_recorded           | Se registra evidencia                          |
| verification_status_changed | Cambia estado                                  |
| confidence_assigned         | Se asigna confianza                            |
| risk_assessed               | Se evalúa riesgo                              |
| escalation_requested        | Se escala                                      |
| verification_approved       | Se aprueba verificación                       |
| verification_rejected       | Se rechaza verificación                       |
| publication_blocked         | Se bloquea publicación por falta de evidencia |

### 26.2 Formato mínimo de evento

```json
{
  "event_type": "verification_approved",
  "news_id": "news_001",
  "verification_id": "ver_001",
  "evidence_level": "E4",
  "confidence_level": "C4",
  "status": "verified",
  "actor_type": "user",
  "actor_ref": "editor_principal",
  "correlation_id": "corr_20260702_xxxxxx",
  "occurred_at": "2026-07-02T00:00:00Z"
}
```

---

## 27. Métricas de verificación

| Métrica                                        | Propósito                     |
| ----------------------------------------------- | ------------------------------ |
| Noticias verificadas                            | Medir volumen aprobado         |
| Noticias rechazadas                             | Medir filtro editorial         |
| Noticias en rumor                               | Medir ruido informativo        |
| Noticias escaladas                              | Medir riesgo editorial         |
| Tiempo promedio de verificación                | Medir eficiencia               |
| Correcciones posteriores                        | Medir calidad de verificación |
| Publicaciones con fuente primaria               | Medir fortaleza editorial      |
| Publicaciones con fuente social única          | Detectar riesgo                |
| Publicaciones bloqueadas por falta de evidencia | Medir disciplina               |
| Fuentes contradictorias detectadas              | Medir complejidad informativa  |

Metas iniciales:

| Métrica                                       |                            Meta |
| ---------------------------------------------- | ------------------------------: |
| Publicaciones con VerificationRecord           |                            100% |
| Piezas sensibles con escalamiento              |                            100% |
| Rumores publicados como hecho                  |                               0 |
| Publicaciones sin fuente registrada            |                               0 |
| Correcciones materiales por mala verificación | 0 objetivo, registrar si ocurre |

---

## 28. Riesgos y mitigaciones

| Riesgo                                    | Impacto | Probabilidad | Mitigación                        |
| ----------------------------------------- | ------: | -----------: | ---------------------------------- |
| Publicar rumor como hecho                 |    Alto |        Media | Estados`rumor` y `monitoring`  |
| Exagerar titular                          |    Alto |        Media | Revisión proporcional a evidencia |
| Usar fuente social como confirmación     |    Alto |         Alta | Matriz de fuente mínima           |
| Interpretar mal dato on-chain             |    Alto |        Media | Separar dato de interpretación    |
| Confundir propuesta legal con aprobación |    Alto |        Media | Checklist regulatorio              |
| Publicar noticia vieja como nueva         |   Medio |        Media | Validación de fecha original      |
| Omitir incertidumbre                      |    Alto |        Media | Lenguaje según confianza          |
| Agente inventa fuente                     |    Alto |        Media | Fuente verificable obligatoria     |
| Falta de trazabilidad                     |    Alto |        Media | VerificationRecord y AuditEvent    |
| Corrección silenciosa                    |    Alto |         Baja | Flujo de corrección y auditoría  |

---

## 29. Antipatrones prohibidos

XCripto debe evitar:

* Publicar por presión de velocidad.
* Usar “se dice” como confirmación.
* Citar screenshots sin origen.
* Afirmar causalidad de mercado sin evidencia.
* Usar IA como fuente.
* Confundir rumor viral con noticia.
* No revisar fecha.
* No buscar fuente primaria.
* No escalar temas sensibles.
* Publicar titulares más fuertes que la evidencia.
* Corregir errores materiales sin registro.
* Borrar publicaciones críticas sin auditoría.
* Presentar opinión como hecho.
* Presentar análisis como recomendación financiera.

---

## 30. Relación con XMIP

XMIP debe soportar este protocolo mediante:

* Source Registry.
* Verification Records.
* Evidence Records.
* Escalation Records.
* Risk classification.
* Agent execution logs.
* Audit events.
* Publication blocking rules.
* Memory records.
* Knowledge relationships.

El protocolo debe convertirse gradualmente en una capacidad del sistema:

```text
si verificación insuficiente
→ bloquear publicación
→ solicitar fuente adicional
→ escalar si es sensible
```

---

## 31. Relación con otros documentos

Este documento se apoya en:

* ORION-005 — Constitución Editorial.
* ORION-006 — Estándares Editoriales.
* ORION-007 — Flujo Editorial.
* ORION-018 — Operaciones Diarias.
* ORION-019 — Flujo de Publicación.
* ORION-020 — Runbook de Producción de Noticias.
* ORION-021 — Gestión de Fuentes.

Este documento gobierna directamente:

* ORION-023 — Pipeline del Newsroom.
* ORION-025 — Distribución Multicanal.
* ORION-027 — Gestión de Incidentes Editoriales.
* ORION-028 — Operación de Agentes Editoriales.
* ORION-029 — Checklist Diario del Newsroom.

---

## 32. Criterios de aceptación

Este documento se considera aceptado cuando:

* [ ] Define principios de verificación editorial.
* [ ] Define estados de verificación.
* [ ] Define niveles de evidencia.
* [ ] Define niveles de confianza.
* [ ] Define matriz de decisión editorial.
* [ ] Define verificación mínima obligatoria.
* [ ] Define verificación por tipo de fuente.
* [ ] Define verificación por tipo de noticia.
* [ ] Define protocolo de breaking news.
* [ ] Define protocolo de rumores.
* [ ] Define protocolo para información contradictoria.
* [ ] Define protocolo para noticia vieja reciclada.
* [ ] Define protocolo para capturas de pantalla.
* [ ] Define protocolo para contenido generado por IA.
* [ ] Define reglas de escalamiento.
* [ ] Define rol de agentes.
* [ ] Define datos mínimos en XMIP.
* [ ] Define lenguaje permitido según nivel de verificación.
* [ ] Define disclaimers.
* [ ] Define checklists.
* [ ] Define auditoría.
* [ ] Define métricas.
* [ ] Define riesgos y mitigaciones.
* [ ] Define relación con XMIP.

---

## 33. Próximos pasos

Después de aprobar ORION-022, continuar con:

1. ORION-023 — Pipeline del Newsroom.
2. ORION-024 — Calendario Editorial.
3. ORION-025 — Distribución Multicanal.
4. ORION-026 — Métricas Operativas.
5. ORION-027 — Gestión de Incidentes Editoriales.

ORION-023 debe convertir operaciones, publicación, fuentes y verificación en un pipeline completo del newsroom dentro de XMIP.

---

## 34. Historial de cambios

| Versión | Fecha      | Cambio                                                    | Autor            |
| -------- | ---------- | --------------------------------------------------------- | ---------------- |
| 1.0      | 2026-07-02 | Versión inicial del protocolo de verificación editorial | Fernando Cuellar |
