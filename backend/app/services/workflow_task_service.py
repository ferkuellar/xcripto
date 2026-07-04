from datetime import UTC, datetime

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (
    WORKFLOW_TASK_PRIORITIES,
)
from app.core.errors import ConflictError, DomainValidationError, NotFoundError
from app.models import (
    AgentExecution,
    AgentOutput,
    NewsItem,
    WorkflowRun,
    WorkflowStep,
    WorkflowTask,
)
from app.schemas.workflow_task import WorkflowTaskCreate

TERMINAL_TASK_STATUSES = {"completed", "completed_with_warnings", "cancelled", "archived"}
RETRYABLE_TASK_STATUSES = {"failed", "blocked", "retrying"}
STARTABLE_TASK_STATUSES = {
    "queued",
    "assigned",
    "running",
    "waiting_input",
    "waiting_review",
    "retrying",
    "escalated",
}
COMPLETED_TASK_STATUSES = {"completed", "completed_with_warnings"}

BOOTSTRAP_TASKS = [
    {
        "task_type": "source_validation",
        "assigned_agent": "SourceValidatorAgent",
        "title": "Validate sources",
        "description": "Validate sources before editorial drafting.",
        "workflow_step_name": "verification",
    },
    {
        "task_type": "risk_review",
        "assigned_agent": "RiskAgent",
        "title": "Review editorial risk",
        "description": "Assess editorial, legal and reputational risk.",
        "workflow_step_name": "risk_review",
    },
    {
        "task_type": "editorial_draft",
        "assigned_agent": "EditorialAgent",
        "title": "Draft editorial content",
        "description": "Prepare editorial draft from verified signals.",
        "workflow_step_name": "content_creation",
    },
    {
        "task_type": "audit_check",
        "assigned_agent": "AuditAgent",
        "title": "Run editorial audit",
        "description": "Confirm readiness for distribution and publication.",
        "workflow_step_name": "audit_review",
    },
    {
        "task_type": "distribution_planning",
        "assigned_agent": "DistributionAgent",
        "title": "Plan distribution",
        "description": "Plan distribution channels and publication timing.",
        "workflow_step_name": "distribution_planning",
    },
]


