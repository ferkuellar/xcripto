import { motion } from 'framer-motion'
import {
  ArrowDownRight,
  ArrowUpRight,
  Bot,
  CalendarClock,
  CheckCircle2,
  PenLine,
  Radar,
  ShieldAlert,
  type LucideIcon,
} from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { cn } from '@/lib/utils'
import type { Kpi } from '@/data/types'

const iconMap: Record<string, LucideIcon> = {
  radar: Radar,
  check: CheckCircle2,
  alert: ShieldAlert,
  pen: PenLine,
  calendar: CalendarClock,
  bot: Bot,
}

const stateRing: Record<Kpi['state'], string> = {
  good: 'text-accent-green bg-accent-green/10 ring-accent-green/25',
  warning: 'text-accent-yellow bg-accent-yellow/10 ring-accent-yellow/25',
  critical: 'text-accent-red bg-accent-red/10 ring-accent-red/25',
  neutral: 'text-ink-secondary bg-white/5 ring-white/10',
}

export function MetricCard({ kpi, index = 0 }: { kpi: Kpi; index?: number }) {
  const Icon = iconMap[kpi.icon] ?? Radar
  const up = kpi.deltaPct >= 0
  // Para "High Risk Items" un aumento es negativo aunque el delta sea positivo.
  const trendVariant = kpi.state === 'critical' ? 'red' : up ? 'green' : 'neutral'

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, delay: index * 0.04 }}
      className="card-surface p-4"
    >
      <div className="flex items-start justify-between gap-2">
        <div className={cn('flex h-8 w-8 items-center justify-center rounded-lg ring-1', stateRing[kpi.state])}>
          <Icon className="h-4 w-4" />
        </div>
        <Badge variant={trendVariant}>
          {up ? <ArrowUpRight className="h-3 w-3" /> : <ArrowDownRight className="h-3 w-3" />}
          {up ? '+' : ''}
          {kpi.deltaPct}%
        </Badge>
      </div>
      <p className="mt-3 text-2xl font-semibold text-ink">{kpi.value}</p>
      <p className="mt-0.5 text-xs text-ink-secondary">{kpi.label}</p>
      <p className="mt-0.5 text-2xs text-ink-muted">vs ayer</p>
    </motion.div>
  )
}
