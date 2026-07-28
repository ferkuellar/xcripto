import { CheckCircle2, Lock, RefreshCw, ShieldAlert, UserCheck, XCircle } from 'lucide-react'
import { SectionHeader } from '@/components/ui/section-header'
import { Badge, type BadgeProps } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { EmptyState, ErrorState, SkeletonRows } from '@/components/ui/async-state'
import { useApiQuery } from '@/hooks/useApi'
import type { RiskReviewRead } from '@/lib/api-types'

type BadgeVariant = NonNullable<BadgeProps['variant']>

const riskLevelVariant: Record<string, BadgeVariant> = {
  critical: 'red',
  high: 'orange',
  medium: 'yellow',
  low: 'green',
  unknown: 'neutral',
}

function formatDate(value: string) {
  return new Date(value).toLocaleString('es-MX', { dateStyle: 'medium', timeStyle: 'short' })
}

export default function RiskReviewPage() {
  const { data, loading, error, refetch } = useApiQuery<RiskReviewRead[]>(
    '/api/v1/risk-reviews?limit=50',
  )
  const reviews = data ?? []

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <SectionHeader
          title="Risk Review"
          subtitle="Revisiones reales de riesgo editorial, legal y reputacional registradas en XMIP"
        />
        <Button size="sm" variant="secondary" onClick={refetch} disabled={loading}>
          <RefreshCw className={loading ? 'h-3.5 w-3.5 animate-spin' : 'h-3.5 w-3.5'} />
          Actualizar
        </Button>
      </div>

      {loading && <SkeletonRows rows={4} />}
      {error && <ErrorState error={error} onRetry={refetch} />}
      {!loading && !error && reviews.length === 0 && (
        <EmptyState
          title="No hay revisiones de riesgo registradas"
          detail="Las revisiones aparecerán aquí cuando RiskAgent complete una evaluación."
        />
      )}

      {!loading && !error && reviews.length > 0 && (
        <div className="grid gap-4 xl:grid-cols-2">
          {reviews.map((review) => (
            <div key={review.id} className="card-surface p-4">
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-2.5">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-accent-red/10 ring-1 ring-accent-red/20">
                    <ShieldAlert className="h-4.5 w-4.5 text-accent-red" />
                  </div>
                  <div>
                    <p className="text-sm font-medium leading-snug text-ink">
                      {review.summary}
                    </p>
                    <p className="text-2xs text-ink-muted">
                      {review.id} · news {review.news_item_id} · {review.entity_type}{' '}
                      {review.entity_id}
                    </p>
                  </div>
                </div>
                <Badge variant={riskLevelVariant[review.risk_level] ?? 'neutral'}>
                  {review.risk_level}
                </Badge>
              </div>

              <div className="mt-3 rounded-lg border border-line bg-surface-elevated/60 p-3">
                <p className="text-2xs font-semibold uppercase tracking-wider text-ink-muted">
                  Decisión recomendada
                </p>
                <p className="mt-1 text-xs text-ink-secondary">
                  {review.decision_recommendation}
                </p>
              </div>

              <div className="mt-3 flex flex-wrap items-center gap-1.5">
                <Badge variant="neutral">severidad {review.severity}</Badge>
                <Badge variant="neutral">creada {formatDate(review.created_at)}</Badge>
                {review.publication_block_recommended && (
                  <Badge variant="red">
                    <Lock className="h-3 w-3" />
                    bloqueo recomendado
                  </Badge>
                )}
                {review.human_review_required && (
                  <Badge variant="yellow">
                    <UserCheck className="h-3 w-3" />
                    revisión humana requerida
                  </Badge>
                )}
              </div>

              {review.risk_flags.length > 0 && (
                <div className="mt-3">
                  <p className="text-2xs font-semibold uppercase tracking-wider text-ink-muted">
                    Flags de riesgo
                  </p>
                  <div className="mt-1 flex flex-wrap gap-1.5">
                    {review.risk_flags.map((flag) => (
                      <Badge key={flag} variant="neutral">
                        {flag}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}

              {review.required_disclaimers.length > 0 && (
                <div className="mt-3">
                  <p className="text-2xs font-semibold uppercase tracking-wider text-ink-muted">
                    Disclaimers requeridos
                  </p>
                  <ul className="mt-1 space-y-0.5">
                    {review.required_disclaimers.map((disclaimer) => (
                      <li key={disclaimer} className="text-2xs text-accent-yellow">
                        · {disclaimer}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {review.language_restrictions.length > 0 && (
                <div className="mt-3">
                  <p className="text-2xs font-semibold uppercase tracking-wider text-ink-muted">
                    Restricciones de lenguaje
                  </p>
                  <ul className="mt-1 space-y-0.5">
                    {review.language_restrictions.map((restriction) => (
                      <li key={restriction} className="text-2xs text-ink-secondary">
                        · {restriction}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {review.reviewer && (
                <p className="mt-3 text-2xs text-ink-muted">Revisor: {review.reviewer}</p>
              )}

              <div className="mt-4 flex gap-2 border-t border-line pt-3">
                <Button
                  size="sm"
                  className="flex-1"
                  disabled
                  title="No hay endpoint backend validado para aprobar RiskReviews desde esta pantalla."
                >
                  <CheckCircle2 className="h-3.5 w-3.5" />
                  Aprobar con condiciones
                </Button>
                <Button
                  size="sm"
                  variant="danger"
                  className="flex-1"
                  disabled
                  title="No hay endpoint backend validado para bloquear RiskReviews desde esta pantalla."
                >
                  <XCircle className="h-3.5 w-3.5" />
                  Bloquear
                </Button>
              </div>
              <p className="mt-2 text-2xs text-ink-muted">
                Acciones deshabilitadas: el backend actual solo permite crear, listar y leer
                RiskReviews.
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
