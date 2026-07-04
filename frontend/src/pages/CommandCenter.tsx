import { motion } from 'framer-motion'
import { Activity, ArrowRight, FileText, Radar, ShieldAlert } from 'lucide-react'
import { Link } from 'react-router-dom'
import { PipelineBoard } from '@/components/newsroom/PipelineBoard'
import { AgentActivity } from '@/components/agents/AgentActivity'
import {
  PipelineAlerts,
  RiskQueuePanel,
  VerificationQueuePanel,
} from '@/components/newsroom/RiskMonitor'
import { EditorialProduction } from '@/components/newsroom/EditorialProduction'
import { CalendarTimeline } from '@/components/newsroom/CalendarTimeline'
import {
  AgentRunsChart,
  ProductionChart,
  PublicationsByChannelChart,
  RisksByCategoryChart,
} from '@/components/metrics/MetricsCharts'
import { SectionHeader } from '@/components/ui/section-header'
import { Badge } from '@/components/ui/badge'
import { DemoTag, ErrorState } from '@/components/ui/async-state'
import { PriorityBadge } from '@/components/ui/status-badges'
import { useApiQuery, useBackendHealth } from '@/hooks/useApi'
import type {
  AgentExecutionRead,
  AuditCheckRead,
  IntakeSignalRead,
  NewsRead,
} from '@/lib/api-types'
import { countBlockingAudits } from '@/lib/audit-status'
import { cn } from '@/lib/utils'

function LiveKpi({
  icon: Icon,
  label,
  value,
  detail,
  tone = 'text-accent-cyan',
  loading,
}: {
  icon: typeof Activity
  label: string
  value: string | number
  detail: string
  tone?: string
  loading?: boolean
}) {
  return (
    <div className="card-surface p-4">
      <div className="flex items-center justify-between">
        <span className="text-2xs uppercase tracking-wider text-ink-muted">{label}</span>
        <Icon className={cn('h-4 w-4', tone)} />
      </div>
      {loading ? (
        <div className="mt-2 h-7 w-16 animate-pulse rounded bg-white/5" />
      ) : (
        <p className="mt-1 text-2xl font-semibold tabular-nums text-ink">{value}</p>
      )}
      <p className="mt-0.5 text-2xs text-ink-secondary">{detail}</p>
    </div>
  )
}

const newsStatusTone: Record<string, string> = {
  detected: 'blue',
  verified: 'green',
  partially_verified: 'yellow',
  rumor: 'orange',
  rejected: 'red',
  approved: 'green',
  published: 'cyan',
  escalated: 'orange',
}

function formatDate(value: string) {
  return new Date(value).toLocaleString('es-MX', { dateStyle: 'medium', timeStyle: 'short' })
}

