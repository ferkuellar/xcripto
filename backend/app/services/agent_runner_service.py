from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ConflictError, NotFoundError
from app.models import AgentExecution, AgentOutput, WorkflowRun, WorkflowTask
from app.schemas.agent_execution import AgentExecutionCreate, AgentExecutionRead
from app.schemas.agent_output import AgentOutputCreate, AgentOutputRead
from app.schemas.agent_runner import (
    AdminAgentRunnerSummary,
    AgentCapability,
    AgentRunnerDryRunResponse,
    AgentRunnerRecentRunItem,
    AgentRunnerRunResponse,
    AgentRunnerTaskEligibility,
    AgentRunnerWorkflowRunNextResponse,
)
from app.schemas.workflow_task import WorkflowTaskRead
from app.services import agent_output_service, workflow_task_service

INTERNAL_RUNNER_VERSION = "internal-runner-v1"
TERMINAL_STATUSES = {"completed", "completed_with_warnings", "cancelled", "archived"}
RUNNABLE_STATUSES = {
    "queued",
    "assigned",
    "running",
    "waiting_input",
    "waiting_review",
    "retrying",
    "escalated",
}
PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "P4": 4}

TASK_AGENT_MAP = {
    "news_intake": "NewsScoutAgent",
    "source_validation": "SourceValidatorAgent",
    "market_impact_assessment": "MarketImpactAgent",
    "risk_review": "RiskAgent",
    "editorial_draft": "EditorialAgent",
    "script_generation": "ScriptAgent",
    "social_variant_generation": "SocialClipAgent",
    "distribution_planning": "DistributionAgent",
    "audit_check": "AuditAgent",
    "calendar_scheduling": "CalendarAgent",
    "metrics_review": "MetricsAgent",
    "memory_review": "MemoryAgent",
    "knowledge_update": "KnowledgeAgent",
    "workflow_recalculation": "System",
    "publication_preparation": "DistributionAgent",
    "generic_task": "System",
}

AGENT_OUTPUT_TYPE_MAP = {
    "NewsScoutAgent": "news_scout_report",
    "SourceValidatorAgent": "source_review",
    "RiskAgent": "risk_review",
    "MarketImpactAgent": "market_impact_assessment",
    "EditorialAgent": "editorial_output",
    "ScriptAgent": "script_output",
    "SocialClipAgent": "social_output",
    "DistributionAgent": "distribution_plan_output",
    "AuditAgent": "audit_check_output",
    "MemoryAgent": "memory_proposal",
    "KnowledgeAgent": "knowledge_graph_proposal",
    "CalendarAgent": "calendar_recommendation",
    "MetricsAgent": "metrics_review",
    "System": "workflow_recommendation",
}

HUMAN_REVIEW_AGENTS = {"RiskAgent", "AuditAgent", "MemoryAgent", "KnowledgeAgent"}


def get_agent_capabilities() -> list[AgentCapability]:
    capabilities: dict[str, list[str]] = {}
    for task_type, agent_name in TASK_AGENT_MAP.items():
        capabilities.setdefault(agent_name, []).append(task_type)

    return [
        AgentCapability(
            agent_name=agent_name,
            supported_task_types=sorted(task_types),
            output_type=AGENT_OUTPUT_TYPE_MAP[agent_name],
            description=(
                "Deterministic internal runner stub. It creates auditable AgentOutput "
                "records without external AI or publication side effects."
            ),
        )
        for agent_name, task_types in sorted(capabilities.items())
    ]


async def dry_run_task(
    session: AsyncSession,
    task_id: str,
    force: bool = False,
) -> AgentRunnerDryRunResponse:
    task = await workflow_task_service.get_workflow_task(session, task_id)
    eligibility = evaluate_task_eligibility(task, force=force)
    payload_preview = build_agent_payload(
        task,
        agent_name=eligibility.recommended_agent or "System",
        output_type=eligibility.output_type or "generic_agent_output",
    )
    return AgentRunnerDryRunResponse(
        task_id=task.id,
        eligible=eligibility.eligible,
        reason=eligibility.reason,
        recommended_agent=eligibility.recommended_agent,
        output_type=eligibility.output_type,
        payload_preview=payload_preview,
    )


