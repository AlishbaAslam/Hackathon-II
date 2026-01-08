# API Contracts: Frontend UI for Todo Web Application

## Authentication Endpoints

### POST /api/auth/login
**Description**: Authenticate user and return JWT token
**Request**:
```json
{
  "email": "string",
  "password": "string"
}
```
**Response (200)**:
```json
{
  "token": "string",
  "user": {
    "id": "string",
    "email": "string",
    "name": "string"
  }
}
```
**Response (401)**:
```json
{
  "error": "string",
  "message": "string"
}
```

### POST /api/auth/signup
**Description**: Register new user and return JWT token
**Request**:
```json
{
  "email": "string",
  "password": "string",
  "name": "string"
}
```
**Response (200)**:
```json
{
  "token": "string",
  "user": {
    "id": "string",
    "email": "string",
    "name": "string"
  }
}
```
**Response (409)**:
```json
{
  "error": "string",
  "message": "string"
}
```

## Task Endpoints

### GET /api/users/{user_id}/tasks
**Description**: Get all tasks for a specific user
**Headers**: Authorization: Bearer {token}
**Response (200)**:
```json
{
  "tasks": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "completed": "boolean",
      "userId": "string",
      "createdAt": "string (ISO date)",
      "updatedAt": "string (ISO date)"
    }
  ]
}
```

### POST /api/users/{user_id}/tasks
**Description**: Create a new task for a user
**Headers**: Authorization: Bearer {token}
**Request**:
```json
{
  "title": "string",
  "description": "string"
}
```
**Response (201)**:
```json
{
  "task": {
    "id": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "userId": "string",
    "createdAt": "string (ISO date)",
    "updatedAt": "string (ISO date)"
  }
}
```

### PUT /api/tasks/{task_id}
**Description**: Update an existing task
**Headers**: Authorization: Bearer {token}
**Request**:
```json
{
  "title": "string",
  "description": "string",
  "completed": "boolean"
}
```
**Response (200)**:
```json
{
  "task": {
    "id": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "userId": "string",
    "createdAt": "string (ISO date)",
    "updatedAt": "string (ISO date)"
  }
}
```

### PATCH /api/tasks/{task_id}/complete
**Description**: Toggle task completion status
**Headers**: Authorization: Bearer {token}
**Request**:
```json
{
  "completed": "boolean"
}
```
**Response (200)**:
```json
{
  "task": {
    "id": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "userId": "string",
    "createdAt": "string (ISO date)",
    "updatedAt": "string (ISO date)"
  }
}
```

### DELETE /api/tasks/{task_id}
**Description**: Delete a task
**Headers**: Authorization: Bearer {token}
**Response (204)**: No content

## Error Response Format
**For all error responses**:
```json
{
  "error": "string",
  "message": "string"
}
```