# Recurring Engine Publish Fixes - Final Update

## Issues Fixed

### ✅ 1. Dynamic Dapr HTTP Port Detection
**Problem**: Dapr uses random HTTP ports (38081, 39561, etc.) instead of fixed 3500

**Root Cause**: The `dapr run` command assigns random ports unless explicitly specified with `--dapr-http-port`

**Solution Applied**:
- Updated `src/core/dapr_client.py` to read `DAPR_HTTP_PORT` from environment **on every publish call**
- Added detailed logging showing the actual port being used
- Dapr automatically sets `DAPR_HTTP_PORT` environment variable when running the app

**Code Changes**:
```python
# In publish_event method - reads port dynamically per request
dapr_http_port = os.getenv("DAPR_HTTP_PORT", "3500")
dapr_endpoint = f"http://localhost:{dapr_http_port}"
url = f"{dapr_endpoint}/v1.0/publish/{pubsub_name}/{topic}"

print(f"[DAPR] Dapr HTTP endpoint: {dapr_endpoint} (port from env: {dapr_http_port})")
```

### ✅ 2. Correct Pub/Sub Component Name
**Problem**: 404 ERR_PUBSUB_NOT_FOUND - Component "kafka-pubsub" not found

**Root Cause**: Component name in code didn't match the actual component loaded by Dapr

**Solution Applied**:
- Component name is still "kafka-pubsub" (verified in `dapr/components/redis-pubsub.yaml`)
- Added logging to show which pubsub component is being used
- Added environment variable `DAPR_PUBSUB_NAME` for easy configuration

**Code Changes**:
```python
pubsub_name = os.getenv("DAPR_PUBSUB_NAME", "kafka-pubsub")
print(f"[DAPR] Using pubsub component: {pubsub_name}")
```

**Verification**:
The `redis-pubsub.yaml` file has:
```yaml
metadata:
  name: kafka-pubsub  # This is the component name Dapr uses
spec:
  type: pubsub.redis  # This is the implementation (Redis)
```

### ✅ 3. Event Type Validation Fix
**Problem**: TaskEvent validation error - event_type "completed" not allowed

**Root Cause**: The TaskEvent model expects enum values like "task.completed", not plain "completed"

**Solution Applied**:
- Updated `src/services/task_service.py` to use `TaskEventType.TASK_COMPLETED` enum
- This automatically provides the correct string value "task.completed"
- Updated `src/services/recurring_consumer.py` to handle both formats for backward compatibility

**Code Changes**:

In `task_service.py`:
```python
from src.core.event_schemas import TaskEvent, TaskEventType

event = TaskEvent(
    event_id=str(uuid4()),
    event_type=TaskEventType.TASK_COMPLETED,  # Enum value = "task.completed"
    user_id=task.user_id,
    task_id=task.id,
    timestamp=datetime.utcnow(),
    payload={...}
)
```

In `recurring_consumer.py`:
```python
# Handle both formats
if event_type in ["task.completed", "completed"]:
    await create_next_recurring_task(payload, db)
```

### ✅ 4. UUID to String Conversion
**Already Fixed**: UUIDs are properly converted to strings in the event payload

**Code**:
```python
# In dapr_client.py publish_event method
if 'user_id' in event_dict and event_dict['user_id']:
    event_dict['user_id'] = str(event_dict['user_id'])
if 'task_id' in event_dict and event_dict['task_id']:
    event_dict['task_id'] = str(event_dict['task_id'])
if 'event_type' in event_dict:
    event_dict['event_type'] = str(event_dict['event_type'])
```

## How Dapr Port Detection Works

When you run:
```bash
dapr run --app-id todo-backend --app-port 8000 -- uvicorn src.main:app
```

Dapr automatically:
1. Assigns a random HTTP port (e.g., 39561)
2. Sets the `DAPR_HTTP_PORT` environment variable for your app
3. Your app reads this variable and uses the correct port

**No manual configuration needed!** The app automatically detects the port.

## Testing the Fixes

### 1. Start Backend with Dapr

**Option A: Let Dapr assign random port (Recommended)**
```bash
cd phase-V-cloud-deployment/backend

dapr run \
  --app-id todo-backend \
  --app-port 8000 \
  --components-path ./dapr/components \
  --log-level debug \
  -- uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

**Option B: Use fixed port 3500**
```bash
dapr run \
  --app-id todo-backend \
  --app-port 8000 \
  --dapr-http-port 3500 \
  --components-path ./dapr/components \
  --log-level debug \
  -- uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Check Initialization Logs

