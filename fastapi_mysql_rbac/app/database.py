from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings


class Base(DeclarativeBase):
    """Base class for ORM models."""


engine = create_async_engine(settings.database_url, echo=settings.echo_sql, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Provide a database session dependency for FastAPI routes."""

    async with SessionLocal() as session:
        yield session


async def init_models() -> None:
    """Create database tables based on the ORM metadata."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
