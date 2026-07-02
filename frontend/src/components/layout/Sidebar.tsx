import { NavLink } from 'react-router-dom'
import { ChevronsLeft, ChevronsRight, Zap } from 'lucide-react'
import { cn } from '@/lib/utils'
import { navItems } from '@/lib/navigation'
import { agents } from '@/data/mock-agents'

interface SidebarProps {
  collapsed: boolean
  onToggle: () => void
}

export function Sidebar({ collapsed, onToggle }: SidebarProps) {
  const activeAgents = agents.filter((a) => a.status === 'running').length

  return (
    <aside
      className={cn(
        'glass sticky top-0 z-30 flex h-screen shrink-0 flex-col border-r border-line transition-all duration-200',
        collapsed ? 'w-16' : 'w-60',
      )}
    >
      {/* Logo */}
      <div className="flex h-14 items-center gap-2.5 border-b border-line px-4">
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-accent-cyan/10 ring-1 ring-accent-cyan/30">
          <Zap className="h-4 w-4 text-accent-cyan" />
        </div>
        {!collapsed && (
          <div className="min-w-0 leading-tight">
            <p className="text-sm font-bold tracking-wide text-ink">XMIP</p>
            <p className="text-2xs text-ink-muted">by XCripto</p>
          </div>
        )}
      </div>

      {/* System status */}
      <div className={cn('border-b border-line px-4 py-3', collapsed && 'px-0 text-center')}>
        <div className={cn('flex items-center gap-2', collapsed && 'justify-center')}>
          <span className="relative flex h-2 w-2">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-accent-green opacity-60" />
            <span className="relative inline-flex h-2 w-2 rounded-full bg-accent-green" />
          </span>
          {!collapsed && <span className="text-xs text-ink-secondary">Sistema operativo</span>}
        </div>
        {!collapsed && (
          <p className="mt-1 text-2xs text-ink-muted">
            {activeAgents} agentes activos · Newsroom OS v0.1
          </p>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto px-2 py-3">
        <ul className="space-y-0.5">
          {navItems.map(({ label, path, icon: Icon }) => (
            <li key={path}>
              <NavLink
                to={path}
                end={path === '/'}
                title={collapsed ? label : undefined}
                className={({ isActive }) =>
                  cn(
                    'flex items-center gap-2.5 rounded-lg px-2.5 py-1.5 text-[13px] transition-colors',
                    collapsed && 'justify-center px-0',
                    isActive
                      ? 'bg-accent-cyan/10 text-accent-cyan'
                      : 'text-ink-secondary hover:bg-white/5 hover:text-ink',
                  )
                }
              >
                <Icon className="h-4 w-4 shrink-0" />
                {!collapsed && <span className="truncate">{label}</span>}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      {/* User */}
      <div className="border-t border-line p-3">
        <div className={cn('flex items-center gap-2.5', collapsed && 'justify-center')}>
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-accent-purple/15 text-xs font-semibold text-accent-purple ring-1 ring-accent-purple/30">
            FC
          </div>
          {!collapsed && (
            <div className="min-w-0 leading-tight">
              <p className="truncate text-xs font-medium text-ink">Fernando Cuellar</p>
              <p className="text-2xs text-ink-muted">Editor / Operator</p>
            </div>
          )}
        </div>
        <button
          onClick={onToggle}
          className="mt-3 flex w-full items-center justify-center gap-1.5 rounded-lg border border-line py-1.5 text-2xs text-ink-muted transition-colors hover:bg-white/5 hover:text-ink"
        >
          {collapsed ? <ChevronsRight className="h-3.5 w-3.5" /> : <ChevronsLeft className="h-3.5 w-3.5" />}
          {!collapsed && 'Colapsar'}
        </button>
      </div>
    </aside>
  )
}
