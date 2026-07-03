import { useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { Bell, Bot, Plus, Search } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { DemoTag } from '@/components/ui/async-state'
import { useBackendHealth } from '@/hooks/useApi'
import { notifications } from '@/data/mock-news'

const operationalDate = new Date().toLocaleDateString('es-MX', {
  weekday: 'long',
  day: 'numeric',
  month: 'long',
  year: 'numeric',
})

export function Topbar() {
  const [showNotifications, setShowNotifications] = useState(false)
  const unread = notifications.filter((n) => n.unread).length
  const navigate = useNavigate()
  const { status: backendStatus, info } = useBackendHealth()

  return (
    <header className="glass sticky top-0 z-20 flex h-14 items-center gap-3 border-b border-line px-4">
      {/* Global search */}
      <div className="relative w-full max-w-sm">
        <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-muted" />
        <input
          placeholder="Buscar noticias, fuentes, agentes…"
          aria-label="Buscar en el newsroom"
          className="h-9 w-full rounded-lg border border-line bg-surface pl-9 pr-3 text-sm text-ink placeholder:text-ink-muted focus:outline-none focus:ring-1 focus:ring-accent-cyan/50"
        />
      </div>

      <div className="ml-auto flex items-center gap-2">
        {/* Estado del sistema — vivo, desde GET /health */}
        <div className="hidden items-center gap-2 lg:flex">
          <span className="text-xs capitalize text-ink-muted">{operationalDate}</span>
          {backendStatus === 'online' && (
            <Badge variant="green">XMIP online · {info?.version}</Badge>
          )}
          {backendStatus === 'offline' && <Badge variant="red">XMIP sin conexión</Badge>}
          {backendStatus === 'checking' && <Badge variant="neutral">conectando…</Badge>}
        </div>

        <Button variant="secondary" size="sm" onClick={() => navigate('/intake')}>
          <Plus className="h-3.5 w-3.5" />
          New Intake
        </Button>
        <Button size="sm" onClick={() => navigate('/agents')}>
          <Bot className="h-3.5 w-3.5" />
          Agents
        </Button>

        {/* Notifications (demo — pendiente de endpoint de notificaciones) */}
        <div className="relative">
          <button
            onClick={() => setShowNotifications((v) => !v)}
            className="relative flex h-9 w-9 items-center justify-center rounded-lg border border-line text-ink-secondary transition-colors hover:bg-white/5 hover:text-ink"
            aria-label="Notificaciones"
          >
            <Bell className="h-4 w-4" />
            {unread > 0 && (
              <span className="absolute -right-0.5 -top-0.5 flex h-4 w-4 items-center justify-center rounded-full bg-accent-red text-2xs font-semibold text-white">
                {unread}
              </span>
            )}
          </button>

          <AnimatePresence>
            {showNotifications && (
              <motion.div
                initial={{ opacity: 0, y: -6 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -6 }}
                transition={{ duration: 0.15 }}
                className="absolute right-0 top-11 w-80 rounded-xl border border-line bg-surface-elevated p-2 shadow-card"
              >
                <p className="flex items-center gap-2 px-2 py-1 text-xs font-semibold text-ink">
                  Notificaciones <DemoTag />
                </p>
                {notifications.map((n) => (
                  <div
                    key={n.id}
                    className="flex items-start gap-2 rounded-lg px-2 py-2 transition-colors hover:bg-white/5"
                  >
                    <span
                      className={
                        n.unread
                          ? 'mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-accent-cyan'
                          : 'mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-white/10'
                      }
                    />
                    <div className="min-w-0">
                      <p className="text-xs font-medium text-ink">{n.title}</p>
                      <p className="text-2xs text-ink-secondary">{n.detail}</p>
                      <p className="mt-0.5 text-2xs text-ink-muted">{n.time}</p>
                    </div>
                  </div>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </header>
  )
}
