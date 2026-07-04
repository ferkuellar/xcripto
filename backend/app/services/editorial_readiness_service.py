from dataclasses import dataclass, field
from typing import Any

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (
    EDITORIAL_READINESS_WEIGHTS,
    SENSITIVE_AGENT_OUTPUT_RISK_FLAGS,
)
from app.core.editorial_gates import is_passing_audit_check
from app.core.errors import NotFoundError
from app.core.source_quality import (
    is_disqualified,
    readiness_score_for_source,
    source_level_for,
)
from app.models import (
    AgentOutput,
    AuditCheck,
    ContentPiece,
    DistributionPlan,
    EditorialReadinessScore,
    KnowledgeEdge,
    KnowledgeNode,
    MemoryItem,
    MetricSnapshot,
    NewsItem,
    PublicationRecord,
    RiskReview,
    VerificationRecord,
    WorkflowRun,
    WorkflowTask,
)
from app.services import source_service


@dataclass
class ComponentResult:
    score: float
    details: dict[str, Any] = field(default_factory=dict)
    missing: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    blocks: list[str] = field(default_factory=list)
    human_review_required: bool = False
    publication_block_recommended: bool = False


async def calculate_editorial_readiness(
    session: AsyncSession,
    news_item_id: str,
    correlation_id: str | None = None,
    calculated_by: str = "system",
) -> EditorialReadinessScore:
    # El snapshot de WorkflowRun (missing_requirements/blocking_reasons) solo se
    # actualiza al recalcular el workflow; sin esto, calculate reportaría como
    # faltantes requisitos ya cumplidos. explain() se mantiene read-only.
    workflow = await _latest_by_news(session, WorkflowRun, news_item_id)
    if workflow is not None:
        from app.services import workflow_service

        await workflow_service.recalculate_workflow_run(session, workflow.id)

    payload = await explain_editorial_readiness(session, news_item_id, calculated_by=calculated_by)
    score = EditorialReadinessScore(**payload)
    if score.correlation_id is None:
        score.correlation_id = correlation_id
    session.add(score)
    await session.commit()
    await session.refresh(score)
    return score


async def explain_editorial_readiness(
    session: AsyncSession,
    news_item_id: str,
    calculated_by: str = "system",
) -> dict[str, Any]:
    news = await session.get(NewsItem, news_item_id)
    if news is None:
        raise NotFoundError("News item")

    workflow = await _latest_by_news(session, WorkflowRun, news_item_id)
    related = {
        "source": await _source_score(session, news),
        "verification": await _verification_score(session, news_item_id),
        "risk": await _risk_score(session, news_item_id),
        "editorial": await _editorial_score(session, news_item_id),
        "audit": await _audit_score(session, news_item_id),
        "workflow": _workflow_score(workflow),
        "task": await _task_score(session, news_item_id, workflow.id if workflow else None),
        "agent_output": await _agent_output_score(
            session, news_item_id, workflow.id if workflow else None
        ),
        "distribution": await _distribution_score(session, news_item_id),
        "publication": await _publication_score(session, news_item_id),
        "metrics": await _metrics_score(session, news_item_id, workflow.id if workflow else None),
        "memory": await _memory_score(session, news_item_id, workflow.id if workflow else None),
        "knowledge": await _knowledge_score(
            session, news_item_id, workflow.id if workflow else None
        ),
    }

    blocking_reasons = _unique(
        reason for result in related.values() for reason in result.blocks
    )
    missing_requirements = _unique(
        item for result in related.values() for item in result.missing
    )
    warnings = _unique(warning for result in related.values() for warning in result.warnings)

    if news.status in {"rejected", "retracted"}:
        blocking_reasons.append(f"NewsItem status is {news.status}")
    score = round(sum(result.score for result in related.values()), 2)
    score = max(0, min(100, score))

    publication = related["publication"]
    blocked = bool(blocking_reasons)
    score_band = _score_band(score, blocked)
    readiness_status = _readiness_status(news.status, publication.details, score, blocked)
    recommended_next_action, next_agent = _recommend_next_action(
        readiness_status, blocking_reasons, missing_requirements, workflow
    )

    component_scores = {
        "source_score": related["source"].score,
        "verification_score": related["verification"].score,
        "risk_score": related["risk"].score,
        "editorial_score": related["editorial"].score,
        "audit_score": related["audit"].score,
        "workflow_score": related["workflow"].score,
        "task_score": related["task"].score,
        "agent_output_score": related["agent_output"].score,
        "distribution_score": related["distribution"].score,
        "publication_score": related["publication"].score,
        "metrics_score": related["metrics"].score,
        "memory_score": related["memory"].score,
        "knowledge_score": related["knowledge"].score,
    }

    return {
        "news_item_id": news_item_id,
        "workflow_run_id": workflow.id if workflow else None,
        "score": score,
        "score_band": score_band,
        "readiness_status": readiness_status,
        **component_scores,
        "blocking_reasons": blocking_reasons,
        "missing_requirements": missing_requirements,
        "warnings": warnings,
        "recommended_next_action": recommended_next_action,
        "next_agent": next_agent,
        "human_review_required": any(result.human_review_required for result in related.values()),
        "publication_block_recommended": any(
            result.publication_block_recommended for result in related.values()
        ),
        "score_payload": {
            "weights": EDITORIAL_READINESS_WEIGHTS,
            "components": {name: result.details for name, result in related.items()},
            "rules": [
                "Score informs readiness only.",
                "Score does not approve publication.",
                "Score does not replace AuditCheck or human review.",
            ],
        },
        "calculated_by": calculated_by,
    }


