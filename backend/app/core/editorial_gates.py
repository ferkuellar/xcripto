from app.models import AuditCheck

PROTECTED_NEWS_STATUSES = {"approved", "scheduled", "published"}
PASSING_AUDIT_ENTITY_TYPES = {"news_item", "NewsItem"}
PASSING_AUDIT_STATUSES = {"passed", "passed_with_warnings"}
PASSING_DECISION_RECOMMENDATIONS = {"allow_to_continue", "allow_with_warnings"}


def requires_passing_audit_check(status: str) -> bool:
    return status in PROTECTED_NEWS_STATUSES


def requires_source_quality_gate(status: str) -> bool:
    """Los estados protegidos también exigen calidad de fuente suficiente.

    Ver ``app.core.source_quality`` y ``docs/SOURCE_QUALITY_POLICY.md``.
    """
    return status in PROTECTED_NEWS_STATUSES


def is_passing_audit_check(check: AuditCheck | None) -> bool:
    if check is None:
        return False

    return (
        check.entity_type in PASSING_AUDIT_ENTITY_TYPES
        and check.ready_to_advance is True
        and check.publication_block_recommended is False
        and check.audit_status in PASSING_AUDIT_STATUSES
        and check.decision_recommendation in PASSING_DECISION_RECOMMENDATIONS
    )