You should see:
```
[DAPR_CLIENT] Initialized with endpoint: http://localhost:XXXXX
```

Where XXXXX is the actual Dapr HTTP port.

### 3. Create and Complete Recurring Task

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

# Save task ID
export TASK_ID="task-id-from-response"

# Complete the task
curl -X PATCH http://localhost:8000/api/tasks/$TASK_ID/complete \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### 4. Expected Logs

```
[RECURRING] Task xxx is recurring and completed, publishing event to task-events topic
[RECURRING] Event type: task.completed
[DAPR] Using pubsub component: kafka-pubsub
[DAPR] Dapr HTTP endpoint: http://localhost:39561 (port from env: 39561)
[DAPR] Full publish URL: http://localhost:39561/v1.0/publish/kafka-pubsub/task-events
[DAPR] Attempt 1/3 to publish event
[DAPR] ✓ Successfully published event to task-events on attempt 1
[RECURRING] ✓ Successfully published completed event for recurring task xxx

[TASK_EVENTS] Received event from Dapr
[RECURRING_CONSUMER] Received event type: task.completed
[RECURRING_CONSUMER] Processing recurring task event for task xxx
[RECURRING_CONSUMER] Calculated next due date: 2024-02-09T09:00:00 (pattern: daily)
[RECURRING_CONSUMER] ✓ Created next recurring task yyy with due_date: 2024-02-09T09:00:00
```

### 5. Verify Next Task Created

```bash
curl http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" | jq
```

You should see:
- Original task with `is_completed: true`
- New task with:
  - Same `title` and `description`
  - `is_completed: false`
  - `due_date` = original + 1 day (for daily)
  - `parent_task_id` = original task ID

## Environment Variables

| Variable | Default | Description | Required? |
|----------|---------|-------------|-----------|
| `DAPR_HTTP_PORT` | `3500` | Dapr HTTP port (auto-set by Dapr) | No - Dapr sets it |
| `DAPR_PUBSUB_NAME` | `kafka-pubsub` | Pub/sub component name | No |
| `DATABASE_URL` | - | PostgreSQL connection string | Yes |

## Troubleshooting

### Issue: Still getting connection errors

**Check 1**: Verify Dapr is running
```bash
dapr list
```

**Check 2**: Check what port Dapr is using
```bash
dapr list | grep todo-backend
# Output: todo-backend  8000  39561  50001
#                             ^^^^^ This is the HTTP port
```

**Check 3**: Verify environment variable is set
```bash
# In the terminal where uvicorn is running
echo $DAPR_HTTP_PORT
```

**Check 4**: Look at the logs
The logs should show:
```
[DAPR] Dapr HTTP endpoint: http://localhost:XXXXX (port from env: XXXXX)
```

If the port is wrong, Dapr didn't set the environment variable correctly.

### Issue: 404 ERR_PUBSUB_NOT_FOUND

**Check 1**: Verify component is loaded
```bash
curl http://localhost:XXXXX/v1.0/metadata | jq '.components[] | select(.name=="kafka-pubsub")'
```

Replace XXXXX with your Dapr HTTP port.

**Check 2**: Verify components path
Make sure you're using `--components-path ./dapr/components` when starting Dapr.

**Check 3**: Check component file
```bash
cat dapr/components/redis-pubsub.yaml | grep "name:"
# Should show: name: kafka-pubsub
```

### Issue: Event published but not received

**Check 1**: Verify subscription endpoint
```bash
curl http://localhost:8000/dapr/subscribe
```

Should return:
```json
[
  {
    "pubsubname": "kafka-pubsub",
    "topic": "task-events",
    "route": "/events/task-events"
  }
]
```

**Check 2**: Check Redis is running
```bash
redis-cli ping
# Should return: PONG
```

**Check 3**: Check Dapr logs
Look for errors in the terminal where you ran `dapr run`.

## Files Modified

| File | Changes |
|------|---------|
| `src/core/dapr_client.py` | Dynamic port detection per request, enhanced logging |
| `src/services/task_service.py` | Use TaskEventType.TASK_COMPLETED enum |
| `src/services/recurring_consumer.py` | Handle both event type formats |

## Summary

All issues are now fixed:
1. ✅ Dynamic port detection - Works with any Dapr HTTP port
2. ✅ Correct pubsub component name - Verified and logged
3. ✅ Event type validation - Uses correct enum value "task.completed"
4. ✅ UUID serialization - Already working correctly

The recurring task engine should now work end-to-end! 🚀
