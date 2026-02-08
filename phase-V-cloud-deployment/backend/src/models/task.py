"""
Task entity model.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum

class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RecurrencePatternEnum(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class Task(SQLModel, table=True):
    """
    Task entity representing a todo item owned by a user.

    Attributes:
        id: Unique task identifier (UUID)
        title: Task title (required, max 200 characters)
        description: Optional task description (max 2000 characters)
        is_completed: Task completion status (default: False)
        user_id: Owner user ID (foreign key to users table)
        created_at: Task creation timestamp
        updated_at: Last update timestamp
        due_date: Optional due date for the task
        priority: Task priority level (low, medium, high)
        tags: Comma-separated tags for the task
        is_recurring: Whether the task is recurring (default: False)
        recurrence_pattern: How often the task recurs (daily, weekly, monthly, yearly)
        remind_at: Time to send reminder (optional)
        parent_task_id: For recurring tasks, the ID of the parent task that generated this instance
        owner: Relationship to the owning user (many-to-one)
    """
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=2000, nullable=True)
    is_completed: bool = Field(default=False, nullable=False)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # New fields for advanced features
    due_date: Optional[datetime] = Field(default=None, nullable=True)
    priority: Optional[PriorityEnum] = Field(default=None, nullable=True)
    tags: Optional[str] = Field(default=None, max_length=500, nullable=True)  # Comma-separated tags
    is_recurring: bool = Field(default=False, nullable=False)
    recurrence_pattern: Optional[RecurrencePatternEnum] = Field(default=None, nullable=True)
    remind_at: Optional[datetime] = Field(default=None, nullable=True)
    parent_task_id: Optional[UUID] = Field(default=None, foreign_key="tasks.id", nullable=True)

    # Relationship (not a database column)
    owner: Optional["User"] = Relationship(back_populates="tasks")


class TaskUpdate(SQLModel):
    """
    Task update model for partial updates to task fields.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[PriorityEnum] = None
    tags: Optional[str] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[RecurrencePatternEnum] = None
    remind_at: Optional[datetime] = None
