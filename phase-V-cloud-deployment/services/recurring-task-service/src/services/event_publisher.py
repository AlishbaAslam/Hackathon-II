"""
Event publisher for recurring task service using Dapr pub/sub.
"""
import logging
from typing import Dict, Any
from uuid import UUID

import httpx
from pydantic import BaseModel

from ....backend.src.core.event_schemas import TaskEventType

logger = logging.getLogger(__name__)


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
        # Construct the event data
        event_data = {
            "event_id": f"recurring-{str(new_task_id)[:8]}-{int(__import__('time').time())}",
            "event_type": "task.recurring.generated",
            "user_id": str(user_id),
            "task_id": str(new_task_id),
            "timestamp": __import__('datetime').datetime.utcnow().isoformat() + "Z",
            "payload": {
                "parent_task_id": str(parent_task_id),
                "new_task_id": str(new_task_id),
                "recurrence_data": recurrence_data
            }
        }

        # Publish to Dapr pub/sub
        dapr_http_endpoint = "http://localhost:3500"  # Should come from config
        topic = "task-events"

        url = f"{dapr_http_endpoint}/v1.0/publish/pubsub/{topic}"

        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
            response = await client.post(url, json=event_data)

            if response.status_code == 200:
                logger.info(f"Task recurring generated event published for parent task {parent_task_id}, new task {new_task_id}")
                return True
            else:
                logger.error(f"Failed to publish task recurring generated event: {response.status_code} - {response.text}")
                return False

    except Exception as e:
        logger.error(f"Error publishing task recurring generated event for parent task {parent_task_id}: {str(e)}")
        return False