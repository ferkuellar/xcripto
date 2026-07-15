from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import require_permission
from app.db.session import get_session
from app.schemas.admin_dashboard import (
    AdminAgentRunnerSummary,
    AdminAuditSummary,
    BlockerItem,
    DashboardOverview,
    EditorialWorkQueueItem,
    FrontendConfig,
    FrontendFeatureFlags,
    FrontendRouteMapGroup,
    FrontendRouteMapItem,
    IntakeQueueItem,
    NewsroomHealth,
    OperationalGap,
    OwnershipBoard,
    PublicationBoardItem,
    ReadinessBoardItem,
    TaskBoardItem,
    UserWorkload,
)
from app.schemas.external_connector import AdminConnectorsSummary
from app.services import (
    admin_dashboard_service,
    agent_runner_service,
    external_connector_service,
    operational_audit_service,
)

router = APIRouter(
    prefix="/admin",
    tags=["admin-dashboard"],
    dependencies=[Depends(require_permission("admin.dashboard.read"))],
)
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("/dashboard/overview", response_model=DashboardOverview)
async def dashboard_overview(session: SessionDep) -> DashboardOverview:
    return await admin_dashboard_service.get_dashboard_overview(session)


@router.get("/dashboard/newsroom-health", response_model=NewsroomHealth)
async def newsroom_health(session: SessionDep) -> NewsroomHealth:
    return await admin_dashboard_service.get_newsroom_health(session)


