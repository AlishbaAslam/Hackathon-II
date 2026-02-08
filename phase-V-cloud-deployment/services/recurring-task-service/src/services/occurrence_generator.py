"""
Occurrence generator for creating new task instances from recurring tasks.
"""
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID

import httpx
from pydantic import BaseModel

from ..types import RecurrencePattern
from .recurrence_logic import calculate_next_occurrence
from .event_publisher import publish_task_recurring_generated_event

logger = logging.getLogger(__name__)


class RecurringTaskData(BaseModel):
    """
    Model for recurring task data.
    """
    task_id: str
    user_id: str
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = "medium"
    tags: Optional[str] = None
    recurrence_pattern: str
    recurrence_interval: int = 1
    parent_task_id: Optional[str] = None


async def generate_next_occurrence(
    recurring_task_data: RecurringTaskData,
    completed_at: datetime
) -> Optional[Dict[str, Any]]:
    """
    Generate the next occurrence of a recurring task.

    Args:
        recurring_task_data: Data about the recurring task
        completed_at: When the parent task was completed

    Returns:
        Dictionary with new task data, or None if generation failed
    """
    try:
        # Validate recurrence pattern
        if not RecurrencePattern(recurring_task_data.recurrence_pattern):
            logger.error(f"Invalid recurrence pattern: {recurring_task_data.recurrence_pattern}")
            return None

        # Calculate next occurrence datetime
        next_occurrence_dt = calculate_next_occurrence(
            completed_at,
            RecurrencePattern(recurring_task_data.recurrence_pattern),
            recurring_task_data.recurrence_interval
        )

        if not next_occurrence_dt:
            logger.error(f"Failed to calculate next occurrence for task {recurring_task_data.task_id}")
            return None

        # Prepare new task data based on original task
        new_task_data = {
            "title": recurring_task_data.title,
            "description": recurring_task_data.description,
            "due_date": next_occurrence_dt.isoformat() if recurring_task_data.due_date else None,
            "priority": recurring_task_data.priority,
            "tags": recurring_task_data.tags,
            "is_recurring": True,  # Preserve recurrence property
            "recurrence_pattern": recurring_task_data.recurrence_pattern,
            "remind_at": next_occurrence_dt.isoformat() if recurring_task_data.due_date else None,
            "parent_task_id": recurring_task_data.task_id  # Link to parent
        }

        # Create the new task via API call to the main backend
        backend_url = "http://localhost:8000"  # This should come from config
        headers = {
            "Authorization": f"Bearer {await _get_admin_token()}",  # Need proper auth
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{backend_url}/api/{recurring_task_data.user_id}/tasks",
                json=new_task_data,
                headers=headers
            )

            if response.status_code == 201:
                new_task = response.json()

                # Publish event about the new occurrence being generated
                await publish_task_recurring_generated_event(
                    user_id=UUID(recurring_task_data.user_id),
                    parent_task_id=UUID(recurring_task_data.task_id),
                    new_task_id=UUID(new_task['id']),
                    recurrence_data={
                        "parent_task_id": recurring_task_data.task_id,
                        "new_task_id": new_task['id'],
                        "recurrence_pattern": recurring_task_data.recurrence_pattern,
                        "calculated_next_date": next_occurrence_dt.isoformat()
                    }
                )

                logger.info(f"Successfully generated next occurrence for task {recurring_task_data.task_id}: {new_task['id']}")
                return new_task
            else:
                logger.error(f"Failed to create new task occurrence: {response.status_code} - {response.text}")
                return None

    except Exception as e:
        logger.error(f"Error generating next occurrence for task {recurring_task_data.task_id}: {str(e)}")
        return None


async def _get_admin_token() -> str:
    """
    Get admin token for API calls. This is a placeholder - implement proper auth.

    Returns:
        Admin token string
    """
    # This is a placeholder implementation
    # In a real implementation, you'd need to securely obtain an admin token
    # or use service-to-service authentication
    return "admin-token-placeholder"