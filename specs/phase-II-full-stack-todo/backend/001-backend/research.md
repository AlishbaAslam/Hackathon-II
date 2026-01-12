# Phase 0: Research & Technology Decisions

**Feature**: Phase-II FastAPI Backend for Full-Stack Todo Web Application
**Date**: 2026-01-06
**Status**: Complete

This document records all technology decisions made during Phase 0 research, including rationale and alternatives considered.

---

## 1. Database ORM Selection

**Decision**: SQLModel 0.0.24+

**Rationale**:
- **Type Safety**: SQLModel combines SQLAlchemy's power with Pydantic's validation, providing full type hints and IDE autocomplete
- **FastAPI Integration**: Designed by FastAPI creator (Sebastián Ramírez) for seamless integration - same Pydantic models work for validation and database
- **Dual Purpose Models**: Single model definition serves both API validation and database schema, reducing code duplication
- **Developer Experience**: Simpler syntax than raw SQLAlchemy while maintaining full ORM capabilities
- **Async Support**: Built on SQLAlchemy 2.0+ with full async/await support for high-performance database operations
- **Migration Path**: Uses Alembic under the hood, providing professional migration tooling when needed in Phase III

**Alternatives Considered**:
- **SQLAlchemy Core**: More flexibility but verbose syntax, requires separate Pydantic models for validation (code duplication), steeper learning curve
- **Raw SQL with psycopg2**: Maximum control and performance but no type safety, prone to SQL injection if not careful, no automatic migration support, high maintenance burden
- **Tortoise ORM**: Django-like async ORM but smaller ecosystem, less FastAPI integration, fewer learning resources

**Constitution Alignment**: Supports Maintainability and Extensibility (clean, typed code), Correctness (Pydantic validation), Progressive Evolution (migration support for Phase III)

---

## 2. JWT Library Selection

**Decision**: python-jose[cryptography] 3.3+

**Rationale**:
- **Industry Standard**: Implements JOSE standards (JSON Object Signing and Encryption) used widely in OAuth2 and OpenID Connect
- **Algorithm Support**: Supports HS256 (HMAC-SHA256) for symmetric signing, suitable for single-service architecture in Phase II
- **FastAPI Documentation**: Featured in official FastAPI security tutorials, well-tested integration patterns
- **Cryptography Backend**: [cryptography] extra provides robust, audited cryptographic implementations
- **Token Validation**: Built-in expiration checking, signature verification, and claim validation
- **Simple API**: Straightforward encode/decode interface, minimal configuration needed

**Alternatives Considered**:
- **PyJWT**: Lighter weight, popular library but less comprehensive than python-jose, missing some JOSE features we may need in Phase III
- **authlib**: More comprehensive (OAuth2 server, client, etc.) but heavyweight for our needs - we only need JWT generation/verification, not full OAuth2 server
- **python-jwt**: Less maintained, smaller community, fewer security audits

**Constitution Alignment**: Supports Security & Authentication (industry-standard JWT), Maintainability (simple API), Progressive Evolution (JOSE standards support for future OAuth2 in Phase IV)

---

## 3. Password Hashing Strategy

**Decision**: bcrypt via passlib[bcrypt] 1.7+

**Rationale**:
- **Industry Standard**: bcrypt is time-tested (since 1999), widely audited, trusted by major companies (Dropbox, Auth0, etc.)
- **Adaptive Cost Factor**: Work factor (rounds) can be increased as computing power grows, maintaining security over time
- **Built-in Salt**: Automatically generates random salt per password, prevents rainbow table attacks
- **passlib Integration**: passlib provides unified interface for multiple hashing algorithms with automatic salt generation and verification
- **Performance Balance**: Slower than argon2 but proven security, suitable for login operations (not called frequently)
- **FastAPI Tutorials**: Featured in FastAPI security documentation with well-tested patterns

**Alternatives Considered**:
- **argon2**: Winner of Password Hashing Competition (2015), more memory-hard, but requires native C libraries (deployment complexity), less mature ecosystem
- **scrypt**: Memory-hard like argon2 but less standardized, fewer libraries support it, potential side-channel vulnerabilities if misconfigured
- **PBKDF2**: SHA-based key derivation, NIST-approved but slower than bcrypt for same security level, less recommended by modern security experts

**Constitution Alignment**: Supports Security & Authentication (cryptographic password storage), Correctness (automatic salt generation prevents common mistakes)

---

## 4. Error Handling Pattern

**Decision**: Custom FastAPI exception handlers with standardized JSON responses

**Rationale**:
- **Consistent API Contract**: All errors return `{"detail": "message", "status_code": XXX}` format per FR-022
- **Client-Friendly**: Frontend can rely on consistent error structure for user feedback
- **Separation of Concerns**: Business logic raises custom exceptions, HTTP layer handles serialization
- **Security**: Custom handlers prevent leaking stack traces or internal details to clients (FR-023, edge case)
- **FastAPI Integration**: Exception handlers integrate seamlessly with FastAPI's dependency injection and middleware
- **Debugging Support**: Logging middleware can capture full error details server-side while returning safe messages to client

