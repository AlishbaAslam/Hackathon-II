"""
WebSocket Service for real-time synchronization of task updates across connected clients.

This service listens to task update events and broadcasts them to all connected
WebSocket clients in real-time.
"""
import asyncio
import json
import logging
import os
from typing import Dict, List, Set
from uuid import UUID

import websockets
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from .services.ws_server import WebSocketManager
from .consumers.task_updates_consumer import handle_task_update

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="WebSocket Service", version="0.1.0")

# Global WebSocket manager instance
ws_manager = WebSocketManager()


@app.on_event("startup")
async def startup_event():
    """Initialize the service on startup."""
    logger.info("WebSocket Service starting up...")
    # Initialize the WebSocket manager
    await ws_manager.initialize()


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("WebSocket Service shutting down...")
    # Disconnect all clients
    await ws_manager.disconnect_all()
    # Cleanup
    await ws_manager.cleanup()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "websocket-service", "connected_clients": len(ws_manager.active_connections)}


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    WebSocket endpoint for real-time task updates.

    Args:
        websocket: WebSocket connection
        user_id: ID of the user connecting
    """
    await ws_manager.connect(websocket, user_id)

    try:
        # Keep the connection alive
        while True:
            # Listen for messages from the client (though in our case we mainly broadcast)
            try:
                data = await websocket.receive_text()
                # Handle any client messages here if needed
                # For now, we just acknowledge receipt
                await websocket.send_text(json.dumps({"type": "ack", "message": "received"}))
            except WebSocketDisconnect:
                break
    except WebSocketDisconnect:
        pass
    finally:
        await ws_manager.disconnect(websocket, user_id)


@app.post("/broadcast-task-update")
async def broadcast_task_update(task_update_data: Dict):
    """
    Endpoint to manually trigger a task update broadcast.
    This would typically be called internally when a task event is received.
    """
    try:
        # Broadcast the update to relevant connected clients
        await ws_manager.broadcast_task_update(task_update_data)
        return {"status": "success", "message": "Update broadcast to relevant clients"}
    except Exception as e:
        logger.error(f"Error broadcasting task update: {str(e)}")
        return {"status": "error", "message": str(e)}


@app.get("/")
async def root():
    """Root endpoint for basic service information."""
    return {
        "message": "WebSocket Service",
        "version": "0.1.0",
        "description": "Provides real-time synchronization of task updates across connected clients"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        reload=True
    )