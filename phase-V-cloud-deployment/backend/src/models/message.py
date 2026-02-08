from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

if TYPE_CHECKING:
    from .user import User
    from .conversation import Conversation


class MessageBase(SQLModel):
    user_id: UUID = Field(foreign_key="users.id", nullable=False)
    conversation_id: int = Field(foreign_key="conversations.id", nullable=False)
    role: str = Field(max_length=20, nullable=False)  # Either "user" or "assistant"
    content: str = Field(max_length=10000, nullable=False)  # Up to 10,000 characters


class Message(MessageBase, table=True):
    """
    Message model representing individual messages within a conversation.
    Contains sender role (user/assistant), content, and timestamp.
    """
    __tablename__ = "messages"

    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    user: "User" = Relationship(back_populates="messages")
    conversation: "Conversation" = Relationship(back_populates="messages")


class MessageRead(MessageBase):
    """Schema for reading message data"""
    id: int
    created_at: datetime


class MessageCreate(MessageBase):
    """Schema for creating message data"""
    pass


class MessageUpdate(SQLModel):
    """Schema for updating message data (messages are immutable after creation)"""
    pass