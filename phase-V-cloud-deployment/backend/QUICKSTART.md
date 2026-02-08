# Quick Start Guide - Phase V Backend with Dapr

## Overview
This guide helps you start the Phase V backend with Dapr integration for recurring tasks.

## Prerequisites

1. **Dapr CLI installed**
   ```bash
   dapr --version
   ```

2. **Dapr initialized**
   ```bash
   dapr init
   ```
   This installs Redis, Zipkin, and Placement service locally.

3. **Python environment**
   ```bash
   cd phase-V-cloud-deployment/backend
   uv sync
   ```

4. **Database configured**
   - Set `DATABASE_URL` in `.env` file
   - Ensure PostgreSQL/Neon is accessible

## Important: Environment Variables

The backend now supports dynamic Dapr port detection. You can configure:

| Variable | Default | Description |
|----------|---------|-------------|
| `DAPR_HTTP_PORT` | `3500` | HTTP port of the Dapr sidecar |
| `DAPR_PUBSUB_NAME` | `kafka-pubsub` | Name of the pub/sub component |

**Recommended**: Use a fixed port (`--dapr-http-port 3500`) when starting Dapr to avoid connection issues.

See [DAPR_CONNECTION_FIX.md](./DAPR_CONNECTION_FIX.md) for detailed information about the Dapr connection improvements.

## Choose Your Pub/Sub Component

### Option 1: Redis (Recommended for Local Development)

Redis is automatically installed by `dapr init` and requires no additional setup.

**Use this component**: `dapr/components/redis-pubsub.yaml`

The component name is still `kafka-pubsub` (for backward compatibility), but it uses Redis underneath.

### Option 2: Kafka (For Production)

Requires Kafka broker running on `localhost:9092`.

**Use this component**: `dapr/components/kafka-pubsub.yaml`

To start Kafka locally:
```bash
# Using Docker
docker run -d --name kafka -p 9092:9092 \
  -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
  confluentinc/cp-kafka:latest
```

## Starting the Backend

### Step 1: Choose Pub/Sub Component

For Redis (recommended):
```bash
cd phase-V-cloud-deployment/backend
cp dapr/components/redis-pubsub.yaml dapr/components/kafka-pubsub.yaml
```

### Step 2: Start Backend with Dapr (Recommended Method)

**Use a fixed HTTP port (3500) to avoid connection issues:**

```bash
cd phase-V-cloud-deployment/backend

dapr run \
  --app-id todo-backend \
  --app-port 8000 \
  --dapr-http-port 3500 \
  --dapr-grpc-port 50001 \
  --components-path ./dapr/components \
  --config ./dapr/config.yaml \
  --log-level debug \
  -- uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

**Important**: The `--dapr-http-port 3500` flag ensures Dapr uses a fixed port. Without this, Dapr assigns a random port which can cause connection issues.

### Alternative: Use Dynamic Port Detection

If you don't specify `--dapr-http-port`, Dapr will assign a random port. The backend will automatically detect it from the `DAPR_HTTP_PORT` environment variable that Dapr sets:

```bash
cd phase-V-cloud-deployment/backend

dapr run \
  --app-id todo-backend \
  --app-port 8000 \
  --components-path ./dapr/components \
  --config ./dapr/config.yaml \
  --log-level debug \
  -- uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

You should see in the logs:
```
[DAPR_CLIENT] Initialized with endpoint: http://localhost:XXXXX
```

Where XXXXX is the dynamically assigned port.

### Step 3: Verify Dapr is Running

In another terminal:
```bash
# Check Dapr is running
dapr list

# Check Dapr metadata
curl http://localhost:3500/v1.0/metadata

# Check subscriptions
curl http://localhost:8000/dapr/subscribe
```

Expected output from `/dapr/subscribe`:
```json
[
  {
    "pubsubname": "kafka-pubsub",
    "topic": "task-events",
    "route": "/events/task-events"
  }
]
```

## Testing Recurring Tasks

### 1. Get JWT Token

First, signup and login to get a JWT token:

```bash
# Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "full_name": "Test User"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

Save the `access_token` from the response.

### 2. Create a Recurring Task

```bash
export TOKEN="your-jwt-token-here"

curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Daily standup meeting",
    "description": "Team standup at 9 AM",
    "isRecurring": true,
    "recurrencePattern": "daily",
    "dueDate": "2024-02-08T09:00:00Z",
    "priority": "high"
  }'
