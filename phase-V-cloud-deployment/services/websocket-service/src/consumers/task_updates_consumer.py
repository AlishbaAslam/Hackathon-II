"""
Consumer for task update events to broadcast to WebSocket clients.
"""
import logging
from datetime import datetime
from typing import Dict, Any

from ..services.ws_server import WebSocketManager

logger = logging.getLogger(__name__)

# Global WebSocket manager instance (should be initialized in main app)
ws_manager = WebSocketManager()


async def handle_task_update(event_data: Dict[str, Any]):
    """
    Handle task update event and broadcast it to connected WebSocket clients.

    Args:
        event_data: The task update event data
    """
    try:
        # Extract relevant information from the event
        event_type = event_data.get('event_type', 'unknown')
        user_id = event_data.get('user_id')
        task_id = event_data.get('task_id')

        logger.info(f"Processing task update event: {event_type} for user {user_id}, task {task_id}")

        # Prepare the update data for WebSocket broadcast
        task_update_data = {
            "event_type": event_type,
            "user_id": user_id,
            "task_id": task_id,
            "payload": event_data.get('payload', {}),
            "timestamp": datetime.utcnow().isoformat()
        }

        # Broadcast the update to the relevant user's connected clients
        await ws_manager.broadcast_task_update(task_update_data)

        logger.info(f"Successfully broadcast task update for user {user_id}, task {task_id}")

    except Exception as e:
        logger.error(f"Error handling task update event: {str(e)}", exc_info=True)