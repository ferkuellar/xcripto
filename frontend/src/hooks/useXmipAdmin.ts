import { useCallback, useEffect, useRef, useState } from 'react'
import { XmipAdminApiError } from '@/lib/xmipAdminApi'

export interface AdminQueryState<T> {
  data: T | null
  loading: boolean
  error: XmipAdminApiError | null
  refetch: () => void
}

export function useXmipAdminQuery<T>(
  loader: (signal: AbortSignal) => Promise<T>,
): AdminQueryState<T> {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<XmipAdminApiError | null>(null)
  const [tick, setTick] = useState(0)
  const abortRef = useRef<AbortController | null>(null)

  useEffect(() => {
    abortRef.current?.abort()
    const controller = new AbortController()
    abortRef.current = controller
    setLoading(true)
    setError(null)

    loader(controller.signal)
      .then((result) => {
        if (!controller.signal.aborted) {
          setData(result)
          setLoading(false)
        }
      })
      .catch((err: unknown) => {
        if (controller.signal.aborted) return
        setError(err instanceof XmipAdminApiError ? err : new XmipAdminApiError(String(err), 0))
        setLoading(false)
      })

    return () => controller.abort()
  }, [loader, tick])

  const refetch = useCallback(() => setTick((current) => current + 1), [])

  return { data, loading, error, refetch }
}
