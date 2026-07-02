// Paleta de series validada (orden fijo) para la superficie #0B1020.
export const SERIES = {
  1: '#0891B2',
  2: '#DB2777',
  3: '#B45309',
  4: '#8B5CF6',
  5: '#059669',
} as const

// Colores de estado — reservados para semántica de riesgo, nunca como "serie 4".
export const STATUS = {
  good: '#22C55E',
  warning: '#FACC15',
  serious: '#FB923C',
  critical: '#EF4444',
} as const

export const GRID_STROKE = 'rgba(255,255,255,0.06)'
export const AXIS_STROKE = 'rgba(255,255,255,0.12)'
export const TICK_STYLE = { fill: '#64748B', fontSize: 11 }
export const SURFACE = '#0B1020'

interface ChartTooltipProps {
  active?: boolean
  label?: string | number
  payload?: {
    dataKey?: string | number
    name?: string | number
    value?: string | number
    color?: string
  }[]
}

export function ChartTooltip({ active, payload, label }: ChartTooltipProps) {
  if (!active || !payload?.length) return null
  return (
    <div className="rounded-lg border border-line bg-surface-elevated px-3 py-2 shadow-card">
      <p className="mb-1 text-2xs font-medium text-ink-secondary">{label}</p>
      {payload.map((entry) => (
        <div key={String(entry.dataKey)} className="flex items-center gap-2 text-xs">
          <span className="h-2 w-2 rounded-sm" style={{ background: entry.color }} />
          <span className="text-ink-secondary">{entry.name}</span>
          <span className="ml-auto pl-3 font-medium tabular-nums text-ink">{entry.value}</span>
        </div>
      ))}
    </div>
  )
}

export function ChartLegend({ items }: { items: { label: string; color: string }[] }) {
  return (
    <div className="mb-2 flex flex-wrap items-center gap-x-4 gap-y-1">
      {items.map((item) => (
        <div key={item.label} className="flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-sm" style={{ background: item.color }} />
          <span className="text-2xs text-ink-secondary">{item.label}</span>
        </div>
      ))}
    </div>
  )
}
