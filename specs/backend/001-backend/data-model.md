# Phase 1: Data Model Design

**Feature**: Phase-II FastAPI Backend for Full-Stack Todo Web Application
**Date**: 2026-01-06
**Status**: Complete

This document defines the database schema, entity relationships, constraints, and indexes for the backend data layer.

---

## Entity Overview

The system has two primary entities:

1. **User**: Represents an authenticated user account
2. **Task**: Represents a todo item owned by a user

**Relationship**: One-to-Many (User → Tasks)
- One user owns zero or more tasks
- Each task belongs to exactly one user
- Cascade delete: Deleting a user deletes all their tasks

---

## Entity Specifications

### User Entity

**Purpose**: Stores user account information for authentication and identification.

**Table Name**: `users`

**Fields**:

| Field           | Type          | Constraints                           | Description                              |
|-----------------|---------------|---------------------------------------|------------------------------------------|
| id              | UUID          | PRIMARY KEY                           | Unique user identifier                   |
| email           | VARCHAR(255)  | UNIQUE, NOT NULL                      | User email for login (unique constraint) |
| hashed_password | VARCHAR(255)  | NOT NULL                              | bcrypt-hashed password (never plain text)|
| name            | VARCHAR(100)  | NOT NULL                              | User display name                        |
| created_at      | TIMESTAMP     | NOT NULL, DEFAULT CURRENT_TIMESTAMP   | Account creation timestamp               |
| updated_at      | TIMESTAMP     | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP | Last update timestamp |

**Indexes**:
- `PRIMARY KEY (id)`: Clustered index for primary key lookups
- `UNIQUE INDEX idx_users_email (email)`: Unique index for fast login queries and email uniqueness enforcement

**Validation Rules** (enforced at application layer via Pydantic):
- Email: Must be valid email format (RFC 5322)
- Password (pre-hashing): Minimum 8 characters (enforced before hashing)
- Name: Non-empty string, max 100 characters

**Security Notes**:
- Password stored as bcrypt hash (never plain text) per FR-003
- Email uniqueness enforced at database level (UNIQUE constraint) per FR-002
- ID uses UUID for non-guessable identifiers

