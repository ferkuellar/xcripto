# Connector Runbook

Operación del rollout de conectores reales (P9). El conector corre **in-process** contra
la base configurada (`DATABASE_URL`); nunca publica.

## 1. Preflight
- [ ] Backend + PostgreSQL arriba y `/ready` verde.
- [ ] Fuente permitida y su feed RSS conocido (ToS: solo lectura de RSS público).
- [ ] Feed registrado en `app/core/source_registry.py` (`FEED_PROVIDER_REGISTRY`).
- [ ] Confirmar `CONNECTOR_AUTO_PROMOTE=false`.

## 2. Enable connector
Setear (solo para la corrida controlada; no commitear):
```bash
export CONNECTORS_ENABLED=true
export RSS_CONNECTOR_ENABLED=true
export RSS_CONNECTOR_ALLOWED_DOMAINS=coindesk.com,cointelegraph.com,decrypt.co,theblock.co
export RSS_CONNECTOR_MAX_ITEMS=20
```

## 3. Run manually
```bash
cd backend
# feed real (necesita red + dominio permitido):
python scripts/run_connector.py --connector rss --feed-url https://www.coindesk.com/feed --max-items 5
# fixture local determinista (sin red):
python scripts/run_connector.py --connector rss --feed-file sample_feed.xml --max-items 5
```
Contra el stack Docker desde el host, apuntar a la DB mapeada:
```bash
DATABASE_URL=postgresql+asyncpg://xmip:xmip@127.0.0.1:55432/xmip \
CONNECTORS_ENABLED=true RSS_CONNECTOR_ENABLED=true \
RSS_CONNECTOR_ALLOWED_DOMAINS=coindesk.com \
python scripts/run_connector.py --connector rss --feed-file sample_feed.xml --max-items 5
```
O dentro del contenedor: `docker compose exec api python scripts/run_connector.py ...`.

## 4. Validate intake
```bash
curl "http://127.0.0.1:8010/api/v1/intake/signals?signal_type=rss&limit=20" \
  -H "X-API-Key: dev-secret" -H "X-Actor-Role: admin"
```
Confirmar `dedupe_status` (unique / exact_duplicate) y que NO hay noticias publicadas.

## 5. Validate audit
```bash
curl "http://127.0.0.1:8010/api/v1/operational-audit/events?event_type=connector_event&limit=50" \
  -H "X-API-Key: dev-secret" -H "X-Actor-Role: admin"
```
Ver `connector.run.started/completed`, `connector.item.ingested/duplicate/rejected`.

## 6. Validate source quality
```bash
curl "http://127.0.0.1:8010/api/v1/sources?limit=20" \
  -H "X-API-Key: dev-secret" -H "X-Actor-Role: admin"
```
Confirmar `trust_level` según el proveedor del feed registrado (CoinDesk=T1/S2,
Cointelegraph=T2/S3, etc.). No aceptar reputación derivada de links arbitrarios dentro
del item.

## 6.1 Validate security gates
- Feed URL fuera del registry → rechazado antes de fetch.
- DNS hacia localhost/private/link-local/metadata/reserved/multicast/unspecified →
  rechazado antes de fetch.
- Redirect hacia host no permitido o IP bloqueada → rechazado.
- RSS con `<!DOCTYPE` o `<!ENTITY` → rechazado antes de parsear.
- Item link fuera de los hosts permitidos del proveedor → rechazado y auditado.

## 7. Disable connector
```bash
export CONNECTORS_ENABLED=false   # kill switch — detiene todo
```

## 8. Rollback
- Kill switch (`CONNECTORS_ENABLED=false`) + detener el runner.
- Revertir el PR si el pipeline se rompe.
- Limpiar solo datos sintéticos (`IntakeSignal` de prueba) si se confirma.
- Rotar credenciales si hubo exposición (no aplica: RSS no usa secretos).

## 9. Troubleshooting
- **disabled** en el resultado → faltan `CONNECTORS_ENABLED`/`RSS_CONNECTOR_ENABLED`.
- **rejected_count alto** → dominio no está en `RSS_CONNECTOR_ALLOWED_DOMAINS`.
- **feed_url does not match an allowed feed provider** → falta registry explícito o el
  dominio no está habilitado.
- **blocked address** → DNS/redirect resolvió a IP no pública o de metadata.
- **DTD/ENTITY** → el XML fue bloqueado antes de parsear.
- **fetch/parse error** → feed inválido o red; queda auditado como `connector.item.error`,
  el conector no crashea.
- **duplicate_count alto** → el feed no cambió desde la última corrida (dedup funcionando).