async def get_latest_readiness_score(
    session: AsyncSession, news_item_id: str
) -> EditorialReadinessScore:
    result = await session.execute(
        select(EditorialReadinessScore)
        .where(EditorialReadinessScore.news_item_id == news_item_id)
        .order_by(EditorialReadinessScore.created_at.desc())
        .limit(1)
    )
    score = result.scalar_one_or_none()
    if score is None:
        raise NotFoundError("Editorial readiness score")
    return score


async def get_readiness_score(session: AsyncSession, score_id: str) -> EditorialReadinessScore:
    score = await session.get(EditorialReadinessScore, score_id)
    if score is None:
        raise NotFoundError("Editorial readiness score")
    return score


async def list_readiness_scores(
    session: AsyncSession,
    news_item_id: str | None = None,
    workflow_run_id: str | None = None,
    score_band: str | None = None,
    readiness_status: str | None = None,
    next_agent: str | None = None,
    human_review_required: bool | None = None,
    publication_block_recommended: bool | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[EditorialReadinessScore]:
    stmt = select(EditorialReadinessScore).order_by(EditorialReadinessScore.created_at.desc())
    filters = {
        "news_item_id": news_item_id,
        "workflow_run_id": workflow_run_id,
        "score_band": score_band,
        "readiness_status": readiness_status,
        "next_agent": next_agent,
        "human_review_required": human_review_required,
        "publication_block_recommended": publication_block_recommended,
    }
    for column_name, value in filters.items():
        if value is not None:
            stmt = stmt.where(getattr(EditorialReadinessScore, column_name) == value)
    result = await session.execute(stmt.limit(limit).offset(offset))
    return list(result.scalars().all())


async def _source_score(session: AsyncSession, news: NewsItem) -> ComponentResult:
    source = await source_service.get_source_for_news_item(session, news)
    if source is None:
        if news.source_url or news.source_name:
            return ComponentResult(
                5,
                details={"signal": "news_item_source_fields", "source_level": "unrated"},
                warnings=["Source not registered as SourceReference; quality unrated"],
            )
        return ComponentResult(0, missing=["SourceReference"], details={"signal": "missing_source"})

    level = source_level_for(source)
    disqualified = is_disqualified(source)
    details = {
        "source_reference_id": source.id,
        "signal": "source_reference",
        "source_level": level,
        "trust_level": source.trust_level,
        "source_status": source.source_status,
    }
    blocks: list[str] = []
    warnings: list[str] = []
    if disqualified:
        blocks.append(
            f"Source is {source.source_status}; cannot sustain publication (SOURCE_QUALITY_POLICY)"
        )
    elif level == "S5":
        blocks.append("Source level S5 (rumor/opaque) cannot be published as fact")
    elif level == "S4":
        warnings.append("Source level S4 (unconfirmed social) requires strong verification")
    elif level == "S3":
        warnings.append("Source level S3 requires additional independent confirmation")
    return ComponentResult(
        readiness_score_for_source(source),
        details=details,
        blocks=blocks,
        warnings=warnings,
        publication_block_recommended=bool(blocks),
    )


async def _verification_score(session: AsyncSession, news_item_id: str) -> ComponentResult:
    record = await _latest_by_news(session, VerificationRecord, news_item_id)
    if record is None:
        return ComponentResult(0, missing=["VerificationRecord"])
    status_scores = {
        "verified": 20,
        "partially_verified": 10,
        "unverified": 5,
        "validating": 5,
    }
    if record.verification_status in {"contradicted", "rejected"}:
        return ComponentResult(
            0,
            blocks=[f"VerificationRecord status is {record.verification_status}"],
            details={"verification_record_id": record.id, "status": record.verification_status},
        )
    warnings = []
    human_review_required = record.human_review_required
    if record.verification_status == "rumor":
        warnings.append("VerificationRecord status is rumor")
    # Conflicto entre fuentes (doc SOURCE_QUALITY_POLICY): las contradicciones
    # exigen revisión humana antes de tratar la señal como hecho.
    if record.contradictions:
        warnings.append("VerificationRecord reports source conflicts (contradictions)")
        human_review_required = True
    return ComponentResult(
        status_scores.get(record.verification_status, 0),
        warnings=warnings,
        human_review_required=human_review_required,
        details={
            "verification_record_id": record.id,
            "status": record.verification_status,
            "contradictions": len(record.contradictions or []),
        },
    )


async def _risk_score(session: AsyncSession, news_item_id: str) -> ComponentResult:
    review = await _latest_by_news(session, RiskReview, news_item_id)
    if review is None:
        return ComponentResult(0, missing=["RiskReview"])
    blocks = []
    if review.risk_level == "critical":
        blocks.append("RiskReview risk_level is critical")
    if review.publication_block_recommended:
        blocks.append("RiskReview recommends publication block")
    if review.decision_recommendation in {"block_publication", "reject"}:
        blocks.append(f"RiskReview decision is {review.decision_recommendation}")
    if blocks:
        return ComponentResult(
            0,
            blocks=blocks,
            human_review_required=True,
            publication_block_recommended=True,
            details={"risk_review_id": review.id, "risk_level": review.risk_level},
        )
    scores = {"low": 15, "medium": 10, "high": 5}
    return ComponentResult(
        scores.get(review.risk_level, 0),
        human_review_required=review.human_review_required or review.risk_level == "high",
        warnings=["RiskReview risk_level is high"] if review.risk_level == "high" else [],
        details={"risk_review_id": review.id, "risk_level": review.risk_level},
    )


async def _editorial_score(session: AsyncSession, news_item_id: str) -> ComponentResult:
    piece = await _latest_by_news(session, ContentPiece, news_item_id)
    if piece is None:
        return ComponentResult(0, missing=["ContentPiece"])
    if piece.status in {"blocked", "rejected"}:
        return ComponentResult(
            0,
            blocks=[f"ContentPiece status is {piece.status}"],
            details={"content_piece_id": piece.id, "status": piece.status},
        )
    scores = {"drafting": 4, "reviewing": 7, "approved": 10}
    return ComponentResult(
        scores.get(piece.status, 0),
        human_review_required=piece.human_review_required,
        details={"content_piece_id": piece.id, "status": piece.status},
    )


async def _audit_score(session: AsyncSession, news_item_id: str) -> ComponentResult:
    check = await _latest_audit_check(session, news_item_id)
    if check is None:
        return ComponentResult(0, missing=["AuditCheck"])
    if check.publication_block_recommended or check.audit_status in {"failed", "blocked", "fail"}:
        return ComponentResult(
            0,
            blocks=[f"AuditCheck status is {check.audit_status}"],
            publication_block_recommended=True,
            details={"audit_check_id": check.id, "audit_status": check.audit_status},
        )
    if is_passing_audit_check(check):
        score = 8 if check.audit_status == "passed_with_warnings" else 15
    else:
        score = 0
    return ComponentResult(
        score,
        missing=[] if score else ["PassingAuditCheck"],
        warnings=(
            ["AuditCheck passed with warnings"]
            if check.audit_status == "passed_with_warnings"
            else []
        ),
        details={"audit_check_id": check.id, "audit_status": check.audit_status},
    )


def _workflow_score(workflow: WorkflowRun | None) -> ComponentResult:
    if workflow is None:
        return ComponentResult(0, missing=["WorkflowRun"])
    if workflow.status in {"blocked", "failed", "escalated"} and workflow.blocking_reasons:
        return ComponentResult(
            0,
            blocks=[
                f"WorkflowRun {workflow.status}: {reason}"
                for reason in workflow.blocking_reasons
            ],
            details={"workflow_run_id": workflow.id, "status": workflow.status},
        )
    scores = {
        "created": 2,
        "running": 2,
        "waiting_input": 2,
        "waiting_review": 3,
        "completed": 5,
    }
    if workflow.readiness_status == "ready_to_advance":
        score = 5
    else:
        score = scores.get(workflow.status, 0)
    return ComponentResult(
        score,
        missing=workflow.missing_requirements or [],
        details={
            "workflow_run_id": workflow.id,
            "status": workflow.status,
            "readiness_status": workflow.readiness_status,
        },
    )


async def _task_score(
    session: AsyncSession, news_item_id: str, workflow_run_id: str | None
) -> ComponentResult:
    stmt = select(WorkflowTask).where(WorkflowTask.news_item_id == news_item_id)
    if workflow_run_id is not None:
        stmt = stmt.where(WorkflowTask.workflow_run_id == workflow_run_id)
    tasks = list((await session.execute(stmt)).scalars().all())
    if not tasks:
        return ComponentResult(0, missing=["WorkflowTask"])
    blocked = [
        task for task in tasks if task.blocking and task.task_status in {"blocked", "failed"}
    ]
    if blocked:
        return ComponentResult(
            0,
            blocks=[
                task.blocking_reason or f"WorkflowTask {task.id} is blocking"
                for task in blocked
            ],
            details={"task_count": len(tasks), "blocking_task_count": len(blocked)},
        )
    completed = [
        task for task in tasks if task.task_status in {"completed", "completed_with_warnings"}
    ]
    if len(completed) == len(tasks):
        score = 5
    elif len(completed) >= max(1, len(tasks) // 2):
        score = 3
    else:
        score = 2
    return ComponentResult(
        score,
        details={"task_count": len(tasks), "completed_count": len(completed)},
    )


async def _agent_output_score(
    session: AsyncSession, news_item_id: str, workflow_run_id: str | None
) -> ComponentResult:
    stmt = select(AgentOutput).where(AgentOutput.news_item_id == news_item_id)
    if workflow_run_id is not None:
        stmt = stmt.where(
            (AgentOutput.workflow_run_id == workflow_run_id)
            | (AgentOutput.workflow_run_id.is_(None))
        )
    outputs = list((await session.execute(stmt)).scalars().all())
    if not outputs:
        return ComponentResult(0, missing=["AgentOutput"])
    critical = [
        output
        for output in outputs
        if set(output.risk_flags or []) & SENSITIVE_AGENT_OUTPUT_RISK_FLAGS
        and output.human_review_required
        and not output.accepted
    ]
    if critical:
        return ComponentResult(
            0,
            blocks=["AgentOutput has critical unaccepted risk flags"],
            human_review_required=True,
            details={"agent_output_count": len(outputs), "critical_pending_count": len(critical)},
        )
    pending_review = [output for output in outputs if output.status == "pending_review"]
    accepted = [output for output in outputs if output.status == "accepted"]
    if accepted:
        score = 5
    elif pending_review:
        score = 2
    else:
        score = 3
    return ComponentResult(
        score,
        warnings=["AgentOutput pending human review"] if pending_review else [],
        human_review_required=bool(pending_review),
        details={"agent_output_count": len(outputs), "accepted_count": len(accepted)},
    )


async def _distribution_score(session: AsyncSession, news_item_id: str) -> ComponentResult:
    plan = await _latest_by_news(session, DistributionPlan, news_item_id)
    if plan is None:
        return ComponentResult(0, missing=["DistributionPlan"])
    if plan.status in {"blocked", "rejected"}:
        return ComponentResult(
            0,
            blocks=[f"DistributionPlan status is {plan.status}"],
            details={"distribution_plan_id": plan.id, "status": plan.status},
        )
    scores = {"proposed": 2, "ready_for_review": 4, "scheduled": 5, "distributed": 5}
    score = scores.get(plan.status, 2 if plan.status.startswith("needs_") else 0)
    return ComponentResult(score, details={"distribution_plan_id": plan.id, "status": plan.status})


async def _publication_score(session: AsyncSession, news_item_id: str) -> ComponentResult:
    record = await _latest_by_news(session, PublicationRecord, news_item_id)
    if record is None:
        return ComponentResult(0, missing=["PublicationRecord"])
    if record.publication_status in {"retracted", "failed"}:
        return ComponentResult(
            0,
            blocks=[f"PublicationRecord status is {record.publication_status}"],
            details={"publication_record_id": record.id, "status": record.publication_status},
        )
    scores = {"scheduled": 3, "published": 5}
    return ComponentResult(
        scores.get(record.publication_status, 0),
        details={"publication_record_id": record.id, "status": record.publication_status},
    )


async def _metrics_score(
    session: AsyncSession, news_item_id: str, workflow_run_id: str | None
) -> ComponentResult:
    stmt = select(MetricSnapshot).where(MetricSnapshot.news_item_id == news_item_id)
    if workflow_run_id is not None:
        stmt = stmt.where(
            (MetricSnapshot.workflow_run_id == workflow_run_id)
            | (MetricSnapshot.workflow_run_id.is_(None))
        )
    snapshots = list((await session.execute(stmt)).scalars().all())
    if not snapshots:
        return ComponentResult(0, missing=["MetricSnapshot"])
    best_quality = {snapshot.data_quality for snapshot in snapshots}
    score = 2 if best_quality & {"medium", "high"} else 1
    return ComponentResult(score, details={"metric_snapshot_count": len(snapshots)})


async def _memory_score(
    session: AsyncSession, news_item_id: str, workflow_run_id: str | None
) -> ComponentResult:
    stmt = select(MemoryItem).where(MemoryItem.news_item_id == news_item_id)
    if workflow_run_id is not None:
        stmt = stmt.where(
            (MemoryItem.workflow_run_id == workflow_run_id)
            | (MemoryItem.workflow_run_id.is_(None))
        )
    memories = list((await session.execute(stmt)).scalars().all())
    if not memories:
        return ComponentResult(0, missing=["MemoryItem"])
    approved = [memory for memory in memories if memory.memory_status == "approved"]
    risky = [memory for memory in memories if memory.risk_flags]
    score = 2 if approved else 1
    return ComponentResult(
        score,
        warnings=["MemoryItem has risk flags"] if risky else [],
        human_review_required=any(memory.human_review_required for memory in memories),
        details={"memory_item_count": len(memories), "approved_count": len(approved)},
    )


async def _knowledge_score(
    session: AsyncSession, news_item_id: str, workflow_run_id: str | None
) -> ComponentResult:
    entity_refs = [("news_item", news_item_id), ("NewsItem", news_item_id)]
    if workflow_run_id is not None:
        entity_refs.extend([("workflow_run", workflow_run_id), ("WorkflowRun", workflow_run_id)])
    clauses = [
        (KnowledgeNode.entity_type == entity_type) & (KnowledgeNode.entity_id == entity_id)
        for entity_type, entity_id in entity_refs
    ]
    nodes = list(
        (await session.execute(select(KnowledgeNode).where(or_(*clauses)))).scalars().all()
    )
    if not nodes:
        return ComponentResult(0, missing=["KnowledgeNode"])
    node_ids = [node.id for node in nodes]
    edges = list(
        (
            await session.execute(
                select(KnowledgeEdge).where(
                    (KnowledgeEdge.source_node_id.in_(node_ids))
                    | (KnowledgeEdge.target_node_id.in_(node_ids))
                )
            )
        )
        .scalars()
        .all()
    )
    warning_edges = [
        edge for edge in edges if edge.status in {"contradictory", "low_confidence", "needs_audit"}
    ]
    return ComponentResult(
        1,
        warnings=["KnowledgeEdge requires review"] if warning_edges else [],
        details={"knowledge_node_count": len(nodes), "knowledge_edge_count": len(edges)},
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


def _score_band(score: float, blocked: bool) -> str:
    if blocked:
        return "blocked"
    if score < 20:
        return "very_low"
    if score < 40:
        return "low"
    if score < 70:
        return "medium"
    if score < 90:
        return "high"
    return "ready"


def _readiness_status(
    news_status: str,
    publication_details: dict[str, Any],
    score: float,
    blocked: bool,
) -> str:
    if news_status == "archived" or publication_details.get("status") == "archived":
        return "archived"
    if publication_details.get("status") == "published":
        return "published"
    if blocked:
        return "blocked"
    if score < 40:
        return "not_ready"
    if score < 70:
        return "partially_ready"
    if score < 90:
        return "ready_for_review"
    return "ready_to_advance"


def _recommend_next_action(
    readiness_status: str,
    blocking_reasons: list[str],
    missing_requirements: list[str],
    workflow: WorkflowRun | None,
) -> tuple[str | None, str]:
    if blocking_reasons:
        return "Resolve critical blockers before advancing.", "HumanEditor"
    if workflow is not None and workflow.recommended_next_action:
        return workflow.recommended_next_action, workflow.next_agent
    if missing_requirements:
        requirement = missing_requirements[0]
        agents = {
            "VerificationRecord": "SourceValidatorAgent",
            "RiskReview": "RiskAgent",
            "ContentPiece": "EditorialAgent",
            "AuditCheck": "AuditAgent",
            "PassingAuditCheck": "AuditAgent",
            "DistributionPlan": "DistributionAgent",
            "PublicationRecord": "CalendarAgent",
            "MetricSnapshot": "MetricsAgent",
            "MemoryItem": "MemoryAgent",
            "KnowledgeNode": "KnowledgeAgent",
        }
        return f"Create or update {requirement} before advancing.", agents.get(requirement, "None")
    if readiness_status == "published":
        return "Review metrics, memory and knowledge after publication.", "MetricsAgent"
    return "Editorial readiness is sufficient for review.", "HumanEditor"


def _unique(values) -> list[str]:
    result: list[str] = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return result
