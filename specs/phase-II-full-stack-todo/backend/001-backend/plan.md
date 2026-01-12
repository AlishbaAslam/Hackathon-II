# Implementation Plan: Phase-II FastAPI Backend for Full-Stack Todo Web Application

**Branch**: `001-backend` | **Date**: 2026-01-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/backend/001-backend/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature implements a RESTful FastAPI backend for the Phase-II full-stack todo web application. The backend provides secure authentication via JWT tokens, complete CRUD operations for user-owned tasks, and user isolation to ensure data security. The implementation uses FastAPI for high-performance async APIs, SQLModel for type-safe database operations with PostgreSQL (Neon DB), and follows a modular architecture with clear separation of concerns between routers, services, models, and core utilities. The system is designed for stateless horizontal scaling and includes comprehensive API documentation via auto-generated OpenAPI/Swagger endpoints.

## Technical Context

**Language/Version**: Python 3.13+ (matches Phase I CLI, constitution Technical Standards)
**Primary Dependencies**: FastAPI 0.115+, SQLModel 0.0.24+, Pydantic 2.0+, python-jose[cryptography] (JWT), passlib[bcrypt] (password hashing), psycopg2-binary (PostgreSQL driver), uvicorn (ASGI server), python-dotenv (environment variables)
**Storage**: PostgreSQL 15+ via Neon DB (serverless PostgreSQL, constitution Deployment Standards), SQLModel ORM for type-safe queries
**Testing**: pytest 8.0+, pytest-asyncio (async test support), httpx (async HTTP client for API tests), pytest-cov (coverage reporting)
**Target Platform**: Linux server (production), cross-platform development (Windows/macOS/Linux via Docker), containerized deployment (future Phase IV)
**Project Type**: Web backend API (determines backend/ source structure with /src, /tests)
**Performance Goals**: <500ms response time for single-user operations (SC-006), 100 concurrent requests without degradation (SC-005), <2s user registration (SC-001), <1s task operations (SC-002)
**Constraints**: Stateless design (no server-side sessions, JWT-only authentication), environment variable configuration (no hardcoded secrets), CORS-enabled for frontend integration, PostgreSQL-compatible only (Neon DB requirement), user-scoped routing with ownership verification (user_id from JWT token must match user_id in path parameter for all task operations)
**Scale/Scope**: Multi-user system (10-1000 users initially), 5 core endpoints + 2 auth endpoints + 2 documentation endpoints (10+ total per SC-004), support 1000+ tasks per user (SC-008), designed for horizontal scaling in Phase IV

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Constitution principles that must be verified:

**✓ Spec-Driven Development (SDD)**: This backend feature originates from approved specification at `/specs/backend/001-backend/spec.md`. Implementation will follow Spec-Kit Plus methodology with plan → tasks → implementation workflow. No code will be written without corresponding specification approval.

**✓ Progressive Evolution**: This feature fits within Phase II (Web Application) scope as defined in constitution section "Project Scope Governance". Phase I (CLI) is completed and frozen. This backend enables Phase II web application and prepares foundation for Phase III (advanced features) and Phase IV (cloud native deployment). Sequential progression is maintained.

**✓ Cloud Native Architecture**: Backend designed for stateless operation using JWT tokens (no server-side sessions), enabling horizontal scaling. Services are containerizable for future Phase IV Kubernetes deployment. PostgreSQL via Neon DB provides serverless, scalable database layer. Architecture supports distributed operation and fault tolerance.

**⚠ AI Agent Integration**: Phase II focus is on backend infrastructure. Natural language processing and AI-powered features are deferred to Phase III as per constitution phasing. This backend provides the data layer and APIs that Phase III AI agents will consume. Current phase establishes secure data access patterns required for AI integration.

**✓ Security & Authentication**: Implements JWT-based authentication with user isolation. All protected endpoints verify tokens and extract user_id for authorization. Passwords are cryptographically hashed using bcrypt. No hardcoded secrets - all credentials loaded from environment variables. User data isolation enforced at database query level.

**⚠ Event-Driven Design**: Phase II focuses on synchronous RESTful APIs. Event-driven patterns for reminders and recurring tasks are deferred to Phase III as per constitution. Current architecture uses simple request-response pattern suitable for basic CRUD operations. Phase III will introduce event sourcing and pub/sub patterns.

**✓ Correctness and Predictability**: Comprehensive error handling with consistent JSON error responses. Input validation using Pydantic models. Edge cases documented in spec (token expiration, concurrent updates, connection loss, pagination beyond bounds). No hidden state - stateless JWT design ensures predictable behavior.

