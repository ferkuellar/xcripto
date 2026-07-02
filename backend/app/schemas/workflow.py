from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constants import (
    WORKFLOW_NEXT_AGENTS,
    WORKFLOW_READINESS_STATUSES,
    WORKFLOW_RUN_STATUSES,
    WORKFLOW_STEP_STATUSES,
    WORKFLOW_STEPS,
    WORKFLOW_TYPES,
)


class WorkflowStartRequest(BaseModel):
    workflow_type: str = "editorial_pipeline"

    @field_validator("workflow_type")
    @classmethod
    def validate_workflow_type(cls, value: str) -> str:
        if value not in WORKFLOW_TYPES:
            raise ValueError(f"workflow_type must be one of {sorted(WORKFLOW_TYPES)}")
        return value


class WorkflowStepRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    workflow_run_id: str
    step_name: str
    step_status: str
    required: bool
    completed: bool
    entity_type: str | None
    entity_id: str | None
    blocking: bool
    blocking_reason: str | None
    started_at: datetime | None
    completed_at: datetime | None
    correlation_id: str | None
    created_at: datetime
    updated_at: datetime


class WorkflowRunBase(BaseModel):
    news_item_id: str = Field(min_length=1, max_length=80)
    workflow_type: str = "editorial_pipeline"
    status: str = "created"
    current_step: str = "intake"
    readiness_status: str = "not_ready"
    blocked: bool = False
    blocking_reasons: list[str] = Field(default_factory=list)
    missing_requirements: list[str] = Field(default_factory=list)
    recommended_next_action: str | None = None
    next_agent: str = "None"
    correlation_id: str | None = Field(default=None, max_length=80)
    completed_at: datetime | None = None

    @field_validator("workflow_type")
    @classmethod
    def validate_workflow_type(cls, value: str) -> str:
        if value not in WORKFLOW_TYPES:
            raise ValueError(f"workflow_type must be one of {sorted(WORKFLOW_TYPES)}")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in WORKFLOW_RUN_STATUSES:
            raise ValueError(f"status must be one of {sorted(WORKFLOW_RUN_STATUSES)}")
        return value

    @field_validator("current_step")
    @classmethod
    def validate_current_step(cls, value: str) -> str:
        if value not in WORKFLOW_STEPS:
            raise ValueError(f"current_step must be one of {sorted(WORKFLOW_STEPS)}")
        return value

    @field_validator("readiness_status")
    @classmethod
    def validate_readiness_status(cls, value: str) -> str:
        if value not in WORKFLOW_READINESS_STATUSES:
            raise ValueError(
                f"readiness_status must be one of {sorted(WORKFLOW_READINESS_STATUSES)}"
            )
        return value

    @field_validator("next_agent")
    @classmethod
    def validate_next_agent(cls, value: str) -> str:
        if value not in WORKFLOW_NEXT_AGENTS:
            raise ValueError(f"next_agent must be one of {sorted(WORKFLOW_NEXT_AGENTS)}")
        return value


class WorkflowRunRead(WorkflowRunBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime


class WorkflowRunDetail(WorkflowRunRead):
    steps: list[WorkflowStepRead] = Field(default_factory=list)


class WorkflowStepCreate(BaseModel):
    workflow_run_id: str
    step_name: str
    step_status: str = "pending"
    required: bool = True
    completed: bool = False
    entity_type: str | None = None
    entity_id: str | None = None
    blocking: bool = False
    blocking_reason: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("step_name")
    @classmethod
    def validate_step_name(cls, value: str) -> str:
        if value not in WORKFLOW_STEPS:
            raise ValueError(f"step_name must be one of {sorted(WORKFLOW_STEPS)}")
        return value

    @field_validator("step_status")
    @classmethod
    def validate_step_status(cls, value: str) -> str:
        if value not in WORKFLOW_STEP_STATUSES:
            raise ValueError(f"step_status must be one of {sorted(WORKFLOW_STEP_STATUSES)}")
        return value
