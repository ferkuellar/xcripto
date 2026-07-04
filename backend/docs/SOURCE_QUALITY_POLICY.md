# XMIP Source Quality Policy

| Campo | Valor |
| --- | --- |
| Proyecto | ORION / XCripto / XMIP |
| Tipo | Política editorial operativa |
| Estado | Enforced (backend) — ver §6 |
| Última actualización | 2026-07-04 |
| Documentos relacionados | `PROFESSIONAL_NEWSROOM_QA.md`, `docs/006-operaciones/ORION-021-Gestion-de-Fuentes.md`, `docs/007-prompts/000-shared/editorial-guardrails.md` |

---

## 1. Propósito

Definir los niveles de calidad de fuente que XMIP usa para decidir si una señal
puede convertirse en noticia y si una noticia puede avanzar hacia publicación.

Regla central:

```text
Nada se publica sin fuente.
La calidad de la fuente determina el techo de certeza de la noticia.
```

---

## 2. Niveles de fuente

| Nivel | Definición | Ejemplos cripto |
| --- | --- | --- |
| **S1** | Fuente primaria oficial | Comunicado de la SEC/CFTC/DOJ, banco central, CNBV u otro regulador; blog/postmortem oficial de un protocolo; release/tag oficial en el GitHub del proyecto; anuncio oficial del exchange; filing regulatorio; transacción verificable en un on-chain explorer |
| **S2** | Medio reconocido / institución con proceso editorial | Agencias y medios establecidos (p. ej. Reuters, Bloomberg, CoinDesk, The Block); comunicados de empresas listadas; datos de proveedores institucionales |
| **S3** | Analista identificado con historial verificable | Investigadores on-chain con identidad y track record público; firmas de análisis identificables |
| **S4** | Social media no confirmada | Cuentas en X/Twitter (incluso "oficiales" sin verificación cruzada), Telegram, Discord, foros |
| **S5** | Rumor / anónimo / fuente opaca | "Fuentes cercanas" sin identificar, capturas sin origen, cadenas reenviadas, cuentas anónimas |

---

## 3. Reglas de uso por nivel

```text
S1 y S2  → pueden alimentar una noticia directamente.
S3       → requiere confirmación adicional (S1/S2 u otra S3 independiente).
S4       → solo es SEÑAL de intake; requiere verificación fuerte antes de
           afirmar cualquier hecho. Nunca es confirmación única.
S5       → NO debe publicarse como hecho. Solo puede existir como señal
           interna en monitoreo, etiquetada como rumor.
```

Reglas cripto-específicas:

```text
- X/Twitter, Telegram y Discord son canales de DETECCIÓN, no de confirmación.
- Un hack/exploit no se afirma sin: confirmación del protocolo afectado (S1),
  o evidencia on-chain verificable (S1) + corroboración independiente.
- Un movimiento on-chain (explorer) prueba la transacción, NO la intención
  ni la identidad del actor — separar hecho de inferencia.
- Anuncios de listados/delistings: solo el exchange (S1) confirma.
- Acciones regulatorias: solo el documento o comunicado del regulador (S1)
  confirma; la cobertura de prensa es S2 y debe citar el documento.
- Métricas de mercado: proveedor identificado y timestamp obligatorios.
```

---

## 4. Mapeo a campos del sistema

| Concepto | Campo XMIP |
| --- | --- |
| Nivel de fuente S1–S5 | `SourceReference.source_type` + `trust_level` (T0≈S1, T1≈S2, T2≈S3, T3≈S4/S5) |
| Estado de la fuente | `SourceReference.source_status` (`proposed/active/trusted/watchlist/restricted/blocked`) |
| Evidencia de una noticia | `VerificationRecord.evidence_level`, `confidence_level`, `source_refs` |
| Señal sin confirmar | `IntakeSignal.confidence_level` (IC0–IC5) + `signal_status` |

Una fuente en `blocked` o `restricted` no puede sostener una noticia por sí sola;
las señales que dependan solo de ella se rechazan o quedan en monitoreo.

---

## 5. Decisión rápida (operador)

```text
¿Existe URL verificable y autor/institución identificable?     NO → S5
¿Es el actor directamente involucrado o un regulador?           SÍ → S1
¿Es un medio/institución con proceso editorial reconocido?      SÍ → S2
¿Es un analista identificado con historial?                     SÍ → S3
¿Es social media?                                               SÍ → S4
```

En caso de duda entre dos niveles, asignar el MÁS BAJO (fail closed).

---

## 6. Enforcement en el sistema

La política se implementa en `app/core/source_quality.py` (módulo puro, S1-S5) y
se aplica en dos puntos, ambos con cobertura de regresión en
`tests/test_source_quality.py`:

**a) Gate de publicación** (`news_service.update_news_status`, estados protegidos
`approved / scheduled / published`). Se resuelve la `SourceReference` que sostiene
la noticia (por `source_url` o `source_name`) y se bloquea la transición con `409`
cuando:

```text
- La fuente está en source_status blocked/restricted  → bloqueo incondicional.
- La fuente es S5 (rumor/opaca)                        → nunca como hecho.
- La fuente es S3 o S4 sin verificación fuerte         → exige confirmación
  independiente (verified, sin contradicciones, con evidencia E3+ o ≥2 fuentes).
- La fuente es S1 o S2                                 → puede sostener publicación.
```

Verificación fuerte = `VerificationRecord` más reciente en estado `verified`, sin
`contradictions`, con `evidence_level` E3+ **o** dos o más `source_refs`
(corroboración independiente: una fuente débil nunca es confirmación única, §3).

**b) Readiness editorial** (`editorial_readiness_service`). El componente `source`
puntúa por nivel (S1=10, S2=9, S3=7, S4=3, S5/descalificada=0), expone
`source_level` / `trust_level` / `source_status` en `score_payload.components.source`
y marca `publication_block_recommended` cuando la fuente es S5 o está
blocked/restricted. El componente `verification` degrada a revisión humana cuando
hay `contradictions` (conflicto entre fuentes).

**Limitación conocida:** la calidad solo se gradúa cuando existe una
`SourceReference` registrada. Una noticia con solo campos denormalizados
(`source_url`/`source_name`, sin fila en `source_references`) no se bloquea por este
gate — sigue gobernada por el gate de `AuditCheck`. La predicción de precios y el
"rumor como hecho" a nivel de contenido se cubren aparte vía los `risk_flags`
sensibles (`price_prediction_risk`, `rumor_as_fact`) en el scoring de `AgentOutput`.
