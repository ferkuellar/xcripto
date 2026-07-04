from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constants import OWNERSHIP_STATUSES, OWNERSHIP_TYPES


class OwnershipAssignmentBase(BaseModel):
    user_id: str = Field(min_length=1, max_length=80)
    entity_type: str = Field(min_length=1, max_length=120)
    entity_id: str = Field(min_length=1, max_length=120)
    ownership_type: str
    status: str = "active"
    assigned_by: str | None = Field(default=None, max_length=120)
    assigned_at: datetime | None = None
    released_at: datetime | None = None
    notes: str | None = None
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("ownership_type")
    @classmethod
    def validate_ownership_type(cls, value: str) -> str:
        if value not in OWNERSHIP_TYPES:
            raise ValueError(f"ownership_type must be one of {sorted(OWNERSHIP_TYPES)}")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in OWNERSHIP_STATUSES:
            raise ValueError(f"status must be one of {sorted(OWNERSHIP_STATUSES)}")
        return value


class OwnershipAssignmentCreate(OwnershipAssignmentBase):
    pass


class OwnershipRelease(BaseModel):
    reason: str | None = None


class OwnershipTransfer(BaseModel):
    new_user_id: str = Field(min_length=1, max_length=80)
    assigned_by: str | None = Field(default=None, max_length=120)
    notes: str | None = None


class OwnershipAssignmentRead(OwnershipAssignmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    assigned_at: datetime
    created_at: datetime
    updated_at: datetime
