# XMIP Professional Newsroom QA

| Campo | Valor |
| --- | --- |
| Proyecto | ORION / XCripto / XMIP |
| Tipo | Estándar editorial + checklists de QA |
| Estado | Draft implementable (Hard Phase P0) |
| Última actualización | 2026-07-03 |
| Documentos relacionados | `SOURCE_QUALITY_POLICY.md`, `docs/002-editorial/`, `docs/007-prompts/000-shared/editorial-guardrails.md` |

---

## 1. Estándar editorial XMIP

XCripto opera como agencia de inteligencia y noticias cripto. El producto es
**confianza**: noticias fidedignas, trazables y verificadas. El sistema debe
hacer difícil publicar mal y fácil publicar bien.

Principios innegociables:

```text
1.  Fuente identificable en toda noticia.
2.  Fuente primaria (S1) preferida; S2 confiable si no hay primaria.
3.  URL verificable y accesible.
4.  Fecha/hora clara del hecho y del registro.
5.  Separación explícita entre hecho, interpretación y opinión.
6.  No afirmar causalidad sin evidencia.
7.  No predecir precios ni dar señales de trading.
8.  No presentar rumores como hechos.
9.  No publicar con contradicción crítica abierta.
10. No publicar sin verificación registrada.
11. No publicar con riesgo legal/editorial crítico sin aprobación humana.
12. Trazabilidad de auditoría en cada paso (correlation_id + audit log).
13. Toda publicación es corregible y retractable, con registro.
14. Un output de agente no es fuente ni aprobación.
```

---

## 2. Criterios de fuente fidedigna

Ver `SOURCE_QUALITY_POLICY.md` (niveles S1–S5). Resumen operativo:

- Publicable directo: S1, S2.
- Con confirmación adicional: S3.
- Solo señal, nunca confirmación única: S4.
- Nunca como hecho: S5.

---

## 3. Noticia publicable (criterios mínimos)

Una noticia puede avanzar a `approved`/`scheduled` solo si:

```text
[x] NewsItem con título factual y no sensacionalista
[x] SourceReference o source_url/source_name verificables (S1/S2, o S3 confirmada)
[x] VerificationRecord con verification_status verified o partially_verified
    (partially_verified exige etiquetado explícito de lo no confirmado)
[x] RiskReview con decision_recommendation permisiva (allow / allow_with_minor_edits)
[x] AuditCheck aprobatorio (passed / passed_with_warnings, ready_to_advance=true,
    sin publication_block_recommended)
[x] AgentOutputs con risk_flags revisados y aceptados por humano (accepted_by)
[x] Editorial readiness sin blocking_reasons
[x] ContentPiece en approved
```

## 4. Noticia bloqueada (cualquiera de estas condiciones)

```text
[ ] Sin fuente o fuente S5 como único soporte
[ ] VerificationRecord en rumor / contradicted / rejected
[ ] Contradicción crítica sin resolver entre fuentes
[ ] RiskReview con block_publication / escalate sin resolución
[ ] AuditCheck con publication_block_recommended=true
[ ] AgentOutput con risk_flags críticos sin aceptación humana
[ ] Predicción de precio o recomendación financiera en el cuerpo
[ ] Causalidad afirmada sin evidencia ("el precio cayó POR X")
[ ] Título que promete lo que el cuerpo no sostiene (clickbait)
```

---

## 5. Checklists operativos

### 5.1 Checklist de verificación (SourceValidator / humano)

```text
1. ¿La URL abre y corresponde a la fuente declarada?
2. ¿La fuente es S1/S2, o S3 con confirmación?
3. ¿La fecha del hecho es actual y está clara?
4. ¿Los claims centrales están respaldados textualmente por la fuente?
5. ¿Hay claims sin verificar? → listarlos en unverified_claims.
6. ¿Hay contradicciones con otras fuentes? → listarlas en contradictions.
7. Asignar evidence_level y confidence_level honestos (fail closed).
```

### 5.2 Checklist de riesgo (RiskAgent / humano)

```text
1. ¿Involucra regulación, demanda, sanción, fraude o acusación? → lenguaje atribuido.
2. ¿Involucra hack/exploit? → nada explotable, nada sin confirmar.
3. ¿Menciona activos específicos? → sin lenguaje de señal financiera.
4. ¿Hay riesgo reputacional o legal para terceros identificables?
5. ¿Requiere disclaimers? → listarlos en required_disclaimers.
6. Decisión del catálogo: allow / revise / hold / block / escalate.
```

