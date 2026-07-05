# Source Connector Registry

Reputación editorial inicial de las fuentes de conector. Implementado en
`app/core/source_registry.py`. `trust_level` mapea a la política S1-S5
(`SOURCE_QUALITY_POLICY.md` §4): T0=S1, T1=S2, T2=S3, T3=S4.

Regla P9.1: **todo feed RSS falla cerrado si no existe como proveedor explícito en
`FEED_PROVIDER_REGISTRY`**. `RSS_CONNECTOR_ALLOWED_DOMAINS` solo habilita proveedores ya
registrados; no basta para aceptar un dominio arbitrario. `source_name` y `trust_level`
siempre salen del registro del proveedor del feed, nunca del dominio del item.

| Source | Feed domains | Item domains | Connector Type | Initial Quality | Trust Rationale | Allowed? | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CoinDesk | coindesk.com | coindesk.com | RSS | **S2** (T1) | Medio cripto establecido con proceso editorial | Sí | RSS público |
| The Block | theblock.co | theblock.co | RSS | **S2** (T1) | Cripto institucional con proceso editorial | Sí | RSS público |
| Cointelegraph | cointelegraph.com | cointelegraph.com | RSS | **S3** (T2) | Medio reconocido; S3 hasta afinar política | Sí | RSS público |
| Decrypt | decrypt.co | decrypt.co | RSS | **S3** (T2) | Medio reconocido; S3 hasta afinar política | Sí | RSS público |
| (no registrado como proveedor) | * | * | RSS | rechazado | No hay identidad/trust explícito | No | Fail-closed antes de fetch |
| (item fuera del proveedor) | registrado | dominio externo | RSS | rechazado | Evita source spoofing | No | Rechazado + auditado |

## Cómo cambiar la reputación
Editar `FEED_PROVIDER_REGISTRY` y, si aplica, `SOURCE_REGISTRY` en
`app/core/source_registry.py` **con** justificación aquí. No se hardcodea reputación sin
este documento. Nunca marcar una fuente social como S1/S2.

Para RSS, actualizar también `FEED_PROVIDER_REGISTRY`: `feed_domains` define de dónde se
puede descargar el feed; `item_domains` define qué links de items son aceptables para ese
proveedor. Un item de CoinDesk que apunte a Cointelegraph, por ejemplo, se rechaza en vez
de heredar reputación del dominio del item.

## SSRF y XML
- `feed_url` se valida antes de fetch: solo `http`/`https`, host en proveedor permitido,
  DNS público/global, sin localhost, private, loopback, link-local, metadata, reserved,
  multicast ni unspecified.
- Los redirects se validan antes de seguirlos y se revalida la URL final.
- RSS con `<!DOCTYPE` o `<!ENTITY` se rechaza antes de `ElementTree.fromstring`.

## SourceReference
Las fuentes RSS se deduplican por `source_type + source_url` canónica, no por
`source_name`. Dos fuentes con el mismo nombre pero URL distinta no colapsan; la misma URL
con `www` o slash final sí deduplica.

## Fuentes explícitamente excluidas de P9
X/Twitter, Telegram, Discord, foros, agregadores anónimos, y cualquier fuente que viole
ToS o requiera scraping de páginas completas.
