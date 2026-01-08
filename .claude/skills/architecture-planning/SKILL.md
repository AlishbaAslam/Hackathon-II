# Architecture Planning Skill for Full-Stack Todo App

## Overview
This skill enables agents (Architecture Planner, Spec Architect, Frontend UI, Backend Engineer) to design, document, and validate the high-level system and component architecture for the full-stack Todo application. It focuses on creating modular, reusable, and spec-driven architecture planning workflows, including component hierarchies, service interactions, database integration, API design, and frontend-backend communication. All architectural diagrams and plans align with project specs, monorepo structure, and multi-user feature requirements.

## Purpose
- Enable comprehensive architecture planning for the Hackathon II Phase 2 Full-Stack Todo Web Application
- Ensure all architectural decisions follow spec-driven development methodology
- Maintain consistency in system design patterns across the codebase
- Document component hierarchies and service interactions
- Plan database integration and API design strategies
- Design frontend-backend communication patterns
- Align architecture with multi-user feature requirements

## Architecture Convention

### Directory Structure
```
/specs/
├── architecture.md           # High-level architecture documentation
├── [feature]/
│   ├── spec.md              # Feature specifications
│   ├── plan.md              # Implementation plans
│   └── tasks.md             # Task breakdown
└── checklists/
    ├── architecture.md      # Architecture review checklist

/backend/
├── main.py                  # FastAPI application entry point
├── models.py                # SQLModel database models
├── db.py                    # Database connection and session management
├── auth.py                  # JWT authentication middleware and utilities
├── api/
│   ├── __init__.py
│   ├── deps.py              # Dependency injection utilities
│   └── v1/
│       ├── __init__.py
│       ├── auth.py          # Authentication endpoints
│       └── todos.py         # Todo-related endpoints
├── schemas/                 # Pydantic request/response models
├── utils/                   # Utility functions
└── config.py                # Configuration settings

/frontend/
├── pages/                   # Next.js pages
├── components/              # Reusable UI components
├── lib/                     # Utility functions and API clients
├── styles/                  # Global styles and Tailwind configuration
├── public/                  # Static assets
└── middleware.js            # Next.js middleware (if needed)

/tests/
├── integration/             # Integration tests
├── unit/                    # Unit tests
└── performance/             # Performance tests
```

### Architecture Layers
- **Presentation Layer**: Next.js frontend with responsive UI components
- **API Layer**: FastAPI RESTful endpoints with proper authentication
- **Business Logic Layer**: Service layer with business rules and validation
- **Data Access Layer**: SQLModel ORM with database operations
- **Data Layer**: Neon PostgreSQL database with proper indexing

## Development Workflow

### 1. Specification Reading
- Read feature specifications from `specs/[feature]/spec.md`
- Understand user stories and acceptance criteria
- Identify architectural implications and constraints
- Note performance and security requirements
- Extract integration and communication needs

### 2. Architecture Planning
- Create high-level architecture plan in `specs/architecture.md`
- Design component hierarchies and relationships
- Plan service interactions and data flow
- Consider scalability and maintainability
- Account for security and performance requirements

### 3. Component Design
- Break down architecture into specific components
- Design API endpoints and request/response schemas
- Plan database models and relationships
- Consider frontend component structure
- Account for authentication and authorization flows

### 4. Documentation
- Document architectural decisions and trade-offs
- Create component diagrams and interaction flows
- Specify API contracts and data models
- Plan for future extensibility and maintenance

## Architecture Design Patterns

### Component Hierarchy Pattern
```
Frontend Components:
├── App
│   ├── Layout
│   │   ├── Header
│   │   │   ├── Navigation
│   │   │   └── UserMenu
│   │   ├── Main
│   │   │   ├── Sidebar
│   │   │   └── Content
│   │   └── Footer
│   └── Pages
│       ├── Auth
│       │   ├── Login
│       │   ├── Signup
│       │   └── ForgotPassword
│       └── Dashboard
│           ├── TaskList
│           │   ├── TaskItem
│           │   │   ├── TaskForm
│           │   │   └── TaskActions
│           │   └── TaskFilters
│           └── UserProfile
└── Shared
    ├── Button
    ├── Input
    ├── Modal
    └── LoadingSpinner
```

