"""
Task service logic for CRUD operations.
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy import func
from fastapi import HTTPException, status
from src.models.task import Task
from src.models.user import User
from src.core.exceptions import ForbiddenException, NotFoundException

# Request/Response Schemas

class TaskCreateRequest(BaseModel):
    """Request schema for creating a task."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)

class TaskUpdateRequest(BaseModel):
    """Request schema for updating a task."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)

class TaskCompletionRequest(BaseModel):
    """Request schema for toggling task completion."""
    # Accept both 'completed' and 'is_completed' field names
    completed: Optional[bool] = Field(default=None, alias="completed")
    is_completed: Optional[bool] = Field(default=None, alias="is_completed")

    class Config:
        populate_by_name = True

class TaskResponse(BaseModel):
    """Response schema for task data."""
    id: str
    title: str
    description: Optional[str]
    is_completed: bool
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TaskListResponse(BaseModel):
    """Response schema for paginated task list."""
    tasks: List[TaskResponse]
    total: int
    limit: int
    offset: int

# Service Functions

async def create_task(
    db: AsyncSession,
    task_data: TaskCreateRequest,
    user: User
) -> TaskResponse:
    """
    Create a new task owned by the authenticated user.

    Args:
        db: Database session
        task_data: Task creation data
        user: Authenticated user

    Returns:
        TaskResponse with created task data
    """
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        user_id=user.id
    )

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    return TaskResponse(
        id=str(new_task.id),
        title=new_task.title,
        description=new_task.description,
        is_completed=new_task.is_completed,
        user_id=str(new_task.user_id),
        created_at=new_task.created_at,
        updated_at=new_task.updated_at
    )

async def get_user_tasks(
    db: AsyncSession,
    user: User,
    limit: int = 50,
    offset: int = 0
) -> TaskListResponse:
    """
    Get paginated list of tasks owned by the authenticated user.

    Args:
        db: Database session
        user: Authenticated user
        limit: Maximum number of tasks to return (default: 50, max: 100)
        offset: Number of tasks to skip (default: 0)

    Returns:
        TaskListResponse with paginated tasks and metadata
    """
    # Enforce limit bounds
    limit = min(limit, 100)

    # Get total count
    count_statement = select(func.count(Task.id)).where(Task.user_id == user.id)
    count_result = await db.execute(count_statement)
    total = count_result.scalar_one()

    # Get paginated tasks (oldest first)
    result = await db.execute(
        select(Task)
        .where(Task.user_id == user.id)
        .order_by(Task.created_at.asc())
        .limit(limit)
        .offset(offset)
    )
    tasks = result.scalars().all()

    return TaskListResponse(
        tasks=[
            TaskResponse(
                id=str(task.id),
                title=task.title,
                description=task.description,
                is_completed=task.is_completed,
                user_id=str(task.user_id),
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in tasks
        ],
        total=total,
        limit=limit,
        offset=offset
    )

async def get_task_by_id(
    db: AsyncSession,
    task_id: UUID,
    user: User
) -> TaskResponse:
    """
    Get a specific task by ID with ownership verification.

    Args:
        db: Database session
        task_id: Task UUID
        user: Authenticated user

    Returns:
        TaskResponse with task data

    Raises:
        HTTPException: 404 if task not found, 403 if not owned by user
    """
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if task is None:
        raise NotFoundException(detail="Task not found")

    if task.user_id != user.id:
        raise ForbiddenException(detail="Not authorized to access this task")

    return TaskResponse(
        id=str(task.id),
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        user_id=str(task.user_id),
        created_at=task.created_at,
        updated_at=task.updated_at
    )

async def update_task(
    db: AsyncSession,
    task_id: UUID,
    task_data: TaskUpdateRequest,
    user: User
) -> TaskResponse:
    """
    Update a task's title and description with ownership verification.

    Args:
        db: Database session
        task_id: Task UUID
        task_data: Update data
        user: Authenticated user

    Returns:
        TaskResponse with updated task data

    Raises:
        HTTPException: 404 if task not found, 403 if not owned by user
    """
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if task is None:
        raise NotFoundException(detail="Task not found")

    if task.user_id != user.id:
        raise ForbiddenException(detail="Not authorized to access this task")

    # Update fields
    task.title = task_data.title
    task.description = task_data.description
    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)

    return TaskResponse(
        id=str(task.id),
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        user_id=str(task.user_id),
        created_at=task.created_at,
        updated_at=task.updated_at
    )

async def toggle_completion(
    db: AsyncSession,
    task_id: UUID,
    completion_data: TaskCompletionRequest,
    user: User
) -> TaskResponse:
    """
    Toggle a task's completion status with ownership verification.

    Args:
        db: Database session
        task_id: Task UUID
        completion_data: Completion status data
        user: Authenticated user

    Returns:
        TaskResponse with updated task data

    Raises:
        HTTPException: 404 if task not found, 403 if not owned by user
    """
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if task is None:
        raise NotFoundException(detail="Task not found")

    if task.user_id != user.id:
        raise ForbiddenException(detail="Not authorized to access this task")

    # Update completion status - support both 'completed' and 'is_completed' field names
    completion_value = completion_data.completed if completion_data.completed is not None else completion_data.is_completed
    if completion_value is None:
        raise ValueError("Either 'completed' or 'is_completed' field is required")
    task.is_completed = completion_value
    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)

    return TaskResponse(
        id=str(task.id),
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        user_id=str(task.user_id),
        created_at=task.created_at,
        updated_at=task.updated_at
    )

async def delete_task(
    db: AsyncSession,
    task_id: UUID,
    user: User
) -> None:
    """
    Delete a task with ownership verification.

    Args:
        db: Database session
        task_id: Task UUID
        user: Authenticated user

    Raises:
        HTTPException: 404 if task not found, 403 if not owned by user
    """
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if task is None:
        raise NotFoundException(detail="Task not found")

    if task.user_id != user.id:
        raise ForbiddenException(detail="Not authorized to access this task")

    await db.delete(task)
    await db.commit()
