"""
Task entity model.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship

class Task(SQLModel, table=True):
    """
    Task entity representing a todo item owned by a user.

    Attributes:
        id: Unique task identifier (UUID)
        title: Task title (required, max 200 characters)
        description: Optional task description (max 2000 characters)
        is_completed: Task completion status (default: False)
        user_id: Owner user ID (foreign key to users table)
        created_at: Task creation timestamp
        updated_at: Last update timestamp
        owner: Relationship to the owning user (many-to-one)
    """
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=2000, nullable=True)
    is_completed: bool = Field(default=False, nullable=False)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship (not a database column)
    owner: Optional["User"] = Relationship(back_populates="tasks")
