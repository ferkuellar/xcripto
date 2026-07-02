import { Clapperboard, FileText, Link2, ScrollText, Send } from 'lucide-react'
import { SectionHeader } from '@/components/ui/section-header'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { VerificationBadge, RiskBadge } from '@/components/ui/status-badges'
import { EditorialProduction } from '@/components/newsroom/EditorialProduction'

export default function EditorialDesk() {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Editorial Desk"
        subtitle="Producción editorial con trazabilidad de fuentes y restricciones"
      />

      <div className="grid gap-4 xl:grid-cols-5">
        {/* Editor preview */}
        <Card className="xl:col-span-3">
          <CardHeader>
            <div className="flex flex-wrap items-center gap-2">
              <FileText className="h-4 w-4 text-accent-cyan" />
              <CardTitle>Qué dice (y qué no dice) la actualización de la SEC</CardTitle>
            </div>
            <CardDescription>
              CNT-702 · Article · Blog / Web · owner: Fernando Cuellar · estado: in_review
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex flex-wrap gap-1.5">
              <VerificationBadge status="verified" />
              <RiskBadge risk="medium" />
              <Badge variant="yellow">revisión editorial pendiente</Badge>
            </div>

            <div className="rounded-lg border border-line bg-surface-elevated/60 p-4 text-sm leading-relaxed text-ink-secondary">
              <p className="font-medium text-ink">Borrador (v3) — vista previa</p>
              <p className="mt-2">
                La SEC publicó una actualización procedimental relacionada con las solicitudes de
                ETF de Ethereum. El documento, disponible en el registro público, establece nuevos
                plazos de revisión y solicita comentarios adicionales…
              </p>
              <p className="mt-2 text-ink-muted">
                [El borrador continúa — 620 palabras, 3 fuentes citadas, disclaimers incluidos]
              </p>
            </div>

            <div className="flex flex-wrap gap-2 border-t border-line pt-3">
              <Button size="sm">
                <ScrollText className="h-3.5 w-3.5" />
                Send to ScriptAgent
              </Button>
              <Button size="sm" variant="secondary">
                <Clapperboard className="h-3.5 w-3.5" />
                Send to SocialClipAgent
              </Button>
              <Button size="sm" variant="outline">
                <Send className="h-3.5 w-3.5" />
                Enviar a revisión final
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Brief estructurado */}
        <div className="space-y-4 xl:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Brief estructurado</CardTitle>
              <CardDescription>Generado por EditorialAgent desde NWS-1041</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3 text-xs">
              <div>
                <p className="text-2xs font-semibold uppercase tracking-wider text-ink-muted">Ángulo</p>
                <p className="mt-0.5 text-ink-secondary">
                  Explicar el alcance real del documento sin especular sobre aprobación.
                </p>
              </div>
              <div>
                <p className="text-2xs font-semibold uppercase tracking-wider text-ink-muted">
                  Hechos confirmados
                </p>
                <ul className="mt-0.5 space-y-0.5 text-ink-secondary">
                  <li>· Existe actualización procedimental publicada</li>
                  <li>· Se establecen nuevos plazos de revisión</li>
                  <li>· Se abre periodo de comentarios</li>
                </ul>
              </div>
              <div>
                <p className="text-2xs font-semibold uppercase tracking-wider text-ink-muted">
                  Fuentes
                </p>
                <ul className="mt-0.5 space-y-1">
                  {['SEC.gov — documento oficial (T5)', 'Filing público asociado (T5)', 'Análisis interno XCripto (T4)'].map(
                    (s) => (
                      <li key={s} className="flex items-center gap-1.5 text-ink-secondary">
                        <Link2 className="h-3 w-3 text-accent-cyan" />
                        {s}
                      </li>
                    ),
                  )}
                </ul>
              </div>
              <div>
                <p className="text-2xs font-semibold uppercase tracking-wider text-ink-muted">
                  Restricciones
                </p>
                <ul className="mt-0.5 space-y-0.5 text-accent-yellow">
                  <li>· No afirmar aprobación ni rechazo del ETF</li>
                  <li>· No incluir proyecciones de precio</li>
                  <li>· Incluir disclaimer de análisis editorial</li>
                </ul>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      <EditorialProduction />
    </div>
  )
}
