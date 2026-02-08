# Phase V Backend Fixes - Recurring Tasks & Dapr Integration

## Issues Fixed

### 1. UUID JSON Serialization Error ✓
**Problem**: `Object of type UUID is not JSON serializable` when publishing events to task-events/task-updates

**Root Cause**: Task.id and Task.user_id are UUID objects, and `json.dumps()` cannot serialize them directly.

**Solution Applied**:
- Updated `src/core/dapr_client.py` - `publish_event()` method
  - Convert `user_id` and `task_id` UUID fields to strings before JSON serialization
  - Convert `timestamp` datetime to ISO format string
  - Added detailed logging for debugging

**Files Modified**:
- `src/core/dapr_client.py` (lines 25-73)

---

### 2. Dapr Pub/Sub Connection Failures ✓
**Problem**: "All connection attempts failed" when publishing to Dapr Pub/Sub

**Root Causes**:
- Incorrect pubsub component name in URL (`pubsub` instead of `kafka-pubsub`)
- Missing timeout and error handling
- No connection error diagnostics

**Solution Applied**:
- Updated `src/core/dapr_client.py` - `publish_event()` method
  - Changed URL from `/v1.0/publish/pubsub/{topic}` to `/v1.0/publish/kafka-pubsub/{topic}`
  - Added 10-second timeout to HTTP requests
  - Added specific exception handling for `httpx.TimeoutException` and `httpx.ConnectError`
  - Added detailed error messages with troubleshooting hints

- Updated `src/services/task_service.py` - `toggle_completion()` method
  - Changed URL to use correct pubsub component name: `kafka-pubsub`
  - Added timeout handling (10 seconds)
  - Added connection error handling with diagnostic messages
  - Enhanced logging with `[RECURRING]` prefix

**Files Modified**:
- `src/core/dapr_client.py` (lines 25-73)
- `src/services/task_service.py` (lines 487-530)

---

### 3. Recurring Task Engine Implementation ✓
**Problem**: No automatic creation of next recurring task when a recurring task is completed

**Solution Applied**:

#### A. Event Publishing (in task_service.py)
- When a recurring task is marked complete, publish "completed" event to "task-events" topic
- Event payload includes:
  ```json
  {
    "event_type": "completed",
    "task_id": "uuid-string",
    "user_id": "uuid-string",
    "recurrence_pattern": "daily|weekly|monthly|yearly",
    "due_date": "ISO-8601-datetime",
    "title": "task title",
    "description": "task description",
    "priority": "low|medium|high",
    "tags": "comma,separated,tags",
    "remind_at": "ISO-8601-datetime"
  }
  ```

#### B. Event Consumer (in recurring_consumer.py)
- Enhanced `create_next_recurring_task()` function:
  - Properly converts string UUIDs to UUID objects
  - Parses ISO format datetime strings
  - Calculates next due date using `calculate_next_due_date()` utility
  - Fetches original task from database
  - Creates new task with same properties but:
    - Updated `due_date` (calculated based on recurrence pattern)
    - `is_completed = False` (new task starts incomplete)
    - `parent_task_id` set to original task ID
    - `is_recurring = True` (keeps recurring for future occurrences)
  - Comprehensive error handling and logging

- Created `handle_task_event()` function:
  - Entry point for FastAPI endpoint
  - Creates database session
  - Processes event and returns Dapr-compatible response
  - Returns `{"status": "SUCCESS"}` on success or `{"status": "RETRY"}` on error

#### C. Dapr Subscription Endpoint (in events.py)
- Added `/dapr/subscribe` GET endpoint:
  - Required by Dapr to discover subscriptions
  - Returns subscription configuration:
    ```json
    [
      {
        "pubsubname": "kafka-pubsub",
        "topic": "task-events",
        "route": "/events/task-events"
      }
    ]
    ```

- Added `/events/task-events` POST endpoint:
  - Receives events from Dapr pub/sub
  - Extracts event data from Dapr's wrapper format
  - Calls `handle_task_event()` to process the event
  - Returns Dapr-compatible response

**Files Modified**:
- `src/services/task_service.py` (lines 487-530)
- `src/services/recurring_consumer.py` (entire file rewritten)
- `src/routers/events.py` (entire file rewritten)

