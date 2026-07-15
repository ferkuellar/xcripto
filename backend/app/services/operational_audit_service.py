from typing import Any
from urllib.parse import urlsplit, urlunsplit

from fastapi import Request
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.errors import NotFoundError
from app.models import OperationalAuditLog
from app.schemas.operational_audit import (
    AdminAuditSummary,
    OperationalAuditLogCreate,
    OperationalAuditLogRead,
)


def redact_url(url: str | None) -> str | None:
    """Drop query string and fragment from a URL before auditing it.

    Source URLs are not secrets, but query params/fragments can carry tokens; we
    keep only scheme + host + path so the audit trail never persists them.
    """
    if not url:
        return url
    try:
        parts = urlsplit(url)
    except ValueError:
        return None
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


async def create_audit_event(
    session: AsyncSession,
    payload: OperationalAuditLogCreate,
    correlation_id: str | None = None,
) -> OperationalAuditLog:
    data = payload.model_dump(exclude={"metadata"})
    audit_event = OperationalAuditLog(**data, event_metadata=payload.metadata)
    if audit_event.correlation_id is None:
        audit_event.correlation_id = correlation_id
    session.add(audit_event)
    await session.commit()
    await session.refresh(audit_event)
    return audit_event


async def record_operational_event(
    session: AsyncSession,
    request: Request,
    *,
    event_type: str,
    action: str,
    decision: str,
    permission: str | None = None,
    outcome: str = "succeeded",
    entity_type: str | None = None,
    entity_id: str | None = None,
    news_item_id: str | None = None,
    workflow_run_id: str | None = None,
    workflow_task_id: str | None = None,
    agent_output_id: str | None = None,
    ownership_id: str | None = None,
    user_id: str | None = None,
    reason: str | None = None,
    before_state: dict[str, Any] | list[Any] | None = None,
    after_state: dict[str, Any] | list[Any] | None = None,
    metadata: dict[str, Any] | list[Any] | None = None,
    error_code: str | None = None,
    error_message: str | None = None,
    actor_id: str | None = None,
    actor_role: str | None = None,
    actor_display: str | None = None,
    actor_source: str | None = None,
) -> OperationalAuditLog:
    request_actor_id = getattr(request.state, "actor_id", None)
    request_actor_role = getattr(request.state, "actor_role", None)
    request_actor_source = getattr(request.state, "actor_source", None)
    if actor_id is None:
        actor_id = request_actor_id
    if actor_role is None:
        actor_role = request_actor_role
    if actor_source is None:
        actor_source = request_actor_source

    settings = get_settings()
    if actor_id is None and actor_role is None and not settings.is_deployed_environment:
        actor_id = request.headers.get("X-Actor-Id")
        actor_role = request.headers.get("X-Actor-Role")
        actor_display = actor_display or request.headers.get("X-Actor-Display")
        actor_source = actor_source or ("header" if actor_id or actor_role else "system")

    payload = OperationalAuditLogCreate(
        event_type=event_type,
        action=action,
        permission=permission,
        actor_id=actor_id,
        actor_role=actor_role or "system",
        actor_display=actor_display or getattr(request.state, "actor_display", None),
        actor_source=actor_source or "system",
        request_method=request.method,
        request_path=request.url.path,
        entity_type=entity_type,
        entity_id=entity_id,
        news_item_id=news_item_id,
        workflow_run_id=workflow_run_id,
        workflow_task_id=workflow_task_id,
        agent_output_id=agent_output_id,
        ownership_id=ownership_id,
        user_id=user_id,
        outcome=outcome,
        decision=decision,
        reason=reason,
        before_state=before_state,
        after_state=after_state,
        metadata=metadata,
        error_code=error_code,
        error_message=error_message,
        correlation_id=getattr(request.state, "correlation_id", None),
    )
    return await create_audit_event(session, payload)


async def list_audit_events(
    session: AsyncSession,
    event_type: str | None = None,
    action: str | None = None,
    permission: str | None = None,
    actor_id: str | None = None,
    actor_role: str | None = None,
    entity_type: str | None = None,
    entity_id: str | None = None,
    news_item_id: str | None = None,
    workflow_run_id: str | None = None,
    workflow_task_id: str | None = None,
    agent_output_id: str | None = None,
    outcome: str | None = None,
    decision: str | None = None,
    correlation_id: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[OperationalAuditLog]:
    stmt = _apply_filters(
        select(OperationalAuditLog).order_by(OperationalAuditLog.created_at.desc()),
        event_type=event_type,
        action=action,
        permission=permission,
        actor_id=actor_id,
        actor_role=actor_role,
        entity_type=entity_type,
        entity_id=entity_id,
        news_item_id=news_item_id,
        workflow_run_id=workflow_run_id,
        workflow_task_id=workflow_task_id,
        agent_output_id=agent_output_id,
        outcome=outcome,
        decision=decision,
        correlation_id=correlation_id,
    )
    result = await session.execute(stmt.limit(limit).offset(offset))
    return list(result.scalars().all())


async def get_audit_event(session: AsyncSession, event_id: str) -> OperationalAuditLog:
    audit_event = await session.get(OperationalAuditLog, event_id)
    if audit_event is None:
        raise NotFoundError("OperationalAuditLog")
    return audit_event


async def get_audit_events_by_correlation_id(
    session: AsyncSession,
    correlation_id: str,
    limit: int = 50,
    offset: int = 0,
) -> list[OperationalAuditLog]:
    return await list_audit_events(
        session, correlation_id=correlation_id, limit=limit, offset=offset
    )


async def get_audit_events_by_actor(
    session: AsyncSession,
    actor_id: str,
    limit: int = 50,
    offset: int = 0,
) -> list[OperationalAuditLog]:
    return await list_audit_events(session, actor_id=actor_id, limit=limit, offset=offset)


async def get_audit_events_by_entity(
    session: AsyncSession,
    entity_type: str,
    entity_id: str,
    limit: int = 50,
    offset: int = 0,
) -> list[OperationalAuditLog]:
    return await list_audit_events(
        session, entity_type=entity_type, entity_id=entity_id, limit=limit, offset=offset
    )


async def get_admin_audit_summary(session: AsyncSession) -> AdminAuditSummary:
    total_events = await _count_all(session)
    by_type = await _group_counts(session, OperationalAuditLog.event_type)
    by_outcome = await _group_counts(session, OperationalAuditLog.outcome)
    by_decision = await _group_counts(session, OperationalAuditLog.decision)
    recent_events = await list_audit_events(session, limit=10, offset=0)
    return AdminAuditSummary(
        total_events=total_events,
        events_by_type=by_type,
        events_by_outcome=by_outcome,
        events_by_decision=by_decision,
        recent_events=[OperationalAuditLogRead.model_validate(event) for event in recent_events],
    )


def _apply_filters(stmt: Select, **filters: str | None) -> Select:
    for column_name, value in filters.items():
        if value is not None:
            stmt = stmt.where(getattr(OperationalAuditLog, column_name) == value)
    return stmt


async def _count_all(session: AsyncSession) -> int:
    result = await session.execute(select(func.count()).select_from(OperationalAuditLog))
    return int(result.scalar_one())


async def _group_counts(session: AsyncSession, column) -> dict[str, int]:
    result = await session.execute(
        select(column, func.count()).select_from(OperationalAuditLog).group_by(column)
    )
    return {str(key): int(count) for key, count in result.all()}
