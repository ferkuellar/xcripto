import { CheckCircle2, PlayCircle, TriangleAlert, XCircle } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { auditChecks } from '@/data/mock-operations'
import { cn } from '@/lib/utils'

const statusStyle = {
  pass: { icon: CheckCircle2, tone: 'text-accent-green', label: 'pass' },
  fail: { icon: XCircle, tone: 'text-accent-red', label: 'fail' },
  warning: { icon: TriangleAlert, tone: 'text-accent-yellow', label: 'warning' },
} as const

export function AuditPanel() {
  const failing = auditChecks.filter((c) => c.status === 'fail').length
  const warnings = auditChecks.filter((c) => c.status === 'warning').length

  return (
    <Card>
      <CardHeader className="flex-row items-start justify-between space-y-0">
        <div>
          <CardTitle>Audit Checks</CardTitle>
          <CardDescription>
            {failing} fallos · {warnings} advertencias · última corrida hace 45 min
          </CardDescription>
        </div>
        <Button size="sm">
          <PlayCircle className="h-3.5 w-3.5" />
          Run Audit
        </Button>
      </CardHeader>
      <CardContent className="space-y-2">
        {auditChecks.map((check) => {
          const { icon: Icon, tone, label } = statusStyle[check.status]
          return (
            <div
              key={check.id}
              className="flex items-start gap-3 rounded-lg border border-line bg-surface-elevated/60 p-3"
            >
              <Icon className={cn('mt-0.5 h-4 w-4 shrink-0', tone)} />
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-center gap-1.5">
                  <p className="text-xs font-medium text-ink">{check.name}</p>
                  <Badge
                    variant={
                      check.status === 'pass' ? 'green' : check.status === 'fail' ? 'red' : 'yellow'
                    }
                  >
                    {label}
                  </Badge>
                </div>
                <p className="mt-0.5 text-2xs text-ink-secondary">{check.detail}</p>
                <p className="mt-1 font-mono text-2xs text-ink-muted">
                  {check.correlationId} · ref: {check.itemRef}
                </p>
              </div>
            </div>
          )
        })}
      </CardContent>
    </Card>
  )
}
