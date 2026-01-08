# CLAUDE.md

This file provides guidance for Claude Code when working with this project.

## Project Overview

This is a spec-driven Next.js web application that implements a todo list manager. The project follows Spec-Kit Plus (SDD) methodology where all code originates from approved specifications.

## Development Workflow

1. **Create/Update Specification** (`/sp.specify`)
   - Define feature requirements in `specs/ui/001-frontend-ui/spec.md`
   - Document user stories with priorities (P1, P2, etc.)

2. **Create Implementation Plan** (`/sp.plan`)
   - Architecture decisions with trade-offs
   - Module structure and data model design
   - Saved to `specs/ui/001-frontend-ui/plan.md`

3. **Generate Tasks** (`/sp.tasks`)
   - Actionable task breakdown organized by user story
   - Saved to `specs/ui/001-frontend-ui/tasks.md`

4. **Implement** (`/sp.implement`)
   - Execute tasks following the plan
   - All code goes in `frontend/` directory

## Code Standards

### TypeScript Conventions

- **Follow TypeScript best practices** including proper typing
- Use interfaces for object shapes
- Use types for union types and aliases

### Next.js Conventions

- **App Router**: Use the Next.js 16+ App Router structure
- **Server Components**: Default choice for data fetching and rendering
- **Client Components**: Only where interactivity is required (use 'use client' directive)
- **File-based routing**: Follow Next.js conventions in `frontend/app/`

### Module Organization

```
frontend/
├── app/                 # Next.js App Router pages and layouts
│   ├── (auth)/          # Authentication-related routes
│   ├── dashboard/
│   ├── tasks/
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/          # Reusable UI components
│   ├── ui/              # Base UI components
│   ├── auth/            # Authentication components
│   ├── tasks/           # Task-related components
│   └── layout/          # Layout components
├── lib/                 # Shared utilities and API functions
│   ├── auth.ts
│   ├── api.ts
│   └── types.ts
├── services/            # API service layer
│   ├── auth-service.ts
│   └── task-service.ts
├── hooks/               # Custom React hooks
│   ├── useAuth.ts
│   └── useTasks.ts
└── public/              # Static assets
```

### Styling

- **Tailwind CSS**: Use utility-first approach with no inline styles
- **Responsive design**: Support from 320px to 1920px screen sizes
- **Accessibility**: Follow WCAG 2.1 AA standards

### Key Principles

- **Separation of concerns**: Components, services, and hooks have distinct responsibilities
- **No magic values**: Use constants or comments for special values
- **Error handling**: Show user-friendly messages, handle API errors gracefully
- **JWT authentication**: Attach tokens to all authenticated API requests

## Technical Constraints

- Next.js 16+ with App Router
- TypeScript 5.0+
- Tailwind CSS for styling (no inline styles)
- Better Auth for authentication
- JWT tokens for API authentication
- Responsive design for all screen sizes
- WCAG 2.1 AA accessibility compliance

## API Integration

- **Centralized API client**: All API calls go through a centralized client in `lib/api.ts`
- **JWT tokens**: Attached to all authenticated requests
- **Error handling**: Consistent error responses and user feedback

## Success Criteria

- All 5 features work correctly via web interface (Add, View, Update, Delete, Mark Complete)
- Application is responsive across desktop, tablet, and mobile
- Authentication flow works correctly with Better Auth
- Loading, empty, and error states are handled gracefully
- UI follows accessibility standards
- Code passes manual review for cleanliness and adherence to Next.js best practices

## Backend Development (Phase II)

### FastAPI Backend Standards

- **Python Version**: Python 3.13+ with uv package manager
- **Framework**: FastAPI 0.115+ for async RESTful APIs
- **ORM**: SQLModel 0.0.24+ for type-safe database operations
- **Database**: PostgreSQL 15+ via Neon DB (serverless PostgreSQL)
- **Authentication**: JWT tokens via python-jose[cryptography]
- **Password Security**: bcrypt hashing via passlib[bcrypt]
- **Testing**: pytest 8.0+ with pytest-asyncio for async tests

### Backend Module Organization

```
backend/
├── src/
│   ├── main.py              # FastAPI app, CORS, middleware
│   ├── config.py            # Environment variables, settings
│   ├── models/
│   │   ├── user.py          # SQLModel User entity
│   │   └── task.py          # SQLModel Task entity
│   ├── routers/
│   │   ├── auth.py          # POST /api/auth/signup, /login
│   │   └── tasks.py         # Task CRUD endpoints
│   ├── services/
│   │   ├── auth_service.py  # Password hashing, JWT logic
│   │   └── task_service.py  # Task business logic
│   └── core/
│       ├── database.py      # SQLModel engine, session
│       ├── dependencies.py  # FastAPI dependencies
│       └── security.py      # JWT utilities
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   ├── test_auth.py         # Auth endpoint tests
│   ├── test_tasks.py        # Task CRUD tests
│   └── test_security.py     # Security utilities tests
└── .env.example             # Environment variable template
```

### Backend Key Principles

- **Stateless Design**: No server-side sessions, JWT-only authentication for horizontal scaling
- **Type Safety**: Full type hints using Python 3.13+ and Pydantic validation
- **User Isolation**: All task queries enforce user ownership via user_id from JWT
- **Error Handling**: Consistent JSON error responses `{"detail": "message", "status_code": XXX}`
- **Security**: Environment variables for secrets, bcrypt for passwords, JWT with expiration
- **API Documentation**: Auto-generated OpenAPI/Swagger at `/docs` and ReDoc at `/redoc`

### Backend API Constraints

- **Authentication**: JWT tokens required for all task endpoints
- **Pagination**: Limit-offset with default limit=50, max=100
- **Validation**: Pydantic models validate all request/response data
- **CORS**: Configured for frontend origins (Next.js on port 3000)
- **Performance**: <500ms response time, handles 100 concurrent requests

### Backend Development Workflow

1. **Specification**: `specs/backend/001-backend/spec.md`
2. **Implementation Plan**: `specs/backend/001-backend/plan.md`
3. **Data Model**: `specs/backend/001-backend/data-model.md`
4. **API Contracts**: `specs/backend/001-backend/contracts/*.openapi.yaml`
5. **Quickstart**: `specs/backend/001-backend/quickstart.md`

## Active Technologies

- TypeScript 5.0+ + Next.js 16+ (001-frontend-ui)
- Tailwind CSS (001-frontend-ui)
- Better Auth (001-frontend-ui)
- Python 3.13+ + FastAPI 0.115+ (001-backend)
- SQLModel 0.0.24+ (001-backend)
- PostgreSQL 15+ via Neon DB (001-backend)

## Recent Changes

- 001-frontend-ui: Added TypeScript 5.0+ + Next.js 16+
- 001-frontend-ui: Added Tailwind CSS
- 001-frontend-ui: Added Better Auth
- 001-backend: Added Python 3.13+ + FastAPI 0.115+
- 001-backend: Added SQLModel 0.0.24+ with PostgreSQL 15+
- 001-backend: Added JWT authentication with python-jose and bcrypt password hashing