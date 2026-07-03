from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ConflictError, NotFoundError
from app.models import OwnershipAssignment, UserAccount
from app.schemas.ownership import OwnershipAssignmentCreate


async def assign_ownership(
    session: AsyncSession,
    payload: OwnershipAssignmentCreate,
    correlation_id: str | None = None,
) -> OwnershipAssignment:
    if await session.get(UserAccount, payload.user_id) is None:
        raise NotFoundError("User account")
    await _ensure_no_active_duplicate(
        session,
        payload.user_id,
        payload.entity_type,
        payload.entity_id,
        payload.ownership_type,
    )
    data = payload.model_dump()
    assignment = OwnershipAssignment(**data)
    if assignment.assigned_at is None:
        assignment.assigned_at = datetime.now(UTC)
    if assignment.correlation_id is None:
        assignment.correlation_id = correlation_id
    session.add(assignment)
    await session.commit()
    await session.refresh(assignment)
    return assignment


async def list_ownership_assignments(
    session: AsyncSession,
    user_id: str | None = None,
    entity_type: str | None = None,
    entity_id: str | None = None,
    ownership_type: str | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[OwnershipAssignment]:
    stmt = select(OwnershipAssignment).order_by(OwnershipAssignment.created_at.desc())
    filters = {
        "user_id": user_id,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "ownership_type": ownership_type,
        "status": status,
    }
    for column_name, value in filters.items():
        if value is not None:
            stmt = stmt.where(getattr(OwnershipAssignment, column_name) == value)
    result = await session.execute(stmt.limit(limit).offset(offset))
    return list(result.scalars().all())


async def get_ownership_assignment(
    session: AsyncSession, ownership_id: str
) -> OwnershipAssignment:
    assignment = await session.get(OwnershipAssignment, ownership_id)
    if assignment is None:
        raise NotFoundError("Ownership assignment")
    return assignment


async def release_ownership(
    session: AsyncSession,
    ownership_id: str,
    reason: str | None = None,
) -> OwnershipAssignment:
    assignment = await get_ownership_assignment(session, ownership_id)
    assignment.status = "released"
    assignment.released_at = datetime.now(UTC)
    assignment.notes = _append_note(assignment.notes, reason)
    await session.commit()
    await session.refresh(assignment)
    return assignment


async def transfer_ownership(
    session: AsyncSession,
    ownership_id: str,
    new_user_id: str,
    assigned_by: str | None = None,
    notes: str | None = None,
) -> OwnershipAssignment:
    assignment = await get_ownership_assignment(session, ownership_id)
    if await session.get(UserAccount, new_user_id) is None:
        raise NotFoundError("New user account")
    await _ensure_no_active_duplicate(
        session,
        new_user_id,
        assignment.entity_type,
        assignment.entity_id,
        assignment.ownership_type,
    )
    assignment.status = "transferred"
    assignment.released_at = datetime.now(UTC)
    assignment.notes = _append_note(assignment.notes, notes)
    new_assignment = OwnershipAssignment(
        user_id=new_user_id,
        entity_type=assignment.entity_type,
        entity_id=assignment.entity_id,
        ownership_type=assignment.ownership_type,
        status="active",
        assigned_by=assigned_by,
        assigned_at=datetime.now(UTC),
        notes=notes,
        correlation_id=assignment.correlation_id,
    )
    session.add(new_assignment)
    await session.commit()
    await session.refresh(new_assignment)
    return new_assignment


async def _ensure_no_active_duplicate(
    session: AsyncSession,
    user_id: str,
    entity_type: str,
    entity_id: str,
    ownership_type: str,
) -> None:
    result = await session.execute(
        select(OwnershipAssignment)
        .where(
            OwnershipAssignment.user_id == user_id,
            OwnershipAssignment.entity_type == entity_type,
            OwnershipAssignment.entity_id == entity_id,
            OwnershipAssignment.ownership_type == ownership_type,
            OwnershipAssignment.status == "active",
        )
        .limit(1)
    )
    if result.scalar_one_or_none() is not None:
        raise ConflictError("Active ownership assignment already exists")


def _append_note(existing: str | None, note: str | None) -> str | None:
    if not note:
        return existing
    if not existing:
        return note
    return f"{existing}\n{note}"