---

## Logging Enhancements

All functions now include comprehensive logging with prefixes for easy filtering:

- `[DAPR]` - Dapr client operations
- `[RECURRING]` - Recurring task event publishing
- `[RECURRING_CONSUMER]` - Recurring task consumer operations
- `[DAPR_SUBSCRIBE]` - Dapr subscription endpoint
- `[TASK_EVENTS]` - Task event handler endpoint

---

## Testing Instructions

### Prerequisites
1. Ensure Dapr is initialized: `dapr init`
2. Ensure Redis is running (used by Dapr for pub/sub)
3. Ensure PostgreSQL/Neon database is accessible

### Test Recurring Task Flow

1. **Start the FastAPI backend with Dapr sidecar**:
   ```bash
   cd phase-V-cloud-deployment/backend
   dapr run --app-id todo-backend --app-port 8000 --dapr-http-port 3500 --components-path ./dapr/components -- uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Verify Dapr subscription**:
   ```bash
   curl http://localhost:8000/dapr/subscribe
   ```
   Expected output:
   ```json
   [
     {
       "pubsubname": "kafka-pubsub",
       "topic": "task-events",
       "route": "/events/task-events"
     }
   ]
   ```

3. **Create a recurring task**:
   ```bash
   curl -X POST http://localhost:8000/api/tasks \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Daily standup",
       "description": "Team standup meeting",
       "isRecurring": true,
       "recurrencePattern": "daily",
       "dueDate": "2024-02-08T09:00:00Z"
     }'
   ```

4. **Mark the task as complete**:
   ```bash
   curl -X PATCH http://localhost:8000/api/tasks/{task_id}/complete \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"completed": true}'
   ```

5. **Check logs for recurring task creation**:
   - Look for `[RECURRING]` logs showing event publication
   - Look for `[TASK_EVENTS]` logs showing event reception
   - Look for `[RECURRING_CONSUMER]` logs showing next task creation

6. **Verify next task was created**:
   ```bash
   curl http://localhost:8000/api/tasks \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```
   - Should see a new task with the same title
   - New task should have `due_date` = original `due_date` + 1 day (for daily)
   - New task should have `is_completed = false`
   - New task should have `parent_task_id` = original task ID

### Troubleshooting

**If events are not being received**:
1. Check Dapr sidecar is running: `dapr list`
2. Check Dapr components are loaded: `curl http://localhost:3500/v1.0/metadata`
3. Check Redis is running: `redis-cli ping`
4. Check backend logs for `[DAPR]` connection errors

**If UUID serialization errors occur**:
1. Check logs for the exact error message
2. Verify all UUID fields are converted to strings in event payloads
3. Check `src/core/dapr_client.py` has the UUID conversion logic

**If next task is not created**:
1. Check `[RECURRING_CONSUMER]` logs for errors
2. Verify database connection is working
3. Check original task exists in database
4. Verify `recurrence_pattern` is valid (daily, weekly, monthly, yearly)

---

## Recurrence Pattern Logic

The `calculate_next_due_date()` function in `src/utils/recurring_utils.py` calculates the next due date:

- **daily**: current_due_date + 1 day
- **weekly**: current_due_date + 7 days
- **monthly**: current_due_date + 30 days
- **yearly**: current_due_date + 365 days

If no due date is provided, it defaults to tomorrow.

---

## Architecture Flow

```
1. User marks recurring task as complete
   ↓
2. task_service.toggle_completion() publishes event to Dapr
   ↓
3. Dapr receives event and forwards to /events/task-events endpoint
   ↓
4. events.handle_task_events() extracts event data
   ↓
5. recurring_consumer.handle_task_event() processes event
   ↓
6. recurring_consumer.create_next_recurring_task() creates new task
   ↓
7. New task saved to database with updated due_date
```

---

## Next Steps

1. **Add Dapr component configuration** if not already present:
   - Create `dapr/components/kafka-pubsub.yaml` with Redis configuration
   - Ensure component name matches `kafka-pubsub`

2. **Add integration tests** for recurring task flow

3. **Add monitoring** for event processing failures

4. **Consider adding**:
   - Dead letter queue for failed events
   - Event replay mechanism
   - Metrics for event processing latency
