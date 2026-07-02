import { CheckCircle2, Lock, ShieldAlert, UserCheck, XCircle } from 'lucide-react'
import { SectionHeader } from '@/components/ui/section-header'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { RiskBadge } from '@/components/ui/status-badges'
import { riskQueue } from '@/data/mock-news'

export default function RiskReviewPage() {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Risk Review"
        subtitle="Cola de decisiones de riesgo editorial, legal y reputacional"
      />

      <div className="grid gap-4 xl:grid-cols-2">
        {riskQueue.map((item) => (
          <div key={item.id} className="card-surface p-4">
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-center gap-2.5">
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-accent-red/10 ring-1 ring-accent-red/20">
                  <ShieldAlert className="h-4.5 w-4.5 text-accent-red" />
                </div>
                <div>
                  <p className="text-sm font-medium leading-snug text-ink">{item.title}</p>
                  <p className="text-2xs text-ink-muted">
                    {item.id} · relacionado a {item.relatedNewsId}
                  </p>
                </div>
              </div>
              <RiskBadge risk={item.level} />
            </div>

            <div className="mt-3 rounded-lg border border-line bg-surface-elevated/60 p-3">
              <p className="text-2xs font-semibold uppercase tracking-wider text-ink-muted">
                Decisión recomendada
              </p>
              <p className="mt-1 text-xs text-ink-secondary">{item.recommendation}</p>
            </div>

            <div className="mt-3 flex flex-wrap items-center gap-1.5">
              <Badge variant="neutral">severidad {item.severity}</Badge>
              {item.blocked && (
                <Badge variant="red">
                  <Lock className="h-3 w-3" />
                  publicación bloqueada
                </Badge>
              )}
              {item.humanReview && (
                <Badge variant="yellow">
                  <UserCheck className="h-3 w-3" />
                  revisión humana requerida
                </Badge>
              )}
            </div>

            {item.disclaimers.length > 0 && (
              <div className="mt-3">
                <p className="text-2xs font-semibold uppercase tracking-wider text-ink-muted">
                  Disclaimers requeridos
                </p>
                <ul className="mt-1 space-y-0.5">
                  {item.disclaimers.map((d) => (
                    <li key={d} className="text-2xs text-accent-yellow">
                      · {d}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div className="mt-4 flex gap-2 border-t border-line pt-3">
              <Button size="sm" className="flex-1">
                <CheckCircle2 className="h-3.5 w-3.5" />
                Aprobar con condiciones
              </Button>
              <Button size="sm" variant="danger" className="flex-1">
                <XCircle className="h-3.5 w-3.5" />
                Bloquear
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
