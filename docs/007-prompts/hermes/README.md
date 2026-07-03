
# Hermes Runtime Prompts

| Campo                  | Valor                                       |
| ---------------------- | ------------------------------------------- |
| Proyecto               | Project ORION / XCripto                     |
| Sistema                | XMIP — XCripto Media Intelligence Platform |
| Dominio                | Runtime Prompts                             |
| Runtime                | Hermes                                      |
| Tipo de documento      | README                                      |
| Nivel documental       | L4 — Operaciones / Runtime Execution       |
| Ruta                   | `docs/007-prompts/hermes/README.md`       |
| Estado                 | Draft Implementable                         |
| Versión               | 0.2.0                                       |
| Owner                  | ORION Architecture                          |
| Última actualización | 2026-07-02                                  |
| Cobertura              | Completa — 18/18 documentos Hermes         |

---

## 1. Propósito

Este directorio contiene los prompts, contratos y adaptadores necesarios para ejecutar agentes XMIP dentro del runtime **Hermes**.

Hermes no es un modelo cognitivo como GPT o Claude.

Hermes es el runtime operativo local encargado de ejecutar tareas sobre el repositorio, archivos, estructura documental, validaciones, contratos, handoffs y flujos controlados de XMIP.

Regla central:

```text
GPT / Claude = motores cognitivos
Hermes = operador de ejecución
```

Hermes debe operar bajo contrato, no improvisar.

---

## 2. Qué es Hermes dentro de XMIP

Hermes es el operador local de ejecución para XMIP.

Su función es:

```text
leer contexto del repositorio
aplicar contratos
ejecutar tareas controladas
crear o modificar archivos permitidos
validar estructura
respetar guardrails
preparar handoffs
reportar resultados
```

Hermes puede ayudar con:

```text
- creación de documentos Markdown
- mantenimiento de estructura documental
- ejecución de agentes bajo contrato
- validación de outputs
- revisión de rutas
- preparación de commits
- generación de handoffs
- revisión de consistencia entre agentes
- operación local sobre el repositorio
```

Hermes no debe actuar como redactor libre, bot autónomo ni publicador externo.

---

## 3. Diferencia entre agente, prompt y runtime

Regla oficial:

```text
El agente pertenece a ORION.
El prompt pertenece al runtime.
La ejecución pertenece a XMIP.
```

Esto significa:

```text
docs/004-agentes/ = definición oficial del agente
docs/007-prompts/gpt/ = adaptación para GPT
docs/007-prompts/claude/ = adaptación para Claude
docs/007-prompts/hermes/ = adaptación para Hermes
```

Los documentos en este directorio **no definen los agentes desde cero**.

Solo adaptan su ejecución al runtime Hermes.

---

## 4. Principios operativos

Hermes debe operar bajo estos principios:

```text
- leer antes de escribir
- respetar contratos
- no inventar contexto
- no publicar contenido
- no modificar arquitectura sin instrucción explícita
- no borrar archivos sin autorización
- no empujar cambios remotos
- no ejecutar acciones externas no autorizadas
- no almacenar secretos
- no convertir rumores en hechos
- no convertir análisis de mercado en recomendación financiera
- no saltarse revisión humana
```

Regla práctica:

```text
Hermes no adivina.
Hermes ejecuta con evidencia, contrato y límites.
```

---

## 5. Estructura del directorio

```text
docs/007-prompts/hermes/
│
├── README.md
├── 00-hermes-global-system.md
├── Hermes-Agent-Execution-Contract.md
│
├── Hermes-RepositoryOperator.md
├── Hermes-DocsMaintenanceAgent.md
│
├── Hermes-NewsScoutAgent.md
├── Hermes-SourceValidatorAgent.md
├── Hermes-EditorialAgent.md
├── Hermes-MarketImpactAgent.md
├── Hermes-ScriptAgent.md
├── Hermes-RiskAgent.md
├── Hermes-AuditAgent.md
├── Hermes-KnowledgeAgent.md
├── Hermes-DistributionAgent.md
├── Hermes-SocialClipAgent.md
├── Hermes-MemoryAgent.md
├── Hermes-MetricsAgent.md
└── Hermes-CalendarAgent.md
```

