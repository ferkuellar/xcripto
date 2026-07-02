import { SectionHeader } from '@/components/ui/section-header'
import { KnowledgeGraphPreview } from '@/components/newsroom/KnowledgeGraphPreview'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { graphEdges } from '@/data/mock-operations'

export default function KnowledgeGraphPage() {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Knowledge Graph"
        subtitle="Modelo conceptual de entidades y relaciones del newsroom (visualización de demostración)"
      />

      <KnowledgeGraphPreview height={520} />

      <Card>
        <CardHeader>
          <CardTitle>Relaciones del modelo</CardTitle>
          <CardDescription>Definidas en ORION-012-Grafo-de-Conocimiento</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-4">
            {graphEdges.map((edge) => (
              <div
                key={`${edge.from}-${edge.to}-${edge.relation}`}
                className="rounded-lg border border-line bg-surface-elevated/60 px-3 py-2 text-2xs"
              >
                <p className="font-mono font-medium text-accent-cyan">{edge.relation}</p>
                <p className="mt-0.5 text-ink-muted">
                  {edge.from} → {edge.to}
                </p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
