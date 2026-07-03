from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_permission
from app.db.session import get_session
from app.schemas.ownership import (
    OwnershipAssignmentCreate,
    OwnershipAssignmentRead,
    OwnershipRelease,
    OwnershipTransfer,
)
from app.services import operational_audit_service, ownership_service

router = APIRouter(tags=["ownership"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "/ownership/assign",
    response_model=OwnershipAssignmentRead,
    status_code=201,
    dependencies=[Depends(require_permission("ownership.assign"))],
)
async def assign_ownership(
    payload: OwnershipAssignmentCreate,
    request: Request,
    session: SessionDep,
) -> OwnershipAssignmentRead:
    assignment = await ownership_service.assign_ownership(
        session, payload, request.state.correlation_id
    )
    response = OwnershipAssignmentRead.model_validate(assignment)
    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="ownership_event",
        action="ownership.assign",
        permission="ownership.assign",
        decision="assigned",
        entity_type="OwnershipAssignment",
        entity_id=assignment.id,
        ownership_id=assignment.id,
        user_id=assignment.user_id,
        metadata={
            "ownership_type": assignment.ownership_type,
            "target_user_id": assignment.user_id,
            "assigned_entity_type": assignment.entity_type,
            "assigned_entity_id": assignment.entity_id,
        },
    )
    return response


@router.get("/ownership", response_model=list[OwnershipAssignmentRead])
async def list_ownership(
    session: SessionDep,
    user_id: str | None = Query(default=None),
    entity_type: str | None = Query(default=None),
    entity_id: str | None = Query(default=None),
    ownership_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[OwnershipAssignmentRead]:
    assignments = await ownership_service.list_ownership_assignments(
        session,
        user_id=user_id,
        entity_type=entity_type,
        entity_id=entity_id,
        ownership_type=ownership_type,
        status=status,
        limit=limit,
        offset=offset,
    )
    return [OwnershipAssignmentRead.model_validate(assignment) for assignment in assignments]


@router.get("/users/{user_id}/ownership", response_model=list[OwnershipAssignmentRead])
async def list_user_ownership(
    user_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[OwnershipAssignmentRead]:
    assignments = await ownership_service.list_ownership_assignments(
        session, user_id=user_id, limit=limit, offset=offset
    )
    return [OwnershipAssignmentRead.model_validate(assignment) for assignment in assignments]


@router.get(
    "/ownership/entity/{entity_type}/{entity_id}",
    response_model=list[OwnershipAssignmentRead],
)
async def list_entity_ownership(
    entity_type: str,
    entity_id: str,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[OwnershipAssignmentRead]:
    assignments = await ownership_service.list_ownership_assignments(
        session,
        entity_type=entity_type,
        entity_id=entity_id,
        limit=limit,
        offset=offset,
    )
    return [OwnershipAssignmentRead.model_validate(assignment) for assignment in assignments]


@router.patch(
    "/ownership/{ownership_id}/release",
    response_model=OwnershipAssignmentRead,
    dependencies=[Depends(require_permission("ownership.release"))],
)
async def release_ownership(
    ownership_id: str,
    payload: OwnershipRelease,
    request: Request,
    session: SessionDep,
) -> OwnershipAssignmentRead:
    assignment = await ownership_service.release_ownership(
        session, ownership_id, payload.reason
    )
    response = OwnershipAssignmentRead.model_validate(assignment)
    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="ownership_event",
        action="ownership.release",
        permission="ownership.release",
        decision="released",
        entity_type="OwnershipAssignment",
        entity_id=assignment.id,
        ownership_id=assignment.id,
        user_id=assignment.user_id,
        reason=payload.reason,
        after_state={"status": assignment.status},
    )
    return response


@router.patch(
    "/ownership/{ownership_id}/transfer",
    response_model=OwnershipAssignmentRead,
    dependencies=[Depends(require_permission("ownership.assign"))],
)
async def transfer_ownership(
    ownership_id: str,
    payload: OwnershipTransfer,
    request: Request,
    session: SessionDep,
) -> OwnershipAssignmentRead:
    assignment = await ownership_service.transfer_ownership(
        session,
        ownership_id,
        new_user_id=payload.new_user_id,
        assigned_by=payload.assigned_by,
        notes=payload.notes,
    )
    response = OwnershipAssignmentRead.model_validate(assignment)
    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="ownership_event",
        action="ownership.transfer",
        permission="ownership.assign",
        decision="transferred",
        entity_type="OwnershipAssignment",
        entity_id=assignment.id,
        ownership_id=assignment.id,
        user_id=assignment.user_id,
        metadata={
            "previous_ownership_id": ownership_id,
            "new_user_id": payload.new_user_id,
            "ownership_type": assignment.ownership_type,
        },
    )
    return response


@router.get("/ownership/{ownership_id}", response_model=OwnershipAssignmentRead)
async def get_ownership(
    ownership_id: str,
    session: SessionDep,
) -> OwnershipAssignmentRead:
    assignment = await ownership_service.get_ownership_assignment(session, ownership_id)
    return OwnershipAssignmentRead.model_validate(assignment)
