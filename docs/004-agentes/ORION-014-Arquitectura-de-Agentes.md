
# ORION-014 — Arquitectura de Agentes

**Proyecto:** Project ORION
**Producto:** XCripto Media Intelligence Platform (XMIP)
**Clasificación:** L2 - Arquitectura Organizacional
**Tipo de Documento:** Arquitectura de Agentes
**Versión:** 1.0.0
**Estado:** Aprobado
**Propietario:** Fernando Cuéllar
**Creado:** 2026-07-01
**Última Actualización:** 2026-07-01

---

# Propósito

Este documento define la estructura organizacional de agentes inteligentes que operan dentro de XMIP.

La arquitectura está inspirada en una empresa editorial moderna y no en un conjunto aislado de asistentes de IA.

Cada agente representa un rol organizacional claramente definido.

Los agentes colaboran entre sí mediante flujos documentados y APIs internas.

---

# Filosofía

En XCripto los agentes no sustituyen personas.

Representan funciones organizacionales.

Cada agente tiene:

- misión;
- responsabilidades;
- autoridad;
- métricas;
- entradas;
- salidas;
- herramientas.

Los agentes constituyen el equipo digital de la organización.

---

# Principios

La arquitectura sigue los siguientes principios.

## Especialización

Cada agente resuelve un único problema.

---

## Colaboración

Los agentes trabajan como una organización.

No como asistentes aislados.

---

## Trazabilidad

Toda decisión importante debe poder reconstruirse.

---

## Supervisión Humana

Las decisiones estratégicas y editoriales permanecen bajo control humano.

---

## Escalabilidad

Cualquier agente podrá duplicarse cuando aumente la carga de trabajo.

---

# Organigrama General

```
                    Founder

                        │

                        ▼

              Director Editorial

                        │

 ┌────────────┬────────────┬────────────┬────────────┐

 ▼            ▼            ▼            ▼

Research    Producción   Distribución   Analytics

Manager      Manager       Manager       Manager
```

Cada manager coordina agentes especializados.

---

# Nivel Ejecutivo

## Founder

Responsable:

Fernando Cuéllar

Funciones:

- estrategia;
- decisiones finales;
- visión;
- aprobación.

No se automatiza.

---

## Director Editorial

Es el coordinador principal del Newsroom.

Responsabilidades:

- asignar prioridades;
- aprobar publicaciones;
- coordinar equipos;
- mantener estándares.

Será asistido por IA.

No será completamente automatizado.

---

# Departamento de Investigación

## Research Manager

Responsable de coordinar toda investigación.

Gestiona:

- Research Agent
- Source Collector
- Fact Checker
- Context Builder

---

## Research Agent

Misión

Encontrar información relevante.

Entradas

RSS

APIs

Redes

Blogs

GitHub

Salidas

Eventos candidatos.

---

## Source Collector

Responsabilidad

Encontrar fuentes primarias.

---

## Fact Checker

Responsabilidad

Validar información.

Nunca genera contenido.

---

## Context Builder

Responsabilidad

Construir antecedentes históricos.

---

# Departamento Editorial

## Story Builder

Agrupa múltiples noticias dentro de una narrativa.

Producto:

Story.

---

## Script Writer

Convierte la Story en un guion.

---

## Editorial Reviewer

Evalúa:

- claridad;
- calidad;
- doctrina;
- estándares editoriales.

---

# Departamento Multimedia

## Thumbnail Strategist

Propone conceptos para miniaturas.

No genera imágenes.

Genera dirección creativa.

---

## Image Prompt Engineer

Genera prompts optimizados.

---

## Video Producer

Construye la estructura audiovisual.

---

# Departamento de Distribución

## Publishing Manager

Coordina publicaciones.

---

## SEO Specialist

Optimiza contenido.

---

## Social Media Agent

Adapta contenido para:

- X
- LinkedIn
- Facebook
- Instagram
- Threads

---

## Newsletter Agent

Genera el boletín diario.

---

# Departamento de Inteligencia

## Knowledge Curator

Actualiza la Base de Conocimiento.

---

## Knowledge Graph Manager

Mantiene relaciones entre entidades.

---

## Trend Analyst

Detecta narrativas emergentes.

---

## Sentiment Analyst

Analiza percepción del mercado.

---

# Departamento de Analítica

## Metrics Analyst

Calcula indicadores.

---

## Performance Analyst

Evalúa rendimiento del contenido.

---

## Recommendation Agent

Propone mejoras.

---

# Departamento de Automatización

## Workflow Orchestrator

Coordina todos los flujos.

---

## Scheduler

Gestiona calendarios.

---

## Notification Agent

Genera alertas.

---

# Interacción Entre Agentes

Todo intercambio deberá realizarse mediante contratos definidos.

Nunca mediante instrucciones ambiguas.

Cada agente conocerá únicamente:

- sus entradas;
- sus responsabilidades;
- sus salidas.

---

# Memoria

Los agentes podrán acceder a:

- Base de Conocimiento.
- Historias.
- Documentación ORION.
- Prompts.
- Contexto operativo.

Nunca deberán depender exclusivamente del contexto de una conversación.

---

# KPIs

Cada agente deberá tener indicadores.

Ejemplos:

Research

- historias detectadas;
- fuentes verificadas.

Editorial

- publicaciones aprobadas;
- correcciones.

Knowledge

- entidades registradas;
- reutilización.

Analytics

- precisión;
- cobertura;
- tiempos.

---

# Escalabilidad

La organización debe crecer mediante especialización.

Nunca aumentando complejidad innecesaria.

Cuando un área supere su capacidad se incorporarán nuevos agentes.

No se modificarán responsabilidades existentes.

---

# Roadmap

Fase 1

Research.

Story.

Script.

Publishing.

Knowledge.

---

Fase 2

Analytics.

SEO.

Newsletter.

---

Fase 3

Automatización completa.

---

Fase 4

Agentes especializados para clientes empresariales.

---

# Definición de Éxito

La Arquitectura de Agentes habrá cumplido su propósito cuando XMIP pueda operar como una redacción digital donde cada agente tenga responsabilidades claramente definidas, procesos documentados y objetivos medibles.

---

# Aprobación

Este documento constituye la estructura organizacional oficial de agentes inteligentes de Project ORION.

Toda automatización futura deberá alinearse con esta arquitectura.