**✓ Maintainability and Extensibility**: Clean modular architecture with separation of concerns: routers (HTTP layer), services (business logic), models (data layer), core utilities (auth, database). Type-safe code using Python type hints and Pydantic validation. Extensible for Phase III features (recurring tasks, reminders, AI integration).

**✓ AI-Assisted Development**: Implementation uses Claude Code following Spec-Kit Plus methodology. All AI-generated code will be human-verified against specification and constitution principles.

**Constitution Gate Status**: ✅ PASS (2 deferrals justified by phase sequencing per constitution)

## Project Structure

### Documentation (this feature)

```text
specs/backend/001-backend/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output: Technology decisions and best practices
├── data-model.md        # Phase 1 output: Entity schemas and relationships
├── quickstart.md        # Phase 1 output: Developer setup and API usage guide
├── contracts/           # Phase 1 output: OpenAPI/JSON schemas
│   ├── auth.openapi.yaml
│   ├── tasks.openapi.yaml
│   └── errors.schema.json
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point, CORS, middleware
│   ├── config.py            # Environment variable loading, app configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # SQLModel User entity with relationships
│   │   └── task.py          # SQLModel Task entity with owner foreign key
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py          # POST /api/auth/signup, /api/auth/login
│   │   └── tasks.py         # CRUD endpoints for tasks
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py  # Password hashing, JWT generation/verification
│   │   └── task_service.py  # Business logic for task operations
│   └── core/
│       ├── __init__.py
│       ├── database.py      # SQLModel engine, session management
│       ├── dependencies.py  # FastAPI dependency injection (get_db, get_current_user)
│       └── security.py      # JWT utilities, password utilities
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures (test client, test database)
│   ├── test_auth.py         # Authentication endpoint tests
│   ├── test_tasks.py        # Task CRUD endpoint tests
│   └── test_security.py     # JWT and password hashing unit tests
├── .env.example             # Template for environment variables
├── pyproject.toml           # Python dependencies (uv package manager)
├── uv.lock                  # Locked dependency versions
└── README.md                # Setup instructions, API overview

frontend/                    # Future Phase II frontend (Next.js)
└── [to be implemented]
```

**Structure Decision**: Web application structure (Option 2) selected. Backend uses modular layered architecture following FastAPI best practices: routers for HTTP endpoints, services for business logic, models for database entities, core for shared utilities. The architecture implements user-scoped routing with ownership verification: all task endpoints require user_id in the path parameter which must match the user_id in the authenticated JWT token. Frontend directory reserved for future Next.js implementation. Tests colocated with backend for rapid feedback during development.

## Complexity Tracking

**No constitution violations requiring justification.** All architectural decisions align with Phase II scope and constitution principles.

---

## Phase 0: Research & Decision Documentation

**Objective**: Resolve all NEEDS CLARIFICATION items from Technical Context and document architectural decisions with rationale.

### Research Areas

1. **Database ORM Selection**: SQLModel vs SQLAlchemy vs raw SQL
   - Need to determine: Type safety, async support, migration tooling, FastAPI integration
   - Constitution requirement: Maintainability and clean code

2. **JWT Library Selection**: python-jose vs PyJWT vs authlib
   - Need to determine: Security features, algorithm support, ease of use
   - Constitution requirement: Security & Authentication

3. **Password Hashing Strategy**: bcrypt vs argon2 vs scrypt
   - Need to determine: Security level, performance, industry standards
   - Constitution requirement: Security & Authentication

4. **Error Handling Pattern**: Custom exception handlers vs default FastAPI
   - Need to determine: Consistency, debugging support, API contract
   - Spec requirement: FR-022 (consistent JSON error responses)

5. **API Versioning Strategy**: URL-based (/api/v1) vs header-based vs no versioning
   - Need to determine: Future compatibility, migration strategy
   - Constitution requirement: Maintainability and Extensibility

6. **Pagination Approach**: Limit-offset vs cursor-based
   - Need to determine: Performance for 1000+ tasks, complexity, frontend UX
   - Spec requirement: FR-009, SC-008

7. **Database Migration Tool**: Alembic vs manual migrations vs no migrations (Phase II)
   - Need to determine: Schema evolution strategy, Phase II vs Phase III needs
   - Constitution requirement: Progressive Evolution

8. **Test Coverage Level**: Critical endpoints only vs full coverage
   - Need to determine: Development speed vs robustness, Phase II priorities
   - Constitution requirement: Correctness and Predictability

9. **Secure Routing Best Practices**: User-scoped path verification vs token-only verification
   - Need to determine: Double verification approach (path + token check), security implications, performance impact
   - Constitution requirement: Security & Authentication

