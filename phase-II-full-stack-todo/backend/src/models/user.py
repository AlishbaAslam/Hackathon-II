"""
User entity model.
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    """
    User entity representing an authenticated user account.

    Attributes:
        id: Unique user identifier (UUID)
        email: User email address (unique, used for login)
        hashed_password: bcrypt hashed password (never stored in plain text)
        name: User display name
        created_at: Account creation timestamp
        updated_at: Last update timestamp
        tasks: Relationship to user's tasks (one-to-many)
    """
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255, nullable=False)
    hashed_password: str = Field(max_length=255, nullable=False)
    name: str = Field(max_length=100, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)

    # Relationship (not a database column)
    tasks: List["Task"] = Relationship(back_populates="owner", sa_relationship_kwargs={"cascade": "all, delete"})
