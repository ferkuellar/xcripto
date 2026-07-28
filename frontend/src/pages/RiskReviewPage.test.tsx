import { afterEach, describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import RiskReviewPage from './RiskReviewPage'
import type { RiskReviewRead } from '@/lib/api-types'

interface FakeResponseInit {
  ok: boolean
  status: number
  body?: unknown
  correlationId?: string | null
}

function fakeResponse({ ok, status, body, correlationId = null }: FakeResponseInit): Response {
  const responseBody = body === undefined && status === 204 ? undefined : body
  return {
    ok,
    status,
    headers: { get: (key: string) => (key === 'X-Correlation-ID' ? correlationId : null) },
    json: async () => responseBody,
    text: async () => (responseBody === undefined ? '' : JSON.stringify(responseBody)),
  } as unknown as Response
}

function mockFetch(body: unknown, init: Partial<FakeResponseInit> = {}) {
  const fetchMock = vi.fn().mockResolvedValue(
    fakeResponse({
      ok: init.ok ?? true,
      status: init.status ?? 200,
      body,
      correlationId: init.correlationId,
    }),
  )
  vi.stubGlobal('fetch', fetchMock)
  return fetchMock
}

const mockTokens = [
  'RSK-301',
  'RSK-302',
  'RSK-303',
  'RSK-304',
  'RSK-305',
  'NWS-1041',
  'NWS-1042',
  'NWS-1043',
  'NWS-1046',
  'NWS-1050',
]

const realReview: RiskReviewRead = {
  id: '6dd04523-3258-4f9e-8e82-3b502e9b18db',
  news_item_id: '8911a5b6-83ae-4a61-b667-4526f2db99e3',
  entity_type: 'WorkflowTask',
  entity_id: 'a5901498-a1c4-4cb9-ba95-1ddf77bd19ba',
  risk_level: 'medium',
  severity: 'R-SEV-2',
  decision_recommendation: 'allow_with_warnings',
  risk_flags: ['source_context_needed'],
  summary: 'Visa stablecoin story requires contextual review before publication.',
  required_disclaimers: ['No es asesoría financiera'],
  language_restrictions: ['No inferir adopción bancaria masiva'],
  human_review_required: true,
  publication_block_recommended: false,
  reviewer: 'editorial-control',
  correlation_id: 'corr-risk-real',
  created_at: '2026-07-18T01:30:00.000Z',
  updated_at: '2026-07-18T01:30:00.000Z',
}

describe('RiskReviewPage', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('queries the real risk reviews endpoint and shows the honest empty state for []', async () => {
    const fetchMock = mockFetch([])

    render(<RiskReviewPage />)

    expect(screen.getByLabelText('Cargando datos')).toBeInTheDocument()
    expect(await screen.findByText('No hay revisiones de riesgo registradas')).toBeInTheDocument()
    expect(
      screen.getByText('Las revisiones aparecerán aquí cuando RiskAgent complete una evaluación.'),
    ).toBeInTheDocument()

    expect(fetchMock).toHaveBeenCalledTimes(1)
    expect(String(fetchMock.mock.calls[0][0])).toBe(
      'http://localhost:8000/api/v1/risk-reviews?limit=50',
    )
    for (const token of mockTokens) {
      expect(screen.queryByText(token, { exact: false })).not.toBeInTheDocument()
    }
  })

  it('does not render mock RSK or NWS references when backend returns no reviews', async () => {
    mockFetch([])

    render(<RiskReviewPage />)

    await screen.findByText('No hay revisiones de riesgo registradas')
    const rendered = document.body.textContent ?? ''
    for (const token of mockTokens) {
      expect(rendered).not.toContain(token)
    }
  })

  it('shows backend errors without falling back to mock data and retries on demand', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(
        fakeResponse({ ok: false, status: 503, body: { error: 'Backend no listo' } }),
      )
      .mockResolvedValueOnce(fakeResponse({ ok: true, status: 200, body: [] }))
    vi.stubGlobal('fetch', fetchMock)

    render(<RiskReviewPage />)

    expect(await screen.findByText('Error al cargar datos')).toBeInTheDocument()
    expect(screen.getByText('Backend no listo')).toBeInTheDocument()
    for (const token of mockTokens) {
      expect(screen.queryByText(token, { exact: false })).not.toBeInTheDocument()
    }

    await userEvent.click(screen.getByRole('button', { name: /reintentar/i }))
    expect(await screen.findByText('No hay revisiones de riesgo registradas')).toBeInTheDocument()
    expect(fetchMock).toHaveBeenCalledTimes(2)
  })

  it('renders only backend DTO fields for real data', async () => {
    mockFetch([realReview])

    render(<RiskReviewPage />)

    expect(await screen.findByText(realReview.summary)).toBeInTheDocument()
    expect(screen.getByText(realReview.id, { exact: false })).toBeInTheDocument()
    expect(screen.getByText(realReview.news_item_id, { exact: false })).toBeInTheDocument()
    expect(screen.getByText(realReview.entity_type, { exact: false })).toBeInTheDocument()
    expect(screen.getByText(realReview.entity_id, { exact: false })).toBeInTheDocument()
    expect(screen.getByText(realReview.risk_level)).toBeInTheDocument()
    expect(screen.getByText(`severidad ${realReview.severity}`)).toBeInTheDocument()
    expect(screen.getByText(realReview.decision_recommendation)).toBeInTheDocument()
    expect(screen.getByText(realReview.risk_flags[0])).toBeInTheDocument()
    expect(screen.getByText(realReview.required_disclaimers[0], { exact: false })).toBeInTheDocument()
    expect(screen.getByText(realReview.language_restrictions[0], { exact: false })).toBeInTheDocument()
    expect(screen.getByText(`Revisor: ${realReview.reviewer}`)).toBeInTheDocument()

    for (const token of mockTokens) {
      expect(screen.queryByText(token, { exact: false })).not.toBeInTheDocument()
    }
  })

  it('keeps decision buttons disabled because no backend action contract exists', async () => {
    mockFetch([realReview])

    render(<RiskReviewPage />)

    expect(await screen.findByText(realReview.summary)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /aprobar con condiciones/i })).toBeDisabled()
    expect(screen.getByRole('button', { name: /bloquear/i })).toBeDisabled()
    expect(
      screen.getByText(
        'Acciones deshabilitadas: el backend actual solo permite crear, listar y leer RiskReviews.',
      ),
    ).toBeInTheDocument()
  })

  it('does not import riskQueue or the mock-news module', () => {
    const source = readFileSync(resolve(__dirname, 'RiskReviewPage.tsx'), 'utf8')

    expect(source).not.toContain('riskQueue')
    expect(source).not.toContain('@/data/mock-news')
  })

  it('does not contain mock identifiers in the risk page source', () => {
    const source = readFileSync(resolve(__dirname, 'RiskReviewPage.tsx'), 'utf8')

    for (const token of mockTokens) {
      expect(source).not.toContain(token)
    }
  })
})
