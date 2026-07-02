import { useState } from 'react'
import { graphEdges, graphNodes } from '@/data/mock-operations'
import { cn } from '@/lib/utils'

const typeColor: Record<string, string> = {
  core: 'bg-accent-cyan',
  input: 'bg-accent-blue',
  control: 'bg-accent-yellow',
  output: 'bg-accent-green',
  feedback: 'bg-accent-purple',
  system: 'bg-ink-secondary',
  governance: 'bg-accent-orange',
}

export function KnowledgeGraphPreview({ height = 420 }: { height?: number }) {
  const [hovered, setHovered] = useState<string | null>(null)

  const related = (nodeId: string) =>
    graphEdges.some(
      (e) => (e.from === hovered && e.to === nodeId) || (e.to === hovered && e.from === nodeId),
    )

  const hoveredEdges = graphEdges.filter((e) => e.from === hovered || e.to === hovered)
  const hoveredNode = graphNodes.find((n) => n.id === hovered)

  return (
    <div
      className="relative w-full overflow-hidden rounded-xl border border-line bg-surface"
      style={{ height }}
    >
      {/* Aristas */}
      <svg viewBox="0 0 100 100" preserveAspectRatio="none" className="absolute inset-0 h-full w-full">
        {graphEdges.map((edge) => {
          const from = graphNodes.find((n) => n.id === edge.from)!
          const to = graphNodes.find((n) => n.id === edge.to)!
          const active = hovered === edge.from || hovered === edge.to
          return (
            <line
              key={`${edge.from}-${edge.to}-${edge.relation}`}
              x1={from.x}
              y1={from.y}
              x2={to.x}
              y2={to.y}
              stroke={active ? 'rgba(0,229,255,0.55)' : 'rgba(255,255,255,0.12)'}
              strokeWidth={active ? 1.5 : 1}
              vectorEffect="non-scaling-stroke"
            />
          )
        })}
      </svg>

      {/* Nodos */}
      {graphNodes.map((node) => {
        const dimmed = hovered !== null && hovered !== node.id && !related(node.id)
        return (
          <div
            key={node.id}
            className={cn(
              'absolute flex -translate-x-1/2 -translate-y-1/2 cursor-pointer flex-col items-center gap-1 transition-opacity',
              dimmed && 'opacity-25',
            )}
            style={{ left: `${node.x}%`, top: `${node.y}%` }}
            onMouseEnter={() => setHovered(node.id)}
            onMouseLeave={() => setHovered(null)}
          >
            <span
              className={cn(
                'h-3 w-3 rounded-full ring-2 ring-background transition-transform',
                typeColor[node.type] ?? 'bg-ink-muted',
                hovered === node.id && 'scale-125 shadow-glow',
              )}
            />
            <span className="whitespace-nowrap rounded-md border border-line bg-surface-elevated/90 px-1.5 py-0.5 text-2xs font-medium text-ink-secondary">
              {node.label}
            </span>
          </div>
        )
      })}

      {/* Relaciones del nodo activo */}
      {hoveredNode && hoveredEdges.length > 0 && (
        <div className="absolute right-3 top-3 w-52 rounded-lg border border-line bg-surface-elevated/90 p-2.5">
          <p className="text-2xs font-semibold text-ink">{hoveredNode.label}</p>
          <ul className="mt-1 space-y-0.5">
            {hoveredEdges.map((e) => (
              <li key={`${e.from}-${e.to}-${e.relation}`} className="text-2xs text-accent-cyan">
                {e.relation}
                <span className="text-ink-muted">
                  {' '}
                  → {graphNodes.find((n) => n.id === (e.from === hovered ? e.to : e.from))?.label}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Leyenda */}
      <div className="absolute bottom-3 left-3 flex flex-wrap gap-x-3 gap-y-1 rounded-lg border border-line bg-surface-elevated/80 px-2.5 py-1.5">
        {Object.entries({
          core: 'Núcleo',
          input: 'Entrada',
          control: 'Control',
          output: 'Salida',
          feedback: 'Feedback',
          governance: 'Gobernanza',
        }).map(([type, label]) => (
          <span key={type} className="flex items-center gap-1 text-2xs text-ink-secondary">
            <span className={cn('h-2 w-2 rounded-full', typeColor[type])} />
            {label}
          </span>
        ))}
      </div>
    </div>
  )
}
