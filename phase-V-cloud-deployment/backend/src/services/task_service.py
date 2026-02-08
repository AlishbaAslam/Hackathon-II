"""
Task service logic for CRUD operations using event-driven architecture.
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy import func, update
from fastapi import HTTPException, status
from src.models.task import Task, TaskUpdate as TaskUpdateModel
from src.models.user import User
from src.core.exceptions import ForbiddenException, NotFoundException
from .event_publisher import (
    publish_task_created_event,
    publish_task_updated_event,
    publish_task_deleted_event,
    publish_task_completed_event
)

# Request/Response Schemas

class TaskCreateRequest(BaseModel):
    """Request schema for creating a task."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    due_date: Optional[datetime] = Field(None, alias="dueDate", description="Task due date in ISO format")
    priority: Optional[str] = None  # low, medium, high
    tags: Optional[str] = None  # comma-separated tags
    is_recurring: bool = Field(default=False, alias="isRecurring")
    recurrence_pattern: Optional[str] = Field(None, alias="recurrencePattern")  # daily, weekly, monthly, yearly
    remind_at: Optional[datetime] = Field(None, alias="remindAt")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class TaskUpdateRequest(BaseModel):
    """Request schema for updating a task."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    due_date: Optional[datetime] = Field(None, alias="dueDate", description="Task due date in ISO format")
    priority: Optional[str] = None  # low, medium, high
    tags: Optional[str] = None  # comma-separated tags
    is_recurring: Optional[bool] = Field(default=None, alias="isRecurring")
    recurrence_pattern: Optional[str] = Field(None, alias="recurrencePattern")  # daily, weekly, monthly, yearly
    remind_at: Optional[datetime] = Field(None, alias="remindAt")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class TaskCompletionRequest(BaseModel):
    """Request schema for toggling task completion."""
    # Accept both 'completed' and 'is_completed' field names
    completed: Optional[bool] = Field(default=None, alias="completed")
    is_completed: Optional[bool] = Field(default=None, alias="is_completed")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class TaskResponse(BaseModel):
    """Response schema for task data."""
    id: str
    title: str
    description: Optional[str]
    is_completed: bool
    user_id: str
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    tags: Optional[str] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None
    remind_at: Optional[datetime] = None
    parent_task_id: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

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
    print("Full request body:", task_data.dict())  # Enhanced debug
    print("Due date raw from request:", task_data.due_date)  # Debug
    print("Due date raw type from request:", type(task_data.due_date))  # Debug

    if task_data.due_date is None:
        print("WARNING: due_date is None in request - check frontend payload")  # Debug

    # Handle potential datetime parsing if needed
    due_date_value = task_data.due_date
    if due_date_value is not None:
        print("Processing due_date value:", due_date_value)  # Debug
        if isinstance(due_date_value, str):
            try:
                # Parse ISO format datetime string
                import re
                # Check if it's an ISO format string
                if re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', due_date_value):
                    # Parse the datetime string and make it timezone-aware if needed
                    parsed_date = datetime.fromisoformat(due_date_value.replace('Z', '+00:00'))
                    due_date_value = parsed_date
                    print("Successfully parsed datetime string:", due_date_value)  # Debug
                else:
                    print("Date string doesn't match ISO format, keeping as is")  # Debug
            except Exception as e:
                print(f"Datetime parse error: {e}")  # Debug
                due_date_value = None
        else:
            print("due_date is already a datetime object, using as is")  # Debug
    else:
        print("due_date is None, setting to None")  # Debug

    print("Setting new_task.due_date to:", due_date_value)  # Debug
    print("Received remind_at:", task_data.remind_at)  # Debug
    print("Received is_recurring:", task_data.is_recurring)  # Debug
    print("Received recurrence_pattern:", task_data.recurrence_pattern)  # Debug
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        user_id=user.id,
        due_date=due_date_value,
        priority=task_data.priority,
        tags=task_data.tags,
        is_recurring=task_data.is_recurring,
        recurrence_pattern=task_data.recurrence_pattern,
        remind_at=task_data.remind_at
    )

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    print("Saved task ID:", new_task.id, "due_date:", new_task.due_date)  # Debug

    # Publish event for the new task
    await publish_task_created_event(
        user_id=user.id,
        task_id=new_task.id,
        task_data={
            "title": new_task.title,
            "description": new_task.description,
            "due_date": new_task.due_date.isoformat() if new_task.due_date else None,
            "priority": new_task.priority,
            "tags": new_task.tags,
            "is_recurring": new_task.is_recurring,
            "recurrence_pattern": new_task.recurrence_pattern,
            "remind_at": new_task.remind_at.isoformat() if new_task.remind_at else None
        }
    )

    print("Creating TaskResponse with due_date:", new_task.due_date)  # Debug
    return TaskResponse(
        id=str(new_task.id),
        title=new_task.title,
        description=new_task.description,
        is_completed=new_task.is_completed,
        user_id=str(new_task.user_id),
        created_at=new_task.created_at,
        updated_at=new_task.updated_at,
        due_date=new_task.due_date,
        priority=new_task.priority,
        tags=new_task.tags,
        is_recurring=new_task.is_recurring,
        recurrence_pattern=new_task.recurrence_pattern,
        remind_at=new_task.remind_at,
        parent_task_id=str(new_task.parent_task_id) if new_task.parent_task_id else None
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

    # Add debug for due dates in retrieved tasks
    for task in tasks:
        print(f"Task {task.id} due_date: {task.due_date}")  # Debug

    return TaskListResponse(
        tasks=[
            TaskResponse(
                id=str(task.id),
                title=task.title,
                description=task.description,
                is_completed=task.is_completed,
                user_id=str(task.user_id),
                created_at=task.created_at,
                updated_at=task.updated_at,
                due_date=task.due_date,
                priority=task.priority,
                tags=task.tags,
                is_recurring=task.is_recurring,
                recurrence_pattern=task.recurrence_pattern,
                remind_at=task.remind_at,
                parent_task_id=str(task.parent_task_id) if task.parent_task_id else None
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

    print(f"Getting single task {task.id} due_date: {task.due_date}")  # Debug
    return TaskResponse(
        id=str(task.id),
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        user_id=str(task.user_id),
        created_at=task.created_at,
        updated_at=task.updated_at,
        due_date=task.due_date,
        priority=task.priority,
        tags=task.tags,
        is_recurring=task.is_recurring,
        recurrence_pattern=task.recurrence_pattern,
        remind_at=task.remind_at,
        parent_task_id=str(task.parent_task_id) if task.parent_task_id else None
    )

async def update_task(
    db: AsyncSession,
    task_id: UUID,
    task_data: TaskUpdateRequest,
    user: User
) -> TaskResponse:
    """
    Update a task's fields with ownership verification.

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

    # Update fields based on provided data
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.due_date is not None:
        print("Full update request body:", task_data.dict())  # Enhanced debug
        print("Updating due_date:", task_data.due_date)  # Debug
        print("Updating due_date type:", type(task_data.due_date))  # Debug

        # Handle potential datetime parsing if needed
        due_date_value = task_data.due_date
        if due_date_value is not None:
            print("Processing due_date value for update:", due_date_value)  # Debug
            if isinstance(due_date_value, str):
                try:
                    # Parse ISO format datetime string
                    import re
                    # Check if it's an ISO format string
                    if re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', due_date_value):
                        # Parse the datetime string and make it timezone-aware if needed
                        parsed_date = datetime.fromisoformat(due_date_value.replace('Z', '+00:00'))
                        due_date_value = parsed_date
                        print("Successfully parsed datetime string for update:", due_date_value)  # Debug
                    else:
                        print("Date string doesn't match ISO format for update, keeping as is")  # Debug
                except Exception as e:
                    print(f"Error parsing due_date for update: {e}")  # Debug
                    due_date_value = None
            else:
                print("due_date is already a datetime object for update, using as is")  # Debug
        else:
            print("due_date is None for update, setting to None")  # Debug
        task.due_date = due_date_value
    if task_data.priority is not None:
        task.priority = task_data.priority
    if task_data.tags is not None:
        task.tags = task_data.tags
    if task_data.is_recurring is not None:
        print("Updating is_recurring:", task_data.is_recurring)  # Debug
        task.is_recurring = task_data.is_recurring
    if task_data.recurrence_pattern is not None:
        print("Updating recurrence_pattern:", task_data.recurrence_pattern)  # Debug
        task.recurrence_pattern = task_data.recurrence_pattern
    if task_data.remind_at is not None:
        print("Updating remind_at:", task_data.remind_at)  # Debug
        task.remind_at = task_data.remind_at

    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)

    # Prepare the updated fields for the event
    updated_fields = {}
    for field in ['title', 'description', 'due_date', 'priority', 'tags', 'is_recurring', 'recurrence_pattern', 'remind_at']:
        if getattr(task_data, field) is not None:
            value = getattr(task, field)
            if hasattr(value, 'isoformat'):  # datetime objects
                updated_fields[field] = value.isoformat()
            else:
                updated_fields[field] = value

    # Publish event for the updated task
    await publish_task_updated_event(
        user_id=user.id,
        task_id=task.id,
        updated_fields=updated_fields
    )

    return TaskResponse(
        id=str(task.id),
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        user_id=str(task.user_id),
        created_at=task.created_at,
        updated_at=task.updated_at,
        due_date=task.due_date,
        priority=task.priority,
        tags=task.tags,
        is_recurring=task.is_recurring,
        recurrence_pattern=task.recurrence_pattern,
        remind_at=task.remind_at,
        parent_task_id=str(task.parent_task_id) if task.parent_task_id else None
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
    print("Task updated at:", task.updated_at)

    await db.commit()
    await db.refresh(task)

    # Publish event for the task completion
    await publish_task_completed_event(
        user_id=user.id,
        task_id=task.id,
        completion_data={
            "is_completed": task.is_completed,
            "completed_at": task.updated_at.isoformat()
        }
    )

    # If this is a recurring task and it was just completed, publish event to create next occurrence
    if task.is_recurring and task.is_completed and task.recurrence_pattern:
        print(f"[RECURRING] ========== RECURRING TASK COMPLETION ==========")
        print(f"[RECURRING] Task {task.id} is recurring and completed")
        print(f"[RECURRING] Recurrence pattern: {task.recurrence_pattern}")
        print(f"[RECURRING] Publishing event to task-events topic")

        try:
            # Import dapr_client here to avoid circular imports
            from src.core.dapr_client import dapr_client
            from src.core.event_schemas import TaskEvent, TaskEventType
            from uuid import uuid4

            # Prepare the event with correct event_type enum value
            # The enum TaskEventType.TASK_COMPLETED has value "task.completed"
            event = TaskEvent(
                event_id=str(uuid4()),
                event_type=TaskEventType.TASK_COMPLETED,  # This will be "task.completed"
                user_id=task.user_id,  # UUID - will be converted to string in dapr_client
                task_id=task.id,  # UUID - will be converted to string in dapr_client
                timestamp=datetime.utcnow(),
                payload={
                    "recurrence_pattern": task.recurrence_pattern,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "title": task.title,
                    "description": task.description,
                    "priority": task.priority,
                    "tags": task.tags,
                    "remind_at": task.remind_at.isoformat() if task.remind_at else None
                }
            )

            print(f"[RECURRING] Event created with type: {event.event_type} (value: {event.event_type.value})")
            print(f"[RECURRING] Event payload keys: {list(event.payload.keys())}")

            # Use the improved DaprClient with retry logic and dynamic port detection
            print(f"[RECURRING] Attempting to publish event...")
            success = await dapr_client.publish_event("task-events", event)

            if success:
                print(f"[RECURRING] ✓ Successfully published completed event for recurring task {task.id}")
                print(f"[RECURRING] Next occurrence will be created by the consumer")
            else:
                # Fallback: Log warning but don't crash the response
                print(f"[RECURRING] ⚠ WARNING: Failed to publish completed event for recurring task {task.id}")
                print(f"[RECURRING] ⚠ Next occurrence will NOT be created automatically")
                print(f"[RECURRING] ⚠ Task completion succeeded, but event publishing failed")
                print(f"[RECURRING] ⚠ Check Dapr sidecar is running and components are loaded")

        except Exception as e:
            # Fallback: Don't crash the response if event publishing fails
            print(f"[RECURRING] ⚠ ERROR: Exception while publishing completed event for recurring task {task.id}")
            print(f"[RECURRING] ⚠ Error: {str(e)}")
            print(f"[RECURRING] ⚠ Task completion succeeded, but next occurrence will NOT be created automatically")
            import traceback
            traceback.print_exc()

        print(f"[RECURRING] ==================================================")

    print("Returning task with due_date:", task.due_date)  # Debug
    return TaskResponse(
        id=str(task.id),
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        user_id=str(task.user_id),
        created_at=task.created_at,
        updated_at=task.updated_at,
        due_date=task.due_date,
        priority=task.priority,
        tags=task.tags,
        is_recurring=task.is_recurring,
        recurrence_pattern=task.recurrence_pattern,
        remind_at=task.remind_at,
        parent_task_id=str(task.parent_task_id) if task.parent_task_id else None
    )

async def delete_task(
    db: AsyncSession,
    task_id: UUID,
    user: User
) -> None:
    """
    Delete a task with ownership verification.
    Clears parent_task_id references in child tasks before deletion.

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

    # Clear parent_task_id references in child tasks to avoid foreign key constraint violation
    await db.execute(
        update(Task)
        .where(Task.parent_task_id == task_id)
        .values(parent_task_id=None)
    )
    print(f"Cleared parent references for task {task_id} before delete")

    # Publish event before deleting the task
    await publish_task_deleted_event(
        user_id=user.id,
        task_id=task.id,
        deletion_reason="Task deleted by user"
    )

    await db.delete(task)
    await db.commit()
