from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_permission
from app.db.session import get_session
from app.schemas.agent_runner import (
    AgentCapability,
    AgentRunnerDryRunResponse,
    AgentRunnerRecentRunItem,
    AgentRunnerRunRequest,
    AgentRunnerRunResponse,
    AgentRunnerWorkflowRunNextRequest,
    AgentRunnerWorkflowRunNextResponse,
)
from app.services import agent_runner_service, operational_audit_service

router = APIRouter(prefix="/agent-runner", tags=["agent-runner"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get(
    "/capabilities",
    response_model=list[AgentCapability],
    dependencies=[Depends(require_permission("agent_runner.read"))],
)
async def list_capabilities() -> list[AgentCapability]:
    return agent_runner_service.get_agent_capabilities()


@router.post(
    "/tasks/{task_id}/dry-run",
    response_model=AgentRunnerDryRunResponse,
    dependencies=[Depends(require_permission("agent_runner.read"))],
)
async def dry_run_task(
    task_id: str,
    request: Request,
    session: SessionDep,
) -> AgentRunnerDryRunResponse:
    response = await agent_runner_service.dry_run_task(session, task_id)
    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="workflow_task_event",
        action="agent_runner.dry_run",
        permission="agent_runner.read",
        decision="no_op",
        entity_type="WorkflowTask",
        entity_id=task_id,
        workflow_task_id=task_id,
        outcome="succeeded" if response.eligible else "blocked",
        reason=response.reason,
        metadata={
            "agent_name": response.recommended_agent,
            "output_type": response.output_type,
        },
    )
    return response


@router.post(
    "/tasks/{task_id}/run",
    response_model=AgentRunnerRunResponse,
    dependencies=[Depends(require_permission("agent_runner.run"))],
)
async def run_task(
    task_id: str,
    payload: AgentRunnerRunRequest,
    request: Request,
    session: SessionDep,
) -> AgentRunnerRunResponse:
    response = await agent_runner_service.run_task(
        session,
        task_id,
        force=payload.force,
        runner=payload.runner,
        correlation_id=request.state.correlation_id,
    )
    await _record_run_event(
        session,
        request,
        response,
        action="agent_runner.run_task",
        force=payload.force,
        runner=payload.runner,
    )
    return response


@router.post(
    "/workflows/{workflow_run_id}/run-next",
    response_model=AgentRunnerWorkflowRunNextResponse,
    dependencies=[Depends(require_permission("agent_runner.run"))],
)
async def run_next_task(
    workflow_run_id: str,
    payload: AgentRunnerWorkflowRunNextRequest,
    request: Request,
    session: SessionDep,
) -> AgentRunnerWorkflowRunNextResponse:
    response = await agent_runner_service.run_next_task_for_workflow(
        session,
        workflow_run_id,
        force=payload.force,
        runner=payload.runner,
        correlation_id=request.state.correlation_id,
    )
    if response.result is None:
        await operational_audit_service.record_operational_event(
            session,
            request,
            event_type="workflow_task_event",
            action="agent_runner.run_next",
            permission="agent_runner.run",
            decision="no_op",
            outcome="skipped",
            entity_type="WorkflowRun",
            entity_id=workflow_run_id,
            workflow_run_id=workflow_run_id,
            metadata={"force": payload.force, "runner": payload.runner},
        )
    else:
        await _record_run_event(
            session,
            request,
            response.result,
            action="agent_runner.run_next",
            force=payload.force,
            runner=payload.runner,
        )
    return response


@router.get(
    "/runs",
    response_model=list[AgentRunnerRecentRunItem],
    dependencies=[Depends(require_permission("agent_runner.read"))],
)
async def list_recent_runs(
    session: SessionDep,
    agent_name: str | None = Query(default=None),
    status: str | None = Query(default=None),
    workflow_run_id: str | None = Query(default=None),
    news_item_id: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[AgentRunnerRecentRunItem]:
    return await agent_runner_service.list_recent_runs(
        session,
        agent_name=agent_name,
        status=status,
        workflow_run_id=workflow_run_id,
        news_item_id=news_item_id,
        limit=limit,
        offset=offset,
    )


async def _record_run_event(
    session: AsyncSession,
    request: Request,
    response: AgentRunnerRunResponse,
    *,
    action: str,
    force: bool,
    runner: str,
) -> None:
    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="workflow_task_event",
        action=action,
        permission="agent_runner.run",
        decision="completed",
        entity_type="WorkflowTask",
        entity_id=response.task.id,
        news_item_id=response.task.news_item_id,
        workflow_run_id=response.task.workflow_run_id,
        workflow_task_id=response.task.id,
        agent_output_id=response.output.id,
        metadata={
            "agent_name": response.output.agent_name,
            "output_type": response.output.output_type,
            "force": force,
            "runner": runner,
        },
    )
