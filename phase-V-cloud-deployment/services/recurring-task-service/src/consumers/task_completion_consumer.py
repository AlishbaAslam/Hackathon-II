"""
Kafka consumer for task completion events to trigger recurring task generation.
"""
import logging
from datetime import datetime
from typing import Dict, Any
from uuid import UUID

from ..types import RecurrencePattern
from ..services.occurrence_generator import RecurringTaskData, generate_next_occurrence

logger = logging.getLogger(__name__)


async def handle_task_completion(event_data: Dict[str, Any]):
    """
    Handle task completion event and generate next occurrence if the task is recurring.

    Args:
        event_data: The task completion event data
    """
    try:
        # Extract relevant information from the event
        event_type = event_data.get('event_type')
        task_payload = event_data.get('payload', {})

        # Only process task completion events
        if event_type != 'task.completed':
            logger.debug(f"Skipping non-completion event: {event_type}")
            return

        # Check if this task is recurring
        task_data = task_payload.get('task_data', {})
        is_recurring = task_data.get('is_recurring', False)

        if not is_recurring:
            logger.debug(f"Task {event_data.get('task_id')} is not recurring, skipping")
            return

        # Validate recurrence pattern
        recurrence_pattern = task_data.get('recurrence_pattern')
        if not recurrence_pattern or recurrence_pattern not in [rp.value for rp in RecurrencePattern]:
            logger.warning(f"Invalid or missing recurrence pattern for task {event_data.get('task_id')}: {recurrence_pattern}")
            return

        # Create recurring task data object
        recurring_task_data = RecurringTaskData(
            task_id=event_data.get('task_id'),
            user_id=event_data.get('user_id'),
            title=task_data.get('title', ''),
            description=task_data.get('description'),
            due_date=datetime.fromisoformat(task_data['due_date'].replace('Z', '+00:00')) if task_data.get('due_date') else None,
            priority=task_data.get('priority', 'medium'),
            tags=task_data.get('tags'),
            recurrence_pattern=recurrence_pattern,
            recurrence_interval=task_data.get('recurrence_interval', 1)  # Default to 1
        )

        # Get completion time
        completion_time_str = task_data.get('completed_at') or event_data.get('timestamp')
        if completion_time_str:
            completed_at = datetime.fromisoformat(completion_time_str.replace('Z', '+00:00'))
        else:
            completed_at = datetime.utcnow()

        # Generate the next occurrence
        new_task = await generate_next_occurrence(recurring_task_data, completed_at)

        if new_task:
            logger.info(f"Successfully generated next occurrence for recurring task {event_data.get('task_id')}")
        else:
            logger.error(f"Failed to generate next occurrence for recurring task {event_data.get('task_id')}")

    except Exception as e:
        logger.error(f"Error handling task completion event: {str(e)}", exc_info=True)