### Service Interaction Pattern
```
Frontend → API Client → HTTP Request → FastAPI Backend → Business Logic → Data Access → Database
```

### API Design Pattern
```python
# Backend API Structure
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db import get_session
from backend.auth import get_current_user

# Versioned API router
api_router = APIRouter(prefix="/api/v1")

# Authentication endpoints
auth_router = APIRouter(prefix="/auth", tags=["authentication"])
api_router.include_router(auth_router)

# Todo endpoints
todo_router = APIRouter(prefix="/todos", tags=["todos"])
api_router.include_router(todo_router)

# Dependencies
def get_db_session():
    with SessionLocal() as session:
        yield session

def get_current_active_user(user_id: int = Depends(get_current_user)):
    return user_id
```

### Database Integration Pattern
```python
# Database Model with Relationships
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # One-to-many relationship with tasks
    tasks: list["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Many-to-one relationship with user
    user: User = Relationship(back_populates="tasks")
```

### Frontend-Backend Communication Pattern
```javascript
// API Client Pattern
class ApiClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        ...this.defaultHeaders,
        ...options.headers,
      },
      ...options,
    };

    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(url, config);

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status}`);
    }

    return response.json();
  }

  // Specific API methods
  async getTasks() {
    return this.request('/api/v1/tasks');
  }

  async createTask(taskData) {
    return this.request('/api/v1/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }
}

export const apiClient = new ApiClient(process.env.NEXT_PUBLIC_API_BASE_URL);
```

## Architecture Decision Records (ADRs)

### API Versioning Strategy
- **Decision**: Use URL versioning (e.g., `/api/v1/`) for API endpoints
- **Rationale**: Clear and explicit versioning that's easy to understand
- **Alternatives**: Header-based versioning, query parameter versioning
- **Consequences**: URLs contain version information, easier debugging

### Authentication Strategy
- **Decision**: JWT tokens with Better Auth integration
- **Rationale**: Stateless authentication, good for microservices
- **Alternatives**: Session-based authentication, OAuth
- **Consequences**: Token management complexity, need for refresh tokens

### Database Strategy
- **Decision**: Neon PostgreSQL with SQLModel ORM
- **Rationale**: Serverless PostgreSQL, good performance, Python integration
- **Alternatives**: SQLite, MongoDB, PostgreSQL with SQLAlchemy
- **Consequences**: Cloud dependency, need for connection pooling

## System Architecture Diagrams

### High-Level Architecture
```
┌─────────────────┐    HTTP/HTTPS     ┌──────────────────┐
│   Frontend      │ ◄──────────────►  │   Backend API    │
│   (Next.js)     │                   │   (FastAPI)      │
└─────────────────┘                   └──────────────────┘
                                              │
                                              ▼
                                    ┌──────────────────┐
                                    │  Database Layer  │
                                    │ (Neon PostgreSQL)│
                                    └──────────────────┘
```

### Component Interaction Flow
```
User Action → Frontend Component → API Call → Authentication → Business Logic → Database → Response → Frontend Update
```

### Multi-User Data Isolation
```
User A Request → JWT Verification → User A Data Access → User A Data Returned
User B Request → JWT Verification → User B Data Access → User B Data Returned
```

## Validation Checks

### Before Creating Architecture Plans
- [ ] Feature specifications are complete and clear
- [ ] User stories and acceptance criteria are understood
- [ ] Performance requirements are identified
- [ ] Security requirements are noted
- [ ] Integration points are identified
- [ ] Scalability requirements are considered

### Before Designing Components
- [ ] Component responsibilities are clearly defined
- [ ] Component interactions follow single responsibility principle
- [ ] Data flow between components is well-defined
- [ ] Error handling is planned for each component
- [ ] Security boundaries are established

### Before Finalizing Architecture
- [ ] Architecture aligns with project specifications
- [ ] Multi-user isolation is properly designed
- [ ] Performance requirements are addressed
- [ ] Security considerations are implemented
- [ ] Scalability patterns are planned
- [ ] Testing strategies are considered

## Agent Integration Guidelines

### For Architecture Planner Agent
- Use this skill to design comprehensive system architecture
- Create component hierarchies and interaction flows
- Plan service interactions and data management
- Consider scalability and maintainability
- Document architectural decisions and trade-offs

### For Spec Architect Agent
- Define architectural requirements in specifications
- Plan component structure and relationships
- Consider performance and security implications
- Account for multi-user requirements
- Specify API contracts and data models

### For Frontend UI Agent
- Design component architecture following system patterns
- Plan frontend-backend communication flows
- Consider responsive design and accessibility
- Implement proper state management
- Follow security best practices for frontend

### For Backend Engineer Agent
- Implement API design following architectural patterns
- Create proper database integration
- Implement authentication and authorization flows
- Follow security best practices
- Plan for performance and scalability

## Quality Standards

### Architecture Quality
- Follow consistent naming conventions
- Maintain clear separation of concerns
- Implement proper component boundaries
- Use appropriate design patterns
- Document architectural decisions

### Scalability Quality
- Design for horizontal scaling
- Consider database performance and indexing
- Plan for load distribution
- Implement caching strategies
- Consider microservice patterns where appropriate

### Security Quality
- Implement proper authentication and authorization
- Design secure data access patterns
- Consider multi-user isolation
- Plan for data encryption and privacy
- Follow security best practices

### Performance Quality
- Design efficient data access patterns
- Plan for proper indexing strategies
- Consider caching and optimization
- Design efficient API endpoints
- Plan for monitoring and observability

## Integration with Spec-Driven Development

### Reading Specifications
- Parse feature specs to understand architectural implications
- Identify performance and security requirements
- Note integration and communication needs
- Extract multi-user and isolation requirements
- Consider scalability and maintainability needs

### Generating Architecture Plans
- Create detailed architecture plans based on specs
- Design component hierarchies and relationships
- Plan service interactions and data flow
- Consider security and performance implications
- Account for future extensibility requirements

### Component Design
- Break down architecture into specific components
- Design API endpoints following spec requirements
- Plan database models with proper relationships
- Consider frontend component structure
- Account for authentication and authorization flows

## Output Formats

### Architecture Documentation Output
- High-level architecture diagrams
- Component hierarchy documentation
- API contract specifications
- Database schema documentation
- Service interaction flows

### Design Document Output
- Architecture decision records (ADRs)
- Component design specifications
- Data flow diagrams
- Security architecture plans
- Performance optimization strategies

### Implementation Plan Output
- Component implementation order
- Dependency relationships
- Integration points documentation
- Testing strategy recommendations
- Deployment architecture plans

## Reusability Patterns

### Common Architecture Components
- Authentication and authorization patterns
- API versioning and routing patterns
- Database connection and session management
- Error handling and logging patterns
- Configuration and environment management

### Design Patterns
- Repository pattern for data access
- Service layer for business logic
- Dependency injection for component management
- Middleware for cross-cutting concerns
- Event-driven patterns for communication

### Security Patterns
- JWT token-based authentication
- Role-based access control
- Input validation and sanitization
- Secure session management
- Data encryption and privacy patterns

## Architecture Review Checklist

### Design Quality
- [ ] Clear separation of concerns
- [ ] Proper component boundaries
- [ ] Consistent naming conventions
- [ ] Appropriate design patterns
- [ ] Well-documented decisions

### Security Considerations
- [ ] Proper authentication and authorization
- [ ] Multi-user data isolation
- [ ] Input validation and sanitization
- [ ] Secure communication protocols
- [ ] Data privacy and encryption

### Performance Considerations
- [ ] Efficient database queries
- [ ] Proper indexing strategies
- [ ] Caching mechanisms
- [ ] API response optimization
- [ ] Resource usage optimization

### Scalability Considerations
- [ ] Horizontal scaling capabilities
- [ ] Load distribution patterns
- [ ] Database connection management
- [ ] Caching strategies
- [ ] Monitoring and observability

### Maintainability Considerations
- [ ] Clear documentation
- [ ] Testable components
- [ ] Modular design
- [ ] Proper error handling
- [ ] Logging and monitoring

## Architecture Planning Tools

### Diagramming Tools
- Use Mermaid diagrams for architecture visualization
- Create component interaction flows
- Document data flow patterns
- Visualize service dependencies
- Plan deployment architecture

### Documentation Standards
- Follow consistent documentation format
- Include architectural decision records
- Document component responsibilities
- Specify interface contracts
- Plan for future modifications