# Data Model: Frontend UI for Todo Web Application

## User Entity

**Fields**:
- id: string (unique identifier)
- email: string (user's email address)
- name: string (optional, user's display name)
- createdAt: string (ISO date string)
- updatedAt: string (ISO date string)

**Validation rules**:
- email must be a valid email format
- email must be unique across all users
- id must be unique and non-empty

**State transitions**:
- Unauthenticated → Authenticated (on successful login)
- Authenticated → Unauthenticated (on logout or token expiration)

## Task Entity

**Fields**:
- id: string (unique identifier)
- title: string (task title, required)
- description: string (optional task description)
- completed: boolean (task completion status)
- userId: string (foreign key to User)
- createdAt: string (ISO date string)
- updatedAt: string (ISO date string)

**Validation rules**:
- title must be non-empty
- userId must reference an existing user
- id must be unique and non-empty

**State transitions**:
- Pending → Completed (when user marks task as complete)
- Completed → Pending (when user unmarks task as complete)

## Relationships

- User (1) → Task (Many): A user can have many tasks
- Task (Many) → User (1): Each task belongs to one user

## API Response Structures

### Authentication Responses
- LoginSuccess: { token: string, user: User }
- LoginError: { error: string, message: string }
- SignupSuccess: { token: string, user: User }
- SignupError: { error: string, message: string }

### Task API Responses
- TaskList: { tasks: Task[] }
- TaskSingle: { task: Task }
- TaskError: { error: string, message: string }