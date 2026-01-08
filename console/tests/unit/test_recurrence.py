"""Unit tests for task recurrence logic."""

import pytest
from datetime import datetime
from src.todo_service import TodoService


def test_validate_time():
    service = TodoService()
    assert service.validate_time("14:30") is True
    assert service.validate_time("00:00") is True
    assert service.validate_time("23:59") is True
    assert service.validate_time("24:00") is False
    assert service.validate_time("14:60") is False
    assert service.validate_time("abc") is False
    assert service.validate_time(None) is True


def test_date_increments():
    service = TodoService()

    # Daily
    assert service.get_next_date("2023-12-31", "Daily") == "2024-01-01"

    # Weekly
    assert service.get_next_date("2023-12-25", "Weekly") == "2024-01-01"

    # Monthly - Normal
    assert service.get_next_date("2023-01-15", "Monthly") == "2023-02-15"

    # Monthly - End of month
    assert service.get_next_date("2023-01-31", "Monthly") == "2023-02-28"
    assert service.get_next_date("2024-01-31", "Monthly") == "2024-02-29"  # Leap year

    # Monthly - December to January
    assert service.get_next_date("2023-12-31", "Monthly") == "2024-01-31"


def test_recurrence_cloning():
    from datetime import datetime, timedelta
    service = TodoService()
    # Use a future date to avoid auto-cloning interference
    future_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    next_date = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')

    task = service.add_task(
        title="Workout",
        due_date=future_date,
        recurrence="Daily"
    )

    # Initial task should be root
    assert task.is_root is True
    assert task.root_id == task.id
    assert task.completed is False

    # Mark complete should trigger cloning
    service.toggle_complete(task.id)
    assert task.completed is True

    # Check for cloned task
    all_tasks = service.get_all_tasks()
    assert len(all_tasks) == 2

    cloned = all_tasks[1]
    assert cloned.title == "Workout"
    assert cloned.due_date == next_date
    assert cloned.completed is False
    assert cloned.is_root is False
    assert cloned.root_id == task.id


def test_batch_reschedule_overdue_functionality():
    from datetime import datetime, timedelta
    service = TodoService()
    # Create an overdue recurring task
    past_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    task = service.add_task(
        title="Overdue Task",
        due_date=past_date,
        due_time="10:00",
        recurrence="Daily"
    )

    # At this point, no auto-cloning should happen
    all_tasks = service.get_all_tasks()
    assert len(all_tasks) == 1  # Only original task, no auto-cloning

    # Now test the new batch reschedule functionality
    new_datetime = datetime.now().strftime('%Y-%m-%d %H:%M')
    count = service.batch_reschedule_overdue(new_datetime)

    # Should reschedule the overdue task
    assert count == 1

    # Check that the task has been rescheduled to the new date/time
    all_tasks_after = service.get_all_tasks()
    rescheduled_task = all_tasks_after[0]

    # The due date and time should be updated to the new values
    new_date = new_datetime.split(' ')[0]
    new_time = new_datetime.split(' ')[1]
    assert rescheduled_task.due_date == new_date
    assert rescheduled_task.due_time == new_time
    # Other metadata should be preserved
    assert rescheduled_task.title == "Overdue Task"
    assert rescheduled_task.recurrence == "Daily"
