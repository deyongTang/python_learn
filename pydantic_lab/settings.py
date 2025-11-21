"""Settings examples for Pydantic learning lab."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Application configuration loaded from environment variables."""

    db_url: str
    debug: bool = False
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_", extra="ignore")


def get_settings() -> AppSettings:
    """Helper used by CLI and FastAPI app."""

    return AppSettings()


__all__ = ["AppSettings", "get_settings"]
