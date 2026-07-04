import { useMemo, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { Bot, Terminal, X } from 'lucide-react'
import { SectionHeader } from '@/components/ui/section-header'
import { Badge, type BadgeProps } from '@/components/ui/badge'
import { EmptyState, ErrorState, SkeletonRows } from '@/components/ui/async-state'
import { useApiQuery } from '@/hooks/useApi'
import type { AgentExecutionRead } from '@/lib/api-types'

type BadgeVariant = NonNullable<BadgeProps['variant']>

/**
 * Registro de agentes ORION (docs/004-agentes y docs/007-prompts).
 * Es metadata de dominio, no mock data: los agentes existen aunque
 * aún no tengan ejecuciones registradas en el backend.
 */
const AGENT_REGISTRY: { name: string; role: string }[] = [
  { name: 'NewsScoutAgent', role: 'Detecta señales y noticias candidatas' },
  { name: 'SourceValidatorAgent', role: 'Evalúa fuentes, evidencia y verificación' },
  { name: 'EditorialAgent', role: 'Prioridad, ángulo y tratamiento editorial' },
  { name: 'MarketImpactAgent', role: 'Clasifica impacto de mercado sin predecir precios' },
  { name: 'RiskAgent', role: 'Riesgo editorial, legal, reputacional y financiero' },
  { name: 'ScriptAgent', role: 'Convierte briefs en guiones audiovisuales' },
  { name: 'SocialClipAgent', role: 'Variantes sociales, hooks y clips' },
  { name: 'DistributionAgent', role: 'Planea distribución multicanal trazable' },
  { name: 'AuditAgent', role: 'Trazabilidad, bloqueos y readiness' },
  { name: 'CalendarAgent', role: 'Agenda editorial y programación' },
  { name: 'MetricsAgent', role: 'Métricas operativas y de audiencia' },
  { name: 'MemoryAgent', role: 'Memoria editorial y operativa reutilizable' },
  { name: 'KnowledgeAgent', role: 'Nodos y relaciones del grafo de conocimiento' },
]

const executionStatusMap: Record<string, BadgeVariant> = {
  queued: 'blue',
  running: 'cyan',
  waiting_context: 'yellow',
  waiting_tool: 'yellow',
  waiting_approval: 'yellow',
  completed: 'green',
  completed_with_warnings: 'yellow',
  failed: 'red',
  blocked_by_policy: 'red',
  rejected: 'red',
  cancelled: 'neutral',
  retrying: 'orange',
  escalated: 'orange',
}

function formatDate(value: string | null) {
  if (!value) return '—'
  return new Date(value).toLocaleString('es-MX', { dateStyle: 'medium', timeStyle: 'short' })
}

export default function AgentsPage() {
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null)
  const { data, loading, error, refetch } = useApiQuery<AgentExecutionRead[]>(
    '/api/v1/agents/executions?limit=200',
  )

  const byAgent = useMemo(() => {
    const map = new Map<string, AgentExecutionRead[]>()
    for (const execution of data ?? []) {
      const list = map.get(execution.agent_name) ?? []
      list.push(execution)
      map.set(execution.agent_name, list)
    }
    return map
  }, [data])

  const selectedRuns = selectedAgent ? (byAgent.get(selectedAgent) ?? []) : []

  return (
    <div className="space-y-6">
      <SectionHeader
        title="Agents"
        subtitle="Los 13 agentes editoriales ORION · ejecuciones reales registradas en el backend XMIP"
      />

      {loading && <SkeletonRows rows={6} />}
      {error && <ErrorState error={error} onRetry={refetch} />}

      {!loading && !error && (
        <>
          {(data?.length ?? 0) === 0 && (
            <EmptyState
              title="Sin ejecuciones de agentes registradas"
              detail="El catálogo de agentes está definido por ORION; las tarjetas mostrarán actividad en cuanto el backend registre ejecuciones (POST /api/v1/agents/executions)."
            />
          )}
          <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
            {AGENT_REGISTRY.map((agent) => {
              const runs = byAgent.get(agent.name) ?? []
              const last = runs[0] ?? null
              const lastVariant: BadgeVariant = last
                ? (executionStatusMap[last.status] ?? 'neutral')
                : 'neutral'
              return (
                <button
                  key={agent.name}
                  onClick={() => setSelectedAgent(agent.name)}
                  className="card-surface group flex flex-col gap-2 p-4 text-left transition-colors hover:bg-white/[0.03] focus:outline-none focus:ring-1 focus:ring-accent-cyan/50"
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="flex items-center gap-2 text-sm font-semibold text-ink">
                      <Bot className="h-4 w-4 text-accent-cyan" />
                      {agent.name}
                    </span>
                    <Badge variant={lastVariant}>{last ? last.status : 'sin actividad'}</Badge>
                  </div>
                  <p className="text-2xs leading-relaxed text-ink-secondary">{agent.role}</p>
                  <div className="mt-auto flex items-center justify-between border-t border-line/50 pt-2 text-2xs text-ink-muted">
                    <span className="tabular-nums">{runs.length} ejecuciones</span>
                    <span>{last ? formatDate(last.created_at) : '—'}</span>
                  </div>
                </button>
              )
            })}
          </div>
        </>
      )}

      <AnimatePresence>
        {selectedAgent && (
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 16 }}
            transition={{ duration: 0.2 }}
            className="fixed bottom-4 right-4 z-40 w-[min(600px,calc(100vw-2rem))] rounded-xl border border-line bg-surface-elevated shadow-card"
          >
            <div className="flex items-center justify-between border-b border-line px-4 py-2.5">
              <p className="flex items-center gap-2 text-xs font-semibold text-ink">
                <Terminal className="h-3.5 w-3.5 text-accent-cyan" />
                Ejecuciones · {selectedAgent}
              </p>
              <button
                onClick={() => setSelectedAgent(null)}
                className="rounded-md p-1 text-ink-muted transition-colors hover:bg-white/5 hover:text-ink"
                aria-label="Cerrar ejecuciones"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
            <div className="max-h-72 space-y-2 overflow-y-auto p-3">
              {selectedRuns.length === 0 && (
                <p className="p-4 text-center text-2xs text-ink-muted">
                  Sin ejecuciones registradas para este agente.
                </p>
              )}
              {selectedRuns.map((run) => (
                <div key={run.id} className="rounded-lg border border-line/50 bg-surface p-3">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <span className="font-mono text-2xs text-ink-muted">
                      {run.id.slice(0, 8)} · v{run.agent_version}
                    </span>
                    <Badge variant={executionStatusMap[run.status] ?? 'neutral'}>{run.status}</Badge>
                  </div>
                  <p className="mt-1 text-2xs text-ink-secondary">
                    {run.input_ref ? `in: ${run.input_ref}` : 'sin input_ref'}
                    {run.output_ref ? ` · out: ${run.output_ref}` : ''}
                  </p>
                  {run.error_message && (
                    <p className="mt-1 text-2xs text-accent-red">{run.error_message}</p>
                  )}
                  <p className="mt-1 text-2xs text-ink-muted">
                    {formatDate(run.started_at ?? run.created_at)}
                    {run.completed_at ? ` → ${formatDate(run.completed_at)}` : ''}
                  </p>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
