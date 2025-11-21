"""Pydantic 学习实验的配置示例，展示如何读取环境变量。"""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """从环境变量加载的应用配置。"""

    db_url: str
    debug: bool = False
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_", extra="ignore")


def get_settings() -> AppSettings:
    """CLI 与 FastAPI 共享的配置加载辅助函数。"""

    return AppSettings()


__all__ = ["AppSettings", "get_settings"]
