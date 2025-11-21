"""Pydantic model examples used in the learning lab."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl, RootModel, field_validator


class Address(BaseModel):
    """Simple nested model for demonstrating composition."""

    city: str
    country: str = Field(default="China", description="Country name, defaults to China")
    postal_code: Optional[str] = Field(default=None, min_length=4, max_length=12)


class Profile(BaseModel):
    """Optional profile information for a user."""

    bio: Optional[str] = None
    website: Optional[HttpUrl] = None
    interests: List[str] = Field(default_factory=list)


class User(BaseModel):
    """User model with basic validation examples."""

    model_config = ConfigDict(validate_assignment=True)

    id: int = Field(ge=1, description="Numeric identifier that must be positive")
    name: str = Field(min_length=1)
    email: EmailStr
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tags: List[str] = Field(default_factory=list)
    address: Optional[Address] = None
    profile: Optional[Profile] = None

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("name cannot be empty or whitespace")
        return cleaned

    @field_validator("tags")
    @classmethod
    def unique_tags(cls, value: List[str]) -> List[str]:
        seen = []
        for tag in value:
            if tag not in seen:
                seen.append(tag)
        return seen


class TagList(RootModel[List[str]]):
    """RootModel demonstration for plain list validation."""

    root: List[str]

    @field_validator("root")
    @classmethod
    def require_lowercase(cls, values: List[str]) -> List[str]:
        return [v.lower() for v in values]


__all__ = ["Address", "Profile", "TagList", "User"]
