# Recurring Task Creation Skill

## Overview
The `recurring-task-creation` skill implements an event-driven system that listens to the "task-events" topic via Dapr Pub/Sub. When a recurring task is marked as "completed", this skill automatically creates the next occurrence of the task based on its recurrence pattern (daily, weekly, or monthly). The newly created task is published back to the "task-events" topic to maintain the event-driven architecture.

## Features
- Listen to "task-events" topic for task completion events
- Identify recurring tasks and their patterns
- Calculate next occurrence date based on recurrence pattern
- Create new task instance with updated dates
- Publish new task event to "task-events" topic

## Task Schema Extension

```typescript
interface RecurringTask extends Task {
  is_recurring: boolean;
  recurrence_pattern: 'daily' | 'weekly' | 'monthly' | 'yearly';
  recurrence_interval: number; // How often the pattern repeats (e.g., every 2 days, every 3 weeks)
  recurrence_end_date?: Date; // Optional end date for the recurrence
  original_task_id?: number; // Reference to the original task that spawned this occurrence
  occurrence_number: number; // Which occurrence this is in the series
}
```

## Event Processing Logic

### 1. Event Subscription
- Subscribe to "task-events" topic via Dapr Pub/Sub
- Filter events for `TASK_COMPLETED` events
- Check if the completed task has `is_recurring: true`

### 2. Recurrence Pattern Detection
- Determine the recurrence pattern from the completed task
- Validate that the task is indeed recurring
- Check if recurrence should continue (not past end date)

### 3. Next Occurrence Calculation

#### Daily Recurrence
- **Pattern**: `recurrence_pattern: 'daily'`
- **Calculation**: Add `recurrence_interval` days to the current task's `due_at` date
- **Example**: If a daily task with `recurrence_interval: 1` is completed on 2024-01-15, the next occurrence will be scheduled for 2024-01-16

```javascript
function calculateNextDailyDate(currentDueDate, interval) {
  const nextDate = new Date(currentDueDate);
  nextDate.setDate(nextDate.getDate() + interval);
  return nextDate;
}
```

#### Weekly Recurrence
- **Pattern**: `recurrence_pattern: 'weekly'`
- **Calculation**: Add `recurrence_interval * 7` days to the current task's `due_at` date
- **Special Handling**: Preserve the day of the week from the original task
- **Example**: If a weekly task is completed on Monday 2024-01-15, the next occurrence will be the following Monday (or after `interval` weeks)

```javascript
function calculateNextWeeklyDate(currentDueDate, interval) {
  const nextDate = new Date(currentDueDate);
  nextDate.setDate(nextDate.getDate() + (interval * 7));
  return nextDate;
}
```

#### Monthly Recurrence
- **Pattern**: `recurrence_pattern: 'monthly'`
- **Calculation**: Add `recurrence_interval` months to the current task's `due_at` date
- **Special Handling**: Handle month-end edge cases (e.g., Jan 31 + 1 month = Feb 28/29)
- **Example**: If a monthly task is completed on January 15th, the next occurrence will be February 15th

```javascript
function calculateNextMonthlyDate(currentDueDate, interval) {
  const nextDate = new Date(currentDueDate);
  const originalDay = nextDate.getDate();

  // Add months
  nextDate.setMonth(nextDate.getMonth() + interval);

  // Handle month-end edge cases (e.g., Jan 31 + 1 month)
  // If the new month has fewer days, adjust to the last day of that month
  if (nextDate.getDate() !== originalDay) {
    // Adjust to the last day of the target month
    nextDate.setDate(0); // Set to last day of previous month
  }

  return nextDate;
}
```

#### Yearly Recurrence
- **Pattern**: `recurrence_pattern: 'yearly'`
- **Calculation**: Add `recurrence_interval` years to the current task's `due_at` date
- **Special Handling**: Handle leap year edge cases (e.g., Feb 29 + 1 year = Feb 28)
- **Example**: If a yearly task is completed on 2024-02-29, the next occurrence will be 2025-02-28

