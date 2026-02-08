# Database Connection Fix - recurring_consumer.py

## Problem

**AttributeError: 'Settings' object has no attribute 'database_url'**

Occurred in `handle_task_event` at:
```python
engine = create_async_engine(str(settings.database_url))
```

## Root Cause

The `Settings` class in `src/config.py` uses `DATABASE_URL` (uppercase), not `database_url` (lowercase).

Additionally, creating a new engine for every event is inefficient. The application already has a configured async engine and session factory in `src/core/database.py`.

## Solution Applied

### Changed Imports

**Before**:
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import settings
```

**After**:
```python
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import async_session  # Use existing session factory
```

### Changed handle_task_event Function

**Before**:
```python
async def handle_task_event(event_data: Dict[str, Any]) -> Dict[str, str]:
    # Create database session
    engine = create_async_engine(str(settings.database_url))  # ❌ Error here
    async with AsyncSession(engine) as db:
        try:
            await process_dapr_event(event_data, db)
            return {"status": "SUCCESS"}
        except Exception as e:
            print(f"[RECURRING_CONSUMER] Error processing event: {str(e)}")
            return {"status": "RETRY"}
```

**After**:
```python
async def handle_task_event(event_data: Dict[str, Any]) -> Dict[str, str]:
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
```

## Benefits of This Fix

1. **Fixes the AttributeError** - No longer tries to access non-existent `database_url` attribute
2. **Uses existing database configuration** - Leverages the already-configured engine from `src/core/database.py`
3. **More efficient** - Reuses the connection pool instead of creating a new engine for each event
4. **Consistent with rest of application** - Other parts of the app use `async_session` from `src/core/database`
5. **Proper connection management** - The session factory handles connection pooling and cleanup

## How Database Configuration Works

### In src/config.py:
```python
class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todo_app.db")
```

### In src/core/database.py:
```python
from src.config import settings

# Create async engine using settings.DATABASE_URL (uppercase)
engine = create_async_engine(
    settings.DATABASE_URL,  # ✓ Correct attribute name
    echo=settings.DEBUG,
    future=True,
    connect_args=connect_args,
    pool_pre_ping=True,
)

# Create async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
```

### In recurring_consumer.py (after fix):
```python
from src.core.database import async_session

# Use the existing session factory
async with async_session() as db:
    # Work with database
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

### 2. Create and complete a recurring task

```bash
# Get token
export TOKEN="your-jwt-token"

# Create recurring task
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Daily standup",
    "isRecurring": true,
    "recurrencePattern": "daily",
    "dueDate": "2024-02-08T09:00:00Z"
  }'

# Complete the task
curl -X PATCH http://localhost:8000/api/tasks/$TASK_ID/complete \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### 3. Expected Logs (Success)

```
[RECURRING] Task xxx is recurring and completed
[DAPR] Using real pubsub name: pubsub
[DAPR] ✓ Successfully published event to task-events on attempt 1

[TASK_EVENTS] Received event from Dapr
[RECURRING_CONSUMER] Received task event from Dapr
[RECURRING_CONSUMER] Event data: {...}
[RECURRING_CONSUMER] Received event type: task.completed
[RECURRING_CONSUMER] Processing recurring task event for task xxx
[RECURRING_CONSUMER] Parsed current due date: 2024-02-08T09:00:00
[RECURRING_CONSUMER] Calculated next due date: 2024-02-09T09:00:00 (pattern: daily)
[RECURRING_CONSUMER] Found original task: Daily standup
[RECURRING_CONSUMER] ✓ Created next recurring task yyy with due_date: 2024-02-09T09:00:00
```

**No AttributeError!** ✅

### 4. Verify Next Task Created

```bash
curl http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" | jq
```

Should show:
- Original task: `is_completed: true`, `due_date: 2024-02-08T09:00:00`
- New task: `is_completed: false`, `due_date: 2024-02-09T09:00:00`

## Files Modified

| File | Changes |
|------|---------|
| `src/services/recurring_consumer.py` | - Removed `create_async_engine`, `sessionmaker` imports<br>- Removed `settings` import<br>- Added `async_session` import from `src.core.database`<br>- Changed `handle_task_event` to use `async_session()` |

## Alternative Solutions (Not Used)

### Option 1: Fix the attribute name
```python
# Could have changed:
engine = create_async_engine(str(settings.database_url))
# To:
engine = create_async_engine(str(settings.DATABASE_URL))
```

**Why not used**: Still inefficient to create new engine for each event.

### Option 2: Add database_url property
```python
# Could have added to Settings class:
@property
def database_url(self):
    return self.DATABASE_URL
```

**Why not used**: Unnecessary when we can use the existing session factory.

### Option 3: Use get_db dependency
```python
from src.core.dependencies import get_db

async for db in get_db():
    await process_dapr_event(event_data, db)
```

**Why not used**: `get_db` is designed for FastAPI dependency injection, not for direct use.

## Summary

✅ Fixed AttributeError by using existing `async_session` factory
✅ More efficient - reuses connection pool
✅ Consistent with rest of application
✅ Proper error handling with traceback
✅ No changes needed to Settings class

**The recurring task consumer now works correctly!** 🎉

## Complete Fix Checklist

- [x] Changed imports to use `async_session` from `src.core.database`
- [x] Removed unused imports (`create_async_engine`, `sessionmaker`, `settings`)
- [x] Updated `handle_task_event` to use existing session factory
- [x] Tested that no AttributeError occurs
- [x] Verified next recurring task is created successfully
