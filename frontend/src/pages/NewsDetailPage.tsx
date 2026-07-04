import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import {
  ArrowLeft,
  Calculator,
  ExternalLink,
  FileSearch,
  GitBranch,
  Radar,
  ShieldAlert,
  ShieldCheck,
} from 'lucide-react'
import { Badge, type BadgeProps } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { PriorityBadge } from '@/components/ui/status-badges'
import { EmptyState, ErrorState, SkeletonRows } from '@/components/ui/async-state'
import { useApiQuery } from '@/hooks/useApi'
import { api, ApiError } from '@/lib/api'
import {
  allowedNewsTransitions,
  type AuditCheckRead,
  type EditorialReadinessScoreRead,
  type IntakeSignalRead,
  type NewsRead,
  type RiskReviewRead,
  type VerificationRecordRead,
} from '@/lib/api-types'

type BadgeVariant = NonNullable<BadgeProps['variant']>

const newsStatusVariant: Record<string, BadgeVariant> = {
  detected: 'blue',
  registered: 'blue',
  classified: 'cyan',
  validating: 'yellow',
  verified: 'green',
  partially_verified: 'yellow',
  rumor: 'orange',
  monitoring: 'blue',
  rejected: 'red',
  prioritized: 'cyan',
  drafting: 'cyan',
  reviewing: 'yellow',
  approved: 'green',
  scheduled: 'cyan',
  published: 'green',
  distributed: 'cyan',
  measured: 'neutral',
  archived: 'neutral',
  corrected: 'orange',
  retracted: 'red',
  escalated: 'orange',
}

const riskLevelVariant: Record<string, BadgeVariant> = {
  critical: 'red',
  high: 'orange',
  medium: 'yellow',
  low: 'green',
  unknown: 'neutral',
}

function formatDate(value: string | null | undefined) {
  if (!value) return '—'
  return new Date(value).toLocaleString('es-MX', { dateStyle: 'medium', timeStyle: 'short' })
}

function statusBadge(status: string) {
  return <Badge variant={newsStatusVariant[status] ?? 'neutral'}>{status}</Badge>
}

export default function NewsDetailPage() {
  const { id = '' } = useParams()
  const news = useApiQuery<NewsRead>(`/api/v1/news/${id}`)

  if (news.loading) {
    return (
      <div className="space-y-6">
        <BackLink />
        <SkeletonRows rows={6} />
      </div>
    )
  }

  if (news.error) {
    if (news.error.status === 404) {
      return (
        <div className="space-y-6">
          <BackLink />
          <EmptyState
            title="Noticia no encontrada"
            detail={`No existe una noticia con id "${id}" en el backend XMIP. Puede haber sido eliminada o el enlace es incorrecto.`}
            action={
              <Button size="sm" variant="secondary" onClick={() => history.back()}>
                <ArrowLeft className="h-3 w-3" />
                Volver
              </Button>
            }
          />
        </div>
      )
    }
    return (
      <div className="space-y-6">
        <BackLink />
        <ErrorState error={news.error} onRetry={news.refetch} />
      </div>
    )
  }

  const item = news.data
  if (!item) return null

  return (
    <div className="space-y-6">
      <BackLink />

      {/* Header editorial */}
      <header className="card-surface p-5">
        <div className="flex flex-wrap items-center gap-2">
          <PriorityBadge priority={item.priority} />
          {statusBadge(item.status)}
          <Badge variant="neutral">{item.category}</Badge>
          <span className="ml-auto font-mono text-2xs text-ink-muted">news · {item.id}</span>
        </div>
        <h1 className="mt-3 text-xl font-semibold leading-snug tracking-tight text-ink lg:text-2xl">
          {item.title}
        </h1>
        <p className="mt-2 text-2xs text-ink-muted">
          Registrada {formatDate(item.created_at)} · actualizada {formatDate(item.updated_at)}
        </p>
      </header>

      <div className="grid gap-4 xl:grid-cols-3">
        {/* Columna principal */}
        <div className="space-y-4 xl:col-span-2">
          {/* Resumen ejecutivo */}
          <section className="card-surface p-5">
            <h2 className="text-xs font-semibold uppercase tracking-wider text-ink-muted">
              Resumen ejecutivo
            </h2>
            <p className="mt-2 whitespace-pre-wrap text-sm leading-relaxed text-ink-secondary">
              {item.summary}
            </p>
            <p className="mt-4 border-t border-line/50 pt-3 text-2xs text-ink-muted">
              El cuerpo editorial completo se gestiona como Content Piece en fases posteriores del
              pipeline; esta ficha muestra el registro de intake verificado.
            </p>
          </section>

          <ReadinessSection newsId={item.id} />
          <VerificationSection newsId={item.id} />
          <RiskSection newsId={item.id} />
          <AuditSection newsId={item.id} />
          <OriginSection newsId={item.id} />
        </div>

        {/* Panel lateral: metadata + fuente + acciones */}
        <aside className="space-y-4">
          <StatusActions item={item} onChanged={news.refetch} />

          <section className="card-surface p-4">
            <h2 className="text-xs font-semibold uppercase tracking-wider text-ink-muted">
              Fuente declarada
            </h2>
            <p className="mt-2 text-sm font-medium text-ink">{item.source_name}</p>
            <a
              href={item.source_url}
              target="_blank"
              rel="noreferrer noopener"
              className="mt-1 inline-flex items-center gap-1 break-all text-2xs text-ink-secondary transition-colors hover:text-accent-cyan"
            >
              {item.source_url}
              <ExternalLink className="h-2.5 w-2.5 shrink-0" />
            </a>
            <p className="mt-3 border-t border-line/50 pt-2 text-2xs text-ink-muted">
              La noticia declara fuente denormalizada (nombre + URL). El vínculo con el registro de
              fuentes (trust tier, estado) no está disponible en la API actual.
            </p>
          </section>

          <section className="card-surface p-4">
            <h2 className="text-xs font-semibold uppercase tracking-wider text-ink-muted">
              Metadata
            </h2>
            <dl className="mt-2 space-y-2 text-2xs">
              <MetaRow label="ID" value={item.id} mono />
              {item.correlation_id && (
                <MetaRow label="Correlation ID" value={item.correlation_id} mono />
              )}
              <MetaRow label="Status" value={item.status} />
              <MetaRow label="Categoría" value={item.category} />
              <MetaRow label="Prioridad" value={item.priority} />
              <MetaRow label="Creada" value={formatDate(item.created_at)} />
              <MetaRow label="Actualizada" value={formatDate(item.updated_at)} />
            </dl>
          </section>
        </aside>
      </div>
    </div>
  )
}