### Research Methodology

- **Concurrent research approach**: Investigate best practices while documenting decisions in `research.md`
- **Decision format**: For each area, document Decision, Rationale, Alternatives Considered
- **Sources**: FastAPI documentation, SQLModel documentation, security best practices (OWASP), PostgreSQL guides

**Output**: `specs/backend/001-backend/research.md` with all 8 research areas documented

---

## Phase 1: Design Artifacts

**Prerequisites**: `research.md` complete with all decisions documented

### 1.1 Data Model Design

**Objective**: Extract entities from feature spec and design database schema with relationships, constraints, and indexes.

**Entities** (from spec Key Entities section):

1. **User Entity**
   - Primary key: id (UUID or integer)
   - Unique constraint: email (used for login)
   - Fields: email, hashed_password, name, created_at, updated_at
   - Relationships: One-to-many with Task (user owns many tasks)
   - Indexes: Unique index on email for fast login lookup

2. **Task Entity**
   - Primary key: id (UUID or integer)
   - Foreign key: user_id (references User.id, cascade delete)
   - Fields: title (max 200 chars), description (max 2000 chars), is_completed (boolean), created_at, updated_at
   - Relationships: Many-to-one with User (task belongs to one user)
   - Indexes: Index on user_id for fast task list queries, composite index on (user_id, created_at) for paginated queries

**Validation Rules** (from spec Functional Requirements):
- FR-008: Task title non-empty, description optional
- FR-002: Email uniqueness enforced at database level
- Edge case: Title max 200 chars, description max 2000 chars
- Edge case: UTF-8 support for unicode/emojis in titles

**State Transitions**:
- Task completion: is_completed toggles between false ↔ true (FR-013)
- Timestamps: created_at set on creation, updated_at updated on any modification (FR-018, FR-019)

**Output**: `specs/backend/001-backend/data-model.md` with:
- Entity diagrams (text-based)
- Field specifications with types and constraints
- Relationship diagrams
- Index strategy
- Migration notes (if applicable from Phase 0 research)
- Ownership verification requirements (user_id foreign key constraints, indexes for efficient user-based queries)

### 1.2 API Contract Generation

**Objective**: Generate OpenAPI schemas for all endpoints defined in functional requirements.

**Endpoints** (extracted from spec):

**Authentication Endpoints**:
- `POST /api/auth/signup` (FR-001)
  - Request: `{email: string, password: string, name: string}`
  - Response 201: `{id: string, email: string, name: string, created_at: datetime}`
  - Response 409: Conflict if email exists (FR-002)
  - Response 422: Validation error

- `POST /api/auth/login` (FR-004)
  - Request: `{email: string, password: string}`
  - Response 200: `{access_token: string, token_type: "bearer", user: {id, email, name}}`
  - Response 401: Unauthorized if credentials incorrect
  - Response 422: Validation error

**Task Endpoints** (all require authentication):
- `POST /api/{user_id}/tasks` (FR-007)
  - Headers: `Authorization: Bearer <token>`
  - Path param: `user_id` (from JWT token, must match authenticated user)
  - Request: `{title: string, description?: string}`
  - Response 201: `{id, title, description, is_completed, user_id, created_at, updated_at}`
  - Response 401: Unauthorized if token invalid
  - Response 403: Forbidden if user_id in path doesn't match authenticated user (FR-016)
  - Response 422: Validation error

- `GET /api/{user_id}/tasks` (FR-009)
  - Headers: `Authorization: Bearer <token>`
  - Path param: `user_id` (from JWT token, must match authenticated user)
  - Query params: `limit?: number, offset?: number`
  - Response 200: `{tasks: [{task}], total: number, limit: number, offset: number}`
  - Response 401: Unauthorized
  - Response 403: Forbidden if user_id in path doesn't match authenticated user (FR-016)

- `GET /api/{user_id}/tasks/{task_id}` (FR-011)
  - Headers: `Authorization: Bearer <token>`
  - Path params: `user_id` (from JWT token, must match authenticated user), `task_id`
  - Response 200: `{task}`
  - Response 401: Unauthorized
  - Response 403: Forbidden if user_id in path doesn't match authenticated user (FR-016)
  - Response 404: Not found (FR-017)

- `PUT /api/{user_id}/tasks/{task_id}` (FR-012)
  - Headers: `Authorization: Bearer <token>`
  - Path params: `user_id` (from JWT token, must match authenticated user), `task_id`
  - Request: `{title: string, description?: string}`
  - Response 200: `{task}` (updated)
  - Response 401/403/404: As above

