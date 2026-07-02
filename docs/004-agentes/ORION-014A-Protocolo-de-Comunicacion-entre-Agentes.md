
# ORION-014A — Protocolo de Comunicación entre Agentes

**Proyecto:** Project ORION
**Producto:** XCripto Media Intelligence Platform (XMIP)
**Clasificación:** L2 - Arquitectura Organizacional
**Tipo de Documento:** Protocolo de Comunicación entre Agentes
**Versión:** 1.0.0
**Estado:** Aprobado
**Propietario:** Fernando Cuéllar
**Creado:** 2026-07-01
**Última Actualización:** 2026-07-01

---

# Propósito

Este documento establece el protocolo oficial mediante el cual los agentes inteligentes de XMIP intercambian información, delegan tareas, coordinan actividades y colaboran durante la ejecución de los procesos editoriales.

Su objetivo principal es garantizar:

- Consistencia.
- Trazabilidad.
- Escalabilidad.
- Reutilización.
- Desacoplamiento.
- Colaboración eficiente.

Todo intercambio de información entre agentes deberá seguir este protocolo.

---

# Principios

La comunicación entre agentes se basa en los siguientes principios.

## Claridad

Toda solicitud debe ser explícita.

Nunca deberán existir instrucciones ambiguas.

---

## Especialización

Cada agente solicita únicamente aquello que otro agente está autorizado para realizar.

---

## Responsabilidad

Cada agente es responsable exclusivamente de sus entregables.

Nunca modifica directamente el trabajo de otro agente.

---

## Trazabilidad

Toda interacción debe dejar evidencia.

Debe poder reconstruirse posteriormente.

---

## Independencia

Los agentes nunca dependerán del estado interno de otro agente.

Toda comunicación deberá contener el contexto necesario.

---

## Idempotencia

Una misma solicitud podrá ejecutarse múltiples veces sin producir resultados inconsistentes.

---

# Filosofía

Los agentes no conversan.

Los agentes intercambian contratos.

Toda interacción representa un compromiso claramente definido.

---

# Modelo General

```
Solicitud

↓

Validación

↓

Ejecución

↓

Resultado

↓

Confirmación

↓

Registro

↓

Base de Conocimiento
```

---

# Contrato de Comunicación

Toda comunicación entre agentes deberá contener la siguiente información.

## Identificador

ID único de la tarea.

---

## Agente Emisor

Quién genera la solicitud.

---

## Agente Receptor

Quién ejecutará la tarea.

---

## Objetivo

Descripción clara del resultado esperado.

---

## Prioridad

- Crítica
- Alta
- Media
- Baja

---

## Contexto

Información necesaria para ejecutar correctamente la tarea.

---

## Entradas

Archivos.

URLs.

Documentos.

Stories.

Datos.

---

## Restricciones

Limitaciones específicas.

---

## Resultado Esperado

Descripción del entregable.

---

## Fecha

Momento de creación.

---

## Estado

Pendiente.

En ejecución.

Completado.

Rechazado.

Escalado.

---

# Flujo de Comunicación

```
Agente A

↓

Crear Solicitud

↓

Validación

↓

Agente B

↓

Procesamiento

↓

Respuesta

↓

Registro

↓

Base de Conocimiento
```

---

# Estados Oficiales

Toda tarea deberá encontrarse exactamente en uno de los siguientes estados.

## Nuevo

La tarea acaba de generarse.

---

## Pendiente

Está esperando procesamiento.

---

## En Ejecución

Está siendo procesada.

---

## En Revisión

Esperando validación.

---

## Completado

Finalizó correctamente.

---

## Rechazado

No pudo ejecutarse.

---

## Escalado

Requiere intervención humana.

---

# Reglas de Delegación

Un agente puede delegar únicamente cuando:

- otro agente sea especialista;
- exista una interfaz documentada;
- el contexto sea suficiente.

Nunca deberá delegarse una responsabilidad completa.

Únicamente tareas específicas.

---

# Manejo de Errores

Cuando ocurra un error el agente deberá:

1. Registrar el problema.
2. Explicar la causa.
3. Proponer acciones.
4. Mantener evidencia.
5. Escalar si corresponde.

Nunca deberá ocultar errores.

---

# Escalamiento

Los siguientes casos requieren revisión humana.

- Información contradictoria.
- Evidencia insuficiente.
- Riesgo reputacional.
- Riesgo legal.
- Posible desinformación.
- Fallas repetidas.
- Decisiones editoriales.

---

# Contexto Compartido

Todos los agentes podrán consultar:

- Project ORION.
- Documentación oficial.
- Base de Conocimiento.
- Historias.
- Glosario.
- Doctrina.
- Principios Operativos.
- Constitución Editorial.

Los agentes no deberán inventar contexto.

---

# Memoria

Los agentes no almacenan conocimiento permanente localmente.

La memoria oficial reside en:

- Base de Conocimiento.
- Grafo de Conocimiento.
- Documentación ORION.

Toda memoria temporal deberá descartarse al finalizar la tarea.

---

# Reutilización

Antes de generar contenido nuevo todo agente deberá verificar:

- ¿Existe una Story relacionada?
- ¿Existe una investigación previa?
- ¿Existe contenido reutilizable?
- ¿Existe una respuesta documentada?

La reutilización tiene prioridad sobre la duplicación.

---

# Seguridad

Los agentes nunca compartirán:

- credenciales;
- secretos;
- información privada;
- datos sensibles;
- claves de API.

El acceso deberá realizarse mediante servicios autorizados.

---

# Observabilidad

Toda interacción deberá registrar:

- agente emisor;
- agente receptor;
- duración;
- resultado;
- errores;
- archivos utilizados;
- documentos consultados.

---

# Indicadores

Cada agente reportará:

- tareas recibidas;
- tareas completadas;
- tiempo promedio;
- errores;
- escalamientos;
- reutilización de conocimiento.

---

# Principios de Calidad

Toda comunicación debe ser:

Correcta.

Completa.

Verificable.

Trazable.

Reutilizable.

Comprensible.

---

# Antipatrones

No están permitidos los siguientes comportamientos.

## Comunicación implícita

Nunca asumir información.

---

## Contexto oculto

Todo contexto importante debe viajar con la solicitud.

---

## Responsabilidades compartidas

Cada tarea tiene un único responsable.

---

## Dependencias circulares

Los agentes no deben depender mutuamente para completar una tarea.

---

## Duplicación

Nunca realizar el mismo trabajo dos veces.

---

# Integración con XMIP

Este protocolo constituye la base para:

- Workflow Engine.
- Orquestador.
- Event Bus.
- APIs internas.
- Automatización.
- Observabilidad.
- Auditoría.
- Dashboards.

Todo componente deberá respetar este protocolo.

---

# Definición de Éxito

El protocolo habrá cumplido su propósito cuando cualquier agente pueda colaborar con otro sin necesidad de instrucciones adicionales, manteniendo trazabilidad, calidad y consistencia en todo el flujo editorial.

La comunicación deberá parecer la de un equipo profesional y no la de una colección de asistentes independientes.

---

# Relación con Otros Documentos

Este documento depende de:

- ORION-000 — Project Charter
- ORION-000A — Glosario del Proyecto
- ORION-000B — Doctrina XCripto
- ORION-003 — Principios Operativos
- ORION-007 — Flujo Editorial
- ORION-014 — Arquitectura de Agentes

---

# Aprobación

Este documento establece el protocolo oficial de comunicación entre todos los agentes de XMIP.

Toda interacción entre agentes deberá implementarse conforme a estas reglas para garantizar una organización digital escalable, trazable y consistente.
