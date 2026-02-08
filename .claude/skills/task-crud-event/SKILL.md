# Task CRUD Event Skill

## Overview
The `task-crud-event` skill provides comprehensive task management functionality with full CRUD operations, robust validation, and event-driven architecture. This skill handles all aspects of task lifecycle management while publishing relevant events to Kafka topics via Dapr Pub/Sub for audit logging, recurring task management, reminder systems, and real-time synchronization.

## Features
- Full task CRUD operations (Create, Read, Update, Delete, Complete)
- Field validation for required attributes (title, status, due_at, remind_at)
- Event publishing to Kafka topics via Dapr Pub/Sub
- Soft delete with `deleted_at` timestamp
- Comprehensive error handling and transaction management

## Task Schema

```typescript
interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  status: 'pending' | 'in-progress' | 'completed';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  due_at?: Date;
  remind_at?: Date;
  completed_at?: Date;
  created_at: Date;
  updated_at: Date;
  deleted_at?: Date; // For soft deletes
  tags?: string[];
}
```

## Operations

### Create Task
- **Input Validation**:
  - `title`: Required (string, min 1 character)
  - `status`: Required, must be one of ['pending', 'in-progress', 'completed']
  - `due_at`: Optional, must be a valid future date if provided
  - `remind_at`: Optional, must be before `due_at` if both are provided
- **Process**:
  - Validate all input fields
  - Create task record with current timestamp
  - Publish `TASK_CREATED` event to `task-events` topic
  - If `remind_at` is set, publish `REMINDER_SCHEDULED` to `reminders` topic
  - Publish `TASK_ADDED` event to `task-updates` topic for real-time sync
- **Returns**: Created task object with ID

### Read Task
- **Single Task**: Get task by ID with user isolation
- **List Tasks**:
  - Filter by status, priority, due date ranges
  - Pagination support (limit, offset)
  - Exclude soft-deleted records by default
- **Validation**: Verify user ownership of requested task(s)

### Update Task
- **Input Validation**:
  - Allow updates to any field except `id` and `created_at`
  - Maintain validation rules for required fields
  - Validate date relationships (remind_at before due_at)
- **Process**:
  - Validate all input fields
  - Apply updates to task record
  - Update `updated_at` timestamp
  - Publish `TASK_UPDATED` event to `task-events` topic
  - If `remind_at` changed, update or schedule reminders in `reminders` topic
  - Publish `TASK_CHANGED` event to `task-updates` topic for real-time sync
- **Returns**: Updated task object

### Complete Task
- **Process**:
  - Validate task exists and belongs to user
  - Update status to 'completed'
  - Set `completed_at` to current timestamp
  - Publish `TASK_COMPLETED` event to `task-events` topic
  - If recurring, schedule next occurrence
  - Publish `TASK_STATUS_CHANGED` event to `task-updates` topic for real-time sync
- **Returns**: Updated task object

### Delete Task (Soft Delete)
- **Process**:
  - Validate task exists and belongs to user
  - Set `deleted_at` to current timestamp (soft delete)
  - Clear any pending reminders
  - Publish `TASK_DELETED` event to `task-events` topic
  - Publish `TASK_REMOVED` event to `task-updates` topic for real-time sync
- **Returns**: Success confirmation

### Restore Task (Undo Soft Delete)
- **Process**:
  - Validate task exists and belongs to user
  - Clear `deleted_at` timestamp
  - Publish `TASK_RESTORED` event to `task-events` topic
  - Publish `TASK_ADDED` event to `task-updates` topic for real-time sync
- **Returns**: Restored task object

## Event Publishing

### Kafka Topics via Dapr Pub/Sub

#### `task-events` Topic
Used for audit logging and recurring task management:
- `TASK_CREATED`: When a new task is created
- `TASK_UPDATED`: When a task is updated
- `TASK_COMPLETED`: When a task is marked complete
- `TASK_DELETED`: When a task is soft deleted
- `TASK_RESTORED`: When a task is restored from deletion

#### `reminders` Topic
Used for due date and reminder notifications:
- `REMINDER_SCHEDULED`: When `remind_at` is set on a task
- `REMINDER_UPDATED`: When `remind_at` is changed
- `REMINDER_CANCELLED`: When a reminder is no longer needed

#### `task-updates` Topic
Used for real-time synchronization:
- `TASK_ADDED`: When a task is created or restored
- `TASK_CHANGED`: When a task is updated
- `TASK_STATUS_CHANGED`: When task status changes
- `TASK_REMOVED`: When a task is deleted

## Implementation Details

### Database Considerations
- Use transactions for all operations that modify data
- Include soft delete in all SELECT queries by default
- Provide option to include soft-deleted records when needed
- Use proper indexing for common query patterns (user_id, status, due_at)

### Validation Rules
- Title must be 1-255 characters
- Status must be one of allowed values
- Due date must be in the future (if provided)
- Remind date must be before due date (if both provided)
- Priority must be one of allowed values
- Tags must be valid (if provided)

### Error Handling
- Return appropriate HTTP status codes
- Provide meaningful error messages
- Log errors for monitoring and debugging
- Handle duplicate key violations appropriately

### Security
- Enforce user isolation through user_id validation
- Validate JWT tokens for authentication
- Sanitize all inputs to prevent injection attacks
- Implement rate limiting for API endpoints

## Usage Examples

### Creating a Task
```javascript
const task = await createTask({
  user_id: "user123",
  title: "Complete project proposal",
  description: "Finish the Q4 project proposal document",
  status: "pending",
  priority: "high",
  due_at: new Date("2024-12-31"),
  remind_at: new Date("2024-12-30T09:00:00Z")
});
```

### Updating a Task
```javascript
const updatedTask = await updateTask({
  id: 123,
  user_id: "user123",
  title: "Complete revised project proposal",
  status: "in-progress"
});
```

### Completing a Task
```javascript
const completedTask = await completeTask(123, "user123");
```

## Dependencies
- Dapr runtime for pub/sub capabilities
- Kafka or compatible message broker
- Database with transaction support
- JWT authentication middleware