export default function CommandCenter() {
  const { status: backendStatus, info } = useBackendHealth()
  const news = useApiQuery<NewsRead[]>('/api/v1/news?limit=200')
  const signals = useApiQuery<IntakeSignalRead[]>('/api/v1/intake/signals?limit=200')
  const executions = useApiQuery<AgentExecutionRead[]>('/api/v1/agents/executions?limit=200')
  const audits = useApiQuery<AuditCheckRead[]>('/api/v1/audit/checks?limit=100')

  const newsItems = news.data ?? []
  const pendingSignals = (signals.data ?? []).filter(
    (s) => !['promoted', 'rejected', 'archived', 'duplicate'].includes(s.signal_status),
  )
  const failedRuns = (executions.data ?? []).filter((e) =>
    ['failed', 'blocked_by_policy'].includes(e.status),
  )
  const blockingAuditCount = countBlockingAudits(audits.data ?? [])

  return (
    <div className="space-y-8">
      {/* Hero operativo — datos reales del backend */}
      <motion.section
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div className="flex flex-wrap items-center gap-3">
          <h1 className="text-xl font-semibold tracking-tight text-ink lg:text-2xl">
            XCripto Newsroom Command Center
          </h1>
          {backendStatus === 'online' && (
            <Badge variant="green">backend online · v{info?.version}</Badge>
          )}
          {backendStatus === 'offline' && <Badge variant="red">backend offline</Badge>}
          {backendStatus === 'checking' && <Badge variant="neutral">verificando backend…</Badge>}
        </div>
        <p className="mt-1 max-w-2xl text-sm text-ink-secondary">
          Detecta, valida, produce y distribuye inteligencia editorial cripto con trazabilidad
          multiagente.
        </p>

        <div className="mt-5 grid grid-cols-2 gap-3 md:grid-cols-4">
          <LiveKpi
            icon={FileText}
            label="Noticias en pipeline"
            value={newsItems.length}
            detail={`${newsItems.filter((n) => n.status === 'verified').length} verificadas · ${newsItems.filter((n) => n.status === 'published').length} publicadas`}
            loading={news.loading}
          />
          <LiveKpi
            icon={Radar}
            label="Señales intake pendientes"
            value={pendingSignals.length}
            detail={`${(signals.data ?? []).filter((s) => ['exact_duplicate', 'probable_duplicate'].includes(s.dedupe_status)).length} duplicadas detectadas`}
            loading={signals.loading}
          />
          <LiveKpi
            icon={Activity}
            label="Ejecuciones de agentes"
            value={(executions.data ?? []).length}
            detail={`${failedRuns.length} fallidas o bloqueadas`}
            tone={failedRuns.length > 0 ? 'text-accent-orange' : 'text-accent-cyan'}
            loading={executions.loading}
          />
          <LiveKpi
            icon={ShieldAlert}
            label="Audit · bloqueos activos"
            value={blockingAuditCount}
            detail={`${(audits.data ?? []).length} checks registrados`}
            tone={blockingAuditCount > 0 ? 'text-accent-red' : 'text-accent-green'}
            loading={audits.loading}
          />
        </div>
      </motion.section>

      {/* Últimas noticias reales */}
      <section>
        <div className="flex items-start justify-between gap-3">
          <SectionHeader
            title="Últimas noticias registradas"
            subtitle="Piezas más recientes del backend XMIP con estado editorial"
          />
          <Link
            to="/news"
            className="inline-flex shrink-0 items-center gap-1 text-xs text-accent-cyan transition-colors hover:text-ink"
          >
            Ver todo el feed
            <ArrowRight className="h-3.5 w-3.5" />
          </Link>
        </div>
        {news.error && <ErrorState error={news.error} onRetry={news.refetch} />}
        {!news.error && newsItems.length === 0 && !news.loading && (
          <p className="card-surface p-5 text-center text-xs text-ink-muted">
            Sin noticias registradas todavía. Promueve señales desde{' '}
            <Link to="/intake" className="text-accent-cyan hover:underline">
              News Intake
            </Link>
            .
          </p>
        )}
        {newsItems.length > 0 && (
          <div className="space-y-2">
            {newsItems.slice(0, 6).map((item) => (
              <Link
                key={item.id}
                to={`/news/${item.id}`}
                className="card-surface flex flex-wrap items-center gap-3 p-3 transition-colors hover:bg-white/[0.03] focus:outline-none focus:ring-1 focus:ring-accent-cyan/50"
              >
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-medium text-ink">{item.title}</p>
                  <p className="truncate text-2xs text-ink-muted">
                    {item.source_name} · {item.category} · {formatDate(item.created_at)}
                  </p>
                </div>
                <PriorityBadge priority={item.priority} compact />
                <Badge variant={(newsStatusTone[item.status] as never) ?? 'neutral'}>
                  {item.status}
                </Badge>
              </Link>
            ))}
          </div>
        )}
      </section>

      {/* News Pipeline (demo) */}
      <section>
        <div className="flex items-center gap-2">
          <SectionHeader
            title="News Pipeline"
            subtitle="Flujo editorial de detección a publicación"
          />
          <DemoTag />
        </div>
        <PipelineBoard />
      </section>

      {/* Agent Activity (demo) */}
      <AgentActivity />

      {/* Risk & Verification Monitor (demo) */}
      <section>
        <div className="flex items-center gap-2">
          <SectionHeader
            title="Risk & Verification Monitor"
            subtitle="Colas de riesgo, verificación y alertas de integridad"
          />
          <DemoTag />
        </div>
        <div className="grid gap-4 xl:grid-cols-3">
          <RiskQueuePanel />
          <VerificationQueuePanel />
          <PipelineAlerts />
        </div>
      </section>

      {/* Producción + Calendario (demo) */}
      <section className="grid gap-4 xl:grid-cols-2">
        <EditorialProduction />
        <CalendarTimeline />
      </section>

      {/* Metrics Overview (demo) */}
      <section>
        <div className="flex items-center gap-2">
          <SectionHeader
            title="Metrics Overview"
            subtitle="Indicadores operativos del newsroom"
          />
          <DemoTag />
        </div>
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <ProductionChart />
          <PublicationsByChannelChart />
          <RisksByCategoryChart />
          <AgentRunsChart />
        </div>
      </section>
    </div>
  )
}