**Custom Exceptions to Define**:
- `UnauthorizedException` (401) - Invalid/expired token
- `ForbiddenException` (403) - Valid token but insufficient permissions (FR-016)
- `NotFoundException` (404) - Resource not found (FR-017)
- `ConflictException` (409) - Resource conflict, e.g. email already exists (FR-002)
- `ValidationException` (422) - Pydantic validation errors

**Alternatives Considered**:
- **Default FastAPI Error Handling**: Inconsistent response formats (validation errors differ from HTTP exceptions), exposes internal details in development mode
- **HTTP Exception Middleware**: Less granular control, harder to customize per exception type, mixes concerns

**Constitution Alignment**: Supports Correctness and Predictability (consistent error responses), Security (safe error messages), Maintainability (clear exception hierarchy)

---

## 5. API Versioning Strategy

**Decision**: No versioning for Phase II, prepare for URL-based versioning (/api/v1) in Phase III

**Rationale**:
- **Phase II Scope**: Initial API implementation, no backward compatibility concerns yet, frontend and backend developed together
- **YAGNI Principle**: Versioning adds complexity without immediate benefit, premature optimization for Phase II
- **Simple URL Structure**: `/api/tasks` cleaner than `/api/v1/tasks` for initial development
- **Easy Migration Path**: When Phase III introduces breaking changes, refactor to `/api/v1/*` (existing) and `/api/v2/*` (new features)
- **URL-Based Future**: URL versioning chosen over headers because it's explicit, cacheable, easier to test/debug

**Alternatives Considered**:
- **URL-Based Versioning Now**: `/api/v1/*` from start - adds complexity without benefit in Phase II, premature planning
- **Header-Based Versioning**: `Accept: application/vnd.api.v1+json` - less visible, harder to test with Swagger UI, not cacheable
- **Query Parameter Versioning**: `/api/tasks?version=1` - non-standard, conflicts with other query params, poor caching

**Constitution Alignment**: Supports Progressive Evolution (simple now, extensible later), Maintainability (avoid premature complexity)

---

## 6. Pagination Approach

**Decision**: Limit-offset pagination with default limit=50, max limit=100

**Rationale**:
- **Simplicity**: Easy to implement and understand, maps directly to SQL `LIMIT`/`OFFSET`
- **Frontend UX**: Supports both "load more" and page numbers patterns
- **Performance Sufficient**: For expected scale (1000+ tasks per user, SC-008), offset pagination performs adequately with proper indexes
- **SQL Optimization**: Index on (user_id, created_at) enables fast queries even at high offsets
- **Standard Response**: `{tasks: [...], total: number, limit: number, offset: number}` provides full pagination metadata

**Query Parameters**:
- `limit`: Number of results to return (default: 50, max: 100)
- `offset`: Number of results to skip (default: 0)
- Example: `GET /api/tasks?limit=20&offset=40` returns tasks 41-60

**Alternatives Considered**:
- **Cursor-Based Pagination**: More efficient for very large datasets, prevents missing items when data changes, but complex to implement, requires opaque cursors (e.g. base64-encoded timestamps), doesn't support page numbers
- **Page-Based Pagination**: `?page=2&size=20` - syntactic sugar over limit-offset, no technical advantage, adds conversion logic

**Constitution Alignment**: Supports Correctness (handles edge cases per spec), Performance (adequate for Phase II scale), Progressive Evolution (can migrate to cursor-based in Phase IV if scale demands)

---

## 7. Database Migration Tool

**Decision**: Defer migrations to Phase III, use SQLModel.metadata.create_all() for Phase II

**Rationale**:
- **Phase II Scope**: Initial schema implementation, no existing data to migrate, development environment only
- **Rapid Iteration**: Direct table creation enables fast schema changes during Phase II development
- **Neon DB**: Serverless PostgreSQL allows easy database recreation for schema changes in development
- **Phase III Planning**: Recurring tasks and reminders (Phase III) will require schema changes - introduce Alembic migrations at that point
- **SQLModel Foundation**: SQLModel uses SQLAlchemy under the hood, making Alembic migration straightforward to add later

**Development Workflow (Phase II)**:
1. Modify SQLModel models
2. Drop and recreate database schema: `await SQLModel.metadata.drop_all(engine)` + `await SQLModel.metadata.create_all(engine)`
3. Reseed test data if needed

**Phase III Migration Plan**:
- Install alembic: `uv add alembic`
- Initialize: `alembic init migrations`
- Generate initial migration: `alembic revision --autogenerate -m "Initial schema"`
- Apply migrations: `alembic upgrade head`

**Alternatives Considered**:
- **Alembic from Start**: Professional approach but adds complexity, migration files to maintain, slower iteration during Phase II development when schema changes frequently
- **Manual SQL Migrations**: Error-prone, no rollback support, doesn't track changes, high maintenance

