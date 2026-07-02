import { Brain, TrendingUp } from 'lucide-react'
import { SectionHeader } from '@/components/ui/section-header'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { CalendarTimeline } from '@/components/newsroom/CalendarTimeline'
import { EditorialProduction } from '@/components/newsroom/EditorialProduction'
import { EngagementChart, PublicationsByChannelChart } from '@/components/metrics/MetricsCharts'
import { PriorityBadge } from '@/components/ui/status-badges'
import { contentPieces, newsItems, scheduledPublications } from '@/data/mock-news'
import { memoryItems } from '@/data/mock-agents'

// ── Market Impact ────────────────────────────────────────────────────────────

const impactScores = [
  { newsId: 'NWS-1041', score: 92, audience: 'Institucional + retail', window: '24–48 h' },
  { newsId: 'NWS-1042', score: 87, audience: 'Usuarios del exchange', window: 'Inmediata' },
  { newsId: 'NWS-1043', score: 81, audience: 'Usuarios DeFi', window: 'Inmediata' },
  { newsId: 'NWS-1047', score: 64, audience: 'Institucional', window: '1 semana' },
  { newsId: 'NWS-1045', score: 55, audience: 'Desarrolladores', window: '72 h' },
]

export function MarketImpactPage() {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Market Impact"
        subtitle="Relevancia editorial estimada por MarketImpactAgent — no es análisis de precio"
      />
      <div className="space-y-2">
        {impactScores.map((impact) => {
          const news = newsItems.find((n) => n.id === impact.newsId)
          if (!news) return null
          return (
            <div key={impact.newsId} className="card-surface flex flex-wrap items-center gap-4 p-4">
              <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-accent-purple/10 ring-1 ring-accent-purple/25">
                <TrendingUp className="h-4 w-4 text-accent-purple" />
              </div>
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium text-ink">{news.title}</p>
                <p className="text-2xs text-ink-muted">
                  {impact.newsId} · audiencia: {impact.audience} · ventana editorial: {impact.window}
                </p>
              </div>
              <PriorityBadge priority={news.priority} compact />
              <div className="w-40">
                <div className="flex items-center justify-between text-2xs text-ink-secondary">
                  <span>Impacto editorial</span>
                  <span className="font-semibold tabular-nums text-ink">{impact.score}</span>
                </div>
                <div className="mt-1 h-1.5 overflow-hidden rounded-full bg-white/5">
                  <div
                    className="h-full rounded-full bg-accent-purple/70"
                    style={{ width: `${impact.score}%` }}
                  />
                </div>
              </div>
            </div>
          )
        })}
      </div>
      <p className="text-2xs text-ink-muted">
        El impacto mide relevancia editorial y de audiencia. XMIP no genera señales de trading ni
        predicciones de precio.
      </p>
    </div>
  )
}

// ── Scripts ──────────────────────────────────────────────────────────────────

export function ScriptsPage() {
  const scripts = contentPieces.filter((p) => p.type === 'Video Script' || p.type === 'Brief')
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Scripts"
        subtitle="Guiones de video generados por ScriptAgent desde briefs aprobados"
      />
      <EditorialProduction pieces={scripts} />
    </div>
  )
}

// ── Social Clips ─────────────────────────────────────────────────────────────

export function SocialClipsPage() {
  const clips = contentPieces.filter((p) => ['Short', 'Thread'].includes(p.type))
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Social Clips"
        subtitle="Shorts, hilos y clips producidos por SocialClipAgent"
      />
      <EditorialProduction pieces={clips} />
    </div>
  )
}

// ── Distribution ─────────────────────────────────────────────────────────────

const channels = [
  'YouTube',
  'YouTube Shorts',
  'TikTok',
  'Instagram Reels',
  'X / Twitter',
  'LinkedIn',
  'Newsletter',
  'Blog / Web',
  'Telegram',
  'Discord',
]

export function DistributionPage() {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Distribution"
        subtitle="Distribución multicanal gestionada por DistributionAgent"
      />
      <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-5">
        {channels.map((channel) => {
          const scheduled = scheduledPublications.filter((p) => p.channel === channel).length
          return (
            <div key={channel} className="card-surface px-3 py-2.5">
              <p className="text-xs font-medium text-ink">{channel}</p>
              <p className="mt-0.5 text-2xs text-ink-muted">
                {scheduled > 0 ? `${scheduled} programadas` : 'sin publicaciones próximas'}
              </p>
            </div>
          )
        })}
      </div>
      <div className="grid gap-4 xl:grid-cols-2">
        <CalendarTimeline />
        <div className="space-y-4">
          <PublicationsByChannelChart />
          <EngagementChart />
        </div>
      </div>
    </div>
  )
}

// ── Calendar ─────────────────────────────────────────────────────────────────

export function CalendarPage() {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Calendar"
        subtitle="Calendario editorial con dependencias y estado por publicación"
      />
      <CalendarTimeline />
    </div>
  )
}

// ── Memory ───────────────────────────────────────────────────────────────────

const memoryTypeLabel: Record<string, string> = {
  editorial_rule: 'Regla editorial',
  source_pattern: 'Patrón de fuente',
  incident_lesson: 'Lección de incidente',
  style_preference: 'Preferencia de estilo',
}

export function MemoryPage() {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Memory"
        subtitle="Memoria institucional consolidada por MemoryAgent"
      />
      <div className="grid gap-3 md:grid-cols-2">
        {memoryItems.map((item) => (
          <div key={item.id} className="card-surface p-4">
            <div className="flex items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <Brain className="h-4 w-4 text-accent-purple" />
                <Badge variant="purple">{memoryTypeLabel[item.type]}</Badge>
              </div>
              <span className="text-2xs text-ink-muted">{item.id}</span>
            </div>
            <p className="mt-2.5 text-sm leading-relaxed text-ink">{item.content}</p>
            <p className="mt-2 text-2xs text-ink-muted">
              creado por {item.createdBy} · {item.createdAt} · reforzado {item.reinforcedCount} veces
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}

// ── Settings ─────────────────────────────────────────────────────────────────

export function SettingsPage() {
  const settings = [
    { label: 'Modo operativo por defecto', value: 'A2 — con revisión humana', section: 'Agentes' },
    { label: 'Umbral de bloqueo por riesgo', value: 'high o superior', section: 'Riesgo' },
    { label: 'Fuentes mínimas para "verified"', value: '2 fuentes T4+', section: 'Verificación' },
    { label: 'Idioma editorial', value: 'Español (MX)', section: 'Editorial' },
    { label: 'Zona horaria operativa', value: 'America/Mexico_City', section: 'Newsroom' },
    { label: 'Retención de logs de agentes', value: '90 días', section: 'Auditoría' },
  ]

  return (
    <div className="space-y-6">
      <SectionHeader
        title="Settings"
        subtitle="Configuración del newsroom (solo lectura en esta versión)"
      />
      <Card>
        <CardHeader>
          <CardTitle>Parámetros operativos</CardTitle>
          <CardDescription>Gobernados por los documentos ORION del proyecto</CardDescription>
        </CardHeader>
        <CardContent className="divide-y divide-line">
          {settings.map((s) => (
            <div key={s.label} className="flex items-center justify-between gap-4 py-2.5">
              <div>
                <p className="text-xs font-medium text-ink">{s.label}</p>
                <p className="text-2xs text-ink-muted">{s.section}</p>
              </div>
              <span className="text-xs text-ink-secondary">{s.value}</span>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}