async def run_task(
    session: AsyncSession,
    task_id: str,
    *,
    force: bool = False,
    runner: str = "internal",
    correlation_id: str | None = None,
) -> AgentRunnerRunResponse:
    task = await workflow_task_service.get_workflow_task(session, task_id)
    eligibility = evaluate_task_eligibility(task, force=force)
    if not eligibility.eligible:
        raise ConflictError(eligibility.reason or "WorkflowTask is not eligible for runner")

    if task.task_status == "blocked" and force:
        task.task_status = "running"
        task.blocking = False
        task.blocking_reason = None
        task.started_at = task.started_at or datetime.now(UTC)
        await session.commit()
        await session.refresh(task)

    agent_name = eligibility.recommended_agent or "System"
    output_type = eligibility.output_type or "generic_agent_output"
    execution = await _create_running_execution(
        session,
        task,
        agent_name=agent_name,
        correlation_id=correlation_id,
    )

    try:
        output = await _create_output_for_task(
            session,
            task,
            execution,
            agent_name=agent_name,
            output_type=output_type,
            runner=runner,
            correlation_id=correlation_id,
        )
        execution.status = "completed"
        execution.output_ref = output.id
        execution.completed_at = datetime.now(UTC)
        await session.commit()
        await session.refresh(execution)

        completed_task = await workflow_task_service.complete_workflow_task(
            session,
            task.id,
            agent_execution_id=execution.id,
            agent_output_id=output.id,
            output_ref=output.id,
            completed_with_warnings=output.human_review_required,
        )
        return AgentRunnerRunResponse(
            status="completed",
            task=WorkflowTaskRead.model_validate(completed_task),
            execution=AgentExecutionRead.model_validate(execution),
            output=AgentOutputRead.model_validate(output),
        )
    except Exception as exc:
        execution.status = "failed"
        execution.error_message = _sanitize_error(str(exc))
        execution.completed_at = datetime.now(UTC)
        await session.commit()
        await workflow_task_service.fail_workflow_task(session, task.id, execution.error_message)
        raise


async def run_next_task_for_workflow(
    session: AsyncSession,
    workflow_run_id: str,
    *,
    force: bool = False,
    runner: str = "internal",
    correlation_id: str | None = None,
) -> AgentRunnerWorkflowRunNextResponse:
    workflow_run = await session.get(WorkflowRun, workflow_run_id)
    if workflow_run is None:
        raise NotFoundError("Workflow run")

    tasks = await workflow_task_service.list_workflow_tasks(
        session,
        workflow_run_id=workflow_run_id,
        limit=200,
        offset=0,
    )
    candidates = [
        task
        for task in tasks
        if task.task_status not in TERMINAL_STATUSES
        and evaluate_task_eligibility(task, force=force).eligible
    ]
    candidates.sort(key=lambda task: (PRIORITY_ORDER.get(task.priority, 99), task.created_at))
    if not candidates:
        return AgentRunnerWorkflowRunNextResponse(
            status="no_eligible_task",
            workflow_run_id=workflow_run_id,
            message="No eligible workflow task found.",
        )

    result = await run_task(
        session,
        candidates[0].id,
        force=force,
        runner=runner,
        correlation_id=correlation_id,
    )
    return AgentRunnerWorkflowRunNextResponse(
        status="completed",
        workflow_run_id=workflow_run_id,
        result=result,
    )


