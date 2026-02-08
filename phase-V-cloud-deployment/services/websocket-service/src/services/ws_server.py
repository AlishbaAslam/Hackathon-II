"""
WebSocket server implementation for real-time task synchronization.
"""
import asyncio
import json
import logging
from typing import Dict, Set, List
from uuid import UUID

from websockets import WebSocketServerProtocol

logger = logging.getLogger(__name__)


class WebSocketManager:
    """
    Manages WebSocket connections and broadcasts messages to connected clients.
    """

    def __init__(self):
        # Dictionary mapping user_id to list of WebSocket connections
        self.active_connections: Dict[str, List[WebSocketServerProtocol]] = {}
        # Track connection IDs to map back to user_ids
        self.connection_to_user: Dict[WebSocketServerProtocol, str] = {}

    async def initialize(self):
        """
        Initialize the WebSocket manager.
        """
        logger.info("WebSocket manager initialized")

    async def connect(self, websocket: WebSocketServerProtocol, user_id: str):
        """
        Add a new WebSocket connection for a user.

        Args:
            websocket: The WebSocket connection
            user_id: The ID of the user connecting
        """
        await websocket.accept()

        # Initialize user's connection list if it doesn't exist
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []

        # Add the connection to the user's list
        self.active_connections[user_id].append(websocket)
        self.connection_to_user[websocket] = user_id

        logger.info(f"WebSocket connected for user {user_id}. Total connections for user: {len(self.active_connections[user_id])}")

    async def disconnect(self, websocket: WebSocketServerProtocol, user_id: str):
        """
        Remove a WebSocket connection for a user.

        Args:
            websocket: The WebSocket connection
            user_id: The ID of the user disconnecting
        """
        if user_id in self.active_connections:
            try:
                self.active_connections[user_id].remove(websocket)
                del self.connection_to_user[websocket]

                if len(self.active_connections[user_id]) == 0:
                    del self.active_connections[user_id]

                logger.info(f"WebSocket disconnected for user {user_id}. Remaining connections: {len(self.active_connections.get(user_id, []))}")
            except ValueError:
                # Connection was already removed
                logger.warning(f"Attempted to remove non-existent connection for user {user_id}")
        else:
            logger.warning(f"User {user_id} not found in active connections during disconnect")

    async def disconnect_all(self):
        """
        Disconnect all active WebSocket connections.
        """
        for user_id in list(self.active_connections.keys()):
            for websocket in self.active_connections[user_id][:]:  # Copy to avoid modification during iteration
                try:
                    await websocket.close(code=1001, reason="Server shutdown")
                except Exception:
                    pass  # Connection might already be closed
            del self.active_connections[user_id]

        self.connection_to_user.clear()
        logger.info("All WebSocket connections disconnected")

    async def broadcast_task_update(self, task_update_data: Dict):
        """
        Broadcast a task update to all connected clients for the affected user.

        Args:
            task_update_data: The task update data to broadcast
        """
        try:
            # Extract the user ID from the update data
            user_id = task_update_data.get('user_id')

            if not user_id:
                logger.error("No user_id found in task update data")
                return

            # Check if user has active connections
            if user_id not in self.active_connections:
                logger.info(f"No active connections for user {user_id}")
                return

            # Prepare the message to send
            message = {
                "type": "task_update",
                "data": task_update_data,
                "timestamp": __import__('datetime').datetime.utcnow().isoformat()
            }

            # Send the message to all connections for this user
            connections_to_remove = []
            for websocket in self.active_connections[user_id][:]:  # Copy to avoid modification during iteration
                try:
                    await websocket.send(json.dumps(message))
                except Exception as e:
                    logger.error(f"Error sending message to user {user_id}: {str(e)}")
                    connections_to_remove.append(websocket)

            # Remove broken connections
            for websocket in connections_to_remove:
                await self.disconnect(websocket, user_id)

            logger.info(f"Broadcast task update to {len(self.active_connections.get(user_id, []))} connections for user {user_id}")

        except Exception as e:
            logger.error(f"Error broadcasting task update: {str(e)}", exc_info=True)

    async def broadcast_to_all(self, message: Dict):
        """
        Broadcast a message to all connected clients.

        Args:
            message: The message to broadcast
        """
        try:
            json_message = json.dumps(message)

            # Collect broken connections to remove later
            connections_to_remove = []

            for user_id, connections in self.active_connections.items():
                for websocket in connections[:]:  # Copy to avoid modification during iteration
                    try:
                        await websocket.send(json_message)
                    except Exception as e:
                        logger.error(f"Error sending message to user {user_id}: {str(e)}")
                        connections_to_remove.append((websocket, user_id))

            # Remove broken connections
            for websocket, user_id in connections_to_remove:
                await self.disconnect(websocket, user_id)

            logger.info(f"Broadcast message to all users. Total connections: {sum(len(conns) for conns in self.active_connections.values())}")

        except Exception as e:
            logger.error(f"Error broadcasting to all: {str(e)}", exc_info=True)

    async def cleanup(self):
        """
        Perform any necessary cleanup operations.
        """
        logger.info("WebSocket manager cleanup completed")