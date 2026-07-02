import { AlertOctagon, Lock, UserCheck } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { RiskBadge, VerificationBadge } from '@/components/ui/status-badges'
import { pipelineAlerts, riskQueue, verificationQueue } from '@/data/mock-news'
import { cn } from '@/lib/utils'

const alertTone: Record<string, string> = {
  critical: 'border-accent-red/30 bg-accent-red/5 text-accent-red',
  high: 'border-accent-orange/30 bg-accent-orange/5 text-accent-orange',
  medium: 'border-accent-yellow/30 bg-accent-yellow/5 text-accent-yellow',
}

export function RiskQueuePanel() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Risk Queue</CardTitle>
        <CardDescription>Items pendientes de decisión de riesgo</CardDescription>
      </CardHeader>
      <CardContent className="space-y-2">
        {riskQueue.map((item) => (
          <div key={item.id} className="rounded-lg border border-line bg-surface-elevated/60 p-3">
            <div className="flex items-start justify-between gap-2">
              <p className="text-xs font-medium leading-snug text-ink">{item.title}</p>
              <RiskBadge risk={item.level} />
            </div>
            <p className="mt-1.5 text-2xs text-ink-secondary">{item.recommendation}</p>
            <div className="mt-2 flex flex-wrap items-center gap-1.5">
              <Badge variant="neutral">{item.severity}</Badge>
              {item.blocked && (
                <Badge variant="red">
                  <Lock className="h-3 w-3" />
                  publicación bloqueada
                </Badge>
              )}
              {item.humanReview && (
                <Badge variant="yellow">
                  <UserCheck className="h-3 w-3" />
                  revisión humana
                </Badge>
              )}
              <span className="ml-auto text-2xs text-ink-muted">{item.relatedNewsId}</span>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}

export function VerificationQueuePanel() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Verification Queue</CardTitle>
        <CardDescription>Estado de verificación por historia</CardDescription>
      </CardHeader>
      <CardContent className="space-y-2">
        {verificationQueue.map((item) => (
          <div
            key={item.id}
            className="flex items-center justify-between gap-3 rounded-lg border border-line bg-surface-elevated/60 px-3 py-2"
          >
            <div className="min-w-0">
              <p className="truncate text-xs font-medium text-ink">{item.title}</p>
              <p className="text-2xs text-ink-muted">
                {item.sources} fuentes · {item.confidence} · {item.agent} · {item.updatedAt}
              </p>
            </div>
            <VerificationBadge status={item.status} />
          </div>
        ))}
      </CardContent>
    </Card>
  )
}

export function PipelineAlerts() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <AlertOctagon className="h-4 w-4 text-accent-red" />
          Alertas de integridad
        </CardTitle>
        <CardDescription>Requisitos faltantes detectados por AuditAgent</CardDescription>
      </CardHeader>
      <CardContent className="space-y-2">
        {pipelineAlerts.map((alert) => (
          <div
            key={alert.id}
            className={cn('rounded-lg border px-3 py-2 text-2xs', alertTone[alert.severity])}
          >
            <p className="font-medium">{alert.message}</p>
            <p className="mt-0.5 opacity-70">
              {alert.type} · {alert.itemRef}
            </p>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}
