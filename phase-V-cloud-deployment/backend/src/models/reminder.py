"""
Reminder entity model for notification scheduling.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
from enum import Enum


class ReminderStatusEnum(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    CANCELLED = "cancelled"
    FAILED = "failed"


class ReminderChannelEnum(str, Enum):
    EMAIL = "email"
    PUSH = "push"
    SMS = "sms"
    WEBHOOK = "webhook"


class Reminder(SQLModel, table=True):
    """
    Reminder entity representing scheduled notifications for tasks.

    Attributes:
        id: Unique reminder identifier (UUID)
        task_id: ID of the task this reminder is for
        user_id: ID of the user who owns the task
        scheduled_time: When the reminder should be sent
        channel: How the reminder should be delivered (email, push, etc.)
        status: Current status of the reminder (pending, sent, cancelled, failed)
        message: Custom message for the reminder
        created_at: Timestamp when the reminder was created
        updated_at: Timestamp when the reminder was last updated
    """
    __tablename__ = "reminders"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    task_id: UUID = Field(foreign_key="tasks.id", nullable=False, index=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    scheduled_time: datetime = Field(nullable=False)
    channel: ReminderChannelEnum = Field(default=ReminderChannelEnum.PUSH, nullable=False)
    status: ReminderStatusEnum = Field(default=ReminderStatusEnum.PENDING, nullable=False)
    message: Optional[str] = Field(default=None, max_length=500, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)