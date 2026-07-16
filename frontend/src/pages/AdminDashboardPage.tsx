import { useCallback, type ReactNode } from 'react'
import {
  Activity,
  AlertTriangle,
  Bot,
  CheckCircle2,
  DatabaseZap,
  FileWarning,
  GitBranch,
  Inbox,
  KeyRound,
  Link2,
  Loader2,
  RefreshCw,
  Server,
  ShieldAlert,
  Users,
} from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { adminApi } from '@/services/adminApi'
import { useXmipAdminQuery, type AdminQueryState } from '@/hooks/useXmipAdmin'
import { XmipAdminApiError } from '@/lib/xmipAdminApi'
import { cn } from '@/lib/utils'
import type {
  AgentRunnerSummary,
  AuditSummary,
  BlockerItem,
  ConnectorsSummary,
  EditorialWorkQueueItem,
  FrontendConfig,
  IntakeQueueItem,
  NewsroomHealth,
  OperationalGap,
  OwnershipBoard,
  PublicationBoardItem,
  ReadinessBoardItem,
  ReadyResponse,
  RouteMapGroup,
  TaskBoardItem,
} from '@/types/xmip'

type BadgeTone = 'neutral' | 'cyan' | 'green' | 'yellow' | 'orange' | 'red' | 'purple' | 'blue'

function formatNumber(value: number | null | undefined) {
  return new Intl.NumberFormat('es-MX').format(value ?? 0)
}

function formatDate(value: string | null | undefined) {
  if (!value) return 'sin fecha'
  return new Date(value).toLocaleString('es-MX', { dateStyle: 'medium', timeStyle: 'short' })
}

// Cubre los catálogos canónicos del backend (readiness, audit, task, risk,
// dedupe, severity). No dejar valores válidos como neutral por desconocimiento.
function toneForStatus(status: string | null | undefined): BadgeTone {
  if (!status) return 'neutral'
  const value = status.toLowerCase()
  // Sano / aprobatorio
  if (
    [
      'ready', 'ready_to_advance', 'healthy', 'completed', 'published', 'distributed',
      'unique', 'active', 'trusted', 'verified', 'approved', 'passed', 'allow_to_continue',
      'allow',
    ].includes(value)
  ) {
    return 'green'
  }
  // Bloqueo / fallo
  if (
    [
      'blocked', 'block_publication', 'failed', 'critical', 'retracted', 'rejected',
      'duplicate', 'exact_duplicate',
    ].includes(value)
  ) {
    return 'red'
  }
  // Advertencia / requiere atención
  if (
    [
      'degraded', 'warning', 'pending', 'pending_review', 'queued', 'scheduled',
      'passed_with_warnings', 'completed_with_warnings', 'allow_with_warnings',
      'needs_revision', 'partially_verified', 'rumor', 'probable_duplicate', 'medium',
    ].includes(value)
  ) {
    return 'yellow'
  }
  // Severidad alta / escalado
  if (['high', 'escalate', 'escalated'].includes(value)) return 'orange'
  // En proceso
  if (['running', 'promoted', 'validating', 'drafting', 'reviewing'].includes(value)) return 'cyan'
  return 'neutral'
}

function AdminStatCard({
  label,
  value,
  detail,
  icon: Icon,
  tone = 'text-accent-cyan',
  loading,
}: {
  label: string
  value: number | string
  detail: string
  icon: typeof Activity
  tone?: string
  loading?: boolean
}) {
  return (
    <Card className="min-h-28">
      <CardContent className="pt-4">
        <div className="flex items-start justify-between gap-3">
          <span className="text-2xs uppercase tracking-wider text-ink-muted">{label}</span>
          <Icon className={cn('h-4 w-4 shrink-0', tone)} />
        </div>
        {loading ? (
          <div className="mt-3 h-7 w-20 animate-pulse rounded bg-white/5" />
        ) : (
          <p className="mt-2 text-2xl font-semibold tabular-nums text-ink">{value}</p>
        )}
        <p className="mt-1 text-2xs text-ink-secondary">{detail}</p>
      </CardContent>
    </Card>
  )
}

