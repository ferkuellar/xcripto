import {
  AlertTriangle,
  CheckCircle2,
  CircleDashed,
  Eye,
  HelpCircle,
  Loader2,
  Lock,
  MessageCircleQuestion,
  ShieldAlert,
  XCircle,
} from 'lucide-react'
import { Badge, type BadgeProps } from '@/components/ui/badge'
import type { AgentStatus, Priority, RiskLevel, VerificationStatus } from '@/data/types'

type BadgeVariant = NonNullable<BadgeProps['variant']>

const priorityMap: Record<Priority, { variant: BadgeVariant; label: string }> = {
  P0: { variant: 'red', label: 'P0 · Crítico' },
  P1: { variant: 'orange', label: 'P1 · Principal' },
  P2: { variant: 'yellow', label: 'P2 · Relevante' },
  P3: { variant: 'blue', label: 'P3 · Seguimiento' },
  P4: { variant: 'neutral', label: 'P4 · Baja' },
}

export function PriorityBadge({ priority, compact = false }: { priority: Priority; compact?: boolean }) {
  const { variant, label } = priorityMap[priority]
  return <Badge variant={variant}>{compact ? priority : label}</Badge>
}

const riskMap: Record<RiskLevel, { variant: BadgeVariant; label: string; icon: typeof ShieldAlert }> = {
  critical: { variant: 'red', label: 'critical', icon: ShieldAlert },
  high: { variant: 'orange', label: 'high', icon: AlertTriangle },
  medium: { variant: 'yellow', label: 'medium', icon: AlertTriangle },
  low: { variant: 'green', label: 'low', icon: CheckCircle2 },
  unknown: { variant: 'neutral', label: 'unknown', icon: HelpCircle },
}

export function RiskBadge({ risk }: { risk: RiskLevel }) {
  const { variant, label, icon: Icon } = riskMap[risk]
  return (
    <Badge variant={variant}>
      <Icon className="h-3 w-3" />
      {label}
    </Badge>
  )
}

const verificationMap: Record<
  VerificationStatus,
  { variant: BadgeVariant; label: string; icon: typeof CheckCircle2 }
> = {
  verified: { variant: 'green', label: 'verified', icon: CheckCircle2 },
  partially_verified: { variant: 'yellow', label: 'partially verified', icon: CheckCircle2 },
  rumor: { variant: 'orange', label: 'rumor', icon: MessageCircleQuestion },
  monitoring: { variant: 'blue', label: 'monitoring', icon: Eye },
  unverified: { variant: 'neutral', label: 'unverified', icon: CircleDashed },
  rejected: { variant: 'red', label: 'rejected', icon: XCircle },
}

export function VerificationBadge({ status }: { status: VerificationStatus }) {
  const { variant, label, icon: Icon } = verificationMap[status]
  return (
    <Badge variant={variant}>
      <Icon className="h-3 w-3" />
      {label}
    </Badge>
  )
}

const agentStatusMap: Record<
  AgentStatus,
  { variant: BadgeVariant; label: string; icon: typeof Loader2; spin?: boolean }
> = {
  running: { variant: 'cyan', label: 'running', icon: Loader2, spin: true },
  waiting_review: { variant: 'yellow', label: 'waiting review', icon: Eye },
  blocked: { variant: 'red', label: 'blocked', icon: Lock },
  completed: { variant: 'green', label: 'completed', icon: CheckCircle2 },
  idle: { variant: 'neutral', label: 'idle', icon: CircleDashed },
}

export function StatusBadge({ status }: { status: AgentStatus }) {
  const { variant, label, icon: Icon, spin } = agentStatusMap[status]
  return (
    <Badge variant={variant}>
      <Icon className={spin ? 'h-3 w-3 animate-spin' : 'h-3 w-3'} />
      {label}
    </Badge>
  )
}
