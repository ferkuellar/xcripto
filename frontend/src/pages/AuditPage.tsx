import { useCallback } from 'react'
import { AlertTriangle, KeyRound, RefreshCw, ShieldCheck } from 'lucide-react'
import { SectionHeader } from '@/components/ui/section-header'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { DemoTag, EmptyState, ErrorState, SkeletonRows } from '@/components/ui/async-state'
import { PipelineAlerts } from '@/components/newsroom/RiskMonitor'
import { useApiQuery } from '@/hooks/useApi'
import { useXmipAdminQuery } from '@/hooks/useXmipAdmin'
import { adminApi } from '@/services/adminApi'
import { XmipAdminApiError } from '@/lib/xmipAdminApi'
import type { AuditCheckRead } from '@/lib/api-types'
import type { OperationalAuditEvent } from '@/types/xmip'
import { type BadgeVariant, auditStatusVariant } from '@/lib/audit-status'

const severityMap: Record<AuditCheckRead['severity'], BadgeVariant> = {
  low: 'green',
  medium: 'yellow',
  high: 'orange',
  critical: 'red',
}

function outcomeTone(outcome: string | null | undefined): BadgeVariant {
  const value = (outcome ?? '').toLowerCase()
  if (['success', 'allow', 'allowed', 'ok', 'passed', 'completed'].includes(value)) return 'green'
  if (['failure', 'failed', 'denied', 'blocked', 'rejected', 'error'].includes(value)) return 'red'
  if (['warning', 'partial', 'pending', 'flagged'].includes(value)) return 'yellow'
  return 'neutral'
}

function formatDate(value: string) {
  return new Date(value).toLocaleString('es-MX', { dateStyle: 'medium', timeStyle: 'short' })
}

export default function AuditPage() {
  const { data, loading, error, refetch } = useApiQuery<AuditCheckRead[]>(
    '/api/v1/audit/checks?limit=100',
  )

  return (
    <div className="space-y-8">
      {/* ── Audit Checks (editorial, público: /api/v1/audit/checks) ── */}
      <div className="space-y-6">
        <SectionHeader
          title="Audit Checks"
          subtitle="Checks editoriales por entidad · GET /api/v1/audit/checks (público) · bloqueos y readiness"
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
                    <Badge variant={auditStatusVariant[check.audit_status] ?? 'neutral'}>
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

      {/* ── Operational Audit (RBAC: /api/v1/operational-audit/events) ── */}
      <OperationalAuditSection />
    </div>
  )
}

/**
 * Registro de auditoría operacional. A diferencia de los Audit Checks (editorial,
 * público), este endpoint está protegido por RBAC: exige sesión HttpOnly con
 * permiso operational_audit.read. Se consume por el cliente admin autenticado.
 */
function OperationalAuditSection() {
  const query = useXmipAdminQuery(
    useCallback((signal) => adminApi.getOperationalAuditEvents(signal), []),
  )
  const events = query.data ?? []

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <SectionHeader
          title="Operational Audit"
          subtitle="Registro RBAC de eventos operativos · GET /api/v1/operational-audit/events (sesión HttpOnly)"
        />
        <div className="flex items-center gap-2">
          <Badge variant="cyan">
            <ShieldCheck className="h-3 w-3" />
            protegido
          </Badge>
          <Button size="sm" variant="secondary" onClick={query.refetch} disabled={query.loading}>
            <RefreshCw className={query.loading ? 'h-3.5 w-3.5 animate-spin' : 'h-3.5 w-3.5'} />
            Actualizar
          </Button>
        </div>
      </div>

      {query.loading && <SkeletonRows rows={4} />}
      {!query.loading && query.error && (
        <OperationalAuditError error={query.error} onRetry={query.refetch} />
      )}
      {!query.loading && !query.error && events.length === 0 && (
        <EmptyState
          title="Sin eventos de auditoría operacional"
          detail="El backend respondió correctamente (auth OK) pero aún no hay eventos registrados para el actor y periodo actuales."
        />
      )}

      {!query.loading && !query.error && events.length > 0 && (
        <div className="space-y-2">
          {events.map((event) => (
            <OperationalAuditRow key={event.id} event={event} />
          ))}
        </div>
      )}
    </div>
  )
}

function OperationalAuditRow({ event }: { event: OperationalAuditEvent }) {
  return (
    <div className="card-surface p-3">
      <div className="flex flex-wrap items-center gap-2">
        <Badge variant="blue">{event.event_type}</Badge>
        {event.action && <Badge variant="neutral">{event.action}</Badge>}
        <Badge variant={outcomeTone(event.outcome)}>{event.outcome}</Badge>
        {event.decision && <Badge variant="neutral">decisión: {event.decision}</Badge>}
        {event.entity_type && (
          <span className="font-mono text-2xs text-ink-muted">
            {event.entity_type}
            {event.entity_id ? ` · ${event.entity_id.slice(0, 12)}` : ''}
          </span>
        )}
        <span className="ml-auto text-2xs text-ink-muted">{formatDate(event.created_at)}</span>
      </div>
      {event.reason && <p className="mt-2 text-xs text-ink-secondary">{event.reason}</p>}
      {event.error_message && (
        <p className="mt-1 text-2xs text-accent-red">{event.error_message}</p>
      )}
      {event.permission && (
        <p className="mt-1 text-2xs text-ink-muted">permiso: {event.permission}</p>
      )}
      <div className="mt-2 flex flex-wrap items-center gap-2">
        {(event.actor_role || event.actor_id) && (
          <span className="text-2xs text-ink-muted">
            actor: {event.actor_role ?? 'rol?'}
            {event.actor_id ? ` · ${event.actor_id}` : ''}
          </span>
        )}
        {event.correlation_id && (
          <span className="ml-auto font-mono text-2xs text-ink-muted">
            corr: {event.correlation_id}
          </span>
        )}
      </div>
    </div>
  )
}

/** Error state específico de operational audit: distingue auth (401/403) de red/otros. */
function OperationalAuditError({
  error,
  onRetry,
}: {
  error: XmipAdminApiError
  onRetry: () => void
}) {
  const isAuth = error.status === 401 || error.status === 403
  const label =
    error.status === 401
      ? 'Sesión requerida'
      : error.status === 403
        ? 'Acceso sin permiso operational_audit.read'
        : error.isNetworkError
          ? 'Backend no disponible'
          : 'Error del backend'
  const Icon = isAuth ? KeyRound : AlertTriangle

  return (
    <div className="card-surface flex flex-col items-center gap-3 p-8 text-center" role="alert">
      <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent-red/10 ring-1 ring-accent-red/20">
        <Icon className="h-5 w-5 text-accent-red" />
      </div>
      <div>
        <p className="text-sm font-medium text-ink">{label}</p>
        <p className="mx-auto mt-1 max-w-md text-xs text-ink-secondary">
          {isAuth
            ? 'Este registro está protegido. Inicia sesión con una cuenta autorizada para ver el detalle operacional.'
            : error.message}
        </p>
        {error.correlationId && (
          <p className="mt-1 font-mono text-2xs text-ink-muted">corr: {error.correlationId}</p>
        )}
      </div>
      <Button size="sm" variant="secondary" onClick={onRetry}>
        <RefreshCw className="h-3 w-3" />
        Reintentar
      </Button>
    </div>
  )
}
