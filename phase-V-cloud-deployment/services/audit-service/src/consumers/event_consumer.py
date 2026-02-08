"""
Event consumer for audit service to handle all task events and log them.
"""
import logging
from datetime import datetime
from typing import Dict, Any

from ..services.audit_logger import log_audit_event

logger = logging.getLogger(__name__)


async def handle_task_event(event_data: Dict[str, Any]):
    """
    Handle any task event and log it to the audit trail.

    Args:
        event_data: The task event data
    """
    try:
        # Extract relevant information from the event
        event_type = event_data.get('event_type', 'unknown')
        user_id = event_data.get('user_id')
        task_id = event_data.get('task_id')

        logger.info(f"Processing task event: {event_type} for user {user_id}, task {task_id}")

        # Log the event to the audit trail
        success = await log_audit_event(event_data)

        if success:
            logger.info(f"Successfully audited event: {event_type} for user {user_id}, task {task_id}")
        else:
            logger.error(f"Failed to audit event: {event_type} for user {user_id}, task {task_id}")

    except Exception as e:
        logger.error(f"Error handling task event for audit: {str(e)}", exc_info=True)