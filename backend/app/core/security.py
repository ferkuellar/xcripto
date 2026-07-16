from collections.abc import Callable
from secrets import compare_digest
from typing import Annotated

from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.permissions import is_valid_role, role_has_permission
from app.db.session import get_session
from app.services.auth_service import resolve_request_principal

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def require_api_key(request: Request) -> None:
    settings = get_settings()
    if not settings.auth_enabled:
        return

    if not settings.api_key:
        raise HTTPException(
            status_code=500,
            detail="API key auth is enabled but API_KEY is not configured",
        )

    provided_api_key = request.headers.get(settings.api_key_header_name)
    if provided_api_key is None:
        raise HTTPException(status_code=401, detail="Missing API key")

    if not compare_digest(provided_api_key, settings.api_key):
        raise HTTPException(status_code=403, detail="Invalid API key")


def _set_legacy_request_state(request: Request) -> tuple[str, str]:
    actor_role = request.headers.get("X-Actor-Role") or "system"
    actor_id = request.headers.get("X-Actor-Id") or actor_role
    request.state.actor_id = actor_id
    request.state.actor_role = actor_role
    request.state.actor_source = "header"
    request.state.actor_display = request.headers.get("X-Actor-Display")
    request.state.user_id = None
    request.state.auth_session_id = None
    return actor_id, actor_role


def _set_session_request_state(request: Request, principal) -> None:
    request.state.actor_id = principal.actor_id
    request.state.actor_role = principal.actor_role
    request.state.actor_source = principal.actor_source
    request.state.actor_display = principal.user.display_name
    request.state.user_id = principal.user.id
    request.state.auth_session_id = principal.session.id if principal.session else None


def require_permission(permission_name: str) -> Callable[[Request, SessionDep], None]:
    async def dependency(request: Request, session: SessionDep) -> None:
        settings = get_settings()
        if not settings.auth_enabled:
            return

        principal = await resolve_request_principal(request, session)
        if principal is not None:
            _set_session_request_state(request, principal)
            if permission_name not in principal.permissions:
                raise HTTPException(status_code=403, detail="Insufficient permission")
            return

        if settings.is_deployed_environment:
            raise HTTPException(status_code=401, detail="Authentication required")

        await require_api_key(request)
        actor_id, actor_role = _set_legacy_request_state(request)
        if not is_valid_role(actor_role):
            raise HTTPException(status_code=403, detail="Invalid actor role")
        if not role_has_permission(actor_role, permission_name):
            raise HTTPException(status_code=403, detail="Insufficient permission")
        request.state.actor_id = actor_id

    return dependency


def require_authentication() -> Callable[[Request, SessionDep], None]:
    async def dependency(request: Request, session: SessionDep) -> None:
        settings = get_settings()
        if not settings.auth_enabled:
            return

        principal = await resolve_request_principal(request, session)
        if principal is not None:
            _set_session_request_state(request, principal)
            return

        if settings.is_deployed_environment:
            raise HTTPException(status_code=401, detail="Authentication required")

        await require_api_key(request)
        _set_legacy_request_state(request)

    return dependency
