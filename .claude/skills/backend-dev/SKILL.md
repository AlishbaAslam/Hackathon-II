# Backend Development Skill (FastAPI + SQLModel) for Full-Stack Todo App

## Overview
This skill enables agents (Backend Engineer, Spec Architect, Auth Integrator) to develop, manage, and maintain backend services using FastAPI and SQLModel, aligned with spec-driven development (Specify → Plan → Tasks → Implement). It focuses on creating modular, chainable, and reusable backend logic, including API endpoint implementation, database interactions, JWT authentication integration, and proper error handling.

## Purpose
- Enable rapid backend development for the Hackathon II Phase 2 Full-Stack Todo Web Application
- Ensure all backend components follow spec-driven development methodology
- Maintain consistency in FastAPI + SQLModel patterns across the codebase
- Integrate JWT authentication with Better Auth for secure user isolation
- Follow monorepo structure with backend in `/backend` and specs in `/specs`

## Backend Structure Convention

### Directory Structure
```
/backend/
├── main.py                 # FastAPI application entry point
├── models.py               # SQLModel database models
├── db.py                   # Database connection and session management
├── auth.py                 # JWT authentication middleware and utilities
├── api/
│   ├── __init__.py
│   ├── deps.py             # Dependency injection utilities
│   └── v1/
│       ├── __init__.py
│       ├── auth.py         # Authentication endpoints
│       └── todos.py        # Todo-related endpoints
├── schemas/                # Pydantic request/response models
│   ├── __init__.py
│   ├── auth.py
│   └── todos.py
├── utils/                  # Utility functions
│   ├── __init__.py
│   └── security.py
└── config.py               # Configuration settings
```

## Development Workflow

### 1. Specification Reading
- Read feature specifications from `specs/[feature]/spec.md`
- Understand API requirements, data models, and authentication needs
- Identify database schema changes required
- Note error handling and validation requirements

### 2. Planning Implementation
- Create architecture plan in `specs/[feature]/plan.md`
- Design API endpoints with request/response schemas
- Define database models and relationships
- Plan authentication and authorization flows
- Consider performance and security implications

### 3. Task Generation
- Break down implementation into specific backend tasks
- Prioritize database schema changes before API endpoints
- Account for authentication integration in all endpoints
- Plan for proper error handling and validation

### 4. Implementation
- Follow FastAPI + SQLModel best practices
- Implement JWT authentication middleware
- Create proper request/response validation
- Ensure proper user isolation and data security

## FastAPI + SQLModel Patterns

