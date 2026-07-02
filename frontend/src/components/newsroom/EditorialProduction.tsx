import { Eye } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge, type BadgeProps } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { contentPieces } from '@/data/mock-news'
import type { ContentPiece } from '@/data/types'

type BadgeVariant = NonNullable<BadgeProps['variant']>

const statusMap: Record<ContentPiece['status'], { variant: BadgeVariant; label: string }> = {
  draft: { variant: 'neutral', label: 'draft' },
  in_review: { variant: 'yellow', label: 'in review' },
  approved: { variant: 'green', label: 'approved' },
  blocked: { variant: 'red', label: 'blocked' },
  scheduled: { variant: 'cyan', label: 'scheduled' },
}

export function EditorialProduction({ pieces = contentPieces }: { pieces?: ContentPiece[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Editorial Production</CardTitle>
        <CardDescription>Contenido en producción por tipo y canal</CardDescription>
      </CardHeader>
      <CardContent className="space-y-2">
        {pieces.map((piece) => {
          const status = statusMap[piece.status]
          return (
            <div key={piece.id} className="rounded-lg border border-line bg-surface-elevated/60 p-3">
              <div className="flex items-start justify-between gap-2">
                <div className="min-w-0">
                  <div className="flex items-center gap-1.5">
                    <Badge variant="purple">{piece.type}</Badge>
                    <Badge variant={status.variant}>{status.label}</Badge>
                    {piece.reviewPending && (
                      <Badge variant="yellow">
                        <Eye className="h-3 w-3" />
                        revisión pendiente
                      </Badge>
                    )}
                  </div>
                  <p className="mt-1.5 truncate text-xs font-medium text-ink">{piece.title}</p>
                  <p className="mt-0.5 text-2xs text-ink-muted">
                    {piece.owner} → {piece.channel}
                  </p>
                </div>
                <span className="shrink-0 text-2xs tabular-nums text-ink-secondary">
                  {piece.progress}%
                </span>
              </div>
              <Progress
                value={piece.progress}
                className="mt-2"
                barClassName={piece.status === 'blocked' ? 'bg-accent-red/60' : undefined}
              />
            </div>
          )
        })}
      </CardContent>
    </Card>
  )
}
