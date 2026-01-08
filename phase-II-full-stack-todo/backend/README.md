# Todo Backend API

Phase-II FastAPI Backend for Full-Stack Todo Web Application

## Features

- User authentication with JWT tokens
- Task CRUD operations with user isolation
- Paginated task listing
- RESTful API design
- Interactive API documentation (Swagger UI)
- PostgreSQL database with SQLModel ORM

## Tech Stack

- **Framework**: FastAPI 0.115+
- **Database**: PostgreSQL 15+ (Neon DB compatible)
- **ORM**: SQLModel 0.0.24+
- **Authentication**: JWT via python-jose
- **Password Hashing**: bcrypt via passlib
- **Testing**: pytest 8.0+
- **Package Manager**: uv

## Quick Start

### Prerequisites

- Python 3.13+
- PostgreSQL 15+ (or Neon DB account)
- uv package manager

### Installation

```bash
# Install dependencies
uv sync

# Copy environment template
cp .env.example .env

# Edit .env with your database URL and secret key
# Generate SECRET_KEY with: openssl rand -hex 32
```

### Running the Server

```bash
# Development mode (auto-reload)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/auth/signup | No | Register new user |
| POST | /api/auth/login | No | Login and get JWT token |
| GET | /api/tasks | Yes | List user's tasks (paginated) |
| POST | /api/tasks | Yes | Create new task |
| GET | /api/tasks/{id} | Yes | Get specific task |
| PUT | /api/tasks/{id} | Yes | Update task |
| PATCH | /api/tasks/{id}/complete | Yes | Toggle completion |
| DELETE | /api/tasks/{id} | Yes | Delete task |

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## Database Setup

### Local PostgreSQL

```bash
# Create database
createdb todo_db

# Update DATABASE_URL in .env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/todo_db
```

### Neon DB (Serverless PostgreSQL)

1. Sign up at [neon.tech](https://neon.tech)
2. Create new project
3. Copy connection string
4. Update DATABASE_URL in .env:
   ```
   DATABASE_URL=postgresql+asyncpg://user:password@host.neon.tech/dbname?sslmode=require
   ```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| DATABASE_URL | Yes | - | PostgreSQL connection string |
| SECRET_KEY | Yes | - | JWT signing key (min 32 chars) |
| ALGORITHM | No | HS256 | JWT algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | No | 30 | Token expiration time |
| CORS_ORIGINS | No | * | Comma-separated frontend origins |
| DEBUG | No | False | Enable debug mode |

## Project Structure

```
backend/
├── src/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment configuration
│   ├── models/
│   │   ├── user.py          # User entity
│   │   └── task.py          # Task entity
│   ├── routers/
│   │   ├── auth.py          # Authentication endpoints
│   │   └── tasks.py         # Task CRUD endpoints
│   ├── services/
│   │   ├── auth_service.py  # Authentication logic
│   │   └── task_service.py  # Task business logic
│   └── core/
│       ├── database.py      # Database connection
│       ├── dependencies.py  # FastAPI dependencies
│       └── security.py      # Security utilities
└── tests/
    ├── conftest.py          # Test fixtures
    ├── test_auth.py         # Authentication tests
    ├── test_tasks.py        # Task CRUD tests
    └── test_security.py     # Security utility tests
```

## Development

### Adding Dependencies

```bash
# Add new dependency
uv add package-name

# Add dev dependency
uv add --dev package-name
```

### Code Quality

```bash
# Run tests with coverage
pytest --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Troubleshooting

### Database Connection Error

- Verify PostgreSQL is running
- Check DATABASE_URL in .env
- For Neon DB, ensure `?sslmode=require` is in connection string

### Token Invalid/Expired

- Tokens expire after 30 minutes (configurable)
- Re-login to get fresh token
- Verify SECRET_KEY hasn't changed

### CORS Errors

- Add frontend origin to CORS_ORIGINS in .env
- Example: `CORS_ORIGINS=http://localhost:3000,http://localhost:3001`
- Restart backend after changing .env

## License

MIT
