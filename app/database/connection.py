from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app import models


def create_db_engine() -> AsyncEngine:
    """Create an asynchronous database engine."""
    return create_async_engine("sqlite+aiosqlite:///products.db")


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create a session factory for asynchronous database sessions."""
    return async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_tables(engine: AsyncEngine) -> None:
    """Create tables in the database."""
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
