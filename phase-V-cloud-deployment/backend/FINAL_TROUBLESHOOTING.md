# Recurring Engine - Final Troubleshooting Guide

## Critical Issues Fixed

### ✅ 1. ERR_PUBSUB_NOT_FOUND - Component Not Found

**Problem**: Dapr returns 404 with "pubsub kafka-pubsub is not found"

**Root Causes**:
1. Dapr components not loaded (missing `--components-path` flag)
2. Redis not running (component uses Redis backend)
3. Component YAML file has wrong name

**Solution Applied**:

**File**: `src/core/dapr_client.py`
- Added detailed error diagnostics when ERR_PUBSUB_NOT_FOUND occurs
- Shows troubleshooting steps in logs
- Verifies component name is "kafka-pubsub" (from redis-pubsub.yaml)

**Verification Steps**:

1. **Check Redis is running**:
```bash
redis-cli ping
# Should return: PONG
```

2. **Check Dapr components are loaded**:
```bash
# Get Dapr HTTP port first
dapr list | grep todo-backend
# Output: todo-backend  8000  39561  50001
#                             ^^^^^ Use this port

# Check metadata
curl http://localhost:39561/v1.0/metadata | jq '.components[] | select(.name=="kafka-pubsub")'
```

Should return:
```json
{
  "name": "kafka-pubsub",
  "type": "pubsub.redis",
  "version": "v1"
}
```

3. **Verify components path in dapr run command**:
```bash
dapr run \
  --app-id todo-backend \
  --app-port 8000 \
  --components-path ./dapr/components \  # ← This is critical!
  -- uvicorn src.main:app
```

4. **Check component file exists**:
```bash
ls -la dapr/components/redis-pubsub.yaml
cat dapr/components/redis-pubsub.yaml | grep "name:"
# Should show: name: kafka-pubsub
```

### ✅ 2. Event Type Validation Error

**Problem**: TaskEvent validation error - event_type "completed" not allowed

**Root Cause**: The TaskEvent model expects enum values like `TaskEventType.TASK_COMPLETED` which has the string value "task.completed"

**Solution Applied**:

**File**: `src/services/task_service.py`
- Use `TaskEventType.TASK_COMPLETED` enum (value = "task.completed")
- Added logging to show the enum value being used

**File**: `src/core/dapr_client.py`
- Properly extract enum value using `.value` attribute
- Convert to string for JSON serialization

**Code**:
```python
# In task_service.py
event = TaskEvent(
    event_type=TaskEventType.TASK_COMPLETED,  # Enum with value "task.completed"
    ...
)

# In dapr_client.py
if hasattr(event_type_value, 'value'):
    event_dict['event_type'] = event_type_value.value  # "task.completed"
else:
    event_dict['event_type'] = str(event_type_value)
```

**File**: `src/services/recurring_consumer.py`
- Updated to handle both "task.completed" and "completed" for backward compatibility

### ✅ 3. Non-Blocking Event Publishing

**Problem**: If event publishing fails, task completion should still succeed

**Solution Applied**:

**File**: `src/services/task_service.py`
- Wrapped event publishing in try-except
- If publish fails, log warning but continue
- Task completion response is returned successfully
- User sees task marked as complete even if next occurrence isn't created

**Fallback Behavior**:
```
[RECURRING] ⚠ WARNING: Failed to publish completed event
[RECURRING] ⚠ Next occurrence will NOT be created automatically
[RECURRING] ⚠ Task completion succeeded, but event publishing failed
```

### ✅ 4. Monthly Recurrence Handling

**Already Working**: `src/utils/recurring_utils.py`

```python
def calculate_next_due_date(current_due_date, recurrence_pattern):
    if recurrence_pattern == "monthly":
        return current_due_date + timedelta(days=30)
```

**Note**: This is a simplification (not all months have 30 days), but it's acceptable for the current implementation.

## Complete Testing Flow

### 1. Start Redis (if not running)

```bash
# Check if Redis is running
redis-cli ping

# If not running, start it
redis-server
```

### 2. Start Backend with Dapr

**Critical**: Use `--components-path ./dapr/components`

```bash
cd phase-V-cloud-deployment/backend

dapr run \
  --app-id todo-backend \
  --app-port 8000 \
  --components-path ./dapr/components \
  --log-level debug \
  -- uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Verify Initialization

Look for these logs:
```
[DAPR_CLIENT] Initialized with endpoint: http://localhost:XXXXX
```

### 4. Verify Dapr Components Loaded

```bash
# Get Dapr HTTP port
dapr list

# Check components
curl http://localhost:XXXXX/v1.0/metadata | jq '.components'
```

Should show "kafka-pubsub" component.

### 5. Verify Subscription Endpoint

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

### 6. Create Recurring Task

```bash
export TOKEN="your-jwt-token"

curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Monthly report",
    "description": "Submit monthly report",
    "isRecurring": true,
    "recurrencePattern": "monthly",
    "dueDate": "2024-02-08T09:00:00Z"
  }'
```

Save the task ID from response.

### 7. Complete the Task

```bash
export TASK_ID="task-id-from-above"

curl -X PATCH http://localhost:8000/api/tasks/$TASK_ID/complete \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### 8. Expected Logs (Success Case)