**SQLModel Definition** (Python):
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255, nullable=False)
    hashed_password: str = Field(max_length=255, nullable=False)
    name: str = Field(max_length=100, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship (not a database column, SQLModel relationship)
    tasks: list["Task"] = Relationship(back_populates="owner", cascade_delete=True)
```

---

### Task Entity

**Purpose**: Stores todo items with ownership and completion tracking.

**Table Name**: `tasks`

**Fields**:

| Field        | Type          | Constraints                                        | Description                          |
|--------------|---------------|----------------------------------------------------|--------------------------------------|
| id           | UUID          | PRIMARY KEY                                        | Unique task identifier               |
| title        | VARCHAR(200)  | NOT NULL                                           | Task title (required, max 200 chars) |
| description  | TEXT          | NULLABLE                                           | Optional task description (max 2000) |
| is_completed | BOOLEAN       | NOT NULL, DEFAULT FALSE                            | Task completion status               |
| user_id      | UUID          | FOREIGN KEY → users(id), NOT NULL, ON DELETE CASCADE | Owner user reference                |
| created_at   | TIMESTAMP     | NOT NULL, DEFAULT CURRENT_TIMESTAMP                | Task creation timestamp              |
| updated_at   | TIMESTAMP     | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP | Last update timestamp      |

**Indexes**:
- `PRIMARY KEY (id)`: Clustered index for primary key lookups
- `INDEX idx_tasks_user_id (user_id)`: Fast filtering by owner (used in `GET /api/tasks`)
- `INDEX idx_tasks_user_created (user_id, created_at DESC)`: Composite index for paginated task lists sorted by creation date (newest first)

**Foreign Keys**:
- `user_id → users(id)`: Enforces referential integrity, cascade delete removes all tasks when user is deleted

**Validation Rules** (enforced at application layer via Pydantic):
- Title: Non-empty string, max 200 characters per FR-008
- Description: Optional string, max 2000 characters (edge case from spec)
- UTF-8 Support: Title and description accept unicode characters including emojis (edge case from spec)

**State Transitions**:
- `is_completed`: Can toggle between `false` (incomplete) ↔ `true` (complete) via PATCH endpoint per FR-013
- `updated_at`: Automatically updated on any field modification per FR-019

**SQLModel Definition** (Python):
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=2000, nullable=True)
    is_completed: bool = Field(default=False, nullable=False)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship (not a database column, SQLModel relationship)
    owner: User = Relationship(back_populates="tasks")
```

---

## Entity Relationship Diagram

```text
┌─────────────────────────────────────┐
│ users                                │
├─────────────────────────────────────┤
│ id (UUID) [PK]                       │
│ email (VARCHAR) [UNIQUE]             │
│ hashed_password (VARCHAR)            │
│ name (VARCHAR)                       │
│ created_at (TIMESTAMP)               │
│ updated_at (TIMESTAMP)               │
└──────────────┬──────────────────────┘
               │
               │ 1
               │
               │
               │ *
┌──────────────▼──────────────────────┐
│ tasks                                │
├─────────────────────────────────────┤
│ id (UUID) [PK]                       │
│ title (VARCHAR)                      │
│ description (TEXT)                   │
│ is_completed (BOOLEAN)               │
│ user_id (UUID) [FK → users.id]       │
│ created_at (TIMESTAMP)               │
│ updated_at (TIMESTAMP)               │
└─────────────────────────────────────┘

Legend:
[PK] = Primary Key
[FK] = Foreign Key
[UNIQUE] = Unique Constraint
1 = One
* = Many
```

**Relationship Description**:
- **One User** has **Many Tasks** (one-to-many)
- **One Task** belongs to **One User** (many-to-one)
- Foreign key `tasks.user_id` references `users.id`
- Cascade delete: When user is deleted, all their tasks are automatically deleted

---

## Index Strategy

### users Table

1. **Primary Key Index** (automatic)
   - **Index**: `PRIMARY KEY (id)`
   - **Type**: Clustered index (InnoDB/PostgreSQL default)
   - **Purpose**: Fast lookups by user ID (used in JWT token verification)

2. **Email Unique Index**
   - **Index**: `UNIQUE INDEX idx_users_email (email)`
   - **Type**: Unique B-tree index
   - **Purpose**:
     - Enforces email uniqueness per FR-002
     - Fast login queries (`SELECT * FROM users WHERE email = ?`)
     - Used in signup to check email existence

### tasks Table

1. **Primary Key Index** (automatic)
   - **Index**: `PRIMARY KEY (id)`
   - **Type**: Clustered index
   - **Purpose**: Fast lookups by task ID (used in GET/PUT/PATCH/DELETE endpoints)

2. **User ID Index**
   - **Index**: `INDEX idx_tasks_user_id (user_id)`
   - **Type**: B-tree index
   - **Purpose**: Fast filtering by owner (`SELECT * FROM tasks WHERE user_id = ?`)
   - **Used By**: All task endpoints to enforce user isolation per FR-010

3. **Composite Pagination Index**
   - **Index**: `INDEX idx_tasks_user_created (user_id, created_at DESC)`
   - **Type**: Composite B-tree index, descending on created_at
   - **Purpose**: Optimized paginated queries with sorting
   - **Query Pattern**: `SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?`
   - **Benefits**: Covers both filtering and sorting, prevents full table scan for pagination
   - **Performance**: Handles 1000+ tasks per user efficiently per SC-008

**Index Selection Rationale**:
- **No index on is_completed**: Most queries filter by user_id first, is_completed is selective but not frequently used alone
- **No full-text index on title/description**: Phase II doesn't include search functionality, defer to Phase III if needed
- **Composite index order**: user_id first (higher selectivity), created_at second (supports ORDER BY)

---

## Data Access Patterns

### Authentication Flows

1. **Signup** (FR-001)
   - Check email uniqueness: `SELECT id FROM users WHERE email = ?` (uses `idx_users_email`)
   - Insert user: `INSERT INTO users (...) VALUES (...)`

2. **Login** (FR-004)
   - Find user by email: `SELECT * FROM users WHERE email = ?` (uses `idx_users_email`)
   - Verify password hash (application layer)
   - Generate JWT with user_id

3. **Token Verification** (FR-006)
   - Decode JWT to extract user_id (application layer)
   - Optionally fetch user: `SELECT * FROM users WHERE id = ?` (uses primary key)

### Task Operations

1. **Create Task** (FR-007)
   - Insert: `INSERT INTO tasks (title, description, user_id, ...) VALUES (?, ?, ?, ...)`
   - Implicitly validates user_id foreign key

2. **List Tasks** (FR-009)
   - Paginated query: `SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?`
   - Uses `idx_tasks_user_created` composite index
   - Count total: `SELECT COUNT(*) FROM tasks WHERE user_id = ?` (uses `idx_tasks_user_id`)

3. **Get Single Task** (FR-011)
   - Query: `SELECT * FROM tasks WHERE id = ? AND user_id = ?`
   - Uses primary key + user_id verification for authorization

4. **Update Task** (FR-012)
   - Query: `UPDATE tasks SET title = ?, description = ?, updated_at = ? WHERE id = ? AND user_id = ?`
   - Uses primary key + user_id verification

5. **Toggle Completion** (FR-013)
   - Query: `UPDATE tasks SET is_completed = ?, updated_at = ? WHERE id = ? AND user_id = ?`
   - Uses primary key + user_id verification

6. **Delete Task** (FR-014)
   - Query: `DELETE FROM tasks WHERE id = ? AND user_id = ?`
   - Uses primary key + user_id verification

**Authorization Pattern**: All task operations include `WHERE user_id = ?` clause to enforce ownership per FR-015

---

## Database Constraints Summary

### Primary Keys
- `users.id` (UUID): Unique user identifier
- `tasks.id` (UUID): Unique task identifier

### Unique Constraints
- `users.email`: Prevents duplicate email addresses (FR-002)

### Foreign Keys
- `tasks.user_id → users.id`: Enforces referential integrity, cascade delete

### NOT NULL Constraints
- `users.email`, `users.hashed_password`, `users.name`: Required fields
- `tasks.title`, `tasks.user_id`: Required fields
- Timestamps (`created_at`, `updated_at`): Always populated

### Check Constraints (application-layer validation)
- Title length: max 200 characters
- Description length: max 2000 characters
- Email format: valid RFC 5322 email

---

## Migration Notes

**Phase II Strategy**: Use `SQLModel.metadata.create_all()` for initial schema creation (per research.md decision #7)

**Schema Creation**:
```python
from sqlmodel import create_engine, SQLModel
from backend.src.models import User, Task

# Create database engine
engine = create_engine(DATABASE_URL)

# Create all tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

**Phase III Migration Plan** (future):
- Introduce Alembic when recurring tasks and reminders require schema changes
- Initial migration will capture current User and Task schema
- Future migrations will add Phase III fields (due_date, recurrence_pattern, reminder_time, etc.)

---

## Data Integrity Rules

1. **Referential Integrity**
   - Foreign key `tasks.user_id → users.id` ensures every task has a valid owner
   - Cascade delete prevents orphaned tasks when user is deleted

2. **User Isolation**
   - All task queries include `WHERE user_id = ?` clause (enforced in service layer)
   - JWT tokens contain user_id, verified on every protected endpoint
   - No cross-user data access per FR-010, SC-003

3. **Timestamp Consistency**
   - `created_at` set once on creation, never updated
   - `updated_at` refreshed on every modification per FR-019
   - Both use UTC timestamps to avoid timezone issues

4. **Email Uniqueness**
   - Unique constraint on `users.email` enforced at database level
   - Case-sensitive comparison (PostgreSQL default)
   - Application layer can normalize email to lowercase before insert

5. **Password Security**
   - Only bcrypt hashes stored, never plain text per FR-003
   - Hash generation happens in service layer before database insert
   - Hashes are irreversible (one-way function)

---

## Performance Considerations

### Query Optimization

1. **Pagination Performance**
   - Composite index `idx_tasks_user_created` eliminates need for filesort
   - Handles 1000+ tasks per user with sub-100ms query time per SC-006
   - Offset limitations: High offsets (e.g. 10,000) may degrade, defer cursor pagination to Phase IV if needed

2. **Authentication Performance**
   - Email index makes login queries fast (O(log n) instead of O(n))
   - JWT verification happens in-memory (no database query) for most requests
   - User lookup only needed if user profile data required

3. **Write Performance**
   - UUID primary keys: Slightly slower inserts than auto-increment integers but better for distributed systems (Phase IV)
   - Indexes add write overhead but critical for read performance (read-heavy workload)
   - Timestamps use database default functions (minimal overhead)

### Scaling Strategy (Phase IV)

- **Horizontal Scaling**: Stateless JWT design enables multiple backend instances
- **Read Replicas**: Read-heavy workload (task lists) can use read replicas
- **Partitioning**: Future option - partition tasks table by user_id if single-user data exceeds millions of tasks
- **Caching**: Redis cache for user profiles, task lists (deferred to Phase IV)

---

## Edge Cases Handled

1. **Empty Task Title** (spec edge case)
   - Validation: Pydantic enforces `min_length=1` per FR-008
   - Database: `NOT NULL` constraint as secondary validation

2. **Excessive Character Lengths** (spec edge case)
   - Title: Pydantic enforces max_length=200
   - Description: Pydantic enforces max_length=2000
   - Database: VARCHAR(200) and TEXT types enforce hard limits

3. **Unicode/Emoji Support** (spec edge case)
   - PostgreSQL TEXT type with UTF-8 encoding supports all unicode
   - Pydantic passes unicode through without modification
   - No special handling needed

4. **Pagination Beyond Total** (spec edge case, SC-008)
   - Query: `SELECT ... LIMIT 10 OFFSET 1000` where only 50 tasks exist
   - Result: Empty array `[]` with pagination metadata showing total=50
   - No error, graceful handling

5. **Concurrent Updates** (spec edge case)
   - Last write wins (PostgreSQL default)
   - `updated_at` reflects latest modification time
   - Phase III could introduce optimistic locking if needed

6. **User Deletion**
   - Cascade delete removes all user's tasks automatically
   - No orphaned tasks remain
   - Frontend should confirm deletion with warning

---

## Schema Validation

**SQLModel Benefits**:
- Type hints provide compile-time validation (IDE support, mypy)
- Pydantic integration validates data at runtime (API request validation)
- Single source of truth for database schema and API models

**Validation Flow**:
1. **API Request** → Pydantic validates request body against model schema
2. **Service Layer** → Business logic operates on validated Pydantic models
3. **Database** → SQLModel writes validated data to PostgreSQL
4. **API Response** → Pydantic serializes database models to JSON

**Example**:
```python
# API endpoint
@router.post("/api/tasks", response_model=TaskResponse)
async def create_task(
    task_in: TaskCreate,  # Pydantic validates request
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Service layer
    task = Task(**task_in.dict(), user_id=current_user.id)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task  # Pydantic serializes response
```

---

## Phase 1.1 Completion Checklist

- [x] User entity specification complete with all fields and constraints
- [x] Task entity specification complete with all fields and constraints
- [x] Entity relationship diagram documented (one-to-many User → Tasks)
- [x] Index strategy documented with rationale
- [x] Data access patterns documented for all CRUD operations
- [x] Database constraints summarized
- [x] Migration strategy documented (SQLModel.metadata.create_all for Phase II)
- [x] Data integrity rules documented
- [x] Performance considerations documented
- [x] Edge cases mapped to database handling
- [x] SQLModel definitions provided for both entities

**Status**: ✅ Phase 1.1 Data Model Design Complete - Ready for Phase 1.2 (API Contracts)