---

## 6. Cobertura actual

| Categoría                  | Documentos | Estado   |
| --------------------------- | ---------: | -------- |
| Base runtime                |          3 | Completo |
| Operadores Hermes           |          2 | Completo |
| Adaptadores de agentes XMIP |         13 | Completo |
| Total                       |         18 | Completo |

---

## 7. Documentos base

### 7.1 `00-hermes-global-system.md`

Define el comportamiento global de Hermes.

Incluye:

```text
- identidad del runtime
- límites operativos
- reglas de repositorio
- reglas de lectura y escritura
- restricciones de seguridad
- reglas de ejecución local
- prohibiciones generales
- comportamiento esperado ante errores
```

Debe cargarse antes de cualquier ejecución Hermes.

---

### 7.2 `Hermes-Agent-Execution-Contract.md`

Define el contrato estándar para ejecutar agentes dentro de Hermes.

Incluye:

```text
- estructura mínima de ejecución
- input esperado
- output esperado
- allowed_read_paths
- allowed_write_paths
- prohibited_actions
- success_criteria
- rollback_notes
- handoff_required
- human_review_required
```

Ningún agente debe ejecutarse sin contrato.

---

### 7.3 `README.md`

Este archivo.

Funciona como índice operativo y mapa de navegación para el runtime Hermes.

---

## 8. Operadores Hermes

### 8.1 `Hermes-RepositoryOperator.md`

Operador técnico para tareas sobre el repositorio.

Uso principal:

```text
- inspeccionar estructura
- crear archivos
- modificar archivos
- validar rutas
- preparar commits
- revisar diff
- generar handoffs técnicos
```

No debe confundirse con un agente editorial.

---

### 8.2 `Hermes-DocsMaintenanceAgent.md`

Operador de mantenimiento documental.

Uso principal:

```text
- revisar consistencia de documentación
- detectar archivos faltantes
- detectar duplicados
- revisar metadata
- revisar índices
- mantener rutas documentales
- alinear estructura documental
```

No crea estrategia editorial ni redefine arquitectura.

---

## 9. Adaptadores Hermes por agente

### 9.1 `Hermes-NewsScoutAgent.md`

Detecta señales noticiosas iniciales.

Función:

```text
identificar señales relevantes, ruido, duplicados y posibles historias
```

No valida fuentes.
No escribe guiones.
No publica.

---

### 9.2 `Hermes-SourceValidatorAgent.md`

Valida evidencia, fuentes y calidad informativa.

Función:

```text
determinar si la evidencia aguanta
```

No decide tratamiento editorial.
No publica.
No transforma rumores en hechos.

---

### 9.3 `Hermes-EditorialAgent.md`

Decide tratamiento editorial.

Función:

```text
determinar si una señal debe avanzar, bajo qué ángulo y hacia qué agente
```

No valida fuentes desde cero.
No escribe guion final.
No publica.

---

### 9.4 `Hermes-MarketImpactAgent.md`

Evalúa impacto potencial de mercado sin predicción.

Función:

```text
explicar qué podría cambiar en percepción, narrativa, riesgo, liquidez o sensibilidad de mercado
```

No predice precios.
No genera señales de trading.
No recomienda compra o venta.

---

### 9.5 `Hermes-ScriptAgent.md`

Convierte inteligencia validada en guion responsable.

Función:

```text
redactar guiones bajo restricciones editoriales, evidencia y guardrails
```

No valida fuentes desde cero.
No publica.
No elimina incertidumbre para mejorar ritmo narrativo.

---

### 9.6 `Hermes-RiskAgent.md`

Evalúa riesgo editorial, legal, reputacional, financiero, operativo y de seguridad.

Función:

```text
detectar riesgo, clasificar severidad, definir mitigación y decidir avance
```

