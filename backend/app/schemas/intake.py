from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.constants import (
    INTAKE_ADAPTER_RUN_STATUSES,
    INTAKE_ADAPTER_TYPES,
    INTAKE_CONFIDENCE_LEVELS,
    INTAKE_DEDUPE_STATUSES,
    INTAKE_SIGNAL_STATUSES,
    INTAKE_SIGNAL_TYPES,
    NEWS_PRIORITIES,
)


class IntakeSignalBase(BaseModel):
    signal_type: str = "manual"
    signal_status: str = "received"
    source_name: str | None = Field(default=None, max_length=180)
    source_url: str | None = Field(default=None, max_length=2048)
    source_type: str | None = Field(default=None, max_length=80)
    source_published_at: datetime | None = None
    raw_title: str | None = Field(default=None, max_length=500)
    raw_summary: str | None = None
    raw_content: str | None = None
    normalized_title: str | None = None
    normalized_summary: str | None = None
    language: str | None = Field(default="en", max_length=20)
    topic: str | None = Field(default=None, max_length=120)
    asset_symbols: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    url_canonical: str | None = None
    content_hash: str | None = None
    dedupe_key: str | None = None
    priority: str = "P3"
    confidence_level: str = "unknown"
    risk_flags: list[str] = Field(default_factory=list)
    adapter_name: str | None = Field(default=None, max_length=120)
    adapter_version: str | None = Field(default=None, max_length=40)
    raw_payload: dict[str, Any] | list[Any] | None = None
    normalized_payload: dict[str, Any] | list[Any] | None = None
    duplicate_of_signal_id: str | None = Field(default=None, max_length=80)
    linked_news_item_id: str | None = Field(default=None, max_length=80)
    promoted_news_item_id: str | None = Field(default=None, max_length=80)
    dedupe_status: str = "not_checked"
    dedupe_score: float | None = None
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("signal_type")
    @classmethod
    def validate_signal_type(cls, value: str) -> str:
        if value not in INTAKE_SIGNAL_TYPES:
            raise ValueError(f"signal_type must be one of {sorted(INTAKE_SIGNAL_TYPES)}")
        return value

    @field_validator("signal_status")
    @classmethod
    def validate_signal_status(cls, value: str) -> str:
        if value not in INTAKE_SIGNAL_STATUSES:
            raise ValueError(f"signal_status must be one of {sorted(INTAKE_SIGNAL_STATUSES)}")
        return value

    @field_validator("dedupe_status")
    @classmethod
    def validate_dedupe_status(cls, value: str) -> str:
        if value not in INTAKE_DEDUPE_STATUSES:
            raise ValueError(f"dedupe_status must be one of {sorted(INTAKE_DEDUPE_STATUSES)}")
        return value

    @field_validator("confidence_level")
    @classmethod
    def validate_confidence_level(cls, value: str) -> str:
        if value not in INTAKE_CONFIDENCE_LEVELS:
            raise ValueError(
                f"confidence_level must be one of {sorted(INTAKE_CONFIDENCE_LEVELS)}"
            )
        return value

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value: str) -> str:
        if value not in NEWS_PRIORITIES:
            raise ValueError(f"priority must be one of {sorted(NEWS_PRIORITIES)}")
        return value

    @field_validator("source_url")
    @classmethod
    def validate_source_url(cls, value: str | None) -> str | None:
        if value is not None and not value.strip().lower().startswith(("http://", "https://")):
            raise ValueError("source_url must start with http:// or https://")
        return value

    @model_validator(mode="after")
    def validate_minimum_content(self) -> "IntakeSignalBase":
        if not (self.raw_title and self.raw_title.strip()) and not (
            self.raw_content and self.raw_content.strip()
        ):
            raise ValueError("IntakeSignal requires raw_title or raw_content")
        return self


class IntakeSignalCreate(IntakeSignalBase):
    pass


class IntakeSignalPromote(BaseModel):
    create_workflow: bool = False
    workflow_type: str = "editorial_pipeline"


class IntakeSignalReject(BaseModel):
    reason: str = Field(min_length=1)


class IntakeSignalRead(IntakeSignalBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    content_hash: str
    dedupe_key: str
    created_at: datetime
    updated_at: datetime


class IntakeAdapterRunBase(BaseModel):
    adapter_name: str = Field(min_length=1, max_length=120)
    adapter_version: str | None = Field(default=None, max_length=40)
    adapter_type: str
    status: str = "created"
    input_payload: dict[str, Any] | list[Any] | None = None
    result_payload: dict[str, Any] | list[Any] | None = None
    signals_created_count: int = Field(default=0, ge=0)
    signals_duplicate_count: int = Field(default=0, ge=0)
    signals_error_count: int = Field(default=0, ge=0)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("adapter_type")
    @classmethod
    def validate_adapter_type(cls, value: str) -> str:
        if value not in INTAKE_ADAPTER_TYPES:
            raise ValueError(f"adapter_type must be one of {sorted(INTAKE_ADAPTER_TYPES)}")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in INTAKE_ADAPTER_RUN_STATUSES:
            raise ValueError(f"status must be one of {sorted(INTAKE_ADAPTER_RUN_STATUSES)}")
        return value


class IntakeAdapterRunCreate(IntakeAdapterRunBase):
    pass


class IntakeAdapterRunRead(IntakeAdapterRunBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
