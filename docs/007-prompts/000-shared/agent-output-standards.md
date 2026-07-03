
# XMIP Agent Output Standards

**Proyecto:** Project ORION / XCripto
**Sistema:** XMIP — XCripto Media Intelligence Platform
**Nivel documental:** L4 — Operaciones / L5 — Ejecución
**Dominio:** Prompts / Agentes / Orquestación / Salidas estructuradas
**Estado:** Aprobado para implementación inicial
**Versión:** 1.0.0
**Owner:** XCripto Architecture Office
**Última actualización:** 2026-07-02
**Documento relacionado:** `docs/007-prompts/000-shared/agent-base-contract.md`

---

## 1. Propósito

Este documento define el estándar obligatorio de salida para todos los agentes digitales de XMIP, sin importar si se ejecutan en GPT, Claude, Hermes u otro runtime futuro.

El objetivo es que cada salida producida por un agente sea:

```text
- estructurada
- trazable
- auditable
- reutilizable
- evaluable
- persistible
- apta para orquestación
```

XMIP no debe depender de texto libre difícil de procesar.

Los agentes pueden redactar en lenguaje natural, pero toda salida operativa debe contener una sección estructurada que pueda ser interpretada por humanos, sistemas y futuros workflows.

---

## 2. Principio rector

Toda salida de agente debe poder responder:

```text
¿Qué se recibió?
¿Qué se procesó?
Qué se concluyó?
Con qué evidencia?
Con qué nivel de confianza?
Qué riesgos existen?
Qué debe pasar después?
Quién debe revisar?
Qué debe guardar XMIP?
```

Si una salida no puede responder estas preguntas, no es una salida válida para XMIP.

---

## 3. Formatos permitidos

Los agentes pueden generar salidas en los siguientes formatos:

```text
markdown
json
yaml
hybrid-markdown-json
```

La regla inicial de XMIP es:

```text
Markdown para revisión humana.
JSON para persistencia, integración y orquestación.
Hybrid Markdown + JSON para operación editorial.
```

---

## 4. Formato recomendado por tipo de uso

### 4.1 Revisión humana

Para revisión editorial, análisis y discusión operativa:

```text
hybrid-markdown-json
```

Debe incluir:

```text
- Resumen ejecutivo en Markdown
- Evidencia en Markdown
- Riesgos en Markdown
- Bloque JSON final con salida estructurada
```

---

### 4.2 Integración con XMIP

Para backend, agentes encadenados, workflows y persistencia:

```text
json
```

Debe cumplir con el esquema base definido en este documento.

---

### 4.3 Operación local con Hermes

Para ejecución desde terminal, VSCode o scripts:

```text
markdown + json
```

Debe incluir:

```text
- acciones ejecutadas
- archivos leídos
- archivos modificados
- validaciones realizadas
- errores encontrados
- salida estructurada
```

---

## 5. Estructura mínima obligatoria

Toda salida de agente debe contener estas secciones:

```markdown
# Resultado del Agente

## 1. Resumen Ejecutivo

## 2. Entrada Procesada

## 3. Análisis

## 4. Evidencia Utilizada

## 5. Nivel de Confianza

## 6. Riesgos e Incertidumbre

## 7. Salida Estructurada

## 8. Siguiente Acción Recomendada

## 9. Revisión Humana
```

Los prompts específicos pueden ampliar esta estructura, pero no eliminar estos elementos salvo que el runtime exija salida JSON pura.

---

## 6. Esquema JSON base

Toda salida estructurada debe poder expresarse con este esquema base:

```json
{
  "output_metadata": {
    "agent_name": "",
    "agent_type": "",
    "runtime": "",
    "prompt_version": "",
    "task_id": "",
    "execution_id": "",
    "created_at": "",
    "language": "es",
    "human_review_required": true
  },
  "input_summary": {
    "input_type": "",
    "input_sources": [],
    "input_received": "",
    "processing_scope": ""
  },
  "result": {
    "summary": "",
    "key_findings": [],
    "analysis": "",
    "confidence_level": "",
    "decision": "",
    "recommended_next_action": ""
  },
  "evidence": [],
  "risks": [],
  "uncertainties": [],
  "handoff": {
    "next_agent": "",
    "requested_action": "",
    "handoff_required": false
  },
  "knowledge_graph_candidates": {
    "entities": [],
    "relationships": []
  },
  "quality_control": {
    "format_valid": true,
    "evidence_sufficient": false,
    "source_conflicts_detected": false,
    "requires_escalation": false,
    "escalation_reason": ""
  }
}
```

---

## 7. Campos obligatorios

### 7.1 `output_metadata`

Define la identidad operativa de la salida.

```json
{
  "agent_name": "NewsScoutAgent",
  "agent_type": "research",
  "runtime": "claude",
  "prompt_version": "1.0.0",
  "task_id": "signal-2026-07-02-001",
  "execution_id": "exec-2026-07-02-001",
  "created_at": "2026-07-02T00:00:00-07:00",
  "language": "es",
  "human_review_required": true
}
```

Reglas:

```text
- agent_name debe coincidir con la documentación oficial de agentes.
- runtime debe indicar gpt, claude, hermes u otro runtime aprobado.
- prompt_version debe existir en el encabezado del prompt usado.
- task_id debe conectar la salida con un workflow o solicitud.
- execution_id debe identificar una ejecución específica.
- created_at debe usar formato ISO 8601.
- language debe ser "es" salvo excepción justificada.
```

---

### 7.2 `input_summary`

Resume lo que recibió el agente.

```json
{
  "input_type": "news_signal",
  "input_sources": [
    "https://example.com/source"
  ],
  "input_received": "Se recibió una señal sobre posible regulación de stablecoins.",
  "processing_scope": "Identificar relevancia editorial inicial y recomendar validación."
}
```

Reglas:

```text
- No copiar entradas largas completas si no es necesario.
- Resumir la entrada con precisión.
- Conservar URLs o referencias necesarias.
- Declarar el alcance real del procesamiento.
```

---

### 7.3 `result`

Contiene la salida principal del agente.

```json
{
  "summary": "La señal parece editorialmente relevante, pero requiere validación primaria.",
  "key_findings": [
    "El tema involucra stablecoins.",
    "Existe posible impacto regulatorio.",
    "La fuente inicial no es primaria."
  ],
  "analysis": "La señal puede afectar la narrativa de mercado si se confirma por un regulador o institución primaria.",
  "confidence_level": "medio",
  "decision": "send_to_validation",
  "recommended_next_action": "Enviar a SourceValidatorAgent para validación de fuente, fecha y autoridad emisora."
}
```

Reglas:

```text
- summary debe ser breve y accionable.
- key_findings debe separar hallazgos en puntos claros.
- analysis debe distinguir hecho, análisis e inferencia.
- confidence_level debe usar la escala oficial.
- decision debe ser una decisión operativa.
- recommended_next_action debe indicar el siguiente paso concreto.
```

---

## 8. Escala oficial de confianza

Los únicos valores permitidos son:

```text
alto
medio
bajo
insuficiente
```

### 8.1 `alto`

Uso permitido cuando:

```text
- Hay fuente primaria.
- La información es verificable.
- No hay contradicciones relevantes.
- La evidencia es suficiente para continuar el workflow.
```

### 8.2 `medio`

Uso permitido cuando:

```text
- Hay evidencia razonable.
- Puede faltar una fuente primaria.
- La interpretación requiere contexto.
- El riesgo de error existe, pero es manejable.
```

### 8.3 `bajo`

Uso obligatorio cuando:

```text
- La fuente es secundaria o débil.
- La información está incompleta.
- Existen dudas relevantes.
- La salida requiere validación antes de cualquier uso editorial.
```

### 8.4 `insuficiente`

Uso obligatorio cuando:

```text
- No hay evidencia verificable.
- La entrada es ambigua.
- Hay contradicciones fuertes.
- Continuar requeriría inventar información.
```