### 5.3 Checklist de auditoría (AuditAgent / humano)

```text
1. ¿Existen VerificationRecord y RiskReview vinculados?
2. ¿El estado editorial es coherente con la evidencia?
3. ¿correlation_id presente en la cadena?
4. ¿Los agentes actuaron dentro de su contrato?
5. ¿ready_to_advance refleja la realidad?
6. Registrar missing_requirements accionables.
```

---

## 6. Criterios anti-clickbait

```text
- El título afirma solo lo que la evidencia sostiene.
- Sin mayúsculas de alarma, sin "URGENTE" salvo breaking verificado.
- Sin preguntas retóricas que insinúan lo indemostrado ("¿Se desploma X?").
- Números con fuente y contexto (base, periodo, denominación).
- La incertidumbre se declara en el título si es material ("según", "reporta").
```

## 7. Criterios cripto/mercados

```text
- Prohibido: predicciones de precio, targets, "señales", buy/sell/long/short.
- Correlación temporal ≠ causalidad; escribir "coincide con", no "provocó",
  salvo evidencia directa.
- Datos on-chain: citar explorer + tx/altura de bloque; la intención del
  actor es inferencia y se etiqueta como tal.
- Métricas de mercado siempre con proveedor y timestamp.
- Diferenciación explícita: hecho / interpretación / opinión de la casa.
```

## 8. Reglas sobre rumores

```text
- Un rumor entra como IntakeSignal con confidence bajo, nunca como NewsItem verificado.
- Estado editorial `rumor` → solo monitoreo interno; no se publica como hecho.
- Si se cubre un rumor relevante (por impacto de mercado), el título y el
  cuerpo lo etiquetan como no confirmado y citan qué falta para confirmarlo.
```

## 9. Reglas sobre predicciones

```text
- XMIP no publica predicciones de precio propias ni de terceros como hechos.
- Escenarios condicionales permitidos solo con: supuestos explícitos,
  factores en contra, y disclaimer de no-recomendación.
```

## 10. Conflicto de interés

```text
- Posiciones propias del equipo en activos cubiertos se declaran internamente.
- Nadie edita/aprueba una pieza sobre un activo en el que tenga interés
  material sin declararlo; el aprobador debe ser otra persona.
- Contenido pagado o patrocinado se etiqueta siempre; nunca se mezcla con noticia.
```

## 11. Correcciones

```text
- Error material detectado → corrección visible, no edición silenciosa.
- El NewsItem pasa a `corrected`; se registra qué cambió, cuándo y por qué.
- La corrección se distribuye por los mismos canales que el original.
```

## 12. Retractaciones

```text
- Si el hecho central resulta falso → `retracted`, no borrado.
- La pieza retirada conserva registro y explicación pública del motivo.
- Post-mortem interno obligatorio: qué falló en la cadena de verificación.
```

---

## 13. Ejemplo de noticia ACEPTABLE

```text
Título: "Exchange X publica reporte de transparencia de reservas"
Fuente: comunicado oficial del exchange (S1) + URL verificable
Cuerpo: hechos del comunicado con atribución ("según el reporte publicado
por X el 3 de julio…"), contexto de reportes anteriores, y una sección de
interpretación claramente separada. Sin targets de precio.
Cadena: VerificationRecord verified (E2/C2) → RiskReview allow →
AuditCheck passed → outputs aceptados → readiness ready_to_advance.
```

## 14. Ejemplo de noticia BLOQUEADA

```text
Título propuesto: "INMINENTE: ballena mueve fondos y el precio se desplomará"
Problemas: fuente S4/S5 (screenshot de Telegram), causalidad afirmada sin
evidencia, predicción de precio, título alarmista, sin VerificationRecord.
Resultado esperado del sistema: VerificationRecord imposible (unverified),
RiskAgent → block_publication, readiness blocked. NO SE PUBLICA.
```

---

## 15. Validación automatizada local

El flujo completo se puede ejercitar localmente con:

```bash
python scripts/local_newsroom_qa.py --base-url http://127.0.0.1:8000 \
    --api-key dev-secret --actor-role admin
```

Ver `LOCAL_RELEASE_CANDIDATE_REPORT.md` para el estado del último ciclo de QA.
