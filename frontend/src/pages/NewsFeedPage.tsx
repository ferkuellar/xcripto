import { useEffect, useMemo, useRef, useState } from 'react'
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
import { useApiListQuery, useBackendHealth } from '@/hooks/useApi'
import { queryString } from '@/lib/api'
import type { NewsPriority, NewsRead } from '@/lib/api-types'
import { cn } from '@/lib/utils'

type BadgeVariant = NonNullable<BadgeProps['variant']>

const PAGE_SIZE = 50

// Catálogo NEWS_STATUSES del backend.
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

/** Rango compacto de páginas: 1 … p-1 p p+1 … total */
function pageRange(current: number, total: number): (number | '…')[] {
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1)
  const pages = new Set<number>([1, total, current - 1, current, current + 1])
  const sorted = [...pages].filter((p) => p >= 1 && p <= total).sort((a, b) => a - b)
  const result: (number | '…')[] = []
  let prev = 0
  for (const p of sorted) {
    if (p - prev > 1) result.push('…')
    result.push(p)
    prev = p
  }
  return result
}

export default function NewsFeedPage() {
  // La URL es la fuente de verdad de todos los filtros (compartible).
  const [searchParams, setSearchParams] = useSearchParams()
  const q = searchParams.get('q') ?? ''
  const status = searchParams.get('status') ?? 'todos'
  const priority = searchParams.get('priority') ?? 'Todas'
  const category = searchParams.get('category') ?? 'todas'
  const source = searchParams.get('source') ?? 'todas'
  const createdFrom = searchParams.get('from') ?? ''
  const createdTo = searchParams.get('to') ?? ''
  const page = Math.max(1, Number(searchParams.get('page') ?? '1') || 1)

  const [lastRefreshed, setLastRefreshed] = useState<Date>(new Date())
  const { status: backendStatus, info } = useBackendHealth()

  // Todos los filtros viajan al backend (autoritativo); nada se filtra localmente.
  const query = queryString({
    q: q || undefined,
    status: status === 'todos' ? undefined : status,
    priority: priority === 'Todas' ? undefined : priority,
    category: category === 'todas' ? undefined : category,
    source: source === 'todas' ? undefined : source,
    created_from: createdFrom || undefined,
    created_to: createdTo || undefined,
    limit: PAGE_SIZE,
    offset: (page - 1) * PAGE_SIZE,
  })
  const { data, totalCount, loading, error, refetch } = useApiListQuery<NewsRead[]>(
    `/api/v1/news${query}`,
  )
  const items = useMemo(() => data ?? [], [data])

  // Búsqueda con debounce: el input local se consolida a la URL a los 350 ms
  // para no disparar un request al backend por cada tecla.
  const [searchInput, setSearchInput] = useState(q)
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  useEffect(() => setSearchInput(q), [q])

  function setParam(key: string, value: string | null, resetPage = true) {
    const next = new URLSearchParams(searchParams)
    if (value === null || value === '') next.delete(key)
    else next.set(key, value)
    if (resetPage) next.delete('page')
    setSearchParams(next, { replace: true })
  }

  function onSearchChange(value: string) {
    setSearchInput(value)
    if (debounceRef.current) clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => setParam('q', value.trim() || null), 350)
  }

  function resetFilters() {
    if (debounceRef.current) clearTimeout(debounceRef.current)
    setSearchInput('')
    setSearchParams({}, { replace: true })
  }

  function goToPage(target: number) {
    setParam('page', target <= 1 ? null : String(target), false)
  }

  function manualRefetch() {
    setLastRefreshed(new Date())
    refetch()
  }

  // Catálogos visuales derivados de la página actual (limitación conocida:
  // no hay endpoint de catálogo de categorías/fuentes; el valor elegido sí
  // se envía al backend y filtra sobre todo el histórico).
  const categories = useMemo(
    () => ['todas', ...new Set([...items.map((n) => n.category), ...(category !== 'todas' ? [category] : [])])],
    [items, category],
  )
  const sources = useMemo(
    () => ['todas', ...new Set([...items.map((n) => n.source_name), ...(source !== 'todas' ? [source] : [])])],
    [items, source],
  )

  const hasActiveFilters =
    q !== '' || status !== 'todos' || priority !== 'Todas' || category !== 'todas' ||
    source !== 'todas' || createdFrom !== '' || createdTo !== ''

  // Paginación: con total real cuando llega X-Total-Count; degradación al
  // comportamiento anterior (siguiente si la página vino llena) si no llega.
  const totalPages = totalCount !== null ? Math.max(1, Math.ceil(totalCount / PAGE_SIZE)) : null
  const hasNextPage = totalPages !== null ? page < totalPages : items.length === PAGE_SIZE
  const pageOutOfRange =
    totalCount !== null && totalCount > 0 && items.length === 0 && page > 1
  const rangeStart = (page - 1) * PAGE_SIZE + 1
  const rangeEnd = (page - 1) * PAGE_SIZE + items.length

  const selectClass =
    'h-8 rounded-lg border border-line bg-surface px-2 text-2xs text-ink focus:outline-none focus:ring-1 focus:ring-accent-cyan/50'

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-start justify-between gap-3">
        <SectionHeader
          title="News Feed"
          subtitle="Feed editorial de XCripto · búsqueda y filtros sobre todo el histórico (backend)"
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
        {totalCount !== null
          ? items.length > 0
            ? `Mostrando ${rangeStart}–${rangeEnd} de ${totalCount} resultados · página ${page}${totalPages ? ` de ${totalPages}` : ''}`
            : `${totalCount} resultados`
          : `${items.length} noticias en vista · página ${page}`}
        {' · actualizado '}
        {lastRefreshed.toLocaleTimeString('es-MX')}
      </p>

      {/* Búsqueda backend (q) */}
      <div className="relative max-w-md">
        <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-muted" />
        <input
          value={searchInput}
          onChange={(e) => onSearchChange(e.target.value)}
          placeholder="Buscar en todo el histórico (título, resumen, fuente, categoría)…"
          aria-label="Buscar noticias"
          className="h-9 w-full rounded-lg border border-line bg-surface pl-9 pr-8 text-sm text-ink placeholder:text-ink-muted focus:outline-none focus:ring-1 focus:ring-accent-cyan/50"
        />
        {searchInput && (
          <button
            onClick={() => onSearchChange('')}
            aria-label="Limpiar búsqueda"
            className="absolute right-2 top-1/2 -translate-y-1/2 rounded p-0.5 text-ink-muted transition-colors hover:text-ink"
          >
            <X className="h-3.5 w-3.5" />
          </button>
        )}
      </div>

      {/* Filtros backend-side */}
      <div className="space-y-2">
        <div className="flex flex-wrap items-center gap-1">
          <span className="mr-1 text-2xs text-ink-muted">Estado:</span>
          {statusFilters.map((s) => (
            <button
              key={s}
              onClick={() => setParam('status', s === 'todos' ? null : s)}
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
            <select
              value={priority}
              onChange={(e) => setParam('priority', e.target.value === 'Todas' ? null : e.target.value)}
              className={selectClass}
            >
              {priorityFilters.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))}
            </select>
          </label>
          <label className="flex items-center gap-1.5 text-2xs text-ink-muted">
            Categoría:
            <select
              value={category}
              onChange={(e) => setParam('category', e.target.value === 'todas' ? null : e.target.value)}
              className={selectClass}
            >
              {categories.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </label>
          <label className="flex items-center gap-1.5 text-2xs text-ink-muted">
            Fuente:
            <select
              value={source}
              onChange={(e) => setParam('source', e.target.value === 'todas' ? null : e.target.value)}
              className={selectClass}
            >
              {sources.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </label>
          <label className="flex items-center gap-1.5 text-2xs text-ink-muted">
            Desde:
            <input
              type="date"
              value={createdFrom}
              onChange={(e) => setParam('from', e.target.value || null)}
              className={selectClass}
              aria-label="Creadas desde"
            />
          </label>
          <label className="flex items-center gap-1.5 text-2xs text-ink-muted">
            Hasta:
            <input
              type="date"
              value={createdTo}
              onChange={(e) => setParam('to', e.target.value || null)}
              className={selectClass}
              aria-label="Creadas hasta"
            />
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

      {pageOutOfRange && !loading && !error && (
        <EmptyState
          title={`La página ${page} no existe para estos filtros`}
          detail={`Hay ${totalCount} resultados en ${totalPages} página${totalPages === 1 ? '' : 's'}.`}
          action={
            <Button size="sm" variant="secondary" onClick={() => goToPage(1)}>
              Ir a página 1
            </Button>
          }
        />
      )}

      {!loading && !error && !pageOutOfRange && items.length === 0 && (
        <EmptyState
          title={hasActiveFilters ? 'Sin resultados con los filtros activos' : 'Sin noticias registradas'}
          detail={
            hasActiveFilters
              ? 'La búsqueda y los filtros se aplican en el backend sobre todo el histórico. Ajusta o limpia los filtros.'
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

      {/* Paginación numerada con total real (degrada a anterior/siguiente sin total) */}
      {!error && (page > 1 || hasNextPage) && (
        <div className="flex flex-wrap items-center justify-between gap-2">
          <Button
            size="sm"
            variant="secondary"
            disabled={page <= 1 || loading}
            onClick={() => goToPage(page - 1)}
          >
            <ChevronLeft className="h-3.5 w-3.5" />
            Anterior
          </Button>
          {totalPages !== null ? (
            <div className="flex items-center gap-1">
              {pageRange(page, totalPages).map((p, i) =>
                p === '…' ? (
                  <span key={`gap-${i}`} className="px-1 text-2xs text-ink-muted">
                    …
                  </span>
                ) : (
                  <button
                    key={p}
                    onClick={() => goToPage(p)}
                    disabled={loading}
                    aria-current={p === page ? 'page' : undefined}
                    className={cn(
                      'h-7 min-w-7 rounded-md px-1.5 text-2xs tabular-nums transition-colors',
                      p === page
                        ? 'bg-accent-cyan/15 font-semibold text-accent-cyan'
                        : 'text-ink-secondary hover:bg-white/5',
                    )}
                  >
                    {p}
                  </button>
                ),
              )}
            </div>
          ) : (
            <span className="text-2xs tabular-nums text-ink-muted">Página {page}</span>
          )}
          <Button
            size="sm"
            variant="secondary"
            disabled={!hasNextPage || loading}
            onClick={() => goToPage(page + 1)}
          >
            Siguiente
            <ChevronRight className="h-3.5 w-3.5" />
          </Button>
        </div>
      )}

      <p className="text-2xs text-ink-muted">
        Búsqueda, estado, prioridad, categoría, fuente, fechas y paginación se resuelven en el
        backend sobre todo el histórico. Los catálogos visibles de categoría y fuente se derivan de
        la página actual (limitación visual hasta tener endpoint de catálogos). Confidence, impacto
        y readiness se consultan en la ficha de cada noticia.
      </p>
    </div>
  )
}
