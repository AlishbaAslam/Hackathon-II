"""
Synchronous Task service logic for CRUD operations.
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException, status
from src.models.task import Task, TaskUpdate
from src.models.user import User
from src.core.exceptions import ForbiddenException, NotFoundException


def create_task(session: Session, task_create) -> Task:
    """
    Create a new task in the database.

    Args:
        session: Database session
        task_create: Task creation data

    Returns:
        Created Task object
    """
    from uuid import UUID

    # Convert string user_id to UUID for database insertion
    user_uuid = UUID(task_create.user_id) if isinstance(task_create.user_id, str) and task_create.user_id else task_create.user_id

    new_task = Task(
        title=task_create.title,
        description=task_create.description or "",
        user_id=user_uuid,
        is_completed=task_create.completed or False
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task


def get_tasks(session: Session, user_id: str, completed: Optional[bool] = None, offset: int = 0, limit: int = 100) -> List[Task]:
    """
    Get tasks for a specific user with optional filtering.

    Args:
        session: Database session
        user_id: ID of the user whose tasks to retrieve
        completed: Filter by completion status (None for all, True for completed, False for pending)
        offset: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of Task objects
    """
    from uuid import UUID

    # Convert string user_id to UUID for database query
    user_uuid = UUID(user_id) if isinstance(user_id, str) and user_id else user_id

    statement = select(Task).where(Task.user_id == user_uuid)

    if completed is not None:
        statement = statement.where(Task.is_completed == completed)

    statement = statement.offset(offset).limit(limit)

    tasks = session.exec(statement).all()
    return tasks


def get_task_by_id(session: Session, task_id: str, user_id: str) -> Optional[Task]:
    """
    Get a specific task by ID for a specific user.

    Args:
        session: Database session
        task_id: ID of the task to retrieve
        user_id: ID of the user who owns the task

    Returns:
        Task object if found and owned by user, None otherwise
    """
    from uuid import UUID

    # Convert string user_id and task_id to UUIDs for database query
    user_uuid = UUID(user_id) if isinstance(user_id, str) and user_id else user_id
    task_uuid = UUID(task_id) if isinstance(task_id, str) and task_id else task_id

    statement = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
    result = session.execute(statement)
    task = result.scalar_one_or_none()
    return task


def update_task(session: Session, task: Task, task_update: TaskUpdate) -> Task:
    """
    Update a task with provided data.

    Args:
        session: Database session
        task: Task object to update
        task_update: Update data

    Returns:
        Updated Task object
    """
    update_data = task_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def delete_task(session: Session, task: Task) -> Task:
    """
    Delete a task from the database.

    Args:
        session: Database session
        task: Task object to delete

    Returns:
        Deleted Task object
    """
    session.delete(task)
    session.commit()

    return task