---

## 9. Evidencia

La evidencia debe representarse como una lista de objetos.

```json
[
  {
    "evidence_id": "ev-001",
    "type": "url",
    "source_name": "Example Source",
    "source_url": "https://example.com/source",
    "published_at": "2026-07-02T00:00:00-07:00",
    "accessed_at": "2026-07-02T00:00:00-07:00",
    "source_tier": "secondary",
    "relevance": "La fuente menciona el evento inicial.",
    "limitations": "No es fuente primaria.",
    "confidence_contribution": "medio"
  }
]
```

---

## 10. Tipos de evidencia permitidos

Valores recomendados para `type`:

```text
url
document
transcript
dataset
market_data
social_post
official_statement
onchain_data
internal_note
manual_observation
```

---

## 11. Clasificación de fuentes

Valores recomendados para `source_tier`:

```text
primary
secondary
tertiary
unknown
```

### 11.1 Fuente primaria

Ejemplos:

```text
- comunicado oficial
- filing regulatorio
- blog oficial de protocolo
- documentación técnica oficial
- repositorio oficial
- transacción onchain verificable
- anuncio directo de una empresa o regulador
```

### 11.2 Fuente secundaria

Ejemplos:

```text
- medio de noticias
- análisis externo
- newsletter
- entrevista publicada
- reporte de research
```

### 11.3 Fuente terciaria

Ejemplos:

```text
- resumen de terceros
- publicación agregada
- comentario en redes
- captura sin fuente original
```

### 11.4 Fuente desconocida

Uso obligatorio cuando:

```text
- no se conoce el origen
- la URL no está disponible
- la evidencia no puede verificarse
- el contenido viene de una cadena informal
```

---

## 12. Riesgos

Los riesgos deben expresarse como objetos estructurados.

```json
[
  {
    "risk_id": "risk-001",
    "risk_type": "source_quality",
    "description": "La fuente inicial no es primaria.",
    "severity": "medio",
    "mitigation": "Validar contra fuente oficial antes de producir contenido."
  }
]
```

Valores recomendados para `risk_type`:

```text
source_quality
market_misinterpretation
legal
regulatory
reputational
financial_advice
editorial_bias
outdated_information
incomplete_context
automation_error
```

Valores permitidos para `severity`:

```text
alto
medio
bajo
```

---

## 13. Incertidumbre

Las incertidumbres deben separarse de los riesgos.

```json
[
  {
    "uncertainty_id": "unc-001",
    "description": "No se ha confirmado si el anuncio proviene de una autoridad oficial.",
    "impact": "Puede cambiar completamente el tratamiento editorial.",
    "data_needed": "Fuente primaria o comunicado oficial."
  }
]
```

Diferencia obligatoria:

```text
Riesgo = algo que puede causar daño operativo, editorial o reputacional.
Incertidumbre = algo que todavía no se sabe con suficiente claridad.
```

---

## 14. Decisiones operativas permitidas

El campo `decision` debe usar valores controlados.

Valores iniciales:

```text
accept
reject
needs_validation
send_to_validation
send_to_editorial
send_to_market_impact
send_to_script
send_to_distribution
send_to_memory
escalate_to_human
insufficient_information
no_action
```

Cada agente puede restringir su propia lista de decisiones válidas.

---

## 15. Handoff entre agentes

Cuando una salida requiere pasar a otro agente, debe incluir:

```json
{
  "handoff": {
    "next_agent": "SourceValidatorAgent",
    "requested_action": "Validar fuente, fecha, autoridad emisora y confiabilidad.",
    "handoff_required": true
  }
}
```

Reglas:

```text
- next_agent debe ser un agente documentado.
- requested_action debe ser concreta.
- handoff_required debe ser true si otro agente debe continuar.
- No se debe mandar trabajo a un agente inexistente.
```

---

## 16. Knowledge Graph candidates

Cuando aplique, los agentes deben proponer candidatos para el Knowledge Graph.