function BackLink() {
  return (
    <Link
      to="/"
      className="inline-flex items-center gap-1.5 text-xs text-ink-secondary transition-colors hover:text-ink"
    >
      <ArrowLeft className="h-3.5 w-3.5" />
      Volver al Command Center
    </Link>
  )
}

function MetaRow({ label, value, mono = false }: { label: string; value: string; mono?: boolean }) {
  return (
    <div className="flex items-start justify-between gap-3">
      <dt className="shrink-0 text-ink-muted">{label}</dt>
      <dd className={`break-all text-right text-ink-secondary ${mono ? 'font-mono' : ''}`}>
        {value}
      </dd>
    </div>
  )
}

/** Acción real: PATCH /news/{id}/status con máquina de estados del backend. */
function StatusActions({ item, onChanged }: { item: NewsRead; onChanged: () => void }) {
  const transitions = allowedNewsTransitions(item.status)
  const [target, setTarget] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function apply() {
    if (!target) return
    setBusy(true)
    setError(null)
    try {
      await api.patch(`/api/v1/news/${item.id}/status`, { status: target })
      setTarget('')
      onChanged()
    } catch (err) {
      setError(err instanceof ApiError ? err.message : String(err))
    } finally {
      setBusy(false)
    }
  }

  return (
    <section className="card-surface p-4">
      <h2 className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-ink-muted">
        <GitBranch className="h-3.5 w-3.5" />
        Transición de estado
      </h2>
      {transitions.length === 0 ? (
        <p className="mt-2 text-2xs text-ink-muted">
          Estado final: <span className="font-medium text-ink-secondary">{item.status}</span>. Sin
          transiciones disponibles.
        </p>
      ) : (
        <>
          <div className="mt-2 flex gap-2">
            <select
              value={target}
              onChange={(e) => setTarget(e.target.value)}
              aria-label="Nuevo estado editorial"
              className="h-9 w-full rounded-lg border border-line bg-surface px-2 text-sm text-ink focus:outline-none focus:ring-1 focus:ring-accent-cyan/50"
            >
              <option value="">{item.status} → …</option>
              {transitions.map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>
            <Button size="sm" disabled={!target || busy} onClick={apply}>
              {busy ? 'Aplicando…' : 'Aplicar'}
            </Button>
          </div>
          <p className="mt-2 text-2xs text-ink-muted">
            El backend valida la transición y los gates editoriales (p. ej. audit check aprobado
            antes de publicar).
          </p>
        </>
      )}
      {error && (
        <p className="mt-2 rounded-lg border border-accent-red/30 bg-accent-red/10 px-2 py-1.5 text-2xs text-accent-red" role="alert">
          {error}
        </p>
      )}
    </section>
  )
}

/** Editorial readiness real: GET latest + acción real POST calculate. */
function ReadinessSection({ newsId }: { newsId: string }) {
  const readiness = useApiQuery<EditorialReadinessScoreRead>(
    `/api/v1/editorial-readiness/news/${newsId}/latest`,
  )
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function calculate() {
    setBusy(true)
    setError(null)
    try {
      await api.post(`/api/v1/editorial-readiness/news/${newsId}/calculate`)
      readiness.refetch()
    } catch (err) {
      setError(err instanceof ApiError ? err.message : String(err))
    } finally {
      setBusy(false)
    }
  }

  const notCalculated = readiness.error?.status === 404
  const score = readiness.data

  return (
    <section className="card-surface p-5">
      <div className="flex items-center justify-between gap-2">
        <h2 className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-ink-muted">
          <Calculator className="h-3.5 w-3.5" />
          Editorial readiness
        </h2>
        <Button size="sm" variant="secondary" disabled={busy} onClick={calculate}>
          {busy ? 'Calculando…' : score ? 'Recalcular' : 'Calcular'}
        </Button>
      </div>

      {readiness.loading && <div className="mt-3 h-16 animate-pulse rounded-lg bg-white/5" />}
      {notCalculated && (
        <p className="mt-3 text-2xs text-ink-muted">
          Aún no se ha calculado el readiness score de esta noticia. El cálculo es determinístico
          sobre fuentes, verificación, riesgo y audit.
        </p>
      )}
      {readiness.error && !notCalculated && (
        <p className="mt-3 text-2xs text-accent-red">{readiness.error.message}</p>
      )}
      {error && <p className="mt-3 text-2xs text-accent-red" role="alert">{error}</p>}

      {score && (
        <div className="mt-3 space-y-3">
          <div className="flex flex-wrap items-center gap-3">
            <span className="text-3xl font-semibold tabular-nums text-ink">
              {Math.round(score.score)}
            </span>
            <Badge variant={score.score >= 70 ? 'green' : score.score >= 40 ? 'yellow' : 'red'}>
              {score.score_band}
            </Badge>
            <Badge variant="neutral">{score.readiness_status}</Badge>
            <span className="ml-auto text-2xs text-ink-muted">{formatDate(score.created_at)}</span>
          </div>
          <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-2xs sm:grid-cols-3">
            {(
              [
                ['Fuentes', score.source_score],
                ['Verificación', score.verification_score],
                ['Riesgo', score.risk_score],
                ['Editorial', score.editorial_score],
                ['Audit', score.audit_score],
              ] as const
            ).map(([label, value]) => (
              <div key={label} className="flex items-center justify-between gap-2">
                <span className="text-ink-muted">{label}</span>
                <span className="font-medium tabular-nums text-ink-secondary">
                  {Math.round(value)}
                </span>
              </div>
            ))}
          </div>
          {score.blocking_reasons.length > 0 && (
            <div className="flex flex-wrap gap-1.5">
              {score.blocking_reasons.map((reason) => (
                <Badge key={reason} variant="red">
                  {reason}
                </Badge>
              ))}
            </div>
          )}
          {score.missing_requirements.length > 0 && (
            <div className="flex flex-wrap gap-1.5">
              {score.missing_requirements.map((req) => (
                <Badge key={req} variant="orange">
                  falta: {req}
                </Badge>
              ))}
            </div>
          )}
          {score.recommended_next_action && (
            <p className="border-t border-line/50 pt-2 text-2xs text-ink-secondary">
              Siguiente acción recomendada: {score.recommended_next_action}
            </p>
          )}
        </div>
      )}
    </section>
  )
}

function VerificationSection({ newsId }: { newsId: string }) {
  const { data, loading, error, refetch } = useApiQuery<VerificationRecordRead[]>(
    `/api/v1/news/${newsId}/verification-records`,
  )

  return (
    <section className="card-surface p-5">
      <h2 className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-ink-muted">
        <ShieldCheck className="h-3.5 w-3.5" />
        Verificación de evidencia
      </h2>
      {loading && <div className="mt-3 h-14 animate-pulse rounded-lg bg-white/5" />}
      {error && <ErrorState error={error} onRetry={refetch} />}
      {!loading && !error && (data?.length ?? 0) === 0 && (
        <p className="mt-3 text-2xs text-ink-muted">
          Sin registros de verificación. Esta noticia no debe avanzar a publicación sin evidencia
          verificada (regla ORION: nada sensible se publica sin verificación).
        </p>
      )}
      {(data ?? []).map((record) => (
        <div key={record.id} className="mt-3 rounded-lg border border-line/50 bg-surface p-3">
          <div className="flex flex-wrap items-center gap-1.5">
            <Badge
              variant={
                record.verification_status === 'verified'
                  ? 'green'
                  : record.verification_status === 'rejected'
                    ? 'red'
                    : 'yellow'
              }
            >
              {record.verification_status}
            </Badge>
            <Badge variant="neutral">evidencia: {record.evidence_level}</Badge>
            <Badge variant="neutral">confianza: {record.confidence_level}</Badge>
            {record.human_review_required && <Badge variant="orange">requiere revisión humana</Badge>}
            <span className="ml-auto text-2xs text-ink-muted">{formatDate(record.created_at)}</span>
          </div>
          <p className="mt-2 text-xs leading-relaxed text-ink-secondary">{record.summary}</p>
          {record.verified_claims.length > 0 && (
            <p className="mt-2 text-2xs text-accent-green">
              ✓ Verificado: {record.verified_claims.join(' · ')}
            </p>
          )}
          {record.unverified_claims.length > 0 && (
            <p className="mt-1 text-2xs text-accent-yellow">
              ? Sin verificar: {record.unverified_claims.join(' · ')}
            </p>
          )}
          {record.contradictions.length > 0 && (
            <p className="mt-1 text-2xs text-accent-red">
              ✗ Contradicciones: {record.contradictions.join(' · ')}
            </p>
          )}
          {record.reviewer && (
            <p className="mt-2 text-2xs text-ink-muted">Revisor: {record.reviewer}</p>
          )}
        </div>
      ))}
    </section>
  )
}

function RiskSection({ newsId }: { newsId: string }) {
  const { data, loading, error, refetch } = useApiQuery<RiskReviewRead[]>(
    `/api/v1/news/${newsId}/risk-reviews`,
  )

  return (
    <section className="card-surface p-5">
      <h2 className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-ink-muted">
        <ShieldAlert className="h-3.5 w-3.5" />
        Revisión de riesgo
      </h2>
      {loading && <div className="mt-3 h-14 animate-pulse rounded-lg bg-white/5" />}
      {error && <ErrorState error={error} onRetry={refetch} />}
      {!loading && !error && (data?.length ?? 0) === 0 && (
        <p className="mt-3 text-2xs text-ink-muted">
          Sin revisiones de riesgo registradas para esta noticia.
        </p>
      )}
      {(data ?? []).map((review) => (
        <div key={review.id} className="mt-3 rounded-lg border border-line/50 bg-surface p-3">
          <div className="flex flex-wrap items-center gap-1.5">
            <Badge variant={riskLevelVariant[review.risk_level] ?? 'neutral'}>
              riesgo: {review.risk_level}
            </Badge>
            <Badge variant="neutral">{review.severity}</Badge>
            {review.publication_block_recommended && (
              <Badge variant="red">bloqueo de publicación recomendado</Badge>
            )}
            {review.human_review_required && <Badge variant="orange">revisión humana</Badge>}
            <span className="ml-auto text-2xs text-ink-muted">{formatDate(review.created_at)}</span>
          </div>
          <p className="mt-2 text-xs leading-relaxed text-ink-secondary">{review.summary}</p>
          <p className="mt-1 text-2xs text-ink-secondary">
            Recomendación: {review.decision_recommendation}
          </p>
          {review.risk_flags.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-1.5">
              {review.risk_flags.map((flag) => (
                <Badge key={flag} variant="neutral">
                  {flag}
                </Badge>
              ))}
            </div>
          )}
          {review.required_disclaimers.length > 0 && (
            <p className="mt-2 text-2xs text-ink-muted">
              Disclaimers requeridos: {review.required_disclaimers.join(' · ')}
            </p>
          )}
        </div>
      ))}
    </section>
  )
}

