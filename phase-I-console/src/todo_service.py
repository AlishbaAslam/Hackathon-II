"""Todo service for managing tasks in memory."""

from typing import List, Optional, Dict
from pathlib import Path
import calendar
from datetime import datetime, timedelta
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import Task


class TodoServiceError(Exception):
    """Base exception for todo service errors."""
    pass


class TaskNotFoundError(TodoServiceError):
    """Raised when a task ID is not found."""
    pass


class TodoService:
    """Manages task operations in memory.

    Provides CRUD operations for tasks with auto-incrementing IDs.
    All data is stored in memory and lost when the application exits.
    """

    PRIORITY_MAP: Dict[str, int] = {
        "High": 0,
        "Medium": 1,
        "Low": 2
    }

    def __init__(self) -> None:
        """Initialize the todo service with empty task list."""
        self._tasks: List[Task] = []
        self._next_id: int = 1
        self._available_ids: List[int] = []  # Pool of reusable IDs (min-heap)

    @staticmethod
    def validate_date(date_str: str) -> bool:
        """Validate if a string matches YYYY-MM-DD format.

        Args:
            date_str: The string to validate.

        Returns:
            True if valid, False otherwise.
        """
        if not date_str:
            return True
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def parse_time_to_24h(time_str: str) -> str:
        """Parse time string in either 12-hour AM/PM format or 24-hour format to 24-hour format.

        Args:
            time_str: Time string in format like '2:30 PM', '10:00 AM', or '14:30'.

        Returns:
            Time string in 24-hour format (HH:MM), or empty string if invalid.
        """
        if not time_str or not time_str.strip():
            return ""

        time_str = time_str.strip()

        # Check if it's already in 24-hour format (HH:MM)
        try:
            datetime.strptime(time_str, "%H:%M")
            return time_str
        except ValueError:
            pass

        # Try to parse 12-hour format with AM/PM
        # Handle formats like: "2:30 PM", "2:30PM", "02:30 PM", "12:00 AM", etc.
        time_str = time_str.upper()

        # Check for AM/PM
        if "AM" in time_str or "PM" in time_str:
            # Remove AM/PM for parsing
            time_part = time_str.replace("AM", "").replace("PM", "").strip()

            try:
                hour, minute = time_part.split(":")
                hour = int(hour)
                minute = int(minute)

                # Validate hour and minute ranges
                if hour < 1 or hour > 12 or minute < 0 or minute > 59:
                    return ""

                # Convert to 24-hour format
                is_pm = "PM" in time_str

                if hour == 12:
                    # 12 AM -> 00, 12 PM -> 12
                    hour_24 = 0 if not is_pm else 12
                elif is_pm:
                    # PM hours: add 12 to hours 1-11
                    hour_24 = hour + 12
                else:
                    # AM hours: keep as is, except 12 AM -> 0
                    hour_24 = hour if hour != 12 else 0

                return f"{hour_24:02d}:{minute:02d}"

            except (ValueError, IndexError):
                return ""

        return ""

    @staticmethod
    def validate_time(time_str: str) -> bool:
        """Validate if a string matches HH:MM format (24-hour) or 12-hour AM/PM format.

        Args:
            time_str: The string to validate.

        Returns:
            True if valid, False otherwise.
        """
        if not time_str:
            return True

        # Use the parsing function to validate
        return TodoService.parse_time_to_24h(time_str) != ""

    @staticmethod
    def get_next_date(current_date_str: str, recurrence: str) -> str:
        """Calculate the next due date based on recurrence interval.

        Args:
            current_date_str: Current due date (YYYY-MM-DD).
            recurrence: 'Daily', 'Weekly', or 'Monthly'.

        Returns:
            Next due date in YYYY-MM-DD format.
        """
        current_date = datetime.strptime(current_date_str, "%Y-%m-%d")

        if recurrence == "Daily":
            next_date = current_date + timedelta(days=1)
        elif recurrence == "Weekly":
            next_date = current_date + timedelta(weeks=1)
        elif recurrence == "Monthly":
            # Handle end-of-month cases (e.g., Jan 31 -> Feb 28/29)
            month = current_date.month % 12 + 1
            year = current_date.year + (current_date.month // 12)

            # Find the same day in the next month, or the last day if it doesn't exist
            _, last_day = calendar.monthrange(year, month)
            day = min(current_date.day, last_day)
            next_date = datetime(year, month, day)
        else:
            return current_date_str

        return next_date.strftime("%Y-%m-%d")

    @staticmethod
    def validate_tags(tags: List[str]) -> List[str]:
        """Validate and normalize tags (max 3, stripped).

        Args:
            tags: Raw list of tags.

        Returns:
            List of up to 3 normalized tags.
        """
        if not tags:
            return []
        # Strip and remove empty tags, then take first 3
        normalized = [t.strip() for t in tags if t and t.strip()]
        return normalized[:3]

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID.

        Args:
            task_id: The unique ID of the task to retrieve.

        Returns:
            The Task if found, None otherwise.
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def add_task(
        self,
        title: str,
        description: Optional[str] = None,
        priority: str = "Medium",
        tags: Optional[List[str]] = None,
        due_date: Optional[str] = None,
        due_time: Optional[str] = None,
        recurrence: Optional[str] = None,
    ) -> Task:
        """Create a new task with auto-generated ID.

        Reuses smallest available ID if any deleted, otherwise uses next_id.

        Args:
            title: The task title (required, non-empty).
            description: Optional detailed description.
            priority: Task priority (High, Medium, Low).
            tags: Optional list of labels (max 3).
            due_date: Optional deadline (YYYY-MM-DD).
            due_time: Optional deadline time (HH:MM).
            recurrence: Optional recurrence (Daily, Weekly, Monthly).

        Returns:
            The newly created Task.

        Raises:
            TodoServiceError: If title is empty or metadata is invalid.
        """
        if not title or not title.strip():
            raise TodoServiceError("Title cannot be empty.")

        if priority not in self.PRIORITY_MAP:
            priority = "Medium"

        if due_date and not self.validate_date(due_date):
            raise TodoServiceError("Invalid date format. Expected YYYY-MM-DD.")

        if due_time and not self.validate_time(due_time):
            raise TodoServiceError("Invalid time format. Use HH:MM (24-hour) or H:MM AM/PM (12-hour) format.")

        # Convert time to 24-hour format for storage
        if due_time:
            due_time = self.parse_time_to_24h(due_time)

        # Reuse smallest available ID, or get next new ID
        if self._available_ids:
            task_id = self._available_ids.pop(0)  # Get smallest available
        else:
            task_id = self._next_id
            self._next_id += 1

        task = Task(
            id=task_id,
            title=title.strip(),
            description=description.strip() if description else None,
            completed=False,
            priority=priority,
            tags=self.validate_tags(tags) if tags else [],
            due_date=due_date,
            due_time=due_time,
            recurrence=recurrence,
            is_root=bool(recurrence),
            root_id=task_id if recurrence else None
        )
        self._tasks.append(task)
        return task

    def search_tasks(self, keyword: str) -> List[Task]:
        """Search tasks by keyword in title or description (case-insensitive).

        Args:
            keyword: The search term.

        Returns:
            List of matching tasks.
        """
        if not keyword:
            return self.get_all_tasks()

        keyword = keyword.lower()
        results = []
        for task in self._tasks:
            if (keyword in task.title.lower()) or (task.description and keyword in task.description.lower()):
                results.append(task)
        return results

    def filter_tasks(
        self,
        status: Optional[bool] = None,
        priority: Optional[str] = None,
        tag: Optional[str] = None
    ) -> List[Task]:
        """Filter tasks by status, priority, or tag.

        Args:
            status: Match completion status.
            priority: Match specific priority name.
            tag: Match if tag is in task's tag list (case-insensitive).

        Returns:
            List of filtered tasks.
        """
        results = self._tasks.copy()

        if status is not None:
            results = [t for t in results if t.completed == status]

        if priority is not None:
            results = [t for t in results if t.priority == priority]

        if tag is not None:
            tag = tag.lower()
            results = [t for t in results if any(tag == existing_tag.lower() for existing_tag in t.tags)]

        return results

    def sort_tasks(self, criterion: str, reverse: bool = False) -> List[Task]:
        """Return a sorted copy of tasks.

        Args:
            criterion: 'alphabetical', 'priority', or 'due_date'.
            reverse: Sort in descending order.

        Returns:
            Sorted list of tasks.
        """
        tasks = self._tasks.copy()

        if criterion == "alphabetical":
            tasks.sort(key=lambda t: t.title.lower(), reverse=reverse)
        elif criterion == "priority":
            # Map strings to int weights
            tasks.sort(key=lambda t: self.PRIORITY_MAP.get(t.priority, 1), reverse=reverse)
        elif criterion == "due_date":
            # Sort by date, with Nones at the end
            tasks.sort(key=lambda t: (t.due_date is None, t.due_date), reverse=reverse)

        return tasks

    def _check_overdue_recurring_tasks(self) -> None:
        """Auto-clone recurring tasks when they become overdue.

        This method should be called before rendering the task list or on app startup
        to ensure recurring tasks are properly cloned when they become overdue.
        """
        now = datetime.now()
        tasks_to_clone = []

        for task in self._tasks:
            # Check if task is recurring, not completed, and overdue
            if (task.recurrence and not task.completed and task.due_date):
                try:
                    due_dt_str = f"{task.due_date} {task.due_time if task.due_time else '00:00'}"
                    due_dt = datetime.strptime(due_dt_str, "%Y-%m-%d %H:%M")

                    if due_dt < now:
                        # Check if a next occurrence for this recurring series already exists
                        # to prevent duplicate clones
                        next_date = self.get_next_date(task.due_date, task.recurrence)
                        already_exists = any(
                            t.root_id == task.root_id and
                            t.due_date == next_date and
                            not t.completed
                            for t in self._tasks
                        )

                        if not already_exists:
                            tasks_to_clone.append(task)
                except ValueError:
                    continue

        # Clone all overdue recurring tasks
        for task in tasks_to_clone:
            self._clone_recurring_task(task)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks.

        Returns:
            List of all tasks in insertion order.
        """
        return self._tasks.copy()

    def get_upcoming_alerts(self, window_minutes: int = 15) -> List[Task]:
        """Get tasks with imminent deadlines (due within window).

        Args:
            window_minutes: Time window in minutes.

        Returns:
            List of tasks matching criteria.
        """
        now = datetime.now()
        upcoming = []

        for task in self._tasks:
            if task.completed or not task.due_date:
                continue

            try:
                # Combine date and time
                due_dt_str = f"{task.due_date} {task.due_time if task.due_time else '00:00'}"
                due_dt = datetime.strptime(due_dt_str, "%Y-%m-%d %H:%M")

                # If task is overdue or due within window
                diff = (due_dt - now).total_seconds() / 60
                # Show if due within window, or overdue by up to 24 hours (recent backlog)
                if -1440 <= diff <= window_minutes:
                    upcoming.append(task)
            except ValueError:
                continue

        return upcoming

    def reschedule_overdue_tasks(self, new_date: str) -> int:
        """Auto-reschedule overdue tasks respecting their recurrence patterns.

        Args:
            new_date: The date to use as reference for rescheduling (YYYY-MM-DD).

        Returns:
            Number of tasks rescheduled.
        """
        if not self.validate_date(new_date):
            raise TodoServiceError("Invalid date format.")

        now = datetime.now()
        count = 0

        for task in self._tasks:
            if not task.due_date or task.completed:  # Only reschedule tasks that have due dates AND are not completed
                continue

            try:
                due_dt_str = f"{task.due_date} {task.due_time if task.due_time else '00:00'}"
                due_dt = datetime.strptime(due_dt_str, "%Y-%m-%d %H:%M")

                if due_dt < now:  # Only reschedule overdue tasks
                    # For recurring tasks, calculate the next occurrence based on recurrence type
                    # If the task's original due date is the same as the reference date (today),
                    # we should advance to the next occurrence in the series rather than staying on the same date
                    if task.recurrence:
                        current_date_obj = datetime.strptime(task.due_date, "%Y-%m-%d")
                        reference_date_obj = datetime.strptime(new_date, "%Y-%m-%d")

                        if task.recurrence == "Daily":
                            # Daily tasks → reschedule to reference date (today), unless already due today
                            # If already due today, advance to tomorrow for better user experience
                            if current_date_obj.date() == reference_date_obj.date():
                                # Already due today, advance to tomorrow
                                next_date_obj = reference_date_obj + timedelta(days=1)
                                task.due_date = next_date_obj.strftime("%Y-%m-%d")
                            else:
                                # Was due in the past, reschedule to reference date (today)
                                task.due_date = new_date
                        elif task.recurrence == "Weekly":
                            # Weekly tasks → reschedule to same weekday next week
                            # If originally due today, advance to same weekday next week
                            # If originally due in the past, advance to same weekday after reference date
                            target_weekday = current_date_obj.weekday()

                            # Calculate days from reference date to the target weekday
                            days_ahead = (target_weekday - reference_date_obj.weekday()) % 7

                            # If target weekday is same as reference weekday, advance to next week
                            if days_ahead == 0:
                                days_ahead = 7

                            new_target_date = reference_date_obj + timedelta(days=days_ahead)
                            task.due_date = new_target_date.strftime("%Y-%m-%d")
                        elif task.recurrence == "Monthly":
                            # Monthly tasks → reschedule to same day next month
                            # If originally due today, advance to same day next month
                            # If originally due in the past, advance to same day after reference date
                            next_month = reference_date_obj.month % 12 + 1
                            next_year = reference_date_obj.year + (reference_date_obj.month // 12)
                            # Handle end-of-month cases (e.g. Jan 31 -> Feb 28/29)
                            _, last_day = calendar.monthrange(next_year, next_month)
                            day = min(current_date_obj.day, last_day)
                            new_target_date = datetime(next_year, next_month, day)
                            task.due_date = new_target_date.strftime("%Y-%m-%d")
                    else:
                        # For non-recurring tasks, move the due date to the reference date
                        # and set time to end of day to give user full day to complete
                        task.due_date = new_date
                        task.due_time = "23:59"

                    count += 1
            except ValueError:
                continue

        return count

    def batch_reschedule_overdue(self, new_datetime: str) -> int:
        """Move all overdue tasks to a new date and time.

        Args:
            new_datetime: The datetime to move tasks to (YYYY-MM-DD HH:MM).

        Returns:
            Number of tasks rescheduled.
        """
        try:
            # Parse the new datetime
            new_dt = datetime.strptime(new_datetime, "%Y-%m-%d %H:%M")
            new_date = new_dt.strftime("%Y-%m-%d")
            new_time = new_dt.strftime("%H:%M")
        except ValueError:
            raise TodoServiceError("Invalid datetime format. Expected YYYY-MM-DD HH:MM.")

        now = datetime.now()
        count = 0

        for task in self._tasks:
            if not task.due_date:  # Only reschedule tasks that have due dates
                continue

            try:
                due_dt_str = f"{task.due_date} {task.due_time if task.due_time else '00:00'}"
                due_dt = datetime.strptime(due_dt_str, "%Y-%m-%d %H:%M")

                if due_dt < now:  # Only reschedule overdue tasks
                    # Update both date and time
                    task.due_date = new_date
                    task.due_time = new_time
                    # Retain all other metadata and recurrence
                    count += 1
            except ValueError:
                continue

        return count

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[List[str]] = None,
        due_date: Optional[str] = None,
        due_time: Optional[str] = None,
        recurrence: Optional[str] = None,
    ) -> bool:
        """Update task title and/or description.

        Args:
            task_id: The ID of the task to update.
            title: New title (optional).
            description: New description (optional).
            priority: New priority (optional).
            tags: New tags list (optional).
            due_date: New due date (optional).
            due_time: New due time (optional).
            recurrence: New recurrence (optional).

        Returns:
            True if task was updated, False if not found.

        Raises:
            TodoServiceError: If title is provided but empty.
        """
        if title is not None and not title.strip():
            raise TodoServiceError("Title cannot be empty.")

        task = self.get_task(task_id)
        if task is None:
            return False

        if title is not None:
            task.title = title.strip()
        if description is not None:
            task.description = description.strip() if description.strip() else None
        if priority is not None:
            task.priority = priority
        if tags is not None:
            task.tags = tags
        if due_date is not None:
            if due_date and not self.validate_date(due_date):
                raise TodoServiceError("Invalid date format. Expected YYYY-MM-DD.")
            task.due_date = due_date
        if due_time is not None:
            if due_time and not self.validate_time(due_time):
                raise TodoServiceError("Invalid time format. Use HH:MM (24-hour) or H:MM AM/PM (12-hour) format.")

            # Convert time to 24-hour format for storage
            if due_time:
                due_time = self.parse_time_to_24h(due_time)
            task.due_time = due_time
        # Process recurrence field - always update when parameter is provided, even if None
        task.recurrence = recurrence
        if recurrence:  # If recurrence has a value (not None)
            task.is_root = True
            if task.root_id is None:
                task.root_id = task.id
        else:  # If recurrence is None
            task.is_root = False
            task.root_id = None  # Reset root_id when recurrence is removed

        return True

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Adds the deleted ID to the pool for reuse.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if task was deleted, False if not found.
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                self._available_ids.append(task_id)  # Reuse this ID later
                self._available_ids.sort()  # Keep smallest first
                return True
        return False

    def toggle_complete(self, task_id: int) -> bool:
        """Toggle task completion status.

        If a recurring task is completed, automatically create the next instance.

        Args:
            task_id: The ID of the task to toggle.

        Returns:
            True if task was toggled, False if not found.
        """
        task = self.get_task(task_id)
        if task is None:
            return False

        task.completed = not task.completed

        # If task was just completed and is recurring, clone it
        if task.completed and task.recurrence and task.due_date:
            self._clone_recurring_task(task)

        return True

    def _clone_recurring_task(self, task: Task) -> Optional[Task]:
        """Create the next instance of a recurring task.

        Args:
            task: The task instance to clone from.

        Returns:
            The newly created Task instance, or None if cloning not applicable.
        """
        if not task.recurrence or not task.due_date:
            return None

        next_date = self.get_next_date(task.due_date, task.recurrence)

        # Create new task instance
        if self._available_ids:
            new_id = self._available_ids.pop(0)
        else:
            new_id = self._next_id
            self._next_id += 1

        new_task = Task(
            id=new_id,
            title=task.title,
            description=task.description,
            completed=False,
            priority=task.priority,
            tags=task.tags.copy(),
            due_date=next_date,
            due_time=task.due_time,
            recurrence=task.recurrence,
            is_root=False,
            root_id=task.root_id if task.root_id else task.id
        )

        self._tasks.append(new_task)
        return new_task

    def _clone_recurring_task_directly(self, task: Task) -> Optional[Task]:
        """Create the next instance of a recurring task without changing the original task's completion status.

        This is used for rescheduling where we want to clone the task without marking the original as completed.

        Args:
            task: The task instance to clone from.

        Returns:
            The newly created Task instance, or None if cloning not applicable.
        """
        if not task.recurrence or not task.due_date:
            return None

        next_date = self.get_next_date(task.due_date, task.recurrence)

        # Create new task instance
        if self._available_ids:
            new_id = self._available_ids.pop(0)
        else:
            new_id = self._next_id
            self._next_id += 1

        new_task = Task(
            id=new_id,
            title=task.title,
            description=task.description,
            completed=False,  # New recurring task is always incomplete
            priority=task.priority,
            tags=task.tags.copy(),
            due_date=next_date,
            due_time=task.due_time,
            recurrence=task.recurrence,
            is_root=False,
            root_id=task.root_id if task.root_id else task.id
        )

        self._tasks.append(new_task)
        return new_task
