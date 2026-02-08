from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

if TYPE_CHECKING:
    from .user import User
    from .message import Message


class ConversationBase(SQLModel):
    user_id: UUID = Field(foreign_key="users.id", nullable=False)


class Conversation(ConversationBase, table=True):
    """
    Conversation model representing a chat session for a user.
    Contains metadata like creation time and user association.
    """
    __tablename__ = "conversations"

    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: list["Message"] = Relationship(back_populates="conversation")


class ConversationRead(ConversationBase):
    """Schema for reading conversation data"""
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime


class ConversationCreate(ConversationBase):
    """Schema for creating conversation data"""
    pass


class ConversationUpdate(SQLModel):
    """Schema for updating conversation data"""
    pass