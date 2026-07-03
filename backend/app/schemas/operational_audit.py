from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constants import (
    OPERATIONAL_AUDIT_DECISIONS,
    OPERATIONAL_AUDIT_EVENT_TYPES,
    OPERATIONAL_AUDIT_OUTCOMES,
)


class OperationalAuditLogBase(BaseModel):
    event_type: str
    action: str = Field(min_length=1, max_length=120)
    permission: str | None = Field(default=None, max_length=120)
    actor_id: str | None = Field(default=None, max_length=120)
    actor_role: str | None = Field(default=None, max_length=60)
    actor_display: str | None = Field(default=None, max_length=180)
    actor_source: str | None = Field(default=None, max_length=40)
    request_method: str | None = Field(default=None, max_length=12)
    request_path: str | None = Field(default=None, max_length=500)
    entity_type: str | None = Field(default=None, max_length=120)
    entity_id: str | None = Field(default=None, max_length=120)
    news_item_id: str | None = Field(default=None, max_length=36)
    workflow_run_id: str | None = Field(default=None, max_length=36)
    workflow_task_id: str | None = Field(default=None, max_length=36)
    agent_output_id: str | None = Field(default=None, max_length=36)
    ownership_id: str | None = Field(default=None, max_length=36)
    user_id: str | None = Field(default=None, max_length=36)
    outcome: str
    decision: str
    reason: str | None = None
    before_state: dict[str, Any] | list[Any] | None = None
    after_state: dict[str, Any] | list[Any] | None = None
    metadata: dict[str, Any] | list[Any] | None = None
    error_code: str | None = Field(default=None, max_length=80)
    error_message: str | None = None
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("event_type")
    @classmethod
    def validate_event_type(cls, value: str) -> str:
        if value not in OPERATIONAL_AUDIT_EVENT_TYPES:
            raise ValueError(f"event_type must be one of {sorted(OPERATIONAL_AUDIT_EVENT_TYPES)}")
        return value

    @field_validator("outcome")
    @classmethod
    def validate_outcome(cls, value: str) -> str:
        if value not in OPERATIONAL_AUDIT_OUTCOMES:
            raise ValueError(f"outcome must be one of {sorted(OPERATIONAL_AUDIT_OUTCOMES)}")
        return value

    @field_validator("decision")
    @classmethod
    def validate_decision(cls, value: str) -> str:
        if value not in OPERATIONAL_AUDIT_DECISIONS:
            raise ValueError(f"decision must be one of {sorted(OPERATIONAL_AUDIT_DECISIONS)}")
        return value


class OperationalAuditLogCreate(OperationalAuditLogBase):
    pass


class OperationalAuditLogRead(OperationalAuditLogBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str
    created_at: datetime
    updated_at: datetime
    metadata: dict[str, Any] | list[Any] | None = Field(
        default=None,
        validation_alias="event_metadata",
        serialization_alias="metadata",
    )


class AdminAuditSummary(BaseModel):
    total_events: int
    events_by_type: dict[str, int] = Field(default_factory=dict)
    events_by_outcome: dict[str, int] = Field(default_factory=dict)
    events_by_decision: dict[str, int] = Field(default_factory=dict)
    recent_events: list[OperationalAuditLogRead] = Field(default_factory=list)
