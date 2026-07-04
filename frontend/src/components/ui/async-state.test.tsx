import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/react'
import { EmptyState, ErrorState } from '@/components/ui/async-state'
import type { ApiError } from '@/lib/api'

function apiError(message: string, isNetworkError: boolean, correlationId: string | null = null) {
  return { message, isNetworkError, correlationId, status: isNetworkError ? 0 : 500 } as ApiError
}

describe('ErrorState', () => {
  it('shows the offline heading and the underlying message when backend is down', () => {
    render(<ErrorState error={apiError('Sin conexión con el backend XMIP', true)} />)

    expect(screen.getByText('Backend no disponible')).toBeInTheDocument()
    expect(screen.getByText('Sin conexión con el backend XMIP')).toBeInTheDocument()
  })

  it('shows the HTTP error heading and message when it is not a network error', () => {
    render(<ErrorState error={apiError('Rol sin permiso', false, 'corr-403')} />)

    expect(screen.getByText('Error al cargar datos')).toBeInTheDocument()
    expect(screen.getByText('Rol sin permiso')).toBeInTheDocument()
    expect(screen.getByText('corr: corr-403')).toBeInTheDocument()
  })
})

describe('EmptyState', () => {
  it('renders its title and detail without crashing', () => {
    render(<EmptyState title="Sin audit checks registrados" detail="Aparecerán aquí." />)

    expect(screen.getByText('Sin audit checks registrados')).toBeInTheDocument()
    expect(screen.getByText('Aparecerán aquí.')).toBeInTheDocument()
  })
})
