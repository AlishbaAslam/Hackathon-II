"""
Kafka topic schemas and event definitions for the event-driven architecture.
"""
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel


class TaskEventType(str, Enum):
    TASK_CREATED = "task.created"
    TASK_UPDATED = "task.updated"
    TASK_DELETED = "task.deleted"
    TASK_COMPLETED = "task.completed"
    TASK_RECURRING_GENERATED = "task.recurring.generated"
    TASK_REMINDER_SCHEDULED = "task.reminder.scheduled"


class TaskEvent(BaseModel):
    """Base event schema for task-related events."""
    event_id: str
    event_type: TaskEventType
    user_id: UUID
    task_id: UUID
    timestamp: datetime
    payload: Dict[str, Any]
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None


class TaskCreatedEvent(TaskEvent):
    """Event emitted when a new task is created."""
    event_type: TaskEventType = TaskEventType.TASK_CREATED
    payload: Dict[str, Any]  # Contains task data


class TaskUpdatedEvent(TaskEvent):
    """Event emitted when a task is updated."""
    event_type: TaskEventType = TaskEventType.TASK_UPDATED
    payload: Dict[str, Any]  # Contains updated fields


class TaskDeletedEvent(TaskEvent):
    """Event emitted when a task is deleted."""
    event_type: TaskEventType = TaskEventType.TASK_DELETED
    payload: Dict[str, Any]  # May contain task metadata before deletion


class TaskCompletedEvent(TaskEvent):
    """Event emitted when a task is marked as completed."""
    event_type: TaskEventType = TaskEventType.TASK_COMPLETED
    payload: Dict[str, Any]  # Contains completion data


class TaskRecurringGeneratedEvent(TaskEvent):
    """Event emitted when a recurring task generates the next occurrence."""
    event_type: TaskEventType = TaskEventType.TASK_RECURRING_GENERATED
    payload: Dict[str, Any]  # Contains parent task ID and new task data


class TaskReminderScheduledEvent(TaskEvent):
    """Event emitted when a reminder is scheduled for a task."""
    event_type: TaskEventType = TaskEventType.TASK_REMINDER_SCHEDULED
    payload: Dict[str, Any]  # Contains reminder details


class KafkaTopics:
    """Constants for Kafka topic names."""
    TASK_EVENTS = "task-events"
    REMINDERS = "reminders"
    TASK_UPDATES = "task-updates"
    AUDIT_LOGS = "audit-logs"


# Event schema registry
EVENT_SCHEMAS = {
    TaskEventType.TASK_CREATED: TaskCreatedEvent,
    TaskEventType.TASK_UPDATED: TaskUpdatedEvent,
    TaskEventType.TASK_DELETED: TaskDeletedEvent,
    TaskEventType.TASK_COMPLETED: TaskCompletedEvent,
    TaskEventType.TASK_RECURRING_GENERATED: TaskRecurringGeneratedEvent,
    TaskEventType.TASK_REMINDER_SCHEDULED: TaskReminderScheduledEvent,
}