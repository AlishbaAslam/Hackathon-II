"""
Audit Service for handling comprehensive audit logging of task operations.

This service listens to all task events and maintains a complete audit trail
of all operations with timestamps and user information.
"""
import asyncio
import logging
import os
from datetime import datetime
from typing import Dict, Any

import httpx
from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel

from .services.audit_logger import log_audit_event
from .consumers.event_consumer import handle_task_event

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Audit Service", version="0.1.0")


@app.on_event("startup")
async def startup_event():
    """Initialize the service on startup."""
    logger.info("Audit Service starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Audit Service shutting down...")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "audit-service"}


@app.post("/events/task-event")
async def task_event_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Webhook endpoint for receiving task events from Dapr pub/sub.

    This endpoint is called by Dapr when any task-related event is published.
    """
    try:
        event_data = await request.json()
        logger.info(f"Received task event: {event_data.get('event_type', 'unknown')}")

        # Process the event in the background to avoid blocking Dapr
        background_tasks.add_task(handle_task_event, event_data)

        # Acknowledge the event to Dapr
        return {"status": "ACK"}

    except Exception as e:
        logger.error(f"Error processing task event: {str(e)}")
        # Return error to Dapr to potentially retry
        return {"status": "NACK"}


@app.get("/audit-log/{user_id}")
async def get_audit_log(user_id: str):
    """
    Endpoint to retrieve audit log for a specific user.
    """
    # This would be implemented to fetch audit logs from storage
    # For now, it's a placeholder
    return {"message": f"Audit log for user {user_id}"}


@app.get("/")
async def root():
    """Root endpoint for basic service information."""
    return {
        "message": "Audit Service",
        "version": "0.1.0",
        "description": "Maintains complete audit trail of all task operations"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8003)),
        reload=True
    )