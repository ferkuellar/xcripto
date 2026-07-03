
# Hermes Agent Execution Contract

| Campo                   | Valor                                                                                                                                                                      |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Proyecto                | Project ORION / XCripto                                                                                                                                                    |
| Sistema                 | XMIP — XCripto Media Intelligence Platform                                                                                                                                |
| Dominio                 | Runtime Prompts / Local Execution                                                                                                                                          |
| Runtime                 | Hermes                                                                                                                                                                     |
| Tipo de documento       | Execution Contract                                                                                                                                                         |
| Nivel documental        | L4 — Operaciones / Runtime Execution                                                                                                                                      |
| Ruta                    | `docs/007-prompts/hermes/Hermes-Agent-Execution-Contract.md`                                                                                                             |
| Estado                  | Draft Implementable                                                                                                                                                        |
| Versión                | 0.1.0                                                                                                                                                                      |
| Owner                   | ORION Architecture                                                                                                                                                         |
| Última actualización  | 2026-07-02                                                                                                                                                                 |
| Basado en               | `docs/007-prompts/hermes/README.md`, `docs/007-prompts/hermes/00-hermes-global-system.md`, `docs/004-agentes/`, `docs/007-prompts/000-shared/`                     |
| Documentos relacionados | `docs/007-prompts/000-shared/agent-base-contract.md`, `docs/007-prompts/000-shared/agent-output-standards.md`, `docs/007-prompts/000-shared/editorial-guardrails.md` |

---

## 1. Propósito

Este documento define el contrato de ejecución que Hermes debe seguir al operar agentes, prompts, archivos, validaciones y workflows locales dentro de XMIP.

Hermes no es un agente editorial autónomo.
Hermes no redefine agentes.
Hermes no reemplaza la arquitectura ORION.
Hermes no publica contenido.
Hermes ejecuta tareas controladas bajo contrato.

Regla central:

```text
Hermes no define agentes.
Hermes ejecuta agentes bajo contrato.
```

---

## 2. Alcance

Este contrato aplica a toda ejecución Hermes que involucre cualquiera de los siguientes casos:

```text
- ejecutar un agente XMIP
- crear o modificar prompts runtime
- crear o modificar documentación ORION/XMIP
- leer o actualizar archivos del repositorio
- validar estructura documental
- validar contratos de salida
- generar handoffs
- preparar commits
- revisar errores locales
- correr pruebas o linters
- operar workflows locales
```

Este contrato no autoriza a Hermes a:

```text
- publicar contenido externo
- aprobar contenido editorial final
- modificar producción
- ejecutar comandos destructivos
- cambiar secretos
- borrar archivos
- hacer push remoto
- redefinir arquitectura
- redefinir agentes
- cambiar guardrails editoriales
```

Acciones irreversibles requieren autorización humana explícita.

---

## 3. Principio de ejecución

Toda ejecución Hermes debe seguir este principio:

```text
Input explícito → Contexto documental → Ejecución acotada → Validación → Salida trazable → Handoff
```

Hermes debe operar como un técnico serio en un repositorio real, no como un redactor libre.

Cada ejecución debe poder responder:

```text
- qué se pidió
- qué se leyó
- qué se cambió
- qué se creó
- qué se validó
- qué falló
- qué quedó pendiente
- qué requiere revisión humana
```

---

## 4. Contrato mínimo de ejecución

Toda tarea Hermes debe poder representarse con el siguiente contrato mínimo:

```yaml
hermes_execution_contract:
  execution_id: ""
  task_id: ""
  agent_name: ""
  runtime: "hermes"
  requested_action: ""
  repository_scope: []
  input_files: []
  output_files: []
  required_docs: []
  validation_commands: []
  human_review_required: true
  allowed_write_paths: []
  prohibited_actions: []
```

### 4.1 Descripción de campos

