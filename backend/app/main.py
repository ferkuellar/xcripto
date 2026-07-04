from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.errors import (
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.core.logging import configure_logging
from app.core.middleware import CorrelationIdMiddleware, RequestLoggingMiddleware
from app.db import health as db_health
from app.db.init_db import init_db

settings = get_settings()
configure_logging(settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    if settings.auto_create_tables:
        await init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    description="Backend API for the XMIP multiagent newsroom platform (XCripto / ORION).",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
    expose_headers=["X-Total-Count", "X-Correlation-ID"],
)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.service_name,
        "version": settings.app_version,
    }


@app.get("/live", tags=["health"])
async def live() -> dict[str, str]:
    return {
        "status": "alive",
        "service": settings.service_name,
        "version": settings.app_version,
    }


@app.get("/ready", tags=["health"])
async def ready() -> JSONResponse:
    checks = {"configuration": "ok"}
    status = "ready"
    status_code = 200
    if settings.db_healthcheck_enabled:
        try:
            await db_health.check_database_health()
            checks["database"] = "ok"
        except Exception:
            checks["database"] = "failed"
            status = "not_ready"
            status_code = 503
    else:
        checks["database"] = "skipped"
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status,
            "service": settings.service_name,
            "version": settings.app_version,
            "checks": checks,
        },
    )
