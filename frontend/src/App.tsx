import { lazy, Suspense } from 'react'
import { HashRouter, Route, Routes } from 'react-router-dom'
import { AppShell } from '@/components/layout/AppShell'

// Code-splitting por ruta: cada página se carga bajo demanda para reducir
// el bundle inicial (recharts y framer-motion solo se descargan donde se usan).
const CommandCenter = lazy(() => import('@/pages/CommandCenter'))
const NewsIntake = lazy(() => import('@/pages/NewsIntake'))
const NewsDetailPage = lazy(() => import('@/pages/NewsDetailPage'))
const SourceValidation = lazy(() => import('@/pages/SourceValidation'))
const RiskReviewPage = lazy(() => import('@/pages/RiskReviewPage'))
const EditorialDesk = lazy(() => import('@/pages/EditorialDesk'))
const AgentsPage = lazy(() => import('@/pages/AgentsPage'))
const KnowledgeGraphPage = lazy(() => import('@/pages/KnowledgeGraphPage'))
const AuditPage = lazy(() => import('@/pages/AuditPage'))
const MetricsPage = lazy(() => import('@/pages/MetricsPage'))

const CalendarPage = lazy(() =>
  import('@/pages/SecondaryPages').then((m) => ({ default: m.CalendarPage })),
)
const DistributionPage = lazy(() =>
  import('@/pages/SecondaryPages').then((m) => ({ default: m.DistributionPage })),
)
const MarketImpactPage = lazy(() =>
  import('@/pages/SecondaryPages').then((m) => ({ default: m.MarketImpactPage })),
)
const MemoryPage = lazy(() =>
  import('@/pages/SecondaryPages').then((m) => ({ default: m.MemoryPage })),
)
const ScriptsPage = lazy(() =>
  import('@/pages/SecondaryPages').then((m) => ({ default: m.ScriptsPage })),
)
const SettingsPage = lazy(() =>
  import('@/pages/SecondaryPages').then((m) => ({ default: m.SettingsPage })),
)
const SocialClipsPage = lazy(() =>
  import('@/pages/SecondaryPages').then((m) => ({ default: m.SocialClipsPage })),
)

function RouteFallback() {
  return (
    <div className="space-y-3 p-1" aria-busy="true" aria-label="Cargando página">
      <div className="h-7 w-64 animate-pulse rounded-lg bg-white/5" />
      <div className="h-4 w-96 max-w-full animate-pulse rounded bg-white/5" />
      <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        {Array.from({ length: 4 }, (_, i) => (
          <div key={i} className="h-24 animate-pulse rounded-xl bg-white/5" />
        ))}
      </div>
    </div>
  )
}

function App() {
  return (
    <HashRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route
            path="/"
            element={
              <Suspense fallback={<RouteFallback />}>
                <CommandCenter />
              </Suspense>
            }
          />
          <Route
            path="/intake"
            element={
              <Suspense fallback={<RouteFallback />}>
                <NewsIntake />
              </Suspense>
            }
          />
          <Route
            path="/news/:id"
            element={
              <Suspense fallback={<RouteFallback />}>
                <NewsDetailPage />
              </Suspense>
            }
          />
          <Route
            path="/sources"
            element={
              <Suspense fallback={<RouteFallback />}>
                <SourceValidation />
              </Suspense>
            }
          />
          <Route
            path="/impact"
            element={
              <Suspense fallback={<RouteFallback />}>
                <MarketImpactPage />
              </Suspense>
            }
          />
          <Route
            path="/risk"
            element={
              <Suspense fallback={<RouteFallback />}>
                <RiskReviewPage />
              </Suspense>
            }
          />
          <Route
            path="/editorial"
            element={
              <Suspense fallback={<RouteFallback />}>
                <EditorialDesk />
              </Suspense>
            }
          />
          <Route
            path="/scripts"
            element={
              <Suspense fallback={<RouteFallback />}>
                <ScriptsPage />
              </Suspense>
            }
          />
          <Route
            path="/clips"
            element={
              <Suspense fallback={<RouteFallback />}>
                <SocialClipsPage />
              </Suspense>
            }
          />
          <Route
            path="/distribution"
            element={
              <Suspense fallback={<RouteFallback />}>
                <DistributionPage />
              </Suspense>
            }
          />
          <Route
            path="/calendar"
            element={
              <Suspense fallback={<RouteFallback />}>
                <CalendarPage />
              </Suspense>
            }
          />
          <Route
            path="/metrics"
            element={
              <Suspense fallback={<RouteFallback />}>
                <MetricsPage />
              </Suspense>
            }
          />
          <Route
            path="/agents"
            element={
              <Suspense fallback={<RouteFallback />}>
                <AgentsPage />
              </Suspense>
            }
          />
          <Route
            path="/graph"
            element={
              <Suspense fallback={<RouteFallback />}>
                <KnowledgeGraphPage />
              </Suspense>
            }
          />
          <Route
            path="/memory"
            element={
              <Suspense fallback={<RouteFallback />}>
                <MemoryPage />
              </Suspense>
            }
          />
          <Route
            path="/audit"
            element={
              <Suspense fallback={<RouteFallback />}>
                <AuditPage />
              </Suspense>
            }
          />
          <Route
            path="/settings"
            element={
              <Suspense fallback={<RouteFallback />}>
                <SettingsPage />
              </Suspense>
            }
          />
        </Route>
      </Routes>
    </HashRouter>
  )
}

export default App
