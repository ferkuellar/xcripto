import { useState } from 'react'
import { ExternalLink, Plus, X } from 'lucide-react'
import { SectionHeader } from '@/components/ui/section-header'
import { Badge, type BadgeProps } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { EmptyState, ErrorState, SkeletonRows } from '@/components/ui/async-state'
import { useApiQuery } from '@/hooks/useApi'
import { api, ApiError } from '@/lib/api'
import type { SourceRead } from '@/lib/api-types'

type BadgeVariant = NonNullable<BadgeProps['variant']>

const statusMap: Record<SourceRead['source_status'], { variant: BadgeVariant; label: string }> = {
  proposed: { variant: 'blue', label: 'proposed' },
  active: { variant: 'green', label: 'active' },
  trusted: { variant: 'cyan', label: 'trusted' },
  watchlist: { variant: 'yellow', label: 'watchlist' },
  restricted: { variant: 'orange', label: 'restricted' },
  blocked: { variant: 'red', label: 'blocked' },
  archived: { variant: 'neutral', label: 'archived' },
}

function trustTone(level: string) {
  if (level === 'T0') return 'text-accent-green'
  if (level === 'T1') return 'text-accent-cyan'
  if (level === 'T2') return 'text-accent-yellow'
  return 'text-accent-red'
}

function formatDate(value: string) {
  return new Date(value).toLocaleDateString('es-MX', { dateStyle: 'medium' })
}

export default function SourceValidation() {
  const [showForm, setShowForm] = useState(false)
  const { data, loading, error, refetch } = useApiQuery<SourceRead[]>('/api/v1/sources?limit=200')

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <SectionHeader
          title="Source Validation"
          subtitle="Registro de fuentes del backend XMIP con nivel de confianza y estado editorial"
        />
        <Button size="sm" onClick={() => setShowForm((v) => !v)}>
          {showForm ? <X className="h-3.5 w-3.5" /> : <Plus className="h-3.5 w-3.5" />}
          {showForm ? 'Cerrar' : 'Registrar fuente'}
        </Button>
      </div>

      {showForm && <SourceForm onCreated={() => { setShowForm(false); refetch() }} />}

      {loading && <SkeletonRows rows={5} />}
      {error && <ErrorState error={error} onRetry={refetch} />}
      {!loading && !error && (data?.length ?? 0) === 0 && (
        <EmptyState
          title="Sin fuentes registradas"
          detail="El registro de fuentes está vacío. Toda noticia requiere una fuente registrada — empieza registrando las fuentes primarias del newsroom."
        />
      )}

      {!loading && !error && data && data.length > 0 && (
        <div className="card-surface overflow-x-auto">
          <table className="w-full min-w-[760px] text-left text-xs">
            <thead>
              <tr className="border-b border-line text-2xs uppercase tracking-wider text-ink-muted">
                <th className="px-4 py-3 font-medium">Fuente</th>
                <th className="px-3 py-3 font-medium">Tipo</th>
                <th className="px-3 py-3 text-center font-medium">Trust</th>
                <th className="px-3 py-3 font-medium">Estado</th>
                <th className="px-3 py-3 font-medium">Notas</th>
                <th className="px-3 py-3 font-medium">Registrada</th>
              </tr>
            </thead>
            <tbody>
              {data.map((source) => {
                const status = statusMap[source.source_status] ?? {
                  variant: 'neutral' as BadgeVariant,
                  label: source.source_status,
                }
                return (
                  <tr
                    key={source.id}
                    className="border-b border-line/50 transition-colors last:border-0 hover:bg-white/[0.02]"
                  >
                    <td className="px-4 py-3">
                      <p className="font-medium text-ink">{source.source_name}</p>
                      <a
                        href={source.source_url}
                        target="_blank"
                        rel="noreferrer noopener"
                        className="inline-flex items-center gap-1 text-2xs text-ink-muted transition-colors hover:text-accent-cyan"
                      >
                        {source.source_url.replace(/^https?:\/\//, '').slice(0, 48)}
                        <ExternalLink className="h-2.5 w-2.5" />
                      </a>
                    </td>
                    <td className="px-3 py-3 text-ink-secondary">{source.source_type}</td>
                    <td
                      className={`px-3 py-3 text-center font-semibold tabular-nums ${trustTone(source.trust_level)}`}
                    >
                      {source.trust_level}
                    </td>
                    <td className="px-3 py-3">
                      <Badge variant={status.variant}>{status.label}</Badge>
                    </td>
                    <td className="max-w-[220px] truncate px-3 py-3 text-ink-muted">
                      {source.notes ?? '—'}
                    </td>
                    <td className="px-3 py-3 text-ink-muted">{formatDate(source.created_at)}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}

      <p className="text-2xs text-ink-muted">
        Escala de confianza: T0 (máxima) a T3. Estados y niveles definidos en
        ORION-021-Gestion-de-Fuentes y validados por el backend.
      </p>
    </div>
  )
}

function SourceForm({ onCreated }: { onCreated: () => void }) {
  const [name, setName] = useState('')
  const [url, setUrl] = useState('')
  const [type, setType] = useState('news_outlet')
  const [trust, setTrust] = useState('T2')
  const [notes, setNotes] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    setSubmitting(true)
    setError(null)
    try {
      await api.post('/api/v1/sources', {
        source_name: name,
        source_url: url,
        source_type: type,
        source_status: 'proposed',
        trust_level: trust,
        notes: notes || undefined,
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
      <p className="text-xs font-semibold text-ink">Registrar fuente (estado inicial: proposed)</p>
      <div className="grid gap-3 md:grid-cols-2">
        <label className="block">
          <span className="mb-1 block text-2xs text-ink-muted">Nombre *</span>
          <input required minLength={2} value={name} onChange={(e) => setName(e.target.value)} className={inputClass} placeholder="p. ej. SEC Newsroom" />
        </label>
        <label className="block">
          <span className="mb-1 block text-2xs text-ink-muted">URL *</span>
          <input required type="url" value={url} onChange={(e) => setUrl(e.target.value)} className={inputClass} placeholder="https://…" />
        </label>
        <label className="block">
          <span className="mb-1 block text-2xs text-ink-muted">Tipo</span>
          <select value={type} onChange={(e) => setType(e.target.value)} className={inputClass}>
            {['news_outlet', 'official', 'regulator', 'exchange', 'onchain_data', 'research', 'social', 'other'].map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </label>
        <label className="block">
          <span className="mb-1 block text-2xs text-ink-muted">Trust level</span>
          <select value={trust} onChange={(e) => setTrust(e.target.value)} className={inputClass}>
            {['T0', 'T1', 'T2', 'T3'].map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </label>
      </div>
      <label className="block">
        <span className="mb-1 block text-2xs text-ink-muted">Notas</span>
        <input value={notes} onChange={(e) => setNotes(e.target.value)} className={inputClass} placeholder="Contexto editorial de la fuente" />
      </label>
      {error && (
        <p className="text-2xs text-accent-red" role="alert">{error}</p>
      )}
      <div className="flex justify-end">
        <Button type="submit" size="sm" disabled={submitting}>
          <Plus className="h-3.5 w-3.5" />
          {submitting ? 'Registrando…' : 'Registrar fuente'}
        </Button>
      </div>
    </form>
  )
}