function AdminErrorState({ error, onRetry }: { error: XmipAdminApiError; onRetry: () => void }) {
  const label =
    error.status === 401
      ? 'Sesión requerida'
      : error.status === 403
        ? 'Rol sin permiso'
        : error.status === 503
          ? 'Backend no listo'
          : error.isNetworkError
            ? 'Backend no disponible'
            : 'Error del backend'

  return (
    <div className="rounded-lg border border-accent-red/20 bg-accent-red/5 p-3" role="alert">
      <div className="flex items-start gap-2">
        <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-accent-red" />
        <div className="min-w-0 flex-1">
          <p className="text-xs font-medium text-ink">{label}</p>
          <p className="mt-0.5 text-xs text-ink-secondary">{error.message}</p>
          {error.correlationId && (
            <p className="mt-1 truncate font-mono text-2xs text-ink-muted">
              corr: {error.correlationId}
            </p>
          )}
        </div>
        <Button size="sm" variant="ghost" onClick={onRetry} title="Reintentar">
          <RefreshCw className="h-3.5 w-3.5" />
        </Button>
      </div>
    </div>
  )
}

function AdminSection<T>({
  title,
  query,
  empty,
  children,
}: {
  title: string
  query: AdminQueryState<T>
  empty?: boolean
  children: (data: T) => ReactNode
}) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        {query.loading && (
          <div className="space-y-2" aria-busy="true">
            <div className="h-8 animate-pulse rounded bg-white/5" />
            <div className="h-8 animate-pulse rounded bg-white/5" />
            <div className="h-8 animate-pulse rounded bg-white/5" />
          </div>
        )}
        {!query.loading && query.error && (
          <AdminErrorState error={query.error} onRetry={query.refetch} />
        )}
        {!query.loading && !query.error && query.data && empty && (
          <div className="flex items-center gap-2 rounded-lg border border-line bg-white/[0.02] p-4 text-xs text-ink-muted">
            <Inbox className="h-4 w-4" />
            Sin elementos operativos.
          </div>
        )}
        {!query.loading && !query.error && query.data && !empty && children(query.data)}
      </CardContent>
    </Card>
  )
}

