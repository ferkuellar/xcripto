from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AuthLoginRequest(BaseModel):
    identifier: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=256)


class AuthUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str | None
    display_name: str
    handle: str | None
    role: str
    roles: list[str] = Field(default_factory=list)
    is_active: bool
    last_login_at: datetime | None


class AuthSessionInfo(BaseModel):
    session_expires_at: datetime
    authenticated: bool = True


class AuthLoginResponse(BaseModel):
    user: AuthUserRead
    session: AuthSessionInfo


class AuthMeResponse(BaseModel):
    authenticated: bool = True
    user: AuthUserRead
    session: AuthSessionInfo