- `PATCH /api/{user_id}/tasks/{task_id}/complete` (FR-013)
  - Headers: `Authorization: Bearer <token>`
  - Path params: `user_id` (from JWT token, must match authenticated user), `task_id`
  - Request: `{is_completed: boolean}`
  - Response 200: `{task}` (updated)
  - Response 401/403/404: As above

- `DELETE /api/{user_id}/tasks/{task_id}` (FR-014)
  - Headers: `Authorization: Bearer <token>`
  - Path params: `user_id` (from JWT token, must match authenticated user), `task_id`
  - Response 204: No content (success)
  - Response 401/403/404: As above

**Documentation Endpoints**:
- `GET /docs` - Interactive Swagger UI (FR-020)
- `GET /redoc` - Alternative ReDoc interface (FR-021)

**Error Response Format** (FR-022):
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

**Output**: `specs/backend/001-backend/contracts/` containing:
- `auth.openapi.yaml` - Authentication endpoints OpenAPI 3.0 spec
- `tasks.openapi.yaml` - Task CRUD endpoints OpenAPI 3.0 spec
- `errors.schema.json` - Error response schemas

### 1.3 Quickstart Guide

**Objective**: Create developer-friendly guide for setting up backend and making first API calls.

**Content**:
1. **Prerequisites**: Python 3.13+, PostgreSQL (or Neon DB account), uv package manager
2. **Setup Steps**:
   - Clone repository
   - Install dependencies: `uv sync`
   - Copy `.env.example` to `.env` and configure DATABASE_URL, SECRET_KEY
   - Run database migrations (if applicable)
   - Start development server: `uvicorn src.main:app --reload`
3. **First API Calls**:
   - Register user: `POST /api/auth/signup`
   - Login: `POST /api/auth/login` (get token)
   - Create task: `POST /api/{user_id}/tasks` with Bearer token (user_id must match authenticated user)
   - List tasks: `GET /api/{user_id}/tasks` with Bearer token (user_id must match authenticated user)
4. **Testing**: `pytest tests/`
5. **API Documentation**: Navigate to `http://localhost:8000/docs`

**Output**: `specs/backend/001-backend/quickstart.md`

### 1.4 Agent Context Update

**Objective**: Update Claude Code agent context (CLAUDE.md) with backend technologies and conventions.

**Command**: `.specify/scripts/bash/update-agent-context.sh claude`

**New Technologies to Add**:
- FastAPI 0.115+ (web framework)
- SQLModel 0.0.24+ (ORM)
- PostgreSQL 15+ via Neon DB (database)
- JWT authentication (python-jose)
- pytest 8.0+ (testing framework)

**Output**: Updated `/mnt/d/Hackathon-II/todo-app/CLAUDE.md` with backend-specific guidance

---

## Phase 2: Re-evaluate Constitution Check

**Objective**: Verify constitution alignment after design artifacts are complete.

**Verification Steps**:
1. Review `data-model.md` for stateless design (Cloud Native Architecture)
2. Review `contracts/*.yaml` for security endpoints (Security & Authentication)
3. Verify error handling patterns in contracts (Correctness and Predictability)
4. Confirm modular structure in source code layout (Maintainability)
5. Validate no Phase III features introduced prematurely (Progressive Evolution)

**Expected Result**: All constitution principles remain satisfied. Any new concerns must be documented in Complexity Tracking section.

---

### Constitution Check Re-Evaluation (Post-Design)

**Date**: 2026-01-06
**Status**: ✅ PASSED - All principles satisfied

**Verification Results**:

1. **✅ Cloud Native Architecture** (data-model.md review)
   - Database design uses UUID primary keys (suitable for distributed systems)
   - No server-side session storage in schema
   - User-Task relationship supports stateless authentication via JWT
   - Indexes optimized for horizontal read scaling
   - Neon DB (serverless PostgreSQL) chosen for cloud-native deployment

