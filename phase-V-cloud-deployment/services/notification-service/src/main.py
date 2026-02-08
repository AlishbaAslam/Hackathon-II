"""
Notification Service for handling task reminders and notifications.

This service listens to reminder scheduling events and delivers notifications
at the specified times using various channels (email, push, etc.).
"""
import asyncio
import logging
import os
from datetime import datetime
from typing import Dict, Any

import httpx
from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel

from .services.job_scheduler import schedule_reminder_job
from .consumers.reminder_consumer import handle_reminder_scheduled
from .services.notification_sender import send_notification

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Notification Service", version="0.1.0")


@app.on_event("startup")
async def startup_event():
    """Initialize the service on startup."""
    logger.info("Notification Service starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Notification Service shutting down...")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "notification-service"}


@app.post("/events/reminder-scheduled")
async def reminder_scheduled_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Webhook endpoint for receiving reminder scheduled events from Dapr pub/sub.

    This endpoint is called by Dapr when a reminder-scheduled event is published.
    """
    try:
        event_data = await request.json()
        logger.info(f"Received reminder scheduled event: {event_data}")

        # Process the event in the background to avoid blocking Dapr
        background_tasks.add_task(handle_reminder_scheduled, event_data)

        # Acknowledge the event to Dapr
        return {"status": "ACK"}

    except Exception as e:
        logger.error(f"Error processing reminder scheduled event: {str(e)}")
        # Return error to Dapr to potentially retry
        return {"status": "NACK"}


@app.post("/trigger-notification")
async def trigger_notification(notification_data: Dict[str, Any]):
    """
    Endpoint to trigger a notification manually.
    """
    try:
        result = await send_notification(notification_data)
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Error sending notification: {str(e)}")
        return {"status": "error", "error": str(e)}


@app.get("/")
async def root():
    """Root endpoint for basic service information."""
    return {
        "message": "Notification Service",
        "version": "0.1.0",
        "description": "Handles task reminders and notifications via various channels"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8002)),
        reload=True
    )