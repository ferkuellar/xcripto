
# ORION-014B — Especificación de Agentes Digitales

**Proyecto:** Project ORION
**Producto:** XCripto Media Intelligence Platform (XMIP)
**Clasificación:** L2 - Arquitectura Organizacional
**Tipo de Documento:** Especificación de Agentes Digitales
**Versión:** 1.0.0
**Estado:** Aprobado
**Propietario:** Fernando Cuéllar
**Creado:** 2026-07-01
**Última Actualización:** 2026-07-01

---

# Propósito

Este documento establece el estándar oficial para diseñar, documentar, implementar y mantener todos los agentes digitales de XMIP.

Su objetivo es garantizar que cualquier agente, independientemente del modelo de inteligencia artificial utilizado, posea una estructura uniforme, responsabilidades claramente definidas y comportamiento consistente.

Los agentes representan puestos organizacionales.

No representan prompts.

---

# Filosofía

Un agente digital es un empleado especializado.

Tiene:

- misión;
- responsabilidades;
- límites;
- indicadores;
- procesos;
- herramientas;
- memoria;
- objetivos.

La inteligencia artificial constituye únicamente el motor de razonamiento.

La definición del agente permanece independiente del proveedor tecnológico.

---

# Objetivos

Esta especificación busca:

- estandarizar todos los agentes;
- facilitar mantenimiento;
- permitir reemplazo de modelos;
- reducir dependencia tecnológica;
- mejorar reutilización;
- facilitar auditoría;
- documentar responsabilidades.

---

# Ciclo de Vida

Todo agente deberá pasar por las siguientes etapas.

```
Diseño

↓

Documentación

↓

Revisión

↓

Implementación

↓

Pruebas

↓

Despliegue

↓

Monitoreo

↓

Mejora Continua
```

---

# Estructura Oficial

Todo agente deberá documentarse utilizando exactamente la siguiente plantilla.

---

# 1. Información General

## Nombre

Nombre oficial.

---

## Código

Identificador único.

Ejemplo

```
AG-001
```

---

## Departamento

Ejemplo:

Research

Editorial

Analytics

Knowledge

Automation

---

## Versión

Versión del agente.

---

## Estado

- Diseño
- Desarrollo
- Pruebas
- Producción
- Retirado

---

# 2. Propósito

Explicar en un párrafo por qué existe el agente.

Debe responder únicamente una necesidad organizacional.

---

# 3. Misión

Describir claramente la misión permanente del agente.

La misión nunca deberá cambiar con frecuencia.

---

# 4. Objetivos

Definir objetivos medibles.

Ejemplo.

- Detectar noticias relevantes.
- Clasificar eventos.
- Reducir tiempo de investigación.

---

# 5. Responsabilidades

Lista completa de responsabilidades.

No deben existir responsabilidades ambiguas.

---

# 6. Responsabilidades Prohibidas

Especificar aquello que el agente nunca debe realizar.

Ejemplo.

- Publicar directamente.
- Inventar información.
- Tomar decisiones editoriales.

---

# 7. Entradas

Todo aquello que el agente puede recibir.

Ejemplo.

- RSS
- APIs
- URLs
- Stories
- Archivos
- Noticias
- Documentos

---

# 8. Salidas

Todo aquello que produce.

Ejemplo.

- Resúmenes
- Dossiers
- Stories
- Reportes
- Prompts
- Entidades

---

# 9. Herramientas Permitidas

Lista de herramientas autorizadas.

Ejemplo.

- Claude
- GPT
- Base de Conocimiento
- APIs
- GitHub
- RSS
- Base Vectorial

---

# 10. Herramientas Restringidas

Herramientas o funciones que requieren autorización especial.

---

# 11. Herramientas Prohibidas

Acciones que nunca podrá ejecutar.

---

# 12. Conocimiento Requerido

Documentos ORION obligatorios.

Ejemplo.

- Project Charter
- Doctrina
- Principios Operativos
- Constitución Editorial

---

# 13. Memoria

Especificar qué memoria puede consultar.

Ejemplo.

- Base de Conocimiento
- Grafo
- Stories
- Documentación
- Historial

