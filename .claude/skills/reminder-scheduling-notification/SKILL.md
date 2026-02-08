# Reminder Scheduling Notification Skill

## Overview
The `reminder-scheduling-notification` skill implements an event-driven reminder system that listens to the "reminders" topic via Dapr Pub/Sub. It schedules precise notifications using Dapr Jobs API for exact time triggering without polling. When the scheduled reminder time arrives, the system sends notifications via push, email, or console simulation depending on the configuration.

## Features
- Listen to "reminders" topic for scheduling requests
- Schedule reminders using Dapr Jobs API with exact time triggers
- Deliver notifications without polling (event-driven)
- Support multiple notification channels (push, email, console)
- Handle reminder cancellation and updates

## Reminder Event Schema

```typescript
interface ReminderEvent {
  id: string;
  user_id: string;
  task_id?: number;
  title: string;
  message: string;
  scheduled_time: Date;
  notification_type: 'push' | 'email' | 'sms' | 'console';
  recipient: string; // Email address, device token, etc.
  priority: 'low' | 'normal' | 'high';
  metadata?: Record<string, any>; // Additional context for the notification
  action?: string; // Optional action to perform when reminder is triggered
}
```

## Architecture Overview

### 1. Event Processing Pipeline
- Subscribe to "reminders" topic via Dapr Pub/Sub
- Process three types of events:
  - `REMINDER_SCHEDULED`: Schedule a new reminder job
  - `REMINDER_UPDATED`: Reschedule an existing reminder job
  - `REMINDER_CANCELLED`: Cancel an existing reminder job

### 2. Dapr Jobs API Integration
- Use Dapr Jobs API to schedule exact-time job execution
- No polling required - jobs execute precisely at the scheduled time
- Leverage Dapr's reliable job scheduling and execution

## Scheduling Mechanism

### Job Creation Process
When a `REMINDER_SCHEDULED` event is received:

```javascript
async function handleReminderScheduled(reminderEvent) {
  // 1. Validate the reminder event
  if (!isValidReminder(reminderEvent)) {
    throw new Error('Invalid reminder event');
  }

  // 2. Create a Dapr Job with exact time trigger
  const jobPayload = {
    reminder_id: reminderEvent.id,
    user_id: reminderEvent.user_id,
    task_id: reminderEvent.task_id,
    title: reminderEvent.title,
    message: reminderEvent.message,
    notification_type: reminderEvent.notification_type,
    recipient: reminderEvent.recipient,
    priority: reminderEvent.priority,
    metadata: reminderEvent.metadata,
    action: reminderEvent.action
  };

  // 3. Schedule the job using Dapr Jobs API
  await daprClient.job.createJob({
    jobId: `reminder-${reminderEvent.id}`,
    schedule: reminderEvent.scheduled_time.toISOString(), // Exact time trigger
    target: {
      actor: 'notificationActor',
      method: 'sendNotification'
    },
    data: jobPayload,
    options: {
      maxRetries: 3,
      timeout: '5m'
    }
  });

  console.log(`Reminder scheduled for ${reminderEvent.scheduled_time} with ID: ${reminderEvent.id}`);
}
```

### Supported Scheduling Patterns

#### Exact Time Scheduling
```javascript
// Schedule for a specific date/time
const exactTimeSchedule = new Date('2024-12-25T09:00:00Z').toISOString();
```

#### Cron Expression Scheduling (Alternative)
```javascript
// For recurring reminders, cron expressions can be used
const cronSchedule = '0 9 * * 1-5'; // Every weekday at 9 AM
```

## Trigger Mechanism Without Polling

### Dapr Jobs API Advantages
- **Precise Timing**: Jobs execute exactly at the scheduled time
- **No Polling Overhead**: No need for constant database checks
- **Reliability**: Built-in retry mechanisms and failure handling
- **Scalability**: Distributed job execution across multiple instances

### Job Execution Flow
1. Dapr Jobs API receives the scheduled job
2. At the exact scheduled time, Dapr triggers the job
3. The job calls the designated target (actor/method)
4. Notification service processes the reminder and delivers it
5. Success/failure is logged and monitored

## Notification Delivery

### Example Trigger Code

