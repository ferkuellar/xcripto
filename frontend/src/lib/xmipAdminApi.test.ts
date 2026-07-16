import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

interface FakeResponseInit {
  ok: boolean
  status: number
  body?: unknown
  correlationId?: string | null
}

function fakeResponse({ ok, status, body, correlationId = null }: FakeResponseInit): Response {
  const responseBody = body === undefined && status === 204 ? undefined : body
  const text = async () => (responseBody === undefined ? '' : JSON.stringify(responseBody))
  return {
    ok,
    status,
    headers: { get: (key: string) => (key === 'X-Correlation-ID' ? correlationId : null) },
    json: async () => responseBody,
    text,
  } as unknown as Response
}

async function loadApi() {
  return import('@/lib/xmipAdminApi')
}

function lastFetchInit(fetchMock: ReturnType<typeof vi.fn>) {
  return fetchMock.mock.calls[0][1] as { headers: Record<string, string> }
}

describe('xmipAdminApi request headers', () => {
  beforeEach(() => {
    vi.resetModules()
    vi.stubEnv('VITE_API_BASE_URL', 'http://backend.test')
  })

  afterEach(() => {
    vi.unstubAllEnvs()
    vi.unstubAllGlobals()
  })

  it('sends a correlation id and includes browser credentials', async () => {
    const fetchMock = vi.fn().mockResolvedValue(fakeResponse({ ok: true, status: 200 }))
    vi.stubGlobal('fetch', fetchMock)

    const { xmipAdminApi } = await loadApi()
    await xmipAdminApi.get('/api/v1/admin/dashboard/overview')

    expect(fetchMock).toHaveBeenCalledTimes(1)
    const [url, init] = fetchMock.mock.calls[0]
    expect(url).toBe('http://backend.test/api/v1/admin/dashboard/overview')
    const headers = (init as { headers: Record<string, string> }).headers
    expect(headers['X-Correlation-ID']).toBeTruthy()
    expect((init as { credentials: string }).credentials).toBe('include')
  })

  it('omits auth headers entirely', async () => {
    const fetchMock = vi.fn().mockResolvedValue(fakeResponse({ ok: true, status: 200 }))
    vi.stubGlobal('fetch', fetchMock)

    const { xmipAdminApi } = await loadApi()
    await xmipAdminApi.get('/x')

    const headers = lastFetchInit(fetchMock).headers
    expect(headers['X-API-Key']).toBeUndefined()
    expect(headers['X-Actor-Role']).toBeUndefined()
    expect(headers['X-Actor-Id']).toBeUndefined()
  })

  it('handles 204 no-content responses without parsing errors', async () => {
    const fetchMock = vi.fn().mockResolvedValue(fakeResponse({ ok: true, status: 204, body: undefined }))
    vi.stubGlobal('fetch', fetchMock)

    const { xmipAdminApi } = await loadApi()
    await expect(xmipAdminApi.post('/api/v1/auth/logout')).resolves.toBeUndefined()
  })
})

describe('xmipAdminApi error handling', () => {
  beforeEach(() => {
    vi.resetModules()
    vi.stubEnv('VITE_API_BASE_URL', 'http://backend.test')
  })

  afterEach(() => {
    vi.unstubAllEnvs()
    vi.unstubAllGlobals()
  })

  it('maps 401 to a clear error carrying status and correlation id', async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      fakeResponse({
        ok: false,
        status: 401,
        body: { error: 'API key requerida' },
        correlationId: 'corr-401',
      }),
    )
    vi.stubGlobal('fetch', fetchMock)

    const { xmipAdminApi, XmipAdminApiError } = await loadApi()
    const error = await xmipAdminApi.get('/x').catch((e) => e)

    expect(error).toBeInstanceOf(XmipAdminApiError)
    expect(error.status).toBe(401)
    expect(error.message).toBe('API key requerida')
    expect(error.correlationId).toBe('corr-401')
    expect(error.isNetworkError).toBe(false)
  })

  it('maps 403 to a clear permission error', async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      fakeResponse({ ok: false, status: 403, body: { error: 'Rol sin permiso' } }),
    )
    vi.stubGlobal('fetch', fetchMock)

    const { xmipAdminApi } = await loadApi()
    const error = await xmipAdminApi.get('/x').catch((e) => e)

    expect(error.status).toBe(403)
    expect(error.message).toBe('Rol sin permiso')
  })

  it('maps backend offline (fetch reject) to a network error without leaking secrets', async () => {
    const fetchMock = vi.fn().mockRejectedValue(new TypeError('Failed to fetch'))
    vi.stubGlobal('fetch', fetchMock)

    const { xmipAdminApi } = await loadApi()
    const error = await xmipAdminApi.get('/x').catch((e) => e)

    expect(error.status).toBe(0)
    expect(error.isNetworkError).toBe(true)
    expect(error.message).toContain('backend.test')
  })
})
