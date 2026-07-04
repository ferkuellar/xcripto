from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.constants import (
    WORKFLOW_TASK_ASSIGNABLE_AGENTS,
    WORKFLOW_TASK_PRIORITIES,
    WORKFLOW_TASK_STATUSES,
    WORKFLOW_TASK_TYPES,
)


class WorkflowTaskBase(BaseModel):
    workflow_run_id: str = Field(min_length=1, max_length=80)
    workflow_step_id: str | None = Field(default=None, max_length=80)
    news_item_id: str | None = Field(default=None, max_length=80)
    task_type: str
    task_status: str = "queued"
    priority: str = "P3"
    assigned_agent: str = "None"
    assigned_to: str | None = Field(default=None, max_length=120)
    title: str = Field(min_length=1, max_length=280)
    description: str = Field(min_length=1)
    input_payload: dict[str, Any] | list[Any] | None = None
    output_ref: str | None = Field(default=None, max_length=180)
    agent_execution_id: str | None = Field(default=None, max_length=80)
    agent_output_id: str | None = Field(default=None, max_length=80)
    blocking: bool = False
    blocking_reason: str | None = None
    attempt_count: int = 0
    max_attempts: int = 3
    due_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    failed_at: datetime | None = None
    cancelled_at: datetime | None = None
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("task_type")
    @classmethod
    def validate_task_type(cls, value: str) -> str:
        if value not in WORKFLOW_TASK_TYPES:
            raise ValueError(f"task_type must be one of {sorted(WORKFLOW_TASK_TYPES)}")
        return value

    @field_validator("task_status")
    @classmethod
    def validate_task_status(cls, value: str) -> str:
        if value not in WORKFLOW_TASK_STATUSES:
            raise ValueError(f"task_status must be one of {sorted(WORKFLOW_TASK_STATUSES)}")
        return value

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value: str) -> str:
        if value not in WORKFLOW_TASK_PRIORITIES:
            raise ValueError(f"priority must be one of {sorted(WORKFLOW_TASK_PRIORITIES)}")
        return value

    @field_validator("assigned_agent")
    @classmethod
    def validate_assigned_agent(cls, value: str) -> str:
        if value not in WORKFLOW_TASK_ASSIGNABLE_AGENTS:
            raise ValueError(
                f"assigned_agent must be one of {sorted(WORKFLOW_TASK_ASSIGNABLE_AGENTS)}"
            )
        return value

    @model_validator(mode="after")
    def validate_task_relations(self) -> "WorkflowTaskBase":
        if self.input_payload is not None and not self.input_payload:
            raise ValueError("input_payload must be a non-empty object or array when provided")
        if self.workflow_step_id and not self.workflow_run_id:
            raise ValueError("workflow_run_id is required when workflow_step_id is provided")
        return self


class WorkflowTaskCreate(WorkflowTaskBase):
    pass


class WorkflowTaskStart(BaseModel):
    assigned_to: str | None = Field(default=None, max_length=120)


class WorkflowTaskComplete(BaseModel):
    agent_execution_id: str | None = Field(default=None, max_length=80)
    agent_output_id: str | None = Field(default=None, max_length=80)
    output_ref: str | None = Field(default=None, max_length=180)
    completed_with_warnings: bool = False


class WorkflowTaskFail(BaseModel):
    reason: str = Field(min_length=1)


class WorkflowTaskCancel(BaseModel):
    reason: str | None = Field(default=None, min_length=1)


class WorkflowTaskRetry(BaseModel):
    pass


class WorkflowTaskRead(WorkflowTaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
