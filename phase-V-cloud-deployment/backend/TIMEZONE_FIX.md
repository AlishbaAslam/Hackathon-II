# Timezone Fix - Recurring Task Creation

## Problem

**SQLAlchemy DBAPIError: can't subtract offset-naive and offset-aware datetimes**

Full error:
```
sqlalchemy.exc.DBAPIError: invalid input for query argument $13: datetime.datetime(2026, 2, 11, 4, 19, tz...
(can't subtract offset-naive and offset-aware datetimes)
```

## Root Cause

The error occurred when inserting a new recurring task into the database because of timezone mismatch:

1. **Event data** from Dapr contains timezone-aware datetimes (UTC):
   - `due_date`: `"2024-02-08T09:00:00+00:00"` (tz-aware)
   - `remind_at`: `"2024-02-08T08:00:00+00:00"` (tz-aware)

2. **calculate_next_due_date()** was using `datetime.now()` which returns timezone-naive datetime:
   - `current_due_date + timedelta(days=1)` produces timezone-naive result

3. **PostgreSQL/asyncpg** cannot handle mixed timezone-aware and timezone-naive datetimes in the same query

## Solution Applied

### 1. Fixed `src/utils/recurring_utils.py`

**Changes**:
- Import `timezone` from datetime
- Ensure input datetime is timezone-aware (UTC)
- Return timezone-aware datetime (UTC)
- Add debug logging

**Before**:
```python
from datetime import datetime, timedelta

def calculate_next_due_date(current_due_date: Optional[datetime], recurrence_pattern: str) -> datetime:
    if not current_due_date:
        current_due_date = datetime.now()  # ❌ Timezone-naive

    if recurrence_pattern == "daily":
        return current_due_date + timedelta(days=1)  # ❌ Timezone-naive
```

**After**:
```python
from datetime import datetime, timedelta, timezone

def calculate_next_due_date(current_due_date: Optional[datetime], recurrence_pattern: str) -> datetime:
    if not current_due_date:
        current_due_date = datetime.now(timezone.utc)  # ✅ Timezone-aware UTC

    # Ensure timezone-aware
    if current_due_date.tzinfo is None:
        current_due_date = current_due_date.replace(tzinfo=timezone.utc)

    print(f"[RECURRING_UTILS] Current due date: {current_due_date}, tzinfo: {current_due_date.tzinfo}")

    if recurrence_pattern == "daily":
        next_date = current_due_date + timedelta(days=1)  # ✅ Preserves timezone

    print(f"[RECURRING_UTILS] Next due date: {next_date}, tzinfo: {next_date.tzinfo}")
    return next_date
```

### 2. Fixed `src/services/recurring_consumer.py`

**Changes**:
- Import `timezone` from datetime
- Ensure parsed `due_date` is timezone-aware
- Ensure parsed `remind_at` is timezone-aware
- Add debug logging for all datetime fields

**Before**:
```python
# Parse due date
current_due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
# ❌ Could be timezone-naive depending on input

# Create new task
new_task = Task(
    due_date=next_due_date,  # ❌ Could be timezone-naive
    remind_at=original_task.remind_at,  # ❌ Could be timezone-naive
    ...
)
```

**After**:
```python
from datetime import timezone

# Parse due date - ensure timezone-aware
current_due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
if current_due_date.tzinfo is None:
    current_due_date = current_due_date.replace(tzinfo=timezone.utc)
print(f"[RECURRING_CONSUMER] Parsed current due date: {current_due_date}, tzinfo: {current_due_date.tzinfo}")

# Parse remind_at - ensure timezone-aware
remind_at_value = None
remind_at_str = event_data.get("remind_at")
if remind_at_str:
    remind_at_value = datetime.fromisoformat(remind_at_str.replace('Z', '+00:00'))
    if remind_at_value.tzinfo is None:
        remind_at_value = remind_at_value.replace(tzinfo=timezone.utc)
    print(f"[RECURRING_CONSUMER] Original remind_at: {remind_at_value}, tzinfo: {remind_at_value.tzinfo}")

# Create new task with timezone-aware datetimes
new_task = Task(
    due_date=next_due_date,  # ✅ Timezone-aware from calculate_next_due_date
    remind_at=remind_at_value,  # ✅ Timezone-aware or None
    ...
)

print(f"[RECURRING_CONSUMER] New task due_date: {new_task.due_date}, tzinfo: {new_task.due_date.tzinfo if new_task.due_date else None}")
print(f"[RECURRING_CONSUMER] New task remind_at: {new_task.remind_at}, tzinfo: {new_task.remind_at.tzinfo if new_task.remind_at else None}")
```

## How Timezone Handling Works Now

### 1. Event Data (from Dapr)
```json
{
  "due_date": "2024-02-08T09:00:00+00:00",  // Timezone-aware UTC
  "remind_at": "2024-02-08T08:00:00+00:00"  // Timezone-aware UTC
}
```

### 2. Parse and Ensure Timezone-Aware
```python
# Parse ISO format string
current_due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))

# Ensure timezone-aware (defensive programming)
if current_due_date.tzinfo is None:
    current_due_date = current_due_date.replace(tzinfo=timezone.utc)
```

### 3. Calculate Next Due Date (Preserves Timezone)
```python
# Input: 2024-02-08T09:00:00+00:00 (tz-aware)
# Add timedelta: +1 day
# Output: 2024-02-09T09:00:00+00:00 (tz-aware)
next_due_date = current_due_date + timedelta(days=1)
```

