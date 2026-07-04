# 007-prompts — Runtime Prompt Layer de XMIP

| Campo                  | Valor                                       |
| ---------------------- | ------------------------------------------- |
| Proyecto               | Project ORION / XCripto                     |
| Sistema                | XMIP — XCripto Media Intelligence Platform |
| Dominio                | Runtime Prompts                             |
| Tipo de documento      | README de volumen                           |
| Nivel documental       | L4 — Operaciones / Runtime Execution       |
| Ruta                   | `docs/007-prompts/README.md`              |
| Estado                 | Draft Implementable                         |
| Versión               | 1.0.0                                       |
| Owner                  | ORION Architecture                          |
| Última actualización | 2026-07-02                                  |

---

## 1. Propósito del volumen

Este volumen contiene la capa de prompts runtime de XMIP: los contratos compartidos y los adaptadores que permiten ejecutar agentes ORION sobre cada runtime disponible.

Regla central del volumen:

```text
El agente pertenece a ORION.
El prompt pertenece al runtime.
La ejecución pertenece a XMIP.
```

Esto significa:

```text
docs/004-agentes/           = definición oficial de cada agente (ORION)
docs/007-prompts/000-shared = contratos y guardrails comunes a todos los runtimes
docs/007-prompts/<runtime>/ = adaptación de los agentes a un runtime concreto
backend/ (XMIP)             = ejecución, persistencia y trazabilidad
```

Ningún documento de este volumen redefine un agente. Solo lo adapta.

---

## 2. Estructura real del volumen

```text
docs/007-prompts/
├── INDEX.md
├── README.md
├── 000-shared/      contratos compartidos entre runtimes (3 docs)
├── claude/          runtime cognitivo y editorial Claude (16 docs)
├── gpt/             runtime cognitivo general GPT (16 docs)
└── hermes/          runtime operador local Hermes (18 docs)
```

---

## 3. Diferencia entre GPT, Claude y Hermes

```text
GPT    = runtime cognitivo general: clasificación, estructuración,
         validación, procesamiento del pipeline, salidas JSON.
Claude = runtime cognitivo y editorial: razonamiento editorial, redacción
         estructurada, análisis documental de contexto largo, revisión de
         consistencia, planeación de handoffs, generación de prompts y documentos.
Hermes = operador local de ejecución: repositorio, archivos, validaciones,
         estructura documental, flujos controlados. No es motor cognitivo.
```

Regla operativa:

```text
GPT / Claude = motores cognitivos
Hermes = operador de ejecución
```

---

## 4. Documentos por carpeta

### 4.1 `000-shared/` — contratos compartidos

| Documento                    | Función                                          |
| ---------------------------- | ------------------------------------------------- |
| `agent-base-contract.md`   | Contrato base de todo agente XMIP                 |
| `agent-output-standards.md` | Estándares de salida estructurada                |
| `editorial-guardrails.md`  | Guardrails editoriales, financieros y de riesgo   |

### 4.2 `gpt/` — 16 documentos

| Documento                          | Función                              |
| ---------------------------------- | ------------------------------------- |
| `README.md`                      | Uso del runtime GPT dentro de XMIP    |
| `00-gpt-global-system.md`        | Comportamiento global del runtime     |
| `GPT-Agent-Execution-Contract.md` | Contrato de ejecución de agentes     |
| `GPT-<AgentName>.md` (13)        | Adaptadores por agente                |

### 4.3 `claude/` — 16 documentos

| Documento                             | Función                              |
| ------------------------------------- | ------------------------------------- |
| `README.md`                         | Uso del runtime Claude dentro de XMIP |
| `00-claude-global-system.md`        | Comportamiento global del runtime     |
| `Claude-Agent-Execution-Contract.md` | Contrato de ejecución de agentes     |
| `Claude-<AgentName>.md` (13)        | Adaptadores por agente                |

### 4.4 `hermes/` — 18 documentos

| Documento                             | Función                                        |
| ------------------------------------- | ----------------------------------------------- |
| `README.md`                         | Uso del runtime Hermes dentro de XMIP           |
| `00-hermes-global-system.md`        | Comportamiento global del runtime               |
| `Hermes-Agent-Execution-Contract.md` | Contrato de ejecución de agentes               |
| `Hermes-<AgentName>.md` (13)        | Adaptadores por agente                          |
| `Hermes-DocsMaintenanceAgent.md`    | Agente propio de Hermes: mantenimiento de docs  |
| `Hermes-RepositoryOperator.md`      | Agente propio de Hermes: operación de repo     |

