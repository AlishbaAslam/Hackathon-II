# Audit Logging Skill

## Overview
The `audit-logging` skill implements a comprehensive audit trail system that listens to the "task-events" topic via Dapr Pub/Sub. It captures and stores a complete history of every task operation (create, update, delete, complete) to ensure full traceability and compliance. The system supports both database and file-based storage options for audit logs.

## Features
- Listen to "task-events" topic for all task operations
- Store complete audit history with rich metadata
- Support for both database and file storage
- Comprehensive logging of all task lifecycle events
- Structured log format for easy querying and analysis

## Audit Log Schema

### Database Schema
```sql
CREATE TABLE task_audit_log (
  id BIGSERIAL PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,           -- Unique identifier for the event
  user_id VARCHAR(255) NOT NULL,            -- ID of the user who initiated the action
  task_id INTEGER,                          -- ID of the affected task
  operation_type VARCHAR(50) NOT NULL,      -- Type of operation (CREATE, UPDATE, DELETE, COMPLETE)
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  ip_address INET,                          -- IP address of the request
  user_agent TEXT,                          -- User agent string
  previous_values JSONB,                    -- Values before the operation (for UPDATE/DELETE)
  new_values JSONB,                         -- Values after the operation (for CREATE/UPDATE)
  metadata JSONB,                           -- Additional contextual information
  correlation_id VARCHAR(255),              -- Correlation ID for request tracing
  session_id VARCHAR(255),                  -- Session identifier
  client_info JSONB                         -- Additional client information
);
```

### File Log Format
```json
{
  "timestamp": "2024-01-15T10:30:00.123Z",
  "event_id": "evt-12345-abcde",
  "user_id": "user-67890",
  "task_id": 12345,
  "operation_type": "CREATE",
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "previous_values": null,
  "new_values": {
    "title": "Complete project proposal",
    "description": "Finish the Q4 project proposal document",
    "status": "pending",
    "priority": "high",
    "due_at": "2024-01-20T09:00:00Z",
    "created_at": "2024-01-15T10:30:00Z",
    "user_id": "user-67890"
  },
  "metadata": {
    "source": "web",
    "version": "1.0.0",
    "device_type": "desktop"
  },
  "correlation_id": "corr-abc-123-def-456",
  "session_id": "sess-xyz-789",
  "client_info": {
    "browser": "Chrome",
    "os": "Windows 10",
    "timezone": "America/New_York"
  }
}
```

## Event Processing

### Supported Operations
The audit logging system captures the following task operations:

1. **CREATE**: When a new task is created
2. **UPDATE**: When an existing task is modified
3. **DELETE**: When a task is deleted (including soft deletes)
4. **COMPLETE**: When a task is marked as completed
5. **RESTORE**: When a soft-deleted task is restored

### Event Listener Implementation
```javascript
async function initializeAuditLogger() {
  // Subscribe to the task-events topic
  daprClient.pubsub.subscribe(
    'task-events',
    'audit-logger',
    handleTaskEvent
  );
}

async function handleTaskEvent(event) {
  try {
    // Parse the incoming event
    const parsedEvent = parseTaskEvent(event);

    // Determine operation type based on event type
    const operationType = mapEventTypeToOperation(parsedEvent.event_type);

    // Create audit log entry
    const auditEntry = {
      event_id: parsedEvent.event_id || generateEventId(),
      user_id: parsedEvent.user_id,
      task_id: parsedEvent.task_id,
      operation_type: operationType,
      timestamp: new Date().toISOString(),
      ip_address: parsedEvent.ip_address,
      user_agent: parsedEvent.user_agent,
      previous_values: parsedEvent.previous_values || null,
      new_values: parsedEvent.new_values || parsedEvent.task_data,
      metadata: parsedEvent.metadata || {},
      correlation_id: parsedEvent.correlation_id,
      session_id: parsedEvent.session_id,
      client_info: parsedEvent.client_info || {}
    };

    // Store the audit entry
    await storeAuditLog(auditEntry);

    console.log(`Audit log created for ${operationType} operation on task ${parsedEvent.task_id}`);
  } catch (error) {
    console.error('Failed to create audit log:', error);
    // Implement error handling and alerting
    await handleError(error, event);
  }
}

function parseTaskEvent(event) {
  // Parse the raw event from Dapr Pub/Sub
  return {
    event_id: event.id,
    event_type: event.type,
    user_id: event.user_id,
    task_id: event.task_id,
    task_data: event.data,
    previous_values: event.previous_values,
    new_values: event.new_values,
    ip_address: event.metadata?.ip_address,
    user_agent: event.metadata?.user_agent,
    metadata: event.metadata,
    correlation_id: event.correlation_id,
    session_id: event.session_id,
    client_info: event.client_info
  };
}

function mapEventTypeToOperation(eventType) {
  const eventToOperationMap = {
    'TASK_CREATED': 'CREATE',
    'TASK_UPDATED': 'UPDATE',
    'TASK_DELETED': 'DELETE',
    'TASK_COMPLETED': 'COMPLETE',
    'TASK_RESTORED': 'RESTORE',
    'TASK_STATUS_CHANGED': 'UPDATE'
  };

  return eventToOperationMap[eventType] || 'UNKNOWN';
}

function generateEventId() {
  return `audit-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}
```

## Storage Options

### Database Storage
```javascript
async function storeAuditLogToDatabase(auditEntry) {
  const query = `
    INSERT INTO task_audit_log (
      event_id, user_id, task_id, operation_type, timestamp,
      ip_address, user_agent, previous_values, new_values,
      metadata, correlation_id, session_id, client_info
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
    RETURNING id
  `;

  const values = [
    auditEntry.event_id,
    auditEntry.user_id,
    auditEntry.task_id,
    auditEntry.operation_type,
    auditEntry.timestamp,
    auditEntry.ip_address,
    auditEntry.user_agent,
    auditEntry.previous_values,
    auditEntry.new_values,
    auditEntry.metadata,
    auditEntry.correlation_id,
    auditEntry.session_id,
    auditEntry.client_info
  ];

  const result = await db.query(query, values);
  return result.rows[0].id;
}
```

### File Storage
```javascript
const fs = require('fs');
const path = require('path');

