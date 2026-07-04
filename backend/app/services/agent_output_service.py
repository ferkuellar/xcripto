from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import SENSITIVE_AGENT_OUTPUT_RISK_FLAGS
from app.core.errors import ConflictError, DomainValidationError, NotFoundError
from app.models import AgentExecution, AgentOutput, NewsItem, WorkflowRun, WorkflowStep
from app.schemas.agent_output import AgentOutputCreate

NON_ACCEPTABLE_OUTPUT_STATUSES = {"rejected", "superseded", "blocked", "failed"}
REJECTABLE_OUTPUT_STATUSES = {"created", "stored", "pending_review", "accepted"}


async def create_agent_output(
    session: AsyncSession,
    payload: AgentOutputCreate,
    correlation_id: str | None = None,
) -> AgentOutput:
    await _validate_minimum_relation(payload)
    await _validate_related_entities(session, payload)

    data = payload.model_dump()
    risk_flags = set(data["risk_flags"])
    if risk_flags & SENSITIVE_AGENT_OUTPUT_RISK_FLAGS:
        data["human_review_required"] = True

    if data["accepted"]:
        data["status"] = "accepted"
        data["accepted_at"] = data["accepted_at"] or datetime.now(UTC)
    elif data["human_review_required"] and data["status"] in {"created", "stored"}:
        data["status"] = "pending_review"

    output = AgentOutput(**data)
    if output.correlation_id is None:
        output.correlation_id = correlation_id
    session.add(output)
    await session.commit()
    await session.refresh(output)
    return output


async def list_agent_outputs(
    session: AsyncSession,
    agent_name: str | None = None,
    output_type: str | None = None,
    status: str | None = None,
    entity_type: str | None = None,
    entity_id: str | None = None,
    news_item_id: str | None = None,
    workflow_run_id: str | None = None,
    agent_execution_id: str | None = None,
    human_review_required: bool | None = None,
    accepted: bool | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[AgentOutput]:
    stmt = select(AgentOutput).order_by(AgentOutput.created_at.desc())
    if agent_name is not None:
        stmt = stmt.where(AgentOutput.agent_name == agent_name)
    if output_type is not None:
        stmt = stmt.where(AgentOutput.output_type == output_type)
    if status is not None:
        stmt = stmt.where(AgentOutput.status == status)
    if entity_type is not None:
        stmt = stmt.where(AgentOutput.entity_type == entity_type)
    if entity_id is not None:
        stmt = stmt.where(AgentOutput.entity_id == entity_id)
    if news_item_id is not None:
        stmt = stmt.where(AgentOutput.news_item_id == news_item_id)
    if workflow_run_id is not None:
        stmt = stmt.where(AgentOutput.workflow_run_id == workflow_run_id)
    if agent_execution_id is not None:
        stmt = stmt.where(AgentOutput.agent_execution_id == agent_execution_id)
    if human_review_required is not None:
        stmt = stmt.where(AgentOutput.human_review_required == human_review_required)
    if accepted is not None:
        stmt = stmt.where(AgentOutput.accepted == accepted)

    result = await session.execute(stmt.limit(limit).offset(offset))
    return list(result.scalars().all())


async def get_agent_output(session: AsyncSession, agent_output_id: str) -> AgentOutput:
    output = await session.get(AgentOutput, agent_output_id)
    if output is None:
        raise NotFoundError("Agent output")
    return output


async def accept_agent_output(
    session: AsyncSession,
    agent_output_id: str,
    accepted_by: str,
) -> AgentOutput:
    output = await get_agent_output(session, agent_output_id)
    if output.status in NON_ACCEPTABLE_OUTPUT_STATUSES:
        raise ConflictError(f"AgentOutput with status {output.status} cannot be accepted")

    output.status = "accepted"
    output.accepted = True
    output.accepted_by = accepted_by
    output.accepted_at = datetime.now(UTC)
    output.rejected_reason = None
    await session.commit()
    await session.refresh(output)
    return output


async def reject_agent_output(
    session: AsyncSession,
    agent_output_id: str,
    rejected_reason: str,
) -> AgentOutput:
    output = await get_agent_output(session, agent_output_id)
    if output.status not in REJECTABLE_OUTPUT_STATUSES:
        raise ConflictError(f"AgentOutput with status {output.status} cannot be rejected")

    output.status = "rejected"
    output.accepted = False
    output.rejected_reason = rejected_reason
    await session.commit()
    await session.refresh(output)
    return output


async def supersede_agent_output(
    session: AsyncSession,
    agent_output_id: str,
    superseded_by_output_id: str,
) -> AgentOutput:
    output = await get_agent_output(session, agent_output_id)
    if output.id == superseded_by_output_id:
        raise DomainValidationError("AgentOutput cannot supersede itself")

    replacement = await session.get(AgentOutput, superseded_by_output_id)
    if replacement is None:
        raise NotFoundError("Superseding agent output")

    output.status = "superseded"
    output.accepted = False
    output.superseded_by_output_id = superseded_by_output_id
    await session.commit()
    await session.refresh(output)
    return output


async def _validate_minimum_relation(payload: AgentOutputCreate) -> None:
    has_entity_reference = bool(payload.entity_type and payload.entity_id)
    has_operational_reference = any(
        [
            payload.agent_execution_id,
            payload.news_item_id,
            payload.workflow_run_id,
            has_entity_reference,
        ]
    )
    if not has_operational_reference:
        raise DomainValidationError(
            "AgentOutput requires agent_execution_id, news_item_id, workflow_run_id, "
            "or entity_type plus entity_id"
        )
    if (payload.entity_type and not payload.entity_id) or (
        payload.entity_id and not payload.entity_type
    ):
        raise DomainValidationError("entity_type and entity_id must be provided together")


async def _validate_related_entities(session: AsyncSession, payload: AgentOutputCreate) -> None:
    if payload.news_item_id and await session.get(NewsItem, payload.news_item_id) is None:
        raise NotFoundError("News item")
    if payload.workflow_run_id and await session.get(WorkflowRun, payload.workflow_run_id) is None:
        raise NotFoundError("Workflow run")
    if (
        payload.workflow_step_id
        and await session.get(WorkflowStep, payload.workflow_step_id) is None
    ):
        raise NotFoundError("Workflow step")
    if (
        payload.agent_execution_id
        and await session.get(AgentExecution, payload.agent_execution_id) is None
    ):
        raise NotFoundError("Agent execution")
