"""
Async Task service logic for CRUD operations that can be used by the agent service.
"""
from datetime import datetime
from typing import Optional, List
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.task import Task, TaskUpdate
from ..models.user import User


async def create_task_async(db: AsyncSession, user_id: str, title: str, description: str = "", is_completed: bool = False) -> Task:
    """
    Create a new task asynchronously.

    Args:
        db: Async database session
        user_id: ID of the user creating the task
        title: Title of the task
        description: Description of the task (optional)
        is_completed: Whether the task is completed (default: False)

    Returns:
        Created Task object
    """
    from uuid import UUID

    # Convert string user_id to UUID for database insertion
    user_uuid = UUID(user_id) if isinstance(user_id, str) and user_id else user_id

    new_task = Task(
        title=title,
        description=description or "",
        user_id=user_uuid,
        is_completed=is_completed
    )

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    return new_task


async def get_tasks_async(db: AsyncSession, user_id: str, completed: Optional[bool] = None) -> List[Task]:
    """
    Get tasks for a specific user with optional filtering asynchronously.

    Args:
        db: Async database session
        user_id: ID of the user whose tasks to retrieve
        completed: Filter by completion status (None for all, True for completed, False for pending)

    Returns:
        List of Task objects
    """
    from uuid import UUID

    # Convert string user_id to UUID for database query
    user_uuid = UUID(user_id) if isinstance(user_id, str) and user_id else user_id

    statement = select(Task).where(Task.user_id == user_uuid)

    if completed is not None:
        statement = statement.where(Task.is_completed == completed)

    result = await db.execute(statement)
    tasks = result.scalars().all()
    return tasks


async def get_task_by_id_async(db: AsyncSession, task_id: str, user_id: str) -> Optional[Task]:
    """
    Get a specific task by ID for a specific user asynchronously.

    Args:
        db: Async database session
        task_id: ID of the task to retrieve
        user_id: ID of the user who owns the task

    Returns:
        Task object if found and owned by user, None otherwise
    """
    # Convert user_id to UUID for database query
    from uuid import UUID
    user_uuid = UUID(user_id) if isinstance(user_id, str) and user_id else user_id

    # Check if task_id is a valid UUID format before converting
    try:
        task_uuid = UUID(task_id) if isinstance(task_id, str) and task_id else task_id
    except ValueError:
        # If task_id is not a valid UUID, return None
        return None

    statement = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
    result = await db.execute(statement)
    task = result.scalar_one_or_none()
    return task


async def update_task_async(db: AsyncSession, task: Task, task_update: TaskUpdate) -> Task:
    """
    Update a task with provided data asynchronously.

    Args:
        db: Async database session
        task: Task object to update
        task_update: Update data

    Returns:
        Updated Task object
    """
    # Use Pydantic model_dump to safely extract update data
    try:
        update_data = task_update.model_dump(exclude_unset=True)
    except AttributeError:
        # Fallback for older Pydantic versions
        update_data = task_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        if hasattr(task, field):
            setattr(task, field, value)

    task.updated_at = datetime.utcnow()

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return task


async def delete_task_async(db: AsyncSession, task: Task) -> Task:
    """
    Delete a task from the database asynchronously.

    Args:
        db: Async database session
        task: Task object to delete

    Returns:
        Deleted Task object
    """
    await db.delete(task)
    await db.commit()

    return task