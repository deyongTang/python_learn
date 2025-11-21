"""Pydantic 学习实验中使用的模型示例（中文注释便于学习）。"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl, RootModel, field_validator


class Address(BaseModel):
    """地址信息，演示嵌套模型的组合能力。"""

    city: str
    country: str = Field(
        default="China",
        description="国家名称，默认 China，便于观察默认值行为",
    )
    postal_code: Optional[str] = Field(
        default=None,
        min_length=4,
        max_length=12,
        description="可选的邮政编码，限制长度展示数值/字符串校验",
    )


class Profile(BaseModel):
    """用户的可选档案信息。"""

    bio: Optional[str] = Field(
        default=None,
        description="个人简介，可为空，演示可选字段与默认值",
    )
    website: Optional[HttpUrl] = Field(
        default=None,
        description="个人站点 URL，使用 HttpUrl 类型自动校验",
    )
    interests: List[str] = Field(
        default_factory=list,
        description="兴趣列表，使用默认工厂避免可变默认值陷阱",
    )


class User(BaseModel):
    """用户模型，展示字段校验与赋值时的自动验证。"""

    model_config = ConfigDict(validate_assignment=True)

    id: int = Field(ge=1, description="自增 ID，要求为正整数")
    name: str = Field(min_length=1, description="姓名不能为空，自动去除首尾空格")
    email: EmailStr = Field(description="邮箱地址，使用 EmailStr 自动校验格式")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="创建时间，默认为当前 UTC 时间"
    )
    tags: List[str] = Field(
        default_factory=list, description="标签列表，自动去重保持顺序"
    )
    address: Optional[Address] = Field(
        default=None, description="可选的地址信息，演示嵌套模型"
    )
    profile: Optional[Profile] = Field(
        default=None, description="可选档案，包含简介、个人站点与兴趣"
    )

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