Los 13 agentes espejo en los tres runtimes son:

```text
NewsScoutAgent
SourceValidatorAgent
EditorialAgent
MarketImpactAgent
ScriptAgent
RiskAgent
AuditAgent
KnowledgeAgent
DistributionAgent
SocialClipAgent
MemoryAgent
MetricsAgent
CalendarAgent
```

---

## 5. Estado esperado por runtime

| Runtime       | Docs | Estado esperado                                              |
| ------------- | ---: | ------------------------------------------------------------ |
| `000-shared` |    3 | Completo — contratos base estables                          |
| `gpt`        |   16 | Completo — global system + contrato + 13 adaptadores        |
| `claude`     |   16 | Completo — global system + contrato + 13 adaptadores        |
| `hermes`     |   18 | Completo — incluye 2 agentes operativos propios del runtime |

Cualquier carpeta que no cumpla su conteo esperado debe tratarse como brecha y reportarse, no ignorarse.

---

## 6. Naming convention

```text
Global system:        00-<runtime>-global-system.md
Execution contract:   <Runtime>-Agent-Execution-Contract.md
Adaptador de agente:  <Runtime>-<AgentName>.md
Contratos compartidos: kebab-case descriptivo (solo en 000-shared/)
README por carpeta:   README.md
```

Ejemplos válidos:

```text
00-claude-global-system.md
GPT-Agent-Execution-Contract.md
Hermes-NewsScoutAgent.md
Claude-EditorialAgent.md
agent-base-contract.md
```

Prohibido:

```text
Prompt-<AgentName>.md        (convención legacy, retirada)
Duplicar un adaptador de un runtime en otro sin adaptación real
Nombres con espacios
```

---

## 7. Handoff entre runtimes

Todo handoff entre runtimes debe ser explícito y trazable:

```yaml
handoff:
  from_agent: ""
  to_agent: ""       # agente, GPT, Claude, Hermes o Human
  reason: ""
  payload: {}
  required_next_action: ""
  human_review_required: true
```

Ruteo estándar:

```text
Procesamiento estructurado del pipeline        → GPT
Razonamiento editorial / contexto largo /
revisión profunda / generación documental      → Claude
Operación local de repositorio o archivos      → Hermes
Aprobación, decisión editorial, juicio legal   → Human
```

Reglas:

```text
- Un handoff sin razón, payload y siguiente acción no es handoff.
- El runtime destino no debe adivinar contexto.
- Un output de agente no es fuente.
- Ningún runtime publica directamente.
```

---

## 8. Reglas críticas editoriales y financieras

Todo prompt de este volumen debe respetar:

```text
Nada se publica sin fuente.
Nada sensible se publica sin verificación.
Nada crítico se publica sin aprobación.
Nada publicado queda sin registro.
La memoria no es fuente factual.
Un agente no publica directamente.
Un output de agente no es fuente.
```

Reglas financieras obligatorias:

```text
No recomendaciones de compra o venta.
No señales de trading.
No predicción de precios.
No promesas de rendimiento.
No urgencia financiera artificial.
Análisis contextual de mercado sí; señal de inversión no.
```

Los guardrails completos viven en `000-shared/editorial-guardrails.md`.

---

## 9. Qué no debe hacer ningún runtime

```text
- inventar fuentes, citas, URLs, métricas o timestamps
- convertir rumores en hechos
- afirmar causalidad sin evidencia
- publicar o programar publicaciones
- dar recomendaciones financieras o predecir precios
- declarar culpabilidad legal sin resolución validada
- exponer secretos, credenciales o datos personales
- persistir conocimiento o memoria sin autorización
- saltarse la revisión humana cuando aplica
- ignorar bloqueos de RiskAgent o AuditAgent
- operar fuera de su rol (cognitivo vs. operador local)
```

---

## 10. Documentos relacionados

```text
docs/004-agentes/                       definición oficial de agentes
docs/002-editorial/                     constitución y estándares editoriales
docs/006-operaciones/                   pipeline y operación del newsroom
docs/007-prompts/INDEX.md               índice detallado del volumen
```

---

## 11. Control de cambios

| Versión | Fecha      | Cambio                          | Autor              |
| -------- | ---------- | -------------------------------- | ------------------ |
| 1.0.0    | 2026-07-02 | Creación inicial del README     | ORION Architecture |
