# Real Connector Rollout Plan

| Campo | Valor |
| --- | --- |
| Fase | P9 — Real Connector Rollout |
| Estado | Implementado, OFF por defecto (kill switches) |
| Base | main `789d5ab` |
| Fecha | 2026-07-05 |

## 1. Objetivo
Activar de forma controlada el primer conector real de fuentes externas (RSS de medios
cripto reconocidos), priorizando **control** sobre volumen: límites, allowed domains,
deduplicación, source quality, auditoría y kill switch. **No publica** — el ingest crea
`IntakeSignal`, no noticias publicadas.

## 2. Fuentes permitidas
Vía `RSS_CONNECTOR_ALLOWED_DOMAINS` (CSV). Iniciales (RSS público, lectura permitida):
`coindesk.com`, `cointelegraph.com`, `decrypt.co`, `theblock.co`. Calidad inicial en
`SOURCE_CONNECTOR_REGISTRY.md` (S2/S3). P9.1 falla cerrado: un dominio no registrado como
proveedor explícito no se ingesta aunque aparezca en configuración.

## 3. Fuentes excluidas
Social (X/Twitter, Telegram, Discord) — **fuera de P9**. Scraping de páginas completas,
paywalls, y cualquier fuente prohibida por ToS. Market data se trata como referencia, no
como noticia editorial (no incluido en este rollout inicial).

## 4. Frecuencia de ingest
`CONNECTOR_RUN_MODE=manual` — ejecución manual vía `scripts/run_connector.py`. No hay
scheduler automático en P9 (se agrega después, con rate limiting explícito).

## 5. Límites por ejecución
`RSS_CONNECTOR_MAX_ITEMS` (default 20), `RSS_CONNECTOR_TIMEOUT_SECONDS` (10), cap de
cuerpo `MAX_FETCH_BYTES=2MB`. `max_items` por corrida se acota al máximo configurado.

## 6. Normalización
Cada item → `NormalizedItem` (external_id, title, summary, url, source_domain,
published_at, raw_payload_hash). Se persiste como `IntakeSignal` (`signal_type=rss`,
`adapter_name=rss_connector`), sin guardar HTML completo.

## 7. Deduplicación
Reutiliza el pipeline de intake (`create_intake_signal` → `apply_deduplication` por
content_hash). Items repetidos quedan marcados `exact_duplicate`/`probable_duplicate` y se
cuentan como duplicados, no como aceptados.

## 8. Source quality mapping
`app/core/source_registry.py` mapea proveedor de feed → `source_name` y `trust_level`
(T0-T3 = S1-S4). El feed debe pertenecer a un proveedor registrado y los links de items
deben pertenecer a los hosts permitidos por ese proveedor. `source_name` y `trust_level`
nunca se derivan del dominio arbitrario del item. Se crea/prepara una `SourceReference`
por URL canónica de fuente (`source_type + source_url`), no por nombre.

## 8.1 Seguridad de red y XML
Antes de hacer fetch se valida `feed_url`: esquema `http`/`https`, proveedor permitido y
DNS resuelto a IP pública/global. Se bloquean localhost, loopback, privadas, link-local,
metadata (`169.254.169.254`), reserved, multicast y unspecified. Los redirects se validan
antes de seguirse y se revalida la URL final. Feeds con `<!DOCTYPE` o `<!ENTITY` se
rechazan antes de parsear XML.

## 9. Operational audit
Eventos `connector_event`: `connector.run.started`, `connector.run.completed`,
`connector.item.ingested`, `connector.item.duplicate`, `connector.item.rejected`,
`connector.item.error`. Metadata: connector_name, source_domain, url, trust_level,
result, reason, correlation_id, actor_role=system. Sin API keys/tokens.

## 10. Admin visibility
Cada corrida crea un `IntakeAdapterRun` (`adapter_type=rss`) con counts y status →
visible por los read models de intake/adapter-runs existentes. Los eventos son visibles
en `/admin/audit/summary` y `/operational-audit/events`. Frontend sin rediseño.

## 11. Kill switch
`CONNECTORS_ENABLED=false` (default) detiene todo. `RSS_CONNECTOR_ENABLED=false` detiene
RSS. `RSS_CONNECTOR_ALLOWED_DOMAINS` vacío rechaza todo. `max_items=0` no ingesta.
`CONNECTOR_AUTO_PROMOTE=true` es inválido por configuración: P9 nunca promueve señales.

## 12. Rollback
Desactivar las env vars (kill switch), detener el runner manual, revertir el PR si rompe
el pipeline, limpiar solo datos sintéticos si se confirma, rotar credenciales si hubo
exposición. Ver `CONNECTOR_RUNBOOK.md` §8.

## 13. GO / NO-GO
**GO** para rollout controlado en staging/local con conectores OFF por defecto y
activación manual acotada. **NO** activar en producción pública ni con auto-promote.
