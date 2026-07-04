# XMIP Source Quality Policy

| Campo | Valor |
| --- | --- |
| Proyecto | ORION / XCripto / XMIP |
| Tipo | Política editorial operativa |
| Estado | Draft implementable (Hard Phase P0) |
| Última actualización | 2026-07-03 |
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
