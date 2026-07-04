from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_permission
from app.db.session import get_session
from app.schemas.user_account import UserAccountCreate, UserAccountRead, UserAccountUpdate
from app.services import operational_audit_service, user_account_service

router = APIRouter(prefix="/users", tags=["users"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "",
    response_model=UserAccountRead,
    status_code=201,
    dependencies=[Depends(require_permission("user.create"))],
)
async def create_user(
    payload: UserAccountCreate,
    request: Request,
    session: SessionDep,
) -> UserAccountRead:
    user = await user_account_service.create_user_account(
        session, payload, request.state.correlation_id
    )
    response = UserAccountRead.model_validate(user)
    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="user_event",
        action="user.create",
        permission="user.create",
        decision="created",
        entity_type="UserAccount",
        entity_id=user.id,
        user_id=user.id,
        metadata={"role": user.role, "status": user.status, "is_system_user": user.is_system_user},
    )
    return response


@router.get("", response_model=list[UserAccountRead])
async def list_users(
    session: SessionDep,
    role: str | None = Query(default=None),
    status: str | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    email: str | None = Query(default=None),
    handle: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[UserAccountRead]:
    users = await user_account_service.list_user_accounts(
        session,
        role=role,
        status=status,
        is_active=is_active,
        email=email,
        handle=handle,
        limit=limit,
        offset=offset,
    )
    return [UserAccountRead.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserAccountRead)
async def get_user(user_id: str, session: SessionDep) -> UserAccountRead:
    user = await user_account_service.get_user_account(session, user_id)
    return UserAccountRead.model_validate(user)


@router.patch(
    "/{user_id}",
    response_model=UserAccountRead,
    dependencies=[Depends(require_permission("user.update"))],
)
async def update_user(
    user_id: str,
    payload: UserAccountUpdate,
    request: Request,
    session: SessionDep,
) -> UserAccountRead:
    user = await user_account_service.update_user_account(session, user_id, payload)
    response = UserAccountRead.model_validate(user)
    await operational_audit_service.record_operational_event(
        session,
        request,
        event_type="user_event",
        action="user.update",
        permission="user.update",
        decision="updated",
        entity_type="UserAccount",
        entity_id=user.id,
        user_id=user.id,
        after_state={"role": user.role, "status": user.status, "is_active": user.is_active},
    )
    return response


@router.patch(
    "/{user_id}/activate",
    response_model=UserAccountRead,
    dependencies=[Depends(require_permission("user.update"))],
)
async def activate_user(user_id: str, session: SessionDep) -> UserAccountRead:
    user = await user_account_service.activate_user_account(session, user_id)
    return UserAccountRead.model_validate(user)


@router.patch(
    "/{user_id}/deactivate",
    response_model=UserAccountRead,
    dependencies=[Depends(require_permission("user.update"))],
)
async def deactivate_user(user_id: str, session: SessionDep) -> UserAccountRead:
    user = await user_account_service.deactivate_user_account(session, user_id)
    return UserAccountRead.model_validate(user)
