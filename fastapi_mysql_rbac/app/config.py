from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables or .env."""

    database_url: str = "mysql+aiomysql://user:password@localhost:3306/fastapi_rbac"
    echo_sql: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


def get_settings() -> Settings:
    """Return cached settings instance."""

    return Settings()


settings = get_settings()
