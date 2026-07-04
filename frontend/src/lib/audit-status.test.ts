import { describe, expect, it } from 'vitest'
import {
  auditStatusToVariant,
  auditStatusVariant,
  countBlockingAudits,
  decisionRecommendationVariant,
  isBlockingAudit,
} from '@/lib/audit-status'

describe('auditStatusVariant (canonical AUDIT_STATUSES)', () => {
  it('maps every canonical status to its badge variant', () => {
    expect(auditStatusVariant).toEqual({
      passed: 'green',
      passed_with_warnings: 'yellow',
      warning: 'yellow',
      pending: 'blue',
      failed: 'red',
      blocked: 'red',
    })
  })

  it('falls back to neutral for legacy/unknown values', () => {
    expect(auditStatusToVariant('pass')).toBe('neutral')
    expect(auditStatusToVariant('fail')).toBe('neutral')
    expect(auditStatusToVariant('totally-unknown')).toBe('neutral')
  })

  it('resolves canonical values through the helper', () => {
    expect(auditStatusToVariant('passed')).toBe('green')
    expect(auditStatusToVariant('failed')).toBe('red')
    expect(auditStatusToVariant('blocked')).toBe('red')
  })
})

describe('decisionRecommendationVariant (canonical AUDIT_DECISION_RECOMMENDATIONS)', () => {
  it('maps every canonical recommendation to its badge variant', () => {
    expect(decisionRecommendationVariant).toEqual({
      allow_to_continue: 'green',
      allow_with_warnings: 'yellow',
      needs_revision: 'yellow',
      block_publication: 'red',
    })
  })
})

describe('isBlockingAudit / countBlockingAudits (P2 regression guard)', () => {
  it('counts failed and blocked as active publication blockers', () => {
    expect(isBlockingAudit({ audit_status: 'failed', publication_block_recommended: false })).toBe(
      true,
    )
    expect(isBlockingAudit({ audit_status: 'blocked', publication_block_recommended: false })).toBe(
      true,
    )
  })

  it('counts an explicit publication_block_recommended regardless of status', () => {
    expect(isBlockingAudit({ audit_status: 'passed', publication_block_recommended: true })).toBe(
      true,
    )
  })

  it('does not treat legacy pass/fail as blockers', () => {
    // El bug P2: contar 'fail' que nunca coincidía con 'failed'. Los valores
    // legacy no deben ser la base del conteo.
    expect(
      isBlockingAudit({
        audit_status: 'fail' as never,
        publication_block_recommended: false,
      }),
    ).toBe(false)
    expect(
      isBlockingAudit({
        audit_status: 'pass' as never,
        publication_block_recommended: false,
      }),
    ).toBe(false)
  })

  it('does not treat unknown statuses as blockers nor as success', () => {
    expect(
      isBlockingAudit({ audit_status: 'weird' as never, publication_block_recommended: false }),
    ).toBe(false)
  })

  it('does not count healthy statuses as blockers', () => {
    for (const status of ['passed', 'passed_with_warnings', 'warning', 'pending'] as const) {
      expect(isBlockingAudit({ audit_status: status, publication_block_recommended: false })).toBe(
        false,
      )
    }
  })

  it('counts blockers across a mixed list', () => {
    const checks = [
      { audit_status: 'passed' as const, publication_block_recommended: false },
      { audit_status: 'failed' as const, publication_block_recommended: false },
      { audit_status: 'blocked' as const, publication_block_recommended: false },
      { audit_status: 'passed' as const, publication_block_recommended: true },
      { audit_status: 'pending' as const, publication_block_recommended: false },
    ]
    expect(countBlockingAudits(checks)).toBe(3)
  })

  it('returns zero for an empty list', () => {
    expect(countBlockingAudits([])).toBe(0)
  })
})
