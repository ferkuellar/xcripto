from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constants import AGENT_EXECUTION_STATUSES


class AgentExecutionBase(BaseModel):
    agent_name: str = Field(min_length=2, max_length=120)
    agent_version: str = Field(min_length=1, max_length=40)
    input_ref: str | None = Field(default=None, max_length=180)
    output_ref: str | None = Field(default=None, max_length=180)
    status: str = "queued"
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in AGENT_EXECUTION_STATUSES:
            raise ValueError(f"status must be one of {sorted(AGENT_EXECUTION_STATUSES)}")
        return value


class AgentExecutionCreate(AgentExecutionBase):
    pass


class AgentExecutionRead(AgentExecutionBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
