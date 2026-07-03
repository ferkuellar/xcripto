from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constants import USER_ROLES, USER_STATUSES


class UserAccountBase(BaseModel):
    email: str | None = Field(default=None, max_length=255)
    display_name: str = Field(min_length=1, max_length=180)
    handle: str | None = Field(default=None, min_length=1, max_length=80)
    status: str = "active"
    role: str
    is_active: bool = True
    is_system_user: bool = False
    timezone: str | None = Field(default=None, max_length=80)
    notes: str | None = None
    last_seen_at: datetime | None = None
    correlation_id: str | None = Field(default=None, max_length=80)

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in USER_STATUSES:
            raise ValueError(f"status must be one of {sorted(USER_STATUSES)}")
        return value

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        if value not in USER_ROLES:
            raise ValueError(f"role must be one of {sorted(USER_ROLES)}")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str | None) -> str | None:
        if value is not None and "@" not in value:
            raise ValueError("email must contain @")
        return value


class UserAccountCreate(UserAccountBase):
    pass


class UserAccountUpdate(BaseModel):
    email: str | None = Field(default=None, max_length=255)
    display_name: str | None = Field(default=None, min_length=1, max_length=180)
    handle: str | None = Field(default=None, min_length=1, max_length=80)
    status: str | None = None
    role: str | None = None
    is_active: bool | None = None
    is_system_user: bool | None = None
    timezone: str | None = Field(default=None, max_length=80)
    notes: str | None = None
    last_seen_at: datetime | None = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str | None) -> str | None:
        if value is not None and value not in USER_STATUSES:
            raise ValueError(f"status must be one of {sorted(USER_STATUSES)}")
        return value

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str | None) -> str | None:
        if value is not None and value not in USER_ROLES:
            raise ValueError(f"role must be one of {sorted(USER_ROLES)}")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str | None) -> str | None:
        if value is not None and "@" not in value:
            raise ValueError("email must contain @")
        return value


class UserAccountRead(UserAccountBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
