/**
 * Cliente HTTP centralizado del backend XMIP.
 *
 * Configuración por entorno:
 *   VITE_API_BASE_URL  — base del backend (default: http://127.0.0.1:8000)
 *   VITE_API_KEY       — opcional; se envía como X-API-Key cuando el backend
 *                        corre con AUTH_ENABLED=true (solo endpoints de escritura)
 */

const BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000').replace(/\/$/, '')
const API_KEY: string | undefined = import.meta.env.VITE_API_KEY || undefined
const DEFAULT_TIMEOUT_MS = 12_000

export class ApiError extends Error {
  readonly status: number
  readonly correlationId: string | null

  constructor(message: string, status: number, correlationId: string | null = null) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.correlationId = correlationId
  }

  /** true cuando el backend no respondió (apagado, red, timeout). */
  get isNetworkError() {
    return this.status === 0
  }
}

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PATCH'
  body?: unknown
  signal?: AbortSignal
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS)
  options.signal?.addEventListener('abort', () => controller.abort(), { once: true })

  const headers: Record<string, string> = {}
  if (options.body !== undefined) headers['Content-Type'] = 'application/json'
  if (API_KEY && options.method && options.method !== 'GET') headers['X-API-Key'] = API_KEY

  let response: Response
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      method: options.method ?? 'GET',
      headers,
      body: options.body !== undefined ? JSON.stringify(options.body) : undefined,
      signal: controller.signal,
    })
  } catch (cause) {
    clearTimeout(timeout)
    if (options.signal?.aborted) throw cause
    throw new ApiError(
      `No se pudo contactar al backend XMIP (${BASE_URL}). Verifica que esté en ejecución.`,
      0,
    )
  }
  clearTimeout(timeout)

  if (!response.ok) {
    // El backend responde { success: false, error, correlation_id } en errores.
    let message = `HTTP ${response.status}`
    let correlationId: string | null = null
    try {
      const payload = (await response.json()) as {
        error?: string
        detail?: string
        correlation_id?: string
      }
      message = payload.error ?? payload.detail ?? message
      correlationId = payload.correlation_id ?? null
    } catch {
      /* cuerpo no-JSON: conservar mensaje HTTP */
    }
    throw new ApiError(message, response.status, correlationId)
  }

  return (await response.json()) as T
}

export const api = {
  baseUrl: BASE_URL,
  get: <T>(path: string, signal?: AbortSignal) => request<T>(path, { signal }),
  post: <T>(path: string, body?: unknown) => request<T>(path, { method: 'POST', body }),
  patch: <T>(path: string, body?: unknown) => request<T>(path, { method: 'PATCH', body }),
}

export function queryString(params: Record<string, string | number | undefined>) {
  const entries = Object.entries(params).filter(([, v]) => v !== undefined && v !== '')
  if (entries.length === 0) return ''
  return `?${entries.map(([k, v]) => `${k}=${encodeURIComponent(String(v))}`).join('&')}`
}
