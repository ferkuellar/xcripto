from collections import Counter

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.models import (
    AgentOutput,
    AuditCheck,
    ContentPiece,
    DistributionPlan,
    EditorialReadinessScore,
    IntakeSignal,
    MemoryItem,
    MetricSnapshot,
    NewsItem,
    OwnershipAssignment,
    PublicationRecord,
    RiskReview,
    UserAccount,
    VerificationRecord,
    WorkflowRun,
    WorkflowTask,
)
from app.schemas.admin_dashboard import (
    BlockerItem,
    DashboardOverview,
    EditorialWorkQueueItem,
    IntakeQueueItem,
    NewsroomHealth,
    OperationalGap,
    OwnershipBoard,
    OwnershipUserSummary,
    PublicationBoardItem,
    ReadinessBoardItem,
    TaskBoardItem,
    UserWorkload,
)

PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "P4": 4}


async def get_dashboard_overview(session: AsyncSession) -> DashboardOverview:
    latest_scores = await _latest_readiness_scores(session)
    return DashboardOverview(
        total_news=await _count(session, NewsItem),
        total_intake_signals=await _count(session, IntakeSignal),
        pending_intake_signals=await _count_where(
            session, IntakeSignal, IntakeSignal.signal_status.in_({"received", "dedupe_pending"})
        ),
        duplicate_intake_signals=await _count_where(
            session,
            IntakeSignal,
            IntakeSignal.signal_status.in_({"duplicate", "probable_duplicate"}),
        ),
        promoted_intake_signals=await _count_where(
            session, IntakeSignal, IntakeSignal.signal_status == "promoted"
        ),
        active_workflows=await _count_where(
            session, WorkflowRun, WorkflowRun.status.in_({"created", "running", "waiting_input"})
        ),
        blocked_workflows=await _count_where(session, WorkflowRun, WorkflowRun.blocked.is_(True)),
        pending_tasks=await _count_where(
            session,
            WorkflowTask,
            WorkflowTask.task_status.in_({"queued", "assigned", "waiting_input", "waiting_review"}),
        ),
        blocked_tasks=await _count_where(
            session,
            WorkflowTask,
            (WorkflowTask.blocking.is_(True)) | (WorkflowTask.task_status == "blocked"),
        ),
        completed_tasks=await _count_where(
            session,
            WorkflowTask,
            WorkflowTask.task_status.in_({"completed", "completed_with_warnings"}),
        ),
        latest_readiness_count=len(latest_scores),
        ready_to_advance_count=sum(
            1 for score in latest_scores if score.readiness_status == "ready_to_advance"
        ),
        blocked_readiness_count=sum(
            1 for score in latest_scores if score.readiness_status == "blocked"
        ),
        published_records_count=await _count_where(
            session, PublicationRecord, PublicationRecord.publication_status == "published"
        ),
        scheduled_publications_count=await _count_where(
            session, PublicationRecord, PublicationRecord.publication_status == "scheduled"
        ),
        pending_agent_reviews_count=await _count_where(
            session,
            AgentOutput,
            (AgentOutput.status == "pending_review")
            | (AgentOutput.human_review_required.is_(True)),
        ),
        active_users_count=await _count_where(
            session, UserAccount, UserAccount.is_active.is_(True)
        ),
        unassigned_news_count=len(await _unassigned_news_ids(session)),
        unassigned_tasks_count=await _count_where(
            session, WorkflowTask, WorkflowTask.assigned_to.is_(None)
        ),
    )


