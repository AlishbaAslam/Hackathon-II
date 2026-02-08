"""
Database connection and session management using async SQLModel.
"""
from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings

# Create async engine
# Handle different database types with appropriate connection arguments
if "postgresql" in settings.DATABASE_URL.lower():
    # For PostgreSQL with asyncpg, ensure we're using the async driver
    if "postgresql+asyncpg" not in settings.DATABASE_URL.lower():
        # Replace postgresql with postgresql+asyncpg to use the async driver
        settings.DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    connect_args = {}
elif "sqlite" in settings.DATABASE_URL.lower():
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    connect_args=connect_args,
    # For PostgreSQL async connections with asyncpg, we use pool_pre_ping for connection health
    pool_pre_ping=True,
)

# Create async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.
    Yields an async session and ensures it's closed after use.
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_tables():
    """
    Create all database tables based on SQLModel metadata.
    Should be called on application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
