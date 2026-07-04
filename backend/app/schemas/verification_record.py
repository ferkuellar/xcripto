from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constants import CONFIDENCE_LEVELS, EVIDENCE_LEVELS, VERIFICATION_STATUSES


class VerificationRecordBase(BaseModel):
    news_item_id: str = Field(min_length=1, max_length=80)
    verification_status: str = "unverified"
    evidence_level: str = "unknown"
    confidence_level: str = "unknown"
    summary: str = Field(min_length=1)
    verified_claims: list[str] = Field(default_factory=list)
    unverified_claims: list[str] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    human_review_required: bool = False
    reviewer: str | None = Field(default=None, max_length=120)
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("verification_status")
    @classmethod
    def validate_verification_status(cls, value: str) -> str:
        if value not in VERIFICATION_STATUSES:
            raise ValueError(f"verification_status must be one of {sorted(VERIFICATION_STATUSES)}")
        return value

    @field_validator("evidence_level")
    @classmethod
    def validate_evidence_level(cls, value: str) -> str:
        if value not in EVIDENCE_LEVELS:
            raise ValueError(f"evidence_level must be one of {sorted(EVIDENCE_LEVELS)}")
        return value

    @field_validator("confidence_level")
    @classmethod
    def validate_confidence_level(cls, value: str) -> str:
        if value not in CONFIDENCE_LEVELS:
            raise ValueError(f"confidence_level must be one of {sorted(CONFIDENCE_LEVELS)}")
        return value


class VerificationRecordCreate(VerificationRecordBase):
    pass


class VerificationRecordRead(VerificationRecordBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
