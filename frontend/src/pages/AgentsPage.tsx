import { useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { Terminal, X } from 'lucide-react'
import { SectionHeader } from '@/components/ui/section-header'
import { AgentCard } from '@/components/agents/AgentCard'
import { agentLogs, agents } from '@/data/mock-agents'

export default function AgentsPage() {
  const [logsFor, setLogsFor] = useState<string | null>(null)
  const selected = agents.find((a) => a.id === logsFor)
  const logs = logsFor ? (agentLogs[logsFor] ?? ['Sin logs recientes para este agente.']) : []

  return (
    <div className="space-y-6">
      <SectionHeader
        title="Agents"
        subtitle="Control center de los 13 agentes editoriales · modos operativos A0 (manual) a A4 (autónomo)"
      />

      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
        {agents.map((agent) => (
          <AgentCard key={agent.id} agent={agent} onViewLogs={setLogsFor} />
        ))}
      </div>

      <AnimatePresence>
        {selected && (
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 16 }}
            transition={{ duration: 0.2 }}
            className="fixed bottom-4 right-4 z-40 w-[min(560px,calc(100vw-2rem))] rounded-xl border border-line bg-surface-elevated shadow-card"
          >
            <div className="flex items-center justify-between border-b border-line px-4 py-2.5">
              <p className="flex items-center gap-2 text-xs font-semibold text-ink">
                <Terminal className="h-3.5 w-3.5 text-accent-cyan" />
                Logs · {selected.name}
              </p>
              <button
                onClick={() => setLogsFor(null)}
                className="rounded-md p-1 text-ink-muted transition-colors hover:bg-white/5 hover:text-ink"
                aria-label="Cerrar logs"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
            <div className="max-h-64 overflow-y-auto p-4">
              <pre className="whitespace-pre-wrap font-mono text-2xs leading-relaxed text-ink-secondary">
                {logs.join('\n')}
              </pre>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
