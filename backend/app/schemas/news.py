from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constants import NEWS_PRIORITIES, NEWS_STATUSES


class NewsBase(BaseModel):
    title: str = Field(min_length=3, max_length=280)
    summary: str = Field(min_length=1)
    category: str = Field(min_length=2, max_length=80)
    priority: str = "P3"
    source_url: str = Field(min_length=1, max_length=2048)
    source_name: str = Field(min_length=2, max_length=180)
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value: str) -> str:
        if value not in NEWS_PRIORITIES:
            raise ValueError(f"priority must be one of {sorted(NEWS_PRIORITIES)}")
        return value


class NewsCreate(NewsBase):
    status: str = "detected"

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in NEWS_STATUSES:
            raise ValueError(f"status must be one of {sorted(NEWS_STATUSES)}")
        return value


class NewsStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in NEWS_STATUSES:
            raise ValueError(f"status must be one of {sorted(NEWS_STATUSES)}")
        return value


class NewsRead(NewsBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    status: str
    created_at: datetime
    updated_at: datetime
