# CRITICAL FIX: Pubsub Component Name

## Problem Identified

**Every publish fails with ERR_PUBSUB_NOT_FOUND for "kafka-pubsub"**

From the logs, Dapr loaded: `pubsub (pubsub.redis/v1)`

This means the component name is **"pubsub"** (the default from `dapr init`), NOT "kafka-pubsub".

## Root Cause

When you run `dapr init`, it creates a default Redis pubsub component named **"pubsub"**.

The code was using "kafka-pubsub" which doesn't exist unless you explicitly load custom components with `--components-path ./dapr/components`.

## Solution Applied

### Files Modified

**1. src/core/dapr_client.py**
```python
# Changed from:
pubsub_name = os.getenv("DAPR_PUBSUB_NAME", "kafka-pubsub")

# To:
pubsub_name = os.getenv("DAPR_PUBSUB_NAME", "pubsub")
```

**2. src/routers/events.py**
```python
# Changed from:
subscriptions = [
    {
        "pubsubname": "kafka-pubsub",
        ...
    }
]

# To:
pubsub_name = os.getenv("DAPR_PUBSUB_NAME", "pubsub")
subscriptions = [
    {
        "pubsubname": pubsub_name,
        ...
    }
]
```

## How to Test

### 1. Start Backend with Dapr (Simple Method)

**Don't use `--components-path` - use the default pubsub from dapr init:**

```bash
cd phase-V-cloud-deployment/backend

dapr run \
  --app-id todo-backend \
  --app-port 8000 \
  -- uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Verify Logs Show Correct Pubsub Name

Look for:
```
[DAPR] Using real pubsub name: pubsub
[DAPR] Full publish URL: http://localhost:XXXXX/v1.0/publish/pubsub/task-events
```

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

# Complete the task
curl -X PATCH http://localhost:8000/api/tasks/$TASK_ID/complete \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### 4. Expected Success Logs

```
[RECURRING] ========== RECURRING TASK COMPLETION ==========
[RECURRING] Task xxx is recurring and completed
[DAPR] ========== PUBLISH EVENT DEBUG ==========
[DAPR] Using real pubsub name: pubsub
[DAPR] Dapr HTTP endpoint: http://localhost:39561 (port from env: 39561)
[DAPR] Full publish URL: http://localhost:39561/v1.0/publish/pubsub/task-events
[DAPR] Event type after conversion: task.completed
[DAPR] Attempt 1/3 to publish event
[DAPR] Response status: 200
[DAPR] ✓ Successfully published event to task-events on attempt 1
[RECURRING] ✓ Successfully published completed event for recurring task xxx

[TASK_EVENTS] Received event from Dapr
[RECURRING_CONSUMER] Received event type: task.completed
[RECURRING_CONSUMER] ✓ Created next recurring task yyy with due_date: 2024-02-09T09:00:00
```

## Alternative: Use Custom Components

If you want to use the custom component files in `dapr/components/`, you need to:

1. **Start with components path**:
```bash
dapr run \
  --app-id todo-backend \
  --app-port 8000 \
  --components-path ./dapr/components \
  -- uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

2. **Set environment variable**:
```bash
export DAPR_PUBSUB_NAME=kafka-pubsub
```

3. **Verify component name in YAML**:
```bash
cat dapr/components/redis-pubsub.yaml | grep "name:"
# Should show: name: kafka-pubsub
```

## Understanding Dapr Components

### Default Component (from dapr init)
- **Name**: `pubsub`
- **Type**: `pubsub.redis`
- **Location**: `~/.dapr/components/`
- **Loaded**: Automatically by Dapr
- **Use when**: Running without `--components-path` flag

### Custom Components (in project)
- **Name**: `kafka-pubsub` (defined in redis-pubsub.yaml)
- **Type**: `pubsub.redis`
- **Location**: `./dapr/components/`
- **Loaded**: Only with `--components-path ./dapr/components`
- **Use when**: You need custom configuration

## Verification Commands

### Check which components are loaded:
```bash
# Get Dapr HTTP port
dapr list | grep todo-backend

# Check metadata (replace XXXXX with actual port)
curl http://localhost:XXXXX/v1.0/metadata | jq '.components[] | select(.type | contains("pubsub"))'
```

### Check subscription endpoint:
```bash
curl http://localhost:8000/dapr/subscribe
```

Should return:
```json
[
  {
    "pubsubname": "pubsub",
    "topic": "task-events",
    "route": "/events/task-events"
  }
]
```

## Troubleshooting

### Still getting ERR_PUBSUB_NOT_FOUND?

1. **Check Redis is running**:
```bash
redis-cli ping
# Should return: PONG
```

2. **Check Dapr metadata**:
```bash
curl http://localhost:XXXXX/v1.0/metadata | jq '.components'
```

Look for a component with `"type": "pubsub.redis"` and note its name.

3. **Set the correct name**:
```bash
export DAPR_PUBSUB_NAME=<name-from-metadata>
```

4. **Restart the backend**

### Event published but not received?

1. **Check subscription matches pubsub name**:
```bash
curl http://localhost:8000/dapr/subscribe
```

The `pubsubname` in the response must match the component name in Dapr metadata.

2. **Check Dapr logs** for subscription errors

## Summary

✅ Changed default pubsub name from "kafka-pubsub" to "pubsub"
✅ Updated both publish and subscribe endpoints
✅ Added environment variable support for flexibility
✅ Event type already fixed to "task.completed"
✅ Fallback warnings already in place

**The recurring task engine should now work with the default Dapr setup!** 🎉

## Quick Start (Recommended)

```bash
# 1. Make sure Redis is running
redis-cli ping

# 2. Start backend (no --components-path needed)
cd phase-V-cloud-deployment/backend
dapr run --app-id todo-backend --app-port 8000 -- uvicorn src.main:app --reload

# 3. Test recurring task completion
# (Create task, complete it, check logs for success)
```
