"""Pydantic 学习实验中使用的模型示例（中文注释便于学习）。"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl, RootModel, field_validator


class Address(BaseModel):
    """地址信息，演示嵌套模型的组合能力。"""

    city: str
    country: str = Field(default="China", description="Country name, defaults to China")
    postal_code: Optional[str] = Field(default=None, min_length=4, max_length=12)


class Profile(BaseModel):
    """用户的可选档案信息。"""

    bio: Optional[str] = None
    website: Optional[HttpUrl] = None
    interests: List[str] = Field(default_factory=list)


class User(BaseModel):
    """用户模型，展示字段校验与赋值时的自动验证。"""

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
        """去除姓名两端空白并确保非空。"""

        cleaned = value.strip()
        if not cleaned:
            raise ValueError("姓名不能为空或仅包含空格")
        return cleaned

    @field_validator("tags")
    @classmethod
    def unique_tags(cls, value: List[str]) -> List[str]:
        """保持标签列表的顺序并去重，便于后续展示。"""

        seen: List[str] = []
        for tag in value:
            if tag not in seen:
                seen.append(tag)
        return seen


class TagList(RootModel[List[str]]):
    """基于 RootModel 的纯列表验证示例。"""

    root: List[str]

    @field_validator("root")
    @classmethod
    def require_lowercase(cls, values: List[str]) -> List[str]:
        """将标签统一为小写，便于比较与搜索。"""

        return [v.lower() for v in values]


__all__ = ["Address", "Profile", "TagList", "User"]
