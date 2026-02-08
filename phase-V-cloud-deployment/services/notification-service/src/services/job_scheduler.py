"""
Job scheduler for reminder notifications using Dapr Jobs API.
"""
import logging
from datetime import datetime
from typing import Dict, Any

import httpx
from pydantic import BaseModel

logger = logging.getLogger(__name__)


async def schedule_reminder_job(reminder_data: Dict[str, Any]) -> bool:
    """
    Schedule a reminder notification using Dapr Jobs API.

    Args:
        reminder_data: Data about the reminder to schedule

    Returns:
        True if successfully scheduled, False otherwise
    """
    try:
        # Extract required data from reminder_data
        reminder_id = reminder_data.get('reminder_id', 'unknown')
        scheduled_time = reminder_data.get('scheduled_time')
        user_id = reminder_data.get('user_id')
        task_id = reminder_data.get('task_id')
        message = reminder_data.get('message', f'Reminder for task {task_id}')

        if not scheduled_time:
            logger.error(f"No scheduled time provided for reminder {reminder_id}")
            return False

        # Parse the scheduled time to datetime object
        if isinstance(scheduled_time, str):
            try:
                scheduled_dt = datetime.fromisoformat(scheduled_time.replace('Z', '+00:00'))
            except ValueError:
                logger.error(f"Invalid scheduled time format: {scheduled_time}")
                return False
        elif isinstance(scheduled_time, datetime):
            scheduled_dt = scheduled_time
        else:
            logger.error(f"Invalid scheduled time type: {type(scheduled_time)}")
            return False

        # Prepare job payload
        job_payload = {
            "jobName": f"reminder-{reminder_id}",
            "schedule": scheduled_dt.strftime("%M %H %d %m %Y"),  # Crontab format
            "target": {
                "type": "HTTP",
                "uri": "http://notification-service:8002/api/send-notification",  # Adjust URL as needed
                "data": {
                    "user_id": user_id,
                    "task_id": task_id,
                    "message": message,
                    "channel": reminder_data.get('channel', 'push')
                }
            },
            "retryCount": 3,
            "timeout": "10m"
        }

        # Schedule the job using Dapr Jobs API
        dapr_http_endpoint = "http://localhost:3500"  # Should come from config
        url = f"{dapr_http_endpoint}/v1.0/jobs"

        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
            response = await client.post(url, json=job_payload)

            if response.status_code in [200, 201, 202]:
                logger.info(f"Successfully scheduled reminder job for {reminder_id}")
                return True
            else:
                logger.error(f"Failed to schedule reminder job: {response.status_code} - {response.text}")
                return False

    except Exception as e:
        logger.error(f"Error scheduling reminder job: {str(e)}", exc_info=True)
        return False


async def cancel_reminder_job(reminder_id: str) -> bool:
    """
    Cancel a scheduled reminder job.

    Args:
        reminder_id: ID of the reminder job to cancel

    Returns:
        True if successfully cancelled, False otherwise
    """
    try:
        job_name = f"reminder-{reminder_id}"
        dapr_http_endpoint = "http://localhost:3500"  # Should come from config
        url = f"{dapr_http_endpoint}/v1.0/jobs/{job_name}"

        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
            response = await client.delete(url)

            if response.status_code == 204:
                logger.info(f"Successfully cancelled reminder job for {reminder_id}")
                return True
            elif response.status_code == 404:
                logger.warning(f"Reminder job {job_name} not found, treating as cancelled")
                return True
            else:
                logger.error(f"Failed to cancel reminder job: {response.status_code} - {response.text}")
                return False

    except Exception as e:
        logger.error(f"Error cancelling reminder job: {str(e)}", exc_info=True)
        return False