```json
{
  "knowledge_graph_candidates": {
    "entities": [
      {
        "name": "Bitcoin",
        "type": "Token",
        "confidence_level": "alto",
        "source_evidence_id": "ev-001"
      },
      {
        "name": "SEC",
        "type": "Regulador",
        "confidence_level": "alto",
        "source_evidence_id": "ev-002"
      }
    ],
    "relationships": [
      {
        "source": "SEC",
        "relation": "regula",
        "target": "Bitcoin ETF",
        "confidence_level": "medio",
        "source_evidence_id": "ev-002"
      }
    ]
  }
}
```

---

## 17. Tipos iniciales de entidades

Valores permitidos inicialmente:

```text
Persona
Organización
Protocolo
Token
Blockchain
Regulador
Evento
Fuente
Narrativa
Riesgo
Publicación
Producto
Empresa
País
Ley
Exchange
Wallet
Contrato
DAO
```

---

## 18. Tipos iniciales de relaciones

Valores permitidos inicialmente:

```text
menciona
pertenece_a
afecta_a
contradice
confirma
depende_de
regula
invierte_en
desarrolla
publica
valida
opera
emite
investiga
sanciona
adquiere
integra
compite_con
relacionado_con
```

---

## 19. Quality control

Todo agente debe incluir una sección de control de calidad.

```json
{
  "quality_control": {
    "format_valid": true,
    "evidence_sufficient": false,
    "source_conflicts_detected": false,
    "requires_escalation": true,
    "escalation_reason": "La fuente inicial no es primaria y el tema tiene posible impacto regulatorio."
  }
}
```

---

## 20. Reglas de escalamiento

`requires_escalation` debe ser `true` cuando:

```text
- La evidencia es insuficiente.
- Hay contradicción entre fuentes.
- El contenido puede afectar percepción de mercado.
- Se involucran hacks, fraudes, insolvencia, reguladores o acusaciones.
- La salida podría interpretarse como recomendación financiera.
- El agente no puede distinguir claramente hecho de inferencia.
- La salida será usada para publicación externa.
```

---

## 21. Salida Markdown estándar

Cuando el agente responda en Markdown, debe usar esta plantilla:

````markdown
# Resultado del Agente

## 1. Resumen Ejecutivo

[Resumen breve y accionable.]

## 2. Entrada Procesada

[Qué recibió el agente y qué alcance tuvo.]

## 3. Análisis

[Separar hechos, análisis e inferencias.]

## 4. Evidencia Utilizada

- Fuente:
- Tipo:
- Fecha:
- Relevancia:
- Limitaciones:

## 5. Nivel de Confianza

**Nivel:** alto | medio | bajo | insuficiente

**Justificación:**  
[Explicar por qué.]

## 6. Riesgos e Incertidumbre

### Riesgos

- [Riesgo identificado]

### Incertidumbre

- [Información faltante]

## 7. Salida Estructurada

