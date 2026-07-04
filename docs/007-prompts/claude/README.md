
# Claude Runtime Prompts — XMIP

**Proyecto:** Project ORION / XCripto
**Sistema:** XMIP — XCripto Media Intelligence Platform
**Nivel documental:** L5 — Ejecución
**Dominio:** Prompts / Claude / Agentes / Newsroom
**Estado:** Aprobado para implementación inicial
**Versión:** 1.0.0
**Owner:** XCripto Architecture Office
**Última actualización:** 2026-07-02

---

## 1. Propósito

Esta carpeta contiene los adaptadores de ejecución para operar agentes XMIP sobre el runtime Claude.

Los documentos aquí definidos no crean agentes nuevos.

Los documentos aquí definidos adaptan agentes existentes al comportamiento esperado de Claude, respetando la arquitectura, contratos, límites editoriales y estándares operativos definidos por Project ORION.

Regla central:

```text
Claude no define al agente.
Claude ejecuta al agente bajo contrato.
```

---

## 2. Ubicación

```text
docs/007-prompts/claude/
```

---

## 3. Relación con la arquitectura XMIP

La definición oficial de cada agente vive en:

```text
docs/004-agentes/
```

Las reglas comunes para todos los runtimes viven en:

```text
docs/007-prompts/000-shared/
```

Los adaptadores Claude viven en:

```text
docs/007-prompts/claude/
```

Por lo tanto:

```text
docs/004-agentes/ = definición organizacional del agente
docs/007-prompts/000-shared/ = reglas comunes de ejecución
docs/007-prompts/claude/ = adaptación del agente a Claude
```

---

## 4. Documentos base requeridos

Todo adaptador Claude debe respetar estos documentos:

```text
docs/007-prompts/000-shared/agent-base-contract.md
docs/007-prompts/000-shared/agent-output-standards.md
docs/007-prompts/000-shared/editorial-guardrails.md
docs/007-prompts/claude/00-claude-global-system.md
docs/007-prompts/claude/Claude-Agent-Execution-Contract.md
docs/004-agentes/
```

Cuando aplique, también debe respetar:

```text
docs/003-arquitectura/
docs/006-operaciones/
docs/002-editorial/
```

---

## 5. Rol de Claude dentro de XMIP

Claude funciona como motor cognitivo para tareas de análisis amplio, redacción estructurada, revisión profunda, síntesis contextual y razonamiento editorial.

Claude es especialmente útil para:

```text
- analizar contexto largo
- revisar documentos extensos
- estructurar razonamiento editorial
- redactar guiones
- evaluar riesgos
- auditar salidas
- extraer conocimiento estructurado
- mantener consistencia documental
```

Claude no debe operar como runtime libre.

Claude debe operar bajo contrato de agente.

---

## 6. Diferencia entre Claude, GPT y Hermes

```text
GPT = motor cognitivo conversacional y analítico
Claude = motor cognitivo de contexto largo y revisión profunda
Hermes = operador local / CLI / runtime de ejecución en repositorio
```

Regla operativa:

```text
GPT / Claude = motores cognitivos
Hermes = operador de ejecución
```

---

## 7. Adaptadores Claude incluidos

La carpeta Claude contiene los siguientes adaptadores:

```text
Claude-NewsScoutAgent.md
Claude-SourceValidatorAgent.md
Claude-EditorialAgent.md
Claude-MarketImpactAgent.md
Claude-ScriptAgent.md
Claude-RiskAgent.md
Claude-AuditAgent.md
Claude-KnowledgeAgent.md
Claude-DistributionAgent.md
Claude-SocialClipAgent.md
Claude-MemoryAgent.md
Claude-MetricsAgent.md
Claude-CalendarAgent.md
```

---

## 8. Pipeline operativo Claude

El pipeline Claude documentado es:

```text
NewsScoutAgent
↓
SourceValidatorAgent
↓
EditorialAgent
↓
MarketImpactAgent
↓
ScriptAgent
↓
RiskAgent
↓
AuditAgent
↓
KnowledgeAgent
↓
DistributionAgent
↓
SocialClipAgent
↓
MemoryAgent
↓
MetricsAgent
↓
CalendarAgent
```

Este orden representa un flujo operativo recomendado.

No todos los agentes son obligatorios en todos los casos, pero cualquier salto de flujo debe estar justificado y ser auditable.

---

## 9. Descripción resumida de agentes

### NewsScoutAgent

Detecta señales relevantes del ecosistema cripto, blockchain, mercados e IA.

No valida definitivamente.

No publica.

---

### SourceValidatorAgent

Evalúa fuentes, evidencia, autoridad, vigencia y suficiencia editorial.

Su función es decidir si la evidencia aguanta.

---

### EditorialAgent

Evalúa prioridad, ángulo, tratamiento editorial, formato, riesgos y siguiente acción.

No sustituye aprobación humana.

---

### MarketImpactAgent

Analiza impacto potencial sobre mercado, narrativas, activos, sectores y percepción.

No predice precios.

No genera señales de trading.

---

### ScriptAgent

Convierte briefs y decisiones editoriales en guiones claros, sobrios y listos para revisión humana.

No valida fuentes.

No publica.

---

### RiskAgent

Evalúa riesgos editoriales, reputacionales, legales, financieros, operativos y de automatización.

Define mitigaciones y controles.

---

### AuditAgent

Audita cumplimiento de contrato, formato, evidencia, JSON, handoff, workflow y guardrails.

Determina si una salida puede operar dentro de XMIP.

---

### KnowledgeAgent

Convierte salidas editoriales en entidades, relaciones, narrativas, hechos estructurados e inferencias candidatas para Knowledge Graph.

