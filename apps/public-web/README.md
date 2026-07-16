# XCripto — Public Web (`apps/public-web`)

Public news site for **xcripto.com.mx**. Next.js (App Router) + Tailwind, **SSR** for SEO.

> Separate app from the XMIP admin console in `../../frontend` (do not mix). This app is
> public-only and consumes the backend public API (`/api/v1/public/*`) with no auth.

## Routes

| Path | Descripción |
|---|---|
| `/` | Home / portada |
| `/news` | Lista de noticias (paginada) |
| `/news/[slug]` | Artículo (SSR, SEO completo, JSON-LD) |
| `/categorias` | Índice de categorías |
| `/categoria/[category]` | Noticias por categoría |
| `/buscar?q=` | Búsqueda |
| `/acerca` | Acerca de |
| `/autor/[author]` | Autor (fallback, noindex — sin contrato de autor todavía) |
| `/sitemap.xml` | Sitemap (nativo) |
| `/robots.txt` | Robots |
| `/rss.xml` | RSS (proxy del feed del backend) |

## Contratos backend consumidos

```
GET /api/v1/public/news?q=&category=&limit=&offset=
GET /api/v1/public/news/{slug}          # artículo con body (requiere content piece approved)
GET /api/v1/public/categories
GET /api/v1/public/search?q=
GET /api/v1/public/rss.xml
GET /sitemap.xml                        # (el sitio también genera el suyo propio)
```

## Variables de entorno

Ver `.env.example`:

- `XCRIPTO_API_URL` — base del backend público (server-side). Production: `https://api.xcripto.com.mx`.
- `NEXT_PUBLIC_SITE_URL` — base pública del sitio (metadataBase/sitemap). Production: `https://xcripto.com.mx`.
- `NEXT_PUBLIC_SITE_NAME` — marca. Default `XCripto`.

## Desarrollo

```bash
cd apps/public-web
cp .env.example .env.local   # ajustar XCRIPTO_API_URL si el backend no está en :8000
npm install
npm run dev        # http://localhost:3000
npm run build      # build de producción
npm run lint
npm run typecheck
```

## Notas

- Todos los fetches son server-side y degradan a estado vacío (no 500) si el backend falla.
- `og_image` / `cover_image_url` son `null` en el contrato actual → se usa un placeholder
  editorial por categoría (fallback). Cuando el backend entregue portadas, se usan directo.
- La página de artículo hace `notFound()` si el item no tiene content piece `approved`.
