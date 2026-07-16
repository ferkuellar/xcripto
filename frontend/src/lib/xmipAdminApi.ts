import type { ApiErrorPayload } from '@/types/xmip'

const BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000').replace(/\/$/, '')
const DEFAULT_TIMEOUT_MS = 12_000

function correlationId() {
  if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) return crypto.randomUUID()
  return `xmip-${Date.now()}-${Math.random().toString(16).slice(2)}`
}

export class XmipAdminApiError extends Error implements ApiErrorPayload {
  readonly status: number
  readonly correlationId: string | null

  constructor(message: string, status: number, correlationId: string | null = null) {
    super(message)
    this.name = 'XmipAdminApiError'
    this.status = status
    this.correlationId = correlationId
  }

  get isNetworkError() {
    return this.status === 0
  }
}

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PATCH'
  body?: unknown
  signal?: AbortSignal
}

async function parseError(response: Response): Promise<XmipAdminApiError> {
  let message = `HTTP ${response.status}`
  let responseCorrelationId: string | null = response.headers.get('X-Correlation-ID')
  try {
    const payload = (await response.json()) as {
      detail?: string | { msg?: string }[]
      error?: string
      correlation_id?: string
    }
    if (typeof payload.detail === 'string') message = payload.detail
    if (Array.isArray(payload.detail) && payload.detail[0]?.msg) message = payload.detail[0].msg
    if (payload.error) message = payload.error
    responseCorrelationId = payload.correlation_id ?? responseCorrelationId
  } catch {
    /* keep HTTP fallback */
  }
  return new XmipAdminApiError(message, response.status, responseCorrelationId)
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS)
  options.signal?.addEventListener('abort', () => controller.abort(), { once: true })

  const headers: Record<string, string> = {
    'X-Correlation-ID': correlationId(),
  }
  if (options.body !== undefined) headers['Content-Type'] = 'application/json'

  let response: Response
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      method: options.method ?? 'GET',
      headers,
      body: options.body !== undefined ? JSON.stringify(options.body) : undefined,
      credentials: 'include',
      signal: controller.signal,
    })
  } catch (cause) {
    clearTimeout(timeout)
    if (options.signal?.aborted) throw cause
    throw new XmipAdminApiError(
      `No se pudo contactar al backend XMIP (${BASE_URL}). Verifica /ready y CORS.`,
      0,
    )
  }
  clearTimeout(timeout)

  if (!response.ok) throw await parseError(response)
  const text = await response.text()
  if (!text) return undefined as T
  return JSON.parse(text) as T
}

export const xmipAdminApi = {
  baseUrl: BASE_URL,
  get: <T>(path: string, signal?: AbortSignal) => request<T>(path, { signal }),
  post: <T>(path: string, body?: unknown) => request<T>(path, { method: 'POST', body }),
  patch: <T>(path: string, body?: unknown) => request<T>(path, { method: 'PATCH', body }),
}