```json
{
  "output_metadata": {},
  "input_summary": {},
  "result": {},
  "evidence": [],
  "risks": [],
  "uncertainties": [],
  "handoff": {},
  "knowledge_graph_candidates": {},
  "quality_control": {}
}
````

## 8. Siguiente Acción Recomendada

[Acción concreta.]

## 9. Revisión Humana

**Requiere revisión humana:** sí | no
**Motivo:** [Motivo]

````

---

## 22. Salida JSON pura estándar

Cuando XMIP solicite JSON puro, el agente debe responder únicamente con JSON válido.

No debe incluir:

```text id="vuq5g3"
- explicación previa
- comentarios
- Markdown
- bloques ```json
- texto después del JSON
````

Formato:

```json
{
  "output_metadata": {
    "agent_name": "",
    "agent_type": "",
    "runtime": "",
    "prompt_version": "",
    "task_id": "",
    "execution_id": "",
    "created_at": "",
    "language": "es",
    "human_review_required": true
  },
  "input_summary": {
    "input_type": "",
    "input_sources": [],
    "input_received": "",
    "processing_scope": ""
  },
  "result": {
    "summary": "",
    "key_findings": [],
    "analysis": "",
    "confidence_level": "",
    "decision": "",
    "recommended_next_action": ""
  },
  "evidence": [],
  "risks": [],
  "uncertainties": [],
  "handoff": {
    "next_agent": "",
    "requested_action": "",
    "handoff_required": false
  },
  "knowledge_graph_candidates": {
    "entities": [],
    "relationships": []
  },
  "quality_control": {
    "format_valid": true,
    "evidence_sufficient": false,
    "source_conflicts_detected": false,
    "requires_escalation": false,
    "escalation_reason": ""
  }
}
```

---

## 23. Manejo de errores

Si el agente no puede completar la tarea, no debe inventar una salida.

Debe responder con estructura de error.

```json
{
  "output_metadata": {
    "agent_name": "",
    "agent_type": "",
    "runtime": "",
    "prompt_version": "",
    "task_id": "",
    "execution_id": "",
    "created_at": "",
    "language": "es",
    "human_review_required": true
  },
  "error": {
    "error_type": "insufficient_information",
    "message": "No hay evidencia suficiente para completar la tarea sin inventar información.",
    "missing_information": [
      "Fuente primaria",
      "Fecha de publicación",
      "Autoridad emisora"
    ],
    "recommended_resolution": "Solicitar validación de fuente antes de continuar."
  },
  "quality_control": {
    "format_valid": true,
    "evidence_sufficient": false,
    "source_conflicts_detected": false,
    "requires_escalation": true,
    "escalation_reason": "Información insuficiente."
  }
}
```

Tipos de error permitidos:

```text
insufficient_information
invalid_input
unsupported_task
source_unavailable
source_conflict
format_error
runtime_limitation
policy_boundary
human_review_required
```

---

## 24. Reglas contra alucinación

Todo agente debe seguir estas reglas:

```text
- No inventar fuentes.
- No inventar fechas.
- No inventar nombres de personas, empresas o protocolos.
- No presentar inferencias como hechos.
- No completar huecos con suposiciones silenciosas.
- No convertir rumores en afirmaciones.
- No producir contenido publicable si la evidencia es insuficiente.
```

Cuando falte información, debe usar:

```text
confidence_level: "insuficiente"
decision: "insufficient_information"
requires_escalation: true
```

---

## 25. Separación obligatoria de contenido

Todo análisis debe separar:

```text
- Hecho verificado
- Dato no verificado
- Interpretación
- Inferencia
- Opinión editorial
- Recomendación operativa
```

Ejemplo:

```markdown
### Hechos verificados

- [Hecho con evidencia]

### Datos no verificados

- [Dato pendiente de validación]

### Interpretación

- [Lectura razonada del hecho]

### Inferencia

- [Conclusión probable, no definitiva]

### Recomendación operativa

