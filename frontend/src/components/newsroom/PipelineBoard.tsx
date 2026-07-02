import { newsItems } from '@/data/mock-news'
import type { PipelineStage } from '@/data/types'
import { NewsCard } from './NewsCard'
import { cn } from '@/lib/utils'

const stages: { id: PipelineStage; label: string; tone: string }[] = [
  { id: 'detected', label: 'Detected', tone: 'bg-ink-muted' },
  { id: 'validating', label: 'Validating', tone: 'bg-accent-blue' },
  { id: 'risk_review', label: 'Risk Review', tone: 'bg-accent-orange' },
  { id: 'drafting', label: 'Drafting', tone: 'bg-accent-purple' },
  { id: 'reviewing', label: 'Reviewing', tone: 'bg-accent-yellow' },
  { id: 'approved', label: 'Approved', tone: 'bg-accent-green' },
  { id: 'scheduled', label: 'Scheduled', tone: 'bg-accent-cyan' },
  { id: 'published', label: 'Published', tone: 'bg-ink-secondary' },
]

export function PipelineBoard() {
  return (
    <div className="-mx-1 overflow-x-auto pb-2">
      <div className="flex min-w-max gap-3 px-1">
        {stages.map((stage) => {
          const items = newsItems.filter((n) => n.stage === stage.id)
          return (
            <div key={stage.id} className="w-64 shrink-0">
              <div className="mb-2 flex items-center gap-2 px-1">
                <span className={cn('h-1.5 w-1.5 rounded-full', stage.tone)} />
                <span className="text-xs font-semibold text-ink">{stage.label}</span>
                <span className="ml-auto rounded-md bg-white/5 px-1.5 text-2xs tabular-nums text-ink-muted">
                  {items.length}
                </span>
              </div>
              <div className="space-y-2 rounded-xl border border-line/60 bg-surface/50 p-2 min-h-[80px]">
                {items.map((item) => (
                  <NewsCard key={item.id} item={item} />
                ))}
                {items.length === 0 && (
                  <p className="py-6 text-center text-2xs text-ink-muted">Sin items</p>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