```

Save the task `id` from the response.

### 3. Mark Task as Complete

```bash
export TASK_ID="task-id-from-previous-step"

curl -X PATCH http://localhost:8000/api/tasks/$TASK_ID/complete \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### 4. Check Logs

Watch the terminal where Dapr is running. You should see:

```
[RECURRING] Task xxx is recurring and completed, publishing event to task-events topic
[RECURRING] Event payload: {...}
[RECURRING] Successfully published completed event for recurring task xxx
[TASK_EVENTS] Received event from Dapr
[RECURRING_CONSUMER] Processing recurring task event for task xxx
[RECURRING_CONSUMER] Calculated next due date: 2024-02-09T09:00:00
[RECURRING_CONSUMER] ✓ Created next recurring task yyy with due_date: 2024-02-09T09:00:00
```

### 5. Verify Next Task Created

```bash
curl http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN"
```

You should see:
- Original task with `is_completed: true`
- New task with:
  - Same `title` and `description`
  - `is_completed: false`
  - `due_date` = original due_date + 1 day (for daily recurrence)
  - `parent_task_id` = original task ID

## Troubleshooting

### Issue: "Connection refused" or "All connection attempts failed" to Dapr

This is the most common issue. The backend cannot connect to the Dapr sidecar.

**Solution 1**: Use fixed port 3500 (Recommended)
```bash
dapr run --dapr-http-port 3500 ...
```

**Solution 2**: Verify Dapr is running
```bash
dapr list
```

**Solution 3**: Check the port matches
```bash
# Get the Dapr HTTP port from dapr list
dapr list | grep todo-backend
# Output: todo-backend  8000  39561  50001
#                             ^^^^^ This is the HTTP port

# If using a different port, set it explicitly
export DAPR_HTTP_PORT=39561
```

**Solution 4**: Check initialization logs
Look for this line when the backend starts:
```
[DAPR_CLIENT] Initialized with endpoint: http://localhost:3500
```

If the port is wrong, the backend won't be able to connect.

**For detailed troubleshooting**, see [DAPR_CONNECTION_FIX.md](./DAPR_CONNECTION_FIX.md)

### Issue: "Failed to publish event"

**Check 1**: Verify Redis is running
```bash
redis-cli ping
# Should return: PONG
```

**Check 2**: Verify Dapr components are loaded
```bash
curl http://localhost:3500/v1.0/metadata | jq '.components'
```

Should show `kafka-pubsub` component.

**Check 3**: Check Dapr logs
```bash
# Dapr logs are in the terminal where you ran 'dapr run'
# Look for errors related to pubsub component
```

### Issue: "UUID is not JSON serializable"

This should be fixed. If you still see this error:

1. Check you're using the updated code
2. Verify `src/core/dapr_client.py` has UUID to string conversion
3. Check logs for the exact line causing the error

### Issue: Next task not created

**Check 1**: Verify event was published
```bash
# Look for [RECURRING] logs in terminal
```

**Check 2**: Verify event was received
```bash
# Look for [TASK_EVENTS] logs in terminal
```

**Check 3**: Check database connection
```bash
# Verify DATABASE_URL in .env is correct
# Check database is accessible
```

**Check 4**: Verify original task exists
```bash
curl http://localhost:8000/api/tasks/$TASK_ID \
  -H "Authorization: Bearer $TOKEN"
```

## Log Prefixes

Filter logs by prefix to debug specific components:

- `[DAPR]` - Dapr client operations
- `[RECURRING]` - Event publishing from task service
- `[DAPR_SUBSCRIBE]` - Subscription endpoint
- `[TASK_EVENTS]` - Event handler endpoint
- `[RECURRING_CONSUMER]` - Recurring task consumer

Example:
```bash
# In the terminal where Dapr is running, grep for specific logs
# (This works if you redirect output to a file)
dapr run ... 2>&1 | tee backend.log

# Then in another terminal:
tail -f backend.log | grep "\[RECURRING\]"
```

## Production Deployment

For production:

1. **Use Kafka instead of Redis** for better scalability
2. **Configure proper error handling** and dead letter queues
3. **Add monitoring** for event processing
4. **Set up proper logging** with structured logs
5. **Configure retries** in Dapr component
6. **Use Dapr secrets** for sensitive configuration

## Next Steps

1. Test with different recurrence patterns (weekly, monthly, yearly)
2. Test with tasks that have reminders
3. Add integration tests for recurring task flow
4. Monitor event processing latency
5. Set up alerts for failed events