- [Siguiente paso dentro del workflow]
```

---

## 26. Reglas para contenido de mercado

Cuando el contenido involucre mercados, precios, tokens o inversión, la salida debe evitar recomendaciones financieras personalizadas.

Lenguaje permitido:

```text
- escenario
- factor
- riesgo
- sensibilidad
- impacto potencial
- narrativa
- invalidación
- probabilidad cualitativa
```

Lenguaje prohibido:

```text
- compra
- vende
- garantizado
- precio seguro
- señal definitiva
- trade obligatorio
- rendimiento esperado garantizado
```

Uso aceptable:

```text
El evento podría aumentar la sensibilidad del mercado hacia la narrativa de regulación de stablecoins si se confirma por fuente primaria.
```

Uso no aceptable:

```text
Compra stablecoins antes de que suban por la noticia.
```

---

## 27. Campos mínimos por agente

### 27.1 NewsScoutAgent

Debe incluir:

```text
- señal detectada
- tema
- fuente inicial
- urgencia
- relevancia editorial
- evidencia mínima
- recomendación de validación
```

---

### 27.2 SourceValidatorAgent

Debe incluir:

```text
- fuente evaluada
- tipo de fuente
- autoridad de la fuente
- fecha
- consistencia
- limitaciones
- veredicto de confiabilidad
```

---

### 27.3 MarketImpactAgent

Debe incluir:

```text
- activo, sector o narrativa afectada
- impacto potencial
- factores a favor
- factores en contra
- riesgos de mala interpretación
- nivel de sensibilidad del mercado
```

---

### 27.4 EditorialAgent

Debe incluir:

```text
- ángulo editorial
- prioridad
- tratamiento recomendado
- riesgo editorial
- decisión editorial
- necesidad de revisión humana
```

---

### 27.5 ScriptAgent

Debe incluir:

```text
- objetivo del guion
- estructura narrativa
- puntos clave
- advertencias editoriales
- CTA permitido
- versión lista para revisión
```

---

### 27.6 DistributionAgent

Debe incluir:

```text
- canal recomendado
- formato
- adaptación por canal
- timing sugerido
- restricciones
- contenido listo para aprobación
```

---

### 27.7 MetricsAgent

Debe incluir:

```text
- métrica observada
- periodo
- interpretación
- anomalías
- aprendizaje operativo
- recomendación de mejora
```

---

### 27.8 MemoryAgent

Debe incluir:

```text
- información a guardar
- razón operativa
- tipo de memoria
- caducidad si aplica
- riesgos de guardar ruido
- relación con Knowledge Graph
```

---

### 27.9 AuditAgent

Debe incluir:

```text
- objeto auditado
- criterio evaluado
- hallazgos
- incumplimientos
- severidad
- corrección recomendada
```

---

### 27.10 RiskAgent

Debe incluir:

```text
- riesgo detectado
- severidad
- probabilidad cualitativa
- impacto
- mitigación
- decisión de escalamiento
```

---

## 28. Ejemplo completo de salida híbrida

````markdown
# Resultado del Agente

## 1. Resumen Ejecutivo

Se detectó una señal potencialmente relevante sobre regulación de stablecoins. La fuente inicial es secundaria, por lo que la señal no debe avanzar a producción editorial sin validación primaria.

## 2. Entrada Procesada

Se recibió una URL con una nota sobre posible anuncio regulatorio relacionado con stablecoins.

## 3. Análisis

### Hechos verificados

- Existe una publicación secundaria que menciona el tema.

### Datos no verificados

- No se ha confirmado el comunicado oficial.
- No se ha validado la autoridad emisora.

### Inferencia

- Si el anuncio se confirma, podría tener impacto narrativo en el sector de stablecoins.

## 4. Evidencia Utilizada

- Fuente: Example Source
- Tipo: URL
- Nivel: secundaria
- Limitación: no es fuente primaria

## 5. Nivel de Confianza

**Nivel:** medio

**Justificación:**  
La señal es plausible, pero requiere validación con fuente primaria.

## 6. Riesgos e Incertidumbre

### Riesgos

- Mala interpretación regulatoria.
- Publicación prematura.

### Incertidumbre

- Falta fuente primaria.
- Falta fecha oficial del anuncio.

## 7. Salida Estructurada

```json
{
  "output_metadata": {
    "agent_name": "NewsScoutAgent",
    "agent_type": "research",
    "runtime": "claude",
    "prompt_version": "1.0.0",
    "task_id": "signal-2026-07-02-001",
    "execution_id": "exec-2026-07-02-001",
    "created_at": "2026-07-02T00:00:00-07:00",
    "language": "es",
    "human_review_required": true
  },
  "input_summary": {
    "input_type": "news_signal",
    "input_sources": [
      "https://example.com/source"
    ],
    "input_received": "Se recibió una señal sobre posible regulación de stablecoins.",
    "processing_scope": "Evaluar relevancia editorial inicial."
  },
  "result": {
    "summary": "La señal puede ser relevante, pero requiere validación primaria.",
    "key_findings": [
      "Tema relacionado con stablecoins.",
      "Fuente inicial secundaria.",
      "Posible impacto narrativo si se confirma."
    ],
    "analysis": "La señal debe avanzar a validación antes de cualquier tratamiento editorial.",
    "confidence_level": "medio",
    "decision": "send_to_validation",
    "recommended_next_action": "Enviar a SourceValidatorAgent."
  },
  "evidence": [
    {
      "evidence_id": "ev-001",
      "type": "url",
      "source_name": "Example Source",
      "source_url": "https://example.com/source",
      "published_at": "",
      "accessed_at": "2026-07-02T00:00:00-07:00",
      "source_tier": "secondary",
      "relevance": "Menciona la señal inicial.",
      "limitations": "No es fuente primaria.",
      "confidence_contribution": "medio"
    }
  ],
  "risks": [
    {
      "risk_id": "risk-001",
      "risk_type": "source_quality",
      "description": "La fuente inicial no es primaria.",
      "severity": "medio",
      "mitigation": "Validar contra fuente oficial."
    }
  ],
  "uncertainties": [
    {
      "uncertainty_id": "unc-001",
      "description": "No se ha confirmado el comunicado oficial.",
      "impact": "Puede cambiar la prioridad editorial.",
      "data_needed": "Fuente primaria."
    }
  ],
  "handoff": {
    "next_agent": "SourceValidatorAgent",
    "requested_action": "Validar fuente, fecha, autoridad emisora y confiabilidad.",
    "handoff_required": true
  },
  "knowledge_graph_candidates": {
    "entities": [
      {
        "name": "stablecoins",
        "type": "Narrativa",
        "confidence_level": "medio",
        "source_evidence_id": "ev-001"
      }
    ],
    "relationships": []
  },
  "quality_control": {
    "format_valid": true,
    "evidence_sufficient": false,
    "source_conflicts_detected": false,
    "requires_escalation": true,
    "escalation_reason": "La fuente inicial no es primaria."
  }
}
````

