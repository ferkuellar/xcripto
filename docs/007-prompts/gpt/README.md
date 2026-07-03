
# GPT Runtime Prompts

| Campo                  | Valor                                       |
| ---------------------- | ------------------------------------------- |
| Proyecto               | Project ORION / XCripto                     |
| Sistema                | XMIP — XCripto Media Intelligence Platform |
| Dominio                | Runtime Prompts                             |
| Runtime                | GPT                                         |
| Tipo de documento      | README                                      |
| Nivel documental       | L4 — Operaciones / Runtime Execution       |
| Ruta                   | `docs/007-prompts/gpt/README.md`          |
| Estado                 | Draft Implementable                         |
| Versión               | 0.1.0                                       |
| Owner                  | ORION Architecture                          |
| Última actualización | 2026-07-02                                  |

---

## 1. Propósito

Este directorio contiene los prompts y adaptadores necesarios para ejecutar agentes XMIP usando **GPT** como motor cognitivo.

GPT no define a los agentes.

GPT adapta la ejecución de agentes ORION/XMIP a un runtime conversacional, analítico y generativo.

Regla central:

```text
El agente pertenece a ORION.
El prompt pertenece al runtime.
La ejecución pertenece a XMIP.
```

---

## 2. Qué es GPT dentro de XMIP

GPT es un motor cognitivo para:

```text
- análisis
- razonamiento
- clasificación
- redacción
- estructuración
- síntesis
- generación de outputs
- revisión de coherencia
- transformación de contenido
```

GPT puede ejecutar tareas de agentes XMIP cuando recibe:

```text
- definición oficial del agente
- contrato base
- guardrails editoriales
- input estructurado
- formato de salida esperado
- restricciones de runtime
```

GPT no debe operar como agente libre sin contrato.

---

## 3. Diferencia entre GPT, Claude y Hermes

```text
GPT / Claude = motores cognitivos
Hermes = operador de ejecución local
```

GPT puede razonar, redactar, analizar y estructurar.

Hermes puede operar archivos, validar rutas, trabajar sobre repositorio y preparar ejecución local.

Por eso:

```text
docs/007-prompts/gpt/     = prompts para ejecución cognitiva con GPT
docs/007-prompts/claude/  = prompts para ejecución cognitiva con Claude
docs/007-prompts/hermes/  = prompts para ejecución operativa local con Hermes
```

---

## 4. Relación con la definición oficial de agentes

Los archivos de este directorio no sustituyen:

```text
docs/004-agentes/
```

Cada adaptador GPT debe partir de la definición oficial del agente correspondiente.

Ejemplo:

```text
docs/004-agentes/NewsScoutAgent.md
docs/007-prompts/gpt/GPT-NewsScoutAgent.md
```

La primera ruta define el agente.

La segunda adapta su ejecución a GPT.

---

## 5. Estructura esperada del directorio

```text
docs/007-prompts/gpt/
│
├── README.md
├── 00-gpt-global-system.md
├── GPT-Agent-Execution-Contract.md
│
├── GPT-NewsScoutAgent.md
├── GPT-SourceValidatorAgent.md
├── GPT-EditorialAgent.md
├── GPT-MarketImpactAgent.md
├── GPT-ScriptAgent.md
├── GPT-RiskAgent.md
├── GPT-AuditAgent.md
├── GPT-KnowledgeAgent.md
├── GPT-DistributionAgent.md
├── GPT-SocialClipAgent.md
├── GPT-MemoryAgent.md
├── GPT-MetricsAgent.md
└── GPT-CalendarAgent.md
```

---

## 6. Documentos base esperados

### 6.1 `00-gpt-global-system.md`

Define el comportamiento global de GPT dentro de XMIP.

Debe incluir:

```text
- identidad del runtime
- límites generales
- reglas de evidencia
- reglas de no publicación
- reglas financieras
- reglas de incertidumbre
- estilo de respuesta
- formato esperado de outputs
```

---

### 6.2 `GPT-Agent-Execution-Contract.md`

Define el contrato estándar para ejecutar agentes XMIP con GPT.

Debe incluir:

```text
- input mínimo
- output esperado
- formato de respuesta
- restricciones
- guardrails
- handoff
- human_review_required
```

---

### 6.3 `README.md`