@router.get("/intake/queue", response_model=list[IntakeQueueItem])
async def intake_queue(
    session: SessionDep,
    signal_status: str | None = Query(default=None),
    dedupe_status: str | None = Query(default=None),
    priority: str | None = Query(default=None),
    topic: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[IntakeQueueItem]:
    return await admin_dashboard_service.get_intake_queue(
        session,
        signal_status=signal_status,
        dedupe_status=dedupe_status,
        priority=priority,
        topic=topic,
        limit=limit,
        offset=offset,
    )


@router.get("/editorial/work-queue", response_model=list[EditorialWorkQueueItem])
async def editorial_work_queue(session: SessionDep) -> list[EditorialWorkQueueItem]:
    return await admin_dashboard_service.get_editorial_work_queue(session)


@router.get("/blockers", response_model=list[BlockerItem])
async def blockers(session: SessionDep) -> list[BlockerItem]:
    return await admin_dashboard_service.get_blockers(session)


@router.get("/readiness/board", response_model=list[ReadinessBoardItem])
async def readiness_board(
    session: SessionDep,
    score_band: str | None = Query(default=None),
    readiness_status: str | None = Query(default=None),
    next_agent: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[ReadinessBoardItem]:
    return await admin_dashboard_service.get_readiness_board(
        session,
        score_band=score_band,
        readiness_status=readiness_status,
        next_agent=next_agent,
        limit=limit,
        offset=offset,
    )


@router.get("/tasks/board", response_model=list[TaskBoardItem])
async def task_board(
    session: SessionDep,
    task_status: str | None = Query(default=None),
    assigned_agent: str | None = Query(default=None),
    assigned_to: str | None = Query(default=None),
    priority: str | None = Query(default=None),
    blocking: bool | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[TaskBoardItem]:
    return await admin_dashboard_service.get_task_board(
        session,
        task_status=task_status,
        assigned_agent=assigned_agent,
        assigned_to=assigned_to,
        priority=priority,
        blocking=blocking,
        limit=limit,
        offset=offset,
    )


@router.get("/publications/board", response_model=list[PublicationBoardItem])
async def publication_board(
    session: SessionDep,
    publication_status: str | None = Query(default=None),
    channel: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[PublicationBoardItem]:
    return await admin_dashboard_service.get_publication_board(
        session,
        publication_status=publication_status,
        channel=channel,
        limit=limit,
        offset=offset,
    )


@router.get("/ownership/board", response_model=OwnershipBoard)
async def ownership_board(session: SessionDep) -> OwnershipBoard:
    return await admin_dashboard_service.get_ownership_board(session)


@router.get("/users/{user_id}/workload", response_model=UserWorkload)
async def user_workload(user_id: str, session: SessionDep) -> UserWorkload:
    return await admin_dashboard_service.get_user_workload(session, user_id)


@router.get("/gaps", response_model=list[OperationalGap])
async def operational_gaps(session: SessionDep) -> list[OperationalGap]:
    return await admin_dashboard_service.get_operational_gaps(session)


@router.get(
    "/audit/summary",
    response_model=AdminAuditSummary,
    dependencies=[Depends(require_permission("operational_audit.read"))],
)
async def audit_summary(session: SessionDep) -> AdminAuditSummary:
    summary = await operational_audit_service.get_admin_audit_summary(session)
    return AdminAuditSummary.model_validate(summary.model_dump())


@router.get(
    "/agent-runner/summary",
    response_model=AdminAgentRunnerSummary,
    dependencies=[Depends(require_permission("agent_runner.read"))],
)
async def agent_runner_summary(session: SessionDep) -> AdminAgentRunnerSummary:
    summary = await agent_runner_service.get_admin_agent_runner_summary(session)
    return AdminAgentRunnerSummary.model_validate(summary.model_dump())


@router.get(
    "/connectors/summary",
    response_model=AdminConnectorsSummary,
    dependencies=[Depends(require_permission("connector.read"))],
)
async def connectors_summary(session: SessionDep) -> AdminConnectorsSummary:
    summary = await external_connector_service.get_admin_connectors_summary(session)
    return AdminConnectorsSummary.model_validate(summary.model_dump())


@router.get("/frontend/config", response_model=FrontendConfig)
async def frontend_config() -> FrontendConfig:
    settings = get_settings()
    return FrontendConfig(
        app_name=settings.app_name,
        app_version=settings.app_version,
        environment=settings.environment,
        auth_enabled=settings.auth_enabled,
        rbac_enabled=True,
        features=FrontendFeatureFlags(),
        required_headers=["X-Correlation-ID"],
    )


@router.get("/frontend/route-map", response_model=list[FrontendRouteMapGroup])
async def frontend_route_map() -> list[FrontendRouteMapGroup]:
    return [
        _route_group(
            "health",
            [
                ("Health", "/health", "GET", None),
                ("Live", "/live", "GET", None),
                ("Ready", "/ready", "GET", None),
            ],
        ),
        _route_group(
            "dashboard",
            [
                ("Overview", "/api/v1/admin/dashboard/overview", "GET", "admin.dashboard.read"),
                (
                    "Newsroom health",
                    "/api/v1/admin/dashboard/newsroom-health",
                    "GET",
                    "admin.dashboard.read",
                ),
                ("Operational gaps", "/api/v1/admin/gaps", "GET", "admin.dashboard.read"),
            ],
        ),
        _route_group(
            "intake",
            [
                ("Intake queue", "/api/v1/admin/intake/queue", "GET", "admin.dashboard.read"),
                ("Create signal", "/api/v1/intake/signals", "POST", "intake.create"),
                (
                    "Promote signal",
                    "/api/v1/intake/signals/{signal_id}/promote",
                    "POST",
                    "intake.promote",
                ),
            ],
        ),
        _route_group(
            "workflow",
            [
                ("Work queue", "/api/v1/admin/editorial/work-queue", "GET", "admin.dashboard.read"),
                (
                    "Start workflow",
                    "/api/v1/workflows/news/{news_id}/start",
                    "POST",
                    "workflow.start",
                ),
                (
                    "Advance workflow",
                    "/api/v1/workflows/{workflow_run_id}/advance",
                    "POST",
                    "workflow.advance",
                ),
            ],
        ),
        _route_group(
            "tasks",
            [
                ("Task board", "/api/v1/admin/tasks/board", "GET", "admin.dashboard.read"),
                ("Create task", "/api/v1/workflow-tasks", "POST", "workflow_task.create"),
                (
                    "Complete task",
                    "/api/v1/workflow-tasks/{task_id}/complete",
                    "PATCH",
                    "workflow_task.complete",
                ),
            ],
        ),
        _route_group(
            "readiness",
            [
                ("Readiness board", "/api/v1/admin/readiness/board", "GET", "admin.dashboard.read"),
                (
                    "Calculate readiness",
                    "/api/v1/editorial-readiness/news/{news_id}/calculate",
                    "POST",
                    "readiness.calculate",
                ),
            ],
        ),
        _route_group(
            "agent_runner",
            [
                (
                    "Runner summary",
                    "/api/v1/admin/agent-runner/summary",
                    "GET",
                    "agent_runner.read",
                ),
                ("Capabilities", "/api/v1/agent-runner/capabilities", "GET", "agent_runner.read"),
                (
                    "Run task",
                    "/api/v1/agent-runner/tasks/{task_id}/run",
                    "POST",
                    "agent_runner.run",
                ),
            ],
        ),
        _route_group(
            "connectors",
            [
                ("Connectors summary", "/api/v1/admin/connectors/summary", "GET", "connector.read"),
                ("List connectors", "/api/v1/connectors", "GET", "connector.read"),
                (
                    "Dry-run connector",
                    "/api/v1/connectors/{connector_id}/dry-run",
                    "POST",
                    "connector.run",
                ),
            ],
        ),
        _route_group(
            "audit",
            [
                ("Audit summary", "/api/v1/admin/audit/summary", "GET", "operational_audit.read"),
                (
                    "Audit events",
                    "/api/v1/operational-audit/events",
                    "GET",
                    "operational_audit.read",
                ),
            ],
        ),
        _route_group(
            "ownership",
            [
                ("Ownership board", "/api/v1/admin/ownership/board", "GET", "admin.dashboard.read"),
                ("Assign ownership", "/api/v1/ownership/assign", "POST", "ownership.assign"),
            ],
        ),
        _route_group(
            "users",
            [
                ("Create user", "/api/v1/users", "POST", "user.create"),
                ("List users", "/api/v1/users", "GET", None),
            ],
        ),
    ]


def _route_group(
    group: str,
    routes: list[tuple[str, str, str, str | None]],
) -> FrontendRouteMapGroup:
    return FrontendRouteMapGroup(
        group=group,
        routes=[
            FrontendRouteMapItem(
                label=label,
                path=path,
                method=method,
                permission=permission,
                frontend_section=group,
            )
            for label, path, method, permission in routes
        ],
    )