## 8. Siguiente Acción Recomendada

Enviar a SourceValidatorAgent para validación primaria.

## 9. Revisión Humana

**Requiere revisión humana:** sí
**Motivo:** La señal puede afectar interpretación de mercado y no tiene fuente primaria validada.

````

---

## 29. Criterios de aceptación

Una salida de agente se considera válida si cumple:

```text id="46yqbz"
- Identifica agente, runtime y versión.
- Resume correctamente la entrada.
- Declara alcance de procesamiento.
- Distingue hechos, análisis e inferencias.
- Incluye evidencia o declara su ausencia.
- Usa nivel de confianza oficial.
- Identifica riesgos e incertidumbre.
- Recomienda una siguiente acción concreta.
- Declara si requiere revisión humana.
- Incluye salida estructurada apta para XMIP.
````

---

## 30. Antipatrones prohibidos

Quedan prohibidas las siguientes salidas:

```text
- Respuestas sin estructura.
- Resúmenes bonitos sin evidencia.
- Opiniones presentadas como hechos.
- JSON inválido.
- Campos críticos vacíos sin justificación.
- Confianza alta sin fuente sólida.
- Handoff a agentes inexistentes.
- Publicación directa sin revisión.
- Recomendaciones financieras personalizadas.
- Conclusiones fuertes con evidencia débil.
```

---

## 31. Estado de implementación

Este estándar aplica a todos los nuevos prompts y adaptadores creados después de su aprobación.

Los prompts existentes en:

```text
docs/007-prompts/gpt/
```

deben alinearse progresivamente.

No se requiere refactor masivo inmediato.

Prioridad de adopción:

```text
1. Claude-NewsScoutAgent
2. Claude-SourceValidatorAgent
3. Claude-EditorialAgent
4. Hermes-Agent-Execution-Contract
5. Prompts GPT existentes
```

---

## 32. Conclusión

Este estándar convierte las respuestas de los agentes en activos operativos de XMIP.

La regla central queda establecida:

```text
Texto libre sirve para leer.
Salida estructurada sirve para operar.
XMIP necesita operar.
```