No censura por reflejo.
No reemplaza asesoría legal.
No aprueba publicación final.

---

### 9.7 `Hermes-AuditAgent.md`

Audita cumplimiento de contrato, formato, evidencia, guardrails y handoff.

Función:

```text
validar si XMIP puede confiar, procesar y auditar una salida
```

No evalúa gusto personal.
No publica.
No perdona contratos rotos.

---

### 9.8 `Hermes-KnowledgeAgent.md`

Convierte salidas auditadas en candidatos para Knowledge Graph.

Función:

```text
extraer entidades, relaciones, eventos, claims, inferencias y provenance
```

No guarda rumores como hechos.
No reemplaza MemoryAgent.
No persiste en producción sin autorización.

---

### 9.9 `Hermes-DistributionAgent.md`

Adapta contenido aprobado a paquetes multicanal.

Función:

```text
preparar distribución por canal sin alterar hechos, disclaimers ni restricciones
```

No publica.
No agenda.
No convierte incertidumbre en clickbait.

---

### 9.10 `Hermes-SocialClipAgent.md`

Crea propuestas de clips y piezas sociales cortas.

Función:

```text
condensar contenido aprobado sin destruir contexto
```

No publica.
No elimina disclaimers.
No usa pánico como hook.

---

### 9.11 `Hermes-MemoryAgent.md`

Evalúa aprendizajes operativos para memoria.

Función:

```text
decidir qué aprendizaje guardar, monitorear, actualizar, caducar o rechazar
```

No guarda todo.
No reemplaza KnowledgeAgent.
No guarda datos sensibles sin revisión.

---

### 9.12 `Hermes-MetricsAgent.md`

Analiza métricas de contenido, audiencia, distribución y operación.

Función:

```text
separar observación, interpretación, hipótesis, conclusión y recomendación
```

No inventa métricas.
No atribuye causalidad sin evidencia.
No manipula datos para justificar decisiones.

---

### 9.13 `Hermes-CalendarAgent.md`

Prepara planificación editorial y calendario operativo.

Función:

```text
ordenar contenido aprobado, dependencias, ventanas, cadencia y prioridades
```

No publica.
No crea eventos externos sin autorización.
No calendariza contenido bloqueado.

---

## 10. Pipeline operativo completo

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

Este pipeline no implica que todos los agentes deban ejecutarse siempre.

La ejecución depende de:

```text
- tipo de contenido
- nivel de riesgo
- evidencia disponible
- formato solicitado
- canal objetivo
- necesidad de memoria
- disponibilidad de métricas
- estado de aprobación
```

---

## 11. Rutas estándar de lectura

Los adaptadores Hermes pueden leer, según contrato específico:

```text
docs/
data/
inputs/
outputs/news-scout/
outputs/source-validator/
outputs/editorial/
outputs/market-impact/
outputs/script/
outputs/risk/
outputs/audit/
outputs/knowledge/
outputs/distribution/
outputs/social-clips/
outputs/memory/
outputs/metrics/
outputs/calendar/
workflows/
```

Cada agente debe limitarse a las rutas declaradas en su contrato.

---

## 12. Rutas estándar de escritura

Cada agente debe escribir únicamente en su carpeta de salida correspondiente:

```text
outputs/news-scout/
outputs/source-validator/
outputs/editorial/
outputs/market-impact/
outputs/script/
outputs/risk/
outputs/audit/
outputs/knowledge/
outputs/distribution/
outputs/social-clips/
outputs/memory/
outputs/metrics/
outputs/calendar/
```

Los documentos de prompts pueden escribirse o modificarse en:

```text
docs/007-prompts/hermes/
```

solo cuando la tarea explícitamente sea crear o mantener adaptadores Hermes.

---

## 13. Convención de nombres

### 13.1 Documentos Hermes

```text
Hermes-<AgentName>.md
```

Ejemplos:

```text
Hermes-NewsScoutAgent.md
Hermes-SourceValidatorAgent.md
Hermes-EditorialAgent.md
Hermes-MarketImpactAgent.md
```

