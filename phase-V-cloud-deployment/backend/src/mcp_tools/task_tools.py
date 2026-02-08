"""MCP Tools for Task Management

This module implements MCP tools for task management operations that can be used by AI agents.
All operations enforce user isolation via user_id validation from JWT.
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Literal
from sqlmodel import Session, select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.task import Task, TaskUpdate
from ..models.user import User
from ..services.task_service_sync import (
    create_task,
    get_tasks,
    get_task_by_id,
    update_task as service_update_task,
    delete_task as service_delete_task
)
from ..services.task_service_async import (
    create_task_async,
    get_tasks_async,
    get_task_by_id_async,
    update_task_async,
    delete_task_async
)


def add_task(user_id: str, title: str, description: Optional[str] = None) -> Dict:
    """
    Create a new task with user_id, title (required), description (optional).

    Args:
        user_id: ID of the user creating the task
        title: Title of the task (required)
        description: Description of the task (optional)

    Returns:
        Dictionary containing task_id, status, and title
    """
    from ..core.database import get_session

    with get_session() as session:
        # Verify user exists
        user = session.get(User, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Prepare task data using the Task model
        task_create = Task(
            user_id=user_id,
            title=title,
            description=description or "",
            is_completed=False
        )

        # Create the task
        task = create_task(session=session, task_create=task_create)

        return {
            "task_id": task.id,
            "status": "success",
            "title": task.title
        }


def list_tasks(user_id: str, status: Optional[Literal["all", "pending", "completed"]] = "all") -> List[Dict]:
    """
    Retrieve tasks with optional status filter (all, pending, completed).

    Args:
        user_id: ID of the user whose tasks to retrieve
        status: Filter status - "all", "pending", or "completed" (default: "all")

    Returns:
        List of task objects with id, title, description, and completed status
    """
    from ..core.database import get_session

    with get_session() as session:
        # Verify user exists
        user = session.get(User, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Prepare filters based on status
        filters = {"user_id": user_id}
        if status and status != "all":
            if status == "pending":
                filters["completed"] = False
            elif status == "completed":
                filters["completed"] = True

        # Get tasks with filters
        tasks = get_tasks(
            session=session,
            user_id=user_id,
            completed=filters.get("completed"),
            offset=0,
            limit=100  # Reasonable limit for AI consumption
        )

        # Convert tasks to dictionary format
        result = []
        for task in tasks:
            result.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            })

        return result


def complete_task(user_id: str, task_id: int) -> Dict:
    """
    Mark a task as complete using user_id and task_id.

    Args:
        user_id: ID of the user who owns the task
        task_id: ID of the task to mark as complete

    Returns:
        Dictionary containing task_id, status, and title
    """
    from ..core.database import get_session

    with get_session() as session:
        # Verify user exists
        user = session.get(User, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Get the task and verify it belongs to the user
        task = get_task_by_id(session=session, task_id=task_id, user_id=user_id)
        if not task:
            raise ValueError(f"Task {task_id} not found for user {user_id}")

        # Update task to completed
        update_data = TaskUpdate(completed=True)
        updated_task = service_update_task(session=session, task=task, task_update=update_data)

        return {
            "task_id": updated_task.id,
            "status": "completed",
            "title": updated_task.title
        }


def delete_task(user_id: str, task_id: int) -> Dict:
    """
    Remove a task using user_id and task_id.

    Args:
        user_id: ID of the user who owns the task
        task_id: ID of the task to delete

    Returns:
        Dictionary containing task_id, status, and title
    """
    from ..core.database import get_session

    with get_session() as session:
        # Verify user exists
        user = session.get(User, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Get the task and verify it belongs to the user
        task = get_task_by_id(session=session, task_id=task_id, user_id=user_id)
        if not task:
            raise ValueError(f"Task {task_id} not found for user {user_id}")

        # Delete the task
        deleted_task = service_delete_task(session=session, task=task)

        return {
            "task_id": deleted_task.id,
            "status": "deleted",
            "title": deleted_task.title
        }


def update_task(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Dict:
    """
    Modify task title or description using user_id, task_id, and optional new values.

    Args:
        user_id: ID of the user who owns the task
        task_id: ID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)

    Returns:
        Dictionary containing task_id, status, and title
    """
    from ..core.database import get_session

    with get_session() as session:
        # Verify user exists
        user = session.get(User, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Get the task and verify it belongs to the user
        task = get_task_by_id(session=session, task_id=task_id, user_id=user_id)
        if not task:
            raise ValueError(f"Task {task_id} not found for user {user_id}")

        # Prepare update data
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description

        # Only update if there are changes
        if not update_data:
            return {
                "task_id": task.id,
                "status": "no_changes",
                "title": task.title
            }

        # Update the task
        task_update = TaskUpdate(**update_data)
        updated_task = service_update_task(session=session, task=task, task_update=task_update)

        return {
            "task_id": updated_task.id,
            "status": "updated",
            "title": updated_task.title
        }


# Async versions of the tools for use with async sessions to prevent greenlet_spawn errors
async def add_task_async(user_id: str, title: str, session: AsyncSession, description: Optional[str] = None) -> Dict:
    """
    Create a new task with user_id, title (required), description (optional) - async version.

    Args:
        user_id: ID of the user creating the task
        title: Title of the task (required)
        session: Async database session
        description: Description of the task (optional)

    Returns:
        Dictionary containing task_id, status, and title
    """
    # Verify user exists
    from uuid import UUID
    user_uuid = UUID(user_id) if isinstance(user_id, str) and user_id else user_id

    user_result = await session.execute(select(User).where(User.id == user_uuid))
    user = user_result.scalar_one_or_none()
    if not user:
        raise ValueError(f"User {user_id} not found")

    # Create the task using async service
    task = await create_task_async(
        db=session,
        user_id=user_id,
        title=title,
        description=description or "",
        is_completed=False
    )

    return {
        "task_id": task.id,
        "status": "success",
        "title": task.title
    }


async def list_tasks_async(user_id: str, session: AsyncSession, status: Optional[Literal["all", "pending", "completed"]] = "all") -> List[Dict]:
    """
    Retrieve tasks with optional status filter (all, pending, completed) - async version.

    Args:
        user_id: ID of the user whose tasks to retrieve
        session: Async database session
        status: Filter status - "all", "pending", or "completed" (default: "all")

    Returns:
        List of task objects with short_id (1-based index), id, title, description, and completed status
    """
    # Verify user exists
    from uuid import UUID
    user_uuid = UUID(user_id) if isinstance(user_id, str) and user_id else user_id

    user_result = await session.execute(select(User).where(User.id == user_uuid))
    user = user_result.scalar_one_or_none()
    if not user:
        raise ValueError(f"User {user_id} not found")

    # Determine completion filter based on status
    completed_filter = None
    if status and status != "all":
        if status == "pending":
            completed_filter = False
        elif status == "completed":
            completed_filter = True

    # Get tasks with filters using async service
    tasks = await get_tasks_async(
        db=session,
        user_id=user_id,
        completed=completed_filter
    )

    # Convert tasks to dictionary format with short_id (1-based index)
    result = []
    for index, task in enumerate(tasks, start=1):
        result.append({
            "short_id": index,
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.is_completed
        })

    return result


async def complete_task_async(user_id: str, task_id: str, session: AsyncSession) -> Dict:
    """
    Mark a task as complete using user_id and task_id - async version.
    Supports both short_id (int) and full UUID (str).

    Args:
        user_id: ID of the user who owns the task
        task_id: ID of the task to mark as complete (either short_id or full UUID)
        session: Async database session

    Returns:
        Dictionary containing task_id, status, and title
    """
    # Verify user exists
    from uuid import UUID
    user_uuid = UUID(user_id) if isinstance(user_id, str) and user_id else user_id

    user_result = await session.execute(select(User).where(User.id == user_uuid))
    user = user_result.scalar_one_or_none()
    if not user:
        raise ValueError(f"User {user_id} not found")

    # Check if task_id is a numeric short_id or a UUID
    import re
    uuid_pattern = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'

    # If task_id matches UUID pattern, treat as UUID
    if re.match(uuid_pattern, task_id.lower()):
        # Direct lookup by UUID
        try:
            UUID(task_id)
            task = await get_task_by_id_async(db=session, task_id=task_id, user_id=user_id)
        except ValueError:
            task = None
    else:
        # Otherwise, treat as short_id (index)
        try:
            short_id = int(task_id)
            if short_id < 1:
                raise ValueError(f"Invalid short_id: {short_id}")

            # Get all user's tasks to find the one at the specified index
            all_tasks_result = await session.execute(
                select(Task).where(Task.user_id == user_uuid).order_by(Task.created_at)
            )
            all_tasks = all_tasks_result.scalars().all()

            if short_id > len(all_tasks):
                raise ValueError(f"Short ID {short_id} is out of range. User has {len(all_tasks)} tasks.")

            task = all_tasks[short_id - 1]  # Convert to 0-based index
        except ValueError:
            # If it's not a valid integer, it's neither a valid UUID nor a short_id
            raise ValueError(f"Invalid task identifier: {task_id}. Must be a valid UUID or a numeric short_id.")

    if not task:
        raise ValueError(f"Task {task_id} not found for user {user_id}")

    # Update task to completed by directly modifying the task object
    task.is_completed = True
    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)

    updated_task = task

    return {
        "task_id": str(updated_task.id),
        "status": "completed",
        "title": updated_task.title
    }


async def delete_task_async(user_id: str, task_id: str, session: AsyncSession) -> Dict:
    """
    Remove a task using user_id and task_id - async version.
    Supports both short_id (int) and full UUID (str).

    Args:
        user_id: ID of the user who owns the task
        task_id: ID of the task to delete (either short_id or full UUID)
        session: Async database session

    Returns:
        Dictionary containing task_id, status, and title
    """
    # Verify user exists
    from uuid import UUID
    user_uuid = UUID(user_id) if isinstance(user_id, str) and user_id else user_id

    user_result = await session.execute(select(User).where(User.id == user_uuid))
    user = user_result.scalar_one_or_none()
    if not user:
        raise ValueError(f"User {user_id} not found")

    # Check if task_id is a numeric short_id or a UUID
    import re
    uuid_pattern = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'

    # If task_id matches UUID pattern, treat as UUID
    if re.match(uuid_pattern, task_id.lower()):
        # Direct lookup by UUID
        try:
            UUID(task_id)
            task = await get_task_by_id_async(db=session, task_id=task_id, user_id=user_id)
        except ValueError:
            task = None
    else:
        # Otherwise, treat as short_id (index)
        try:
            short_id = int(task_id)
            if short_id < 1:
                raise ValueError(f"Invalid short_id: {short_id}")

            # Get all user's tasks to find the one at the specified index
            all_tasks_result = await session.execute(
                select(Task).where(Task.user_id == user_uuid).order_by(Task.created_at)
            )
            all_tasks = all_tasks_result.scalars().all()

            if short_id > len(all_tasks):
                raise ValueError(f"Short ID {short_id} is out of range. User has {len(all_tasks)} tasks.")

            task = all_tasks[short_id - 1]  # Convert to 0-based index
        except ValueError:
            # If it's not a valid integer, it's neither a valid UUID nor a short_id
            raise ValueError(f"Invalid task identifier: {task_id}. Must be a valid UUID or a numeric short_id.")

    if not task:
        raise ValueError(f"Task {task_id} not found for user {user_id}")

    # Delete the task directly using the session
    await session.delete(task)
    await session.commit()

    deleted_task = task

    return {
        "task_id": str(deleted_task.id),
        "status": "deleted",
        "title": deleted_task.title
    }


async def update_task_async(user_id: str, task_id: str, session: AsyncSession, title: Optional[str] = None, description: Optional[str] = None) -> Dict:
    """
    Modify task title or description using user_id, task_id, and optional new values - async version.
    Supports both short_id (int) and full UUID (str).

    Args:
        user_id: ID of the user who owns the task
        task_id: ID of the task to update (either short_id or full UUID)
        session: Async database session
        title: New title for the task (optional)
        description: New description for the task (optional)

    Returns:
        Dictionary containing task_id, status, and title
    """
    # Verify user exists
    from uuid import UUID
    user_uuid = UUID(user_id) if isinstance(user_id, str) and user_id else user_id

    user_result = await session.execute(select(User).where(User.id == user_uuid))
    user = user_result.scalar_one_or_none()
    if not user:
        raise ValueError(f"User {user_id} not found")

    # Check if task_id is a numeric short_id or a UUID
    import re
    uuid_pattern = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'

    # If task_id matches UUID pattern, treat as UUID
    if re.match(uuid_pattern, task_id.lower()):
        # Direct lookup by UUID
        try:
            UUID(task_id)
            task = await get_task_by_id_async(db=session, task_id=task_id, user_id=user_id)
        except ValueError:
            task = None
    else:
        # Otherwise, treat as short_id (index)
        try:
            short_id = int(task_id)
            if short_id < 1:
                raise ValueError(f"Invalid short_id: {short_id}")

            # Get all user's tasks to find the one at the specified index
            all_tasks_result = await session.execute(
                select(Task).where(Task.user_id == user_uuid).order_by(Task.created_at)
            )
            all_tasks = all_tasks_result.scalars().all()

            if short_id > len(all_tasks):
                raise ValueError(f"Short ID {short_id} is out of range. User has {len(all_tasks)} tasks.")

            task = all_tasks[short_id - 1]  # Convert to 0-based index
        except ValueError:
            # If it's not a valid integer, it's neither a valid UUID nor a short_id
            raise ValueError(f"Invalid task identifier: {task_id}. Must be a valid UUID or a numeric short_id.")

    if not task:
        raise ValueError(f"Task {task_id} not found for user {user_id}")

    # Prepare update data
    update_data = {}
    if title is not None:
        update_data["title"] = title
    if description is not None:
        update_data["description"] = description

    # Only update if there are changes
    if not update_data:
        return {
            "task_id": str(task.id),
            "status": "no_changes",
            "title": task.title
        }

    # Update the task by directly modifying the task object
    if "title" in update_data:
        task.title = update_data["title"]
    if "description" in update_data:
        task.description = update_data["description"]

    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)

    updated_task = task

    return {
        "task_id": str(updated_task.id),
        "status": "updated",
        "title": updated_task.title
    }