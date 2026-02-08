"""
Recurrence logic for calculating next occurrence of recurring tasks.
"""
import logging
from datetime import datetime, timedelta
from typing import Optional

from ...types import RecurrencePattern

logger = logging.getLogger(__name__)


def calculate_next_occurrence(
    current_datetime: datetime,
    recurrence_pattern: RecurrencePattern,
    interval: int = 1
) -> Optional[datetime]:
    """
    Calculate the next occurrence datetime based on the recurrence pattern.

    Args:
        current_datetime: The current datetime to calculate from
        recurrence_pattern: The pattern for recurrence (daily, weekly, monthly, yearly)
        interval: The interval multiplier (e.g., every 2 days, every 3 weeks)

    Returns:
        The calculated next occurrence datetime, or None if invalid pattern
    """
    try:
        if recurrence_pattern == RecurrencePattern.DAILY:
            return current_datetime + timedelta(days=interval)
        elif recurrence_pattern == RecurrencePattern.WEEKLY:
            return current_datetime + timedelta(weeks=interval)
        elif recurrence_pattern == RecurrencePattern.MONTHLY:
            # For monthly recurrence, we need to handle day overflow carefully
            # Add the interval in months by adjusting year and month
            year = current_datetime.year
            month = current_datetime.month + interval

            # Adjust year if month > 12
            while month > 12:
                year += 1
                month -= 12

            # Handle day overflow (e.g., Jan 31 + 1 month should be Feb 28/29, not Mar 3)
            day = min(current_datetime.day, _days_in_month(year, month))

            return current_datetime.replace(year=year, month=month, day=day)
        elif recurrence_pattern == RecurrencePattern.YEARLY:
            # Add the interval in years
            year = current_datetime.year + interval
            # Handle leap year edge cases (Feb 29)
            day = min(current_datetime.day, _days_in_month(year, current_datetime.month))

            return current_datetime.replace(year=year, month=current_datetime.month, day=day)
        else:
            logger.warning(f"Invalid recurrence pattern: {recurrence_pattern}")
            return None
    except Exception as e:
        logger.error(f"Error calculating next occurrence: {str(e)}")
        return None


def _days_in_month(year: int, month: int) -> int:
    """
    Get the number of days in a given month/year.

    Args:
        year: The year
        month: The month (1-12)

    Returns:
        Number of days in the month
    """
    import calendar
    return calendar.monthrange(year, month)[1]


def validate_recurrence_pattern(pattern: str) -> bool:
    """
    Validate if the provided pattern is a valid recurrence pattern.

    Args:
        pattern: The pattern string to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        RecurrencePattern(pattern)
        return True
    except ValueError:
        return False