**Constitution Alignment**: Supports Progressive Evolution (introduce migrations when needed), Maintainability (simpler Phase II development), Correctness (Alembic provides rollback safety in Phase III)

---

## 8. Test Coverage Level

**Decision**: High coverage (80%+) with focus on critical paths - authentication, authorization, and data isolation

**Rationale**:
- **Constitution Requirement**: Correctness and Predictability demands comprehensive testing, especially for security-critical features
- **Critical Test Areas**:
  - **Authentication**: Password hashing, JWT generation/verification, token expiration
  - **Authorization**: User data isolation (FR-010, SC-003), ownership verification (FR-015, FR-016)
  - **Task CRUD**: All 5 functional requirements (create, read, update, delete, complete)
  - **Error Handling**: All error scenarios from spec edge cases
  - **Pagination**: Edge cases per SC-008 (empty results, offset beyond total, 1000+ tasks)
- **Test Strategy**:
  - Unit tests: Password hashing, JWT utilities, business logic in services
  - Integration tests: API endpoints with test database, request/response validation
  - Fixture-based: pytest fixtures for test client, test database, authenticated user tokens
- **Fast Feedback**: In-memory test database (SQLite) for unit tests, dedicated test database (PostgreSQL) for integration tests

**Test Categories**:
- `tests/test_auth.py`: Signup, login, token validation (User Story 1)
- `tests/test_tasks.py`: Task CRUD operations (User Stories 2, 3, 4)
- `tests/test_security.py`: Password hashing, JWT utilities (unit tests)
- `tests/conftest.py`: Shared pytest fixtures

**Alternatives Considered**:
- **Critical Paths Only (60% coverage)**: Faster development but risks missing edge cases, insufficient for security-critical authentication system
- **100% Coverage**: Diminishing returns, tests low-value code like getters/setters, slows down development without proportional benefit

**Constitution Alignment**: Supports Correctness and Predictability (comprehensive testing), Security & Authentication (test all auth flows), Maintainability (fixture-based tests)

---

## Implementation Priorities

Based on research, recommended implementation order:

1. **Setup** (Phase 3): Project structure, dependencies, environment configuration
2. **Database Foundation** (Phase 4): SQLModel models (User, Task), database session management
3. **Authentication Core** (Phase 5): Password hashing, JWT generation, authentication dependency
4. **Auth Endpoints** (Phase 5): Signup and login APIs
5. **Task CRUD** (Phase 6): Task service layer and all task endpoints
6. **Error Handling** (Phase 7): Custom exceptions and handlers
7. **Testing** (Phase 8): Unit and integration tests achieving 80%+ coverage

---

## Environment Variables

**Required Configuration** (to be documented in .env.example):

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname
# For Neon DB: postgresql+asyncpg://user:password@host.neon.tech/dbname?sslmode=require

# JWT Configuration
SECRET_KEY=your-secret-key-min-32-chars  # Generate with: openssl rand -hex 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (frontend origin)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Application
API_TITLE="Todo Backend API"
API_VERSION="1.0.0"
DEBUG=False
```

**Security Notes**:
- Never commit .env to version control (.gitignore)
- Use strong SECRET_KEY (32+ random bytes)
- Restrict CORS_ORIGINS to known frontend domains
- Disable DEBUG in production

---

## Dependencies Summary

**Core Framework**:
- `fastapi = "^0.115.0"` - Web framework
- `uvicorn[standard] = "^0.32.0"` - ASGI server with performance extras
- `python-dotenv = "^1.0.0"` - Environment variable loading

**Database**:
- `sqlmodel = "^0.0.24"` - ORM with Pydantic integration
- `psycopg2-binary = "^2.9.10"` - PostgreSQL driver
- `asyncpg = "^0.30.0"` - Async PostgreSQL driver

**Security**:
- `python-jose[cryptography] = "^3.3.0"` - JWT handling
- `passlib[bcrypt] = "^1.7.4"` - Password hashing

**Validation**:
- `pydantic = "^2.10.0"` - Data validation (included with FastAPI)
- `email-validator = "^2.2.0"` - Email validation

**Testing**:
- `pytest = "^8.0.0"` - Test framework
- `pytest-asyncio = "^0.24.0"` - Async test support
- `httpx = "^0.27.0"` - Async HTTP client for API tests
- `pytest-cov = "^6.0.0"` - Coverage reporting

---

## Phase 0 Completion Checklist

- [x] Database ORM decision documented (SQLModel)
- [x] JWT library decision documented (python-jose)
- [x] Password hashing decision documented (bcrypt via passlib)
- [x] Error handling pattern documented (custom exception handlers)
- [x] API versioning decision documented (no versioning for Phase II)
- [x] Pagination approach documented (limit-offset)
- [x] Database migration strategy documented (defer to Phase III)
- [x] Test coverage level documented (80%+ with focus on critical paths)
- [x] Environment variables documented
- [x] Dependencies summarized

**Status**: ✅ Phase 0 Research Complete - Ready for Phase 1 (Design Artifacts)
