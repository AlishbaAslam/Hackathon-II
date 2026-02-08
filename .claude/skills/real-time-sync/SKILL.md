# Real-Time Sync Skill

## Overview
The `real-time-sync` skill implements a real-time synchronization system that listens to the "task-updates" topic via Dapr Pub/Sub and broadcasts task changes to all connected clients using WebSocket connections. This enables real-time updates across multiple clients without requiring manual refresh or polling.

## Features
- Listen to "task-updates" topic for task change events
- Manage WebSocket connections with connected clients
- Broadcast task changes to all relevant connected clients
- Support for different event types (ADD, CHANGE, STATUS_CHANGE, REMOVE)
- Connection management and error handling

## WebSocket Connection Management

### Connection Schema
```typescript
interface WebSocketConnection {
  id: string;                // Unique connection ID
  userId: string;            // Associated user ID
  socket: WebSocket;         // WebSocket connection object
  connectedAt: Date;         // Connection establishment time
  lastActivity: Date;        // Last activity timestamp
  subscriptions: string[];   // Task subscriptions for this user
}
```

### Connection Handler Implementation
```javascript
class WebSocketManager {
  constructor() {
    this.connections = new Map(); // userId -> [WebSocketConnection]
    this.broadcastTopic = 'task-updates';
  }

  // Initialize WebSocket server
  async initializeWebSocketServer(server) {
    const wss = new WebSocket.Server({ server });

    wss.on('connection', (ws, req) => {
      // Extract user ID from connection headers or JWT token
      const userId = this.extractUserIdFromRequest(req);

      if (!userId) {
        ws.close(4001, 'Unauthorized: Missing or invalid user ID');
        return;
      }

      // Create new connection object
      const connectionId = this.generateConnectionId();
      const connection = {
        id: connectionId,
        userId: userId,
        socket: ws,
        connectedAt: new Date(),
        lastActivity: new Date(),
        subscriptions: []
      };

      // Store the connection
      this.addConnection(connection);

      // Set up event listeners for the WebSocket
      this.setupConnectionListeners(ws, connection);

      console.log(`New WebSocket connection established for user ${userId} (${connectionId})`);
    });

    // Subscribe to Dapr Pub/Sub for task updates
    await this.subscribeToTaskUpdates();
  }

  // Extract user ID from request (could be from JWT, header, or query param)
  extractUserIdFromRequest(req) {
    // Example: Extract from Authorization header
    const authHeader = req.headers.authorization;
    if (authHeader && authHeader.startsWith('Bearer ')) {
      try {
        const token = authHeader.substring(7);
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        return decoded.userId;
      } catch (error) {
        console.error('Failed to decode JWT:', error);
        return null;
      }
    }

    // Alternative: Extract from query parameter
    const urlParams = new URLSearchParams(req.url.split('?')[1]);
    return urlParams.get('userId');
  }

  // Add a new connection to the registry
  addConnection(connection) {
    if (!this.connections.has(connection.userId)) {
      this.connections.set(connection.userId, []);
    }

    this.connections.get(connection.userId).push(connection);
  }

  // Remove a connection from the registry
  removeConnection(connectionId) {
    for (const [userId, connections] of this.connections.entries()) {
      const index = connections.findIndex(conn => conn.id === connectionId);
      if (index !== -1) {
        connections.splice(index, 1);

        // Clean up user entry if no connections remain
        if (connections.length === 0) {
          this.connections.delete(userId);
        }
        return true;
      }
    }
    return false;
  }

  // Get all connections for a specific user
  getUserConnections(userId) {
    return this.connections.get(userId) || [];
  }

  // Set up listeners for WebSocket events
  setupConnectionListeners(ws, connection) {
    ws.on('message', (data) => {
      this.handleClientMessage(data, connection);
    });

    ws.on('close', () => {
      this.removeConnection(connection.id);
      console.log(`WebSocket connection closed for user ${connection.userId} (${connection.id})`);
    });

    ws.on('error', (error) => {
      console.error(`WebSocket error for user ${connection.userId}:`, error);
      this.removeConnection(connection.id);
    });

    ws.on('pong', () => {
      connection.lastActivity = new Date();
    });
  }

  // Handle messages from connected clients
  handleClientMessage(data, connection) {
    try {
      const message = JSON.parse(data.toString());
      connection.lastActivity = new Date();

      switch (message.type) {
        case 'subscribe':
          this.handleSubscription(message, connection);
          break;
        case 'unsubscribe':
          this.handleUnsubscription(message, connection);
          break;
        case 'ping':
          connection.socket.send(JSON.stringify({ type: 'pong' }));
          break;
        default:
          console.warn(`Unknown message type: ${message.type}`);
      }
    } catch (error) {
      console.error('Error parsing client message:', error);
    }
  }

  // Handle subscription requests
  handleSubscription(message, connection) {
    if (message.taskId) {
      connection.subscriptions.push(message.taskId);
    } else if (message.all) {
      // Subscribe to all user's tasks
      connection.subscriptions.push('ALL');
    }
  }

  // Handle unsubscription requests
  handleUnsubscription(message, connection) {
    if (message.taskId) {
      const index = connection.subscriptions.indexOf(message.taskId);
      if (index > -1) {
        connection.subscriptions.splice(index, 1);
      }
    } else if (message.all) {
      connection.subscriptions = [];
    }
  }

  // Generate unique connection ID
  generateConnectionId() {
    return `conn-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}
