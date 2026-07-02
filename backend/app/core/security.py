from secrets import compare_digest

from fastapi import HTTPException, Request

from app.core.config import get_settings


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
