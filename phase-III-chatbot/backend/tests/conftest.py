"""
Test configuration and fixtures for the backend.
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from src.main import app
from src.core.database import get_db
from src.models.user import User
from src.core.security import get_password_hash


@pytest.fixture(scope="session")
def event_loop():
    """Override event loop to session scope."""
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db():
    """Create an in-memory test database."""
    from src.config import settings
    # Use in-memory SQLite for testing
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    yield async_session
    app.dependency_overrides.clear()


@pytest.fixture
async def client(test_db):
    """Create a test client."""
    from httpx import ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def authenticated_user(client):
    """Create an authenticated user and return their token."""
    # Create user via signup endpoint
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User"
    }

    response = await client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 201

    # Login to get token
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }

    response = await client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200

    token_data = response.json()
    token = token_data["access_token"]
    user_info = token_data["user"]

    return {
        "user": user_info,
        "token": token
    }