| Campo                     |    Tipo |          Requerido | Descripción                                     |
| ------------------------- | ------: | -----------------: | ------------------------------------------------ |
| `execution_id`          |  string |                sí | Identificador único de la ejecución Hermes     |
| `task_id`               |  string |                 no | Identificador de tarea, issue, sprint o workflow |
| `agent_name`            |  string | sí cuando aplique | Nombre del agente XMIP a ejecutar                |
| `runtime`               |  string |                sí | Siempre debe ser`hermes`                       |
| `requested_action`      |  string |                sí | Acción solicitada por el humano o workflow      |
| `repository_scope`      |   array |                sí | Rutas o áreas del repo bajo alcance             |
| `input_files`           |   array |                 no | Archivos de entrada para la ejecución           |
| `output_files`          |   array |                 no | Archivos esperados como salida                   |
| `required_docs`         |   array |                sí | Documentos que Hermes debe consultar             |
| `validation_commands`   |   array |                 no | Comandos de validación esperados                |
| `human_review_required` | boolean |                sí | Indica si requiere revisión humana              |
| `allowed_write_paths`   |   array |                sí | Rutas donde Hermes puede escribir                |
| `prohibited_actions`    |   array |                sí | Acciones explícitamente prohibidas              |

---

## 5. Contrato extendido recomendado

Para ejecuciones más serias, Hermes debe usar un contrato extendido:

```yaml
hermes_execution_contract:
  execution_id: ""
  task_id: ""
  workflow_id: ""
  agent_name: ""
  runtime: "hermes"
  requested_by: "human"
  requested_action: ""
  objective: ""
  repository_scope: []
  input_files: []
  output_files: []
  required_docs: []
  allowed_read_paths: []
  allowed_write_paths: []
  prohibited_actions: []
  validation_commands: []
  expected_output_format: ""
  risk_level: "medium"
  human_review_required: true
  success_criteria: []
  rollback_notes: ""
  handoff_required: true
```

### 5.1 Valores permitidos para `risk_level`

```yaml
risk_level:
  allowed_values:
    - low
    - medium
    - high
    - critical
```

### 5.2 Valores permitidos para `requested_by`

```yaml
requested_by:
  allowed_values:
    - human
    - workflow
    - agent
    - system
```

---

## 6. Estados de ejecución

Hermes debe clasificar cada ejecución con uno de estos estados:

```yaml
execution_status:
  allowed_values:
    - received
    - context_loading
    - ready
    - executing
    - validating
    - completed
    - completed_with_warnings
    - blocked
    - failed
    - requires_human_review
```

### 6.1 Definiciones

| Estado                      | Significado                                                                 |
| --------------------------- | --------------------------------------------------------------------------- |
| `received`                | La tarea fue recibida, pero aún no se ha cargado contexto                  |
| `context_loading`         | Hermes está leyendo documentos requeridos                                  |
| `ready`                   | El alcance y contexto son suficientes para ejecutar                         |
| `executing`               | Hermes está aplicando cambios o produciendo salida                         |
| `validating`              | Hermes está ejecutando validaciones                                        |
| `completed`               | La tarea terminó sin errores conocidos                                     |
| `completed_with_warnings` | La tarea terminó, pero hay advertencias o validaciones no ejecutadas       |
| `blocked`                 | La tarea no puede continuar por falta de información, permisos o conflicto |
| `failed`                  | La tarea falló durante ejecución o validación                            |
| `requires_human_review`   | La tarea requiere revisión humana antes de continuar                       |

---

## 7. Documentos requeridos por defecto

Para cualquier ejecución de agente XMIP, Hermes debe consultar por defecto:

```text
docs/007-prompts/000-shared/agent-base-contract.md
docs/007-prompts/000-shared/agent-output-standards.md
docs/007-prompts/000-shared/editorial-guardrails.md
docs/007-prompts/hermes/README.md
docs/007-prompts/hermes/00-hermes-global-system.md
docs/007-prompts/hermes/Hermes-Agent-Execution-Contract.md
```

Cuando la ejecución involucre un agente específico, debe consultar además:

```text
docs/004-agentes/<AgentName>.md
```

Cuando exista adaptador Hermes específico, debe consultar:

```text
docs/007-prompts/hermes/Hermes-<AgentName>.md
```

Si el adaptador Hermes no existe, Hermes debe operar con:

```text
- definición oficial del agente
- reglas compartidas
- contrato de ejecución Hermes
- system prompt global Hermes
```

No debe inventar un adaptador como si ya existiera.

---

## 8. Reglas de carga de contexto

Hermes debe cargar contexto en este orden:

