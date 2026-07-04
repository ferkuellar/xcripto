from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constants import (
    CONTENT_STATUSES,
    CONTENT_TYPES,
    NEWS_PRIORITIES,
    RISK_LEVELS,
    VERIFICATION_STATUSES,
)


class ContentPieceBase(BaseModel):
    news_item_id: str = Field(min_length=1, max_length=80)
    content_type: str
    title: str = Field(min_length=3, max_length=280)
    summary: str = Field(min_length=1)
    body: str = Field(min_length=1)
    status: str = "drafting"
    category: str = Field(min_length=2, max_length=80)
    priority: str = "P3"
    verification_status: str
    risk_level: str
    source_refs: list[str] = Field(default_factory=list)
    disclaimer_required: bool = False
    human_review_required: bool = False
    owner: str | None = Field(default=None, max_length=120)
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("content_type")
    @classmethod
    def validate_content_type(cls, value: str) -> str:
        if value not in CONTENT_TYPES:
            raise ValueError(f"content_type must be one of {sorted(CONTENT_TYPES)}")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in CONTENT_STATUSES:
            raise ValueError(f"status must be one of {sorted(CONTENT_STATUSES)}")
        return value

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value: str) -> str:
        if value not in NEWS_PRIORITIES:
            raise ValueError(f"priority must be one of {sorted(NEWS_PRIORITIES)}")
        return value

    @field_validator("verification_status")
    @classmethod
    def validate_verification_status(cls, value: str) -> str:
        if value not in VERIFICATION_STATUSES:
            raise ValueError(f"verification_status must be one of {sorted(VERIFICATION_STATUSES)}")
        return value

    @field_validator("risk_level")
    @classmethod
    def validate_risk_level(cls, value: str) -> str:
        if value not in RISK_LEVELS:
            raise ValueError(f"risk_level must be one of {sorted(RISK_LEVELS)}")
        return value


class ContentPieceCreate(ContentPieceBase):
    pass


class ContentPieceStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in CONTENT_STATUSES:
            raise ValueError(f"status must be one of {sorted(CONTENT_STATUSES)}")
        return value


class ContentPieceRead(ContentPieceBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