function AuditSection({ newsId }: { newsId: string }) {
  const { data, loading, error, refetch } = useApiQuery<AuditCheckRead[]>(
    `/api/v1/audit/checks?entity_type=news_item&entity_id=${encodeURIComponent(newsId)}&limit=20`,
  )

  return (
    <section className="card-surface p-5">
      <h2 className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-ink-muted">
        <FileSearch className="h-3.5 w-3.5" />
        Audit checks
      </h2>
      {loading && <div className="mt-3 h-14 animate-pulse rounded-lg bg-white/5" />}
      {error && <ErrorState error={error} onRetry={refetch} />}
      {!loading && !error && (data?.length ?? 0) === 0 && (
        <p className="mt-3 text-2xs text-ink-muted">
          Sin audit checks para esta noticia. Las transiciones sensibles (aprobar, publicar)
          requieren un audit check aprobado — el backend las bloqueará hasta entonces.
        </p>
      )}
      {(data ?? []).map((check) => (
        <div key={check.id} className="mt-3 rounded-lg border border-line/50 bg-surface p-3">
          <div className="flex flex-wrap items-center gap-1.5">
            <Badge
              variant={
                check.audit_status === 'pass'
                  ? 'green'
                  : check.audit_status === 'fail'
                    ? 'red'
                    : check.audit_status === 'warning'
                      ? 'yellow'
                      : 'blue'
              }
            >
              {check.audit_status}
            </Badge>
            <Badge variant={riskLevelVariant[check.severity] ?? 'neutral'}>{check.severity}</Badge>
            {check.publication_block_recommended && (
              <Badge variant="red">bloquea publicación</Badge>
            )}
            {check.ready_to_advance && <Badge variant="green">ready to advance</Badge>}
            <span className="ml-auto text-2xs text-ink-muted">{formatDate(check.created_at)}</span>
          </div>
          {check.decision_recommendation && (
            <p className="mt-2 text-xs text-ink-secondary">{check.decision_recommendation}</p>
          )}
          {check.missing_requirements.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-1.5">
              {check.missing_requirements.map((req) => (
                <Badge key={req} variant="orange">
                  falta: {req}
                </Badge>
              ))}
            </div>
          )}
          {check.correlation_id && (
            <p className="mt-2 font-mono text-2xs text-ink-muted">corr: {check.correlation_id}</p>
          )}
        </div>
      ))}
    </section>
  )
}