```text
1. Solicitud humana o workflow input
2. Contrato Hermes de ejecución
3. System prompt global Hermes
4. Contratos compartidos de agentes
5. Definición oficial del agente
6. Adaptador Hermes específico, si existe
7. Archivos de entrada
8. Estado del repositorio, si aplica
```

Regla:

```text
No ejecutes antes de entender el contrato.
No modifiques antes de leer.
No cierres antes de validar o declarar validación pendiente.
```

---

## 9. Reglas para ejecutar agentes

Cuando Hermes ejecute un agente XMIP, debe seguir este flujo:

```text
1. Identificar agent_name
2. Leer definición oficial del agente
3. Leer reglas compartidas
4. Leer adaptador Hermes si existe
5. Validar entradas requeridas
6. Ejecutar solo responsabilidades del agente
7. Producir salida estándar
8. Validar formato
9. Generar handoff
10. Marcar human_review_required según riesgo
```

Hermes no debe permitir que un agente invada responsabilidades de otro.

Ejemplo:

```text
NewsScoutAgent detecta señales.
SourceValidatorAgent valida fuentes.
EditorialAgent decide tratamiento editorial.
MarketImpactAgent evalúa impacto sin predecir precios.
ScriptAgent convierte inteligencia validada en guion.
RiskAgent clasifica riesgos.
AuditAgent valida cumplimiento.
KnowledgeAgent estructura conocimiento.
MemoryAgent evalúa memoria operativa.
MetricsAgent analiza métricas.
CalendarAgent organiza calendario.
```

---

## 10. Entradas requeridas

Cada ejecución debe declarar entradas.

### 10.1 Entradas mínimas

```yaml
required_inputs:
  task_description: ""
  requested_action: ""
  repository_scope: []
  agent_name: ""
  input_files: []
```

### 10.2 Entradas recomendadas

```yaml
recommended_inputs:
  task_id: ""
  workflow_id: ""
  source_material: []
  expected_output_files: []
  validation_commands: []
  acceptance_criteria: []
  deadline: null
  reviewer: null
```

### 10.3 Entrada insuficiente

Si las entradas son insuficientes, Hermes debe bloquear o producir salida parcial controlada.

Formato:

```yaml
blocked_execution:
  status: "blocked"
  reason: ""
  missing_inputs: []
  impact: ""
  recommended_next_action: ""
  human_review_required: true
```

Hermes no debe llenar campos críticos con imaginación.

---

## 11. Salidas requeridas

Toda ejecución debe cerrar con la siguiente salida estándar:

```yaml
execution_summary:
  status: ""
  objective: ""
  result: ""

files_read: []

files_created: []

files_modified: []

validations_run:
  - command: ""
    status: ""
    notes: ""

errors_detected:
  - severity: ""
    type: ""
    description: ""
    impact: ""
    recommended_action: ""

agent_output: {}

handoff:
  current_state: ""
  next_recommended_action: ""
  blockers: []
  risks: []

human_review_required: true
```

Si no aplica `agent_output`, debe indicarse:

```yaml
agent_output: null
```

Si no hubo comandos ejecutados:

```yaml
validations_run: []
validation_status: "not_run"
reason: "Document drafted only; repository validation pending."
```

---

## 12. Salida de agente

Cuando Hermes ejecute un agente, `agent_output` debe incluir:

```yaml
agent_output:
  agent_name: ""
  runtime: "hermes"
  output_type: ""
  status: ""
  summary: ""
  evidence: []
  findings: []
  recommendations: []
  risk_flags: []
  handoff_to: []
  human_review_required: true
```

### 12.1 Campos

| Campo                     | Descripción                          |
| ------------------------- | ------------------------------------- |
| `agent_name`            | Nombre del agente ejecutado           |
| `runtime`               | Siempre`hermes`                     |
| `output_type`           | Tipo de salida producida              |
| `status`                | Estado de la salida                   |
| `summary`               | Resumen ejecutivo                     |
| `evidence`              | Evidencia consultada                  |
| `findings`              | Hallazgos estructurados               |
| `recommendations`       | Recomendaciones o siguientes acciones |
| `risk_flags`            | Riesgos detectados                    |
| `handoff_to`            | Agente, humano o workflow siguiente   |
| `human_review_required` | Indica si requiere revisión humana   |

---

## 13. Tipos de salida permitidos

