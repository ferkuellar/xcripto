import { ArrowUpRight, Bot, Clock, Link2 } from 'lucide-react'
import { motion } from 'framer-motion'
import { PriorityBadge, RiskBadge, VerificationBadge } from '@/components/ui/status-badges'
import type { NewsItem } from '@/data/types'

export function NewsCard({ item }: { item: NewsItem }) {
  return (
    <motion.div
      whileHover={{ y: -2 }}
      transition={{ duration: 0.15 }}
      className="group rounded-lg border border-line bg-surface-elevated/80 p-3 shadow-card"
    >
      <div className="flex items-center justify-between gap-2">
        <span className="text-2xs font-medium text-ink-muted">{item.id}</span>
        <PriorityBadge priority={item.priority} compact />
      </div>
      <p className="mt-1.5 line-clamp-2 text-[13px] font-medium leading-snug text-ink">
        {item.title}
      </p>
      <p className="mt-1 text-2xs text-ink-muted">{item.category}</p>

      <div className="mt-2 flex flex-wrap gap-1">
        <VerificationBadge status={item.verification} />
        <RiskBadge risk={item.risk} />
      </div>

      {item.missing.length > 0 && (
        <p className="mt-2 rounded-md border border-accent-red/20 bg-accent-red/5 px-2 py-1 text-2xs text-accent-red">
          Falta: {item.missing.join(', ')}
        </p>
      )}

      <div className="mt-2 space-y-1 text-2xs text-ink-secondary">
        <p className="flex items-center gap-1.5">
          <Link2 className="h-3 w-3 shrink-0 text-ink-muted" />
          <span className="truncate">{item.source}</span>
        </p>
        <p className="flex items-center gap-1.5">
          <Bot className="h-3 w-3 shrink-0 text-ink-muted" />
          {item.agent}
        </p>
        <p className="flex items-center gap-1.5">
          <Clock className="h-3 w-3 shrink-0 text-ink-muted" />
          {item.timestamp}
        </p>
      </div>

      <button className="mt-2.5 flex w-full items-center justify-center gap-1 rounded-md border border-line py-1 text-2xs font-medium text-ink-secondary opacity-0 transition-all hover:bg-white/5 hover:text-ink group-hover:opacity-100">
        Open
        <ArrowUpRight className="h-3 w-3" />
      </button>
    </motion.div>
  )
}