Este archivo.

Funciona como índice operativo del runtime GPT.

---

## 7. Adaptadores GPT por agente

### 7.1 `GPT-NewsScoutAgent.md`

Detecta señales noticiosas iniciales.

No valida fuentes.
No redacta guiones finales.
No publica.

---

### 7.2 `GPT-SourceValidatorAgent.md`

Evalúa evidencia, calidad de fuente, corroboración y confiabilidad.

Pregunta central:

```text
¿La evidencia aguanta?
```

No decide ángulo editorial.
No publica.
No convierte rumores en hechos.

---

### 7.3 `GPT-EditorialAgent.md`

Define tratamiento editorial, prioridad, ángulo y siguiente agente.

No valida fuentes desde cero.
No escribe guion final.
No publica.

---

### 7.4 `GPT-MarketImpactAgent.md`

Evalúa impacto potencial de mercado.

No predice precios.
No recomienda comprar o vender.
No genera señales de trading.

Regla:

```text
Impacto potencial no es predicción.
Análisis de mercado no es recomendación financiera.
```

---

### 7.5 `GPT-ScriptAgent.md`

Convierte inteligencia validada en guion.

Debe preservar:

```text
- hechos validados
- incertidumbre
- disclaimers
- restricciones narrativas
- tono editorial
```

No debe inventar claims ni publicar.

---

### 7.6 `GPT-RiskAgent.md`

Evalúa riesgo editorial, legal, reputacional, financiero, operativo y de seguridad.

Debe producir:

```text
- riesgos
- severidad
- mitigaciones
- claims bloqueados
- decisión de avance
```

No reemplaza asesoría legal.

---

### 7.7 `GPT-AuditAgent.md`

Audita cumplimiento de contrato, formato, evidencia, guardrails y handoff.

No evalúa gusto personal.

Evalúa si una salida puede procesarse de forma confiable dentro de XMIP.

---

### 7.8 `GPT-KnowledgeAgent.md`

Convierte salidas auditadas en candidatos de Knowledge Graph.

Debe separar:

```text
- hechos
- claims
- eventos
- relaciones
- inferencias
- rumores
```

No guarda rumores como hechos.

---

### 7.9 `GPT-DistributionAgent.md`

Adapta contenido aprobado a paquetes multicanal.

No publica.
No cambia hechos.
No elimina disclaimers.

---

### 7.10 `GPT-SocialClipAgent.md`

Crea propuestas de clips cortos, captions y texto en pantalla.

Debe conservar contexto crítico.

No convierte incertidumbre en clickbait.

---

### 7.11 `GPT-MemoryAgent.md`

Evalúa aprendizajes operativos.

No reemplaza KnowledgeAgent.

Regla:

```text
Knowledge Graph = qué sabe XMIP del mundo.
Memoria operativa = qué aprende XMIP para operar mejor.
```

---

### 7.12 `GPT-MetricsAgent.md`

Analiza métricas sin inventar datos ni causalidad.

Debe separar:

```text
observación
interpretación
hipótesis
conclusión
recomendación
```

---

### 7.13 `GPT-CalendarAgent.md`

Prepara planificación editorial.

No publica.
No agenda automáticamente.
No calendariza contenido bloqueado.

---

## 8. Pipeline XMIP soportado

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

GPT puede ejecutar uno o varios pasos del pipeline, siempre bajo contrato y con output estructurado.

---

## 9. Reglas globales de GPT

GPT debe:

```text
- respetar la definición oficial del agente
- respetar guardrails editoriales
- declarar incertidumbre
- separar hechos de inferencias
- evitar claims no validados
- producir output estructurado
- marcar human_review_required cuando aplique
- preparar handoff claro al siguiente agente
```

GPT no debe:

```text
- publicar contenido
- programar publicaciones
- inventar fuentes
- inventar métricas
- validar hechos externos sin evidencia
- convertir rumores en hechos
- dar recomendaciones financieras
- predecir precios
- afirmar causalidad sin soporte
- eliminar disclaimers obligatorios
```

---

## 10. Reglas financieras y de mercado

GPT debe bloquear o reformular cualquier salida que use lenguaje como:

```text
compra
vende
long
short
entrada
salida
stop loss
take profit
precio objetivo
señal confirmada
esto va a subir
esto va a caer
trade recomendado
```