```yaml
output_type:
  allowed_values:
    - repository_change
    - documentation_update
    - prompt_update
    - agent_execution
    - validation_report
    - audit_report
    - handoff
    - error_report
    - implementation_plan
    - workflow_result
```

---

## 14. Reglas de escritura de archivos

Hermes solo puede escribir en rutas permitidas por el contrato.

Ejemplo:

```yaml
allowed_write_paths:
  - "docs/007-prompts/hermes/"
```

Hermes no debe escribir fuera de alcance.

Si necesita modificar otro archivo, debe registrarlo:

```yaml
out_of_scope_change_request:
  requested_path: ""
  reason: ""
  risk_level: ""
  human_review_required: true
```

No debe aplicar el cambio sin autorización si afecta arquitectura, contratos, seguridad, producción o contenido publicado.

---

## 15. Reglas para crear archivos Markdown

Los documentos Markdown de ORION/XMIP deben incluir:

```text
- título
- metadata
- propósito
- alcance
- reglas operativas
- relación con documentos existentes
- criterios de terminado
- control de cambios
```

Debe respetarse el estilo:

```text
enterprise-grade
documentation-first
operacional
claro
directo
sin relleno
```

No deben crearse documentos duplicados.

No deben crearse documentos sin ruta clara.

---

## 16. Validaciones

Hermes debe validar siempre que sea razonable.

### 16.1 Validaciones documentales

```text
- existe la ruta esperada
- el nombre del archivo cumple convención
- la metadata está completa
- el documento tiene propósito y alcance
- existen documentos relacionados
- no contradice reglas superiores
```

### 16.2 Validaciones técnicas

```text
- JSON válido
- YAML válido
- pruebas automatizadas
- linters
- formato Markdown
- estructura de carpetas
- git diff acotado
- git status revisado
```

### 16.3 Comandos típicos

```bash
git status
git diff
pytest
ruff check .
npm test
npm run lint
markdownlint
```

Si una validación no está disponible, Hermes debe reportarlo.

---

## 17. Registro de validaciones

Cada validación debe registrarse así:

```yaml
validations_run:
  - command: "git status"
    status: "passed"
    notes: "Working tree reviewed."
  - command: "markdownlint docs/007-prompts/hermes/"
    status: "not_run"
    notes: "markdownlint not available in current environment."
```

Valores permitidos:

```yaml
validation_status:
  allowed_values:
    - passed
    - failed
    - warning
    - not_run
```

---

## 18. Manejo de errores

Cuando ocurra un error, Hermes debe registrarlo con estructura:

```yaml
error:
  severity: "medium"
  type: ""
  location: ""
  description: ""
  impact: ""
  recommended_action: ""
  blocks_execution: false
```

### 18.1 Severidades

```yaml
severity:
  allowed_values:
    - low
    - medium
    - high
    - critical
```

### 18.2 Tipos de error

```yaml
error_type:
  allowed_values:
    - missing_input
    - missing_document
    - invalid_format
    - validation_failed
    - out_of_scope
    - unsafe_action
    - conflicting_documents
    - insufficient_evidence
    - runtime_error
    - repository_error
    - permission_required
```

---

## 19. Condiciones de bloqueo

Hermes debe bloquear ejecución cuando ocurra cualquiera de estos casos:

```text
- falta un documento obligatorio
- falta una entrada crítica
- el alcance no está definido
- la acción solicitada es destructiva
- la acción requiere acceso no autorizado
- la tarea contradice reglas superiores
- hay conflicto documental no resoluble
- se requiere publicación externa
- se requiere modificar producción
- se detectan secretos expuestos
- la validación crítica falla
```

Formato:

```yaml
blocked_execution:
  status: "blocked"
  blocking_reason: ""
  blocking_type: ""
  affected_files: []
  required_human_decision: ""
  recommended_next_action: ""
  human_review_required: true
```

---

## 20. Revisión humana obligatoria

Hermes debe marcar `human_review_required: true` cuando exista:

```text
- contenido financiero sensible
- contenido legal o regulatorio
- posible difamación
- publicación externa
- cambios en arquitectura
- cambios en contratos de agentes
- cambios en guardrails editoriales
- eliminación de archivos
- comandos destructivos
- manejo de secretos
- configuración productiva
- validación fallida
- evidencia insuficiente
- conflicto documental
- incertidumbre material
```

