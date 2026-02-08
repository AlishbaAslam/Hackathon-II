"""
Database connection and session management using async SQLModel.
"""
from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from contextlib import contextmanager
from src.config import settings

# Import all models to register them with SQLModel metadata
from src.models import User, Task, Conversation, Message, EventLog, Reminder, WebSocketSession

# Create async engine
# Handle different database types with appropriate connection arguments
if "postgresql" in settings.DATABASE_URL.lower():
    # For PostgreSQL with asyncpg, ensure we're using the async driver
    if "postgresql+asyncpg" not in settings.DATABASE_URL.lower():
        # Replace postgresql with postgresql+asyncpg to use the async driver
        settings.DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

    # Parse the URL to separate the connection parameters that asyncpg can't handle
    from urllib.parse import urlparse, parse_qs, urlencode
    parsed = urlparse(settings.DATABASE_URL)
    query_params = parse_qs(parsed.query)

    # Remove parameters that cause issues with asyncpg
    problematic_params = {'sslmode', 'channel_binding', 'sslcert', 'sslkey', 'sslrootcert'}
    filtered_params = {k: v for k, v in query_params.items() if k not in problematic_params}

    # Reconstruct the URL without problematic parameters since they're handled by asyncpg automatically
    new_query = urlencode(filtered_params, doseq=True)
    reconstructed_url = parsed._replace(query=new_query).geturl()
    settings.DATABASE_URL = reconstructed_url

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

# Create sync engine and session factory for sync operations
if "postgresql" in settings.DATABASE_URL.lower():
    # For PostgreSQL with sync driver
    sync_database_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://").replace("postgresql://", "postgresql://")
    sync_connect_args = {}
elif "sqlite" in settings.DATABASE_URL.lower():
    sync_connect_args = {"check_same_thread": False}
else:
    sync_connect_args = {}

sync_engine = create_engine(
    settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://"),
    echo=settings.DEBUG,
    connect_args=sync_connect_args
)

sync_session = sessionmaker(
    sync_engine,
    expire_on_commit=False
)


@contextmanager
def get_session():
    """
    Context manager that provides a synchronous database session.
    Yields a sync session and ensures it's closed after use.
    """
    session = sync_session()
    try:
        yield session
    finally:
        session.close()

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
        # For PostgreSQL, we need to handle enum types specially to avoid conflicts
        # when they already exist in the database
        from sqlalchemy import text

        # Check if this is a PostgreSQL database
        if "postgresql" in str(engine.url).lower():
            # First, try to create enums individually with IF NOT EXISTS
            # Handle enum conflicts by catching the exception
            try:
                # Create all tables, ignoring errors for existing enums
                await conn.run_sync(SQLModel.metadata.create_all)
            except Exception as e:
                # If it's an enum conflict, try to continue gracefully
                if "duplicate key value violates unique constraint" in str(e) and "pg_type" in str(e):
                    # For PostgreSQL, try to create tables individually to bypass enum conflicts
                    for table in SQLModel.metadata.sorted_tables:
                        try:
                            await conn.run_sync(lambda sync_conn: table.create(sync_conn, checkfirst=True))
                        except Exception:
                            # If individual table creation fails due to enum conflicts, continue
                            pass
                else:
                    raise
        else:
            # For non-PostgreSQL databases, use the standard approach
            await conn.run_sync(SQLModel.metadata.create_all)