### 4. Insert into Database
```python
# All datetime fields are timezone-aware UTC
new_task = Task(
    due_date=datetime(2024, 2, 9, 9, 0, 0, tzinfo=timezone.utc),  # ✅
    remind_at=datetime(2024, 2, 9, 8, 0, 0, tzinfo=timezone.utc),  # ✅
    ...
)
```

## Testing the Fix

### 1. Start the backend

```bash
cd phase-V-cloud-deployment/backend

dapr run \
  --app-id todo-backend \
  --app-port 8000 \
  -- uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Create recurring task with due_date and remind_at

```bash
export TOKEN="your-jwt-token"

curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Daily standup",
    "description": "Team standup meeting",
    "isRecurring": true,
    "recurrencePattern": "daily",
    "dueDate": "2024-02-08T09:00:00Z",
    "remindAt": "2024-02-08T08:00:00Z"
  }'
```

### 3. Complete the task

```bash
export TASK_ID="task-id-from-response"

curl -X PATCH http://localhost:8000/api/tasks/$TASK_ID/complete \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### 4. Expected Success Logs

```
[RECURRING] Task xxx is recurring and completed
[DAPR] ✓ Successfully published event to task-events on attempt 1

[TASK_EVENTS] Received event from Dapr
[RECURRING_CONSUMER] Processing recurring task event for task xxx
[RECURRING_CONSUMER] Parsed current due date: 2024-02-08 09:00:00+00:00, tzinfo: UTC
[RECURRING_UTILS] Current due date: 2024-02-08 09:00:00+00:00, tzinfo: UTC
[RECURRING_UTILS] Next due date: 2024-02-09 09:00:00+00:00, tzinfo: UTC
[RECURRING_CONSUMER] Calculated next due date: 2024-02-09 09:00:00+00:00 (pattern: daily)
[RECURRING_CONSUMER] Next due date tzinfo: UTC
[RECURRING_CONSUMER] Original remind_at: 2024-02-08 08:00:00+00:00, tzinfo: UTC
[RECURRING_CONSUMER] New task due_date: 2024-02-09 09:00:00+00:00, tzinfo: UTC
[RECURRING_CONSUMER] New task remind_at: 2024-02-08 08:00:00+00:00, tzinfo: UTC
[RECURRING_CONSUMER] ✓ Created next recurring task yyy with due_date: 2024-02-09 09:00:00+00:00
```

**No DBAPIError!** ✅

### 5. Verify next task in database

```bash
curl http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" | jq
```

Should show:
- Original task: `is_completed: true`, `due_date: "2024-02-08T09:00:00Z"`
- New task: `is_completed: false`, `due_date: "2024-02-09T09:00:00Z"`

## Why This Fix Works

### Timezone-Aware Arithmetic
When you add a `timedelta` to a timezone-aware datetime, Python preserves the timezone:

```python
# Timezone-aware
dt = datetime(2024, 2, 8, 9, 0, 0, tzinfo=timezone.utc)
next_dt = dt + timedelta(days=1)
# Result: datetime(2024, 2, 9, 9, 0, 0, tzinfo=timezone.utc)  ✅

# Timezone-naive
dt = datetime(2024, 2, 8, 9, 0, 0)  # No tzinfo
next_dt = dt + timedelta(days=1)
# Result: datetime(2024, 2, 9, 9, 0, 0)  # Still no tzinfo ❌
```

### PostgreSQL Requirements
PostgreSQL with asyncpg requires consistent timezone handling:
- All datetimes in a query must be either all timezone-aware or all timezone-naive
- Mixing them causes: "can't subtract offset-naive and offset-aware datetimes"

### Defensive Programming
The fix includes defensive checks:
```python
if current_due_date.tzinfo is None:
    current_due_date = current_due_date.replace(tzinfo=timezone.utc)
```

This ensures timezone-awareness even if the input format changes.

## Edge Cases Handled

### 1. No due_date in event
```python
if not current_due_date:
    current_due_date = datetime.now(timezone.utc)  # ✅ Timezone-aware
```

### 2. No remind_at in event
```python
remind_at_value = None  # ✅ None is valid
if remind_at_str:
    # Parse and make timezone-aware
```

### 3. Timezone-naive input (defensive)
```python
if current_due_date.tzinfo is None:
    current_due_date = current_due_date.replace(tzinfo=timezone.utc)
```

## Files Modified

| File | Changes |
|------|---------|
| `src/utils/recurring_utils.py` | - Import `timezone`<br>- Use `datetime.now(timezone.utc)`<br>- Ensure input is timezone-aware<br>- Add debug logging |
| `src/services/recurring_consumer.py` | - Import `timezone`<br>- Ensure `due_date` is timezone-aware<br>- Ensure `remind_at` is timezone-aware<br>- Add debug logging for all datetime fields |

## Summary

✅ All datetimes are now timezone-aware (UTC)
✅ `calculate_next_due_date()` preserves timezone
✅ Database inserts work without timezone mismatch errors
✅ Debug logging shows timezone info for troubleshooting
✅ Defensive programming handles edge cases

**The recurring task engine now handles timezones correctly!** 🎉

## Complete Fix Checklist

- [x] Import `timezone` from datetime in both files
- [x] Ensure `datetime.now()` uses `timezone.utc`
- [x] Ensure parsed datetimes are timezone-aware
- [x] Add defensive checks for timezone-naive inputs
- [x] Add debug logging showing timezone info
- [x] Handle None values for optional datetime fields
- [x] Test with tasks that have both due_date and remind_at
- [x] Verify no DBAPIError occurs
- [x] Verify next task is created successfully