async def list_recent_runs(
    session: AsyncSession,
    agent_name: str | None = None,
    status: str | None = None,
    workflow_run_id: str | None = None,
    news_item_id: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[AgentRunnerRecentRunItem]:
    stmt = select(AgentExecution).where(AgentExecution.agent_version == INTERNAL_RUNNER_VERSION)
    if agent_name is not None:
        stmt = stmt.where(AgentExecution.agent_name == agent_name)
    if status is not None:
        stmt = stmt.where(AgentExecution.status == status)
    if workflow_run_id is not None or news_item_id is not None:
        output_stmt = select(AgentOutput.agent_execution_id).where(
            AgentOutput.agent_execution_id.is_not(None)
        )
        if workflow_run_id is not None:
            output_stmt = output_stmt.where(AgentOutput.workflow_run_id == workflow_run_id)
        if news_item_id is not None:
            output_stmt = output_stmt.where(AgentOutput.news_item_id == news_item_id)
        output_result = await session.execute(output_stmt)
        execution_ids = set(output_result.scalars().all())
        if not execution_ids:
            return []
        stmt = stmt.where(AgentExecution.id.in_(execution_ids))

    result = await session.execute(
        stmt.order_by(AgentExecution.created_at.desc()).limit(limit).offset(offset)
    )
    return [_recent_run_item(execution) for execution in result.scalars().all()]


async def get_admin_agent_runner_summary(session: AsyncSession) -> AdminAgentRunnerSummary:
    total_internal_runs = await _count_internal_runs(session)
    completed_runs = await _count_internal_runs(session, status="completed")
    failed_runs = await _count_internal_runs(session, status="failed")
    pending_review = await session.execute(
        select(func.count())
        .select_from(AgentOutput)
        .where(
            AgentOutput.agent_version == INTERNAL_RUNNER_VERSION,
            AgentOutput.status == "pending_review",
        )
    )
    tasks = await workflow_task_service.list_workflow_tasks(session, limit=500, offset=0)
    eligible_count = sum(1 for task in tasks if evaluate_task_eligibility(task).eligible)
    recent_runs = await list_recent_runs(session, limit=10)
    return AdminAgentRunnerSummary(
        total_internal_runs=total_internal_runs,
        completed_runs=completed_runs,
        failed_runs=failed_runs,
        outputs_pending_review=int(pending_review.scalar_one()),
        tasks_eligible_for_runner=eligible_count,
        recent_runs=recent_runs,
    )


def evaluate_task_eligibility(
    task: WorkflowTask,
    force: bool = False,
) -> AgentRunnerTaskEligibility:
    agent_name = _resolve_agent(task, force=force)
    output_type = AGENT_OUTPUT_TYPE_MAP.get(agent_name or "")
    reason = None
    eligible = True

    if task.task_status in TERMINAL_STATUSES:
        eligible = False
        reason = f"WorkflowTask with status {task.task_status} cannot be run"
    elif task.task_status == "blocked" and not force:
        eligible = False
        reason = "WorkflowTask is blocked; use force=true to run with internal runner"
    elif task.task_status not in RUNNABLE_STATUSES and task.task_status != "blocked":
        eligible = False
        reason = f"WorkflowTask with status {task.task_status} is not runnable"
    elif agent_name is None or output_type is None:
        eligible = False
        reason = "WorkflowTask task_type or assigned_agent is not supported by internal runner"

    return AgentRunnerTaskEligibility(
        eligible=eligible,
        reason=reason,
        task_id=task.id,
        task_status=task.task_status,
        task_type=task.task_type,
        assigned_agent=task.assigned_agent,
        recommended_agent=agent_name,
        output_type=output_type,
    )


def build_agent_payload(
    task: WorkflowTask,
    *,
    agent_name: str,
    output_type: str,
) -> dict[str, Any]:
    base = {
        "agent": agent_name,
        "task_id": task.id,
        "task_type": task.task_type,
        "workflow_run_id": task.workflow_run_id,
        "news_item_id": task.news_item_id,
        "runner": "internal",
        "external_integrations": False,
    }
    recommendations = {
        "NewsScoutAgent": {
            "finding": "Internal scout placeholder generated from WorkflowTask input.",
            "signals": [],
            "requires_human_review": True,
        },
        "SourceValidatorAgent": {
            "source_status": "needs_review",
            "missing_requirements": ["VerificationRecord"],
            "recommendation": "Create or review VerificationRecord before advancing.",
        },
        "RiskAgent": {
            "risk_level": "unknown",
            "risk_flags": ["requires_human_review"],
            "recommendation": "Create RiskReview before publication decisions.",
        },
        "EditorialAgent": {
            "draft_status": "placeholder",
            "recommendation": "Create ContentPiece using verified facts only.",
        },
        "AuditAgent": {
            "audit_status": "needs_human_review",
            "recommendation": "Create AuditCheck before approval or publication.",
        },
        "MetricsAgent": {
            "metrics_status": "not_connected",
            "recommendation": "Create MetricSnapshot manually or connect analytics later.",
        },
    }
    payload = {
        **base,
        **recommendations.get(
            agent_name,
            {
                "output_type": output_type,
                "recommendation": "Review this deterministic internal runner output manually.",
            },
        ),
    }
    if task.input_payload is not None:
        payload["input_payload_summary"] = "WorkflowTask input_payload was present."
    return payload


async def _create_running_execution(
    session: AsyncSession,
    task: WorkflowTask,
    *,
    agent_name: str,
    correlation_id: str | None,
) -> AgentExecution:
    execution = AgentExecution(
        **AgentExecutionCreate(
            agent_name=agent_name,
            agent_version=INTERNAL_RUNNER_VERSION,
            input_ref=task.id,
            status="running",
            started_at=datetime.now(UTC),
            correlation_id=correlation_id or task.correlation_id,
        ).model_dump()
    )
    session.add(execution)
    await session.commit()
    await session.refresh(execution)
    return execution


async def _create_output_for_task(
    session: AsyncSession,
    task: WorkflowTask,
    execution: AgentExecution,
    *,
    agent_name: str,
    output_type: str,
    runner: str,
    correlation_id: str | None,
) -> AgentOutput:
    payload = build_agent_payload(task, agent_name=agent_name, output_type=output_type)
    risk_flags = _risk_flags_for_agent(agent_name)
    missing_requirements = _missing_requirements_for_task(task)
    output = await agent_output_service.create_agent_output(
        session,
        AgentOutputCreate(
            agent_execution_id=execution.id,
            agent_name=agent_name,
            agent_version=INTERNAL_RUNNER_VERSION,
            output_type=output_type,
            status="stored",
            entity_type="WorkflowTask",
            entity_id=task.id,
            news_item_id=task.news_item_id,
            workflow_run_id=task.workflow_run_id,
            workflow_step_id=task.workflow_step_id,
            summary=f"Internal runner output for {task.task_type} via {agent_name}.",
            payload={**payload, "runner_name": runner},
            risk_flags=risk_flags,
            missing_requirements=missing_requirements,
            next_agent=None,
            human_review_required=agent_name in HUMAN_REVIEW_AGENTS or bool(risk_flags),
            correlation_id=correlation_id or task.correlation_id,
        ),
        correlation_id=correlation_id or task.correlation_id,
    )
    return output


def _resolve_agent(task: WorkflowTask, force: bool = False) -> str | None:
    if task.assigned_agent in AGENT_OUTPUT_TYPE_MAP:
        return task.assigned_agent
    if task.assigned_agent in {"HumanEditor", "Operator"} and not force:
        return None
    if task.assigned_agent in {"HumanEditor", "Operator"} and force:
        return "System"
    if task.assigned_agent in {"None", "System"}:
        return TASK_AGENT_MAP.get(task.task_type)
    return TASK_AGENT_MAP.get(task.task_type)


def _risk_flags_for_agent(agent_name: str) -> list[str]:
    if agent_name == "RiskAgent":
        return ["requires_human_review"]
    if agent_name == "AuditAgent":
        return ["publication_without_approval"]
    return []


def _missing_requirements_for_task(task: WorkflowTask) -> list[str]:
    return {
        "source_validation": ["VerificationRecord"],
        "risk_review": ["RiskReview"],
        "editorial_draft": ["ContentPiece"],
        "audit_check": ["AuditCheck"],
        "distribution_planning": ["DistributionPlan"],
        "metrics_review": ["MetricSnapshot"],
        "memory_review": ["MemoryItem"],
        "knowledge_update": ["KnowledgeNode"],
    }.get(task.task_type, [])


def _recent_run_item(execution: AgentExecution) -> AgentRunnerRecentRunItem:
    return AgentRunnerRecentRunItem(
        id=execution.id,
        agent_name=execution.agent_name,
        agent_version=execution.agent_version,
        input_ref=execution.input_ref,
        output_ref=execution.output_ref,
        status=execution.status,
        started_at=execution.started_at,
        completed_at=execution.completed_at,
        error_message=execution.error_message,
        correlation_id=execution.correlation_id,
        created_at=execution.created_at,
    )


async def _count_internal_runs(session: AsyncSession, status: str | None = None) -> int:
    stmt = select(func.count()).select_from(AgentExecution).where(
        AgentExecution.agent_version == INTERNAL_RUNNER_VERSION
    )
    if status is not None:
        stmt = stmt.where(AgentExecution.status == status)
    result = await session.execute(stmt)
    return int(result.scalar_one())


def _sanitize_error(message: str) -> str:
    return message[:500] or "Internal agent runner failed"
