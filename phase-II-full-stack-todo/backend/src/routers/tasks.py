"""
Task CRUD API endpoints with user-scoped routing.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.core.dependencies import get_current_user
from src.models.user import User
from src.services.task_service import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskCompletionRequest,
    TaskResponse,
    TaskListResponse,
    create_task,
    get_user_tasks,
    get_task_by_id,
    update_task,
    toggle_completion,
    delete_task
)

router = APIRouter(prefix="/api", tags=["Tasks"])

@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(
    user_id: UUID,
    task_data: TaskCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new task for a specific user.

    - **user_id**: The ID of the user who will own the task
    - **title**: Task title (required, max 200 characters)
    - **description**: Optional task description (max 2000 characters)

    Requires authentication via Bearer token. The user_id in the path must match the authenticated user's ID.
    """
    # Verify that the user_id in the path matches the authenticated user's ID
    if str(user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    return await create_task(db, task_data, current_user)

@router.get("/{user_id}/tasks", response_model=TaskListResponse)
async def list_tasks_endpoint(
    user_id: UUID,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get paginated list of tasks for a specific user.

    - **user_id**: The ID of the user whose tasks to retrieve
    - **limit**: Maximum number of tasks to return (default: 50, max: 100)
    - **offset**: Number of tasks to skip (default: 0)

    Tasks are returned in newest-first order.
    Requires authentication via Bearer token. The user_id in the path must match the authenticated user's ID.
    """
    # Verify that the user_id in the path matches the authenticated user's ID
    if str(user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access tasks for this user"
        )

    return await get_user_tasks(db, current_user, limit, offset)

@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task_endpoint(
    user_id: UUID,
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific task by ID for a specific user.

    - **user_id**: The ID of the user who owns the task
    - **task_id**: The ID of the task to retrieve

    The authenticated user must be the owner of the task and the user_id in the path must match the authenticated user's ID.
    Requires authentication via Bearer token.
    """
    # Verify that the user_id in the path matches the authenticated user's ID
    if str(user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access tasks for this user"
        )

    return await get_task_by_id(db, task_id, current_user)

@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(
    user_id: UUID,
    task_id: UUID,
    task_data: TaskUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a task's title and description for a specific user.

    - **user_id**: The ID of the user who owns the task
    - **task_id**: The ID of the task to update
    - **title**: New task title (required, max 200 characters)
    - **description**: New task description (optional, max 2000 characters)

    The authenticated user must be the owner of the task and the user_id in the path must match the authenticated user's ID.
    Requires authentication via Bearer token.
    """
    # Verify that the user_id in the path matches the authenticated user's ID
    if str(user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update tasks for this user"
        )

    return await update_task(db, task_id, task_data, current_user)

@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_completion_endpoint(
    user_id: UUID,
    task_id: UUID,
    completion_data: TaskCompletionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Toggle a task's completion status for a specific user.

    - **user_id**: The ID of the user who owns the task
    - **task_id**: The ID of the task to update
    - **is_completed**: New completion status (true/false)

    The authenticated user must be the owner of the task and the user_id in the path must match the authenticated user's ID.
    Requires authentication via Bearer token.
    """
    # Verify that the user_id in the path matches the authenticated user's ID
    if str(user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update tasks for this user"
        )

    return await toggle_completion(db, task_id, completion_data, current_user)

@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
    user_id: UUID,
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a task permanently for a specific user.

    - **user_id**: The ID of the user who owns the task
    - **task_id**: The ID of the task to delete

    The authenticated user must be the owner of the task and the user_id in the path must match the authenticated user's ID.
    Requires authentication via Bearer token.
    Returns 204 No Content on success.
    """
    # Verify that the user_id in the path matches the authenticated user's ID
    if str(user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete tasks for this user"
        )

    await delete_task(db, task_id, current_user)
