from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.editorial_gates import is_passing_audit_check
from app.core.errors import ConflictError, NotFoundError
from app.models import (
    AuditCheck,
    ContentPiece,
    DistributionPlan,
    NewsItem,
    PublicationRecord,
    RiskReview,
    VerificationRecord,
    WorkflowRun,
    WorkflowStep,
)

WORKFLOW_STEP_ORDER = [
    "intake",
    "verification",
    "risk_review",
    "content_creation",
    "audit_review",
    "distribution_planning",
    "publication",
    "measurement",
    "memory_review",
    "knowledge_update",
    "completed",
]

STEP_REQUIREMENTS = {
    "intake": "NewsItem",
    "verification": "VerificationRecord",
    "risk_review": "RiskReview",
    "content_creation": "ContentPiece",
    "audit_review": "AuditCheck",
    "distribution_planning": "DistributionPlan",
    "publication": "PublicationRecord",
    "measurement": "MetricSnapshot",
    "memory_review": "MemoryReview",
    "knowledge_update": "KnowledgeGraphUpdate",
}

STEP_NEXT_AGENTS = {
    "intake": "NewsScoutAgent",
    "verification": "SourceValidatorAgent",
    "risk_review": "RiskAgent",
    "content_creation": "EditorialAgent",
    "audit_review": "AuditAgent",
    "distribution_planning": "DistributionAgent",
    "publication": "CalendarAgent",
    "measurement": "MetricsAgent",
    "memory_review": "MemoryAgent",
    "knowledge_update": "KnowledgeAgent",
    "completed": "None",
}

STEP_ACTIONS = {
    "verification": "Create VerificationRecord before content production.",
    "risk_review": "Create RiskReview before editorial production advances.",
    "content_creation": "Create ContentPiece from verified and risk-reviewed news.",
    "audit_review": "Create passing AuditCheck before distribution planning.",
    "distribution_planning": "Create DistributionPlan before publication.",
    "publication": "Create PublicationRecord once distribution is scheduled.",
    "measurement": "Create MetricSnapshot after publication.",
    "memory_review": "Review publication learnings for editorial memory.",
    "knowledge_update": "Update knowledge graph after memory review.",
    "completed": "Workflow completed.",
}


@dataclass
class WorkflowAssessment:
    current_step: str
    status: str
    readiness_status: str
    blocked: bool
    blocking_reasons: list[str]
    missing_requirements: list[str]
    recommended_next_action: str | None
    next_agent: str
    completed_at: datetime | None
    completed_steps: dict[str, tuple[str | None, str | None]]


async def create_workflow_run(
    session: AsyncSession,
    news_item_id: str,
    workflow_type: str = "editorial_pipeline",
    correlation_id: str | None = None,
) -> WorkflowRun:
    if await session.get(NewsItem, news_item_id) is None:
        raise NotFoundError("News item")

    run = WorkflowRun(
        news_item_id=news_item_id,
        workflow_type=workflow_type,
        status="created",
        current_step="intake",
        readiness_status="not_ready",
        correlation_id=correlation_id,
    )
    session.add(run)
    await session.flush()

    for step_name in WORKFLOW_STEP_ORDER:
        session.add(
            WorkflowStep(
                workflow_run_id=run.id,
                step_name=step_name,
                step_status="pending",
                required=step_name != "completed",
                correlation_id=correlation_id,
            )
        )

    await session.commit()
    await recalculate_workflow_run(session, run.id)
    return await get_workflow_run(session, run.id)


