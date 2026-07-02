import { Link } from 'react-router-dom'
import { ArrowUpRight } from 'lucide-react'
import { agents } from '@/data/mock-agents'
import { AgentCard } from './AgentCard'
import { SectionHeader } from '@/components/ui/section-header'
import { buttonVariants } from '@/components/ui/button'
import { cn } from '@/lib/utils'

export function AgentActivity() {
  const featured = agents.slice(0, 6)

  return (
    <section>
      <SectionHeader
        title="Agent Activity"
        subtitle="Centro de control de agentes editoriales"
        actions={
          <Link to="/agents" className={cn(buttonVariants({ variant: 'outline', size: 'sm' }))}>
            Ver todos
            <ArrowUpRight className="h-3 w-3" />
          </Link>
        }
      />
      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
        {featured.map((agent) => (
          <AgentCard key={agent.id} agent={agent} />
        ))}
      </div>
    </section>
  )
}
