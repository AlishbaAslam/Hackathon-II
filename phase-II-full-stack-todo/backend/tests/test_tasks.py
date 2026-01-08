"""
Task CRUD tests for the backend with user-scoped endpoints.
"""
import pytest
from httpx import AsyncClient
from uuid import UUID
from datetime import datetime


@pytest.mark.asyncio
async def test_create_task_success(client, authenticated_user):
    """Test authenticated user creates task, returns 201 with task data."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}
    task_data = {
        "title": "Test Task",
        "description": "Test Description"
    }

    response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["is_completed"] is False
    assert "id" in data
    assert "user_id" in data
    assert "created_at" in data
    assert "updated_at" in data

    # Verify the user_id matches the authenticated user
    assert data["user_id"] == str(authenticated_user['user']['id'])


@pytest.mark.asyncio
async def test_create_task_without_description(client, authenticated_user):
    """Test task with only title succeeds."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}
    task_data = {
        "title": "Test Task Without Description"
        # No description field
    }

    response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] is None  # Should be None when not provided
    assert data["is_completed"] is False
    assert data["user_id"] == str(authenticated_user['user']['id'])


@pytest.mark.asyncio
async def test_create_task_empty_title(client, authenticated_user):
    """Test empty title returns 422."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}
    task_data = {
        "title": "",
        "description": "Test Description"
    }

    response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_task_unauthenticated(client):
    """Test no token returns 401."""
    task_data = {
        "title": "Test Task",
        "description": "Test Description"
    }

    response = await client.post(f"/api/123/tasks", json=task_data)  # Using fake user_id since auth should fail first
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_tasks_empty(client, authenticated_user):
    """Test user with no tasks returns empty array."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    response = await client.get(f"/api/{authenticated_user['user']['id']}/tasks", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "tasks" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    assert len(data["tasks"]) == 0
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_list_tasks_multiple(client, authenticated_user):
    """Test user with 5 tasks returns all 5."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Create 5 tasks
    for i in range(5):
        task_data = {
            "title": f"Test Task {i}",
            "description": f"Test Description {i}"
        }
        response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
        assert response.status_code == 201

    # Get the list
    response = await client.get(f"/api/{authenticated_user['user']['id']}/tasks", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert len(data["tasks"]) == 5
    assert data["total"] == 5


@pytest.mark.asyncio
async def test_list_tasks_pagination(client, authenticated_user):
    """Test limit=2 offset=0 returns first 2 tasks with correct metadata."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Create 5 tasks
    for i in range(5):
        task_data = {
            "title": f"Pagination Task {i}",
            "description": f"Test Description {i}"
        }
        response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
        assert response.status_code == 201

    # Get first 2 tasks
    response = await client.get(f"/api/{authenticated_user['user']['id']}/tasks?limit=2&offset=0", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert len(data["tasks"]) == 2
    assert data["limit"] == 2
    assert data["offset"] == 0
    assert data["total"] == 5

    # Verify the tasks are in the right order (newest first)
    assert data["tasks"][0]["title"] == "Pagination Task 4"  # Newest first
    assert data["tasks"][1]["title"] == "Pagination Task 3"


@pytest.mark.asyncio
async def test_list_tasks_user_isolation(client, authenticated_user):
    """Test User A cannot see User B's tasks - CRITICAL."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Create some tasks for first user
    task_data = {
        "title": "User A Task",
        "description": "Task for User A"
    }
    response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
    assert response.status_code == 201
    user_a_task = response.json()

    # Create a second user
    user_b_data = {
        "email": "userb@example.com",
        "password": "userbpassword123",
        "name": "User B"
    }
    response = await client.post("/api/auth/signup", json=user_b_data)
    assert response.status_code == 201

    # Login as User B
    login_data = {
        "email": "userb@example.com",
        "password": "userbpassword123"
    }
    response = await client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    user_b_token = response.json()["access_token"]
    user_b_headers = {"Authorization": f"Bearer {user_b_token}"}

    # Get user B's ID from their token by logging in and checking response
    user_b_info = response.json()["user"]
    user_b_id = user_b_info["id"]

    # Create a task for User B
    task_data_b = {
        "title": "User B Task",
        "description": "Task for User B"
    }
    response = await client.post(f"/api/{user_b_id}/tasks", json=task_data_b, headers=user_b_headers)
    assert response.status_code == 201
    user_b_task = response.json()

    # User A should not see User B's task
    response = await client.get(f"/api/{authenticated_user['user']['id']}/tasks", headers=headers)
    assert response.status_code == 200
    user_a_tasks = response.json()
    user_a_task_ids = [task["id"] for task in user_a_tasks["tasks"]]
    assert user_b_task["id"] not in user_a_task_ids

    # User B should not see User A's task
    response = await client.get(f"/api/{user_b_id}/tasks", headers=user_b_headers)
    assert response.status_code == 200
    user_b_tasks = response.json()
    user_b_task_ids = [task["id"] for task in user_b_tasks["tasks"]]
    assert user_a_task["id"] not in user_b_task_ids


@pytest.mark.asyncio
async def test_list_tasks_pagination_beyond_total(client, authenticated_user):
    """Test offset exceeds total returns empty array with metadata."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Create 2 tasks
    for i in range(2):
        task_data = {
            "title": f"Offset Test Task {i}",
            "description": f"Test Description {i}"
        }
        response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
        assert response.status_code == 201

    # Get tasks with offset beyond total
    response = await client.get(f"/api/{authenticated_user['user']['id']}/tasks?limit=2&offset=10", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert len(data["tasks"]) == 0
    assert data["limit"] == 2
    assert data["offset"] == 10
    assert data["total"] == 2


@pytest.mark.asyncio
async def test_get_task_success(client, authenticated_user):
    """Test owner can retrieve their task."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Create a task
    task_data = {
        "title": "Retrievable Task",
        "description": "Task to retrieve"
    }
    response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
    assert response.status_code == 201
    created_task = response.json()

    # Retrieve the task
    task_id = created_task["id"]
    response = await client.get(f"/api/{authenticated_user['user']['id']}/tasks/{task_id}", headers=headers)
    assert response.status_code == 200

    retrieved_task = response.json()
    assert retrieved_task["id"] == created_task["id"]
    assert retrieved_task["title"] == created_task["title"]
    assert retrieved_task["description"] == created_task["description"]


@pytest.mark.asyncio
async def test_get_task_not_owner(client, authenticated_user):
    """Test non-owner gets 403."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Create a task as first user
    task_data = {
        "title": "Protected Task",
        "description": "Task to protect"
    }
    response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
    assert response.status_code == 201
    protected_task = response.json()

    # Create a second user
    user2_data = {
        "email": "user2@example.com",
        "password": "user2password123",
        "name": "User 2"
    }
    response = await client.post("/api/auth/signup", json=user2_data)
    assert response.status_code == 201

    # Login as User 2
    login_data = {
        "email": "user2@example.com",
        "password": "user2password123"
    }
    response = await client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    user2_token = response.json()["access_token"]
    user2_headers = {"Authorization": f"Bearer {user2_token}"}

    # Get user2's ID from the login response
    user2_info = response.json()["user"]
    user2_id = user2_info["id"]

    # Try to access first user's task using first user's ID in path (should fail with 403)
    task_id = protected_task["id"]
    response = await client.get(f"/api/{authenticated_user['user']['id']}/tasks/{task_id}", headers=user2_headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_task_not_found(client, authenticated_user):
    """Test invalid task_id returns 404."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Use a random UUID
    fake_task_id = "123e4567-e89b-12d3-a456-426614174000"
    response = await client.get(f"/api/{authenticated_user['user']['id']}/tasks/{fake_task_id}", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_task_success(client, authenticated_user):
    """Test owner updates task, returns 200 with updated data."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Create a task
    task_data = {
        "title": "Original Title",
        "description": "Original Description"
    }
    response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
    assert response.status_code == 201
    created_task = response.json()

    # Update the task
    updated_data = {
        "title": "Updated Title",
        "description": "Updated Description"
    }
    task_id = created_task["id"]
    response = await client.put(f"/api/{authenticated_user['user']['id']}/tasks/{task_id}", json=updated_data, headers=headers)
    assert response.status_code == 200

    updated_task = response.json()
    assert updated_task["id"] == created_task["id"]
    assert updated_task["title"] == updated_data["title"]
    assert updated_task["description"] == updated_data["description"]
    # Verify the updated_at timestamp changed
    assert updated_task["updated_at"] != created_task["updated_at"]


@pytest.mark.asyncio
async def test_update_task_not_owner(client, authenticated_user):
    """Test non-owner gets 403."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Create a task as first user
    task_data = {
        "title": "Protected Task",
        "description": "Task to protect"
    }
    response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
    assert response.status_code == 201
    protected_task = response.json()

    # Create a second user
    user2_data = {
        "email": "user2update@example.com",
        "password": "user2password123",
        "name": "User 2 Update"
    }
    response = await client.post("/api/auth/signup", json=user2_data)
    assert response.status_code == 201

    # Login as User 2
    login_data = {
        "email": "user2update@example.com",
        "password": "user2password123"
    }
    response = await client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    user2_token = response.json()["access_token"]
    user2_headers = {"Authorization": f"Bearer {user2_token}"}

    # Get user2's ID from the login response
    user2_info = response.json()["user"]
    user2_id = user2_info["id"]

    # Try to update first user's task
    updated_data = {
        "title": "Hacked Title",
        "description": "Hacked Description"
    }
    task_id = protected_task["id"]
    response = await client.put(f"/api/{authenticated_user['user']['id']}/tasks/{task_id}", json=updated_data, headers=user2_headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_task_not_found(client, authenticated_user):
    """Test invalid task_id returns 404."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    updated_data = {
        "title": "Updated Title",
        "description": "Updated Description"
    }
    fake_task_id = "123e4567-e89b-12d3-a456-426614174000"
    response = await client.put(f"/api/{authenticated_user['user']['id']}/tasks/{fake_task_id}", json=updated_data, headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_task_empty_title(client, authenticated_user):
    """Test empty title returns 422."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Create a task
    task_data = {
        "title": "Original Title",
        "description": "Original Description"
    }
    response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
    assert response.status_code == 201
    created_task = response.json()

    # Try to update with empty title
    updated_data = {
        "title": "",
        "description": "Updated Description"
    }
    task_id = created_task["id"]
    response = await client.put(f"/api/{authenticated_user['user']['id']}/tasks/{task_id}", json=updated_data, headers=headers)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_task_timestamp_refreshed(client, authenticated_user):
    """Test updated_at timestamp changes after update."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Create a task
    task_data = {
        "title": "Timestamp Test Task",
        "description": "Task to test timestamp"
    }
    response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
    assert response.status_code == 201
    created_task = response.json()

    original_updated_at = created_task["updated_at"]

    # Update the task
    import time
    time.sleep(0.01)  # Small delay to ensure timestamp difference

    updated_data = {
        "title": "Updated Timestamp Test Task",
        "description": "Updated task to test timestamp"
    }
    task_id = created_task["id"]
    response = await client.put(f"/api/{authenticated_user['user']['id']}/tasks/{task_id}", json=updated_data, headers=headers)
    assert response.status_code == 200

    updated_task = response.json()
    assert updated_task["updated_at"] != original_updated_at


@pytest.mark.asyncio
async def test_toggle_completion_mark_complete(client, authenticated_user):
    """Test incomplete→complete returns 200."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Create an incomplete task
    task_data = {
        "title": "Completion Test Task",
        "description": "Task to test completion"
    }
    response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
    assert response.status_code == 201
    created_task = response.json()

    assert created_task["is_completed"] is False

    # Mark it as complete
    completion_data = {"is_completed": True}
    task_id = created_task["id"]
    response = await client.patch(f"/api/{authenticated_user['user']['id']}/tasks/{task_id}/complete", json=completion_data, headers=headers)
    assert response.status_code == 200

    updated_task = response.json()
    assert updated_task["is_completed"] is True


@pytest.mark.asyncio
async def test_toggle_completion_mark_incomplete(client, authenticated_user):
    """Test complete→incomplete returns 200."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Create a task and mark it complete
    task_data = {
        "title": "Uncompletion Test Task",
        "description": "Task to test uncompletion"
    }
    response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
    assert response.status_code == 201
    created_task = response.json()

    # Mark it as complete
    completion_data = {"is_completed": True}
    task_id = created_task["id"]
    response = await client.patch(f"/api/{authenticated_user['user']['id']}/tasks/{task_id}/complete", json=completion_data, headers=headers)
    assert response.status_code == 200

    completed_task = response.json()
    assert completed_task["is_completed"] is True

    # Mark it as incomplete again
    completion_data = {"is_completed": False}
    response = await client.patch(f"/api/{authenticated_user['user']['id']}/tasks/{task_id}/complete", json=completion_data, headers=headers)
    assert response.status_code == 200

    uncompleted_task = response.json()
    assert uncompleted_task["is_completed"] is False


@pytest.mark.asyncio
async def test_toggle_completion_not_owner(client, authenticated_user):
    """Test non-owner gets 403."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Create a task as first user
    task_data = {
        "title": "Protected Completion Task",
        "description": "Task to protect from completion"
    }
    response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
    assert response.status_code == 201
    protected_task = response.json()

    # Create a second user
    user2_data = {
        "email": "user2complete@example.com",
        "password": "user2password123",
        "name": "User 2 Complete"
    }
    response = await client.post("/api/auth/signup", json=user2_data)
    assert response.status_code == 201

    # Login as User 2
    login_data = {
        "email": "user2complete@example.com",
        "password": "user2password123"
    }
    response = await client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    user2_token = response.json()["access_token"]
    user2_headers = {"Authorization": f"Bearer {user2_token}"}

    # Get user2's ID from the login response
    user2_info = response.json()["user"]
    user2_id = user2_info["id"]

    # Try to toggle completion of first user's task
    completion_data = {"is_completed": True}
    task_id = protected_task["id"]
    response = await client.patch(f"/api/{authenticated_user['user']['id']}/tasks/{task_id}/complete", json=completion_data, headers=user2_headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_toggle_completion_not_found(client, authenticated_user):
    """Test invalid task_id returns 404."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    completion_data = {"is_completed": True}
    fake_task_id = "123e4567-e89b-12d3-a456-426614174000"
    response = await client.patch(f"/api/{authenticated_user['user']['id']}/tasks/{fake_task_id}/complete", json=completion_data, headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_success(client, authenticated_user):
    """Test owner deletes task, returns 204."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Create a task
    task_data = {
        "title": "Deletable Task",
        "description": "Task to delete"
    }
    response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
    assert response.status_code == 201
    created_task = response.json()

    # Delete the task
    task_id = created_task["id"]
    response = await client.delete(f"/api/{authenticated_user['user']['id']}/tasks/{task_id}", headers=headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_task_verifies_removal(client, authenticated_user):
    """Test deleted task not in subsequent GET /api/{user_id}/tasks."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Create a task
    task_data = {
        "title": "Task to Verify Deletion",
        "description": "Task to verify deletion works"
    }
    response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
    assert response.status_code == 201
    created_task = response.json()

    task_id = created_task["id"]

    # Verify task exists
    response = await client.get(f"/api/{authenticated_user['user']['id']}/tasks/{task_id}", headers=headers)
    assert response.status_code == 200

    # Delete the task
    response = await client.delete(f"/api/{authenticated_user['user']['id']}/tasks/{task_id}", headers=headers)
    assert response.status_code == 204

    # Verify task no longer exists
    response = await client.get(f"/api/{authenticated_user['user']['id']}/tasks/{task_id}", headers=headers)
    assert response.status_code == 404

    # Verify task not in task list
    response = await client.get(f"/api/{authenticated_user['user']['id']}/tasks", headers=headers)
    assert response.status_code == 200
    data = response.json()
    task_ids = [task["id"] for task in data["tasks"]]
    assert task_id not in task_ids


@pytest.mark.asyncio
async def test_delete_task_not_owner(client, authenticated_user):
    """Test non-owner gets 403."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Create a task as first user
    task_data = {
        "title": "Protected Delete Task",
        "description": "Task to protect from deletion"
    }
    response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
    assert response.status_code == 201
    protected_task = response.json()

    # Create a second user
    user2_data = {
        "email": "user2delete@example.com",
        "password": "user2password123",
        "name": "User 2 Delete"
    }
    response = await client.post("/api/auth/signup", json=user2_data)
    assert response.status_code == 201

    # Login as User 2
    login_data = {
        "email": "user2delete@example.com",
        "password": "user2password123"
    }
    response = await client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    user2_token = response.json()["access_token"]
    user2_headers = {"Authorization": f"Bearer {user2_token}"}

    # Get user2's ID from the login response
    user2_info = response.json()["user"]
    user2_id = user2_info["id"]

    # Try to delete first user's task
    task_id = protected_task["id"]
    response = await client.delete(f"/api/{authenticated_user['user']['id']}/tasks/{task_id}", headers=user2_headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_task_not_found(client, authenticated_user):
    """Test invalid task_id returns 404."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    fake_task_id = "123e4567-e89b-12d3-a456-426614174000"
    response = await client.delete(f"/api/{authenticated_user['user']['id']}/tasks/{fake_task_id}", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_already_deleted(client, authenticated_user):
    """Test delete again returns 404."""
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Create a task
    task_data = {
        "title": "Double Delete Task",
        "description": "Task to delete twice"
    }
    response = await client.post(f"/api/{authenticated_user['user']['id']}/tasks", json=task_data, headers=headers)
    assert response.status_code == 201
    created_task = response.json()

    task_id = created_task["id"]

    # Delete the task
    response = await client.delete(f"/api/{authenticated_user['user']['id']}/tasks/{task_id}", headers=headers)
    assert response.status_code == 204

    # Try to delete again
    response = await client.delete(f"/api/{authenticated_user['user']['id']}/tasks/{task_id}", headers=headers)
    assert response.status_code == 404