### Database Model Pattern
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks (one-to-many)
    tasks: list["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user (many-to-one)
    user: User = Relationship(back_populates="tasks")
```

### API Endpoint Pattern
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.db import get_session
from backend.models import Task
from backend.schemas.todos import TaskCreate, TaskRead, TaskUpdate
from backend.api.deps import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskRead)
async def create_task(
    task: TaskCreate,
    current_user_id: int = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Ensure user can only create tasks for themselves
    db_task = Task(**task.dict(), user_id=current_user_id)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int,
    current_user_id: int = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    # Ensure user can only access their own tasks
    if task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )
    return task
```

### JWT Authentication Pattern
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os

security = HTTPBearer()

def verify_token(token: str) -> int:
    """Verify JWT token and return user_id"""
    try:
        payload = jwt.decode(
            token,
            os.getenv("JWT_SECRET_KEY"),
            algorithms=[os.getenv("JWT_ALGORITHM", "HS256")]
        )
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """Get current user ID from JWT token"""
    return verify_token(credentials.credentials)
```

## Error Handling Standards

### HTTP Status Codes
- `200`: Success for GET, PUT, PATCH
- `201`: Created for POST
- `204`: No Content for DELETE
- `400`: Bad Request for validation errors
- `401`: Unauthorized for authentication failures
- `403`: Forbidden for authorization failures
- `404`: Not Found for missing resources
- `422`: Unprocessable Entity for validation errors
- `500`: Internal Server Error for unexpected errors

### Error Response Format
```json
{
  "detail": "Human-readable error message",
  "error_code": "machine-readable-error-code",
  "timestamp": "2023-12-01T10:00:00Z"
}
```

## Database Operations Best Practices

### Session Management
- Always use dependency injection for database sessions
- Follow the pattern: `session: Session = Depends(get_session)`
- Sessions are automatically closed after the request
- Use transactions for operations that modify data

### Query Patterns
```python
# Get by ID
item = session.get(Model, id)

# List with filters
items = session.exec(
    select(Model).where(Model.field == value)
).all()

# Count with filters
count = session.exec(
    select(func.count(Model.id)).where(Model.field == value)
).one()

# Update
item.field = new_value
session.add(item)
session.commit()
session.refresh(item)

# Delete
session.delete(item)
session.commit()
```

## Authentication Integration

### User Isolation
- All endpoints that access user-specific data must verify user_id
- Use JWT middleware to extract user_id from tokens
- Validate that requested resources belong to the authenticated user
- Return 403 Forbidden for unauthorized access attempts

### Token Handling
- Use Better Auth for token generation and validation
- Store JWT secrets in environment variables
- Set appropriate token expiration times
- Handle token refresh if needed

## Testing Guidelines

### Unit Tests
- Test individual functions and utilities
- Mock database connections and external services
- Validate input/output behavior
- Test error handling paths

### Integration Tests
- Test API endpoints with real database
- Verify authentication flows
- Test user isolation between different users
- Validate data integrity constraints

## Validation Checks

### Before Creating API Endpoints
- [ ] Endpoint specification is clear and complete
- [ ] Request/response schemas are defined
- [ ] Authentication requirements are identified
- [ ] User isolation is properly planned
- [ ] Error handling is specified
- [ ] Database operations are validated

### Before Implementing Database Models
- [ ] Data model specifications are complete
- [ ] Relationships between models are defined
- [ ] Indexes for performance are planned
- [ ] Validation constraints are specified
- [ ] Migration strategy is considered

### Before Adding Authentication
- [ ] JWT configuration is properly set up
- [ ] Secret keys are stored securely
- [ ] Token expiration is configured
- [ ] User isolation is implemented
- [ ] Error responses follow standards

## Agent Integration Guidelines

### For Backend Engineer Agent
- Use this skill to implement API endpoints following FastAPI patterns
- Create SQLModel database models with proper relationships
- Implement JWT authentication middleware
- Follow error handling standards
- Ensure proper user isolation in all endpoints

### For Spec Architect Agent
- Define API endpoint specifications with proper request/response schemas
- Specify database models and relationships
- Plan authentication and authorization requirements
- Include error handling and validation requirements
- Consider performance implications of API designs

### For Auth Integrator Agent
- Implement JWT authentication flows using Better Auth
- Create middleware for token validation
- Ensure proper user isolation in all endpoints
- Handle token refresh and expiration
- Implement secure session management

## Quality Standards

### Code Quality
- Follow FastAPI and SQLModel best practices
- Use type hints for all function signatures
- Implement proper error handling
- Follow consistent naming conventions
- Include docstrings for complex functions

### Security Quality
- Validate all user inputs
- Implement proper authentication and authorization
- Ensure user data isolation
- Use parameterized queries to prevent SQL injection
- Implement rate limiting where appropriate

### Performance Quality
- Use database indexes appropriately
- Optimize queries for common access patterns
- Implement pagination for list endpoints
- Use eager loading to prevent N+1 queries
- Cache frequently accessed data when appropriate

## Integration with Spec-Driven Development

### Reading Specifications
- Parse feature specs to understand API requirements
- Identify database schema changes needed
- Note authentication and authorization requirements
- Extract validation and error handling requirements

### Generating Implementation Plans
- Create detailed architecture plans based on specs
- Design database models and relationships
- Plan API endpoint structure and authentication flows
- Consider integration points with frontend

### Task Generation
- Break down backend implementation into specific tasks
- Prioritize database schema changes
- Plan authentication integration
- Account for testing and validation

## Output Formats

### API Endpoint Output
- FastAPI route functions with proper type hints
- Request/response models using Pydantic
- Proper HTTP status codes and error handling
- Database session integration

### Database Model Output
- SQLModel classes with proper field definitions
- Relationships between models
- Indexes and constraints
- Validation rules and constraints

### Authentication Output
- JWT middleware functions
- Token validation utilities
- User identification functions
- Authorization verification functions

## Reusability Patterns

### Common Response Models
- Create reusable response models for common data structures
- Use generic response wrappers for consistency
- Implement pagination response models
- Create error response models

### Database Utilities
- Reusable database session dependency
- Common query functions
- Pagination utilities
- Database migration helpers

### Authentication Utilities
- JWT token creation and validation functions
- User identification utilities
- Permission checking functions
- Secure password handling utilities