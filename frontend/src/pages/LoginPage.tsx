import { useEffect, useState, type FormEvent } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { AlertTriangle, ArrowRight, Loader2, LogOut, ShieldCheck } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { useAuth } from '@/context/AuthContext'

export default function LoginPage() {
  const { status, user, login, logout } = useAuth()
  const [identifier, setIdentifier] = useState('')
  const [password, setPassword] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [message, setMessage] = useState<string | null>(null)
  const [formError, setFormError] = useState<string | null>(null)
  const navigate = useNavigate()
  const location = useLocation()
  const from = (location.state as { from?: string } | null)?.from ?? '/'

  useEffect(() => {
    if (status === 'authenticated' && user) {
      setMessage(`Sesión activa para ${user.display_name}`)
    }
  }, [status, user])

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setSubmitting(true)
    setFormError(null)
    setMessage(null)
    try {
      await login(identifier, password)
      navigate(from, { replace: true })
    } catch (err) {
      setFormError(err instanceof Error ? err.message : String(err))
    } finally {
      setSubmitting(false)
    }
  }

  async function handleLogout() {
    setSubmitting(true)
    try {
      await logout()
      setMessage('Sesión cerrada')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-background p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <ShieldCheck className="h-5 w-5 text-accent-cyan" />
            Acceso administrativo
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm text-ink-secondary">
            Inicia sesión para operar el dashboard con identidad verificada por el servidor.
          </p>

          {status === 'authenticated' && user ? (
            <div className="space-y-3">
              <div className="rounded-lg border border-line bg-white/[0.02] p-3 text-sm">
                <p className="font-medium text-ink">{user.display_name}</p>
                <p className="text-2xs text-ink-muted">
                  {user.email ?? user.handle ?? user.id} · {user.role}
                </p>
              </div>
              <Button className="w-full" onClick={() => void handleLogout()} disabled={submitting}>
                <LogOut className="h-4 w-4" />
                Cerrar sesión
              </Button>
            </div>
          ) : (
            <form className="space-y-3" onSubmit={handleSubmit}>
              <Input
                value={identifier}
                onChange={(event) => setIdentifier(event.target.value)}
                placeholder="Email o usuario"
                autoComplete="username"
              />
              <Input
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                type="password"
                placeholder="Contraseña"
                autoComplete="current-password"
              />
              {formError && (
                <div className="flex items-start gap-2 rounded-lg border border-accent-red/20 bg-accent-red/5 p-3 text-xs text-ink-secondary">
                  <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-accent-red" />
                  <span>{formError}</span>
                </div>
              )}
              {message && (
                <div className="rounded-lg border border-accent-green/20 bg-accent-green/5 p-3 text-xs text-ink-secondary">
                  {message}
                </div>
              )}
              <Button className="w-full" type="submit" disabled={submitting}>
                {submitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <ArrowRight className="h-4 w-4" />}
                Entrar
              </Button>
            </form>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
