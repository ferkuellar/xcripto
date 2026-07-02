from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constants import AUDIT_SEVERITIES, AUDIT_STATUSES


class AuditCheckBase(BaseModel):
    entity_type: str = Field(min_length=2, max_length=80)
    entity_id: str = Field(min_length=1, max_length=80)
    audit_status: str = "pending"
    severity: str = "medium"
    decision_recommendation: str | None = Field(default=None, max_length=240)
    ready_to_advance: bool = False
    publication_block_recommended: bool = False
    missing_requirements: list[str] = Field(default_factory=list)
    audit_flags: list[str] = Field(default_factory=list)
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("audit_status")
    @classmethod
    def validate_audit_status(cls, value: str) -> str:
        if value not in AUDIT_STATUSES:
            raise ValueError(f"audit_status must be one of {sorted(AUDIT_STATUSES)}")
        return value

    @field_validator("severity")
    @classmethod
    def validate_severity(cls, value: str) -> str:
        if value not in AUDIT_SEVERITIES:
            raise ValueError(f"severity must be one of {sorted(AUDIT_SEVERITIES)}")
        return value


class AuditCheckCreate(AuditCheckBase):
    pass


class AuditCheckRead(AuditCheckBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