### 13.2 Outputs por agente

Convención recomendada:

```text
outputs/<agent-domain>/<execution_id>.json
```

Ejemplos:

```text
outputs/news-scout/hns-20260702-001.json
outputs/source-validator/hsv-20260702-001.json
outputs/editorial/hed-20260702-001.json
outputs/market-impact/hmi-20260702-001.json
```

---

## 14. Estados estándar

Los adaptadores Hermes pueden usar estados como:

```text
draft_ready
draft_ready_with_warnings
blocked
requires_validation
requires_audit
requires_risk_review
requires_human_review
insufficient_inputs
insufficient_data
```

Cada adaptador puede definir estados adicionales específicos.

Regla:

```text
El status debe explicar si la salida puede avanzar, requiere revisión o está bloqueada.
```

---

## 15. Salida estándar Hermes

Toda ejecución Hermes debe producir, como mínimo:

```yaml
execution_summary: ""
files_read: []
files_created: []
files_modified: []
validations_run: []
errors_detected: []
agent_output: {}
handoff: {}
human_review_required: true
```

Cuando el agente produzca JSON, debe respetar el esquema específico del adaptador.

---

## 16. Handoff estándar

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

Regla:

```text
Un handoff sin razón y payload suficiente no es handoff.
Es abandono.
```

---

## 17. Revisión humana

Por defecto:

```yaml
human_review_required: true
```

Puede ser `false` solo en tareas internas, de bajo riesgo, sin publicación externa, sin datos sensibles y sin impacto financiero, legal, reputacional o de seguridad.

Debe ser `true` cuando exista:

```text
- publicación externa prevista
- contenido financiero o de mercado
- activos específicos
- regulación, demanda, sanción o investigación
- acusación pública
- hack, exploit o incidente de seguridad
- claims no completamente validados
- fuente única
- evidencia parcial
- riesgo high o critical
- contenido sensible
- cambio de calendario público
- persistencia de conocimiento o memoria
```

---

## 18. Reglas financieras y de mercado

Hermes debe bloquear o devolver a RiskAgent cualquier salida que contenga:

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
contenido informativo
impacto potencial
sensibilidad de mercado
incertidumbre
factores a favor
factores en contra
datos faltantes
no constituye recomendación financiera
```

Regla:

```text
XMIP puede explicar mercado.
XMIP no debe dar señales de trading.
```

---

## 19. Reglas de evidencia

Hermes debe preservar diferencia entre:

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
Lo no validado no se promueve a hecho.
Lo inferido no se guarda como certeza.
Lo dudoso no se maquilla para sonar mejor.
```

---

## 20. Reglas de publicación

Hermes no debe:

```text
- publicar contenido
- programar publicaciones
- crear eventos externos
- enviar emails
- subir videos
- llamar APIs de redes sociales
- hacer push remoto
```

salvo autorización explícita, contrato separado y herramienta permitida.

En este directorio, todos los adaptadores generan salidas **preparatorias**, no acciones externas finales.

---

## 21. Orden recomendado para ejecutar Hermes

Para cualquier tarea con agente:

```text
1. Leer `00-hermes-global-system.md`
2. Leer `Hermes-Agent-Execution-Contract.md`
3. Leer definición oficial en `docs/004-agentes/<AgentName>.md`
4. Leer adaptador Hermes correspondiente
5. Leer reglas compartidas en `docs/007-prompts/000-shared/`
6. Cargar input del workflow
7. Validar allowed_read_paths y allowed_write_paths
8. Ejecutar tarea
9. Generar output estructurado
10. Generar handoff
11. Marcar human_review_required
```

---

## 22. Cuándo usar cada archivo