```javascript
function calculateNextYearlyDate(currentDueDate, interval) {
  const nextDate = new Date(currentDueDate);
  const originalMonth = nextDate.getMonth();
  const originalDay = nextDate.getDate();

  // Add years
  nextDate.setFullYear(nextDate.getFullYear() + interval);

  // Handle leap year edge cases (e.g., Feb 29 + 1 year)
  // If the calculated date moved to a different month, adjust to last day of target month
  if (nextDate.getMonth() !== originalMonth) {
    // Adjust to the last day of the target month
    nextDate.setDate(0);
  }

  return nextDate;
}
```

### 4. Recurrence End Conditions
The system checks the following conditions to determine if a recurring task should continue:
- If `recurrence_end_date` is set, compare with the calculated next occurrence date
- If the task has a maximum number of occurrences, increment counter and check
- If the recurrence pattern is invalid or missing, stop the recurrence

### 5. New Task Creation Process
When creating the next occurrence, the system:

1. **Copies Task Properties**: Most properties from the completed task are copied to the new task
2. **Updates Dates**:
   - `due_at`: Updated to the calculated next occurrence date
   - `remind_at`: Adjusted proportionally to maintain the same time difference from due date
   - `created_at`: Set to current timestamp
   - `updated_at`: Set to current timestamp
   - `completed_at`: Reset to undefined
3. **Sets Recurrence Fields**:
   - `original_task_id`: Points to the original recurring task
   - `occurrence_number`: Incremented from the previous occurrence
4. **Resets Status**: Sets status back to 'pending'

### 6. Event Publishing
After creating the new task:
- Publish a `TASK_CREATED` event to the "task-events" topic
- Include all relevant task information in the event payload
- This allows other services to react to the new task creation

## Implementation Algorithm

```javascript
async function processTaskCompletedEvent(taskEvent) {
  // 1. Validate the event is for a completed recurring task
  if (!taskEvent.is_recurring || taskEvent.status !== 'completed') {
    return; // Not a recurring task completion, ignore
  }

  // 2. Check if recurrence should continue
  if (hasRecurrenceEnded(taskEvent)) {
    return; // Recurrence has ended, no more occurrences
  }

  // 3. Calculate the next occurrence date
  const nextOccurrenceDate = calculateNextOccurrenceDate(taskEvent);

  // 4. Create the new task instance
  const newTask = createNextOccurrence(taskEvent, nextOccurrenceDate);

  // 5. Persist the new task to the database
  const persistedTask = await saveTask(newTask);

  // 6. Publish the new task event
  await publishTaskCreatedEvent(persistedTask);
}

function calculateNextOccurrenceDate(task) {
  switch (task.recurrence_pattern) {
    case 'daily':
      return calculateNextDailyDate(task.due_at, task.recurrence_interval);
    case 'weekly':
      return calculateNextWeeklyDate(task.due_at, task.recurrence_interval);
    case 'monthly':
      return calculateNextMonthlyDate(task.due_at, task.recurrence_interval);
    case 'yearly':
      return calculateNextYearlyDate(task.due_at, task.recurrence_interval);
    default:
      throw new Error(`Unsupported recurrence pattern: ${task.recurrence_pattern}`);
  }
}
```

## Error Handling

### Retry Logic
- Implement retry mechanism for failed task creations
- Use exponential backoff for transient failures
- Log failed attempts for monitoring and alerting

### Validation Checks
- Verify that the completed task is indeed recurring
- Validate that the recurrence pattern is supported
- Ensure the next occurrence date is in the future
- Confirm that recurrence hasn't exceeded end conditions

## Monitoring and Observability
- Track metrics for recurring task creation success/failure rates
- Monitor for tasks that fail to create subsequent occurrences
- Log important events for debugging and auditing purposes

## Dependencies
- Dapr runtime for pub/sub capabilities
- Database for storing tasks
- Logging system for observability