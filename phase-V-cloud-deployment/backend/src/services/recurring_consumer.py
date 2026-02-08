"""
Recurring task consumer service that listens to Dapr events and creates new task instances for recurring tasks.
"""
import asyncio
from datetime import datetime
from typing import Dict, Any
from uuid import UUID
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Task
from src.core.database import async_session  # Use existing session factory
from src.utils.recurring_utils import calculate_next_due_date


async def create_next_recurring_task(event_data: Dict[str, Any], db: AsyncSession) -> None:
    """
    Create the next recurring task instance based on the event data.

    Args:
        event_data: The event data containing task information
        db: Database session
    """
    from datetime import timezone

    # Extract data from event
    task_id_str = event_data.get("task_id")
    user_id_str = event_data.get("user_id")
    recurrence_pattern = event_data.get("recurrence_pattern")
    due_date_str = event_data.get("due_date")

    print(f"[RECURRING_CONSUMER] ========== PROCESSING RECURRING TASK ==========")
    print(f"[RECURRING_CONSUMER] Task ID: {task_id_str}")
    print(f"[RECURRING_CONSUMER] Recurrence pattern: {recurrence_pattern}")

    # Convert string IDs to UUIDs
    try:
        task_id = UUID(task_id_str)
        user_id = UUID(user_id_str)
    except (ValueError, TypeError) as e:
        print(f"[RECURRING_CONSUMER] ✗ Error converting IDs to UUID: {e}")
        return

    # Parse due date if provided - ensure timezone-aware
    current_due_date = None
    if due_date_str:
        try:
            current_due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
            # CRITICAL: Ensure timezone-aware (UTC)
            if current_due_date.tzinfo is None:
                print(f"[RECURRING_CONSUMER] WARNING: Parsed due_date was naive, forcing UTC")
                current_due_date = current_due_date.replace(tzinfo=timezone.utc)
            print(f"[RECURRING_CONSUMER] Current due date: {current_due_date}, tzinfo: {current_due_date.tzinfo}")
        except (ValueError, TypeError) as e:
            print(f"[RECURRING_CONSUMER] ✗ Could not parse due date: {due_date_str}, error: {e}")

    # Calculate next due date (will be timezone-aware)
    next_due_date = calculate_next_due_date(current_due_date, recurrence_pattern)
    print(f"[RECURRING_CONSUMER] Next due date: {next_due_date}, tzinfo: {next_due_date.tzinfo}")

    try:
        # Get the original task to copy its properties
        result = await db.execute(select(Task).where(Task.id == task_id))
        original_task = result.scalar_one_or_none()

        if not original_task:
            print(f"[RECURRING_CONSUMER] ✗ Original task {task_id} not found, skipping recurring task creation")
            return

        print(f"[RECURRING_CONSUMER] Found original task: {original_task.title}")

        # Use original_task.due_date as base for next_due calculation (not completed_at)
        base_due_date = original_task.due_date if original_task.due_date else current_due_date

        # Make base_due_date timezone-aware for calculation
        if base_due_date and base_due_date.tzinfo is None:
            base_due_date = base_due_date.replace(tzinfo=timezone.utc)

        print(f"[RECURRING_CONSUMER] Base due_date for calculation: {base_due_date}")

        # Calculate next_due_date inline (preserves timezone)
        if recurrence_pattern == "daily":
            from datetime import timedelta
            next_due_date = base_due_date + timedelta(days=1)
        elif recurrence_pattern == "weekly":
            from datetime import timedelta
            next_due_date = base_due_date + timedelta(weeks=1)
        elif recurrence_pattern == "monthly":
            try:
                from dateutil.relativedelta import relativedelta
                next_due_date = base_due_date + relativedelta(months=1)
            except ImportError:
                from datetime import timedelta
                next_due_date = base_due_date + timedelta(days=30)
        elif recurrence_pattern == "yearly":
            try:
                from dateutil.relativedelta import relativedelta
                next_due_date = base_due_date + relativedelta(years=1)
            except ImportError:
                from datetime import timedelta
                next_due_date = base_due_date + timedelta(days=365)
        else:
            from datetime import timedelta
            next_due_date = base_due_date + timedelta(days=1)

        print(f"[RECURRING_CONSUMER] Calculated next_due_date: {next_due_date}, tzinfo: {next_due_date.tzinfo}")

        # Calculate next remind_at if original task had one
        next_remind_at = None

        if original_task.remind_at is not None and original_task.due_date is not None:
            print(f"[RECURRING_CONSUMER] Original task has remind_at, calculating next remind_at...")

            # Make timezone-aware for calculation
            original_remind_at = original_task.remind_at
            if original_remind_at.tzinfo is None:
                original_remind_at = original_remind_at.replace(tzinfo=timezone.utc)

            original_due_date = original_task.due_date
            if original_due_date.tzinfo is None:
                original_due_date = original_due_date.replace(tzinfo=timezone.utc)

            # Calculate offset: how much before/after due_date is remind_at
            remind_offset = original_due_date - original_remind_at

            print(f"[RECURRING_CONSUMER] Original due_date: {original_due_date}")
            print(f"[RECURRING_CONSUMER] Original remind_at: {original_remind_at}")
            print(f"[RECURRING_CONSUMER] Remind offset (due - remind): {remind_offset}")

            # Apply same offset to next_due_date
            next_remind_at = next_due_date - remind_offset

            print(f"[RECURRING_CONSUMER] Next remind_at (before making naive): {next_remind_at}, tzinfo: {next_remind_at.tzinfo}")
        else:
            print(f"[RECURRING_CONSUMER] Original task has no remind_at or due_date, next task will have no remind_at")

        # CRITICAL: Make all datetimes NAIVE before DB insert (PostgreSQL expects TIMESTAMP WITHOUT TIME ZONE)
        next_due_date_naive = next_due_date.replace(tzinfo=None) if next_due_date and next_due_date.tzinfo else next_due_date
        next_remind_at_naive = next_remind_at.replace(tzinfo=None) if next_remind_at and next_remind_at.tzinfo else next_remind_at

        print(f"[RECURRING_CONSUMER] ========== MAKING DATETIMES NAIVE FOR DB ==========")
        print(f"[RECURRING_CONSUMER] next_due_date_naive: {next_due_date_naive}, tzinfo: {next_due_date_naive.tzinfo if next_due_date_naive else None}")
        print(f"[RECURRING_CONSUMER] next_remind_at_naive: {next_remind_at_naive}, tzinfo: {next_remind_at_naive.tzinfo if next_remind_at_naive else None}")

        # IDEMPOTENCY CHECK: Check if a task with the same parent_task_id and due_date already exists
        print(f"[RECURRING_CONSUMER] Processing task.completed for task_id: {task_id}")
        existing_check = await db.execute(
            select(Task).where(
                Task.parent_task_id == original_task.id,
                Task.due_date == next_due_date_naive
            )
        )
        existing_task = existing_check.scalar_one_or_none()

        if existing_task:
            print(f"[RECURRING_CONSUMER] Found existing next task with due_date {next_due_date_naive} → skipping")
            print(f"[RECURRING_CONSUMER] Duplicate next task skipped for due_date {next_due_date_naive}")
            print(f"[RECURRING_CONSUMER] ================================================")
            return

        # Create a new task with the same properties but updated due date
        new_task = Task(
            title=original_task.title,
            description=original_task.description,
            user_id=original_task.user_id,
            due_date=next_due_date_naive,  # NAIVE datetime for DB
            priority=original_task.priority,
            tags=original_task.tags,
            is_recurring=True,
            recurrence_pattern=original_task.recurrence_pattern,
            remind_at=next_remind_at_naive,  # NAIVE datetime for DB
            parent_task_id=original_task.id,
            is_completed=False
        )

        print(f"[RECURRING_CONSUMER] ========== NEW TASK DETAILS (BEFORE COMMIT) ==========")
        print(f"[RECURRING_CONSUMER] Title: {new_task.title}")
        print(f"[RECURRING_CONSUMER] Due date: {new_task.due_date}, tzinfo: {new_task.due_date.tzinfo if new_task.due_date else None}")
        print(f"[RECURRING_CONSUMER] Remind at: {new_task.remind_at}, tzinfo: {new_task.remind_at.tzinfo if new_task.remind_at else None}")
        print(f"[RECURRING_CONSUMER] Is completed: {new_task.is_completed}")
        print(f"[RECURRING_CONSUMER] Parent task ID: {new_task.parent_task_id}")
        print(f"[RECURRING_CONSUMER] ==========================================")

        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)

        print(f"[RECURRING_CONSUMER] ✓ Successfully created next recurring task {new_task.id}")
        print(f"[RECURRING_CONSUMER] ================================================")

    except Exception as e:
        print(f"[RECURRING_CONSUMER] ✗ Error creating next recurring task: {str(e)}")
        import traceback
        traceback.print_exc()
        await db.rollback()
        print(f"[RECURRING_CONSUMER] ================================================")


