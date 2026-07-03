from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.constants import (
    MEMORY_CONFIDENCE_LEVELS,
    MEMORY_EXPIRATION_RECOMMENDATIONS,
    MEMORY_PERSISTENCE_LEVELS,
    MEMORY_SCOPES,
    MEMORY_STATUSES,
    MEMORY_TYPES,
)

AUTO_REVIEW_MEMORY_TYPES = {"source_memory", "risk_memory", "incident_memory"}


class MemoryItemBase(BaseModel):
    memory_type: str
    memory_status: str = "proposed"
    title: str = Field(min_length=1, max_length=280)
    memory_statement: str = Field(min_length=1)
    why_it_matters: str | None = None
    how_to_use: str | None = None
    how_not_to_use: str | None = None
    source_or_origin: str = Field(min_length=1)
    entity_type: str | None = Field(default=None, max_length=80)
    entity_id: str | None = Field(default=None, max_length=80)
    news_item_id: str | None = Field(default=None, max_length=80)
    workflow_run_id: str | None = Field(default=None, max_length=80)
    agent_output_id: str | None = Field(default=None, max_length=80)
    audit_check_id: str | None = Field(default=None, max_length=80)
    metric_snapshot_id: str | None = Field(default=None, max_length=80)
    confidence_level: str = "MC2"
    persistence_level: str = "M2"
    scope: str = "topic_specific"
    risk_flags: list[str] = Field(default_factory=list)
    expiration_recommendation: str = "review_quarterly"
    expires_at: datetime | None = None
    human_review_required: bool = False
    approved_by: str | None = Field(default=None, max_length=120)
    approved_at: datetime | None = None
    invalidated_by: str | None = Field(default=None, max_length=120)
    invalidated_at: datetime | None = None
    invalidation_reason: str | None = None
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("memory_type")
    @classmethod
    def validate_memory_type(cls, value: str) -> str:
        if value not in MEMORY_TYPES:
            raise ValueError(f"memory_type must be one of {sorted(MEMORY_TYPES)}")
        return value

    @field_validator("memory_status")
    @classmethod
    def validate_memory_status(cls, value: str) -> str:
        if value not in MEMORY_STATUSES:
            raise ValueError(f"memory_status must be one of {sorted(MEMORY_STATUSES)}")
        return value

    @field_validator("confidence_level")
    @classmethod
    def validate_confidence_level(cls, value: str) -> str:
        if value not in MEMORY_CONFIDENCE_LEVELS:
            raise ValueError(f"confidence_level must be one of {sorted(MEMORY_CONFIDENCE_LEVELS)}")
        return value

    @field_validator("persistence_level")
    @classmethod
    def validate_persistence_level(cls, value: str) -> str:
        if value not in MEMORY_PERSISTENCE_LEVELS:
            raise ValueError(
                f"persistence_level must be one of {sorted(MEMORY_PERSISTENCE_LEVELS)}"
            )
        return value

    @field_validator("scope")
    @classmethod
    def validate_scope(cls, value: str) -> str:
        if value not in MEMORY_SCOPES:
            raise ValueError(f"scope must be one of {sorted(MEMORY_SCOPES)}")
        return value

    @field_validator("expiration_recommendation")
    @classmethod
    def validate_expiration_recommendation(cls, value: str) -> str:
        if value not in MEMORY_EXPIRATION_RECOMMENDATIONS:
            raise ValueError(
                "expiration_recommendation must be one of "
                f"{sorted(MEMORY_EXPIRATION_RECOMMENDATIONS)}"
            )
        return value

    @model_validator(mode="after")
    def validate_relations(self) -> "MemoryItemBase":
        if (self.entity_type and not self.entity_id) or (self.entity_id and not self.entity_type):
            raise ValueError("entity_type and entity_id must be provided together")
        return self


class MemoryItemCreate(MemoryItemBase):
    pass


class MemoryItemApprove(BaseModel):
    approved_by: str = Field(min_length=1, max_length=120)


class MemoryItemReject(BaseModel):
    reason: str = Field(min_length=1)


class MemoryItemInvalidate(BaseModel):
    invalidated_by: str = Field(min_length=1, max_length=120)
    reason: str = Field(min_length=1)


class MemoryItemArchive(BaseModel):
    reason: str | None = Field(default=None, min_length=1)


class MemoryItemRead(MemoryItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
