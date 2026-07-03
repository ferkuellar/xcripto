import logging
from time import perf_counter
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import get_settings

REQUEST_LOG_SKIP_PATHS = {"/health", "/live", "/ready", "/docs", "/openapi.json", "/redoc"}
request_logger = logging.getLogger("xmip.request")


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        correlation_id = request.headers.get("X-Correlation-ID") or f"corr_{uuid4().hex[:12]}"
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        settings = get_settings()
        if not settings.request_logging_enabled:
            return await call_next(request)

        start = perf_counter()
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        except Exception as exc:
            if request.url.path not in REQUEST_LOG_SKIP_PATHS:
                request_logger.exception(
                    "request failed",
                    extra={
                        "correlation_id": getattr(request.state, "correlation_id", None),
                        "request_method": request.method,
                        "request_path": request.url.path,
                        "status_code": status_code,
                        "duration_ms": round((perf_counter() - start) * 1000, 2),
                        "actor_role": getattr(request.state, "actor_role", None),
                        "exception_type": type(exc).__name__,
                    },
                )
            raise
        finally:
            if request.url.path not in REQUEST_LOG_SKIP_PATHS:
                request_logger.info(
                    "request completed",
                    extra={
                        "correlation_id": getattr(request.state, "correlation_id", None),
                        "request_method": request.method,
                        "request_path": request.url.path,
                        "status_code": status_code,
                        "duration_ms": round((perf_counter() - start) * 1000, 2),
                        "actor_role": getattr(request.state, "actor_role", None),
                    },
                )
