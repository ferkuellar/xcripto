# XMIP — XCripto Media Intelligence Platform

Frontend del **Newsroom OS** de XCripto: una plataforma interna para detectar noticias,
validar fuentes, revisar riesgos, producir contenido, calendarizar publicaciones y
operar agentes editoriales con trazabilidad completa.

> Todos los datos de esta versión son **mock data ficticia de demostración**.
> No hay backend, autenticación ni llamadas a APIs externas.

## Stack

- React 19 + TypeScript + Vite
- Tailwind CSS 3
- Componentes estilo shadcn/ui (`src/components/ui`, con `cva` + `tailwind-merge`)
- lucide-react (iconos)
- framer-motion (animaciones)
- Recharts (gráficas)
- react-router-dom (navegación con HashRouter)

## Instalación y ejecución

```bash
cd frontend
npm install
npm run dev      # servidor de desarrollo en http://localhost:5173
npm run build    # build de producción (tsc + vite build)
npm run preview  # sirve el build de producción
```

## Estructura

```txt
src/
  components/
    layout/      AppShell, Sidebar, Topbar
    newsroom/    PipelineBoard, NewsCard, RiskMonitor, CalendarTimeline,
                 EditorialProduction, AuditPanel, KnowledgeGraphPreview
    agents/      AgentCard, AgentActivity
    metrics/     MetricCard, MetricsCharts, chart-theme
    ui/          button, card, badge, input, progress, status-badges,
                 section-header (primitivos estilo shadcn)
  data/          types.ts + mock-news, mock-agents, mock-metrics, mock-operations
  lib/           utils (cn), navigation
  pages/         CommandCenter, NewsIntake, SourceValidation, RiskReviewPage,
                 EditorialDesk, AgentsPage, KnowledgeGraphPage, AuditPage,
                 MetricsPage, SecondaryPages (Market Impact, Scripts, Social
                 Clips, Distribution, Calendar, Memory, Settings)
```

## Sobre shadcn/ui

Los primitivos de `src/components/ui` siguen las convenciones de shadcn/ui
(`cva`, `cn`, forwardRef, variantes), por lo que puedes agregar componentes
oficiales cuando lo necesites:

```bash
npx shadcn@latest init
npx shadcn@latest add dialog dropdown-menu tabs
```

El alias `@/*` ya está configurado en `vite.config.ts` y `tsconfig.app.json`.

## Sistema visual

Tokens definidos en `tailwind.config.js`:

- Fondo `#05070D`, superficies `#0B1020` / `#111827`, bordes `rgba(255,255,255,0.08)`
- Acentos: cyan `#00E5FF`, verde `#22C55E`, amarillo `#FACC15`, rojo `#EF4444`, púrpura `#8B5CF6`
- Paleta de series para gráficas (`chart.1`–`chart.5`): orden fijo, validada para
  separación por daltonismo y contraste ≥3:1 sobre `#0B1020`. No reordenar.
- Los colores de estado (riesgo/verificación) siempre van acompañados de icono y
  etiqueta — nunca color solo.

## Reglas editoriales del producto

XMIP mide relevancia editorial y trazabilidad. No genera señales de compra/venta,
predicciones de precio ni promesas de trading.
