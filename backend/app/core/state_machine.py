from app.core.constants import NEWS_STATUSES

FINAL_NEWS_STATUSES = {"rejected", "archived", "corrected", "retracted", "escalated"}

NEWS_STATUS_TRANSITIONS: dict[str, set[str]] = {
    "detected": {"registered"},
    "registered": {"classified"},
    "classified": {"validating"},
    "validating": {"verified", "partially_verified", "rumor", "rejected"},
    "verified": {"prioritized"},
    "partially_verified": {"prioritized"},
    "rumor": {"monitoring"},
    "monitoring": {"validating"},
    "prioritized": {"drafting"},
    "drafting": {"reviewing"},
    "reviewing": {"approved", "rejected"},
    "approved": {"scheduled"},
    "scheduled": {"published"},
    "published": {"distributed", "corrected", "retracted"},
    "distributed": {"measured"},
    "measured": {"archived"},
}


def get_allowed_news_status_transitions(current_status: str) -> set[str]:
    if current_status not in NEWS_STATUSES:
        return set()

    allowed = set(NEWS_STATUS_TRANSITIONS.get(current_status, set()))
    if current_status not in FINAL_NEWS_STATUSES:
        allowed.add("escalated")
    return allowed


def is_valid_news_status_transition(current_status: str, next_status: str) -> bool:
    if next_status not in NEWS_STATUSES:
        return False
    if current_status == next_status:
        return True
    return next_status in get_allowed_news_status_transitions(current_status)
