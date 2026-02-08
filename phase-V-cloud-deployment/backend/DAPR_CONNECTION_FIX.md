# Dapr Connection Fix - Recurring Task Engine

## Problem Summary

When completing a recurring task, the backend failed to publish events to Dapr with the error:
```
[RECURRING] Connection error publishing completed event ... All connection attempts failed
[DAPR] Make sure Dapr sidecar is running on http://localhost:3500
```

**Root Cause**: The Dapr sidecar uses a random HTTP port (e.g., 39561, 43091) when started with `dapr run`, but the code was hardcoded to use port 3500.

## Solution Applied

### 1. Dynamic Port Detection (src/core/dapr_client.py)

**Before**:
```python
def __init__(self, dapr_http_endpoint: str = "http://localhost:3500"):
    self.dapr_http_endpoint = dapr_http_endpoint
```

**After**:
```python
def __init__(self, dapr_http_endpoint: Optional[str] = None):
    # Use dynamic port from environment variable
    if dapr_http_endpoint is None:
        dapr_http_port = os.getenv("DAPR_HTTP_PORT", "3500")
        dapr_http_endpoint = f"http://localhost:{dapr_http_port}"

    self.dapr_http_endpoint = dapr_http_endpoint
    print(f"[DAPR_CLIENT] Initialized with endpoint: {self.dapr_http_endpoint}")
```

### 2. Retry Logic with Exponential Backoff

Added 3 retry attempts with exponential backoff (1s, 2s, 4s):

```python
async def publish_event(self, topic: str, event: TaskEvent, max_retries: int = 3) -> bool:
    for attempt in range(1, max_retries + 1):
        try:
            response = await self.http_client.post(url, json=event_dict, timeout=10.0)

            if response.status_code in [200, 204]:
                print(f"[DAPR] ✓ Successfully published event to {topic} on attempt {attempt}")
                return True

            # Retry with exponential backoff
            if attempt < max_retries:
                wait_time = 2 ** (attempt - 1)
                await asyncio.sleep(wait_time)
        except Exception as e:
            # Handle errors and retry
```

### 3. Configurable Pub/Sub Component Name

```python
pubsub_name = os.getenv("DAPR_PUBSUB_NAME", "kafka-pubsub")
url = f"{self.dapr_http_endpoint}/v1.0/publish/{pubsub_name}/{topic}"
```

### 4. Enhanced Debug Logging

```python
print(f"[DAPR] Dapr HTTP endpoint used: {url}")
print(f"[DAPR] Publishing event to topic: {topic}")
print(f"[DAPR] Attempt {attempt}/{max_retries} to publish event")
print(f"[DAPR] Check DAPR_HTTP_PORT environment variable (current: {os.getenv('DAPR_HTTP_PORT', '3500')})")
```

### 5. Updated task_service.py to Use DaprClient

**Before**: Direct httpx calls with hardcoded port
```python
async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
    response = await client.post(
        "http://localhost:3500/v1.0/publish/kafka-pubsub/task-events",
        json=event_payload
    )
```

**After**: Use improved DaprClient with retry and dynamic port
```python
from src.core.dapr_client import dapr_client
from src.core.event_schemas import TaskEvent

event = TaskEvent(
    event_id=str(uuid4()),
    event_type="completed",
    user_id=str(task.user_id),
    task_id=str(task.id),
    timestamp=datetime.utcnow(),
    payload={...}
)

success = await dapr_client.publish_event("task-events", event)
```

### 6. Non-Blocking Event Publishing

If event publishing fails, the task completion still succeeds:

```python
try:
    success = await dapr_client.publish_event("task-events", event)
    if success:
        print(f"[RECURRING] ✓ Successfully published completed event")
    else:
        print(f"[RECURRING] ✗ Failed to publish, next occurrence will not be created")
except Exception as e:
    # Don't crash the response if event publishing fails
    print(f"[RECURRING] Task completion succeeded, but next occurrence will not be created")
```

## Environment Variables

The following environment variables are now supported:

| Variable | Default | Description |
|----------|---------|-------------|
| `DAPR_HTTP_PORT` | `3500` | HTTP port of the Dapr sidecar |
| `DAPR_PUBSUB_NAME` | `kafka-pubsub` | Name of the pub/sub component |

## How to Use

### Option 1: Specify Port When Starting Dapr (Recommended)

