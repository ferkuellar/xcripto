import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowUpRight, Copy, Plus, Radar, RefreshCw, X } from 'lucide-react'
import { SectionHeader } from '@/components/ui/section-header'
import { Badge, type BadgeProps } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { PriorityBadge } from '@/components/ui/status-badges'
import { EmptyState, ErrorState, SkeletonRows } from '@/components/ui/async-state'
import { useApiQuery } from '@/hooks/useApi'
import { api, ApiError, queryString } from '@/lib/api'
import type { IntakeSignalRead, NewsPriority } from '@/lib/api-types'
import { cn } from '@/lib/utils'

type BadgeVariant = NonNullable<BadgeProps['variant']>

// Catálogos espejo de INTAKE_SIGNAL_STATUSES / INTAKE_DEDUPE_STATUSES (backend constants).
const statusFilters = [
  'todas',
  'unique',
  'probable_duplicate',
  'duplicate',
  'promoted',
  'rejected',
] as const
const priorityFilters = ['Todas', 'P0', 'P1', 'P2', 'P3', 'P4'] as const

const signalStatusMap: Record<string, { variant: BadgeVariant; label: string }> = {
  received: { variant: 'blue', label: 'received' },
  normalized: { variant: 'cyan', label: 'normalized' },
  dedupe_pending: { variant: 'neutral', label: 'dedupe pending' },
  duplicate: { variant: 'orange', label: 'duplicate' },
  probable_duplicate: { variant: 'yellow', label: 'probable duplicate' },
  unique: { variant: 'green', label: 'unique' },
  linked: { variant: 'cyan', label: 'linked' },
  promoted: { variant: 'green', label: 'promoted' },
  rejected: { variant: 'red', label: 'rejected' },
  archived: { variant: 'neutral', label: 'archived' },
  error: { variant: 'red', label: 'error' },
}

const dedupeStatusMap: Record<string, { variant: BadgeVariant; label: string }> = {
  not_checked: { variant: 'neutral', label: 'dedupe pendiente' },
  unique: { variant: 'green', label: 'única' },
  exact_duplicate: { variant: 'red', label: 'duplicado exacto' },
  probable_duplicate: { variant: 'orange', label: 'probable duplicado' },
  related: { variant: 'blue', label: 'relacionada' },
  needs_review: { variant: 'yellow', label: 'requiere revisión' },
  false_positive: { variant: 'neutral', label: 'falso positivo' },
}

function formatDate(value: string) {
  return new Date(value).toLocaleString('es-MX', { dateStyle: 'medium', timeStyle: 'short' })
}

