# Quickstart Guide: Phase-II FastAPI Backend

**Feature**: Phase-II FastAPI Backend for Full-Stack Todo Web Application
**Date**: 2026-01-06
**Audience**: Backend developers setting up local development environment

This guide walks you through setting up the backend, making your first API calls, and exploring the interactive documentation.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Database Setup](#database-setup)
5. [Running the Server](#running-the-server)
6. [First API Calls](#first-api-calls)
7. [Interactive API Documentation](#interactive-api-documentation)
8. [Running Tests](#running-tests)
9. [Common Issues](#common-issues)

---

## Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.13+**: Check with `python --version` or `python3 --version`
- **uv Package Manager**: Install with `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **PostgreSQL 15+**: Either local installation or Neon DB account
- **Git**: For cloning the repository

**Optional but Recommended**:
- **Docker**: For containerized PostgreSQL (easier than local install)
- **Postman or curl**: For API testing (though Swagger UI works great too)

---

## Installation

### 1. Clone the Repository

```bash
cd /path/to/your/projects
git clone https://github.com/yourusername/todo-app.git
cd todo-app
```

### 2. Checkout Backend Branch

```bash
git checkout 001-backend
```

### 3. Install Dependencies

The project uses `uv` for dependency management, which is faster than `pip`.

```bash
# Navigate to backend directory
cd backend

# Install dependencies (uv will create virtual environment automatically)
uv sync

# Activate virtual environment (optional, uv handles this automatically)
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows
```

**Dependencies Installed**:
- FastAPI 0.115+ (web framework)
- Uvicorn (ASGI server)
- SQLModel 0.0.24+ (ORM)
- psycopg2-binary (PostgreSQL driver)
- python-jose[cryptography] (JWT)
- passlib[bcrypt] (password hashing)
- python-dotenv (environment variables)
- pytest & httpx (testing)

---

## Configuration

### 1. Create Environment File

Copy the example environment file and customize it:

```bash
cp .env.example .env
```

### 2. Configure Environment Variables

Edit `.env` with your configuration:

```bash
# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/todo_db
# For Neon DB: postgresql+asyncpg://user:password@host.neon.tech/dbname?sslmode=require

# JWT Configuration
SECRET_KEY=your-secret-key-here-min-32-chars-recommended-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration (frontend origins)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Application Settings
API_TITLE=Todo Backend API
API_VERSION=1.0.0
DEBUG=True
```

**Generating a Secure SECRET_KEY**:

```bash
# Option 1: Using openssl (recommended)
openssl rand -hex 32

# Option 2: Using Python
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Database Connection Options

**Option A: Neon DB (Serverless PostgreSQL)**

1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string
4. Set `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL=postgresql+asyncpg://user:password@ep-cool-name-123456.us-east-2.aws.neon.tech/dbname?sslmode=require
   ```

**Option B: Local PostgreSQL**

```bash
# Install PostgreSQL (example for Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres psql
CREATE DATABASE todo_db;
CREATE USER todo_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE todo_db TO todo_user;
\q

# Set DATABASE_URL in .env
DATABASE_URL=postgresql+asyncpg://todo_user:your_password@localhost:5432/todo_db
```

**Option C: Docker PostgreSQL**

```bash
# Run PostgreSQL container
docker run --name todo-postgres \
  -e POSTGRES_DB=todo_db \
  -e POSTGRES_USER=todo_user \
  -e POSTGRES_PASSWORD=your_password \
  -p 5432:5432 \
  -d postgres:15

# Set DATABASE_URL in .env
DATABASE_URL=postgresql+asyncpg://todo_user:your_password@localhost:5432/todo_db
```

---

## Database Setup

### Phase II: Auto-Create Tables

In Phase II, we use `SQLModel.metadata.create_all()` to automatically create tables on server startup.

**Tables Created Automatically**:
- `users` (id, email, hashed_password, name, created_at, updated_at)
- `tasks` (id, title, description, is_completed, user_id, created_at, updated_at)

**No manual migration needed** for Phase II. Tables are created on first server start.

---

## Running the Server

### Development Server (Auto-Reload)

```bash
# From backend/ directory
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Server Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process using WatchFiles
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Access Points**:
- API Base: `http://localhost:8000`
- Swagger UI (Interactive Docs): `http://localhost:8000/docs`
- ReDoc (Alternative Docs): `http://localhost:8000/redoc`
- Health Check (if implemented): `http://localhost:8000/health`

### Production Server (No Auto-Reload)

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## First API Calls

### Using curl

#### 1. Register a New User

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "SecurePass123!",
    "name": "Alice Johnson"
  }'
```

**Expected Response (201 Created)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "alice@example.com",
  "name": "Alice Johnson",
  "created_at": "2026-01-06T10:30:00Z"
}
```

#### 2. Login to Get JWT Token

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "SecurePass123!"
  }'
```

**Expected Response (200 OK)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "alice@example.com",
    "name": "Alice Johnson"
  }
}
```

**Save the `access_token` for subsequent requests!**

#### 3. Create a Task

```bash
# Replace <YOUR_TOKEN> with actual token from login response
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }'
```

**Expected Response (201 Created)**:
```json
{
  "id": "650e8400-e29b-41d4-a716-446655440001",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_completed": false,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2026-01-06T10:35:00Z",
  "updated_at": "2026-01-06T10:35:00Z"
}
```

#### 4. List All Tasks

```bash
curl -X GET "http://localhost:8000/api/tasks?limit=50&offset=0" \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

**Expected Response (200 OK)**:
```json
{
  "tasks": [
    {
      "id": "650e8400-e29b-41d4-a716-446655440001",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "is_completed": false,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "created_at": "2026-01-06T10:35:00Z",
      "updated_at": "2026-01-06T10:35:00Z"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

#### 5. Mark Task as Complete

```bash
# Replace <TASK_ID> with actual task ID
curl -X PATCH "http://localhost:8000/api/tasks/<TASK_ID>/complete" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -d '{"is_completed": true}'
```

#### 6. Update Task

```bash
curl -X PUT "http://localhost:8000/api/tasks/<TASK_ID>" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -d '{
    "title": "Buy groceries (updated)",
    "description": "Milk, eggs, bread, butter"
  }'
```

#### 7. Delete Task

```bash
curl -X DELETE "http://localhost:8000/api/tasks/<TASK_ID>" \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

**Expected Response (204 No Content)** - Empty body

---

## Interactive API Documentation

FastAPI automatically generates interactive API documentation. This is the easiest way to test endpoints!

### Swagger UI (Recommended)

1. Start the server: `uvicorn src.main:app --reload`
2. Open browser: `http://localhost:8000/docs`
3. You'll see all endpoints with "Try it out" buttons

**How to Use**:
1. **Signup**: Expand `POST /api/auth/signup`, click "Try it out", fill in request body, execute
2. **Login**: Expand `POST /api/auth/login`, execute to get token
3. **Authorize**: Click green "Authorize" button at top, paste token (without "Bearer"), click "Authorize"
4. **Try Protected Endpoints**: All task endpoints now use your token automatically

### ReDoc (Alternative)

- URL: `http://localhost:8000/redoc`
- More polished documentation view, but no "Try it out" functionality
- Better for sharing API reference with frontend team

---

## Running Tests

### Full Test Suite

```bash
# From backend/ directory
pytest tests/ -v
```

**Expected Output**:
```
tests/test_auth.py::test_signup_success PASSED
tests/test_auth.py::test_signup_duplicate_email PASSED
tests/test_auth.py::test_login_success PASSED
tests/test_auth.py::test_login_invalid_credentials PASSED
tests/test_tasks.py::test_create_task PASSED
tests/test_tasks.py::test_list_tasks PASSED
tests/test_tasks.py::test_user_isolation PASSED
...
==================== 25 passed in 3.42s ====================
```

### Run Specific Test File

```bash
pytest tests/test_auth.py -v
```

### Run with Coverage Report

```bash
pytest tests/ --cov=src --cov-report=html
```

Open `htmlcov/index.html` to view coverage report.

### Test Categories

- `tests/test_auth.py`: Authentication (signup, login, token validation)
- `tests/test_tasks.py`: Task CRUD operations and user isolation
- `tests/test_security.py`: Password hashing and JWT utilities (unit tests)

---

## Common Issues

### Issue 1: Database Connection Error

**Error**:
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solutions**:
- Verify PostgreSQL is running: `sudo systemctl status postgresql` (Linux)
- Check `DATABASE_URL` in `.env` is correct
- For Neon DB, ensure `?sslmode=require` is appended to connection string
- Test connection: `psql $DATABASE_URL` (requires psql client)

### Issue 2: Token Invalid/Expired

**Error** (401 Unauthorized):
```json
{"detail": "Invalid authentication credentials", "status_code": 401}
```

**Solutions**:
- Token expires after 30 minutes (configurable in `.env`)
- Re-login to get fresh token
- Verify token is passed in header: `Authorization: Bearer <token>`
- Check `SECRET_KEY` hasn't changed (tokens become invalid if key changes)

### Issue 3: Import Errors

**Error**:
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solutions**:
- Ensure virtual environment is activated: `source .venv/bin/activate`
- Reinstall dependencies: `uv sync`
- Check you're in `backend/` directory, not repo root

### Issue 4: Port Already in Use

**Error**:
```
OSError: [Errno 98] Address already in use
```

**Solutions**:
- Stop other process using port 8000: `lsof -ti:8000 | xargs kill`
- Use different port: `uvicorn src.main:app --reload --port 8001`
- Check no other backend instances are running

### Issue 5: CORS Errors (When Integrating with Frontend)

**Error** (in browser console):
```
Access to fetch at 'http://localhost:8000/api/tasks' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solutions**:
- Add frontend origin to `CORS_ORIGINS` in `.env`:
  ```
  CORS_ORIGINS=http://localhost:3000,http://localhost:3001
  ```
- Restart backend server after changing `.env`
- For production, set frontend production URL in `CORS_ORIGINS`

---

## Next Steps

After successful quickstart:

1. **Explore API Documentation**: Familiarize yourself with all endpoints at `/docs`
2. **Read Data Model**: Review `specs/backend/001-backend/data-model.md` for database schema
3. **Check Contracts**: OpenAPI specs in `specs/backend/001-backend/contracts/`
4. **Frontend Integration**: Share API base URL and `/docs` link with frontend team
5. **Phase III Planning**: Once frontend connects successfully, plan advanced features (recurring tasks, reminders)

---

## API Endpoints Summary

| Method | Endpoint                      | Auth Required | Description                     |
|--------|-------------------------------|---------------|---------------------------------|
| POST   | /api/auth/signup              | No            | Register new user               |
| POST   | /api/auth/login               | No            | Login and get JWT token         |
| GET    | /api/tasks                    | Yes           | List user's tasks (paginated)   |
| POST   | /api/tasks                    | Yes           | Create new task                 |
| GET    | /api/tasks/{task_id}          | Yes           | Get specific task               |
| PUT    | /api/tasks/{task_id}          | Yes           | Update task title/description   |
| PATCH  | /api/tasks/{task_id}/complete | Yes           | Toggle task completion          |
| DELETE | /api/tasks/{task_id}          | Yes           | Delete task permanently         |
| GET    | /docs                         | No            | Swagger UI (interactive)        |
| GET    | /redoc                        | No            | ReDoc (alternative docs)        |

---

## Environment Variables Reference

| Variable                      | Required | Default | Description                              |
|-------------------------------|----------|---------|------------------------------------------|
| DATABASE_URL                  | Yes      | -       | PostgreSQL connection string             |
| SECRET_KEY                    | Yes      | -       | JWT signing key (min 32 chars)           |
| ALGORITHM                     | No       | HS256   | JWT algorithm                            |
| ACCESS_TOKEN_EXPIRE_MINUTES   | No       | 30      | Token expiration time                    |
| CORS_ORIGINS                  | No       | *       | Comma-separated frontend origins         |
| API_TITLE                     | No       | -       | API title in documentation               |
| API_VERSION                   | No       | 1.0.0   | API version in documentation             |
| DEBUG                         | No       | False   | Enable debug mode (verbose errors)       |

---

## Support & Resources

- **API Documentation**: http://localhost:8000/docs (when server is running)
- **Specification**: `specs/backend/001-backend/spec.md`
- **Data Model**: `specs/backend/001-backend/data-model.md`
- **Implementation Plan**: `specs/backend/001-backend/plan.md`
- **Research Decisions**: `specs/backend/001-backend/research.md`
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLModel Docs**: https://sqlmodel.tiangolo.com

---

**Happy Coding!** 🚀

If you encounter issues not covered here, check the main README.md or consult the backend implementation plan.