async def create_workflow_task(
    session: AsyncSession,
    payload: WorkflowTaskCreate,
    correlation_id: str | None = None,
) -> WorkflowTask:
    workflow_run = await _require_workflow_run(session, payload.workflow_run_id)
    workflow_step = await _optional_workflow_step(session, payload.workflow_step_id)
    news_item = await _optional_news_item(session, payload.news_item_id)
    agent_execution = await _optional_agent_execution(session, payload.agent_execution_id)
    agent_output = await _optional_agent_output(session, payload.agent_output_id)

    if payload.workflow_step_id and workflow_step.workflow_run_id != workflow_run.id:
        raise DomainValidationError("workflow_step_id must belong to workflow_run_id")
    if payload.news_item_id and news_item.id != workflow_run.news_item_id:
        raise DomainValidationError("news_item_id must match workflow_run_id")
    if agent_output is not None:
        if agent_output.news_item_id and agent_output.news_item_id != workflow_run.news_item_id:
            raise DomainValidationError("agent_output_id must match workflow_run_id news_item_id")
        if agent_output.workflow_run_id and agent_output.workflow_run_id != workflow_run.id:
            raise DomainValidationError("agent_output_id must match workflow_run_id")

    task = WorkflowTask(
        workflow_run_id=workflow_run.id,
        workflow_step_id=workflow_step.id if workflow_step is not None else None,
        news_item_id=(news_item.id if news_item is not None else workflow_run.news_item_id),
        task_type=payload.task_type,
        task_status=payload.task_status,
        priority=payload.priority,
        assigned_agent=payload.assigned_agent,
        assigned_to=payload.assigned_to,
        title=payload.title,
        description=payload.description,
        input_payload=payload.input_payload,
        output_ref=payload.output_ref,
        agent_execution_id=agent_execution.id if agent_execution is not None else None,
        agent_output_id=agent_output.id if agent_output is not None else None,
        blocking=payload.blocking,
        blocking_reason=payload.blocking_reason,
        attempt_count=payload.attempt_count,
        max_attempts=payload.max_attempts,
        due_at=payload.due_at,
        started_at=payload.started_at,
        completed_at=payload.completed_at,
        failed_at=payload.failed_at,
        cancelled_at=payload.cancelled_at,
        correlation_id=payload.correlation_id or correlation_id,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def list_workflow_tasks(
    session: AsyncSession,
    workflow_run_id: str | None = None,
    workflow_step_id: str | None = None,
    news_item_id: str | None = None,
    task_type: str | None = None,
    task_status: str | None = None,
    priority: str | None = None,
    assigned_agent: str | None = None,
    assigned_to: str | None = None,
    blocking: bool | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[WorkflowTask]:
    stmt = select(WorkflowTask).order_by(WorkflowTask.created_at.desc())
    if workflow_run_id is not None:
        stmt = stmt.where(WorkflowTask.workflow_run_id == workflow_run_id)
    if workflow_step_id is not None:
        stmt = stmt.where(WorkflowTask.workflow_step_id == workflow_step_id)
    if news_item_id is not None:
        stmt = stmt.where(WorkflowTask.news_item_id == news_item_id)
    if task_type is not None:
        stmt = stmt.where(WorkflowTask.task_type == task_type)
    if task_status is not None:
        stmt = stmt.where(WorkflowTask.task_status == task_status)
    if priority is not None:
        stmt = stmt.where(WorkflowTask.priority == priority)
    if assigned_agent is not None:
        stmt = stmt.where(WorkflowTask.assigned_agent == assigned_agent)
    if assigned_to is not None:
        stmt = stmt.where(WorkflowTask.assigned_to == assigned_to)
    if blocking is not None:
        stmt = stmt.where(WorkflowTask.blocking == blocking)
    result = await session.execute(stmt.limit(limit).offset(offset))
    return list(result.scalars().all())


async def get_workflow_task(session: AsyncSession, task_id: str) -> WorkflowTask:
    task = await session.get(WorkflowTask, task_id)
    if task is None:
        raise NotFoundError("Workflow task")
    return task


async def start_workflow_task(
    session: AsyncSession,
    task_id: str,
    assigned_to: str | None = None,
) -> WorkflowTask:
    task = await get_workflow_task(session, task_id)
    _ensure_non_terminal(task)
    if task.task_status not in STARTABLE_TASK_STATUSES:
        raise ConflictError(f"WorkflowTask with status {task.task_status} cannot be started")
    task.task_status = "running"
    task.started_at = task.started_at or datetime.now(UTC)
    if assigned_to is not None:
        task.assigned_to = assigned_to
    if task.assigned_agent == "None" and assigned_to is not None:
        task.assigned_agent = "HumanEditor"
    await session.commit()
    await session.refresh(task)
    return task


async def complete_workflow_task(
    session: AsyncSession,
    task_id: str,
    agent_execution_id: str | None = None,
    agent_output_id: str | None = None,
    output_ref: str | None = None,
    completed_with_warnings: bool = False,
) -> WorkflowTask:
    task = await get_workflow_task(session, task_id)
    _ensure_non_terminal(task)
    if task.task_status not in {
        "queued",
        "assigned",
        "running",
        "waiting_input",
        "waiting_review",
        "retrying",
        "escalated",
    }:
        raise ConflictError(f"WorkflowTask with status {task.task_status} cannot be completed")

    if agent_execution_id is not None:
        await _optional_agent_execution(session, agent_execution_id)
        task.agent_execution_id = agent_execution_id
    if agent_output_id is not None:
        output = await _optional_agent_output(session, agent_output_id)
        if output.workflow_run_id and output.workflow_run_id != task.workflow_run_id:
            raise DomainValidationError("agent_output_id must match workflow_run_id")
        if output.news_item_id and task.news_item_id and output.news_item_id != task.news_item_id:
            raise DomainValidationError("agent_output_id must match news_item_id")
        task.agent_output_id = agent_output_id

    task.output_ref = output_ref or task.output_ref
    task.task_status = "completed_with_warnings" if completed_with_warnings else "completed"
    task.completed_at = datetime.now(UTC)
    task.blocking = False
    task.blocking_reason = None
    await session.commit()
    await session.refresh(task)
    return task


async def fail_workflow_task(
    session: AsyncSession,
    task_id: str,
    reason: str,
) -> WorkflowTask:
    task = await get_workflow_task(session, task_id)
    _ensure_non_terminal(task)
    task.task_status = "failed"
    task.failed_at = datetime.now(UTC)
    task.blocking = True
    task.blocking_reason = reason
    await session.commit()
    await session.refresh(task)
    return task


async def block_workflow_task(
    session: AsyncSession,
    task_id: str,
    reason: str,
) -> WorkflowTask:
    task = await get_workflow_task(session, task_id)
    _ensure_non_terminal(task)
    task.task_status = "blocked"
    task.blocking = True
    task.blocking_reason = reason
    await session.commit()
    await session.refresh(task)
    return task


async def cancel_workflow_task(
    session: AsyncSession,
    task_id: str,
    reason: str | None = None,
) -> WorkflowTask:
    task = await get_workflow_task(session, task_id)
    _ensure_non_terminal(task)
    task.task_status = "cancelled"
    task.cancelled_at = datetime.now(UTC)
    if reason is not None:
        task.blocking_reason = reason
    await session.commit()
    await session.refresh(task)
    return task


async def retry_workflow_task(
    session: AsyncSession,
    task_id: str,
) -> WorkflowTask:
    task = await get_workflow_task(session, task_id)
    if task.task_status not in RETRYABLE_TASK_STATUSES:
        raise ConflictError(f"WorkflowTask with status {task.task_status} cannot be retried")
    if task.attempt_count >= task.max_attempts:
        raise ConflictError("WorkflowTask has reached max_attempts")

    task.attempt_count += 1
    task.task_status = "retrying"
    task.blocking = False
    task.blocking_reason = None
    task.failed_at = None
    task.cancelled_at = None
    await session.commit()
    await session.refresh(task)
    return task


async def bootstrap_workflow_tasks(
    session: AsyncSession,
    workflow_run_id: str,
    correlation_id: str | None = None,
) -> list[WorkflowTask]:
    workflow_run = await _require_workflow_run(session, workflow_run_id)
    news_item = await session.get(NewsItem, workflow_run.news_item_id)
    priority = news_item.priority if news_item is not None else "P3"
    if priority not in WORKFLOW_TASK_PRIORITIES:
        priority = "P3"

    existing = await session.execute(
        select(WorkflowTask.task_type).where(WorkflowTask.workflow_run_id == workflow_run.id)
    )
    existing_task_types = set(existing.scalars().all())

    created_tasks: list[WorkflowTask] = []
    for definition in BOOTSTRAP_TASKS:
        if definition["task_type"] in existing_task_types:
            continue
        workflow_step = await _workflow_step_by_name(
            session, workflow_run.id, definition["workflow_step_name"]
        )
        task = WorkflowTask(
            workflow_run_id=workflow_run.id,
            workflow_step_id=workflow_step.id if workflow_step is not None else None,
            news_item_id=workflow_run.news_item_id,
            task_type=definition["task_type"],
            task_status="queued",
            priority=priority,
            assigned_agent=definition["assigned_agent"],
            assigned_to=None,
            title=definition["title"],
            description=definition["description"],
            blocking=False,
            attempt_count=0,
            max_attempts=3,
            correlation_id=correlation_id or workflow_run.correlation_id,
        )
        session.add(task)
        created_tasks.append(task)

    await session.commit()
    for task in created_tasks:
        await session.refresh(task)
    return created_tasks


async def summarize_workflow_tasks(
    session: AsyncSession,
    workflow_run_id: str,
) -> dict[str, int]:
    total = await _count_tasks(session, workflow_run_id)
    completed = await _count_tasks(session, workflow_run_id, status_in=COMPLETED_TASK_STATUSES)
    blocking = await _count_tasks(session, workflow_run_id, blocking=True)
    pending = await _count_tasks(
        session,
        workflow_run_id,
        status_in={
            "queued",
            "assigned",
            "running",
            "waiting_input",
            "waiting_review",
            "retrying",
            "escalated",
        },
    )
    return {
        "task_count": int(total or 0),
        "completed_task_count": int(completed or 0),
        "blocking_task_count": int(blocking or 0),
        "pending_task_count": int(pending or 0),
    }


async def _require_workflow_run(session: AsyncSession, workflow_run_id: str) -> WorkflowRun:
    workflow_run = await session.get(WorkflowRun, workflow_run_id)
    if workflow_run is None:
        raise NotFoundError("Workflow run")
    return workflow_run


async def _workflow_step_by_name(
    session: AsyncSession,
    workflow_run_id: str,
    step_name: str,
) -> WorkflowStep | None:
    result = await session.execute(
        select(WorkflowStep)
        .where(
            WorkflowStep.workflow_run_id == workflow_run_id,
            WorkflowStep.step_name == step_name,
        )
        .limit(1)
    )
    return result.scalar_one_or_none()


async def _optional_workflow_step(
    session: AsyncSession,
    workflow_step_id: str | None,
) -> WorkflowStep | None:
    if workflow_step_id is None:
        return None
    workflow_step = await session.get(WorkflowStep, workflow_step_id)
    if workflow_step is None:
        raise NotFoundError("Workflow step")
    return workflow_step


async def _optional_news_item(
    session: AsyncSession,
    news_item_id: str | None,
) -> NewsItem | None:
    if news_item_id is None:
        return None
    news_item = await session.get(NewsItem, news_item_id)
    if news_item is None:
        raise NotFoundError("News item")
    return news_item


async def _optional_agent_execution(
    session: AsyncSession,
    agent_execution_id: str | None,
) -> AgentExecution | None:
    if agent_execution_id is None:
        return None
    agent_execution = await session.get(AgentExecution, agent_execution_id)
    if agent_execution is None:
        raise NotFoundError("Agent execution")
    return agent_execution


async def _optional_agent_output(
    session: AsyncSession,
    agent_output_id: str | None,
) -> AgentOutput | None:
    if agent_output_id is None:
        return None
    agent_output = await session.get(AgentOutput, agent_output_id)
    if agent_output is None:
        raise NotFoundError("Agent output")
    return agent_output


def _ensure_non_terminal(task: WorkflowTask) -> None:
    if task.task_status in {"completed", "completed_with_warnings", "cancelled", "archived"}:
        raise ConflictError(f"WorkflowTask with status {task.task_status} cannot be modified")


async def _count_tasks(
    session: AsyncSession,
    workflow_run_id: str,
    status_in: set[str] | None = None,
    blocking: bool | None = None,
) -> int:
    stmt = select(func.count(WorkflowTask.id)).where(
        WorkflowTask.workflow_run_id == workflow_run_id
    )
    if status_in is not None:
        stmt = stmt.where(WorkflowTask.task_status.in_(status_in))
    if blocking is not None:
        if blocking:
            stmt = stmt.where(
                or_(WorkflowTask.blocking.is_(True), WorkflowTask.task_status == "blocked")
            )
        else:
            stmt = stmt.where(WorkflowTask.blocking.is_(False))
    result = await session.execute(stmt)
    return int(result.scalar_one() or 0)
