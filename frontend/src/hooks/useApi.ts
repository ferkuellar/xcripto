import { useCallback, useEffect, useRef, useState } from 'react'
import { api, ApiError } from '@/lib/api'
import type { HealthResponse } from '@/lib/api-types'

export interface QueryState<T> {
  data: T | null
  loading: boolean
  error: ApiError | null
  refetch: () => void
}

/**
 * Hook genérico de lectura contra el backend XMIP.
 * Cancela requests en curso al desmontar o al cambiar el path,
 * evitando llamadas duplicadas y setState sobre componentes muertos.
 */
export function useApiQuery<T>(path: string): QueryState<T> {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<ApiError | null>(null)
  const [tick, setTick] = useState(0)
  const abortRef = useRef<AbortController | null>(null)

  useEffect(() => {
    abortRef.current?.abort()
    const controller = new AbortController()
    abortRef.current = controller
    setLoading(true)
    setError(null)

    api
      .get<T>(path, controller.signal)
      .then((result) => {
        if (!controller.signal.aborted) {
          setData(result)
          setLoading(false)
        }
      })
      .catch((err: unknown) => {
        if (controller.signal.aborted) return
        setError(err instanceof ApiError ? err : new ApiError(String(err), 0))
        setLoading(false)
      })

    return () => controller.abort()
  }, [path, tick])

  const refetch = useCallback(() => setTick((t) => t + 1), [])

  return { data, loading, error, refetch }
}

export interface ListQueryState<T> extends QueryState<T> {
  /** Total filtrado desde X-Total-Count; null si el backend no lo envía (degradar). */
  totalCount: number | null
}

/**
 * Variante de useApiQuery para listados paginados: expone el total filtrado
 * del header X-Total-Count cuando el backend lo devuelve.
 */
export function useApiListQuery<T>(path: string): ListQueryState<T> {
  const [data, setData] = useState<T | null>(null)
  const [totalCount, setTotalCount] = useState<number | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<ApiError | null>(null)
  const [tick, setTick] = useState(0)
  const abortRef = useRef<AbortController | null>(null)

  useEffect(() => {
    abortRef.current?.abort()
    const controller = new AbortController()
    abortRef.current = controller
    setLoading(true)
    setError(null)

    api
      .getWithMeta<T>(path, controller.signal)
      .then((result) => {
        if (!controller.signal.aborted) {
          setData(result.data)
          const total = result.headers.get('X-Total-Count')
          setTotalCount(total !== null && !Number.isNaN(Number(total)) ? Number(total) : null)
          setLoading(false)
        }
      })
      .catch((err: unknown) => {
        if (controller.signal.aborted) return
        setError(err instanceof ApiError ? err : new ApiError(String(err), 0))
        setLoading(false)
      })

    return () => controller.abort()
  }, [path, tick])

  const refetch = useCallback(() => setTick((t) => t + 1), [])

  return { data, totalCount, loading, error, refetch }
}

export type BackendStatus = 'checking' | 'online' | 'offline'

/** Estado vivo del backend vía GET /health, con re-chequeo periódico. */
export function useBackendHealth(intervalMs = 30_000) {
  const [status, setStatus] = useState<BackendStatus>('checking')
  const [info, setInfo] = useState<HealthResponse | null>(null)

  useEffect(() => {
    let cancelled = false

    const check = () => {
      api
        .get<HealthResponse>('/health')
        .then((health) => {
          if (!cancelled) {
            setInfo(health)
            setStatus(health.status === 'ok' ? 'online' : 'offline')
          }
        })
        .catch(() => {
          if (!cancelled) setStatus('offline')
        })
    }

    check()
    const id = setInterval(check, intervalMs)
    return () => {
      cancelled = true
      clearInterval(id)
    }
  }, [intervalMs])

  return { status, info }
}