El valor por defecto debe ser:

```yaml
human_review_required: true
```

Solo puede cambiar a `false` cuando el cambio sea:

```text
- bajo riesgo
- acotado
- reversible
- documental o técnico menor
- validado
- sin impacto externo
```

---

## 21. Reglas de seguridad

Hermes no debe exponer secretos.

Nunca imprimir completos:

```text
- API keys
- tokens
- passwords
- private keys
- connection strings
- cookies
- session tokens
- secretos CI/CD
```

Si detecta secretos:

```yaml
secret_detected:
  status: "risk_detected"
  secret_type: ""
  location: ""
  exposed_value: "redacted"
  recommended_action:
    - "rotate_secret"
    - "move_to_secret_manager"
    - "remove_from_repository_history_if_needed"
  human_review_required: true
```

---

## 22. Acciones prohibidas

Hermes no debe ejecutar sin autorización explícita:

```text
- borrar archivos
- hacer push remoto
- forzar push
- modificar producción
- ejecutar terraform apply/destroy
- eliminar bases de datos
- limpiar historial git
- ejecutar comandos destructivos
- publicar contenido externo
- cambiar secretos
- cambiar permisos críticos
```

Comandos peligrosos:

```bash
rm -rf
git reset --hard
git clean -fd
git push --force
docker system prune
terraform apply
terraform destroy
kubectl delete
drop database
truncate table
```

---

## 23. Preparación de commits

Hermes puede preparar commits, pero no debe ejecutarlos salvo instrucción explícita.

Antes de proponer commit:

```bash
git status
git diff
```

Formato recomendado:

```text
<type>(<scope>): <summary>
```

Ejemplos:

```text
docs(hermes): add agent execution contract
docs(prompts): add hermes runtime base
ops(hermes): define repository execution rules
```

Salida esperada:

```yaml
commit_preparation:
  suggested_message: "docs(hermes): add agent execution contract"
  files_to_include:
    - "docs/007-prompts/hermes/Hermes-Agent-Execution-Contract.md"
  validations_before_commit:
    - "git status"
    - "git diff"
```

---

## 24. Handoff

Toda ejecución relevante debe cerrar con handoff.

Formato:

```yaml
handoff:
  current_state: ""
  completed:
    - ""
  pending:
    - ""
  next_recommended_action: ""
  blockers: []
  risks: []
  suggested_owner: ""
```

Ejemplo:

```yaml
handoff:
  current_state: "Hermes base execution contract drafted."
  completed:
    - "Created Hermes-Agent-Execution-Contract.md content."
  pending:
    - "Copy file into docs/007-prompts/hermes/"
    - "Run markdown validation."
  next_recommended_action: "Create Hermes-RepositoryOperator.md."
  blockers: []
  risks:
    - "Repository validation pending."
  suggested_owner: "ORION Architecture"
```

---

## 25. Logs de ejecución

Cuando sea necesario, Hermes debe producir logs estructurados.

Formato:

```yaml
execution_log:
  execution_id: ""
  started_at: ""
  finished_at: ""
  runtime: "hermes"
  requested_action: ""
  status: ""
  steps:
    - step: 1
      name: "context_loading"
      status: "completed"
      notes: ""
    - step: 2
      name: "execution"
      status: "completed"
      notes: ""
```

No deben incluirse secretos en logs.

---

## 26. Ejemplo de contrato para crear documentación Hermes

```yaml
hermes_execution_contract:
  execution_id: "hermes-docs-20260702-001"
  task_id: "docs-007-hermes-base"
  workflow_id: "xmip-runtime-prompts"
  agent_name: "Hermes-DocsMaintenanceAgent"
  runtime: "hermes"
  requested_by: "human"
  requested_action: "create_document"
  objective: "Create Hermes-Agent-Execution-Contract.md under docs/007-prompts/hermes/"
  repository_scope:
    - "docs/007-prompts/hermes/"
  input_files:
    - "docs/007-prompts/hermes/README.md"
    - "docs/007-prompts/hermes/00-hermes-global-system.md"
  output_files:
    - "docs/007-prompts/hermes/Hermes-Agent-Execution-Contract.md"
  required_docs:
    - "docs/007-prompts/000-shared/agent-base-contract.md"
    - "docs/007-prompts/000-shared/agent-output-standards.md"
    - "docs/007-prompts/000-shared/editorial-guardrails.md"
  allowed_read_paths:
    - "docs/"
  allowed_write_paths:
    - "docs/007-prompts/hermes/"
  prohibited_actions:
    - "delete_files"
    - "publish_content"
    - "modify_production"
    - "push_remote"
  validation_commands:
    - "git status"
    - "markdownlint docs/007-prompts/hermes/Hermes-Agent-Execution-Contract.md"
  expected_output_format: "markdown"
  risk_level: "low"
  human_review_required: true
  success_criteria:
    - "File exists in expected path"
    - "Metadata is complete"
    - "Execution contract is explicit"
    - "Output format is documented"
    - "Human review rules are defined"
  rollback_notes: "Remove created file if rejected during review."
  handoff_required: true
```

