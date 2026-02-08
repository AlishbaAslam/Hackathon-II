"""
WebSocket session entity model for real-time sync.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


class WebSocketSession(SQLModel, table=True):
    """
    WebSocket session entity representing active real-time connections.

    Attributes:
        id: Unique session identifier (UUID)
        user_id: ID of the user who established the connection
        session_token: Unique token identifying the WebSocket connection
        connection_url: URL of the WebSocket connection
        connected_at: Timestamp when the connection was established
        disconnected_at: Timestamp when the connection was closed (nullable)
        is_active: Whether the session is currently active
    """
    __tablename__ = "websocket_sessions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    session_token: str = Field(max_length=255, nullable=False, unique=True)
    connection_url: str = Field(max_length=500, nullable=False)
    connected_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    disconnected_at: Optional[datetime] = Field(default=None, nullable=True)
    is_active: bool = Field(default=True, nullable=False)