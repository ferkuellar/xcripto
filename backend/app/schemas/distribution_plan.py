from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constants import (
    DISTRIBUTION_CHANNELS,
    DISTRIBUTION_STATUSES,
    DISTRIBUTION_TYPES,
    RISK_LEVELS,
)


class DistributionPlanBase(BaseModel):
    content_piece_id: str = Field(min_length=1, max_length=80)
    news_item_id: str = Field(min_length=1, max_length=80)
    primary_channel: str
    secondary_channels: list[str] = Field(default_factory=list)
    distribution_type: str
    status: str = "proposed"
    scheduled_at: datetime | None = None
    owner: str | None = Field(default=None, max_length=120)
    dependencies: list[str] = Field(default_factory=list)
    metric_plan: dict[str, Any] = Field(default_factory=dict)
    risk_level: str = "unknown"
    publication_readiness: str = Field(default="draft", min_length=1, max_length=80)
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("primary_channel")
    @classmethod
    def validate_primary_channel(cls, value: str) -> str:
        if value not in DISTRIBUTION_CHANNELS:
            raise ValueError(f"primary_channel must be one of {sorted(DISTRIBUTION_CHANNELS)}")
        return value

    @field_validator("secondary_channels")
    @classmethod
    def validate_secondary_channels(cls, value: list[str]) -> list[str]:
        invalid_channels = sorted(set(value) - DISTRIBUTION_CHANNELS)
        if invalid_channels:
            raise ValueError(f"secondary_channels contains invalid values: {invalid_channels}")
        return value

    @field_validator("distribution_type")
    @classmethod
    def validate_distribution_type(cls, value: str) -> str:
        if value not in DISTRIBUTION_TYPES:
            raise ValueError(f"distribution_type must be one of {sorted(DISTRIBUTION_TYPES)}")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in DISTRIBUTION_STATUSES:
            raise ValueError(f"status must be one of {sorted(DISTRIBUTION_STATUSES)}")
        return value

    @field_validator("risk_level")
    @classmethod
    def validate_risk_level(cls, value: str) -> str:
        if value not in RISK_LEVELS:
            raise ValueError(f"risk_level must be one of {sorted(RISK_LEVELS)}")
        return value


class DistributionPlanCreate(DistributionPlanBase):
    pass


class DistributionPlanStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in DISTRIBUTION_STATUSES:
            raise ValueError(f"status must be one of {sorted(DISTRIBUTION_STATUSES)}")
        return value


class DistributionPlanRead(DistributionPlanBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