2. **✅ Security & Authentication** (contracts/*.yaml review)
   - auth.openapi.yaml defines secure signup/login flows with JWT
   - tasks.openapi.yaml enforces BearerAuth on all task endpoints with user-scoped routing
   - User-scoped routing requires user_id in path parameter to match user_id in JWT token
   - Ownership verification ensures users can only access their own tasks
   - errors.schema.json documents 401/403 authorization scenarios
   - Password hashing (bcrypt) documented in research.md
   - JWT token expiration (30 min) configured
   - CORS configured for frontend origins only

3. **✅ Correctness and Predictability** (contracts/*.yaml review)
   - errors.schema.json defines consistent error format: `{"detail": "msg", "status_code": XXX}`
   - All edge cases from spec mapped to specific error responses
   - Validation errors follow Pydantic format with field locations
   - Pagination beyond total returns empty array (graceful handling)
   - Concurrent updates use last-write-wins (predictable behavior)

4. **✅ Maintainability and Extensibility** (source code layout review)
   - Clean separation: routers → services → models → core utilities
   - Each layer has single responsibility (routing, business logic, data, utilities)
   - Extensible for Phase III: services layer can add recurring task logic without touching routers
   - Type-safe: SQLModel + Pydantic provide full type hints
   - Testable: Each layer can be unit tested independently

5. **✅ Progressive Evolution** (design scope review)
   - No recurring tasks, reminders, or AI features in data model (deferred to Phase III per constitution)
   - No event-driven patterns in contracts (deferred to Phase III per constitution)
   - Simple RESTful CRUD focused on Phase II scope
   - Database schema is extensible: can add due_date, recurrence_pattern fields in Phase III migrations
   - Authentication foundation ready for Phase III AI agent integration

**Deferred Features Status** (from initial Constitution Check):
- **AI Agent Integration**: Still deferred to Phase III ✅ (backend provides data layer, no AI endpoints yet)
- **Event-Driven Design**: Still deferred to Phase III ✅ (synchronous REST only, no pub/sub or events)

**New Concerns**: None identified

**Conclusion**: Constitution principles remain fully satisfied after design phase. Backend architecture aligns with Phase II scope while preparing foundation for Phase III and IV features. No violations or complexity justifications needed.

---

## Development Phases (Post-Planning)

*These phases are executed by `/sp.tasks` and `/sp.implement` commands, not by `/sp.plan`.*

### Phase 3: Setup & Configuration (Future)
- Initialize backend/ directory structure
- Configure pyproject.toml with dependencies
- Create .env.example template
- Setup database connection and session management

### Phase 4: Models & Database (Future)
- Implement SQLModel User and Task models
- Create database initialization script
- Setup migrations (if decided in Phase 0)
- Write model unit tests

### Phase 5: Authentication (Future)
- Implement password hashing utilities
- Implement JWT generation and verification
- Create authentication dependency for FastAPI
- Implement /api/auth/signup endpoint
- Implement /api/auth/login endpoint
- Write authentication tests

### Phase 6: Task CRUD (Future)
- Implement task service layer (business logic)
- Implement POST /api/tasks endpoint
- Implement GET /api/tasks with pagination
- Implement GET /api/tasks/{task_id}
- Implement PUT /api/tasks/{task_id}
- Implement PATCH /api/tasks/{task_id}/complete
- Implement DELETE /api/tasks/{task_id}
- Write task endpoint tests

### Phase 7: Error Handling & CORS (Future)
- Implement custom exception handlers
- Configure CORS middleware for frontend origin
- Add request validation error handling
- Write error handling tests

### Phase 8: Testing & Documentation (Future)
- Achieve target test coverage (determined in Phase 0)
- Manual API testing via Swagger UI
- Integration testing with test database
- Update README.md with API overview

---

## Quality Gates

**Before Phase 0**: Constitution Check must pass ✅
**After Phase 0**: research.md complete with all 8 decisions documented
**After Phase 1**: data-model.md, contracts/, quickstart.md generated and reviewed
**After Phase 1**: Agent context updated with backend technologies
**After Phase 2**: Constitution Check re-verified, no new violations

---

## Success Metrics (from Spec)

- SC-001: User registration completes in <2s
- SC-002: Task creation and retrieval in <1s
- SC-003: 100% user data isolation enforced
- SC-004: API documentation accessible with 10+ endpoints
- SC-005: 100 concurrent requests handled without errors
- SC-006: API responses <500ms for single-user operations
- SC-007: 100% consistent JSON error format
- SC-008: Pagination handles 1000+ tasks correctly
- SC-009: 100% invalid tokens rejected with appropriate errors
- SC-010: Frontend can integrate without backend modifications

---

## Notes

- This plan covers Phase 0 (Research) and Phase 1 (Design) only, as per `/sp.plan` command scope
- Task generation (tasks.md) will be handled by `/sp.tasks` command after plan approval
- Implementation will be handled by `/sp.implement` command after tasks approval
- Backend serves as API layer for future Phase II frontend (Next.js)
- Architecture prepares for Phase III advanced features (recurring tasks, reminders, AI)
- Stateless design enables Phase IV cloud native deployment (Kubernetes, horizontal scaling)
