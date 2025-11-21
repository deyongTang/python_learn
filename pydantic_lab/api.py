"""FastAPI 应用：演示 Pydantic 的请求体验证。"""
from __future__ import annotations

from typing import Dict

from fastapi import FastAPI, HTTPException

from .models import User
from .settings import get_settings

app = FastAPI(title="Pydantic Lab")
settings = get_settings()
_database: Dict[int, User] = {}


@app.get("/settings")
def read_settings() -> dict:
    """返回当前加载的配置，便于调试和学习。"""

    return settings.model_dump()


@app.post("/users", response_model=User)
def create_user(user: User) -> User:
    """创建用户；若主键重复则返回 400。"""

    if user.id in _database:
        raise HTTPException(status_code=400, detail="用户已存在")
    _database[user.id] = user
    return user


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int) -> User:
    """根据用户 ID 查询，未找到则返回 404。"""

    try:
        return _database[user_id]
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="未找到对应用户") from exc