async def process_dapr_event(payload: Dict[str, Any], db: AsyncSession) -> None:
    """
    Process incoming Dapr event for recurring tasks.

    Args:
        payload: The event payload from Dapr
        db: Database session
    """
    event_type = payload.get("event_type")

    print(f"[RECURRING_CONSUMER] Received event type: {event_type}")

    # Fix: Handle both "task.completed" (new format) and "completed" (legacy)
    if event_type in ["task.completed", "completed"]:
        await create_next_recurring_task(payload, db)
    else:
        print(f"[RECURRING_CONSUMER] Unknown event type: {event_type}, ignoring")
        print(f"[RECURRING_CONSUMER] Expected 'task.completed' or 'completed'")


# FastAPI endpoint handler for Dapr subscription
async def handle_task_event(event_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Handle incoming task events from Dapr pub/sub.
    This function is called by the FastAPI endpoint.

    Args:
        event_data: The event data from Dapr

    Returns:
        Response dictionary for Dapr
    """
    print(f"[RECURRING_CONSUMER] Received task event from Dapr")
    print(f"[RECURRING_CONSUMER] Event data: {event_data}")

    # Fix: Use existing async_session factory instead of creating new engine
    async with async_session() as db:
        try:
            await process_dapr_event(event_data, db)
            return {"status": "SUCCESS"}
        except Exception as e:
            print(f"[RECURRING_CONSUMER] Error processing event: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"status": "RETRY"}


async def start_recurring_consumer():
    """
    Start the recurring task consumer service.
    This function would typically subscribe to Dapr pubsub events in a real implementation.
    For this implementation, we'll simulate the event processing.
    """
    print("[RECURRING_CONSUMER] Starting recurring task consumer service...")
    print("[RECURRING_CONSUMER] Waiting for Dapr to send events to /dapr/subscribe endpoint")
    print("[RECURRING_CONSUMER] Recurring task consumer service started and listening for events")


if __name__ == "__main__":
    # For testing purposes
    asyncio.run(start_recurring_consumer())