from fastapi import APIRouter

from app.api.v1.endpoints import agent_executions, audit_checks, news, sources

api_router = APIRouter()
api_router.include_router(news.router)
api_router.include_router(sources.router)
api_router.include_router(agent_executions.router)
api_router.include_router(audit_checks.router)