No guarda rumores como hechos.

---

### DistributionAgent

Adapta contenido aprobado a paquetes multicanal.

No publica.

No cambia hechos.

No elimina advertencias.

---

### SocialClipAgent

Convierte contenido aprobado o validado en clips sociales cortos.

Condensa sin deformar.

No convierte incertidumbre en clickbait.

---

### MemoryAgent

Decide qué aprendizajes operativos deben guardarse, monitorearse, caducar o rechazarse.

No guarda ruido.

No reemplaza KnowledgeAgent.

---

### MetricsAgent

Analiza métricas, rendimiento editorial y resultados por canal.

Separa observación, interpretación, hipótesis, conclusión y recomendación.

No inventa métricas.

---

### CalendarAgent

Organiza, prioriza y programa piezas editoriales dentro del calendario operativo.

No publica.

No programa contenido bloqueado.

---

## 10. Reglas generales para adaptadores Claude

Todo adaptador Claude debe incluir:

```text
- metadata documental
- propósito
- identidad del agente
- rol operativo para Claude
- responsabilidades
- entradas permitidas
- salidas esperadas
- acciones prohibidas
- reglas de escalamiento
- valores controlados
- formato de salida Markdown + JSON
- esquema JSON base
- prompt operativo
- ejemplos de comportamiento
- criterios de aceptación
- antipatrones prohibidos
- regla final
```

---

## 11. Formato de salida esperado

Por defecto, todo agente Claude debe producir salida híbrida:

```text
Markdown para revisión humana
+
JSON estructurado para XMIP
```

El JSON debe permitir:

```text
- persistencia
- auditoría
- handoff
- ejecución de workflows
- evaluación de calidad
- integración con Knowledge Graph
- integración con memoria
- análisis posterior
```

---

## 12. Reglas editoriales obligatorias

Claude debe respetar siempre:

```text
- No inventar fuentes.
- No inventar hechos.
- No ocultar incertidumbre.
- No convertir rumores en afirmaciones.
- No emitir recomendaciones financieras personalizadas.
- No prometer rendimientos.
- No publicar contenido directamente.
- No saltarse revisión humana cuando aplique.
- No operar fuera de la misión del agente.
```

---

## 13. Reglas financieras

Claude no debe producir:

```text
- señales de compra o venta
- instrucciones de entrada o salida
- predicciones como certeza
- promesas de rendimiento
- urgencia financiera artificial
- lenguaje de FOMO
```

Lenguaje permitido:

```text
- escenario
- contexto
- narrativa
- riesgo
- sensibilidad
- factores a favor
- factores en contra
- condiciones de confirmación
- condiciones de invalidación
```

---

## 14. Reglas de evidencia

Toda salida debe declarar:

```text
- qué se recibió
- qué se procesó
- qué evidencia se usó
- qué nivel de confianza corresponde
- qué incertidumbre existe
- qué riesgos se detectaron
- qué siguiente acción se recomienda
```

Si la evidencia es insuficiente, Claude debe decirlo.

No debe completar huecos con suposiciones.

---

## 15. Reglas de handoff

Todo handoff debe incluir:

```text
from_agent
to_agent
task_id
context_summary
input_payload
evidence
confidence_level
known_risks
requested_action
required_output
human_review_required
```

El handoff debe ser claro, accionable y auditable.

---

## 16. Política de revisión humana

La revisión humana es obligatoria cuando:

```text
- el contenido puede publicarse externamente
- hay riesgo alto o crítico
- hay hacks, exploits, fraude, insolvencia o regulación
- se mencionan personas o empresas en contexto negativo
- hay posible interpretación financiera
- hay evidencia insuficiente
- hay conflicto de fuentes
- se requiere decisión editorial sensible
```

---

## 17. Política de Knowledge Graph y memoria

Claude puede proponer candidatos para Knowledge Graph y memoria, pero debe distinguir:

```text
Knowledge Graph = qué sabemos sobre el mundo
Memoria operativa = qué aprendió XMIP para operar mejor
```

Claude no debe guardar rumores como hechos.

Claude no debe convertir inferencias en relaciones confirmadas.

Claude no debe proponer memoria permanente sin utilidad, evidencia, alcance y caducidad.

---

## 18. Mantenimiento

Cuando se modifique un adaptador Claude, debe actualizarse:

```text
- versión
- fecha de última actualización
- sección afectada
- relación con documentos shared
- criterios de aceptación si cambian las salidas
```

Cambios mayores deben generar ADR si afectan arquitectura, flujo de agentes o contrato de salida.

---

## 19. Estado actual

La cobertura Claude está completa: gobierno del runtime más los 13 agentes espejo.

Resumen:

```text
Documentos de gobierno:     2  (00-claude-global-system.md, Claude-Agent-Execution-Contract.md)
Claude agents creados:     13
Claude agents faltantes:    0
Total carpeta claude/:     16  (incluye este README)
```

---

## 20. Siguiente fase

La carpeta Hermes ya está documentada y completa en:

```text
docs/007-prompts/hermes/
```

Hermes debe tratarse como:

```text
runtime local / CLI / operador de ejecución
```

La siguiente fase del volumen 007 es de mantenimiento: versionar en git las carpetas `000-shared/`, `claude/` y `hermes/` (hoy excluidas por `.gitignore`; requiere coordinación) y ejecutar una revisión cruzada de consistencia semántica entre los tres runtimes.

No como otro motor cognitivo.

---

## 21. Regla final

```text
Claude piensa, estructura y revisa.
XMIP decide, orquesta y audita.
ORION define el sistema.
```