export default function NewsIntake() {
  const [statusFilter, setStatusFilter] = useState<string>('todas')
  const [priority, setPriority] = useState<string>('Todas')
  const [showForm, setShowForm] = useState(false)
  const [actionError, setActionError] = useState<string | null>(null)
  const [busyId, setBusyId] = useState<string | null>(null)

  const query = queryString({
    signal_status: statusFilter === 'todas' ? undefined : statusFilter,
    limit: 100,
  })
  const { data, loading, error, refetch } = useApiQuery<IntakeSignalRead[]>(
    `/api/v1/intake/signals${query}`,
  )

  const signals = useMemo(
    () => (data ?? []).filter((s) => priority === 'Todas' || s.priority === priority),
    [data, priority],
  )

  async function runAction(id: string, action: () => Promise<unknown>) {
    setBusyId(id)
    setActionError(null)
    try {
      await action()
      refetch()
    } catch (err) {
      setActionError(err instanceof ApiError ? err.message : String(err))
    } finally {
      setBusyId(null)
    }
  }

  const promote = (s: IntakeSignalRead) =>
    runAction(s.id, () => api.post(`/api/v1/intake/signals/${s.id}/promote`, {}))
  const reject = (s: IntakeSignalRead) =>
    runAction(s.id, () =>
      api.patch(`/api/v1/intake/signals/${s.id}/reject`, { reason: 'Rechazada desde el newsroom UI' }),
    )
  const recheckDedupe = (s: IntakeSignalRead) =>
    runAction(s.id, () => api.post(`/api/v1/intake/signals/${s.id}/dedupe`))

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <SectionHeader
          title="News Intake"
          subtitle="Señales del pipeline de intake · normalización y deduplicación en backend XMIP"
        />
        <Button size="sm" onClick={() => setShowForm((v) => !v)}>
          {showForm ? <X className="h-3.5 w-3.5" /> : <Plus className="h-3.5 w-3.5" />}
          {showForm ? 'Cerrar' : 'Registrar señal'}
        </Button>
      </div>

      {showForm && <ManualSignalForm onCreated={() => { setShowForm(false); refetch() }} />}

      {/* Filtros */}
      <div className="flex flex-wrap items-center gap-4">
        <div className="flex flex-wrap items-center gap-1.5">
          <span className="text-2xs text-ink-muted">Estado:</span>
          {statusFilters.map((s) => (
            <button
              key={s}
              onClick={() => setStatusFilter(s)}
              className={cn(
                'rounded-md px-2 py-1 text-2xs transition-colors',
                statusFilter === s
                  ? 'bg-accent-cyan/15 text-accent-cyan'
                  : 'text-ink-secondary hover:bg-white/5',
              )}
            >
              {s}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-2xs text-ink-muted">Prioridad:</span>
          {priorityFilters.map((p) => (
            <button
              key={p}
              onClick={() => setPriority(p)}
              className={cn(
                'rounded-md px-2 py-1 text-2xs transition-colors',
                priority === p
                  ? 'bg-accent-cyan/15 text-accent-cyan'
                  : 'text-ink-secondary hover:bg-white/5',
              )}
            >
              {p}
            </button>
          ))}
        </div>
      </div>

      {actionError && (
        <p className="rounded-lg border border-accent-red/30 bg-accent-red/10 px-3 py-2 text-xs text-accent-red" role="alert">
          {actionError}
        </p>
      )}

      {loading && <SkeletonRows rows={5} />}
      {error && <ErrorState error={error} onRetry={refetch} />}
      {!loading && !error && signals.length === 0 && (
        <EmptyState
          title="Sin señales de intake"
          detail="El backend respondió correctamente pero no hay señales para los filtros seleccionados. Registra una señal manual o ejecuta un adapter de intake."
        />
      )}

      {!loading && !error && signals.length > 0 && (
        <div className="space-y-2">
          {signals.map((signal) => {
            const status = signalStatusMap[signal.signal_status] ?? {
              variant: 'neutral' as BadgeVariant,
              label: signal.signal_status,
            }
            const dedupe = dedupeStatusMap[signal.dedupe_status] ?? {
              variant: 'neutral' as BadgeVariant,
              label: signal.dedupe_status,
            }
            const title = signal.normalized_title ?? signal.raw_title ?? '(sin título)'
            const isDuplicate =
              signal.dedupe_status === 'exact_duplicate' || signal.signal_status === 'duplicate'
            const isFinal = ['promoted', 'rejected', 'archived'].includes(signal.signal_status)
            const busy = busyId === signal.id

            return (
              <div
                key={signal.id}
                className={cn(
                  'card-surface flex flex-wrap items-center gap-3 p-3 transition-colors hover:bg-white/[0.02]',
                  isFinal && 'opacity-70',
                )}
              >
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-accent-cyan/10 ring-1 ring-accent-cyan/20">
                  <Radar className="h-4 w-4 text-accent-cyan" />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-medium text-ink">{title}</p>
                  <p className="truncate text-2xs text-ink-muted">
                    {signal.source_name ?? 'fuente desconocida'}
                    {signal.topic ? ` · ${signal.topic}` : ''}
                    {' · '}
                    {formatDate(signal.created_at)}
                    {signal.asset_symbols.length > 0 && ` · ${signal.asset_symbols.join(', ')}`}
                  </p>
                </div>
                <div className="flex flex-wrap items-center gap-1.5">
                  <PriorityBadge priority={signal.priority as NewsPriority} compact />
                  <Badge variant={status.variant}>{status.label}</Badge>
                  <Badge variant={dedupe.variant}>
                    {isDuplicate && <Copy className="h-3 w-3" />}
                    {dedupe.label}
                  </Badge>
                </div>
                {!isFinal && (
                  <div className="flex items-center gap-1.5">
                    <Button
                      size="sm"
                      variant="secondary"
                      disabled={busy}
                      onClick={() => recheckDedupe(signal)}
                      title="Recalcular deduplicación"
                    >
                      <RefreshCw className={cn('h-3 w-3', busy && 'animate-spin')} />
                      Dedupe
                    </Button>
                    <Button
                      size="sm"
                      variant="danger"
                      disabled={busy}
                      onClick={() => reject(signal)}
                    >
                      <X className="h-3 w-3" />
                      Rechazar
                    </Button>
                    <Button size="sm" disabled={busy || isDuplicate} onClick={() => promote(signal)}>
                      <ArrowUpRight className="h-3 w-3" />
                      Promover
                    </Button>
                  </div>
                )}
                {signal.promoted_news_item_id && (
                  <Link
                    to={`/news/${signal.promoted_news_item_id}`}
                    className="font-mono text-2xs text-accent-green transition-colors hover:text-accent-cyan hover:underline"
                  >
                    → news {signal.promoted_news_item_id.slice(0, 8)}
                  </Link>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

function ManualSignalForm({ onCreated }: { onCreated: () => void }) {
  const [title, setTitle] = useState('')
  const [summary, setSummary] = useState('')
  const [sourceName, setSourceName] = useState('')
  const [sourceUrl, setSourceUrl] = useState('')
  const [priority, setPriority] = useState<NewsPriority>('P3')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    setSubmitting(true)
    setError(null)
    try {
      await api.post('/api/v1/intake/signals', {
        signal_type: 'manual',
        raw_title: title,
        raw_summary: summary || undefined,
        source_name: sourceName || undefined,
        source_url: sourceUrl || undefined,
        priority,
      })
      onCreated()
    } catch (err) {
      setError(err instanceof ApiError ? err.message : String(err))
    } finally {
      setSubmitting(false)
    }
  }

  const inputClass =
    'h-9 w-full rounded-lg border border-line bg-surface px-3 text-sm text-ink placeholder:text-ink-muted focus:outline-none focus:ring-1 focus:ring-accent-cyan/50'

  return (
    <form onSubmit={submit} className="card-surface space-y-3 p-4">
      <p className="text-xs font-semibold text-ink">Registrar señal manual</p>
      <div className="grid gap-3 md:grid-cols-2">
        <label className="block">
          <span className="mb-1 block text-2xs text-ink-muted">Título *</span>
          <input
            required
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Título de la señal detectada"
            className={inputClass}
          />
        </label>
        <label className="block">
          <span className="mb-1 block text-2xs text-ink-muted">Fuente</span>
          <input
            value={sourceName}
            onChange={(e) => setSourceName(e.target.value)}
            placeholder="Nombre de la fuente"
            className={inputClass}
          />
        </label>
        <label className="block">
          <span className="mb-1 block text-2xs text-ink-muted">URL de la fuente</span>
          <input
            type="url"
            value={sourceUrl}
            onChange={(e) => setSourceUrl(e.target.value)}
            placeholder="https://…"
            className={inputClass}
          />
        </label>
        <label className="block">
          <span className="mb-1 block text-2xs text-ink-muted">Prioridad</span>
          <select
            value={priority}
            onChange={(e) => setPriority(e.target.value as NewsPriority)}
            className={inputClass}
          >
            {(['P0', 'P1', 'P2', 'P3', 'P4'] as const).map((p) => (
              <option key={p} value={p}>
                {p}
              </option>
            ))}
          </select>
        </label>
      </div>
      <label className="block">
        <span className="mb-1 block text-2xs text-ink-muted">Resumen</span>
        <textarea
          value={summary}
          onChange={(e) => setSummary(e.target.value)}
          rows={2}
          placeholder="Contexto breve de la señal"
          className="w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm text-ink placeholder:text-ink-muted focus:outline-none focus:ring-1 focus:ring-accent-cyan/50"
        />
      </label>
      {error && (
        <p className="text-2xs text-accent-red" role="alert">
          {error}
        </p>
      )}
      <div className="flex justify-end">
        <Button type="submit" size="sm" disabled={submitting || title.trim().length === 0}>
          <Plus className="h-3.5 w-3.5" />
          {submitting ? 'Registrando…' : 'Registrar señal'}
        </Button>
      </div>
    </form>
  )
}
