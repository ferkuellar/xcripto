from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_api_key
from app.db.session import get_session
from app.schemas.workflow_task import (
    WorkflowTaskCancel,
    WorkflowTaskComplete,
    WorkflowTaskCreate,
    WorkflowTaskFail,
    WorkflowTaskRead,
    WorkflowTaskRetry,
    WorkflowTaskStart,
)
from app.schemas.workflow_task_summary import WorkflowTaskSummary
from app.services import operational_audit_service, workflow_task_service

router = APIRouter(tags=["workflow-tasks"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "/workflow-tasks",
    response_model=WorkflowTaskRead,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
async def create_workflow_task(
    payload: WorkflowTaskCreate,
    request: Request,
    session: SessionDep,
) -> WorkflowTaskRead:
    task = await workflow_task_service.create_workflow_task(
        session, payload, request.state.correlation_id
    )
    return WorkflowTaskRead.model_validate(task)


@router.get("/workflow-tasks", response_model=list[WorkflowTaskRead])
async def list_workflow_tasks(
    session: SessionDep,
    workflow_run_id: str | None = Query(default=None),
    workflow_step_id: str | None = Query(default=None),
    news_item_id: str | None = Query(default=None),
    task_type: str | None = Query(default=None),
    task_status: str | None = Query(default=None),
    priority: str | None = Query(default=None),
    assigned_agent: str | None = Query(default=None),
    assigned_to: str | None = Query(default=None),
    blocking: bool | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[WorkflowTaskRead]:
    tasks = await workflow_task_service.list_workflow_tasks(
        session,
        workflow_run_id=workflow_run_id,
        workflow_step_id=workflow_step_id,
        news_item_id=news_item_id,
        task_type=task_type,
        task_status=task_status,
        priority=priority,
        assigned_agent=assigned_agent,
        assigned_to=assigned_to,
        blocking=blocking,
        limit=limit,
        offset=offset,
    )
    return [WorkflowTaskRead.model_validate(task) for task in tasks]


@router.get("/workflow-tasks/{task_id}", response_model=WorkflowTaskRead)
async def get_workflow_task(task_id: str, session: SessionDep) -> WorkflowTaskRead:
    task = await workflow_task_service.get_workflow_task(session, task_id)
    return WorkflowTaskRead.model_validate(task)


@router.get("/workflows/{workflow_run_id}/tasks", response_model=list[WorkflowTaskRead])
async def list_workflow_tasks_by_workflow(
    workflow_run_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[WorkflowTaskRead]:
    tasks = await workflow_task_service.list_workflow_tasks(
        session, workflow_run_id=workflow_run_id, limit=limit, offset=offset
    )
    return [WorkflowTaskRead.model_validate(task) for task in tasks]


@router.get("/news/{news_id}/tasks", response_model=list[WorkflowTaskRead])
async def list_news_tasks(
    news_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[WorkflowTaskRead]:
    tasks = await workflow_task_service.list_workflow_tasks(
        session, news_item_id=news_id, limit=limit, offset=offset
    )
    return [WorkflowTaskRead.model_validate(task) for task in tasks]


@router.post(
    "/workflows/{workflow_run_id}/tasks/bootstrap",
    response_model=list[WorkflowTaskRead],
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
async def bootstrap_workflow_tasks(
    workflow_run_id: str,
    request: Request,
    session: SessionDep,
) -> list[WorkflowTaskRead]:
    tasks = await workflow_task_service.bootstrap_workflow_tasks(
        session, workflow_run_id, request.state.correlation_id
    )
    return [WorkflowTaskRead.model_validate(task) for task in tasks]


@router.get("/workflows/{workflow_run_id}/tasks/summary", response_model=WorkflowTaskSummary)
async def workflow_task_summary(
    workflow_run_id: str,
    session: SessionDep,
) -> WorkflowTaskSummary:
    summary = await workflow_task_service.summarize_workflow_tasks(session, workflow_run_id)
    return WorkflowTaskSummary.model_validate(summary)


@router.patch(
    "/workflow-tasks/{task_id}/start",
    response_model=WorkflowTaskRead,
    dependencies=[Depends(require_api_key)],
)
async def start_workflow_task(
    task_id: str,
    payload: WorkflowTaskStart,
    request: Request,
    session: SessionDep,
) -> WorkflowTaskRead:
    task = await workflow_task_service.start_workflow_task(session, task_id, payload.assigned_to)
    response = WorkflowTaskRead.model_validate(task)
    await _record_task_event(session, request, task, "workflow_task.start", "started")
    return response


@router.patch(
    "/workflow-tasks/{task_id}/complete",
    response_model=WorkflowTaskRead,
    dependencies=[Depends(require_api_key)],
)
async def complete_workflow_task(
    task_id: str,
    payload: WorkflowTaskComplete,
    request: Request,
    session: SessionDep,
) -> WorkflowTaskRead:
    task = await workflow_task_service.complete_workflow_task(
        session,
        task_id,
        agent_execution_id=payload.agent_execution_id,
        agent_output_id=payload.agent_output_id,
        output_ref=payload.output_ref,
        completed_with_warnings=payload.completed_with_warnings,
    )
    response = WorkflowTaskRead.model_validate(task)
    await _record_task_event(session, request, task, "workflow_task.complete", "completed")
    return response


@router.patch(
    "/workflow-tasks/{task_id}/fail",
    response_model=WorkflowTaskRead,
    dependencies=[Depends(require_api_key)],
)
async def fail_workflow_task(
    task_id: str,
    payload: WorkflowTaskFail,
    request: Request,
    session: SessionDep,
) -> WorkflowTaskRead:
    task = await workflow_task_service.fail_workflow_task(session, task_id, payload.reason)
    response = WorkflowTaskRead.model_validate(task)
    await _record_task_event(
        session, request, task, "workflow_task.fail", "failed", reason=payload.reason
    )
    return response


@router.patch(
    "/workflow-tasks/{task_id}/block",
    response_model=WorkflowTaskRead,
    dependencies=[Depends(require_api_key)],
)
async def block_workflow_task(
    task_id: str,
    payload: WorkflowTaskFail,
    request: Request,
    session: SessionDep,
) -> WorkflowTaskRead:
    task = await workflow_task_service.block_workflow_task(session, task_id, payload.reason)
    response = WorkflowTaskRead.model_validate(task)
    await _record_task_event(
        session, request, task, "workflow_task.block", "blocked", reason=payload.reason
    )
    return response


@router.patch(
    "/workflow-tasks/{task_id}/cancel",
    response_model=WorkflowTaskRead,
    dependencies=[Depends(require_api_key)],
)
async def cancel_workflow_task(
    task_id: str,
    payload: WorkflowTaskCancel,
    request: Request,
    session: SessionDep,
) -> WorkflowTaskRead:
    task = await workflow_task_service.cancel_workflow_task(session, task_id, payload.reason)
    response = WorkflowTaskRead.model_validate(task)
    await _record_task_event(
        session, request, task, "workflow_task.cancel", "cancelled", reason=payload.reason
    )
    return response


@router.patch(
    "/workflow-tasks/{task_id}/retry",
    response_model=WorkflowTaskRead,
    dependencies=[Depends(require_api_key)],
)
async def retry_workflow_task(
    task_id: str,
    _payload: WorkflowTaskRetry,
    request: Request,
    session: SessionDep,
) -> WorkflowTaskRead:
    task = await workflow_task_service.retry_workflow_task(session, task_id)
    response = WorkflowTaskRead.model_validate(task)
    await _record_task_event(session, request, task, "workflow_task.retry", "retried")
    return response


async def _record_task_event(
    session: SessionDep,
    request: Request,
    task,
    action: str,
    decision: str,
    reason: str | None = None,
) -> None:
    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="workflow_task_event",
        action=action,
        permission=action,
        decision=decision,
        outcome="succeeded",
        entity_type="WorkflowTask",
        entity_id=task.id,
        news_item_id=task.news_item_id,
        workflow_run_id=task.workflow_run_id,
        workflow_task_id=task.id,
        agent_output_id=task.agent_output_id,
        reason=reason,
        after_state={
            "task_status": task.task_status,
            "blocking": task.blocking,
            "attempt_count": task.attempt_count,
        },
    )
