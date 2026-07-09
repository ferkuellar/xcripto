# Public Site — Backend Contract Gap Report (para Codex)

> Diagnóstico read-only del backend para construir el **sitio público de noticias**
> (xcripto.com): Home, Noticias, **Página de artículo**, Categorías, Buscar, Autor.
> No se tocó backend. No se construyó frontend público todavía.
> Fecha: 2026-07-09. Base: `main` (post Fase 20, commit `ed62d8e`).

---

## TL;DR — Veredicto

**NO alcanza todavía para una página de artículo pública real.** El cuerpo del artículo
(`body`) **sí existe** en el backend (`ContentPiece.body`), pero **no hay un contrato público de
"artículo publicado"** listo para SEO. Hoy, para armar un artículo habría que:

1. leer 2–3 recursos internos (`news` + `content-pieces` + `publication-records`) y unirlos en el cliente,
2. consumir endpoints editoriales que **exponen borradores y campos internos** (verification_status,
   risk_level, human_review_required, owner, disclaimer_required), sin filtro de "publicado",
3. **inventar** slug, autor, canonical y campos SEO en el frontend (prohibido por las reglas del MVP).

Por eso: **me detengo y reporto el gap a Codex** (según la instrucción). Se necesita un
**read model público de artículo publicado** antes de construir la página de artículo.

---

## 1. Qué SÍ existe hoy (contratos reales)

Los GET de lectura son **públicos** (sin API key; auth solo en escrituras):

- `GET /api/v1/news` (lista, `X-Total-Count`, filtros `q`, `status`, `priority`, `limit`, `offset`) — público
- `GET /api/v1/news/{id}` — público
- `GET /api/v1/news/{id}/content-pieces` — público (aquí vive `body`)
- `GET /api/v1/content-pieces/{id}` — público
- `GET /api/v1/news/{id}/publication-records` — público (aquí viven `published_at` y `published_url`)

### Read models actuales

| Recurso | Campos relevantes |
|---|---|
| `NewsRead` | id, title, summary, **category**, priority, source_url, source_name, status, created_at, updated_at |
| `ContentPieceRead` | id, news_item_id, content_type, title, summary, **body**, status, category, priority, verification_status, risk_level, source_refs, disclaimer_required, human_review_required, **owner**, created_at, updated_at |
| `PublicationRecordRead` | id, content_piece_id, news_item_id, channel, publication_status, **published_url**, external_id, **published_at**, owner, created_at, updated_at |

---

## 2. Checklist de artículo público — campo por campo

| Campo requerido | ¿Existe? | Dónde / observación |
|---|---|---|
| **title** | ✅ | `NewsRead.title` / `ContentPieceRead.title` |
| **summary** | ✅ | `NewsRead.summary` / `ContentPieceRead.summary` |
| **body / content** | ⚠️ Parcial | `ContentPieceRead.body` existe, pero **solo vía endpoint editorial** que no filtra por publicado y expone campos internos. **No hay read model público de artículo.** |
| **category** | ⚠️ Parcial | Existe como **string libre** en news/content. **No hay catálogo/endpoint de categorías** (sin slug, sin conteo, sin listado). |
| **author** | ❌ | No hay entidad autor ni byline público. Solo `owner` (dueño editorial interno), no apto como autor público. |
| **published_at** | ⚠️ Parcial | Existe en `PublicationRecordRead.published_at`, pero es por-canal y separado; no está en un read model de artículo. `NewsRead` solo tiene `created_at`/`updated_at`. |
| **canonical_url** | ❌ | `source_url` = origen **externo** (fuente). `published_url` = URL del canal de distribución. Ninguno es el canonical del artículo en xcripto.com. |
| **slug** | ❌ | Solo `id` (UUID). Sin slug → URLs no limpias, malas para SEO. |
| **SEO (meta_title, meta_description, og_image)** | ❌ | `summary` podría servir de description, pero no hay `og_image`, `seo_title` ni campos SEO dedicados. |
| **estado "publicado" filtrable** | ⚠️ Parcial | `NEWS_STATUSES` incluye `published` (→ `GET /news?status=published`), pero `GET /news/{id}/content-pieces` **no filtra** por publicado; devuelve borradores también. |
| **RSS / sitemap (output)** | ❌ | El conector RSS es de **ingesta** (leer fuentes externas), no de salida. Sin feed/sitemap público. |