async def get_newsroom_health(session: AsyncSession) -> NewsroomHealth:
    task_blockers = await _count_where(
        session,
        WorkflowTask,
        (WorkflowTask.blocking.is_(True)) | (WorkflowTask.task_status == "blocked"),
    )
    readiness_blockers = sum(
        1
        for score in await _latest_readiness_scores(session)
        if score.readiness_status == "blocked"
    )
    retracted = await _count_where(
        session, PublicationRecord, PublicationRecord.publication_status == "retracted"
    )
    critical_risks = await _count_where(session, RiskReview, RiskReview.risk_level == "critical")
    blocking_audits = await _count_where(
        session,
        AuditCheck,
        (AuditCheck.publication_block_recommended.is_(True))
        | (AuditCheck.audit_status.in_({"failed", "blocked"})),
    )
    critical_count = retracted + critical_risks + blocking_audits
    degraded_count = task_blockers + readiness_blockers
    if critical_count:
        status = "critical"
        score = 35
    elif degraded_count:
        status = "degraded"
        score = 70
    else:
        status = "healthy"
        score = 95
    return NewsroomHealth(
        health_status=status,
        health_score=score,
        critical_blockers=_labels(
            [
                ("retracted_publications", retracted),
                ("critical_risk_reviews", critical_risks),
                ("blocking_audit_checks", blocking_audits),
            ]
        ),
        warnings=_labels(
            [
                ("blocked_tasks", task_blockers),
                ("blocked_readiness_scores", readiness_blockers),
            ]
        ),
        recommended_actions=_recommended_actions(status),
        counts_by_news_status=await _counts_by(session, NewsItem.status),
        counts_by_workflow_status=await _counts_by(session, WorkflowRun.status),
        counts_by_task_status=await _counts_by(session, WorkflowTask.task_status),
        counts_by_readiness_status=Counter(
            score.readiness_status for score in await _latest_readiness_scores(session)
        ),
    )


