"""
Recurring Task Service for handling automatic generation of recurring tasks.

This service listens to task completion events and generates the next occurrence
for recurring tasks based on the recurrence pattern.
"""
import asyncio
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Any

import httpx
from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel

from .services.recurrence_logic import calculate_next_occurrence
from .services.occurrence_generator import generate_next_occurrence
from .services.event_publisher import publish_task_recurring_generated_event
from .consumers.task_completion_consumer import handle_task_completion

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Recurring Task Service", version="0.1.0")


@app.on_event("startup")
async def startup_event():
    """Initialize the service on startup."""
    logger.info("Recurring Task Service starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Recurring Task Service shutting down...")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "recurring-task-service"}


@app.post("/events/task-completed")
async def task_completed_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Webhook endpoint for receiving task completion events from Dapr pub/sub.

    This endpoint is called by Dapr when a task-completed event is published.
    """
    try:
        event_data = await request.json()
        logger.info(f"Received task completion event: {event_data}")

        # Process the event in the background to avoid blocking Dapr
        background_tasks.add_task(handle_task_completion, event_data)

        # Acknowledge the event to Dapr
        return {"status": "ACK"}

    except Exception as e:
        logger.error(f"Error processing task completion event: {str(e)}")
        # Return error to Dapr to potentially retry
        return {"status": "NACK"}


@app.get("/")
async def root():
    """Root endpoint for basic service information."""
    return {
        "message": "Recurring Task Service",
        "version": "0.1.0",
        "description": "Handles automatic generation of recurring task occurrences"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8001)),
        reload=True
    )