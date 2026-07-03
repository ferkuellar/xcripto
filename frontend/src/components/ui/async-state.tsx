import type { ReactNode } from 'react'
import { AlertTriangle, Inbox, RefreshCw, ServerOff } from 'lucide-react'
import { Button } from '@/components/ui/button'
import type { ApiError } from '@/lib/api'
import { cn } from '@/lib/utils'

/** Filas skeleton para listas y tablas mientras carga el backend. */
export function SkeletonRows({ rows = 4, className }: { rows?: number; className?: string }) {
  return (
    <div className={cn('space-y-2', className)} aria-busy="true" aria-label="Cargando datos">
      {Array.from({ length: rows }, (_, i) => (
        <div key={i} className="card-surface flex items-center gap-3 p-3">
          <div className="h-8 w-8 shrink-0 animate-pulse rounded-lg bg-white/5" />
          <div className="flex-1 space-y-2">
            <div className="h-3 w-2/3 animate-pulse rounded bg-white/5" />
            <div className="h-2.5 w-1/3 animate-pulse rounded bg-white/5" />
          </div>
          <div className="h-5 w-16 animate-pulse rounded-full bg-white/5" />
        </div>
      ))}
    </div>
  )
}

/** Error del backend con acción de reintento. Distingue backend apagado de error HTTP. */
export function ErrorState({ error, onRetry }: { error: ApiError; onRetry?: () => void }) {
  const offline = error.isNetworkError
  const Icon = offline ? ServerOff : AlertTriangle
  return (
    <div className="card-surface flex flex-col items-center gap-3 p-8 text-center" role="alert">
      <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent-red/10 ring-1 ring-accent-red/20">
        <Icon className="h-5 w-5 text-accent-red" />
      </div>
      <div>
        <p className="text-sm font-medium text-ink">
          {offline ? 'Backend no disponible' : 'Error al cargar datos'}
        </p>
        <p className="mx-auto mt-1 max-w-md text-xs text-ink-secondary">{error.message}</p>
        {error.correlationId && (
          <p className="mt-1 font-mono text-2xs text-ink-muted">corr: {error.correlationId}</p>
        )}
      </div>
      {onRetry && (
        <Button size="sm" variant="secondary" onClick={onRetry}>
          <RefreshCw className="h-3 w-3" />
          Reintentar
        </Button>
      )}
    </div>
  )
}

/** Estado vacío profesional: distingue "sin datos aún" de un bug. */
export function EmptyState({
  title,
  detail,
  action,
}: {
  title: string
  detail?: string
  action?: ReactNode
}) {
  return (
    <div className="card-surface flex flex-col items-center gap-3 p-8 text-center">
      <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-white/5 ring-1 ring-line">
        <Inbox className="h-5 w-5 text-ink-muted" />
      </div>
      <div>
        <p className="text-sm font-medium text-ink">{title}</p>
        {detail && <p className="mx-auto mt-1 max-w-md text-xs text-ink-secondary">{detail}</p>}
      </div>
      {action}
    </div>
  )
}

/**
 * Etiqueta para widgets que aún muestran datos de demostración
 * (sin endpoint backend disponible todavía). Al integrar el endpoint real,
 * eliminar la etiqueta junto con el mock correspondiente en src/data/.
 */
export function DemoTag() {
  return (
    <span
      className="inline-flex items-center rounded border border-accent-yellow/30 bg-accent-yellow/10 px-1.5 py-0.5 font-mono text-2xs uppercase tracking-wider text-accent-yellow"
      title="Datos de demostración — pendiente de endpoint backend"
    >
      demo
    </span>
  )
}
