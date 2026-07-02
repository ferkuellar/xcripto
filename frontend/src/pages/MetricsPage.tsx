import { SectionHeader } from '@/components/ui/section-header'
import {
  AgentRunsChart,
  EngagementChart,
  ProductionChart,
  PublicationsByChannelChart,
  RisksByCategoryChart,
  VerificationTimeChart,
} from '@/components/metrics/MetricsCharts'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { incidentMetrics, qualityMetrics } from '@/data/mock-metrics'

function StatGrid({ items }: { items: { label: string; value: string }[] }) {
  return (
    <div className="grid gap-2 sm:grid-cols-2">
      {items.map((m) => (
        <div key={m.label} className="rounded-lg border border-line bg-surface-elevated/60 px-3 py-2.5">
          <p className="text-lg font-semibold text-ink">{m.value}</p>
          <p className="mt-0.5 text-2xs text-ink-secondary">{m.label}</p>
        </div>
      ))}
    </div>
  )
}

export default function MetricsPage() {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Metrics"
        subtitle="Dashboard de métricas operativas, editoriales y de distribución (datos de demostración)"
      />

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <ProductionChart />
        <PublicationsByChannelChart />
        <RisksByCategoryChart />
        <AgentRunsChart />
        <VerificationTimeChart />
        <EngagementChart />
      </div>

      <div className="grid gap-4 xl:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Métricas de calidad</CardTitle>
            <CardDescription>Trazabilidad y estándares editoriales</CardDescription>
          </CardHeader>
          <CardContent>
            <StatGrid items={qualityMetrics} />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Métricas de incidentes</CardTitle>
            <CardDescription>Gestión de incidentes editoriales</CardDescription>
          </CardHeader>
          <CardContent>
            <StatGrid items={incidentMetrics} />
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