---

## 3. Gap concreto a implementar por Codex (propuesta)

Se necesita un **contrato público de solo-lectura, solo-publicado**, que no filtre datos editoriales
internos. Propuesta mínima (nombres orientativos):

### 3.1 Read model `PublicArticleRead`
```
id
slug                     # NUEVO — URL limpia estable (ej. "sec-charges-crypto-firm")
title
dek / summary            # bajada
body                     # markdown o HTML sanitizado (desde ContentPiece.body publicado)
category { name, slug }  # categoría con slug
author { name, slug }    # NUEVO — byline público (mapear desde owner o un catálogo de autores)
published_at             # desde PublicationRecord.published_at
updated_at
canonical_url            # NUEVO — canonical del artículo en xcripto.com
seo { meta_title, meta_description, og_image_url }   # NUEVO
source { name, url }     # atribución (source_name / source_url)
reading_time_min?        # opcional
```

### 3.2 Endpoints públicos nuevos (sugeridos)
```
GET /api/v1/public/articles?category=&q=&limit=&offset=   # SOLO published; devuelve PublicArticleRead[]
GET /api/v1/public/articles/{slug}                        # por slug; SOLO published; 404 si no publicado
GET /api/v1/public/categories                             # catálogo: [{ name, slug, count }]
GET /api/v1/public/authors/{slug}?limit=&offset=          # autor + sus artículos (si habrá páginas de autor)
GET /rss.xml  ·  GET /sitemap.xml                          # salida (backend o frontend)
```

### 3.3 Reglas de exposición
- Excluir del contrato público: `verification_status`, `risk_level`, `human_review_required`,
  `disclaimer_required`, `owner`, `correlation_id` y cualquier campo del pipeline editorial.
- Solo exponer artículos con estado publicado (news `published` **y** content piece publicado).
- `body` sanitizado / en formato renderizable (markdown o HTML seguro).

### 3.4 Mínimo indispensable para desbloquear la **página de artículo**
`slug`, `body` publicado, `published_at`, `canonical_url`, y `author` (aunque sea derivado).
Categorías y RSS/sitemap pueden ir en una segunda iteración (la Home/lista pueden arrancar con
`GET /news?status=published` + category string mientras tanto).

---

## 4. Decisión de arquitectura frontend (acordada)

- **Mantener `frontend/`** como **consola admin XMIP** (React+Vite, hash-routing, sin cambios).
- **Crear app separada** para el sitio público en **`apps/public-web`** (o `newsroom/`), **sin mezclar**
  el hash-routing admin con el sitio SEO.
- El sitio público requiere **SSR/SSG** (Next.js / Astro / Remix) para SEO real (metadata por artículo,
  OpenGraph, JSON-LD Article, canonical, sitemap). Un SPA con hash-routing **no sirve** para SEO.
- La app pública consumirá **solo** los contratos públicos (idealmente los nuevos de §3), sin auth,
  con `VITE`/`NEXT_PUBLIC` base URL al backend.

---

## 5. Estado / siguiente paso

- **Bloqueante para la página de artículo:** falta el read model público de artículo publicado (§3).
- **No bloqueante para empezar** Home + Lista + Buscar en modo "titulares" (title/summary/category/link)
  usando `GET /news?status=published` — pero **sin cuerpo de artículo** hasta que Codex entregue §3.4.
- **Acción:** Codex implementa el contrato público §3; luego se scaffolda `apps/public-web` (SSR/SSG)
  y se conecta. No se inventan mocks permanentes.
