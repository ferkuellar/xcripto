NEWS_STATUSES = {
    "detected",
    "registered",
    "classified",
    "validating",
    "verified",
    "partially_verified",
    "rumor",
    "monitoring",
    "rejected",
    "prioritized",
    "drafting",
    "reviewing",
    "approved",
    "scheduled",
    "published",
    "distributed",
    "measured",
    "archived",
    "corrected",
    "retracted",
    "escalated",
}

AGENT_EXECUTION_STATUSES = {
    "queued",
    "running",
    "waiting_context",
    "waiting_tool",
    "waiting_approval",
    "completed",
    "completed_with_warnings",
    "failed",
    "blocked_by_policy",
    "rejected",
    "cancelled",
    "retrying",
    "escalated",
}

SOURCE_STATUSES = {
    "proposed",
    "active",
    "trusted",
    "watchlist",
    "restricted",
    "blocked",
    "archived",
}

TRUST_LEVELS = {"T0", "T1", "T2", "T3"}

AUDIT_STATUSES = {"pass", "fail", "warning", "pending"}
AUDIT_SEVERITIES = {"low", "medium", "high", "critical"}
NEWS_PRIORITIES = {"P0", "P1", "P2", "P3", "P4"}

