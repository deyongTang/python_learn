from collections.abc import Sequence

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .database import get_session, init_models
from .models import Permission, Role, User
from .schemas import (
    AssignmentResponse,
    PermissionCreate,
    PermissionRead,
    RoleCreate,
    RoleRead,
    UserCreate,
    UserRead,
)

app = FastAPI(title="FastAPI RBAC with MySQL")


@app.on_event("startup")
async def on_startup() -> None:
    await init_models()


@app.post("/permissions", response_model=PermissionRead, status_code=status.HTTP_201_CREATED)
async def create_permission(
    payload: PermissionCreate, session: AsyncSession = Depends(get_session)
) -> Permission:
    permission = Permission(name=payload.name, description=payload.description)
    session.add(permission)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Permission already exists")
    await session.refresh(permission)
    return permission


@app.get("/permissions", response_model=list[PermissionRead])
async def list_permissions(session: AsyncSession = Depends(get_session)) -> Sequence[Permission]:
    result = await session.scalars(select(Permission))
    return result.all()


@app.post("/roles", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
async def create_role(payload: RoleCreate, session: AsyncSession = Depends(get_session)) -> Role:
    role = Role(name=payload.name, description=payload.description)
    session.add(role)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Role already exists")
    await session.refresh(role)
    return role


@app.get("/roles", response_model=list[RoleRead])
async def list_roles(session: AsyncSession = Depends(get_session)) -> Sequence[Role]:
    result = await session.scalars(select(Role).options(selectinload(Role.permissions), selectinload(Role.users)))
    return result.unique().all()


@app.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, session: AsyncSession = Depends(get_session)) -> User:
    user = User(email=payload.email, full_name=payload.full_name, is_active=payload.is_active)
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    await session.refresh(user)
    return user


@app.get("/users", response_model=list[UserRead])
async def list_users(session: AsyncSession = Depends(get_session)) -> Sequence[User]:
    result = await session.scalars(select(User).options(selectinload(User.roles)))
    return result.unique().all()


@app.post("/roles/{role_id}/permissions/{permission_id}", response_model=AssignmentResponse)
async def assign_permission_to_role(
    role_id: int, permission_id: int, session: AsyncSession = Depends(get_session)
) -> AssignmentResponse:
    role = await session.get(Role, role_id)
    permission = await session.get(Permission, permission_id)
    if role is None or permission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role or permission not found")

    if permission not in role.permissions:
        role.permissions.append(permission)
        await session.commit()
    return AssignmentResponse(message=f"Permission {permission.name} added to role {role.name}")


@app.post("/users/{user_id}/roles/{role_id}", response_model=AssignmentResponse)
async def assign_role_to_user(
    user_id: int, role_id: int, session: AsyncSession = Depends(get_session)
) -> AssignmentResponse:
    user = await session.get(User, user_id)
    role = await session.get(Role, role_id)
    if user is None or role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or role not found")

    if role not in user.roles:
        user.roles.append(role)
        await session.commit()
    return AssignmentResponse(message=f"Role {role.name} added to user {user.email}")


@app.get("/users/{user_id}/permissions", response_model=list[PermissionRead])
async def list_user_permissions(user_id: int, session: AsyncSession = Depends(get_session)) -> Sequence[Permission]:
    user = await session.get(User, user_id, options=[selectinload(User.roles).selectinload(Role.permissions)])
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    permissions = {permission for role in user.roles for permission in role.permissions}
    return list(permissions)
