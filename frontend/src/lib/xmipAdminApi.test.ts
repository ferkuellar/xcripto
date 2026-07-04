import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

interface FakeResponseInit {
  ok: boolean
  status: number
  body?: unknown
  correlationId?: string | null
}

function fakeResponse({ ok, status, body = {}, correlationId = null }: FakeResponseInit): Response {
  return {
    ok,
    status,
    headers: { get: (key: string) => (key === 'X-Correlation-ID' ? correlationId : null) },
    json: async () => body,
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
    vi.stubEnv('VITE_API_KEY', 'super-secret-key')
    vi.stubEnv('VITE_ACTOR_ROLE', 'admin')
    vi.stubEnv('VITE_ACTOR_ID', 'local-admin')
  })

  afterEach(() => {
    vi.unstubAllEnvs()
    vi.unstubAllGlobals()
  })

  it('sends X-API-Key, X-Actor-Role, X-Actor-Id and a correlation id from env', async () => {
    const fetchMock = vi.fn().mockResolvedValue(fakeResponse({ ok: true, status: 200 }))
    vi.stubGlobal('fetch', fetchMock)

    const { xmipAdminApi } = await loadApi()
    await xmipAdminApi.get('/api/v1/admin/dashboard/overview')

    expect(fetchMock).toHaveBeenCalledTimes(1)
    const [url, init] = fetchMock.mock.calls[0]
    expect(url).toBe('http://backend.test/api/v1/admin/dashboard/overview')
    const headers = (init as { headers: Record<string, string> }).headers
    expect(headers['X-API-Key']).toBe('super-secret-key')
    expect(headers['X-Actor-Role']).toBe('admin')
    expect(headers['X-Actor-Id']).toBe('local-admin')
    expect(headers['X-Correlation-ID']).toBeTruthy()
  })

  it('omits auth/actor headers when env vars are empty', async () => {
    vi.stubEnv('VITE_API_KEY', '')
    vi.stubEnv('VITE_ACTOR_ROLE', '')
    vi.stubEnv('VITE_ACTOR_ID', '')
    const fetchMock = vi.fn().mockResolvedValue(fakeResponse({ ok: true, status: 200 }))
    vi.stubGlobal('fetch', fetchMock)

    const { xmipAdminApi } = await loadApi()
    await xmipAdminApi.get('/x')

    const headers = lastFetchInit(fetchMock).headers
    expect(headers['X-API-Key']).toBeUndefined()
    expect(headers['X-Actor-Role']).toBeUndefined()
    expect(headers['X-Actor-Id']).toBeUndefined()
  })
})

describe('xmipAdminApi error handling', () => {
  beforeEach(() => {
    vi.resetModules()
    vi.stubEnv('VITE_API_BASE_URL', 'http://backend.test')
    vi.stubEnv('VITE_API_KEY', 'super-secret-key')
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

  it('maps backend offline (fetch reject) to a network error without leaking the API key', async () => {
    const fetchMock = vi.fn().mockRejectedValue(new TypeError('Failed to fetch'))
    vi.stubGlobal('fetch', fetchMock)

    const { xmipAdminApi } = await loadApi()
    const error = await xmipAdminApi.get('/x').catch((e) => e)

    expect(error.status).toBe(0)
    expect(error.isNetworkError).toBe(true)
    expect(error.message).not.toContain('super-secret-key')
    expect(error.message).toContain('backend.test')
  })
})