---

## 27. Ejemplo de cierre de ejecución

```yaml
execution_summary:
  status: "completed_with_warnings"
  objective: "Create Hermes-Agent-Execution-Contract.md"
  result: "Document content prepared and ready to copy into repository."

files_read:
  - "docs/007-prompts/hermes/README.md"
  - "docs/007-prompts/hermes/00-hermes-global-system.md"

files_created:
  - "docs/007-prompts/hermes/Hermes-Agent-Execution-Contract.md"

files_modified: []

validations_run: []
validation_status: "not_run"
reason: "Document drafted outside repository runtime; local validation pending."

errors_detected: []

agent_output:
  agent_name: "Hermes-DocsMaintenanceAgent"
  runtime: "hermes"
  output_type: "documentation_update"
  status: "draft_ready"
  summary: "Created execution contract for Hermes agent operations."
  evidence:
    - "Hermes README"
    - "Hermes global system prompt"
    - "Shared XMIP prompt architecture"
  findings: []
  recommendations:
    - "Copy file into docs/007-prompts/hermes/"
    - "Run markdown validation"
    - "Proceed with Hermes-RepositoryOperator.md"
  risk_flags:
    - "repository_validation_pending"
  handoff_to:
    - "ORION Architecture"
  human_review_required: true

handoff:
  current_state: "Hermes base execution contract is drafted."
  next_recommended_action: "Create Hermes-RepositoryOperator.md."
  blockers: []
  risks:
    - "Validation pending after file is copied into repository."

human_review_required: true
```

---

## 28. Criterios de terminado

Una ejecución Hermes se considera terminada cuando:

```text
- el objetivo fue cumplido o bloqueado explícitamente
- el alcance fue respetado
- los archivos leídos fueron registrados
- los archivos creados o modificados fueron registrados
- las validaciones fueron ejecutadas o justificadas como no ejecutadas
- los errores fueron reportados
- el handoff quedó claro
- human_review_required fue definido
```

No se permite cerrar con estado ambiguo.

---

## 29. Relación con próximos adaptadores Hermes

Este contrato debe ser usado por todos los adaptadores Hermes futuros:

```text
Hermes-NewsScoutAgent.md
Hermes-SourceValidatorAgent.md
Hermes-EditorialAgent.md
Hermes-MarketImpactAgent.md
Hermes-ScriptAgent.md
Hermes-RiskAgent.md
Hermes-AuditAgent.md
Hermes-KnowledgeAgent.md
Hermes-DistributionAgent.md
Hermes-SocialClipAgent.md
Hermes-MemoryAgent.md
Hermes-MetricsAgent.md
Hermes-CalendarAgent.md
Hermes-RepositoryOperator.md
Hermes-DocsMaintenanceAgent.md
```

Cada adaptador podrá agregar reglas específicas, pero no puede contradecir este contrato.

---

## 30. Regla final

```text
Hermes debe ser útil porque ejecuta con control.

No por producir más texto.
No por improvisar arquitectura.
No por actuar como agente editorial.
No por correr comandos sin criterio.

Hermes existe para convertir documentación ORION en operación local segura, auditable y repetible.
```

---

## 31. Control de cambios

| Versión |      Fecha | Cambio                                                         | Owner              |
| -------- | ---------: | -------------------------------------------------------------- | ------------------ |
| 0.1.0    | 2026-07-02 | Creación inicial del contrato de ejecución de agentes Hermes | ORION Architecture |
