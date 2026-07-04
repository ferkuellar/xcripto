from collections.abc import Callable
from secrets import compare_digest

from fastapi import HTTPException, Request

from app.core.config import get_settings
from app.core.permissions import is_valid_role, role_has_permission


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


def require_permission(permission_name: str) -> Callable[[Request], None]:
    async def dependency(request: Request) -> None:
        settings = get_settings()
        if not settings.auth_enabled:
            return

        await require_api_key(request)
        actor_role = request.headers.get("X-Actor-Role") or "system"
        request.state.actor_id = request.headers.get("X-Actor-Id")
        request.state.actor_role = actor_role

        if not is_valid_role(actor_role):
            raise HTTPException(status_code=403, detail="Invalid actor role")
        if not role_has_permission(actor_role, permission_name):
            raise HTTPException(status_code=403, detail="Insufficient permission")

    return dependency