```

## Task Updates Topic Listener

### Event Processing
```javascript
// Subscribe to task-updates topic via Dapr Pub/Sub
async function subscribeToTaskUpdates() {
  daprClient.pubsub.subscribe(
    'task-updates',
    'real-time-sync',
    handleTaskUpdateEvent
  );
}

async function handleTaskUpdateEvent(event) {
  try {
    const parsedEvent = parseTaskUpdateEvent(event);

    // Broadcast the event to all relevant connected clients
    await broadcastToConnectedClients(parsedEvent);

    console.log(`Broadcasted task update event: ${parsedEvent.event_type} for task ${parsedEvent.task_id}`);
  } catch (error) {
    console.error('Failed to handle task update event:', error);
  }
}

function parseTaskUpdateEvent(event) {
  return {
    event_id: event.id,
    event_type: event.type,
    user_id: event.user_id,
    task_id: event.task_id,
    task_data: event.data,
    timestamp: event.timestamp || new Date().toISOString(),
    metadata: event.metadata || {}
  };
}
```

## WebSocket Broadcasting

### Broadcast Implementation
```javascript
// Broadcast task update to all connected clients
async function broadcastToConnectedClients(event) {
  const message = {
    type: 'task_update',
    event_type: event.event_type,
    task_id: event.task_id,
    user_id: event.user_id,
    data: event.task_data,
    timestamp: event.timestamp,
    metadata: event.metadata
  };

  // Convert event type to broadcast action
  const broadcastAction = mapEventTypeToBroadcastAction(event.event_type);

  // Prepare the broadcast message based on action type
  const broadcastMessage = {
    action: broadcastAction,
    ...message
  };

  // Get all connections for the affected user
  const userConnections = webSocketManager.getUserConnections(event.user_id);

  // Send the message to all connected sockets for this user
  userConnections.forEach(connection => {
    try {
      // Check if connection is still alive
      if (connection.socket.readyState === WebSocket.OPEN) {
        connection.socket.send(JSON.stringify(broadcastMessage));
        console.log(`Sent ${broadcastAction} update to user ${event.user_id} (connection ${connection.id})`);
      } else {
        // Remove dead connections
        webSocketManager.removeConnection(connection.id);
      }
    } catch (error) {
      console.error(`Failed to send message to user ${event.user_id}:`, error);
      webSocketManager.removeConnection(connection.id);
    }
  });

  // Also broadcast to any clients watching shared tasks (if applicable)
  await broadcastToSharedTaskWatchers(event, broadcastMessage);
}

function mapEventTypeToBroadcastAction(eventType) {
  const eventTypeToActionMap = {
    'TASK_ADDED': 'task_created',
    'TASK_CHANGED': 'task_updated',
    'TASK_STATUS_CHANGED': 'task_status_changed',
    'TASK_REMOVED': 'task_deleted',
    'TASK_RESTORED': 'task_restored'
  };

  return eventTypeToActionMap[eventType] || 'task_unknown_event';
}