async function storeAuditLogToFile(auditEntry) {
  const logDir = path.join(__dirname, 'logs', 'audit');

  // Create directory if it doesn't exist
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
  }

  // Create daily log file
  const dateStr = new Date().toISOString().split('T')[0];
  const logFilePath = path.join(logDir, `audit-${dateStr}.log`);

  // Write audit entry as JSON line
  const logLine = JSON.stringify(auditEntry) + '\n';
  fs.appendFileSync(logFilePath, logLine);

  return logFilePath;
}
```

## Example Stored Entries

### Task Creation Entry
```json
{
  "id": 1001,
  "event_id": "evt-12345-abcde",
  "user_id": "user-67890",
  "task_id": 12345,
  "operation_type": "CREATE",
  "timestamp": "2024-01-15T10:30:00.123Z",
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "previous_values": null,
  "new_values": {
    "id": 12345,
    "user_id": "user-67890",
    "title": "Complete project proposal",
    "description": "Finish the Q4 project proposal document",
    "status": "pending",
    "priority": "high",
    "due_at": "2024-01-20T09:00:00Z",
    "remind_at": "2024-01-20T08:00:00Z",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "tags": ["work", "important"]
  },
  "metadata": {
    "source": "web",
    "version": "1.0.0",
    "device_type": "desktop"
  },
  "correlation_id": "corr-abc-123-def-456",
  "session_id": "sess-xyz-789",
  "client_info": {
    "browser": "Chrome",
    "os": "Windows 10",
    "timezone": "America/New_York"
  }
}
```

### Task Update Entry
```json
{
  "id": 1002,
  "event_id": "evt-12346-bcdef",
  "user_id": "user-67890",
  "task_id": 12345,
  "operation_type": "UPDATE",
  "timestamp": "2024-01-15T11:45:22.456Z",
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "previous_values": {
    "title": "Complete project proposal",
    "status": "pending",
    "priority": "high",
    "due_at": "2024-01-20T09:00:00Z"
  },
  "new_values": {
    "title": "Complete Q4 project proposal",
    "status": "in-progress",
    "priority": "high",
    "due_at": "2024-01-25T09:00:00Z",
    "updated_at": "2024-01-15T11:45:22Z"
  },
  "metadata": {
    "source": "web",
    "version": "1.0.0",
    "device_type": "desktop",
    "fields_changed": ["title", "status", "due_at"]
  },
  "correlation_id": "corr-abc-123-def-457",
  "session_id": "sess-xyz-789",
  "client_info": {
    "browser": "Chrome",
    "os": "Windows 10",
    "timezone": "America/New_York"
  }
}
```

### Task Completion Entry
```json
{
  "id": 1003,
  "event_id": "evt-12347-cdefg",
  "user_id": "user-67890",
  "task_id": 12345,
  "operation_type": "COMPLETE",
  "timestamp": "2024-01-25T14:20:10.789Z",
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)",
  "previous_values": {
    "status": "in-progress",
    "completed_at": null
  },
  "new_values": {
    "status": "completed",
    "completed_at": "2024-01-25T14:20:10Z",
    "updated_at": "2024-01-25T14:20:10Z"
  },
  "metadata": {
    "source": "mobile",
    "version": "1.0.0",
    "device_type": "mobile"
  },
  "correlation_id": "corr-abc-123-def-458",
  "session_id": "sess-uvw-012",
  "client_info": {
    "browser": "Mobile Safari",
    "os": "iOS 15.0",
    "timezone": "America/Los_Angeles"
  }
}
```

## Querying Capabilities

### Common Queries
```sql
-- Get all operations for a specific task
SELECT * FROM task_audit_log WHERE task_id = 12345 ORDER BY timestamp DESC;

-- Get all operations by a specific user
SELECT * FROM task_audit_log WHERE user_id = 'user-67890' ORDER BY timestamp DESC;

-- Get all operations of a specific type within a date range
SELECT * FROM task_audit_log
WHERE operation_type = 'UPDATE'
AND timestamp BETWEEN '2024-01-01' AND '2024-01-31'
ORDER BY timestamp DESC;

-- Count operations by type for a specific user
SELECT operation_type, COUNT(*) as count
FROM task_audit_log
WHERE user_id = 'user-67890'
GROUP BY operation_type;
```

## Error Handling and Retries

### Failure Scenarios
- Database connection failures
- Disk space issues (for file storage)
- Network issues during Dapr Pub/Sub communication

### Retry Logic
```javascript
async function storeAuditLogWithRetry(auditEntry, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await storeAuditLog(auditEntry);
    } catch (error) {
      if (attempt === maxRetries) {
        console.error(`Failed to store audit log after ${maxRetries} attempts:`, error);

        // Store in a dead letter queue or backup location
        await storeFailedAuditLog(auditEntry, error);
        throw error;
      }

      // Wait before retry with exponential backoff
      await sleep(Math.pow(2, attempt) * 1000);
    }
  }
}
```

## Security Considerations
- Encrypt sensitive data in audit logs
- Implement access controls for audit log data
- Regular security audits of the logging system
- Data retention policies to comply with regulations

## Dependencies
- Dapr runtime for pub/sub capabilities
- Database system (PostgreSQL, MySQL, etc.) or file system access
- Logging framework for error handling
- Monitoring and alerting system