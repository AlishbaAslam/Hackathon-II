"""Task data model for the todo console application."""

from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique identifier for the task (auto-assigned).
        title: Brief description of what needs to be done (required).
        description: Optional detailed notes about the task.
        completed: Whether the task has been completed (default False).
        priority: Task priority (High, Medium, Low).
        tags: Optional labels for the task (max 3).
        due_date: Optional deadline in YYYY-MM-DD format.
    """

    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "Medium"
    tags: List[str] = field(default_factory=list)
    due_date: Optional[str] = None
    due_time: Optional[str] = None
    recurrence: Optional[str] = None
    root_id: Optional[int] = None
    is_root: bool = False
