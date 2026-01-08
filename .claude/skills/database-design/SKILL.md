# Database Design Skill (Neon PostgreSQL) for Full-Stack Todo App

## Overview
This skill enables agents (Database Designer, Backend Engineer, Spec Architect) to design, manage, and optimize database schemas using Neon PostgreSQL. It focuses on creating modular, reusable, and spec-driven database designs aligned with project specifications, including tables, relationships, indexes, constraints, and foreign key integrations. The skill covers multi-user isolation, integration with backend models (SQLModel), and best practices for performance, security, and maintainability.

## Purpose
- Enable rapid database schema design for the Hackathon II Phase 2 Full-Stack Todo Web Application
- Ensure all database designs follow spec-driven development methodology
- Maintain consistency in Neon PostgreSQL patterns across the schema
- Implement proper multi-user isolation and security measures
- Follow best practices for performance and maintainability
- Integrate seamlessly with SQLModel backend models

## Database Structure Convention

### Directory Structure
```
/backend/
├── models.py               # SQLModel database models
├── db.py                   # Database connection and session management
└── alembic/
    ├── versions/           # Migration files
    └── env.py              # Alembic environment
```

### Schema Organization
- Use a single schema (public) for simplicity
- Follow naming conventions: snake_case for tables and columns
- Prefix tables with domain context (e.g., `user_`, `task_`, `auth_`)
- Use consistent suffixes for special columns (e.g., `_at` for timestamps, `_id` for foreign keys)

## Development Workflow

### 1. Specification Reading
- Read feature specifications from `specs/[feature]/spec.md`
- Understand data requirements, relationships, and constraints
- Identify multi-user isolation requirements
- Note performance and security considerations
- Extract indexing requirements for optimal queries

### 2. Database Design Planning
- Create database schema plan in `specs/[feature]/plan.md`
- Design table structures with proper data types
- Define relationships and foreign key constraints
- Plan indexes for query optimization
- Consider data integrity and validation constraints

### 3. Task Generation
- Break down database implementation into specific tasks
- Prioritize table creation before relationships
- Plan migration strategies for existing data
- Account for security and performance requirements

### 4. Implementation
- Follow SQLModel + Neon PostgreSQL best practices
- Implement proper multi-user isolation
- Create efficient indexes for common queries
- Ensure data validation and integrity constraints

## SQLModel Integration Patterns

### Basic Model Pattern
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from pydantic import EmailStr

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks (one-to-many)
    tasks: list["Task"] = Relationship(back_populates="user", cascade_delete=True)

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium", max_length=20)  # low, medium, high
    due_date: Optional[datetime] = Field(default=None)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user (many-to-one)
    user: User = Relationship(back_populates="tasks")
```

### Advanced Model Pattern with Indexes and Constraints
```python
from sqlmodel import SQLModel, Field, Relationship, create_engine
from typing import Optional
from datetime import datetime
from sqlalchemy import Index, CheckConstraint

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Core fields
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

    # Enum-like field with constraints
    priority: str = Field(
        default="medium",
        max_length=20,
        sa_column_kwargs={
            "server_default": "medium"
        }
    )

    # Date fields
    due_date: Optional[datetime] = Field(default=None)
    user_id: int = Field(foreign_key="users.id", index=True)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="tasks")

    # Table-level constraints
    __table_args__ = (
        CheckConstraint("priority IN ('low', 'medium', 'high')", name="valid_priority"),
        Index("idx_tasks_user_completed", "user_id", "completed"),
        Index("idx_tasks_due_date", "due_date"),
        Index("idx_tasks_created_at", "created_at"),
    )
```

## Neon PostgreSQL Best Practices

### Connection Management
- Use connection pooling for optimal performance
- Configure appropriate timeout values
- Implement retry logic for transient failures
- Monitor connection usage and performance

### Data Types
- Use `UUID` for primary keys if high security is needed
- Use `TIMESTAMPTZ` for timezone-aware timestamps
- Use `TEXT` for variable-length strings without length limits
- Use appropriate numeric types (`INTEGER`, `BIGINT`, `DECIMAL`)
- Use `JSONB` for flexible, semi-structured data

### Indexing Strategy
```sql
-- Primary indexes (automatically created by SQLModel)
-- Primary keys and foreign keys should be indexed

