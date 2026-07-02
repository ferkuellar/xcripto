from fastapi import APIRouter

from app.api.v1.endpoints import (
    agent_executions,
    agent_outputs,
    audit_checks,
    content_pieces,
    distribution_plans,
    news,
    publication_records,
    risk_reviews,
    sources,
    verification_records,
    workflows,
)

api_router = APIRouter()
api_router.include_router(news.router)
api_router.include_router(sources.router)
api_router.include_router(agent_executions.router)
api_router.include_router(agent_outputs.router)
api_router.include_router(audit_checks.router)
api_router.include_router(verification_records.router)
api_router.include_router(risk_reviews.router)
api_router.include_router(content_pieces.router)
api_router.include_router(distribution_plans.router)
api_router.include_router(publication_records.router)
api_router.include_router(workflows.router)
