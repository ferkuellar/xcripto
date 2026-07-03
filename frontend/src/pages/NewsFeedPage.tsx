import { useMemo, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import {
  ArrowRight,
  ChevronLeft,
  ChevronRight,
  FilterX,
  RefreshCw,
  Search,
  X,
} from 'lucide-react'
import { SectionHeader } from '@/components/ui/section-header'
import { Badge, type BadgeProps } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { PriorityBadge } from '@/components/ui/status-badges'
import { EmptyState, ErrorState, SkeletonRows } from '@/components/ui/async-state'
import { useApiQuery, useBackendHealth } from '@/hooks/useApi'
import { queryString } from '@/lib/api'
import type { NewsPriority, NewsRead } from '@/lib/api-types'
import { cn } from '@/lib/utils'

type BadgeVariant = NonNullable<BadgeProps['variant']>

const PAGE_SIZE = 50

// Catálogo NEWS_STATUSES del backend (filtro backend-side vía ?status=).
const statusFilters = [
  'todos',
  'detected',
  'registered',
  'classified',
  'validating',
  'verified',
  'partially_verified',
  'rumor',
  'monitoring',
  'prioritized',
  'drafting',
  'reviewing',
  'approved',
  'scheduled',
  'published',
  'distributed',
  'rejected',
  'archived',
] as const

const priorityFilters = ['Todas', 'P0', 'P1', 'P2', 'P3', 'P4'] as const

const statusVariant: Record<string, BadgeVariant> = {
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

function formatDate(value: string) {
  return new Date(value).toLocaleString('es-MX', { dateStyle: 'medium', timeStyle: 'short' })
}

export default function NewsFeedPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [search, setSearch] = useState(searchParams.get('q') ?? '')
  const [status, setStatus] = useState<string>('todos')
  const [priority, setPriority] = useState<string>('Todas')
  const [category, setCategory] = useState<string>('todas')
  const [source, setSource] = useState<string>('todas')
  const [page, setPage] = useState(0)
  const [lastRefreshed, setLastRefreshed] = useState<Date>(new Date())

  const { status: backendStatus, info } = useBackendHealth()

  // status/limit/offset son los únicos filtros que soporta GET /api/v1/news.
  const query = queryString({
    status: status === 'todos' ? undefined : status,
    limit: PAGE_SIZE,
    offset: page * PAGE_SIZE,
  })
  const { data, loading, error, refetch } = useApiQuery<NewsRead[]>(`/api/v1/news${query}`)

  // Catálogos derivados de los datos reales cargados (no inventados).
  const categories = useMemo(
    () => ['todas', ...new Set((data ?? []).map((n) => n.category))],
    [data],
  )
  const sources = useMemo(
    () => ['todas', ...new Set((data ?? []).map((n) => n.source_name))],
    [data],
  )

  // Búsqueda + categoría/prioridad/fuente son client-side sobre la página
  // cargada: la API aún no expone search ni esos filtros. Al existir en
  // backend, mover a queryString y eliminar este bloque.
  const items = useMemo(() => {
    const term = search.trim().toLowerCase()
    return (data ?? []).filter(
      (n) =>
        (priority === 'Todas' || n.priority === priority) &&
        (category === 'todas' || n.category === category) &&
        (source === 'todas' || n.source_name === source) &&
        (!term ||
          n.title.toLowerCase().includes(term) ||
          n.summary.toLowerCase().includes(term) ||
          n.source_name.toLowerCase().includes(term) ||
          n.category.toLowerCase().includes(term)),
    )
  }, [data, search, priority, category, source])

  const hasActiveFilters =
    search !== '' || status !== 'todos' || priority !== 'Todas' || category !== 'todas' || source !== 'todas'
  const hasNextPage = (data?.length ?? 0) === PAGE_SIZE

  function updateSearch(value: string) {
    setSearch(value)
    setSearchParams(value ? { q: value } : {}, { replace: true })
  }

  function resetFilters() {
    updateSearch('')
    setStatus('todos')
    setPriority('Todas')
    setCategory('todas')
    setSource('todas')
    setPage(0)
  }

  function manualRefetch() {
    setLastRefreshed(new Date())
    refetch()
  }

  const selectClass =
    'h-8 rounded-lg border border-line bg-surface px-2 text-2xs text-ink focus:outline-none focus:ring-1 focus:ring-accent-cyan/50'

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-start justify-between gap-3">
        <SectionHeader
          title="News Feed"
          subtitle="Feed editorial de XCripto · registro completo de noticias del backend XMIP"
        />
        <div className="flex items-center gap-2">
          {backendStatus === 'online' && <Badge variant="green">XMIP online · {info?.version}</Badge>}
          {backendStatus === 'offline' && <Badge variant="red">XMIP sin conexión</Badge>}
          <Button size="sm" variant="secondary" onClick={manualRefetch} disabled={loading}>
            <RefreshCw className={cn('h-3.5 w-3.5', loading && 'animate-spin')} />
            Actualizar
          </Button>
        </div>
      </div>
      <p className="-mt-4 text-2xs text-ink-muted">
        {items.length} noticias en vista · página {page + 1} · actualizado{' '}
        {lastRefreshed.toLocaleTimeString('es-MX')}
      </p>

      {/* Búsqueda */}
      <div className="relative max-w-md">
        <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-muted" />
        <input
          value={search}
          onChange={(e) => updateSearch(e.target.value)}
          placeholder="Buscar por título, resumen, fuente o categoría…"
          aria-label="Buscar noticias"
          className="h-9 w-full rounded-lg border border-line bg-surface pl-9 pr-8 text-sm text-ink placeholder:text-ink-muted focus:outline-none focus:ring-1 focus:ring-accent-cyan/50"
        />
        {search && (
          <button
            onClick={() => updateSearch('')}
            aria-label="Limpiar búsqueda"
            className="absolute right-2 top-1/2 -translate-y-1/2 rounded p-0.5 text-ink-muted transition-colors hover:text-ink"
          >
            <X className="h-3.5 w-3.5" />
          </button>
        )}
      </div>

      {/* Filtros */}
      <div className="space-y-2">
        <div className="flex flex-wrap items-center gap-1">
          <span className="mr-1 text-2xs text-ink-muted">Estado:</span>
          {statusFilters.map((s) => (
            <button
              key={s}
              onClick={() => {
                setStatus(s)
                setPage(0)
              }}
              className={cn(
                'rounded-md px-2 py-1 text-2xs transition-colors',
                status === s
                  ? 'bg-accent-cyan/15 text-accent-cyan'
                  : 'text-ink-secondary hover:bg-white/5',
              )}
            >
              {s}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <label className="flex items-center gap-1.5 text-2xs text-ink-muted">
            Prioridad:
            <select value={priority} onChange={(e) => setPriority(e.target.value)} className={selectClass}>
              {priorityFilters.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))}
            </select>
          </label>
          <label className="flex items-center gap-1.5 text-2xs text-ink-muted">
            Categoría:
            <select value={category} onChange={(e) => setCategory(e.target.value)} className={selectClass}>
              {categories.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </label>
          <label className="flex items-center gap-1.5 text-2xs text-ink-muted">
            Fuente:
            <select value={source} onChange={(e) => setSource(e.target.value)} className={selectClass}>
              {sources.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </label>
          {hasActiveFilters && (
            <Button size="sm" variant="secondary" onClick={resetFilters}>
              <FilterX className="h-3 w-3" />
              Limpiar filtros
            </Button>
          )}
        </div>
      </div>

      {loading && <SkeletonRows rows={8} />}
      {error && <ErrorState error={error} onRetry={manualRefetch} />}
      {!loading && !error && items.length === 0 && (
        <EmptyState
          title={hasActiveFilters ? 'Sin resultados con los filtros activos' : 'Sin noticias registradas'}
          detail={
            hasActiveFilters
              ? 'Los filtros de prioridad, categoría, fuente y búsqueda operan sobre la página cargada. Limpia los filtros o cambia de página/estado.'
              : 'Las noticias aparecen aquí al promover señales desde News Intake o registrar intake directo.'
          }
          action={
            hasActiveFilters ? (
              <Button size="sm" variant="secondary" onClick={resetFilters}>
                <FilterX className="h-3 w-3" />
                Limpiar filtros
              </Button>
            ) : undefined
          }
        />
      )}

      {/* Tabla editorial */}
      {!loading && !error && items.length > 0 && (
        <div className="card-surface overflow-x-auto">
          <table className="w-full min-w-[880px] text-left text-xs">
            <thead>
              <tr className="border-b border-line text-2xs uppercase tracking-wider text-ink-muted">
                <th className="px-4 py-3 font-medium">Noticia</th>
                <th className="px-3 py-3 font-medium">Estado</th>
                <th className="px-3 py-3 font-medium">Categoría</th>
                <th className="px-3 py-3 font-medium">Prioridad</th>
                <th className="px-3 py-3 font-medium">Fuente</th>
                <th className="px-3 py-3 font-medium">Registrada</th>
                <th className="px-3 py-3 text-right font-medium">Ficha</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr
                  key={item.id}
                  className="border-b border-line/50 transition-colors last:border-0 hover:bg-white/[0.02]"
                >
                  <td className="max-w-[380px] px-4 py-3">
                    <Link
                      to={`/news/${item.id}`}
                      className="line-clamp-2 font-medium text-ink transition-colors hover:text-accent-cyan"
                    >
                      {item.title}
                    </Link>
                    <p className="mt-0.5 truncate text-2xs text-ink-muted">{item.summary}</p>
                  </td>
                  <td className="px-3 py-3">
                    <Badge variant={statusVariant[item.status] ?? 'neutral'}>{item.status}</Badge>
                  </td>
                  <td className="px-3 py-3 text-ink-secondary">{item.category}</td>
                  <td className="px-3 py-3">
                    <PriorityBadge priority={item.priority as NewsPriority} compact />
                  </td>
                  <td className="max-w-[160px] truncate px-3 py-3 text-ink-secondary">
                    {item.source_name}
                  </td>
                  <td className="whitespace-nowrap px-3 py-3 text-ink-muted">
                    {formatDate(item.created_at)}
                  </td>
                  <td className="px-3 py-3">
                    <div className="flex justify-end">
                      <Link
                        to={`/news/${item.id}`}
                        aria-label={`Abrir ficha de ${item.title}`}
                        className="flex h-7 w-7 items-center justify-center rounded-lg border border-line text-ink-secondary transition-colors hover:bg-white/5 hover:text-accent-cyan"
                      >
                        <ArrowRight className="h-3.5 w-3.5" />
                      </Link>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Paginación backend real (limit/offset; la API no expone total) */}
      {!error && (page > 0 || hasNextPage) && (
        <div className="flex items-center justify-between">
          <Button
            size="sm"
            variant="secondary"
            disabled={page === 0 || loading}
            onClick={() => setPage((p) => Math.max(0, p - 1))}
          >
            <ChevronLeft className="h-3.5 w-3.5" />
            Anterior
          </Button>
          <span className="text-2xs tabular-nums text-ink-muted">Página {page + 1}</span>
          <Button
            size="sm"
            variant="secondary"
            disabled={!hasNextPage || loading}
            onClick={() => setPage((p) => p + 1)}
          >
            Siguiente
            <ChevronRight className="h-3.5 w-3.5" />
          </Button>
        </div>
      )}

      <p className="text-2xs text-ink-muted">
        Confidence, impacto y readiness score se consultan en la ficha de cada noticia (el listado
        del backend no los incluye; se evita hacer N+1 llamadas por fila). Filtro de estado y
        paginación: backend. Búsqueda, prioridad, categoría y fuente: sobre la página cargada.
      </p>
    </div>
  )
}