async def get_intake_queue(
    session: AsyncSession,
    signal_status: str | None = None,
    dedupe_status: str | None = None,
    priority: str | None = None,
    topic: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[IntakeQueueItem]:
    stmt = select(IntakeSignal)
    filters = {
        "signal_status": signal_status,
        "dedupe_status": dedupe_status,
        "priority": priority,
        "topic": topic,
    }
    for column_name, value in filters.items():
        if value is not None:
            stmt = stmt.where(getattr(IntakeSignal, column_name) == value)
    result = await session.execute(stmt)
    signals = sorted(
        result.scalars().all(),
        key=lambda signal: (PRIORITY_ORDER.get(signal.priority, 9), signal.created_at),
        reverse=False,
    )
    signals = list(reversed(signals[offset : offset + limit]))
    return [
        IntakeQueueItem(
            signal_id=signal.id,
            raw_title=signal.raw_title,
            normalized_title=signal.normalized_title,
            source_name=signal.source_name,
            source_url=signal.source_url,
            signal_status=signal.signal_status,
            dedupe_status=signal.dedupe_status,
            priority=signal.priority,
            confidence_level=signal.confidence_level,
            duplicate_of_signal_id=signal.duplicate_of_signal_id,
            promoted_news_item_id=signal.promoted_news_item_id,
            created_at=signal.created_at,
        )
        for signal in signals
    ]


async def get_editorial_work_queue(session: AsyncSession) -> list[EditorialWorkQueueItem]:
    news_items = list((await session.execute(select(NewsItem))).scalars().all())
    latest_scores = {score.news_item_id: score for score in await _latest_readiness_scores(session)}
    latest_workflows = await _latest_workflows_by_news(session)
    owner_map = await _owners_by_entity(session, "NewsItem")
    items: list[EditorialWorkQueueItem] = []
    for news in news_items:
        missing = await _missing_requirements_for_news(session, news.id)
        score = latest_scores.get(news.id)
        workflow = latest_workflows.get(news.id)
        pending_tasks, blocking_tasks = await _task_counts_for_news(session, news.id)
        pending_outputs = await _count_where(
            session,
            AgentOutput,
            AgentOutput.news_item_id == news.id,
            AgentOutput.status == "pending_review",
        )
        if not (missing or pending_tasks or blocking_tasks or pending_outputs or _low_score(score)):
            continue
        items.append(
            EditorialWorkQueueItem(
                news_item_id=news.id,
                title=news.title,
                status=news.status,
                priority=news.priority,
                workflow_run_id=workflow.id if workflow else None,
                current_step=workflow.current_step if workflow else None,
                readiness_status=score.readiness_status if score else None,
                score=score.score if score else None,
                missing_requirements=score.missing_requirements if score else missing,
                blocking_reasons=score.blocking_reasons if score else [],
                next_agent=score.next_agent if score else None,
                recommended_next_action=score.recommended_next_action if score else None,
                pending_task_count=pending_tasks,
                blocking_task_count=blocking_tasks,
                owner=owner_map.get(news.id),
                created_at=news.created_at,
                updated_at=news.updated_at,
            )
        )
    return sorted(items, key=lambda item: (PRIORITY_ORDER.get(item.priority, 9), item.created_at))


async def get_blockers(session: AsyncSession) -> list[BlockerItem]:
    blockers: list[BlockerItem] = []
    for task in (
        await session.execute(
            select(WorkflowTask).where(
                (WorkflowTask.blocking.is_(True)) | (WorkflowTask.task_status == "blocked")
            )
        )
    ).scalars():
        blockers.append(
            BlockerItem(
                blocker_type="blocked_task",
                entity_type="WorkflowTask",
                entity_id=task.id,
                news_item_id=task.news_item_id,
                title_or_summary=task.title,
                reason=task.blocking_reason or "Task is blocked",
                severity="high",
                recommended_action="Resolve or reassign blocked task.",
                created_at=task.created_at,
            )
        )
    for review in (
        await session.execute(select(RiskReview).where(RiskReview.risk_level == "critical"))
    ).scalars():
        blockers.append(
            BlockerItem(
                blocker_type="critical_risk_review",
                entity_type="RiskReview",
                entity_id=review.id,
                news_item_id=review.news_item_id,
                title_or_summary=review.summary,
                reason="RiskReview risk_level is critical",
                severity="critical",
                recommended_action="Escalate to editor in chief.",
                created_at=review.created_at,
            )
        )
    for check in (
        await session.execute(
            select(AuditCheck).where(
                (AuditCheck.publication_block_recommended.is_(True))
                | (AuditCheck.audit_status.in_({"failed", "blocked"}))
            )
        )
    ).scalars():
        blockers.append(
            BlockerItem(
                blocker_type="blocking_audit_check",
                entity_type="AuditCheck",
                entity_id=check.id,
                news_item_id=(
                    check.entity_id if check.entity_type in {"news_item", "NewsItem"} else None
                ),
                title_or_summary=check.audit_status,
                reason="AuditCheck blocks publication",
                severity="critical",
                recommended_action="Resolve audit requirements.",
                created_at=check.created_at,
            )
        )
    for score in await _latest_readiness_scores(session):
        if score.readiness_status == "blocked":
            blockers.append(
                BlockerItem(
                    blocker_type="blocked_readiness_score",
                    entity_type="EditorialReadinessScore",
                    entity_id=score.id,
                    news_item_id=score.news_item_id,
                    title_or_summary=score.score_band,
                    reason="; ".join(score.blocking_reasons) or "Readiness is blocked",
                    severity="high",
                    recommended_action=(
                        score.recommended_next_action or "Resolve readiness blockers."
                    ),
                    created_at=score.created_at,
                )
            )
    return sorted(blockers, key=lambda item: item.created_at, reverse=True)


async def get_readiness_board(
    session: AsyncSession,
    score_band: str | None = None,
    readiness_status: str | None = None,
    next_agent: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[ReadinessBoardItem]:
    news_map = {item.id: item for item in (await session.execute(select(NewsItem))).scalars()}
    scores = await _latest_readiness_scores(session)
    if score_band:
        scores = [score for score in scores if score.score_band == score_band]
    if readiness_status:
        scores = [score for score in scores if score.readiness_status == readiness_status]
    if next_agent:
        scores = [score for score in scores if score.next_agent == next_agent]
    scores = scores[offset : offset + limit]
    return [
        ReadinessBoardItem(
            news_item_id=score.news_item_id,
            title=(
                news_map.get(score.news_item_id).title
                if news_map.get(score.news_item_id)
                else None
            ),
            score=score.score,
            score_band=score.score_band,
            readiness_status=score.readiness_status,
            human_review_required=score.human_review_required,
            publication_block_recommended=score.publication_block_recommended,
            missing_requirements=score.missing_requirements,
            warnings=score.warnings,
            blocking_reasons=score.blocking_reasons,
            next_agent=score.next_agent,
            recommended_next_action=score.recommended_next_action,
            calculated_at=score.created_at,
        )
        for score in scores
    ]


async def get_task_board(
    session: AsyncSession,
    task_status: str | None = None,
    assigned_agent: str | None = None,
    assigned_to: str | None = None,
    priority: str | None = None,
    blocking: bool | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[TaskBoardItem]:
    stmt = select(WorkflowTask).order_by(WorkflowTask.created_at.desc())
    filters = {
        "task_status": task_status,
        "assigned_agent": assigned_agent,
        "assigned_to": assigned_to,
        "priority": priority,
        "blocking": blocking,
    }
    for column_name, value in filters.items():
        if value is not None:
            stmt = stmt.where(getattr(WorkflowTask, column_name) == value)
    tasks = (await session.execute(stmt.limit(limit).offset(offset))).scalars().all()
    return [_task_item(task) for task in tasks]


async def get_publication_board(
    session: AsyncSession,
    publication_status: str | None = None,
    channel: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[PublicationBoardItem]:
    stmt = select(PublicationRecord).order_by(PublicationRecord.created_at.desc())
    if publication_status:
        stmt = stmt.where(PublicationRecord.publication_status == publication_status)
    if channel:
        stmt = stmt.where(PublicationRecord.channel == channel)
    records = (await session.execute(stmt.limit(limit).offset(offset))).scalars().all()
    news_map = {item.id: item for item in (await session.execute(select(NewsItem))).scalars()}
    return [
        PublicationBoardItem(
            publication_record_id=record.id,
            news_item_id=record.news_item_id,
            content_piece_id=record.content_piece_id,
            distribution_plan_id=record.distribution_plan_id,
            title=(
                news_map.get(record.news_item_id).title
                if news_map.get(record.news_item_id)
                else None
            ),
            channel=record.channel,
            publication_status=record.publication_status,
            published_url=record.published_url,
            external_id=record.external_id,
            published_at=record.published_at,
            owner=record.owner,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )
        for record in records
    ]


async def get_ownership_board(session: AsyncSession) -> OwnershipBoard:
    users = list((await session.execute(select(UserAccount))).scalars().all())
    assignments = list((await session.execute(select(OwnershipAssignment))).scalars().all())
    tasks = list((await session.execute(select(WorkflowTask))).scalars().all())
    summary_items = []
    for user in users:
        active_assignments = [
            assignment
            for assignment in assignments
            if assignment.user_id == user.id and assignment.status == "active"
        ]
        summary_items.append(
            OwnershipUserSummary(
                user_id=user.id,
                display_name=user.display_name,
                role=user.role,
                active_assignment_count=len(active_assignments),
                active_task_count=len([t for t in tasks if t.assigned_to == user.id]),
                owned_news_count=len(
                    [a for a in active_assignments if a.entity_type == "NewsItem"]
                ),
                review_items_count=len(
                    [a for a in active_assignments if a.ownership_type == "reviewer"]
                ),
            )
        )
    return OwnershipBoard(
        users=summary_items,
        assignments=[
            {
                "id": assignment.id,
                "user_id": assignment.user_id,
                "entity_type": assignment.entity_type,
                "entity_id": assignment.entity_id,
                "ownership_type": assignment.ownership_type,
                "status": assignment.status,
            }
            for assignment in assignments
        ],
        unassigned_news=await _unassigned_news_ids(session),
        unassigned_tasks=[task.id for task in tasks if task.assigned_to is None],
        unassigned_content_pieces=await _unassigned_content_piece_ids(session),
    )


async def get_user_workload(session: AsyncSession, user_id: str) -> UserWorkload:
    user = await session.get(UserAccount, user_id)
    if user is None:
        raise NotFoundError("User account")
    assignments = (
        await session.execute(
            select(OwnershipAssignment).where(OwnershipAssignment.user_id == user_id)
        )
    ).scalars().all()
    tasks = (
        await session.execute(select(WorkflowTask).where(WorkflowTask.assigned_to == user_id))
    ).scalars().all()
    task_items = [_task_item(task) for task in tasks]
    blocking_tasks = [task for task in task_items if task.blocking]
    news_owned = [
        assignment.entity_id
        for assignment in assignments
        if assignment.entity_type == "NewsItem" and assignment.status == "active"
    ]
    pending_reviews = [
        {"entity_type": assignment.entity_type, "entity_id": assignment.entity_id}
        for assignment in assignments
        if assignment.ownership_type == "reviewer" and assignment.status == "active"
    ]
    return UserWorkload(
        user={"id": user.id, "display_name": user.display_name, "role": user.role},
        ownership_assignments=[
            {
                "id": assignment.id,
                "entity_type": assignment.entity_type,
                "entity_id": assignment.entity_id,
                "ownership_type": assignment.ownership_type,
                "status": assignment.status,
            }
            for assignment in assignments
        ],
        workflow_tasks=task_items,
        news_items_owned=news_owned,
        blocking_tasks=blocking_tasks,
        pending_reviews=pending_reviews,
        summary_counts={
            "ownership_assignments": len(assignments),
            "workflow_tasks": len(tasks),
            "blocking_tasks": len(blocking_tasks),
            "pending_reviews": len(pending_reviews),
        },
    )


async def get_operational_gaps(session: AsyncSession) -> list[OperationalGap]:
    news_ids = [item.id for item in (await session.execute(select(NewsItem))).scalars()]
    gaps = [
        await _gap_missing_model(
            session, "news_without_verification", news_ids, VerificationRecord
        ),
        await _gap_missing_model(session, "news_without_risk_review", news_ids, RiskReview),
        await _gap_missing_model(session, "news_without_content", news_ids, ContentPiece),
    ]
    gaps.extend(
        [
            OperationalGap(
                gap_type="news_without_source",
                count=await _count_where(
                    session,
                    NewsItem,
                    (NewsItem.source_url == "") | (NewsItem.source_name == ""),
                ),
                severity="high",
                recommended_action="Add source metadata before editorial work.",
                sample_entity_ids=[],
            ),
            await _approved_content_without_distribution(session),
            await _scheduled_distribution_without_publication(session),
            await _published_without_metrics(session),
            await _simple_gap(
                session,
                "agent_outputs_pending_review",
                AgentOutput,
                AgentOutput.status == "pending_review",
                "medium",
                "Review pending agent outputs.",
            ),
            await _simple_gap(
                session,
                "memory_items_needing_review",
                MemoryItem,
                MemoryItem.memory_status.in_({"proposed", "needs_review"}),
                "medium",
                "Review proposed memory items.",
            ),
            OperationalGap(
                gap_type="knowledge_items_needing_review",
                count=0,
                severity="low",
                recommended_action="Review knowledge items needing attention.",
                sample_entity_ids=[],
            ),
            OperationalGap(
                gap_type="tasks_without_owner",
                count=await _count_where(session, WorkflowTask, WorkflowTask.assigned_to.is_(None)),
                severity="medium",
                recommended_action="Assign owners to workflow tasks.",
                sample_entity_ids=[
                    task.id
                    for task in (
                        await session.execute(
                            select(WorkflowTask)
                            .where(WorkflowTask.assigned_to.is_(None))
                            .limit(5)
                        )
                    ).scalars()
                ],
            ),
            OperationalGap(
                gap_type="news_without_owner",
                count=len(await _unassigned_news_ids(session)),
                severity="medium",
                recommended_action="Assign ownership for active news items.",
                sample_entity_ids=(await _unassigned_news_ids(session))[:5],
            ),
        ]
    )
    return gaps


async def _count(session: AsyncSession, model) -> int:
    return await _count_where(session, model)


async def _count_where(session: AsyncSession, model, *conditions) -> int:
    stmt = select(func.count()).select_from(model)
    for condition in conditions:
        stmt = stmt.where(condition)
    return int((await session.execute(stmt)).scalar_one())


async def _counts_by(session: AsyncSession, column) -> dict[str, int]:
    result = await session.execute(select(column, func.count()).group_by(column))
    return {str(key): count for key, count in result.all()}


async def _latest_readiness_scores(session: AsyncSession) -> list[EditorialReadinessScore]:
    result = await session.execute(
        select(EditorialReadinessScore).order_by(EditorialReadinessScore.created_at.desc())
    )
    latest: dict[str, EditorialReadinessScore] = {}
    for score in result.scalars().all():
        latest.setdefault(score.news_item_id, score)
    return list(latest.values())


async def _latest_workflows_by_news(session: AsyncSession) -> dict[str, WorkflowRun]:
    result = await session.execute(select(WorkflowRun).order_by(WorkflowRun.created_at.desc()))
    latest: dict[str, WorkflowRun] = {}
    for workflow in result.scalars().all():
        latest.setdefault(workflow.news_item_id, workflow)
    return latest


async def _owners_by_entity(session: AsyncSession, entity_type: str) -> dict[str, str]:
    result = await session.execute(
        select(OwnershipAssignment).where(
            OwnershipAssignment.entity_type == entity_type,
            OwnershipAssignment.ownership_type == "owner",
            OwnershipAssignment.status == "active",
        )
    )
    return {assignment.entity_id: assignment.user_id for assignment in result.scalars().all()}


async def _unassigned_news_ids(session: AsyncSession) -> list[str]:
    news_ids = {item.id for item in (await session.execute(select(NewsItem))).scalars()}
    owned_ids = set((await _owners_by_entity(session, "NewsItem")).keys())
    return sorted(news_ids - owned_ids)


async def _unassigned_content_piece_ids(session: AsyncSession) -> list[str]:
    pieces = (await session.execute(select(ContentPiece))).scalars().all()
    return [piece.id for piece in pieces if not piece.owner]


async def _task_counts_for_news(session: AsyncSession, news_item_id: str) -> tuple[int, int]:
    tasks = (
        await session.execute(select(WorkflowTask).where(WorkflowTask.news_item_id == news_item_id))
    ).scalars().all()
    pending = len(
        [task for task in tasks if task.task_status not in {"completed", "completed_with_warnings"}]
    )
    blocking = len([task for task in tasks if task.blocking or task.task_status == "blocked"])
    return pending, blocking


async def _missing_requirements_for_news(session: AsyncSession, news_id: str) -> list[str]:
    missing = []
    for label, model in [
        ("VerificationRecord", VerificationRecord),
        ("RiskReview", RiskReview),
        ("ContentPiece", ContentPiece),
        ("AuditCheck", AuditCheck),
    ]:
        if model is AuditCheck:
            exists = await _count_where(
                session,
                AuditCheck,
                AuditCheck.entity_type.in_({"news_item", "NewsItem"}),
                AuditCheck.entity_id == news_id,
            )
        else:
            exists = await _count_where(session, model, model.news_item_id == news_id)
        if not exists:
            missing.append(label)
    return missing


def _low_score(score: EditorialReadinessScore | None) -> bool:
    return bool(score and (score.readiness_status == "blocked" or score.score < 70))


def _task_item(task: WorkflowTask) -> TaskBoardItem:
    return TaskBoardItem(
        task_id=task.id,
        workflow_run_id=task.workflow_run_id,
        news_item_id=task.news_item_id,
        title=task.title,
        task_type=task.task_type,
        task_status=task.task_status,
        priority=task.priority,
        assigned_agent=task.assigned_agent,
        assigned_to=task.assigned_to,
        blocking=task.blocking,
        blocking_reason=task.blocking_reason,
        attempt_count=task.attempt_count,
        max_attempts=task.max_attempts,
        due_at=task.due_at,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


def _labels(items: list[tuple[str, int]]) -> list[str]:
    return [f"{name}: {count}" for name, count in items if count]


def _recommended_actions(status: str) -> list[str]:
    if status == "critical":
        return ["Escalate critical blockers before publication work continues."]
    if status == "degraded":
        return ["Resolve blocked tasks and readiness blockers."]
    return ["Continue normal editorial operations."]


async def _gap_missing_model(
    session: AsyncSession, gap_type: str, news_ids: list[str], model
) -> OperationalGap:
    existing = {
        item.news_item_id
        for item in (await session.execute(select(model))).scalars().all()
    }
    missing = [news_id for news_id in news_ids if news_id not in existing]
    return OperationalGap(
        gap_type=gap_type,
        count=len(missing),
        severity="high" if missing else "low",
        recommended_action=f"Create missing {model.__name__} records.",
        sample_entity_ids=missing[:5],
    )


async def _approved_content_without_distribution(session: AsyncSession) -> OperationalGap:
    pieces = (
        await session.execute(select(ContentPiece).where(ContentPiece.status == "approved"))
    ).scalars().all()
    plan_piece_ids = {
        plan.content_piece_id
        for plan in (await session.execute(select(DistributionPlan))).scalars().all()
    }
    missing = [piece.id for piece in pieces if piece.id not in plan_piece_ids]
    return OperationalGap(
        gap_type="approved_content_without_distribution",
        count=len(missing),
        severity="medium",
        recommended_action="Create DistributionPlan for approved content.",
        sample_entity_ids=missing[:5],
    )


async def _scheduled_distribution_without_publication(session: AsyncSession) -> OperationalGap:
    plans = (
        await session.execute(
            select(DistributionPlan).where(DistributionPlan.status == "scheduled")
        )
    ).scalars().all()
    publication_plan_ids = {
        record.distribution_plan_id
        for record in (await session.execute(select(PublicationRecord))).scalars().all()
    }
    missing = [plan.id for plan in plans if plan.id not in publication_plan_ids]
    return OperationalGap(
        gap_type="scheduled_distribution_without_publication",
        count=len(missing),
        severity="high",
        recommended_action="Create PublicationRecord for scheduled distribution.",
        sample_entity_ids=missing[:5],
    )


async def _published_without_metrics(session: AsyncSession) -> OperationalGap:
    records = (
        await session.execute(
            select(PublicationRecord).where(PublicationRecord.publication_status == "published")
        )
    ).scalars().all()
    metric_publication_ids = {
        metric.publication_record_id
        for metric in (await session.execute(select(MetricSnapshot))).scalars().all()
        if metric.publication_record_id
    }
    missing = [record.id for record in records if record.id not in metric_publication_ids]
    return OperationalGap(
        gap_type="published_without_metrics",
        count=len(missing),
        severity="medium",
        recommended_action="Capture MetricSnapshot after publication.",
        sample_entity_ids=missing[:5],
    )


async def _simple_gap(
    session: AsyncSession,
    gap_type: str,
    model,
    condition,
    severity: str,
    recommended_action: str,
) -> OperationalGap:
    result = await session.execute(select(model).where(condition).limit(5))
    samples = [item.id for item in result.scalars().all()]
    return OperationalGap(
        gap_type=gap_type,
        count=await _count_where(session, model, condition),
        severity=severity,
        recommended_action=recommended_action,
        sample_entity_ids=samples,
    )
