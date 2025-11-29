from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr, Field


class PermissionBase(BaseModel):
    name: str = Field(..., examples=["view_reports"])
    description: str | None = Field(None, examples=["Allows reading the reporting dashboard"])


class PermissionCreate(PermissionBase):
    pass


class PermissionRead(PermissionBase):
    id: int

    model_config = {"from_attributes": True}


class RoleBase(BaseModel):
    name: str = Field(..., examples=["admin"])
    description: str | None = Field(None, examples=["Full access to all resources"])


class RoleCreate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: int
    permissions: List[PermissionRead] = []

    model_config = {"from_attributes": True}


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., examples=["Ada Lovelace"])
    is_active: bool = True


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    created_at: datetime
    roles: List[RoleRead] = []

    model_config = {"from_attributes": True}


class AssignmentResponse(BaseModel):
    message: str
