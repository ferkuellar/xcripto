import { Flag, ShieldCheck } from 'lucide-react'
import { SectionHeader } from '@/components/ui/section-header'
import { Badge, type BadgeProps } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { sources } from '@/data/mock-operations'
import type { SourceRecord } from '@/data/types'

type BadgeVariant = NonNullable<BadgeProps['variant']>

const statusMap: Record<SourceRecord['status'], { variant: BadgeVariant; label: string }> = {
  active: { variant: 'green', label: 'active' },
  under_review: { variant: 'yellow', label: 'under review' },
  flagged: { variant: 'orange', label: 'flagged' },
  blocked: { variant: 'red', label: 'blocked' },
}

function levelTone(level: string) {
  const n = Number(level[1])
  if (n >= 4) return 'text-accent-green'
  if (n >= 2) return 'text-accent-yellow'
  return 'text-accent-red'
}

export default function SourceValidation() {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Source Validation"
        subtitle="Registro de fuentes con niveles de confianza, evidencia y confiabilidad"
      />

      <div className="card-surface overflow-x-auto">
        <table className="w-full min-w-[820px] text-left text-xs">
          <thead>
            <tr className="border-b border-line text-2xs uppercase tracking-wider text-ink-muted">
              <th className="px-4 py-3 font-medium">Fuente</th>
              <th className="px-3 py-3 font-medium">Tipo</th>
              <th className="px-3 py-3 text-center font-medium">Trust</th>
              <th className="px-3 py-3 text-center font-medium">Evidence</th>
              <th className="px-3 py-3 text-center font-medium">Confidence</th>
              <th className="px-3 py-3 font-medium">Estado</th>
              <th className="px-3 py-3 font-medium">Última revisión</th>
              <th className="px-3 py-3 text-right font-medium">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {sources.map((source) => {
              const status = statusMap[source.status]
              return (
                <tr
                  key={source.id}
                  className="border-b border-line/50 transition-colors last:border-0 hover:bg-white/[0.02]"
                >
                  <td className="px-4 py-3">
                    <p className="font-medium text-ink">{source.name}</p>
                    <p className="text-2xs text-ink-muted">
                      {source.id} · {source.linkedItems} items vinculados
                    </p>
                  </td>
                  <td className="px-3 py-3 text-ink-secondary">{source.type}</td>
                  <td className={`px-3 py-3 text-center font-semibold tabular-nums ${levelTone(source.trust)}`}>
                    {source.trust}
                  </td>
                  <td className={`px-3 py-3 text-center font-semibold tabular-nums ${levelTone(source.evidence)}`}>
                    {source.evidence}
                  </td>
                  <td className={`px-3 py-3 text-center font-semibold tabular-nums ${levelTone(source.confidence)}`}>
                    {source.confidence}
                  </td>
                  <td className="px-3 py-3">
                    <Badge variant={status.variant}>{status.label}</Badge>
                  </td>
                  <td className="px-3 py-3 text-ink-muted">{source.lastChecked}</td>
                  <td className="px-3 py-3">
                    <div className="flex justify-end gap-1.5">
                      <Button size="sm" variant="secondary">
                        <ShieldCheck className="h-3 w-3" />
                        Validate
                      </Button>
                      <Button size="sm" variant="danger">
                        <Flag className="h-3 w-3" />
                        Flag
                      </Button>
                    </div>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      <p className="text-2xs text-ink-muted">
        Escalas: Trust T0–T5 · Evidence E0–E5 · Confidence C0–C5. Definidas en
        ORION-021-Gestion-de-Fuentes.
      </p>
    </div>
  )
}
