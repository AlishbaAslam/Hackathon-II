"""
Type definitions for the recurring task service.
"""
from enum import Enum


class RecurrencePattern(str, Enum):
    """
    Recurrence pattern enumeration.
    """
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"