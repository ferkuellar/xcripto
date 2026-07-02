import { useMemo, useState } from 'react'
import { Copy, Plus, Radar, Trash2 } from 'lucide-react'
import { SectionHeader } from '@/components/ui/section-header'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { PriorityBadge } from '@/components/ui/status-badges'
import { signals } from '@/data/mock-news'
import { cn } from '@/lib/utils'

const categories = ['Todas', 'Regulación', 'Mercados', 'Seguridad', 'Tecnología'] as const
const priorities = ['Todas', 'P0', 'P1', 'P2', 'P3', 'P4'] as const

const sourceStatusMap = {
  active: { variant: 'green', label: 'fuente activa' },
  flagged: { variant: 'yellow', label: 'fuente marcada' },
  blocked: { variant: 'red', label: 'fuente bloqueada' },
} as const

export default function NewsIntake() {
  const [category, setCategory] = useState<string>('Todas')
  const [priority, setPriority] = useState<string>('Todas')

  const filtered = useMemo(
    () =>
      signals.filter(
        (s) =>
          (category === 'Todas' || s.category === category) &&
          (priority === 'Todas' || s.priority === priority),
      ),
    [category, priority],
  )

  const active = filtered.filter((s) => !s.discarded)
  const discarded = filtered.filter((s) => s.discarded)

  return (
    <div className="space-y-6">
      <SectionHeader
        title="News Intake"
        subtitle="Señales detectadas por NewsScoutAgent en fuentes monitoreadas"
      />

      {/* Filtros */}
      <div className="flex flex-wrap items-center gap-4">
        <div className="flex items-center gap-1.5">
          <span className="text-2xs text-ink-muted">Categoría:</span>
          {categories.map((c) => (
            <button
              key={c}
              onClick={() => setCategory(c)}
              className={cn(
                'rounded-md px-2 py-1 text-2xs transition-colors',
                category === c
                  ? 'bg-accent-cyan/15 text-accent-cyan'
                  : 'text-ink-secondary hover:bg-white/5',
              )}
            >
              {c}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-2xs text-ink-muted">Prioridad:</span>
          {priorities.map((p) => (
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

      {/* Señales activas */}
      <div className="space-y-2">
        {active.map((signal) => {
          const src = sourceStatusMap[signal.sourceStatus]
          return (
            <div
              key={signal.id}
              className="card-surface flex flex-wrap items-center gap-3 p-3 transition-colors hover:bg-white/[0.02]"
            >
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-accent-cyan/10 ring-1 ring-accent-cyan/20">
                <Radar className="h-4 w-4 text-accent-cyan" />
              </div>
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium text-ink">{signal.title}</p>
                <p className="text-2xs text-ink-muted">
                  {signal.id} · {signal.category} · {signal.source} · detectada {signal.detectedAt}
                </p>
              </div>
              <div className="flex flex-wrap items-center gap-1.5">
                <PriorityBadge priority={signal.priority} compact />
                <Badge variant={src.variant}>{src.label}</Badge>
                {signal.duplicate && (
                  <Badge variant="neutral">
                    <Copy className="h-3 w-3" />
                    duplicado
                  </Badge>
                )}
              </div>
              <Button size="sm" variant="secondary" disabled={signal.duplicate}>
                <Plus className="h-3 w-3" />
                Create NewsItem
              </Button>
            </div>
          )
        })}
        {active.length === 0 && (
          <p className="card-surface p-6 text-center text-xs text-ink-muted">
            Sin señales para los filtros seleccionados.
          </p>
        )}
      </div>

      {/* Descartadas */}
      {discarded.length > 0 && (
        <div>
          <SectionHeader title="Señales descartadas" subtitle="Excluidas del pipeline" />
          <div className="space-y-2">
            {discarded.map((signal) => (
              <div
                key={signal.id}
                className="flex items-center gap-3 rounded-xl border border-line/50 bg-surface/50 p-3 opacity-60"
              >
                <Trash2 className="h-4 w-4 shrink-0 text-ink-muted" />
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm text-ink-secondary line-through">{signal.title}</p>
                  <p className="text-2xs text-ink-muted">
                    {signal.id} · {signal.source}
                  </p>
                </div>
                <Badge variant="red">fuente bloqueada</Badge>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