-- Composite indexes for common query patterns
CREATE INDEX idx_tasks_user_status_priority ON tasks (user_id, completed, priority);

-- Partial indexes for common filtered queries
CREATE INDEX idx_tasks_active_user ON tasks (user_id) WHERE completed = false;

-- Expression indexes for computed values
CREATE INDEX idx_tasks_due_week ON tasks (user_id) WHERE due_date >= current_date AND due_date < current_date + 7;
```

### Partitioning (for large datasets)
- Use time-based partitioning for historical data
- Partition by user_id for multi-tenant scenarios
- Consider range or hash partitioning based on access patterns

## Multi-User Isolation Patterns

### Row-Level Security (RLS)
```sql
-- Enable RLS on sensitive tables
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

-- Create policy to restrict access to user's own data
CREATE POLICY user_tasks_policy ON tasks
FOR ALL
TO app_user
USING (user_id = current_setting('app.current_user_id')::int);
```

### Application-Level Isolation
- Always include user_id in queries for user-specific data
- Validate user_id matches authenticated user in all endpoints
- Use parameterized queries to prevent injection
- Implement proper authorization checks

### Example with SQLModel
```python
# Safe query pattern - always filter by user_id
def get_user_tasks(session: Session, user_id: int, completed: Optional[bool] = None):
    query = select(Task).where(Task.user_id == user_id)
    if completed is not None:
        query = query.where(Task.completed == completed)
    return session.exec(query).all()

# Unsafe pattern - could expose other users' data
# def get_tasks_by_status(session: Session, completed: bool):
#     return session.exec(select(Task).where(Task.completed == completed)).all()
```

## Security Considerations

### Data Encryption
- Use Neon's built-in encryption at rest
- Encrypt sensitive data in transit with SSL
- Consider application-level encryption for highly sensitive fields
- Never store plaintext passwords (always hash with bcrypt or similar)

### Access Control
- Implement role-based access control (RBAC)
- Use least-privilege principle for database users
- Implement proper authentication and authorization
- Log sensitive operations for audit trails

### SQL Injection Prevention
- Always use parameterized queries (SQLModel handles this automatically)
- Validate and sanitize user inputs
- Use ORM methods instead of raw SQL when possible
- Implement proper input validation at API level

## Performance Optimization

### Query Optimization
- Use EXPLAIN ANALYZE to understand query performance
- Create appropriate indexes for common access patterns
- Avoid N+1 query problems with proper eager loading
- Use LIMIT and OFFSET for pagination

### Connection Optimization
- Configure appropriate connection pool size
- Use connection timeouts to handle dead connections
- Monitor query execution times
- Implement caching for frequently accessed data

### Schema Optimization
- Normalize data to reduce redundancy
- Denormalize strategically for read performance
- Use appropriate data types to minimize storage
- Consider read replicas for read-heavy workloads

## Migration Strategy

### Alembic Integration
```python
# Example migration file
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade() -> None:
    # Create new table
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("completed", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("priority", sa.String(length=20), nullable=False, server_default="medium"),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint("priority IN ('low', 'medium', 'high')", name="valid_priority")
    )

    # Create indexes
    op.create_index("idx_tasks_user_completed", "tasks", ["user_id", "completed"])
    op.create_index("idx_tasks_due_date", "tasks", ["due_date"])

def downgrade() -> None:
    op.drop_index("idx_tasks_due_date")
    op.drop_index("idx_tasks_user_completed")
    op.drop_table("tasks")
