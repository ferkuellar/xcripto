import { Bot, FileText, Play, Timer } from 'lucide-react'
import { motion } from 'framer-motion'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { StatusBadge } from '@/components/ui/status-badges'
import type { Agent } from '@/data/types'

export function AgentCard({ agent, onViewLogs }: { agent: Agent; onViewLogs?: (id: string) => void }) {
  return (
    <motion.div
      whileHover={{ y: -2 }}
      transition={{ duration: 0.15 }}
      className="card-surface flex flex-col p-3.5"
    >
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-2">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-accent-purple/10 ring-1 ring-accent-purple/25">
            <Bot className="h-3.5 w-3.5 text-accent-purple" />
          </div>
          <div className="leading-tight">
            <p className="text-[13px] font-semibold text-ink">{agent.name}</p>
            <p className="text-2xs text-ink-muted">
              {agent.id} · modo {agent.mode}
            </p>
          </div>
        </div>
        <StatusBadge status={agent.status} />
      </div>

      <p className="mt-2.5 line-clamp-2 text-xs text-ink-secondary">{agent.currentTask}</p>

      <div className="mt-2.5 flex flex-wrap items-center gap-1.5 text-2xs text-ink-muted">
        <Badge variant="neutral">
          <Timer className="h-3 w-3" />
          {agent.avgRuntime}
        </Badge>
        <Badge variant="neutral">outputs: {agent.outputCount}</Badge>
        <span className="ml-auto">última ejecución {agent.lastRun}</span>
      </div>

      <div className="mt-3 flex gap-2 border-t border-line pt-2.5">
        <Button size="sm" className="flex-1">
          <Play className="h-3 w-3" />
          Run
        </Button>
        <Button size="sm" variant="outline" className="flex-1" onClick={() => onViewLogs?.(agent.id)}>
          <FileText className="h-3 w-3" />
          View logs
        </Button>
      </div>
    </motion.div>
  )
}