| Necesidad                                  | Archivo                                |
| ------------------------------------------ | -------------------------------------- |
| Configurar comportamiento global de Hermes | `00-hermes-global-system.md`         |
| Ejecutar cualquier agente bajo contrato    | `Hermes-Agent-Execution-Contract.md` |
| Operar archivos del repo                   | `Hermes-RepositoryOperator.md`       |
| Mantener documentación                    | `Hermes-DocsMaintenanceAgent.md`     |
| Detectar señales noticiosas               | `Hermes-NewsScoutAgent.md`           |
| Validar fuentes                            | `Hermes-SourceValidatorAgent.md`     |
| Decidir tratamiento editorial              | `Hermes-EditorialAgent.md`           |
| Evaluar impacto de mercado                 | `Hermes-MarketImpactAgent.md`        |
| Escribir guion                             | `Hermes-ScriptAgent.md`              |
| Revisar riesgos                            | `Hermes-RiskAgent.md`                |
| Auditar cumplimiento                       | `Hermes-AuditAgent.md`               |
| Estructurar conocimiento                   | `Hermes-KnowledgeAgent.md`           |
| Preparar distribución                     | `Hermes-DistributionAgent.md`        |
| Crear clips cortos                         | `Hermes-SocialClipAgent.md`          |
| Evaluar memoria operativa                  | `Hermes-MemoryAgent.md`              |
| Analizar métricas                         | `Hermes-MetricsAgent.md`             |
| Preparar calendario editorial              | `Hermes-CalendarAgent.md`            |

---

## 23. Criterios de salud del runtime Hermes

Hermes está sano cuando:

```text
- todos los agentes tienen adaptador
- todos los adaptadores declaran límites
- todos los adaptadores tienen contrato
- todos los outputs tienen schema
- todos los handoffs son explícitos
- human_review_required está presente
- no hay rutas ambiguas
- no hay acciones externas implícitas
- no hay publicación automática
- no hay claims sin evidencia
```

---

## 24. Estado de cobertura

```yaml
hermes_runtime_coverage:
  status: "complete"
  total_documents: 18
  base_documents: 3
  operators: 2
  agent_adapters: 13
  completed:
    - "README.md"
    - "00-hermes-global-system.md"
    - "Hermes-Agent-Execution-Contract.md"
    - "Hermes-RepositoryOperator.md"
    - "Hermes-DocsMaintenanceAgent.md"
    - "Hermes-NewsScoutAgent.md"
    - "Hermes-SourceValidatorAgent.md"
    - "Hermes-EditorialAgent.md"
    - "Hermes-MarketImpactAgent.md"
    - "Hermes-ScriptAgent.md"
    - "Hermes-RiskAgent.md"
    - "Hermes-AuditAgent.md"
    - "Hermes-KnowledgeAgent.md"
    - "Hermes-DistributionAgent.md"
    - "Hermes-SocialClipAgent.md"
    - "Hermes-MemoryAgent.md"
    - "Hermes-MetricsAgent.md"
    - "Hermes-CalendarAgent.md"
```

---

## 25. Próximo paso recomendado

Con la cobertura Hermes completa, el siguiente paso operativo es probar una ejecución end-to-end controlada:

```text
NewsScoutAgent
→ SourceValidatorAgent
→ EditorialAgent
→ MarketImpactAgent
→ ScriptAgent
→ RiskAgent
→ AuditAgent
→ KnowledgeAgent
→ DistributionAgent
→ SocialClipAgent
→ MemoryAgent
→ MetricsAgent
→ CalendarAgent
```

Prueba recomendada:

```text
Caso: noticia cripto sensible
Tema: exchange suspende retiros / regulación / exploit / ETF / stablecoin
Objetivo: validar contratos, handoffs, bloqueos, revisión humana y outputs JSON
```

---

## 26. Control de cambios

| Versión |      Fecha | Cambio                                                                                         | Owner              |
| -------- | ---------: | ---------------------------------------------------------------------------------------------- | ------------------ |
| 0.1.0    | 2026-07-02 | Creación inicial del README Hermes                                                            | ORION Architecture |
| 0.2.0    | 2026-07-02 | Actualización con cobertura completa: 3 documentos base, 2 operadores y 13 adaptadores Hermes | ORION Architecture |