async def list_workflow_runs(
    session: AsyncSession,
    news_item_id: str | None = None,
    status: str | None = None,
    workflow_type: str | None = None,
    current_step: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[WorkflowRun]:
    stmt = select(WorkflowRun).order_by(WorkflowRun.created_at.desc())
    if news_item_id is not None:
        stmt = stmt.where(WorkflowRun.news_item_id == news_item_id)
    if status is not None:
        stmt = stmt.where(WorkflowRun.status == status)
    if workflow_type is not None:
        stmt = stmt.where(WorkflowRun.workflow_type == workflow_type)
    if current_step is not None:
        stmt = stmt.where(WorkflowRun.current_step == current_step)
    result = await session.execute(stmt.limit(limit).offset(offset))
    return list(result.scalars().all())


async def get_workflow_run(session: AsyncSession, workflow_run_id: str) -> WorkflowRun:
    run = await session.get(WorkflowRun, workflow_run_id)
    if run is None:
        raise NotFoundError("Workflow run")
    return run


async def get_workflow_steps(session: AsyncSession, workflow_run_id: str) -> list[WorkflowStep]:
    result = await session.execute(
        select(WorkflowStep).where(WorkflowStep.workflow_run_id == workflow_run_id)
    )
    steps = list(result.scalars().all())
    return sorted(steps, key=lambda step: WORKFLOW_STEP_ORDER.index(step.step_name))


async def get_latest_workflow_for_news(session: AsyncSession, news_item_id: str) -> WorkflowRun:
    result = await session.execute(
        select(WorkflowRun)
        .where(WorkflowRun.news_item_id == news_item_id)
        .order_by(WorkflowRun.created_at.desc())
        .limit(1)
    )
    run = result.scalar_one_or_none()
    if run is None:
        raise NotFoundError("Workflow run")
    return run


async def recalculate_workflow_run(session: AsyncSession, workflow_run_id: str) -> WorkflowRun:
    run = await get_workflow_run(session, workflow_run_id)
    assessment = await assess_workflow(session, run.news_item_id)
    _apply_assessment(run, assessment)
    await _sync_workflow_steps(session, run, assessment)
    await session.commit()
    await session.refresh(run)
    return run


async def advance_workflow_run(session: AsyncSession, workflow_run_id: str) -> WorkflowRun:
    run = await recalculate_workflow_run(session, workflow_run_id)
    if run.blocked:
        raise ConflictError("Workflow cannot advance while blocked")
    if run.missing_requirements:
        raise ConflictError("Workflow cannot advance while critical requirements are missing")

    if run.current_step in {"completed", "measurement", "memory_review", "knowledge_update"}:
        return run

    next_step = _next_step_after(run.current_step)
    if next_step is not None:
        run.current_step = next_step
        run.status = "running"
    await session.commit()
    await session.refresh(run)
    return await recalculate_workflow_run(session, run.id)


async def assess_workflow(session: AsyncSession, news_item_id: str) -> WorkflowAssessment:
    if await session.get(NewsItem, news_item_id) is None:
        return _blocked_assessment("intake", ["NewsItem does not exist"], ["NewsItem"])

    verification = await _latest_by_news(session, VerificationRecord, news_item_id)
    risk_review = await _latest_by_news(session, RiskReview, news_item_id)
    content_piece = await _latest_by_news(session, ContentPiece, news_item_id)
    audit_check = await _latest_audit_check(session, news_item_id)
    distribution_plan = await _latest_by_news(session, DistributionPlan, news_item_id)
    publication_record = await _latest_by_news(session, PublicationRecord, news_item_id)

    completed_steps: dict[str, tuple[str | None, str | None]] = {
        "intake": ("news_item", news_item_id)
    }
    blocking_reasons: list[str] = []

    if verification is None:
        return _missing_assessment(
            "verification",
            "not_ready",
            ["VerificationRecord"],
            completed_steps,
        )
    if verification.verification_status in {"contradicted", "rejected"}:
        return _blocked_assessment(
            "verification",
            [f"VerificationRecord status is {verification.verification_status}"],
            [],
            completed_steps,
        )
    if verification.verification_status == "rumor":
        return _blocked_assessment(
            "verification",
            ["VerificationRecord status is rumor"],
            [],
            completed_steps,
            status="waiting_review",
        )
    if verification.verification_status not in {"verified", "partially_verified"}:
        return _missing_assessment(
            "verification",
            "not_ready",
            ["VerificationRecord"],
            completed_steps,
        )
    completed_steps["verification"] = ("verification_record", verification.id)

    if risk_review is None:
        return _missing_assessment(
            "risk_review",
            "not_ready",
            ["RiskReview"],
            completed_steps,
        )
    if risk_review.publication_block_recommended:
        blocking_reasons.append("RiskReview recommends publication block")
    if risk_review.decision_recommendation in {"block_publication", "reject"}:
        blocking_reasons.append(
            f"RiskReview decision is {risk_review.decision_recommendation}"
        )
    if risk_review.risk_level == "critical":
        blocking_reasons.append("RiskReview risk_level is critical")
    if blocking_reasons:
        return _blocked_assessment("risk_review", blocking_reasons, [], completed_steps)
    completed_steps["risk_review"] = ("risk_review", risk_review.id)

    if content_piece is None:
        return _missing_assessment(
            "content_creation",
            "partially_ready",
            ["ContentPiece"],
            completed_steps,
        )
    if content_piece.status in {"blocked", "rejected"}:
        return _blocked_assessment(
            "content_creation",
            [f"ContentPiece status is {content_piece.status}"],
            [],
            completed_steps,
        )
    completed_steps["content_creation"] = ("content_piece", content_piece.id)

    if audit_check is None or not is_passing_audit_check(audit_check):
        if audit_check is not None and audit_check.publication_block_recommended:
            return _blocked_assessment(
                "audit_review",
                ["AuditCheck recommends publication block"],
                [],
                completed_steps,
            )
        return _missing_assessment(
            "audit_review",
            "ready_for_review",
            ["AuditCheck"],
            completed_steps,
        )
    completed_steps["audit_review"] = ("audit_check", audit_check.id)

    if distribution_plan is None:
        return _missing_assessment(
            "distribution_planning",
            "ready_to_advance",
            ["DistributionPlan"],
            completed_steps,
        )
    if distribution_plan.status in {"blocked", "rejected"}:
        return _blocked_assessment(
            "distribution_planning",
            [f"DistributionPlan status is {distribution_plan.status}"],
            [],
            completed_steps,
        )
    completed_steps["distribution_planning"] = ("distribution_plan", distribution_plan.id)

    if publication_record is None:
        return _missing_assessment(
            "publication",
            "ready_to_advance",
            ["PublicationRecord"],
            completed_steps,
        )
    if publication_record.publication_status == "retracted":
        return _blocked_assessment(
            "publication",
            ["PublicationRecord status is retracted"],
            [],
            completed_steps,
        )
    completed_steps["publication"] = ("publication_record", publication_record.id)

    if publication_record.publication_status == "published":
        return WorkflowAssessment(
            current_step="measurement",
            status="completed",
            readiness_status="completed",
            blocked=False,
            blocking_reasons=[],
            missing_requirements=["MetricSnapshot"],
            recommended_next_action=STEP_ACTIONS["measurement"],
            next_agent="MetricsAgent",
            completed_at=datetime.now(UTC),
            completed_steps=completed_steps,
        )

    return WorkflowAssessment(
        current_step="publication",
        status="running",
        readiness_status="ready_to_advance",
        blocked=False,
        blocking_reasons=[],
        missing_requirements=[],
        recommended_next_action="Publish or mark PublicationRecord as published.",
        next_agent="CalendarAgent",
        completed_at=None,
        completed_steps=completed_steps,
    )


async def _latest_by_news(session: AsyncSession, model, news_item_id: str):
    result = await session.execute(
        select(model)
        .where(model.news_item_id == news_item_id)
        .order_by(model.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def _latest_audit_check(session: AsyncSession, news_item_id: str) -> AuditCheck | None:
    result = await session.execute(
        select(AuditCheck)
        .where(
            AuditCheck.entity_type.in_({"news_item", "NewsItem"}),
            AuditCheck.entity_id == news_item_id,
        )
        .order_by(AuditCheck.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


def _missing_assessment(
    step: str,
    readiness_status: str,
    missing_requirements: list[str],
    completed_steps: dict[str, tuple[str | None, str | None]] | None = None,
) -> WorkflowAssessment:
    return WorkflowAssessment(
        current_step=step,
        status="waiting_input",
        readiness_status=readiness_status,
        blocked=False,
        blocking_reasons=[],
        missing_requirements=missing_requirements,
        recommended_next_action=STEP_ACTIONS.get(step),
        next_agent=STEP_NEXT_AGENTS.get(step, "None"),
        completed_at=None,
        completed_steps=completed_steps or {},
    )


def _blocked_assessment(
    step: str,
    blocking_reasons: list[str],
    missing_requirements: list[str],
    completed_steps: dict[str, tuple[str | None, str | None]] | None = None,
    status: str = "blocked",
) -> WorkflowAssessment:
    return WorkflowAssessment(
        current_step=step,
        status=status,
        readiness_status="blocked",
        blocked=True,
        blocking_reasons=blocking_reasons,
        missing_requirements=missing_requirements,
        recommended_next_action="Resolve blocking editorial review before advancing.",
        next_agent=STEP_NEXT_AGENTS.get(step, "None"),
        completed_at=None,
        completed_steps=completed_steps or {},
    )


def _apply_assessment(run: WorkflowRun, assessment: WorkflowAssessment) -> None:
    run.current_step = assessment.current_step
    run.status = assessment.status
    run.readiness_status = assessment.readiness_status
    run.blocked = assessment.blocked
    run.blocking_reasons = assessment.blocking_reasons
    run.missing_requirements = assessment.missing_requirements
    run.recommended_next_action = assessment.recommended_next_action
    run.next_agent = assessment.next_agent
    run.completed_at = assessment.completed_at


async def _sync_workflow_steps(
    session: AsyncSession,
    run: WorkflowRun,
    assessment: WorkflowAssessment,
) -> None:
    steps = await get_workflow_steps(session, run.id)
    current_index = WORKFLOW_STEP_ORDER.index(assessment.current_step)
    for step in steps:
        if step.step_name in assessment.completed_steps:
            entity_type, entity_id = assessment.completed_steps[step.step_name]
            step.step_status = "completed"
            step.completed = True
            step.blocking = False
            step.blocking_reason = None
            step.entity_type = entity_type
            step.entity_id = entity_id
            if step.completed_at is None:
                step.completed_at = datetime.now(UTC)
        elif step.step_name == assessment.current_step:
            step.step_status = "blocked" if assessment.blocked else "waiting_dependency"
            step.completed = False
            step.blocking = assessment.blocked
            step.blocking_reason = "; ".join(assessment.blocking_reasons) or None
        elif WORKFLOW_STEP_ORDER.index(step.step_name) < current_index:
            step.step_status = "skipped"
            step.completed = False
            step.blocking = False
        else:
            step.step_status = "pending"
            step.completed = False
            step.blocking = False
            step.blocking_reason = None


def _next_step_after(step: str) -> str | None:
    index = WORKFLOW_STEP_ORDER.index(step)
    if index + 1 >= len(WORKFLOW_STEP_ORDER):
        return None
    return WORKFLOW_STEP_ORDER[index + 1]
