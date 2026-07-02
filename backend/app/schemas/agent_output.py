from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.constants import (
    AGENT_NAMES,
    AGENT_OUTPUT_STATUSES,
    AGENT_OUTPUT_TYPES,
    AGENT_OUTPUT_TYPES_BY_AGENT,
    WORKFLOW_NEXT_AGENTS,
)


class AgentOutputBase(BaseModel):
    agent_execution_id: str | None = Field(default=None, max_length=80)
    agent_name: str
    agent_version: str | None = Field(default=None, max_length=40)
    output_type: str
    status: str = "stored"
    entity_type: str | None = Field(default=None, max_length=80)
    entity_id: str | None = Field(default=None, max_length=80)
    news_item_id: str | None = Field(default=None, max_length=80)
    workflow_run_id: str | None = Field(default=None, max_length=80)
    workflow_step_id: str | None = Field(default=None, max_length=80)
    summary: str = Field(min_length=1)
    payload: dict[str, Any] | list[Any]
    risk_flags: list[str] = Field(default_factory=list)
    missing_requirements: list[str] = Field(default_factory=list)
    next_agent: str | None = None
    human_review_required: bool = False
    accepted: bool = False
    accepted_by: str | None = Field(default=None, max_length=120)
    accepted_at: datetime | None = None
    rejected_reason: str | None = None
    superseded_by_output_id: str | None = Field(default=None, max_length=80)
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("agent_name")
    @classmethod
    def validate_agent_name(cls, value: str) -> str:
        if value not in AGENT_NAMES:
            raise ValueError(f"agent_name must be one of {sorted(AGENT_NAMES)}")
        return value

    @field_validator("output_type")
    @classmethod
    def validate_output_type(cls, value: str) -> str:
        if value not in AGENT_OUTPUT_TYPES:
            raise ValueError(f"output_type must be one of {sorted(AGENT_OUTPUT_TYPES)}")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in AGENT_OUTPUT_STATUSES:
            raise ValueError(f"status must be one of {sorted(AGENT_OUTPUT_STATUSES)}")
        return value

    @field_validator("next_agent")
    @classmethod
    def validate_next_agent(cls, value: str | None) -> str | None:
        if value is not None and value not in WORKFLOW_NEXT_AGENTS:
            raise ValueError(f"next_agent must be one of {sorted(WORKFLOW_NEXT_AGENTS)}")
        return value

    @field_validator("payload")
    @classmethod
    def validate_payload(cls, value: dict[str, Any] | list[Any]) -> dict[str, Any] | list[Any]:
        if not value:
            raise ValueError("payload must be a non-empty object or array")
        return value

    @model_validator(mode="after")
    def validate_agent_output_type_pair(self) -> "AgentOutputBase":
        allowed_types = AGENT_OUTPUT_TYPES_BY_AGENT.get(self.agent_name, set())
        if self.output_type not in allowed_types:
            raise ValueError(f"{self.agent_name} cannot produce {self.output_type}")
        return self


class AgentOutputCreate(AgentOutputBase):
    pass


class AgentOutputAccept(BaseModel):
    accepted_by: str = Field(min_length=1, max_length=120)


class AgentOutputReject(BaseModel):
    rejected_reason: str = Field(min_length=1)


class AgentOutputSupersede(BaseModel):
    superseded_by_output_id: str = Field(min_length=1, max_length=80)


class AgentOutputRead(AgentOutputBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
