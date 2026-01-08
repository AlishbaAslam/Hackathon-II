# Backend (FastAPI) — CLAUDE.md

This folder contains the **Phase II backend API** for the Todo app. It is a **FastAPI + SQLModel** service designed for **stateless JWT authentication**, **user-isolated task CRUD**, and **PostgreSQL/Neon-compatible persistence**.

## Purpose

- Provide a RESTful API consumed by the Next.js frontend
- Persist users and tasks in a relational database
- Enforce **user isolation** on all task operations (tasks belong to the authenticated user)
- Implement **stateless authentication** via signed JWTs (no server-side sessions)
- Provide consistent error responses and API docs

## Key features

- **Auth**: signup/login issuing JWT access tokens
- **Task CRUD**: create, list (paginated), read, update, delete
- **Completion toggle**: mark complete/incomplete
- **User isolation**: all task queries are scoped to the user from the JWT
- **Validation**: Pydantic/SQLModel validation for requests and responses
- **Docs**: Swagger/OpenAPI at `/docs`, ReDoc at `/redoc`
- **Testing**: pytest suite for auth, tasks, security, integration, and error handling

## Tech stack

- **Python**: 3.12+ (project requirement in `pyproject.toml`)
- **FastAPI**: 0.115+
- **SQLModel**: 0.0.24+
- **Database**: PostgreSQL 15+ (Neon compatible)
  - Local development/tests may also use SQLite (see local DB files in repo)
- **JWT**: `python-jose[cryptography]`
- **Password hashing**: `passlib[bcrypt]`
- **Server**: `uvicorn`
- **Package manager**: `uv`

## High-level architecture

- `src/main.py` boots the FastAPI app, configures CORS, registers routers, and installs exception handlers.
- `src/routers/` defines HTTP endpoints and request/response contracts.
- `src/services/` contains business logic (auth and task operations).
- `src/models/` defines SQLModel entities.
- `src/core/` holds cross-cutting concerns: database session/engine, dependencies, security/JWT helpers, middleware, and exceptions.
- `tests/` contains pytest test suite.

## Directory structure

```
backend/
├── src/
│   ├── main.py              # FastAPI app entrypoint (routers, CORS, errors)
│   ├── config.py            # Settings/env configuration
│   ├── core/
│   │   ├── database.py      # Engine/session + table creation
│   │   ├── dependencies.py  # FastAPI dependencies (db session, current user, etc.)
│   │   ├── security.py      # JWT helpers, password hashing helpers
│   │   ├── jwt_middleware.py# JWT validation middleware (if used by routes)
│   │   └── exceptions.py    # Domain exceptions + status codes
│   ├── models/
│   │   ├── user.py          # User SQLModel
│   │   └── task.py          # Task SQLModel
│   ├── routers/
│   │   ├── auth.py          # /api/auth/* endpoints
│   │   └── tasks.py         # /api/tasks* endpoints
│   └── services/
│       ├── auth_service.py  # Auth logic (signup/login, token creation)
│       └── task_service.py  # Task business logic
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_tasks.py
│   ├── test_security.py
│   ├── test_errors.py
│   ├── test_docs.py
│   └── test_integration.py
├── pyproject.toml           # Dependencies + tooling config (pytest, coverage)
├── uv.lock                  # Locked dependency graph
├── .env                     # Local environment (do not commit secrets)
└── README.md                # Setup and endpoint overview
```

## Error handling contract

The API aims to return consistent JSON error shapes:

```json
{ "detail": "message", "status_code": 401 }
```

(See exception handlers in `src/main.py`.)

## Environment variables

Configured via `.env` (see `README.md` for details). Typical values:

- `DATABASE_URL` (PostgreSQL/Neon connection string)
- `SECRET_KEY` (JWT signing key)
- `ALGORITHM` (default HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `CORS_ORIGINS`
- `DEBUG`

## Common commands

From this folder:

- Install deps: `uv sync`
- Run dev server: `uvicorn src.main:app --reload --host 0.0.0.0 --port 8000`
- Run tests: `pytest`

## Conventions (project-specific)

- Keep routes thin; put business rules in `src/services/`.
- Enforce user isolation at the service/query level (derive user identity from JWT).
- Don’t introduce server-side sessions; stay stateless (JWT only).
- Prefer consistent error responses (`detail` + `status_code`).
- Avoid committing secrets; use environment variables.