```javascript
// Actor method that gets called by Dapr Jobs API
class NotificationActor {
  async sendNotification(jobData) {
    try {
      const { reminder_id, user_id, task_id, title, message,
              notification_type, recipient, priority, metadata, action } = jobData;

      // Deliver notification based on type
      switch (notification_type) {
        case 'push':
          await this.sendPushNotification(recipient, title, message, metadata);
          break;
        case 'email':
          await this.sendEmailNotification(recipient, title, message, metadata);
          break;
        case 'sms':
          await this.sendSMSNotification(recipient, message);
          break;
        case 'console':
          await this.sendConsoleNotification(user_id, title, message);
          break;
        default:
          throw new Error(`Unsupported notification type: ${notification_type}`);
      }

      // Log successful delivery
      await this.logNotificationDelivery(reminder_id, user_id, 'success');

      // Execute any associated action
      if (action) {
        await this.executeAction(action, user_id, task_id);
      }

      return { success: true, reminder_id };
    } catch (error) {
      console.error(`Failed to deliver notification for reminder ${jobData.reminder_id}:`, error);

      // Log failure
      await this.logNotificationDelivery(jobData.reminder_id, jobData.user_id, 'failed', error.message);

      // Optionally retry or escalate
      throw error;
    }
  }

  async sendPushNotification(deviceToken, title, message, metadata) {
    // Implementation for sending push notifications
    // Could use Firebase Cloud Messaging, Apple Push Notification Service, etc.
    console.log(`Sending push notification to ${deviceToken}: ${title} - ${message}`);

    // Example using a push notification service
    /*
    return await pushService.send({
      deviceToken,
      title,
      body: message,
      data: metadata
    });
    */
  }

  async sendEmailNotification(emailAddress, subject, body, metadata) {
    // Implementation for sending email notifications
    console.log(`Sending email to ${emailAddress}: ${subject}`);

    // Example using an email service
    /*
    return await emailService.send({
      to: emailAddress,
      subject: subject,
      html: `<p>${body}</p>`,
      metadata
    });
    */
  }

  async sendSMSNotification(phoneNumber, message) {
    // Implementation for sending SMS notifications
    console.log(`Sending SMS to ${phoneNumber}: ${message}`);

    // Example using an SMS service
    /*
    return await smsService.send({
      to: phoneNumber,
      message: message
    });
    */
  }

  async sendConsoleNotification(userId, title, message) {
    // Console simulation for development/testing
    console.log(`[${userId}] REMINDER: ${title} - ${message}`);
  }

  async executeAction(action, userId, taskId) {
    // Execute any associated action when reminder fires
    console.log(`Executing action '${action}' for user ${userId}, task ${taskId}`);

    // Implementation depends on the specific action
    // Could be triggering a webhook, updating a status, etc.
  }

  async logNotificationDelivery(reminderId, userId, status, errorMessage = null) {
    // Log notification delivery status for monitoring
    console.log(`Notification delivery - Reminder: ${reminderId}, User: ${userId}, Status: ${status}`);

    // In production, this would write to a database or logging system
    /*
    await db.notifications.insert({
      reminder_id: reminderId,
      user_id: userId,
      status: status,
      error_message: errorMessage,
      delivered_at: new Date()
    });
    */
  }
}
```

## Event Handling Examples

### Scheduling a New Reminder
```javascript
// Example event from "reminders" topic
const reminderEvent = {
  id: 'rem-12345',
  user_id: 'user-abc',
  task_id: 789,
  title: 'Meeting Reminder',
  message: 'Your team meeting starts in 15 minutes',
  scheduled_time: new Date('2024-01-15T09:45:00Z'),
  notification_type: 'push',
  recipient: 'device-token-xyz',
  priority: 'high'
};

await handleReminderScheduled(reminderEvent);
```

### Updating an Existing Reminder
```javascript
// Cancel the old job and schedule a new one
async function handleReminderUpdated(reminderEvent) {
  // Cancel existing job
  await daprClient.job.deleteJob(`reminder-${reminderEvent.id}`);

  // Schedule new job with updated time
  await handleReminderScheduled(reminderEvent);
}
```

### Cancelling a Reminder
```javascript
async function handleReminderCancelled(reminderId) {
  await daprClient.job.deleteJob(`reminder-${reminderId}`);
  console.log(`Reminder cancelled: ${reminderId}`);
}
```

## Error Handling and Retry Logic

### Job Failure Handling
- Dapr Jobs API includes built-in retry mechanisms
- Configure max retries and timeout options per job
- Implement dead letter queue for failed notifications
- Monitor and alert on job failures

### Compensation Logic
```javascript
async function handleJobFailure(jobId, error) {
  // Attempt compensation or alternative delivery method
  const reminderId = jobId.replace('reminder-', '');

  // Try alternative notification method
  await sendFallbackNotification(reminderId, error);

  // Alert administrators
  await alertAdmins(`Reminder job failed: ${jobId}`, error);
}
```

## Monitoring and Observability

### Metrics to Track
- Number of scheduled reminders
- Successful notification deliveries
- Failed notification deliveries
- Average delivery time
- Job execution duration

### Health Checks
- Dapr Jobs API connectivity
- Notification service availability
- Database connectivity for logging

## Dependencies
- Dapr runtime with Jobs API component
- Notification services (push, email, SMS gateways)
- Database for logging and tracking
- Monitoring and alerting system