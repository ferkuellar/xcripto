from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constants import SOURCE_STATUSES, TRUST_LEVELS


class SourceBase(BaseModel):
    source_name: str = Field(min_length=2, max_length=180)
    source_url: str = Field(min_length=1, max_length=2048)
    source_type: str = Field(min_length=2, max_length=80)
    source_status: str = "proposed"
    trust_level: str = "T2"
    notes: str | None = None
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("source_status")
    @classmethod
    def validate_source_status(cls, value: str) -> str:
        if value not in SOURCE_STATUSES:
            raise ValueError(f"source_status must be one of {sorted(SOURCE_STATUSES)}")
        return value

    @field_validator("trust_level")
    @classmethod
    def validate_trust_level(cls, value: str) -> str:
        if value not in TRUST_LEVELS:
            raise ValueError(f"trust_level must be one of {sorted(TRUST_LEVELS)}")
        return value


class SourceCreate(SourceBase):
    pass


class SourceRead(SourceBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
