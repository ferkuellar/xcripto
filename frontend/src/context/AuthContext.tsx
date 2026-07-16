import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from 'react'
import { authApi } from '@/services/authApi'
import type { AuthMeResponse, AuthUser } from '@/types/xmip'

type AuthStatus = 'loading' | 'authenticated' | 'anonymous'

interface AuthContextValue {
  status: AuthStatus
  user: AuthUser | null
  expiresAt: string | null
  error: string | null
  refresh: () => Promise<void>
  login: (identifier: string, password: string) => Promise<void>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [status, setStatus] = useState<AuthStatus>('loading')
  const [user, setUser] = useState<AuthUser | null>(null)
  const [expiresAt, setExpiresAt] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const applySession = useCallback((payload: AuthMeResponse | null) => {
    if (payload) {
      setStatus('authenticated')
      setUser(payload.user)
      setExpiresAt(payload.session.session_expires_at)
      setError(null)
    } else {
      setStatus('anonymous')
      setUser(null)
      setExpiresAt(null)
    }
  }, [])

  const refresh = useCallback(async () => {
    try {
      const session = await authApi.me()
      applySession(session)
    } catch (err) {
      applySession(null)
      if (err instanceof Error && err.message !== 'Authentication required') {
        setError(err.message)
      } else {
        setError(null)
      }
    }
  }, [applySession])

  useEffect(() => {
    void refresh()
  }, [refresh])

  const login = useCallback(async (identifier: string, password: string) => {
    const response = await authApi.login(identifier, password)
    setStatus('authenticated')
    setUser(response.user)
    setExpiresAt(response.session.session_expires_at)
    setError(null)
  }, [])

  const logout = useCallback(async () => {
    await authApi.logout()
    applySession(null)
    setError(null)
  }, [applySession])

  const value = useMemo<AuthContextValue>(
    () => ({ status, user, expiresAt, error, refresh, login, logout }),
    [status, user, expiresAt, error, refresh, login, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
