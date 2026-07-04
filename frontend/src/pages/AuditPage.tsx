import { SectionHeader } from '@/components/ui/section-header'
import { Badge, type BadgeProps } from '@/components/ui/badge'
import { DemoTag, EmptyState, ErrorState, SkeletonRows } from '@/components/ui/async-state'
import { PipelineAlerts } from '@/components/newsroom/RiskMonitor'
import { useApiQuery } from '@/hooks/useApi'
import type { AuditCheckRead } from '@/lib/api-types'

type BadgeVariant = NonNullable<BadgeProps['variant']>

const auditStatusMap: Record<AuditCheckRead['audit_status'], BadgeVariant> = {
  passed: 'green',
  passed_with_warnings: 'yellow',
  warning: 'yellow',
  pending: 'blue',
  failed: 'red',
  blocked: 'red',
}

const severityMap: Record<AuditCheckRead['severity'], BadgeVariant> = {
  low: 'green',
  medium: 'yellow',
  high: 'orange',
  critical: 'red',
}

function formatDate(value: string) {
  return new Date(value).toLocaleString('es-MX', { dateStyle: 'medium', timeStyle: 'short' })
}

export default function AuditPage() {
  const { data, loading, error, refetch } = useApiQuery<AuditCheckRead[]>(
    '/api/v1/audit/checks?limit=100',
  )

  return (
    <div className="space-y-6">
      <SectionHeader
        title="Audit"
        subtitle="Audit checks reales del backend XMIP · trazabilidad, bloqueos y readiness"
      />

      <div className="grid gap-4 xl:grid-cols-3">
        <div className="space-y-2 xl:col-span-2">
          {loading && <SkeletonRows rows={5} />}
          {error && <ErrorState error={error} onRetry={refetch} />}
          {!loading && !error && (data?.length ?? 0) === 0 && (
            <EmptyState
              title="Sin audit checks registrados"
              detail="Los audit checks aparecerán aquí cuando AuditAgent o el pipeline los registre (POST /api/v1/audit/checks)."
            />
          )}
          {!loading &&
            !error &&
            data?.map((check) => (
              <div key={check.id} className="card-surface p-3">
                <div className="flex flex-wrap items-center gap-2">
                  <Badge variant={auditStatusMap[check.audit_status] ?? 'neutral'}>
                    {check.audit_status}
                  </Badge>
                  <Badge variant={severityMap[check.severity] ?? 'neutral'}>
                    {check.severity}
                  </Badge>
                  <span className="font-mono text-2xs text-ink-muted">
                    {check.entity_type} · {check.entity_id.slice(0, 12)}
                  </span>
                  <span className="ml-auto text-2xs text-ink-muted">
                    {formatDate(check.created_at)}
                  </span>
                </div>
                {check.decision_recommendation && (
                  <p className="mt-2 text-xs text-ink-secondary">
                    {check.decision_recommendation}
                  </p>
                )}
                <div className="mt-2 flex flex-wrap items-center gap-1.5">
                  {check.publication_block_recommended && (
                    <Badge variant="red">bloqueo de publicación recomendado</Badge>
                  )}
                  {check.ready_to_advance ? (
                    <Badge variant="green">ready to advance</Badge>
                  ) : (
                    <Badge variant="yellow">no listo para avanzar</Badge>
                  )}
                  {check.missing_requirements.map((req) => (
                    <Badge key={req} variant="orange">
                      falta: {req}
                    </Badge>
                  ))}
                  {check.audit_flags.map((flag) => (
                    <Badge key={flag} variant="neutral">
                      {flag}
                    </Badge>
                  ))}
                </div>
                {check.correlation_id && (
                  <p className="mt-2 font-mono text-2xs text-ink-muted">
                    corr: {check.correlation_id}
                  </p>
                )}
              </div>
            ))}
        </div>
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <DemoTag />
            <span className="text-2xs text-ink-muted">
              Alertas de integridad — pendiente de endpoint
            </span>
          </div>
          <PipelineAlerts />
        </div>
      </div>
    </div>
  )
}
