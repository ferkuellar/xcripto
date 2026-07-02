from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_api_key
from app.db.session import get_session
from app.schemas.workflow import WorkflowRunDetail, WorkflowRunRead, WorkflowStartRequest
from app.services import workflow_service

router = APIRouter(tags=["workflows"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def _workflow_detail(session: AsyncSession, workflow_run_id: str) -> WorkflowRunDetail:
    run = await workflow_service.get_workflow_run(session, workflow_run_id)
    steps = await workflow_service.get_workflow_steps(session, workflow_run_id)
    return WorkflowRunDetail.model_validate(run).model_copy(update={"steps": steps})


@router.post(
    "/workflows/news/{news_id}/start",
    response_model=WorkflowRunDetail,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
async def start_news_workflow(
    news_id: str,
    payload: WorkflowStartRequest,
    request: Request,
    session: SessionDep,
) -> WorkflowRunDetail:
    run = await workflow_service.create_workflow_run(
        session,
        news_id,
        workflow_type=payload.workflow_type,
        correlation_id=request.state.correlation_id,
    )
    return await _workflow_detail(session, run.id)


@router.get("/workflows", response_model=list[WorkflowRunRead])
async def list_workflows(
    session: SessionDep,
    news_item_id: str | None = Query(default=None),
    status: str | None = Query(default=None),
    workflow_type: str | None = Query(default=None),
    current_step: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[WorkflowRunRead]:
    runs = await workflow_service.list_workflow_runs(
        session,
        news_item_id=news_item_id,
        status=status,
        workflow_type=workflow_type,
        current_step=current_step,
        limit=limit,
        offset=offset,
    )
    return [WorkflowRunRead.model_validate(run) for run in runs]


@router.get("/workflows/{workflow_run_id}", response_model=WorkflowRunDetail)
async def get_workflow(workflow_run_id: str, session: SessionDep) -> WorkflowRunDetail:
    return await _workflow_detail(session, workflow_run_id)


@router.get("/news/{news_id}/workflow", response_model=WorkflowRunDetail)
async def get_news_workflow(news_id: str, session: SessionDep) -> WorkflowRunDetail:
    run = await workflow_service.get_latest_workflow_for_news(session, news_id)
    return await _workflow_detail(session, run.id)


@router.post(
    "/workflows/{workflow_run_id}/recalculate",
    response_model=WorkflowRunDetail,
    dependencies=[Depends(require_api_key)],
)
async def recalculate_workflow(
    workflow_run_id: str,
    session: SessionDep,
) -> WorkflowRunDetail:
    run = await workflow_service.recalculate_workflow_run(session, workflow_run_id)
    return await _workflow_detail(session, run.id)


@router.post(
    "/workflows/{workflow_run_id}/advance",
    response_model=WorkflowRunDetail,
    dependencies=[Depends(require_api_key)],
)
async def advance_workflow(
    workflow_run_id: str,
    session: SessionDep,
) -> WorkflowRunDetail:
    run = await workflow_service.advance_workflow_run(session, workflow_run_id)
    return await _workflow_detail(session, run.id)
