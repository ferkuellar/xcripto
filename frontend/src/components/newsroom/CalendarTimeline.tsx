import { CalendarClock, Lock } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge, type BadgeProps } from '@/components/ui/badge'
import { RiskBadge } from '@/components/ui/status-badges'
import { scheduledPublications } from '@/data/mock-news'
import type { ScheduledPublication } from '@/data/types'

type BadgeVariant = NonNullable<BadgeProps['variant']>

const statusMap: Record<ScheduledPublication['status'], { variant: BadgeVariant; label: string }> = {
  ready: { variant: 'green', label: 'ready' },
  pending_deps: { variant: 'yellow', label: 'pending deps' },
  blocked: { variant: 'red', label: 'blocked' },
  published: { variant: 'neutral', label: 'published' },
}

export function CalendarTimeline({ items = scheduledPublications }: { items?: ScheduledPublication[] }) {
  const days = [...new Set(items.map((i) => i.day))]

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <CalendarClock className="h-4 w-4 text-accent-cyan" />
          Distribution Calendar
        </CardTitle>
        <CardDescription>Publicaciones programadas por canal (datos de demostración)</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {days.map((day) => (
          <div key={day}>
            <p className="mb-2 text-2xs font-semibold uppercase tracking-wider text-ink-muted">
              {day}
            </p>
            <div className="space-y-2 border-l border-line pl-3">
              {items
                .filter((i) => i.day === day)
                .map((item) => {
                  const status = statusMap[item.status]
                  return (
                    <div
                      key={item.id}
                      className="relative rounded-lg border border-line bg-surface-elevated/60 p-3"
                    >
                      <span className="absolute -left-[17px] top-4 h-2 w-2 rounded-full bg-accent-cyan/60 ring-2 ring-background" />
                      <div className="flex flex-wrap items-center gap-1.5">
                        <span className="text-xs font-semibold tabular-nums text-ink">{item.time}</span>
                        <Badge variant="blue">{item.channel}</Badge>
                        <Badge variant={status.variant}>{status.label}</Badge>
                        <RiskBadge risk={item.risk} />
                      </div>
                      <p className="mt-1.5 text-xs text-ink">{item.title}</p>
                      <div className="mt-1 flex items-center justify-between gap-2 text-2xs text-ink-muted">
                        <span>métrica esperada: {item.expectedMetric}</span>
                        {item.missingDeps.length > 0 && (
                          <span className="flex items-center gap-1 text-accent-red">
                            <Lock className="h-3 w-3" />
                            falta: {item.missingDeps.join(', ')}
                          </span>
                        )}
                      </div>
                    </div>
                  )
                })}
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}
