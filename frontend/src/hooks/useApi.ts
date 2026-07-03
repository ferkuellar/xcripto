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
