import { SectionHeader } from '@/components/ui/section-header'
import { AuditPanel } from '@/components/newsroom/AuditPanel'
import { PipelineAlerts } from '@/components/newsroom/RiskMonitor'

export default function AuditPage() {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Audit"
        subtitle="Verificación de integridad, trazabilidad y requisitos del pipeline"
      />
      <div className="grid gap-4 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <AuditPanel />
        </div>
        <PipelineAlerts />
      </div>
    </div>
  )
}