/** Señal de intake que originó esta noticia (trazabilidad hacia atrás). */
function OriginSection({ newsId }: { newsId: string }) {
  const { data, loading, error, refetch } = useApiQuery<IntakeSignalRead[]>(
    `/api/v1/intake/signals?promoted_news_item_id=${encodeURIComponent(newsId)}&limit=5`,
  )

  return (
    <section className="card-surface p-5">
      <h2 className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-ink-muted">
        <Radar className="h-3.5 w-3.5" />
        Origen · señal de intake
      </h2>
      {loading && <div className="mt-3 h-14 animate-pulse rounded-lg bg-white/5" />}
      {error && <ErrorState error={error} onRetry={refetch} />}
      {!loading && !error && (data?.length ?? 0) === 0 && (
        <p className="mt-3 text-2xs text-ink-muted">
          Esta noticia no proviene de una señal de intake registrada (pudo crearse por intake
          directo).
        </p>
      )}
      {(data ?? []).map((signal) => (
        <div key={signal.id} className="mt-3 rounded-lg border border-line/50 bg-surface p-3">
          <div className="flex flex-wrap items-center gap-1.5">
            <Badge variant="cyan">{signal.signal_type}</Badge>
            <Badge variant="neutral">dedupe: {signal.dedupe_status}</Badge>
            {signal.adapter_name && <Badge variant="neutral">{signal.adapter_name}</Badge>}
            <span className="ml-auto text-2xs text-ink-muted">{formatDate(signal.created_at)}</span>
          </div>
          <p className="mt-2 text-xs text-ink-secondary">
            {signal.normalized_title ?? signal.raw_title}
          </p>
          <p className="mt-1 font-mono text-2xs text-ink-muted">
            señal {signal.id.slice(0, 8)} · hash {signal.content_hash.slice(0, 12)}…
            {signal.correlation_id ? ` · corr ${signal.correlation_id}` : ''}
          </p>
        </div>
      ))}
    </section>
  )
}
