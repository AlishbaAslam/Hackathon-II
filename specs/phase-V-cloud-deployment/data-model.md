# Data Model: Phase V - Advanced Cloud-Native Todo Chatbot

## Enhanced Task Entity

### Task Model
Represents a user's task with advanced features including recurrence, scheduling, and categorization.

**Fields:**
- `id`: Integer (Primary Key, Auto-increment)
- `user_id`: String (Foreign Key to User, required for user isolation)
- `title`: String (Task title, required, max 255 chars)
- `description`: Text (Optional task description)
- `completed`: Boolean (Completion status, default: false)
- `created_at`: DateTime (Timestamp of creation, auto-generated)
- `updated_at`: DateTime (Timestamp of last update, auto-generated)
- `due_at`: DateTime (Optional due date/time for the task)
- `remind_at`: DateTime (Optional reminder time for notifications)
- `priority`: Enum (Values: 'low', 'medium', 'high', 'urgent', default: 'medium')
- `tags`: JSON (Array of string tags for categorization, e.g., ['work', 'personal'])
- `recurrence_pattern`: JSON (Recurrence configuration object, optional)
  - `type`: Enum ('none', 'daily', 'weekly', 'monthly', 'yearly')
  - `interval`: Integer (Interval multiplier, e.g., every 2 weeks)
  - `end_condition`: Object (Either 'after_occurrences': int or 'until_date': datetime)
- `parent_task_id`: Integer (Foreign Key to Task, for recurring task lineage, nullable)
- `next_occurrence_id`: Integer (Foreign Key to Task, next occurrence in series, nullable)

### Recurrence Pattern Details
When a recurring task is completed, the system automatically creates the next occurrence based on the recurrence_pattern. The original task becomes the "template" for future occurrences.

## User Entity (Existing, Extended)

### User Model
Represents a registered user in the system with authentication details.

