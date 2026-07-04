# XMIP — XCripto Media Intelligence Platform

Frontend del **Newsroom OS** de XCripto: una plataforma interna para detectar noticias,
validar fuentes, revisar riesgos, producir contenido, calendarizar publicaciones y
operar agentes editoriales con trazabilidad completa.

## Integración con backend

El frontend consume el **backend XMIP real** (FastAPI, `/api/v1`) para los módulos
operativos principales; los widgets sin endpoint disponible muestran datos de
demostración claramente etiquetados con un badge `DEMO`.

| Módulo               | Fuente de datos                                             |
| -------------------- | ----------------------------------------------------------- |
| Command Center KPIs  | ✅ Real — news, intake signals, executions, audit checks    |
| Últimas noticias     | ✅ Real — `GET /api/v1/news`                                |
| News Intake          | ✅ Real — signals + promote / reject / dedupe / alta manual |
| Source Validation    | ✅ Real — `GET/POST /api/v1/sources`                        |
| Agents               | ✅ Real — `GET /api/v1/agents/executions` por agente        |
| Audit                | ✅ Real — `GET /api/v1/audit/checks`                        |
| Estado del backend   | ✅ Real — `GET /health` con poll cada 30 s (Topbar)         |
| Pipeline board, risk queues, calendario, métricas, notificaciones | ⚠️ DEMO — pendientes de endpoint |

Capa de integración: `src/lib/api.ts` (cliente), `src/lib/api-types.ts` (contratos),
`src/hooks/useApi.ts` (loading/error/refetch + health). Estados async en
`src/components/ui/async-state.tsx`. Mock data aislada en `src/data/mock-*.ts`
con advertencia en el encabezado.

### Variables de entorno

Copia `.env.example` a `.env.local`:

| Variable            | Default                  | Descripción                                                   |
| ------------------- | ------------------------ | ------------------------------------------------------------- |
| `VITE_API_BASE_URL` | `http://127.0.0.1:8000`  | Base del backend XMIP, sin slash final                        |
| `VITE_API_KEY`      | *(vacío)*                | API key de desarrollo/admin interno cuando `AUTH_ENABLED=true` |
| `VITE_ACTOR_ROLE`   | `admin`                  | Rol RBAC enviado como `X-Actor-Role`                          |
| `VITE_ACTOR_ID`     | `local-admin`            | Actor opcional enviado como `X-Actor-Id`                      |

Si el backend está apagado, la UI lo indica ("XMIP sin conexión" en el topbar) y
cada módulo muestra un estado de error con reintento — no pantallas rotas.

## Frontend/Admin Integration

La ruta `#/admin` conecta el panel operativo al contrato de backend de Fase 17.
Usa un cliente separado en `src/lib/xmipAdminApi.ts` para enviar:

- `X-API-Key` desde `VITE_API_KEY`
- `X-Actor-Role` desde `VITE_ACTOR_ROLE`
- `X-Actor-Id` desde `VITE_ACTOR_ID`
- `X-Correlation-ID` generado por request

`VITE_API_KEY` solo es aceptable para desarrollo local o una consola admin interna.
Un frontend público de producción no debe exponer API keys; una fase futura debe
introducir login real con JWT/OAuth/SSO o un backend-for-frontend.

### Endpoints admin consumidos

| UI | Endpoint |
| --- | --- |
| Readiness banner | `GET /ready` |
| Frontend config | `GET /api/v1/admin/frontend/config` |
| Route map | `GET /api/v1/admin/frontend/route-map` |
| Overview cards | `GET /api/v1/admin/dashboard/overview` |
| Newsroom health | `GET /api/v1/admin/dashboard/newsroom-health` |
| Intake queue | `GET /api/v1/admin/intake/queue` |
| Editorial work queue | `GET /api/v1/admin/editorial/work-queue` |
| Blockers | `GET /api/v1/admin/blockers` |
| Readiness board | `GET /api/v1/admin/readiness/board` |
| Task board | `GET /api/v1/admin/tasks/board` |
| Publication board | `GET /api/v1/admin/publications/board` |
| Ownership board | `GET /api/v1/admin/ownership/board` |
| Operational gaps | `GET /api/v1/admin/gaps` |
| Agent runner summary | `GET /api/v1/admin/agent-runner/summary` |
| Connectors summary | `GET /api/v1/admin/connectors/summary` |
| Audit summary | `GET /api/v1/admin/audit/summary` |

### Probar contra backend local

```bash
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

```bash
cd frontend
cp .env.example .env.local
npm run dev
```

Abre `http://localhost:5173/#/admin`.

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