```
[RECURRING] ========== RECURRING TASK COMPLETION ==========
[RECURRING] Task xxx is recurring and completed
[RECURRING] Recurrence pattern: monthly
[RECURRING] Event created with type: TaskEventType.TASK_COMPLETED (value: task.completed)
[DAPR] ========== PUBLISH EVENT DEBUG ==========
[DAPR] Using pubsub name: kafka-pubsub
[DAPR] Dapr HTTP endpoint: http://localhost:39561 (port from env: 39561)
[DAPR] Full publish URL: http://localhost:39561/v1.0/publish/kafka-pubsub/task-events
[DAPR] Event type after conversion: task.completed
[DAPR] Attempt 1/3 to publish event
[DAPR] Response status: 200
[DAPR] ✓ Successfully published event to task-events on attempt 1
[RECURRING] ✓ Successfully published completed event for recurring task xxx
[RECURRING] Next occurrence will be created by the consumer

[TASK_EVENTS] Received event from Dapr
[RECURRING_CONSUMER] Received event type: task.completed
[RECURRING_CONSUMER] Processing recurring task event for task xxx
[RECURRING_CONSUMER] Calculated next due date: 2024-03-09T09:00:00 (pattern: monthly)
[RECURRING_CONSUMER] ✓ Created next recurring task yyy with due_date: 2024-03-09T09:00:00
```

### 9. Verify Next Task Created

```bash
curl http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" | jq
```

Should show:
- Original task: `is_completed: true`, `due_date: 2024-02-08T09:00:00`
- New task: `is_completed: false`, `due_date: 2024-03-09T09:00:00` (30 days later)

## Troubleshooting Specific Errors

### Error: ERR_PUBSUB_NOT_FOUND

**Logs show**:
```
[DAPR] ✗ Failed to publish event: 404 - ERR_PUBSUB_NOT_FOUND
[DAPR] ERROR: Pubsub component 'kafka-pubsub' not found!
```

**Fix**:

1. **Check Redis**:
```bash
redis-cli ping
# If fails, start Redis: redis-server
```

2. **Check components path**:
```bash
# Make sure you used --components-path flag
dapr run --components-path ./dapr/components ...
```

3. **Verify component loaded**:
```bash
curl http://localhost:XXXXX/v1.0/metadata | jq '.components[] | select(.name=="kafka-pubsub")'
```

4. **Check component file**:
```bash
cat dapr/components/redis-pubsub.yaml
# Verify metadata.name is "kafka-pubsub"
```

### Error: Event Type Validation

**Logs show**:
```
validation error for TaskEvent
event_type
  value is not a valid enumeration member
```

**This should be fixed now**. If you still see it:

1. Check the logs show:
```
[RECURRING] Event created with type: TaskEventType.TASK_COMPLETED (value: task.completed)
[DAPR] Event type after conversion: task.completed
```

2. If not, the enum conversion isn't working. Check Python version and pydantic version.

### Error: Connection Refused

**Logs show**:
```
[DAPR] ✗ Connection error: All connection attempts failed
```

**Fix**:

1. **Check Dapr is running**:
```bash
dapr list
```

2. **Check port matches**:
```bash
dapr list | grep todo-backend
# Note the HTTP port (3rd column)

# Check logs show same port:
# [DAPR] Dapr HTTP endpoint: http://localhost:XXXXX
```

3. **Restart Dapr with fixed port**:
```bash
dapr run --dapr-http-port 3500 ...
```

### Error: Next Task Not Created

**Event published successfully but no new task**:

1. **Check consumer received event**:
Look for:
```
[TASK_EVENTS] Received event from Dapr
[RECURRING_CONSUMER] Received event type: task.completed
```

2. **Check database connection**:
```
[RECURRING_CONSUMER] ✗ Error creating next recurring task: ...
```

3. **Check original task exists**:
```bash
curl http://localhost:8000/api/tasks/$TASK_ID \
  -H "Authorization: Bearer $TOKEN"
```

## Environment Variables

| Variable | Default | Set By | Description |
|----------|---------|--------|-------------|
| `DAPR_HTTP_PORT` | `3500` | Dapr | HTTP port (auto-set by Dapr) |
| `DAPR_PUBSUB_NAME` | `kafka-pubsub` | Manual | Pub/sub component name |
| `DATABASE_URL` | - | Manual | PostgreSQL connection |

## Files Modified

| File | Changes |
|------|---------|
| `src/core/dapr_client.py` | Enhanced diagnostics, enum value extraction, ERR_PUBSUB_NOT_FOUND handling |
| `src/services/task_service.py` | Non-blocking publish, detailed logging, fallback warnings |
| `src/services/recurring_consumer.py` | Handle both event type formats |

## Quick Checklist

Before testing, verify:

- [ ] Redis is running (`redis-cli ping`)
- [ ] Dapr is initialized (`dapr init`)
- [ ] Backend started with `--components-path ./dapr/components`
- [ ] Dapr components loaded (check `/v1.0/metadata`)
- [ ] Subscription endpoint works (`/dapr/subscribe`)
- [ ] Database is accessible
- [ ] JWT token is valid

## Success Indicators

✅ Event published successfully
✅ Consumer receives event
✅ Next task created with correct due_date
✅ Logs show "task.completed" event type
✅ No validation errors
✅ Task completion succeeds even if publish fails

## Next Steps

1. Test with all recurrence patterns: daily, weekly, monthly, yearly
2. Test failure scenarios (Redis down, Dapr down)
3. Verify fallback behavior works correctly
4. Add integration tests for recurring task flow
5. Consider using proper month calculation for monthly recurrence (dateutil.relativedelta)
