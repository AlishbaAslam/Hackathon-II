"""
Event log entity model for audit trail.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
from enum import Enum


class EventTypeEnum(str, Enum):
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"
    TASK_COMPLETED = "task_completed"
    TASK_RECURRING_GENERATED = "task_recurring_generated"
    TASK_REMINDER_SCHEDULED = "task_reminder_scheduled"


class EventLog(SQLModel, table=True):
    """
    Event log entity representing audit trail of all task operations.

    Attributes:
        id: Unique event identifier (UUID)
        user_id: ID of the user who initiated the event
        task_id: ID of the task involved in the event (if applicable)
        event_type: Type of event (task_created, task_updated, etc.)
        event_data: Additional data about the event in JSON format
        created_at: Timestamp when the event occurred
    """
    __tablename__ = "event_logs"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(nullable=False, index=True)
    task_id: Optional[UUID] = Field(default=None, nullable=True, index=True)
    event_type: EventTypeEnum = Field(nullable=False)
    event_data: Optional[str] = Field(default=None, max_length=2000, nullable=True)  # JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)