function ReadyBanner({ query }: { query: AdminQueryState<ReadyResponse> }) {
  if (query.loading) {
    return (
      <Card>
        <CardContent className="flex items-center gap-3 pt-4">
          <Loader2 className="h-4 w-4 animate-spin text-accent-cyan" />
          <span className="text-sm text-ink-secondary">Verificando readiness del backend</span>
        </CardContent>
      </Card>
    )
  }

  if (query.error) {
    return (
      <Card className="border-accent-red/30">
        <CardContent className="pt-4">
          <AdminErrorState error={query.error} onRetry={query.refetch} />
        </CardContent>
      </Card>
    )
  }

  const ready = query.data?.status === 'ready'
  return (
    <Card className={ready ? 'border-accent-green/30' : 'border-accent-yellow/30'}>
      <CardContent className="flex flex-wrap items-center justify-between gap-3 pt-4">
        <div className="flex items-center gap-3">
          {ready ? (
            <CheckCircle2 className="h-5 w-5 text-accent-green" />
          ) : (
            <AlertTriangle className="h-5 w-5 text-accent-yellow" />
          )}
          <div>
            <p className="text-sm font-medium text-ink">
              {ready ? 'Backend ready' : 'Backend not ready'}
            </p>
            <p className="text-xs text-ink-secondary">
              {query.data?.service} · v{query.data?.version}
            </p>
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          {Object.entries(query.data?.checks ?? {}).map(([key, value]) => (
            <Badge key={key} variant={value === 'ok' ? 'green' : 'yellow'}>
              {key}: {value}
            </Badge>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

function ConfigBanner({
  config,
  routeMap,
}: {
  config: AdminQueryState<FrontendConfig>
  routeMap: AdminQueryState<RouteMapGroup[]>
}) {
  if (config.loading && routeMap.loading) return null
  return (
    <Card>
      <CardContent className="grid gap-3 pt-4 md:grid-cols-3">
        <div className="flex items-center gap-3">
          <KeyRound className="h-4 w-4 text-accent-cyan" />
          <div>
            <p className="text-xs font-medium text-ink">
              {config.data?.auth_enabled ? 'Auth habilitado' : 'Auth deshabilitado'}
            </p>
            <p className="text-2xs text-ink-muted">
              RBAC {config.data?.rbac_enabled ? 'activo' : 'inactivo'} ·{' '}
              {config.data?.environment ?? 'unknown'}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <GitBranch className="h-4 w-4 text-accent-purple" />
          <div>
            <p className="text-xs font-medium text-ink">
              {formatNumber(routeMap.data?.reduce((total, group) => total + group.routes.length, 0))}{' '}
              rutas admin
            </p>
            <p className="text-2xs text-ink-muted">route-map frontend-safe</p>
          </div>
        </div>
        <div className="flex flex-wrap gap-1">
          {Object.entries(config.data?.features ?? {})
            .filter(([, enabled]) => enabled)
            .slice(0, 6)
            .map(([feature]) => (
              <Badge key={feature} variant="blue">
                {feature}
              </Badge>
            ))}
        </div>
      </CardContent>
    </Card>
  )
}

function Rows<T>({
  items,
  getKey,
  render,
}: {
  items: T[]
  getKey: (item: T, index: number) => string
  render: (item: T) => ReactNode
}) {
  return <div className="space-y-2">{items.map((item, index) => <div key={getKey(item, index)}>{render(item)}</div>)}</div>
}

function ChipList({ values, max = 3 }: { values: string[]; max?: number }) {
  if (values.length === 0) return <span className="text-2xs text-ink-muted">sin brechas</span>
  return (
    <div className="flex flex-wrap gap-1">
      {values.slice(0, max).map((value) => (
        <Badge key={value} variant="neutral">
          {value}
        </Badge>
      ))}
      {values.length > max && <Badge variant="neutral">+{values.length - max}</Badge>}
    </div>
  )
}

export default function AdminDashboardPage() {
  const ready = useXmipAdminQuery(useCallback((signal) => adminApi.getReady(signal), []))
  const config = useXmipAdminQuery(useCallback((signal) => adminApi.getFrontendConfig(signal), []))
  const routeMap = useXmipAdminQuery(useCallback((signal) => adminApi.getRouteMap(signal), []))
  const overview = useXmipAdminQuery(useCallback((signal) => adminApi.getDashboardOverview(signal), []))
  const health = useXmipAdminQuery(useCallback((signal) => adminApi.getNewsroomHealth(signal), []))
  const intake = useXmipAdminQuery(useCallback((signal) => adminApi.getIntakeQueue(signal), []))
  const workQueue = useXmipAdminQuery(
    useCallback((signal) => adminApi.getEditorialWorkQueue(signal), []),
  )
  const blockers = useXmipAdminQuery(useCallback((signal) => adminApi.getBlockers(signal), []))
  const readiness = useXmipAdminQuery(useCallback((signal) => adminApi.getReadinessBoard(signal), []))
  const tasks = useXmipAdminQuery(useCallback((signal) => adminApi.getTaskBoard(signal), []))
  const publications = useXmipAdminQuery(
    useCallback((signal) => adminApi.getPublicationBoard(signal), []),
  )
  const ownership = useXmipAdminQuery(useCallback((signal) => adminApi.getOwnershipBoard(signal), []))
  const gaps = useXmipAdminQuery(useCallback((signal) => adminApi.getOperationalGaps(signal), []))
  const agentRunner = useXmipAdminQuery(
    useCallback((signal) => adminApi.getAgentRunnerSummary(signal), []),
  )
  const connectors = useXmipAdminQuery(useCallback((signal) => adminApi.getConnectorsSummary(signal), []))
  const audit = useXmipAdminQuery(useCallback((signal) => adminApi.getAuditSummary(signal), []))

  const overviewData = overview.data

  return (
    <div className="space-y-6">
      <section>
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 className="text-xl font-semibold tracking-tight text-ink lg:text-2xl">
              Admin Operations
            </h1>
            <p className="mt-1 text-sm text-ink-secondary">
              XMIP backend operativo · dashboard API real
            </p>
          </div>
          <Badge variant={ready.data?.status === 'ready' ? 'green' : 'yellow'}>
            /ready {ready.data?.status ?? (ready.loading ? 'checking' : 'error')}
          </Badge>
        </div>
      </section>

      <ReadyBanner query={ready} />
      <ConfigBanner config={config} routeMap={routeMap} />

      <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        <AdminStatCard
          label="Noticias"
          value={formatNumber(overviewData?.total_news)}
          detail={`${formatNumber(overviewData?.unassigned_news_count)} sin owner`}
          icon={FileWarning}
          loading={overview.loading}
        />
        <AdminStatCard
          label="Intake pendiente"
          value={formatNumber(overviewData?.pending_intake_signals)}
          detail={`${formatNumber(overviewData?.duplicate_intake_signals)} duplicadas`}
          icon={Inbox}
          loading={overview.loading}
        />
        <AdminStatCard
          label="Tareas bloqueadas"
          value={formatNumber(overviewData?.blocked_tasks)}
          detail={`${formatNumber(overviewData?.pending_tasks)} pendientes`}
          icon={ShieldAlert}
          tone={(overviewData?.blocked_tasks ?? 0) > 0 ? 'text-accent-red' : 'text-accent-green'}
          loading={overview.loading}
        />
        <AdminStatCard
          label="Readiness"
          value={formatNumber(overviewData?.ready_to_advance_count)}
          detail={`${formatNumber(overviewData?.blocked_readiness_count)} bloqueadas`}
          icon={CheckCircle2}
          tone="text-accent-green"
          loading={overview.loading}
        />
        <AdminStatCard
          label="Publicaciones"
          value={formatNumber(overviewData?.published_records_count)}
          detail={`${formatNumber(overviewData?.scheduled_publications_count)} programadas`}
          icon={Link2}
          tone="text-accent-purple"
          loading={overview.loading}
        />
        <AdminStatCard
          label="Agentes"
          value={formatNumber(agentRunner.data?.total_internal_runs)}
          detail={`${formatNumber(agentRunner.data?.outputs_pending_review)} outputs en revisión`}
          icon={Bot}
          loading={agentRunner.loading}
        />
        <AdminStatCard
          label="Conectores"
          value={formatNumber(connectors.data?.total_connectors)}
          detail={`${formatNumber(connectors.data?.dry_run_only_connectors)} dry-run only`}
          icon={DatabaseZap}
          loading={connectors.loading}
        />
        <AdminStatCard
          label="Audit events"
          value={formatNumber(audit.data?.total_events)}
          detail={`${formatNumber(overviewData?.active_users_count)} usuarios activos`}
          icon={Activity}
          tone="text-accent-blue"
          loading={audit.loading}
        />
      </section>

      <section className="grid gap-4 xl:grid-cols-3">
        <AdminSection title="Newsroom health" query={health}>
          {(data: NewsroomHealth) => (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <Badge variant={toneForStatus(data.health_status)}>{data.health_status}</Badge>
                <span className="text-2xl font-semibold tabular-nums text-ink">
                  {data.health_score}
                </span>
              </div>
              <ChipList values={data.critical_blockers} />
              <ChipList values={data.warnings} />
            </div>
          )}
        </AdminSection>

        <AdminSection
          title="Operational gaps"
          query={gaps}
          empty={(gaps.data ?? []).length === 0}
        >
          {(items: OperationalGap[]) => (
            <Rows
              items={items.slice(0, 5)}
              getKey={(item) => item.gap_type}
              render={(item) => (
                <div className="rounded-lg border border-line bg-white/[0.02] p-3">
                  <div className="flex items-center justify-between gap-2">
                    <p className="truncate text-xs font-medium text-ink">{item.gap_type}</p>
                    <Badge variant={toneForStatus(item.severity)}>{formatNumber(item.count)}</Badge>
                  </div>
                  <p className="mt-1 line-clamp-2 text-2xs text-ink-secondary">
                    {item.recommended_action}
                  </p>
                </div>
              )}
            />
          )}
        </AdminSection>

        <AdminSection title="Ownership" query={ownership}>
          {(data: OwnershipBoard) => (
            <div className="space-y-3">
              <div className="grid grid-cols-3 gap-2">
                <div className="rounded-lg bg-white/[0.03] p-3">
                  <p className="text-2xs text-ink-muted">Usuarios</p>
                  <p className="text-xl font-semibold text-ink">{formatNumber(data.users.length)}</p>
                </div>
                <div className="rounded-lg bg-white/[0.03] p-3">
                  <p className="text-2xs text-ink-muted">News sin owner</p>
                  <p className="text-xl font-semibold text-ink">
                    {formatNumber(data.unassigned_news.length)}
                  </p>
                </div>
                <div className="rounded-lg bg-white/[0.03] p-3">
                  <p className="text-2xs text-ink-muted">Tasks sin owner</p>
                  <p className="text-xl font-semibold text-ink">
                    {formatNumber(data.unassigned_tasks.length)}
                  </p>
                </div>
              </div>
              <Rows
                items={data.users.slice(0, 4)}
                getKey={(item) => item.user_id}
                render={(user) => (
                  <div className="flex items-center justify-between rounded-lg border border-line bg-white/[0.02] p-2">
                    <div className="min-w-0">
                      <p className="truncate text-xs font-medium text-ink">{user.display_name}</p>
                      <p className="text-2xs text-ink-muted">{user.role}</p>
                    </div>
                    <Badge variant="purple">{user.active_assignment_count} asignaciones</Badge>
                  </div>
                )}
              />
            </div>
          )}
        </AdminSection>
      </section>

      <section className="grid gap-4 xl:grid-cols-2">
        <AdminSection
          title="Intake queue"
          query={intake}
          empty={(intake.data ?? []).length === 0}
        >
          {(items: IntakeQueueItem[]) => (
            <Rows
              items={items}
              getKey={(item) => item.signal_id}
              render={(item) => (
                <div className="rounded-lg border border-line bg-white/[0.02] p-3">
                  <div className="flex items-start justify-between gap-2">
                    <div className="min-w-0">
                      <p className="truncate text-sm font-medium text-ink">
                        {item.normalized_title ?? item.raw_title ?? 'Untitled signal'}
                      </p>
                      <p className="truncate text-2xs text-ink-muted">
                        {item.source_name ?? 'sin fuente'} · {formatDate(item.created_at)}
                      </p>
                    </div>
                    <Badge variant={toneForStatus(item.dedupe_status)}>{item.dedupe_status}</Badge>
                  </div>
                </div>
              )}
            />
          )}
        </AdminSection>

        <AdminSection
          title="Editorial work queue"
          query={workQueue}
          empty={(workQueue.data ?? []).length === 0}
        >
          {(items: EditorialWorkQueueItem[]) => (
            <Rows
              items={items}
              getKey={(item) => item.news_item_id}
              render={(item) => (
                <div className="rounded-lg border border-line bg-white/[0.02] p-3">
                  <div className="flex items-start justify-between gap-2">
                    <div className="min-w-0">
                      <p className="truncate text-sm font-medium text-ink">{item.title}</p>
                      <p className="text-2xs text-ink-muted">
                        {item.priority} · {item.status} · owner {item.owner ?? 'none'}
                      </p>
                    </div>
                    <Badge variant={toneForStatus(item.readiness_status)}>
                      {item.readiness_status ?? 'no score'}
                    </Badge>
                  </div>
                  <div className="mt-2">
                    <ChipList values={item.missing_requirements} max={4} />
                  </div>
                </div>
              )}
            />
          )}
        </AdminSection>

        <AdminSection
          title="Blockers"
          query={blockers}
          empty={(blockers.data ?? []).length === 0}
        >
          {(items: BlockerItem[]) => (
            <Rows
              items={items}
              getKey={(item, index) => `${item.entity_type}-${item.entity_id}-${index}`}
              render={(item) => (
                <div className="rounded-lg border border-accent-red/20 bg-accent-red/5 p-3">
                  <div className="flex items-start justify-between gap-2">
                    <p className="text-sm font-medium text-ink">{item.title_or_summary}</p>
                    <Badge variant={toneForStatus(item.severity)}>{item.severity}</Badge>
                  </div>
                  <p className="mt-1 text-xs text-ink-secondary">{item.reason}</p>
                </div>
              )}
            />
          )}
        </AdminSection>

        <AdminSection
          title="Readiness board"
          query={readiness}
          empty={(readiness.data ?? []).length === 0}
        >
          {(items: ReadinessBoardItem[]) => (
            <Rows
              items={items}
              getKey={(item) => item.news_item_id}
              render={(item) => (
                <div className="rounded-lg border border-line bg-white/[0.02] p-3">
                  <div className="flex items-center justify-between gap-3">
                    <div className="min-w-0">
                      <p className="truncate text-sm font-medium text-ink">{item.title}</p>
                      <p className="text-2xs text-ink-muted">
                        {item.score_band} · {formatDate(item.calculated_at)}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-lg font-semibold tabular-nums text-ink">{item.score}</p>
                      <Badge variant={toneForStatus(item.readiness_status)}>
                        {item.readiness_status}
                      </Badge>
                    </div>
                  </div>
                </div>
              )}
            />
          )}
        </AdminSection>

        <AdminSection title="Task board" query={tasks} empty={(tasks.data ?? []).length === 0}>
          {(items: TaskBoardItem[]) => (
            <Rows
              items={items}
              getKey={(item) => item.task_id}
              render={(item) => (
                <div className="rounded-lg border border-line bg-white/[0.02] p-3">
                  <div className="flex items-start justify-between gap-2">
                    <div className="min-w-0">
                      <p className="truncate text-sm font-medium text-ink">{item.title}</p>
                      <p className="text-2xs text-ink-muted">
                        {item.task_type} · {item.assigned_agent ?? 'unassigned'}
                      </p>
                    </div>
                    <Badge variant={item.blocking ? 'red' : toneForStatus(item.task_status)}>
                      {item.task_status}
                    </Badge>
                  </div>
                </div>
              )}
            />
          )}
        </AdminSection>

        <AdminSection
          title="Publication board"
          query={publications}
          empty={(publications.data ?? []).length === 0}
        >
          {(items: PublicationBoardItem[]) => (
            <Rows
              items={items}
              getKey={(item) => item.publication_record_id}
              render={(item) => (
                <div className="rounded-lg border border-line bg-white/[0.02] p-3">
                  <div className="flex items-start justify-between gap-2">
                    <div className="min-w-0">
                      <p className="truncate text-sm font-medium text-ink">{item.title}</p>
                      <p className="text-2xs text-ink-muted">
                        {item.channel} · {item.owner ?? 'sin owner'}
                      </p>
                    </div>
                    <Badge variant={toneForStatus(item.publication_status)}>
                      {item.publication_status}
                    </Badge>
                  </div>
                </div>
              )}
            />
          )}
        </AdminSection>
      </section>

      <section className="grid gap-4 lg:grid-cols-3">
        <AdminSection title="Agent runner" query={agentRunner}>
          {(data: AgentRunnerSummary) => (
            <div className="grid grid-cols-2 gap-2 text-sm">
              <Badge variant="cyan">runs {formatNumber(data.total_internal_runs)}</Badge>
              <Badge variant="green">completed {formatNumber(data.completed_runs)}</Badge>
              <Badge variant="red">failed {formatNumber(data.failed_runs)}</Badge>
              <Badge variant="yellow">eligible {formatNumber(data.tasks_eligible_for_runner)}</Badge>
            </div>
          )}
        </AdminSection>

        <AdminSection title="Connectors" query={connectors}>
          {(data: ConnectorsSummary) => (
            <div className="space-y-2">
              <div className="grid grid-cols-3 gap-2">
                <Badge variant="cyan">total {formatNumber(data.total_connectors)}</Badge>
                <Badge variant="green">enabled {formatNumber(data.enabled_connectors)}</Badge>
                <Badge variant="yellow">dry-run {formatNumber(data.dry_run_only_connectors)}</Badge>
              </div>
              <ChipList values={Object.keys(data.connectors_by_type)} max={5} />
            </div>
          )}
        </AdminSection>

        <AdminSection title="Operational audit" query={audit}>
          {(data: AuditSummary) => (
            <div className="space-y-2">
              <Badge variant="blue">events {formatNumber(data.total_events)}</Badge>
              <ChipList values={Object.keys(data.events_by_outcome)} max={5} />
              <p className="text-2xs text-ink-muted">
                recent events: {formatNumber(data.recent_events.length)}
              </p>
            </div>
          )}
        </AdminSection>
      </section>

      <section>
        <Card>
          <CardContent className="flex flex-wrap items-center gap-3 pt-4 text-xs text-ink-secondary">
            <Server className="h-4 w-4 text-accent-cyan" />
            <span>Base URL desde VITE_API_BASE_URL</span>
            <Users className="h-4 w-4 text-accent-purple" />
            <span>Sesión HttpOnly emitida por el backend</span>
          </CardContent>
        </Card>
      </section>
    </div>
  )
}
