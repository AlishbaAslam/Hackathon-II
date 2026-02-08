"""
Event handling router for Dapr pub/sub events.
"""
from fastapi import APIRouter, Request, HTTPException
from typing import Dict, Any, List
import logging
import os

from src.services.recurring_consumer import handle_task_event

router = APIRouter(tags=["events"])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get("/dapr/subscribe")
async def dapr_subscribe():
    """
    Dapr subscription endpoint.

    This endpoint tells Dapr which topics this service wants to subscribe to.
    Dapr will call this endpoint to discover subscriptions.
    """
    # Fix: Use "pubsub" as default (created by dapr init)
    pubsub_name = os.getenv("DAPR_PUBSUB_NAME", "pubsub")

    subscriptions = [
        {
            "pubsubname": pubsub_name,
            "topic": "task-events",
            "route": "/events/task-events"
        }
    ]

    logger.info(f"[DAPR_SUBSCRIBE] Using pubsub name: {pubsub_name}")
    logger.info(f"[DAPR_SUBSCRIBE] Returning subscriptions: {subscriptions}")
    return subscriptions


@router.post("/events/task-events")
async def handle_task_events(request: Request):
    """
    Handle task events from Dapr pub/sub.

    This endpoint receives events from the 'task-events' topic via Dapr.
    Dapr sends events in a specific format with 'data' field containing the actual event.
    """
    try:
        # Parse the request body
        body = await request.json()

        logger.info(f"[TASK_EVENTS] Received event from Dapr")
        logger.info(f"[TASK_EVENTS] Full body: {body}")

        # Dapr wraps the event in a 'data' field
        event_data = body.get("data", body)

        logger.info(f"[TASK_EVENTS] Event data: {event_data}")

        # Process the event
        result = await handle_task_event(event_data)

        logger.info(f"[TASK_EVENTS] Processing result: {result}")

        # Return success response for Dapr
        # Dapr expects a 200 status code to acknowledge the message
        return {"status": "SUCCESS"}

    except Exception as e:
        logger.error(f"[TASK_EVENTS] Error processing event: {str(e)}")
        import traceback
        traceback.print_exc()

        # Return RETRY status to tell Dapr to retry this message
        return {"status": "RETRY"}


@router.get("/health")
async def health_check():
    """
    Health check endpoint for the event handler service.
    """
    return {"status": "healthy", "service": "event-handler"}