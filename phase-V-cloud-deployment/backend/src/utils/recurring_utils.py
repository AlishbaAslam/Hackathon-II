"""
Utility functions for recurring task date calculations.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional

try:
    from dateutil.relativedelta import relativedelta
    HAS_RELATIVEDELTA = True
except ImportError:
    HAS_RELATIVEDELTA = False
    print("[RECURRING_UTILS] Warning: python-dateutil not installed, using timedelta (less accurate for monthly)")


def calculate_next_due_date(current_due_date: Optional[datetime], recurrence_pattern: str) -> datetime:
    """
    Calculate the next due date based on the recurrence pattern.
    Returns timezone-naive datetime for PostgreSQL TIMESTAMP WITHOUT TIME ZONE.

    Args:
        current_due_date: The current due date of the task (can be None)
        recurrence_pattern: The recurrence pattern ('daily', 'weekly', 'monthly', 'yearly')

    Returns:
        datetime: The calculated next due date (timezone-naive)
    """
    # If no due date, set it to now (UTC) then make naive
    if not current_due_date:
        current_due_date = datetime.now(timezone.utc).replace(tzinfo=None)
        print(f"[RECURRING_UTILS] No due date provided, using current time (naive): {current_due_date}")
        return current_due_date

    # Make timezone-aware for calculation if needed
    if current_due_date.tzinfo is None:
        current_due_date = current_due_date.replace(tzinfo=timezone.utc)

    print(f"[RECURRING_UTILS] Input current_due_date: {current_due_date}, tzinfo: {current_due_date.tzinfo}")

    # Calculate next due date based on pattern
    if HAS_RELATIVEDELTA:
        if recurrence_pattern == "daily":
            next_date = current_due_date + relativedelta(days=1)
        elif recurrence_pattern == "weekly":
            next_date = current_due_date + relativedelta(weeks=1)
        elif recurrence_pattern == "monthly":
            next_date = current_due_date + relativedelta(months=1)
        elif recurrence_pattern == "yearly":
            next_date = current_due_date + relativedelta(years=1)
        else:
            print(f"[RECURRING_UTILS] Unknown pattern '{recurrence_pattern}', defaulting to daily")
            next_date = current_due_date + relativedelta(days=1)
    else:
        # Fallback to timedelta
        if recurrence_pattern == "daily":
            next_date = current_due_date + timedelta(days=1)
        elif recurrence_pattern == "weekly":
            next_date = current_due_date + timedelta(weeks=1)
        elif recurrence_pattern == "monthly":
            next_date = current_due_date + timedelta(days=30)
        elif recurrence_pattern == "yearly":
            next_date = current_due_date + timedelta(days=365)
        else:
            print(f"[RECURRING_UTILS] Unknown pattern '{recurrence_pattern}', defaulting to daily")
            next_date = current_due_date + timedelta(days=1)

    # CRITICAL: Make naive for PostgreSQL TIMESTAMP WITHOUT TIME ZONE
    next_date_naive = next_date.replace(tzinfo=None) if next_date.tzinfo else next_date

    print(f"[RECURRING_UTILS] Output next_due_date (naive): {next_date_naive}, tzinfo: {next_date_naive.tzinfo}")

    return next_date_naive