```

### Zero-Downtime Migration Patterns
- Add new columns with default values
- Add indexes concurrently when possible
- Use transaction blocks appropriately
- Test migrations on staging before production

## Validation Checks

### Before Creating Tables
- [ ] Data model specifications are complete and clear
- [ ] Relationships between tables are properly defined
- [ ] Primary and foreign key constraints are specified
- [ ] Indexes for performance are planned
- [ ] Multi-user isolation is properly considered
- [ ] Security and privacy requirements are addressed

### Before Adding Indexes
- [ ] Query patterns are analyzed for optimal indexing
- [ ] Indexes don't create unnecessary overhead
- [ ] Composite indexes follow proper column order
- [ ] Partial indexes are appropriate for the use case
- [ ] Maintenance impact is considered

### Before Implementing Constraints
- [ ] Business rules are properly represented
- [ ] Constraints don't conflict with application logic
- [ ] Error handling for constraint violations is planned
- [ ] Migration strategy accounts for existing data
- [ ] Performance impact is evaluated

## Agent Integration Guidelines

### For Database Designer Agent
- Use this skill to design comprehensive database schemas
- Create proper relationships and constraints
- Plan indexing strategies for performance
- Ensure multi-user isolation in schema design
- Follow Neon PostgreSQL best practices

### For Backend Engineer Agent
- Implement SQLModel models that align with database design
- Create proper database session management
- Implement query optimization patterns
- Ensure proper user isolation in data access
- Handle database errors gracefully

### For Spec Architect Agent
- Define database requirements in specifications
- Plan data relationships and constraints
- Consider performance and security implications
- Account for multi-user isolation requirements
- Specify migration and deployment strategies

## Quality Standards

### Schema Quality
- Follow consistent naming conventions
- Use appropriate data types for each field
- Implement proper normalization
- Include necessary constraints for data integrity
- Plan for future extensibility

### Performance Quality
- Create indexes for common query patterns
- Avoid unnecessary columns or tables
- Use appropriate data types to minimize storage
- Consider partitioning for large datasets
- Optimize queries for expected load patterns

### Security Quality
- Implement proper user isolation
- Use parameterized queries to prevent injection
- Apply appropriate access controls
- Encrypt sensitive data appropriately
- Follow least-privilege principles

## Integration with Spec-Driven Development

### Reading Specifications
- Parse feature specs to understand data requirements
- Identify relationships between different data entities
- Note multi-user isolation requirements
- Extract performance and security requirements
- Consider data validation and constraint needs

### Generating Implementation Plans
- Create detailed database schema plans based on specs
- Design table structures with proper relationships
- Plan indexing strategy for optimal performance
- Consider migration strategies for existing data
- Account for security and privacy requirements

### Task Generation
- Break down database implementation into specific tasks
- Prioritize critical path database changes
- Plan for backward compatibility if needed
- Account for testing and validation of database changes
- Consider deployment and rollback strategies

## Output Formats

### Database Model Output
- SQLModel classes with proper field definitions
- Relationships between models with proper constraints
- Indexes and constraints for performance and integrity
- Validation rules and constraints

### Migration Output
- Alembic migration files with proper upgrade/downgrade functions
- SQL commands for schema changes
- Data migration scripts if needed
- Rollback procedures for failed migrations

### Performance Output
- Index creation statements
- Query optimization recommendations
- Database configuration settings
- Monitoring and alerting specifications

## Reusability Patterns

### Common Field Patterns
- Created/updated timestamp fields
- Soft delete patterns with deleted_at
- Tenant/user isolation fields
- Audit trail fields (created_by, updated_by)

### Index Patterns
- Foreign key indexes
- Common query pattern indexes
- Partial indexes for filtered queries
- Composite indexes for multi-column queries

### Constraint Patterns
- Check constraints for enum-like fields
- Unique constraints for business rules
- Foreign key constraints for referential integrity
- Not-null constraints for required fields

## Testing Guidelines

### Unit Tests
- Test individual model validation
- Verify relationship constraints
- Validate custom validators
- Test computed properties

### Integration Tests
- Test database queries with real data
- Verify foreign key constraints
- Test transaction behavior
- Validate multi-user isolation
- Performance testing for critical queries