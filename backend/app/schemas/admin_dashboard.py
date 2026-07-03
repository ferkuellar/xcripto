from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class DashboardOverview(BaseModel):
    total_news: int
    total_intake_signals: int
    pending_intake_signals: int
    duplicate_intake_signals: int
    promoted_intake_signals: int
    active_workflows: int
    blocked_workflows: int
    pending_tasks: int
    blocked_tasks: int
    completed_tasks: int
    latest_readiness_count: int
    ready_to_advance_count: int
    blocked_readiness_count: int
    published_records_count: int
    scheduled_publications_count: int
    pending_agent_reviews_count: int
    active_users_count: int
    unassigned_news_count: int
    unassigned_tasks_count: int


class NewsroomHealth(BaseModel):
    health_status: str
    health_score: int
    critical_blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    counts_by_news_status: dict[str, int] = Field(default_factory=dict)
    counts_by_workflow_status: dict[str, int] = Field(default_factory=dict)
    counts_by_task_status: dict[str, int] = Field(default_factory=dict)
    counts_by_readiness_status: dict[str, int] = Field(default_factory=dict)


class IntakeQueueItem(BaseModel):
    signal_id: str
    raw_title: str | None
    normalized_title: str | None
    source_name: str | None
    source_url: str | None
    signal_status: str
    dedupe_status: str
    priority: str
    confidence_level: str
    duplicate_of_signal_id: str | None
    promoted_news_item_id: str | None
    created_at: datetime


class EditorialWorkQueueItem(BaseModel):
    news_item_id: str
    title: str
    status: str
    priority: str
    workflow_run_id: str | None
    current_step: str | None
    readiness_status: str | None
    score: float | None
    missing_requirements: list[str] = Field(default_factory=list)
    blocking_reasons: list[str] = Field(default_factory=list)
    next_agent: str | None
    recommended_next_action: str | None
    pending_task_count: int
    blocking_task_count: int
    owner: str | None
    created_at: datetime
    updated_at: datetime


class BlockerItem(BaseModel):
    blocker_type: str
    entity_type: str
    entity_id: str
    news_item_id: str | None
    title_or_summary: str | None
    reason: str
    severity: str
    recommended_action: str
    created_at: datetime


class ReadinessBoardItem(BaseModel):
    news_item_id: str
    title: str | None
    score: float
    score_band: str
    readiness_status: str
    human_review_required: bool
    publication_block_recommended: bool
    missing_requirements: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    blocking_reasons: list[str] = Field(default_factory=list)
    next_agent: str
    recommended_next_action: str | None
    calculated_at: datetime


class TaskBoardItem(BaseModel):
    task_id: str
    workflow_run_id: str
    news_item_id: str | None
    title: str
    task_type: str
    task_status: str
    priority: str
    assigned_agent: str
    assigned_to: str | None
    blocking: bool
    blocking_reason: str | None
    attempt_count: int
    max_attempts: int
    due_at: datetime | None
    created_at: datetime
    updated_at: datetime


class PublicationBoardItem(BaseModel):
    publication_record_id: str
    news_item_id: str
    content_piece_id: str
    distribution_plan_id: str
    title: str | None
    channel: str
    publication_status: str
    published_url: str | None
    external_id: str | None
    published_at: datetime | None
    owner: str | None
    created_at: datetime
    updated_at: datetime


class OwnershipUserSummary(BaseModel):
    user_id: str
    display_name: str
    role: str
    active_assignment_count: int
    active_task_count: int
    owned_news_count: int
    review_items_count: int


class OwnershipBoard(BaseModel):
    users: list[OwnershipUserSummary]
    assignments: list[dict[str, Any]]
    unassigned_news: list[str]
    unassigned_tasks: list[str]
    unassigned_content_pieces: list[str]


class UserWorkload(BaseModel):
    user: dict[str, Any]
    ownership_assignments: list[dict[str, Any]]
    workflow_tasks: list[TaskBoardItem]
    news_items_owned: list[str]
    blocking_tasks: list[TaskBoardItem]
    pending_reviews: list[dict[str, Any]]
    summary_counts: dict[str, int]


class OperationalGap(BaseModel):
    gap_type: str
    count: int
    severity: str
    recommended_action: str
    sample_entity_ids: list[str] = Field(default_factory=list)