---

# 14. Memoria Temporal

Definir qué información puede mantener únicamente durante una ejecución.

---

# 15. Contexto Mínimo

Información indispensable antes de ejecutar una tarea.

---

# 16. Flujo de Trabajo

Describir paso a paso el proceso que sigue el agente.

---

# 17. Interacciones

Indicar con qué agentes puede comunicarse.

Ejemplo.

Research Agent

↓

Fact Checker

↓

Story Builder

↓

Script Writer

---

# 18. Reglas Operativas

Lista de reglas obligatorias.

Ejemplo.

- Nunca inventar datos.
- Siempre citar fuentes.
- Registrar decisiones.
- Respetar la Doctrina.

---

# 19. Criterios de Escalamiento

Situaciones donde debe solicitar intervención humana.

Ejemplo.

- Evidencia insuficiente.
- Riesgo legal.
- Conflicto editorial.
- Información contradictoria.

---

# 20. KPIs

Cada agente deberá tener indicadores propios.

Ejemplo.

- tareas completadas;
- tiempo promedio;
- precisión;
- reutilización;
- errores;
- escalamientos.

---

# 21. Calidad Esperada

Definir el nivel mínimo aceptable.

---

# 22. Casos Límite

Documentar situaciones especiales.

Ejemplo.

- información incompleta;
- datos contradictorios;
- múltiples fuentes;
- eventos simultáneos.

---

# 23. Riesgos

Riesgos asociados al agente.

---

# 24. Mitigaciones

Acciones para reducir riesgos.

---

# 25. Prompt del Sistema

Descripción funcional del comportamiento esperado.

No deberá contener lógica de negocio.

---

# 26. Prompt del Desarrollador

Instrucciones específicas para la implementación.

---

# 27. Plantillas

Templates utilizados por el agente.

---

# 28. Ejemplos

Ejemplos reales de entradas y salidas.

---

# 29. Casos de Prueba

Escenarios utilizados para validar el agente.

---

# 30. Observabilidad

Definir qué métricas registra.

---

# 31. Auditoría

Información mínima que debe quedar registrada.

- fecha;
- tarea;
- resultado;
- duración;
- herramientas utilizadas.

---

# 32. Dependencias

Otros agentes o servicios requeridos.

---

# 33. Versionado

Todo cambio importante deberá incrementar la versión.

---

# Convención de Identificadores

```
AG-001 Research Agent

AG-002 Fact Checker

AG-003 Context Builder

AG-004 Story Builder

AG-005 Script Writer

AG-006 Editorial Reviewer

AG-007 Publishing Manager

AG-008 Knowledge Curator

...
```

---

# Principios de Diseño

Todo agente debe cumplir:

- Una única misión.
- Una única responsabilidad principal.
- Interfaces simples.
- Entradas claramente definidas.
- Salidas claramente definidas.
- Documentación completa.
- Reutilización máxima.
- Bajo acoplamiento.
- Alta cohesión.

---

# Antipatrones

Nunca diseñar agentes que:

- hagan múltiples trabajos;
- oculten decisiones;
- dependan del contexto del chat;
- modifiquen responsabilidades ajenas;
- inventen información;
- publiquen sin revisión.

---

# Definición de Éxito

La arquitectura de agentes habrá alcanzado su objetivo cuando cualquier nuevo agente pueda diseñarse, implementarse y desplegarse utilizando esta especificación sin necesidad de definir nuevamente su estructura.

La organización deberá crecer incorporando nuevos agentes siguiendo exactamente el mismo estándar.

---

# Relación con Otros Documentos

Este documento depende de:

- ORION-003 — Principios Operativos
- ORION-007 — Flujo Editorial
- ORION-009 — Principios de Arquitectura Empresarial
- ORION-014 — Arquitectura de Agentes
- ORION-014A — Protocolo de Comunicación entre Agentes

---

# Aprobación

La Especificación de Agentes Digitales constituye el estándar oficial para el diseño e implementación de todos los empleados digitales de XMIP.

Ningún agente podrá incorporarse a la plataforma sin una especificación completa basada en este documento.
