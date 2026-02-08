"""
Event publisher functions for task events using Dapr pub/sub.
"""
from typing import Dict, Any
from uuid import UUID
import logging

from ..core.dapr_client import publish_task_event
from ..core.event_schemas import TaskEventType

logger = logging.getLogger(__name__)


async def publish_task_created_event(user_id: UUID, task_id: UUID, task_data: Dict[str, Any]) -> bool:
    """
    Publish an event when a task is created.

    Args:
        user_id: ID of the user who created the task
        task_id: ID of the created task
        task_data: Task data to include in the event

    Returns:
        True if event was published successfully, False otherwise
    """
    try:
        payload = {
            "task_id": str(task_id),
            "user_id": str(user_id),
            "task_data": task_data
        }

        success = await publish_task_event(
            event_type=TaskEventType.TASK_CREATED,
            user_id=str(user_id),
            task_id=str(task_id),
            payload=payload
        )

        if success:
            logger.info(f"Task created event published for task {task_id}")
        else:
            logger.error(f"Failed to publish task created event for task {task_id}")

        return success
    except Exception as e:
        logger.error(f"Error publishing task created event for task {task_id}: {str(e)}")
        return False


async def publish_task_updated_event(user_id: UUID, task_id: UUID, updated_fields: Dict[str, Any]) -> bool:
    """
    Publish an event when a task is updated.

    Args:
        user_id: ID of the user who updated the task
        task_id: ID of the updated task
        updated_fields: Dictionary of fields that were updated

    Returns:
        True if event was published successfully, False otherwise
    """
    try:
        payload = {
            "task_id": str(task_id),
            "user_id": str(user_id),
            "updated_fields": updated_fields
        }

        success = await publish_task_event(
            event_type=TaskEventType.TASK_UPDATED,
            user_id=str(user_id),
            task_id=str(task_id),
            payload=payload
        )

        if success:
            logger.info(f"Task updated event published for task {task_id}")
        else:
            logger.error(f"Failed to publish task updated event for task {task_id}")

        return success
    except Exception as e:
        logger.error(f"Error publishing task updated event for task {task_id}: {str(e)}")
        return False


async def publish_task_deleted_event(user_id: UUID, task_id: UUID, deletion_reason: str = None) -> bool:
    """
    Publish an event when a task is deleted.

    Args:
        user_id: ID of the user who deleted the task
        task_id: ID of the deleted task
        deletion_reason: Optional reason for deletion

    Returns:
        True if event was published successfully, False otherwise
    """
    try:
        payload = {
            "task_id": str(task_id),
            "user_id": str(user_id),
            "deletion_reason": deletion_reason
        }

        success = await publish_task_event(
            event_type=TaskEventType.TASK_DELETED,
            user_id=str(user_id),
            task_id=str(task_id),
            payload=payload
        )

        if success:
            logger.info(f"Task deleted event published for task {task_id}")
        else:
            logger.error(f"Failed to publish task deleted event for task {task_id}")

        return success
    except Exception as e:
        logger.error(f"Error publishing task deleted event for task {task_id}: {str(e)}")
        return False


async def publish_task_completed_event(user_id: UUID, task_id: UUID, completion_data: Dict[str, Any] = None) -> bool:
    """
    Publish an event when a task is marked as completed.

    Args:
        user_id: ID of the user who completed the task
        task_id: ID of the completed task
        completion_data: Optional additional data about the completion

    Returns:
        True if event was published successfully, False otherwise
    """
    try:
        payload = {
            "task_id": str(task_id),
            "user_id": str(user_id),
            "completion_data": completion_data or {}
        }

        success = await publish_task_event(
            event_type=TaskEventType.TASK_COMPLETED,
            user_id=str(user_id),
            task_id=str(task_id),
            payload=payload
        )

        if success:
            logger.info(f"Task completed event published for task {task_id}")
        else:
            logger.error(f"Failed to publish task completed event for task {task_id}")

        return success
    except Exception as e:
        logger.error(f"Error publishing task completed event for task {task_id}: {str(e)}")
        return False


async def publish_task_recurring_generated_event(
    user_id: UUID,
    parent_task_id: UUID,
    new_task_id: UUID,
    recurrence_data: Dict[str, Any]
) -> bool:
    """
    Publish an event when a recurring task generates the next occurrence.

    Args:
        user_id: ID of the user who owns the recurring task
        parent_task_id: ID of the parent recurring task
        new_task_id: ID of the newly generated task
        recurrence_data: Information about the recurrence pattern

    Returns:
        True if event was published successfully, False otherwise
    """
    try:
        payload = {
            "parent_task_id": str(parent_task_id),
            "new_task_id": str(new_task_id),
            "user_id": str(user_id),
            "recurrence_data": recurrence_data
        }

        success = await publish_task_event(
            event_type=TaskEventType.TASK_RECURRING_GENERATED,
            user_id=str(user_id),
            task_id=str(new_task_id),  # Using new task ID as the main task ID for this event
            payload=payload
        )

        if success:
            logger.info(f"Task recurring generated event published for parent task {parent_task_id}, new task {new_task_id}")
        else:
            logger.error(f"Failed to publish task recurring generated event for parent task {parent_task_id}")

        return success
    except Exception as e:
        logger.error(f"Error publishing task recurring generated event for parent task {parent_task_id}: {str(e)}")
        return False


async def publish_task_reminder_scheduled_event(
    user_id: UUID,
    task_id: UUID,
    reminder_data: Dict[str, Any]
) -> bool:
    """
    Publish an event when a reminder is scheduled for a task.

    Args:
        user_id: ID of the user who owns the task
        task_id: ID of the task for which reminder is scheduled
        reminder_data: Information about the scheduled reminder

    Returns:
        True if event was published successfully, False otherwise
    """
    try:
        payload = {
            "task_id": str(task_id),
            "user_id": str(user_id),
            "reminder_data": reminder_data
        }

        success = await publish_task_event(
            event_type=TaskEventType.TASK_REMINDER_SCHEDULED,
            user_id=str(user_id),
            task_id=str(task_id),
            payload=payload
        )

        if success:
            logger.info(f"Task reminder scheduled event published for task {task_id}")
        else:
            logger.error(f"Failed to publish task reminder scheduled event for task {task_id}")

        return success
    except Exception as e:
        logger.error(f"Error publishing task reminder scheduled event for task {task_id}: {str(e)}")
        return False


# Bulk event publisher for multiple operations
async def publish_multiple_events(events_data: list) -> Dict[str, int]:
    """
    Publish multiple events in bulk.

    Args:
        events_data: List of tuples containing (event_func, args) for different event types

    Returns:
        Dictionary with counts of successful and failed events
    """
    results = {"success": 0, "failed": 0}

    for event_func, args in events_data:
        try:
            success = await event_func(*args)
            if success:
                results["success"] += 1
            else:
                results["failed"] += 1
        except Exception as e:
            logger.error(f"Error in bulk event publishing: {str(e)}")
            results["failed"] += 1

    return results