**Fields:**
- `id`: Integer (Primary Key, Auto-increment)
- `email`: String (Unique email address, required)
- `hashed_password`: String (BCrypt hashed password, required)
- `full_name`: String (User's full name, optional)
- `created_at`: DateTime (Account creation timestamp, auto-generated)
- `updated_at`: DateTime (Last update timestamp, auto-generated)
- `is_active`: Boolean (Account status, default: true)

## Conversation Entity (Enhanced)

### Conversation Model
Represents a chat session between user and AI assistant for task management.

**Fields:**
- `id`: Integer (Primary Key, Auto-increment)
- `user_id`: String (Foreign Key to User, required for user isolation)
- `title`: String (Conversation title, optional, auto-generated from first message)
- `created_at`: DateTime (Session creation timestamp, auto-generated)
- `updated_at`: DateTime (Last activity timestamp, auto-generated)

## Message Entity (Enhanced)

### Message Model
Represents a single message in a conversation between user and AI assistant.

**Fields:**
- `id`: Integer (Primary Key, Auto-increment)
- `user_id`: String (Foreign Key to User, required for user isolation)
- `conversation_id`: Integer (Foreign Key to Conversation, required)
- `role`: Enum ('user', 'assistant', 'system') (Message sender type)
- `content`: Text (Message content)
- `created_at`: DateTime (Message timestamp, auto-generated)
- `tool_calls`: JSON (Optional array of tool calls made during this message)
- `task_ids_referenced`: JSON (Optional array of task IDs referenced in message)

## Event Log Entity

### EventLog Model
Represents audit trail of all task operations for compliance and debugging.

**Fields:**
- `id`: Integer (Primary Key, Auto-increment)
- `user_id`: String (Foreign Key to User, required for user isolation)
- `event_type`: Enum ('task_created', 'task_updated', 'task_completed', 'task_deleted', 'task_recurring_generated', 'reminder_scheduled', 'notification_sent')
- `entity_type`: Enum ('task', 'conversation', 'message', 'reminder', 'notification')
- `entity_id`: Integer (ID of the affected entity)
- `previous_state`: JSON (Previous state of the entity before change, nullable)
- `new_state`: JSON (New state of the entity after change, nullable)
- `operation_details`: JSON (Additional details about the operation)
- `timestamp`: DateTime (Event timestamp, auto-generated)
- `source_service`: String (Service that generated the event, e.g., 'todo-api', 'recurring-task-service')

## Reminder Entity

### Reminder Model
Represents scheduled reminder notifications (may be stored separately for Dapr Jobs integration).

**Fields:**
- `id`: Integer (Primary Key, Auto-increment)
- `user_id`: String (Foreign Key to User, required for user isolation)
- `task_id`: Integer (Foreign Key to Task, required)
- `scheduled_time`: DateTime (When the reminder should be triggered)
- `notification_channels`: JSON (Array of channels to send notification, e.g., ['websocket', 'email', 'push'])
- `status`: Enum ('scheduled', 'triggered', 'cancelled', 'failed')
- `created_at`: DateTime (Creation timestamp, auto-generated)
- `triggered_at`: DateTime (Actual trigger time, nullable)

## WebSocket Session Entity

### WebSocketSession Model
Represents active WebSocket connections for real-time synchronization.

**Fields:**
- `id`: String (Primary Key, WebSocket connection ID)
- `user_id`: String (Foreign Key to User, required for user isolation)
- `connected_at`: DateTime (Connection establishment time)
- `last_heartbeat`: DateTime (Last heartbeat received from client)
- `status`: Enum ('connected', 'disconnected')
- `client_info`: JSON (Information about the client, e.g., device type, IP)

## Relationship Diagram

```
[User] 1 --- * [Task]
[User] 1 --- * [Conversation]
[User] 1 --- * [EventLog]
[User] 1 --- * [Reminder]
[User] 1 --- * [WebSocketSession]

[Conversation] 1 --- * [Message]

[Task] 1 --- * [Message] (via task_ids_referenced)

[Task] * --- 1 [Task] (via parent_task_id for recurring tasks)
[Task] 1 --- 1 [Task] (via next_occurrence_id for next occurrence)

[EventLog] * --- 1 [Task] (via entity_id when entity_type = 'task')
[EventLog] * --- 1 [User] (via entity_id when entity_type = 'user')
```

## Validation Rules

### Task Entity
- Title must be 1-255 characters
- Cannot set both due_at and remind_at in the past
- Priority must be one of the allowed enum values
- Tags array must contain only strings
- Recurrence pattern validation:
  - If recurrence_type != 'none', interval must be >= 1
  - End condition must specify either after_occurrences or until_date
  - Cannot set recurrence on already recurring task
  - Parent_task_id cannot create circular references

### User Entity
- Email must be valid email format and unique
- Hashed password must be properly formatted BCrypt hash

### Message Entity
- Role must be one of allowed enum values
- Content cannot be empty
- Conversation must belong to the same user

### EventLog Entity
- Event type must be one of allowed values
- Entity type and entity_id must reference a valid entity
- Previous and new state should be consistent with entity type

## State Transitions

### Task State Transitions
```
Pending -> Completed (via complete_task)
Completed -> Pending (via update_task with completed=false)
Any -> Deleted (via delete_task)
```

### Recurring Task State Transitions
```
Active Recurring -> Completed -> Next Occurrence Created -> New Active Recurring
Active Recurring -> Deleted -> Series Stopped
```

### Reminder State Transitions
```
Scheduled -> Triggered (automatically at scheduled_time)
Scheduled -> Cancelled (when task is deleted/completed early)
Scheduled -> Failed (if notification delivery fails)
```

## Indexes for Performance

### Task Table
- Index on `(user_id, completed)` for efficient user task queries
- Index on `due_at` for efficient due date queries
- Index on `remind_at` for efficient reminder scheduling
- Index on `parent_task_id` for efficient recurrence queries

### EventLog Table
- Index on `(user_id, timestamp DESC)` for user audit trails
- Index on `event_type` for efficient event type queries
- Index on `entity_type, entity_id` for entity-specific events

### Message Table
- Index on `(conversation_id, created_at)` for chronological conversation retrieval
- Index on `user_id` for user message queries