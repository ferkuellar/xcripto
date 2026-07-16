from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.session import get_session
from app.schemas.auth import (
    AuthLoginRequest,
    AuthLoginResponse,
    AuthMeResponse,
    AuthUserRead,
)
from app.services import operational_audit_service
from app.services.auth_service import (
    authenticate_user,
    cookie_settings,
    count_recent_failed_logins,
    create_session,
    login_rate_limit_exceeded,
    normalize_login_identifier,
    resolve_request_principal,
    revoke_session_by_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


def _build_user_payload(user) -> AuthUserRead:
    return AuthUserRead(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        handle=user.handle,
        role=user.role,
        roles=[user.role],
        is_active=user.is_active,
        last_login_at=user.last_login_at,
    )


@router.post("/login", response_model=AuthLoginResponse)
async def login(
    payload: AuthLoginRequest,
    request: Request,
    session: SessionDep,
) -> JSONResponse:
    identifier = normalize_login_identifier(payload.identifier)
    failed_attempts = await count_recent_failed_logins(session, identifier)
    if login_rate_limit_exceeded(failed_attempts):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts",
        )

    user = await authenticate_user(session, payload.identifier, payload.password)
    if user is None:
        await operational_audit_service.record_operational_event(
            session,
            request,
            event_type="auth_event",
            action="auth.login",
            decision="deny",
            outcome="failed",
            actor_id=identifier,
            actor_role="system",
            actor_source="login",
            metadata={"identifier": identifier, "reason": "invalid_credentials"},
        )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    auth_session, token = await create_session(session, user, request=request)
    request.state.actor_id = user.handle or user.email or user.id
    request.state.actor_role = user.role
    request.state.actor_source = "session"
    request.state.actor_display = user.display_name
    request.state.user_id = user.id
    request.state.auth_session_id = auth_session.id

    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="auth_event",
        action="auth.login",
        decision="accepted",
        outcome="succeeded",
        actor_id=user.handle or user.email or user.id,
        actor_role=user.role,
        actor_source="session",
        user_id=user.id,
        entity_type="AuthSession",
        entity_id=auth_session.id,
        metadata={"identifier": identifier},
    )

    payload_model = AuthLoginResponse(
        user=_build_user_payload(user),
        session={"session_expires_at": auth_session.expires_at, "authenticated": True},
    )
    response = JSONResponse(content=payload_model.model_dump(mode="json"))
    response.set_cookie(key=get_settings().session_cookie_name, value=token, **cookie_settings())
    return response


@router.get("/me", response_model=AuthMeResponse)
async def me(request: Request, session: SessionDep) -> AuthMeResponse:
    principal = await resolve_request_principal(request, session)
    if principal is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    return AuthMeResponse(
        authenticated=True,
        user=_build_user_payload(principal.user),
        session={
            "session_expires_at": principal.session.expires_at if principal.session else None,
            "authenticated": True,
        },
    )


@router.post("/logout", status_code=204)
async def logout(request: Request, session: SessionDep, response: Response) -> Response:
    settings = get_settings()
    token = request.cookies.get(settings.session_cookie_name)
    if token:
        await revoke_session_by_token(session, token)
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie(
        key=settings.session_cookie_name,
        path=settings.session_cookie_path,
        secure=settings.session_cookie_secure,
        samesite=settings.session_cookie_samesite,
    )
    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="auth_event",
        action="auth.logout",
        decision="deleted",
        outcome="succeeded",
        actor_id=getattr(request.state, "actor_id", None),
        actor_role=getattr(request.state, "actor_role", None),
        actor_source=getattr(request.state, "actor_source", None),
        user_id=getattr(request.state, "user_id", None),
        entity_type="AuthSession",
        entity_id=getattr(request.state, "auth_session_id", None),
    )
    return response