Lenguaje permitido:

```text
impacto potencial
sensibilidad de mercado
factores a favor
factores en contra
incertidumbre
datos faltantes
escenario
no constituye recomendación financiera
```

---

## 11. Reglas de evidencia

GPT debe distinguir siempre:

```text
hecho
claim
rumor
opinión
hipótesis
inferencia
evento
relación
observación
conclusión
```

Regla:

```text
Lo no validado no se presenta como hecho.
Lo inferido no se presenta como certeza.
Lo dudoso no se maquilla para sonar mejor.
```

---

## 12. Formato estándar de salida

Cuando ejecute un agente, GPT debe producir como mínimo:

```yaml
agent_output:
  agent_name: ""
  runtime: "gpt"
  output_type: ""
  status: ""
  summary: ""
  findings: []
  recommendations: []
  risk_flags: []
  handoff_to: []
  human_review_required: true
```

Cada adaptador puede definir un esquema más específico.

---

## 13. Handoff estándar

Todo handoff debe declarar:

```yaml
handoff:
  from_agent: ""
  to_agent: ""
  reason: ""
  payload: {}
  required_next_action: ""
  human_review_required: true
```

Un handoff válido debe incluir razón, destino y payload suficiente.

---

## 14. Revisión humana

Por defecto:

```yaml
human_review_required: true
```

Debe ser `true` cuando exista:

```text
- publicación externa prevista
- contenido financiero o de mercado
- activos específicos
- regulación, demanda, sanción o investigación
- acusación pública
- hack, exploit o incidente de seguridad
- fuente única
- evidencia parcial
- riesgo high o critical
- persistencia de conocimiento
- persistencia de memoria
- cambio de calendario público
```

---

## 15. Uso recomendado

Para ejecutar un agente con GPT:

```text
1. Leer definición oficial en docs/004-agentes/<AgentName>.md
2. Leer reglas compartidas en docs/007-prompts/000-shared/
3. Leer 00-gpt-global-system.md
4. Leer GPT-Agent-Execution-Contract.md
5. Leer adaptador GPT correspondiente
6. Cargar input estructurado
7. Ejecutar tarea
8. Producir agent_output
9. Producir handoff
10. Marcar human_review_required
```

---

## 16. Estado de cobertura esperado

```yaml
gpt_runtime_coverage:
  status: "target_structure_defined"
  base_documents:
    - "README.md"
    - "00-gpt-global-system.md"
    - "GPT-Agent-Execution-Contract.md"
  agent_adapters:
    - "GPT-NewsScoutAgent.md"
    - "GPT-SourceValidatorAgent.md"
    - "GPT-EditorialAgent.md"
    - "GPT-MarketImpactAgent.md"
    - "GPT-ScriptAgent.md"
    - "GPT-RiskAgent.md"
    - "GPT-AuditAgent.md"
    - "GPT-KnowledgeAgent.md"
    - "GPT-DistributionAgent.md"
    - "GPT-SocialClipAgent.md"
    - "GPT-MemoryAgent.md"
    - "GPT-MetricsAgent.md"
    - "GPT-CalendarAgent.md"
```

---

## 17. Criterios de salud del runtime GPT

El runtime GPT está sano cuando:

```text
- existe README.md
- existe prompt global
- existe contrato de ejecución
- cada agente tiene adaptador GPT
- cada adaptador declara límites
- cada adaptador tiene output esperado
- cada adaptador tiene handoff
- cada adaptador marca human_review_required
- no hay publicación automática
- no hay claims sin evidencia
- no hay recomendaciones financieras
```

---

## 18. Próximo paso recomendado

Verificar físicamente el directorio:

```bash
tree /F docs\007-prompts\gpt
```

Después comparar contra la estructura esperada de este README.

Si faltan documentos, crearlos en este orden:

```text
1. 00-gpt-global-system.md
2. GPT-Agent-Execution-Contract.md
3. Adaptadores GPT faltantes por agente
```

---

## 19. Control de cambios

| Versión |      Fecha | Cambio                                        | Owner              |
| -------- | ---------: | --------------------------------------------- | ------------------ |
| 0.1.0    | 2026-07-02 | Creación inicial del README para runtime GPT | ORION Architecture |