// Broadcast to clients watching shared tasks
async function broadcastToSharedTaskWatchers(event, broadcastMessage) {
  // This would be implemented based on your sharing model
  // For example, if tasks can be shared among users
  const sharedWithUsers = await getSharedWithUsers(event.task_id);

  for (const userId of sharedWithUsers) {
    const connections = webSocketManager.getUserConnections(userId);
    connections.forEach(connection => {
      try {
        if (connection.socket.readyState === WebSocket.OPEN) {
          connection.socket.send(JSON.stringify(broadcastMessage));
        }
      } catch (error) {
        console.error(`Failed to send shared task update to user ${userId}:`, error);
      }
    });
  }
}
```

## Example WebSocket Broadcast Messages

### Task Created Event
```json
{
  "type": "task_update",
  "action": "task_created",
  "event_type": "TASK_ADDED",
  "task_id": 12345,
  "user_id": "user-67890",
  "data": {
    "id": 12345,
    "user_id": "user-67890",
    "title": "New task created",
    "description": "Description of the new task",
    "status": "pending",
    "priority": "medium",
    "due_at": "2024-01-30T10:00:00Z",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  "timestamp": "2024-01-15T10:30:00.123Z",
  "metadata": {
    "source": "web",
    "version": "1.0.0"
  }
}
```

### Task Updated Event
```json
{
  "type": "task_update",
  "action": "task_updated",
  "event_type": "TASK_CHANGED",
  "task_id": 12345,
  "user_id": "user-67890",
  "data": {
    "id": 12345,
    "user_id": "user-67890",
    "title": "Updated task title",
    "description": "Updated description of the task",
    "status": "in-progress",
    "priority": "high",
    "due_at": "2024-01-30T10:00:00Z",
    "updated_at": "2024-01-15T11:45:00Z"
  },
  "timestamp": "2024-01-15T11:45:00.456Z",
  "metadata": {
    "source": "mobile",
    "version": "1.0.0",
    "fields_changed": ["title", "status", "priority"]
  }
}
```

### Task Status Changed Event
```json
{
  "type": "task_update",
  "action": "task_status_changed",
  "event_type": "TASK_STATUS_CHANGED",
  "task_id": 12345,
  "user_id": "user-67890",
  "data": {
    "id": 12345,
    "status": "completed",
    "completed_at": "2024-01-15T14:20:00Z",
    "updated_at": "2024-01-15T14:20:00Z"
  },
  "timestamp": "2024-01-15T14:20:00.789Z",
  "metadata": {
    "source": "mobile",
    "version": "1.0.0",
    "previous_status": "in-progress"
  }
}
```

## Client-Side WebSocket Implementation

### Example Client Code
```javascript
class TaskSyncClient {
  constructor(userId, onTaskUpdate) {
    this.userId = userId;
    this.onTaskUpdate = onTaskUpdate;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000; // Start with 1 second
  }

  async connect() {
    const token = localStorage.getItem('jwt_token');
    const wsUrl = `${window.location.protocol === 'https:' ? 'wss://' : 'ws://'}${window.location.host}/ws?userId=${this.userId}&token=${token}`;

    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      console.log('Connected to real-time sync service');
      this.reconnectAttempts = 0; // Reset on successful connection

      // Subscribe to all user's tasks
      this.subscribeToAllTasks();
    };

    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.onTaskUpdate(message);
    };

    this.ws.onclose = (event) => {
      console.log('WebSocket connection closed:', event.code, event.reason);

      // Attempt to reconnect
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        setTimeout(() => {
          this.reconnectAttempts++;
          this.connect();
        }, this.reconnectDelay * Math.pow(2, this.reconnectAttempts)); // Exponential backoff
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  subscribeToAllTasks() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        type: 'subscribe',
        all: true
      }));
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
    }
  }
}
```

## Connection Health and Maintenance

### Heartbeat System
```javascript
// Implement periodic ping/pong to detect broken connections
setInterval(() => {
  for (const [userId, connections] of webSocketManager.connections.entries()) {
    connections.forEach(connection => {
      if (connection.socket.readyState === WebSocket.OPEN) {
        // Send ping to check if connection is still alive
        connection.socket.ping();
      } else {
        // Remove dead connections
        webSocketManager.removeConnection(connection.id);
      }
    });
  }
}, 30000); // Ping every 30 seconds
```

## Error Handling and Recovery

### Connection Error Handling
```javascript
// Handle connection errors and implement recovery mechanisms
async function handleConnectionError(connection, error) {
  console.error(`Connection error for user ${connection.userId}:`, error);

  // Log the error for monitoring
  await logConnectionError(connection, error);

  // Attempt to notify the client
  try {
    if (connection.socket.readyState === WebSocket.OPEN) {
      connection.socket.send(JSON.stringify({
        type: 'error',
        message: 'Connection error occurred, attempting to recover'
      }));
    }
  } catch (sendError) {
    console.error('Failed to send error message to client:', sendError);
  }

  // Remove the connection if it's no longer viable
  webSocketManager.removeConnection(connection.id);
}
```

## Dependencies
- Dapr runtime for pub/sub capabilities
- WebSocket server library (ws, Socket.IO, etc.)
- JWT library for authentication
- Database for storing connection state (optional)
- Monitoring and logging system