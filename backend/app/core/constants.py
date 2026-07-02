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

AUDIT_STATUSES = {"pass", "fail", "warning", "pending", "passed", "passed_with_warnings", "failed"}
AUDIT_SEVERITIES = {"low", "medium", "high", "critical"}
NEWS_PRIORITIES = {"P0", "P1", "P2", "P3", "P4"}

VERIFICATION_STATUSES = {
    "unverified",
    "validating",
    "verified",
    "partially_verified",
    "rumor",
    "contradicted",
    "rejected",
    "escalated",
    "monitoring",
    "outdated",
}
EVIDENCE_LEVELS = {"E0", "E1", "E2", "E3", "E4", "E5", "unknown"}
CONFIDENCE_LEVELS = {"C0", "C1", "C2", "C3", "C4", "C5", "unknown"}

RISK_LEVELS = {"low", "medium", "high", "critical", "unknown"}
RISK_SEVERITIES = {"R-SEV-0", "R-SEV-1", "R-SEV-2", "R-SEV-3", "R-SEV-4"}
RISK_DECISION_RECOMMENDATIONS = {
    "allow",
    "allow_with_minor_edits",
    "revise_before_publication",
    "require_human_review",
    "escalate",
    "block_publication",
    "hold_for_verification",
    "reject",
    "monitor_only",
}

CONTENT_TYPES = {
    "editorial_brief",
    "news_article",
    "analysis",
    "explainer",
    "newsletter_item",
    "linkedin_post",
    "blog_article",
    "script_base",
    "internal_note",
}
CONTENT_STATUSES = {"drafting", "reviewing", "approved", "rejected", "blocked", "archived"}

DISTRIBUTION_CHANNELS = {
    "YouTube",
    "YouTube Shorts",
    "TikTok",
    "Instagram Reels",
    "X / Twitter",
    "LinkedIn",
    "Newsletter",
    "Blog / Web",
    "Telegram",
    "Discord",
    "internal",
}
DISTRIBUTION_TYPES = {
    "primary_publication",
    "secondary_distribution",
    "clip_distribution",
    "thread_distribution",
    "newsletter_distribution",
    "community_distribution",
    "blog_distribution",
    "video_distribution",
    "alert_distribution",
    "scheduled_distribution",
    "follow_up_distribution",
    "internal_monitoring",
}
DISTRIBUTION_STATUSES = {
    "proposed",
    "ready_for_review",
    "needs_approval",
    "needs_source",
    "needs_verification",
    "needs_risk_review",
    "needs_channel_variant",
    "needs_schedule",
    "blocked",
    "rejected",
    "scheduled",
    "distributed",
    "archived",
}

PUBLICATION_STATUSES = {
    "scheduled",
    "published",
    "failed",
    "cancelled",
    "corrected",
    "retracted",
    "archived",
}
