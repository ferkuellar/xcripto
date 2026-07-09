from fastapi import APIRouter

from app.api.v1.endpoints import (
    admin_dashboard,
    agent_executions,
    agent_outputs,
    agent_runner,
    audit_checks,
    connectors,
    content_pieces,
    distribution_plans,
    editorial_readiness,
    intake,
    knowledge,
    memory_items,
    metric_snapshots,
    news,
    operational_audit,
    ownership,
    public_news,
    publication_records,
    risk_reviews,
    sources,
    users,
    verification_records,
    workflow_tasks,
    workflows,
)

api_router = APIRouter()
api_router.include_router(admin_dashboard.router)
api_router.include_router(agent_runner.router)
api_router.include_router(connectors.router)
api_router.include_router(news.router)
api_router.include_router(operational_audit.router)
api_router.include_router(sources.router)
api_router.include_router(agent_executions.router)
api_router.include_router(agent_outputs.router)
api_router.include_router(audit_checks.router)
api_router.include_router(verification_records.router)
api_router.include_router(risk_reviews.router)
api_router.include_router(content_pieces.router)
api_router.include_router(distribution_plans.router)
api_router.include_router(editorial_readiness.router)
api_router.include_router(intake.router)
api_router.include_router(publication_records.router)
api_router.include_router(public_news.router)
api_router.include_router(workflow_tasks.router)
api_router.include_router(metric_snapshots.router)
api_router.include_router(memory_items.router)
api_router.include_router(knowledge.router)
api_router.include_router(ownership.router)
api_router.include_router(users.router)
api_router.include_router(workflows.router)
