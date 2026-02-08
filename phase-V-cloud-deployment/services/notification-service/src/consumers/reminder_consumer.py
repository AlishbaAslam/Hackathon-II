"""
Kafka consumer for reminder scheduling events to trigger notification scheduling.
"""
import logging
from datetime import datetime
from typing import Dict, Any

from ..services.job_scheduler import schedule_reminder_job

logger = logging.getLogger(__name__)


async def handle_reminder_scheduled(event_data: Dict[str, Any]):
    """
    Handle reminder scheduled event and schedule the notification.

    Args:
        event_data: The reminder scheduled event data
    """
    try:
        # Extract relevant information from the event
        event_type = event_data.get('event_type')

        # Only process reminder scheduled events
        if event_type != 'task.reminder.scheduled':
            logger.debug(f"Skipping non-reminder event: {event_type}")
            return

        # Extract reminder data from the event payload
        reminder_payload = event_data.get('payload', {})
        reminder_data = reminder_payload.get('reminder_data', {})

        # Create reminder data structure for scheduling
        formatted_reminder_data = {
            'reminder_id': event_data.get('event_id', 'unknown'),
            'user_id': event_data.get('user_id'),
            'task_id': event_data.get('task_id'),
            'scheduled_time': reminder_data.get('scheduled_time'),
            'message': reminder_data.get('message', f'Reminder for task {event_data.get("task_id")}'),
            'channel': reminder_data.get('channel', 'push')
        }

        # Schedule the reminder job
        success = await schedule_reminder_job(formatted_reminder_data)

        if success:
            logger.info(f"Successfully scheduled reminder for task {event_data.get('task_id')}")
        else:
            logger.error(f"Failed to schedule reminder for task {event_data.get('task_id')}")

    except Exception as e:
        logger.error(f"Error handling reminder scheduled event: {str(e)}", exc_info=True)