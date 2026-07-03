from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_permission
from app.db.session import get_session
from app.schemas.admin_dashboard import (
    BlockerItem,
    DashboardOverview,
    EditorialWorkQueueItem,
    IntakeQueueItem,
    NewsroomHealth,
    OperationalGap,
    OwnershipBoard,
    PublicationBoardItem,
    ReadinessBoardItem,
    TaskBoardItem,
    UserWorkload,
)
from app.services import admin_dashboard_service

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
