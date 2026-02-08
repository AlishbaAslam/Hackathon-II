"""
Integration tests for the backend.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_full_flow_integration(client):
    """Full flow: signup → login → create task → list tasks → update → delete."""
    # Step 1: Signup
    user_data = {
        "email": "integration@example.com",
        "password": "integrationpassword123",
        "name": "Integration User"
    }
    response = await client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 201
    signup_data = response.json()
    user_id = signup_data["id"]
    assert signup_data["email"] == user_data["email"]

    # Step 2: Login
    login_data = {
        "email": "integration@example.com",
        "password": "integrationpassword123"
    }
    response = await client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 3: Create task
    task_data = {
        "title": "Integration Test Task",
        "description": "Task created during integration test"
    }
    response = await client.post(f"/api/{user_id}/tasks", json=task_data, headers=headers)
    assert response.status_code == 201
    created_task = response.json()
    assert created_task["title"] == task_data["title"]
    assert created_task["is_completed"] is False

    # Step 4: List tasks
    response = await client.get(f"/api/{user_id}/tasks", headers=headers)
    assert response.status_code == 200
    tasks_data = response.json()
    assert tasks_data["total"] == 1
    assert len(tasks_data["tasks"]) == 1
    assert tasks_data["tasks"][0]["id"] == created_task["id"]

    # Step 5: Update task
    update_data = {
        "title": "Updated Integration Test Task",
        "description": "Updated task description"
    }
    task_id = created_task["id"]
    response = await client.put(f"/api/{user_id}/tasks/{task_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == update_data["title"]

    # Step 6: Mark complete
    completion_data = {"is_completed": True}
    response = await client.patch(f"/api/{user_id}/tasks/{task_id}/complete", json=completion_data, headers=headers)
    assert response.status_code == 200
    completed_task = response.json()
    assert completed_task["is_completed"] is True

    # Step 7: Delete task
    response = await client.delete(f"/api/{user_id}/tasks/{task_id}", headers=headers)
    assert response.status_code == 204

    # Verify task was deleted
    response = await client.get(f"/api/{user_id}/tasks/{task_id}", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_user_isolation_integration(client):
    """User A and User B cannot access each other's data."""
    # Create User A
    user_a_data = {
        "email": "usera@example.com",
        "password": "userapassword123",
        "name": "User A"
    }
    response = await client.post("/api/auth/signup", json=user_a_data)
    assert response.status_code == 201
    user_a_id = response.json()["id"]

    # Login as User A
    login_a_data = {
        "email": "usera@example.com",
        "password": "userapassword123"
    }
    response = await client.post("/api/auth/login", json=login_a_data)
    assert response.status_code == 200
    user_a_token = response.json()["access_token"]
    user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

    # Create a task for User A
    task_a_data = {
        "title": "User A's Task",
        "description": "Task belonging to User A"
    }
    response = await client.post(f"/api/{user_a_id}/tasks", json=task_a_data, headers=user_a_headers)
    assert response.status_code == 201
    user_a_task = response.json()

    # Create User B
    user_b_data = {
        "email": "userb@example.com",
        "password": "userbpassword123",
        "name": "User B"
    }
    response = await client.post("/api/auth/signup", json=user_b_data)
    assert response.status_code == 201
    user_b_id = response.json()["id"]

    # Login as User B
    login_b_data = {
        "email": "userb@example.com",
        "password": "userbpassword123"
    }
    response = await client.post("/api/auth/login", json=login_b_data)
    assert response.status_code == 200
    user_b_token = response.json()["access_token"]
    user_b_headers = {"Authorization": f"Bearer {user_b_token}"}

    # Create a task for User B
    task_b_data = {
        "title": "User B's Task",
        "description": "Task belonging to User B"
    }
    response = await client.post(f"/api/{user_b_id}/tasks", json=task_b_data, headers=user_b_headers)
    assert response.status_code == 201
    user_b_task = response.json()

    # Verify User A cannot see User B's task
    response = await client.get(f"/api/{user_a_id}/tasks", headers=user_a_headers)
    assert response.status_code == 200
    user_a_tasks = response.json()
    user_a_task_ids = [task["id"] for task in user_a_tasks["tasks"]]
    assert user_b_task["id"] not in user_a_task_ids

    # Verify User B cannot see User A's task
    response = await client.get(f"/api/{user_b_id}/tasks", headers=user_b_headers)
    assert response.status_code == 200
    user_b_tasks = response.json()
    user_b_task_ids = [task["id"] for task in user_b_tasks["tasks"]]
    assert user_a_task["id"] not in user_b_task_ids

    # Verify User A cannot access User B's task directly
    response = await client.get(f"/api/{user_a_id}/tasks/{user_b_task['id']}", headers=user_a_headers)
    assert response.status_code == 403

    # Verify User B cannot access User A's task directly
    response = await client.get(f"/api/{user_b_id}/tasks/{user_a_task['id']}", headers=user_b_headers)
    assert response.status_code == 403

    # Verify User A cannot update User B's task
    update_data = {"title": "Hacked Task", "description": "Hacked description"}
    response = await client.put(f"/api/{user_a_id}/tasks/{user_b_task['id']}", json=update_data, headers=user_a_headers)
    assert response.status_code == 403

    # Verify User B cannot update User A's task
    response = await client.put(f"/api/{user_b_id}/tasks/{user_a_task['id']}", json=update_data, headers=user_b_headers)
    assert response.status_code == 403

    # Verify User A cannot delete User B's task
    response = await client.delete(f"/api/{user_a_id}/tasks/{user_b_task['id']}", headers=user_a_headers)
    assert response.status_code == 403

    # Verify User B cannot delete User A's task
    response = await client.delete(f"/api/{user_b_id}/tasks/{user_a_task['id']}", headers=user_b_headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_pagination_integration(client, authenticated_user):
    """Create 100 tasks, paginate correctly."""
    user_id = authenticated_user['user']['id']
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Create 100 tasks
    created_task_ids = []
    for i in range(100):
        task_data = {
            "title": f"Pagination Task {i}",
            "description": f"Task #{i} for pagination testing"
        }
        response = await client.post(f"/api/{user_id}/tasks", json=task_data, headers=headers)
        assert response.status_code == 201
        created_task_ids.append(response.json()["id"])

    # Test pagination: get first 10
    response = await client.get(f"/api/{user_id}/tasks?limit=10&offset=0", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 100
    assert data["limit"] == 10
    assert data["offset"] == 0
    assert len(data["tasks"]) == 10

    # Test pagination: get next 10
    response = await client.get(f"/api/{user_id}/tasks?limit=10&offset=10", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 100
    assert data["limit"] == 10
    assert data["offset"] == 10
    assert len(data["tasks"]) == 10

    # Test pagination: get last few
    response = await client.get(f"/api/{user_id}/tasks?limit=10&offset=90", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 100
    assert data["limit"] == 10
    assert data["offset"] == 90
    # Should have 10 tasks left (90-99)
    assert len(data["tasks"]) == 10

    # Verify all tasks are properly paginated and in the right order (newest first)
    # Get first page and verify ordering
    response = await client.get(f"/api/{user_id}/tasks?limit=5&offset=0", headers=headers)
    data = response.json()
    # Tasks should be in reverse chronological order (newest first)
    # So the first task on the page should be the one with the highest index
    assert data["tasks"][0]["title"] == "Pagination Task 99"
    assert data["tasks"][1]["title"] == "Pagination Task 98"
    assert data["tasks"][2]["title"] == "Pagination Task 97"
    assert data["tasks"][3]["title"] == "Pagination Task 96"
    assert data["tasks"][4]["title"] == "Pagination Task 95"