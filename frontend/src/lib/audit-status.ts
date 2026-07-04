import type { BadgeProps } from '@/components/ui/badge'
import type { AuditCheckRead } from '@/lib/api-types'

export type BadgeVariant = NonNullable<BadgeProps['variant']>

/**
 * Catálogo canónico AUDIT_STATUSES del backend → variante de badge.
 * Fuente única de verdad para AuditPage, NewsDetailPage y cualquier consumidor.
 * Los valores legacy 'pass'/'fail' fueron retirados (el backend los rechaza).
 */
export const auditStatusVariant: Record<AuditCheckRead['audit_status'], BadgeVariant> = {
  passed: 'green',
  passed_with_warnings: 'yellow',
  warning: 'yellow',
  pending: 'blue',
  failed: 'red',
  blocked: 'red',
}

/** Catálogo canónico AUDIT_DECISION_RECOMMENDATIONS del backend → variante de badge. */
export const decisionRecommendationVariant: Record<
  NonNullable<AuditCheckRead['decision_recommendation']>,
  BadgeVariant
> = {
  allow_to_continue: 'green',
  allow_with_warnings: 'yellow',
  needs_revision: 'yellow',
  block_publication: 'red',
}

/** Variante de badge para un audit_status, con fallback neutral defensivo. */
export function auditStatusToVariant(status: string): BadgeVariant {
  return auditStatusVariant[status as AuditCheckRead['audit_status']] ?? 'neutral'
}

type BlockingAuditInput = Pick<AuditCheckRead, 'audit_status' | 'publication_block_recommended'>

/**
 * Un audit check cuenta como bloqueo de publicación activo cuando recomienda
 * explícitamente bloquear o su estado canónico es `failed`/`blocked`.
 *
 * Guarda de regresión (bug P2): los valores legacy 'pass'/'fail' y cualquier
 * estado desconocido NO deben contarse como bloqueo — ni como éxito.
 */
export function isBlockingAudit(check: BlockingAuditInput): boolean {
  return (
    check.publication_block_recommended === true ||
    check.audit_status === 'failed' ||
    check.audit_status === 'blocked'
  )
}

/** Cuenta los audit checks que bloquean publicación en una lista. */
export function countBlockingAudits(checks: ReadonlyArray<BlockingAuditInput>): number {
  return checks.filter(isBlockingAudit).length
}
