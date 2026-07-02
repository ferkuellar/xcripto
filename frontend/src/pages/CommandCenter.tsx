import { motion } from 'framer-motion'
import { MetricCard } from '@/components/metrics/MetricCard'
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
import { kpis } from '@/data/mock-news'

export default function CommandCenter() {
  return (
    <div className="space-y-8">
      {/* Hero operativo */}
      <motion.section
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <h1 className="text-xl font-semibold tracking-tight text-ink lg:text-2xl">
          XCripto Newsroom Command Center
        </h1>
        <p className="mt-1 max-w-2xl text-sm text-ink-secondary">
          Detecta, valida, produce y distribuye inteligencia editorial cripto con trazabilidad
          multiagente.
        </p>

        <div className="mt-5 grid grid-cols-2 gap-3 md:grid-cols-3 xl:grid-cols-6">
          {kpis.map((kpi, i) => (
            <MetricCard key={kpi.id} kpi={kpi} index={i} />
          ))}
        </div>
      </motion.section>

      {/* News Pipeline */}
      <section>
        <SectionHeader
          title="News Pipeline"
          subtitle="Flujo editorial de detección a publicación"
        />
        <PipelineBoard />
      </section>

      {/* Agent Activity */}
      <AgentActivity />

      {/* Risk & Verification Monitor */}
      <section>
        <SectionHeader
          title="Risk & Verification Monitor"
          subtitle="Colas de riesgo, verificación y alertas de integridad"
        />
        <div className="grid gap-4 xl:grid-cols-3">
          <RiskQueuePanel />
          <VerificationQueuePanel />
          <PipelineAlerts />
        </div>
      </section>

      {/* Producción + Calendario */}
      <section className="grid gap-4 xl:grid-cols-2">
        <EditorialProduction />
        <CalendarTimeline />
      </section>

      {/* Metrics Overview */}
      <section>
        <SectionHeader
          title="Metrics Overview"
          subtitle="Indicadores operativos del newsroom (datos de demostración)"
        />
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