```bash
cd phase-V-cloud-deployment/backend

# Start with fixed port 3500
dapr run \
  --app-id todo-backend \
  --app-port 8000 \
  --dapr-http-port 3500 \
  --dapr-grpc-port 50001 \
  --components-path ./dapr/components \
  --log-level debug \
  -- uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 2: Use Environment Variable

If Dapr assigns a random port, set the environment variable:

```bash
# Find the Dapr HTTP port
dapr list
# Output shows: todo-backend  8000  39561  50001  ...
#                                    ^^^^^ This is the HTTP port

# Set environment variable and start backend
export DAPR_HTTP_PORT=39561
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Let Dapr Set the Environment Variable

When you use `dapr run`, Dapr automatically sets the `DAPR_HTTP_PORT` environment variable for the application:

```bash
dapr run \
  --app-id todo-backend \
  --app-port 8000 \
  --components-path ./dapr/components \
  -- uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

The application will automatically detect the port from the environment.

## Verification

### 1. Check Dapr Client Initialization

When the backend starts, you should see:
```
[DAPR_CLIENT] Initialized with endpoint: http://localhost:3500
```

### 2. Check Event Publishing

When completing a recurring task:
```
[RECURRING] Task xxx is recurring and completed, publishing event to task-events topic
[DAPR] Dapr HTTP endpoint used: http://localhost:3500/v1.0/publish/kafka-pubsub/task-events
[DAPR] Publishing event to topic: task-events
[DAPR] Attempt 1/3 to publish event
[DAPR] ✓ Successfully published event to task-events on attempt 1
[RECURRING] ✓ Successfully published completed event for recurring task xxx
```

### 3. Check Event Reception

In the Dapr logs, you should see:
```
[TASK_EVENTS] Received event from Dapr
[RECURRING_CONSUMER] Processing recurring task event for task xxx
[RECURRING_CONSUMER] ✓ Created next recurring task yyy with due_date: 2024-02-09T09:00:00
```

## Troubleshooting

### Issue: Still getting connection errors

**Solution 1**: Verify Dapr is running
```bash
dapr list
```

**Solution 2**: Check the port matches
```bash
# Get the Dapr HTTP port from dapr list
dapr list | grep todo-backend

# Set it explicitly
export DAPR_HTTP_PORT=<port-from-above>
```

**Solution 3**: Use fixed port 3500
```bash
dapr run --dapr-http-port 3500 ...
```

### Issue: Events published but not received

**Solution**: Check Dapr subscription endpoint
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

### Issue: Wrong pub/sub component name

**Solution**: Set the environment variable
```bash
export DAPR_PUBSUB_NAME=redis-pubsub  # or kafka-pubsub
```

Or check your component file:
```bash
cat dapr/components/kafka-pubsub.yaml | grep "name:"
```

## Testing the Fix

1. **Start backend with Dapr**:
   ```bash
   cd phase-V-cloud-deployment/backend

   dapr run \
     --app-id todo-backend \
     --app-port 8000 \
     --dapr-http-port 3500 \
     --components-path ./dapr/components \
     --log-level debug \
     -- uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Create a recurring task**:
   ```bash
   curl -X POST http://localhost:8000/api/tasks \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Daily standup",
       "isRecurring": true,
       "recurrencePattern": "daily",
       "dueDate": "2024-02-08T09:00:00Z"
     }'
   ```

3. **Complete the task**:
   ```bash
   curl -X PATCH http://localhost:8000/api/tasks/$TASK_ID/complete \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"completed": true}'
   ```

4. **Check logs** for successful event publishing and next task creation

5. **Verify next task created**:
   ```bash
   curl http://localhost:8000/api/tasks \
     -H "Authorization: Bearer $TOKEN"
   ```

## Summary of Changes

| File | Changes |
|------|---------|
| `src/core/dapr_client.py` | - Dynamic port detection from `DAPR_HTTP_PORT`<br>- Retry logic with exponential backoff (3 attempts)<br>- Configurable pub/sub component name<br>- Enhanced debug logging |
| `src/services/task_service.py` | - Use DaprClient instead of direct httpx<br>- Non-blocking event publishing<br>- Better error handling |

## Benefits

1. **Automatic port detection**: Works with any Dapr HTTP port
2. **Retry logic**: Handles transient network issues
3. **Better debugging**: Clear logs showing exact endpoint and retry attempts
4. **Non-blocking**: Task completion succeeds even if event publishing fails
5. **Configurable**: Easy to change pub/sub component via environment variable
