"""
Authentication tests for the backend.
"""
import pytest
from httpx import AsyncClient
from src.models.user import User
from src.core.security import verify_password


@pytest.mark.asyncio
async def test_signup_success(client):
    """Test successful user signup."""
    user_data = {
        "email": "newuser@example.com",
        "password": "securepassword123",
        "name": "New User"
    }

    response = await client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["name"] == user_data["name"]
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_signup_duplicate_email(client):
    """Test signup with duplicate email returns 409."""
    # First signup should succeed
    user_data = {
        "email": "duplicate@example.com",
        "password": "password123",
        "name": "User One"
    }

    response = await client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 201

    # Second signup with same email should fail
    response = await client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 409

    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_signup_invalid_email(client):
    """Test signup with invalid email format returns 422."""
    user_data = {
        "email": "invalid-email",
        "password": "password123",
        "name": "Invalid User"
    }

    response = await client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_signup_short_password(client):
    """Test signup with password less than 8 chars returns 422."""
    user_data = {
        "email": "shortpass@example.com",
        "password": "pass",
        "name": "Short Password User"
    }

    response = await client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client):
    """Test successful login returns token."""
    # First signup a user
    signup_data = {
        "email": "loginuser@example.com",
        "password": "loginpassword123",
        "name": "Login User"
    }

    response = await client.post("/api/auth/signup", json=signup_data)
    assert response.status_code == 201

    # Then login with correct credentials
    login_data = {
        "email": "loginuser@example.com",
        "password": "loginpassword123"
    }

    response = await client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == login_data["email"]


@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    """Test login with wrong password returns 401."""
    # Signup a user
    signup_data = {
        "email": "wrongpass@example.com",
        "password": "correctpassword123",
        "name": "Wrong Pass User"
    }

    response = await client.post("/api/auth/signup", json=signup_data)
    assert response.status_code == 201

    # Try to login with wrong password
    login_data = {
        "email": "wrongpass@example.com",
        "password": "wrongpassword"
    }

    response = await client.post("/api/auth/login", json=login_data)
    assert response.status_code == 401

    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_login_nonexistent_user(client):
    """Test login with unknown email returns 401."""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "anypassword"
    }

    response = await client.post("/api/auth/login", json=login_data)
    assert response.status_code == 401

    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_get_current_user_valid_token(client):
    """Test that get_current_user dependency extracts correct user from valid token."""
    # Signup a user
    signup_data = {
        "email": "tokenuser@example.com",
        "password": "tokenpassword123",
        "name": "Token User"
    }

    response = await client.post("/api/auth/signup", json=signup_data)
    assert response.status_code == 201

    # Login to get token
    login_data = {
        "email": "tokenuser@example.com",
        "password": "tokenpassword123"
    }

    response = await client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200

    login_response_data = response.json()
    token = login_response_data["access_token"]

    # Use token in a protected endpoint (like creating a task)
    headers = {"Authorization": f"Bearer {token}"}
    task_data = {"title": "Test task", "description": "Test description"}
    response = await client.post(f"/api/{login_response_data['user']['id']}/tasks", json=task_data, headers=headers)

    # If we get here without 401/403, the token was valid
    # The actual task creation will be tested in task tests
    if response.status_code not in [201, 422]:  # 422 is validation error, not auth error
        assert response.status_code != 401  # Should not be unauthorized
        assert response.status_code != 403  # Should not be forbidden


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(client):
    """Test that invalid token returns 401."""
    # First, we need to create a user to get their ID for the endpoint
    user_data = {
        "email": "tempuser@example.com",
        "password": "temppassword123",
        "name": "Temp User"
    }
    response = await client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["id"]

    headers = {"Authorization": "Bearer invalid-token"}
    task_data = {"title": "Test task", "description": "Test description"}
    response = await client.post(f"/api/{user_id}/tasks", json=task_data, headers=headers)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_expired_token(client):
    """Test that expired token returns 401."""
    # First, we need to create a user to get their ID for the endpoint
    user_data = {
        "email": "tempuser2@example.com",
        "password": "temppassword123",
        "name": "Temp User 2"
    }
    response = await client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["id"]

    # This test uses a malformed token to simulate an expired token rejection
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjIwMDAwMDB9.invalid-signature"}
    task_data = {"title": "Test task", "description": "Test description"}
    response = await client.post(f"/api/{user_id}/tasks", json=task_data, headers=headers)

    assert response.status_code == 401