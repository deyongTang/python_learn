"""FastAPI application showcasing Pydantic validation."""
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
    """Return currently loaded settings for debugging."""

    return settings.model_dump()


@app.post("/users", response_model=User)
def create_user(user: User) -> User:
    if user.id in _database:
        raise HTTPException(status_code=400, detail="User already exists")
    _database[user.id] = user
    return user


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int) -> User:
    try:
        return _database[user_id]
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="User not found") from exc
