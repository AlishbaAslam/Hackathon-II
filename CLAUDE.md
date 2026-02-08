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

### Active Agents for Project
- **mcp-tools-specialist**: Use this agent when designing and implementing MCP tools using the Official MCP SDK in the current project. This agent should be used specifically for creating stateless tools with user_id isolation and DB persistence that follow the Spec-Driven Development (SDD) workflow. It ALWAYS uses Context7 MCP for all doc access/updates.
- **ai-agent-engineer**: Use this agent when building and configuring OpenAI Agents SDK logic using OpenRouter (no OpenAI key) for the AI-powered chatbot project. This agent handles agent creation, tool calling, behavior mapping, confirmation responses, and error handling. It ALWAYS uses Context7 MCP for all doc access/updates.
- **chatbot-spec-architect**: Use this agent when writing, validating, and updating specifications for the AI-powered chatbot project (overview, features, API endpoints, MCP tools, agent behavior, conversation flow, database models). It ALWAYS uses Context7 MCP for all doc access/updates.
- **chat-endpoint-developer**: Use this agent when implementing the stateless FastAPI chat endpoint (/api/{user_id}/chat). Handles message reception, conversation history fetch/store from DB, agent invocation with OpenRouter, and response handling. It ALWAYS uses Context7 MCP for all doc access/updates.
- **chatkit-ui-integrator**: Use this agent when integrating OpenAI ChatKit frontend for the AI-powered chatbot project. Handles ChatKit setup, domain allowlist configuration, environment variables, and connecting the chat UI to the backend endpoint. It ALWAYS uses Context7 MCP for all doc access/updates.

## Recent Changes

- 001-frontend-ui: Added TypeScript 5.0+ + Next.js 16+
- 001-frontend-ui: Added Tailwind CSS
- 001-frontend-ui: Added Better Auth
- 001-backend: Added Python 3.13+ + FastAPI 0.115+
- 001-backend: Added SQLModel 0.0.24+ with PostgreSQL 15+
- 001-backend: Added JWT authentication with python-jose and bcrypt password hashing

### Phase III Project Requirements (Todo AI Chatbot)

**Requirements**
Implement conversational interface for all Basic Level features
Use OpenAI Agents SDK for AI logic
Build MCP server with Official MCP SDK that exposes task operations as tools
Stateless chat endpoint that persists conversation state to database
AI agents use MCP tools to manage tasks. The MCP tools will also be stateless and will store state in the database.

**Technology Stack**

Component | Technology
---|---
Frontend | OpenAI ChatKit
Backend | Python FastAPI
AI Framework | OpenAI Agents SDK
MCP Server | Official MCP SDK
ORM | SQLModel
Database | Neon Serverless PostgreSQL
Authentication | Better Auth

**Database Models**

Model | Fields | Description
---|---|---
Task | user_id, id, title, description, completed, created_at, updated_at | Todo items
Conversation | user_id, id, created_at, updated_at | Chat session
Message | user_id, id, conversation_id, role (user/assistant), content, created_at | Chat history

**Chat API Endpoint**

Method | Endpoint | Description
---|---|---
POST | /api/{user_id}/chat | Send message & get AI response

**Request**

Field | Type | Required | Description
---|---|---|---
conversation_id | integer | No | Existing conversation ID (creates new if not provided)
message | string | Yes | User's natural language message

**Response**

Field | Type | Description
---|---|---
conversation_id | integer | The conversation ID
response | string | AI assistant's response
tool_calls | array | List of MCP tools invoked

**MCP Tools Specification**
The MCP server must expose the following tools for the AI agent:

Tool: add_task
Purpose: Create a new task
Parameters: user_id (string, required), title (string, required), description (string, optional)
Returns: task_id, status, title

Tool: list_tasks
Purpose: Retrieve tasks from the list
Parameters: status (string, optional: "all", "pending", "completed")
Returns: Array of task objects

Tool: complete_task
Purpose: Mark a task as complete
Parameters: user_id (string, required), task_id (integer, required)
Returns: task_id, status, title

Tool: delete_task
Purpose: Remove a task from the list
Parameters: user_id (string, required), task_id (integer, required)
Returns: task_id, status, title

Tool: update_task
Purpose: Modify task title or description
Parameters: user_id (string, required), task_id (integer, required), title (string, optional), description (string, optional)
Returns: task_id, status, title

**Agent Behavior Specification**

Behavior | Description
---|---
Task Creation | When user mentions adding/creating/remembering something, use add_task
Task Listing | When user asks to see/show/list tasks, use list_tasks with appropriate filter
Task Completion | When user says done/complete/finished, use complete_task
Task Deletion | When user says delete/remove/cancel, use delete_task
Task Update | When user says change/update/rename, use update_task
Confirmation | Always confirm actions with friendly response
Error Handling | Gracefully handle task not found and other errors

**Conversation Flow (Stateless Request Cycle)**
1. Receive user message
2. Fetch conversation history from database
3. Build message array for agent (history + new message)
4. Store user message in database
5. Run agent with MCP tools
6. Agent invokes appropriate MCP tool(s)
7. Store assistant response in database
8. Return response to client
Server holds NO state (ready for next request)

**Natural Language Commands**
The chatbot should understand and respond to:

User Says | Agent Should
---|---
"Add a task to buy groceries" | Call add_task with title "Buy groceries"
"Show me all my tasks" | Call list_tasks with status "all"
"What's pending?" | Call list_tasks with status "pending"
"Mark task 3 as complete" | Call complete_task with task_id 3
"Delete the meeting task" | Call list_tasks first, then delete_task
"Change task 1 to 'Call mom tonight'" | Call update_task with new title
"I need to remember to pay bills" | Call add_task with title "Pay bills"
"What have I completed?" | Call list_tasks with status "completed"

**OpenAI ChatKit Setup & Deployment**
Domain Allowlist Configuration (Required for Hosted ChatKit)

Before deploying your chatbot frontend, you must configure OpenAI's domain allowlist for security:

- Deploy your frontend first to get a production URL:
  - Vercel: https://your-app.vercel.app
  - GitHub Pages: https://username.github.io/repo-name
  - Custom domain: https://yourdomain.com

- Add your domain to OpenAI's allowlist:
  - Navigate to: https://platform.openai.com/settings/organization/security/domain-allowlist
  - Click "Add domain"
  - Enter your frontend URL (without trailing slash)
  - Save changes

- Get your ChatKit domain key:
  - After adding the domain, OpenAI will provide a domain key
  - Pass this key to your ChatKit configuration

**Environment Variables**
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key-here

Note: The hosted ChatKit option only works after adding the correct domains under Security → Domain Allowlist. Local development (localhost) typically works without this configuration.

## Custom Agents

### Todo API Agent
Description: Core backend agent using FastAPI that handles all task CRUD (create, read, update, delete, complete) operations. Publishes events to Kafka topics via Dapr Pub/Sub: task-events, reminders, task-updates. Uses Dapr for Pub/Sub, State, Service Invocation, and Secrets. Task model includes recurring, due_at, remind_at, priority, and tags fields.
When to use: When implementing core task management functionality, event publishing, or when you need a robust backend service that integrates with Dapr for distributed capabilities.

### Recurring Task Agent
Description: An event-driven agent that listens to the "task-events" topic via Dapr Pub/Sub. When a recurring task is marked as completed, this agent automatically creates the next occurrence of the task and publishes the new task back to the "task-events" topic for further processing.
When to use: When implementing recurring task functionality where completed tasks need to automatically generate future instances based on recurrence rules.

### Notification / Reminder Agent
Description: A Dapr-based agent that listens to the "reminders" topic via Dapr Pub/Sub. It schedules exact-time reminders using Dapr Jobs API and sends notifications (push, email, console) at the designated trigger time to users.
When to use: When implementing reminder systems, scheduled notifications, or time-based alerts that need to be delivered reliably at specific times.

### Audit / Logging Agent
Description: An audit trail agent that listens to the "task-events" topic via Dapr Pub/Sub. It captures and stores a complete log/history of every task operation including timestamps and user information to a database or file storage for compliance and monitoring purposes.
When to use: When implementing audit logging, compliance tracking, or when you need to maintain a complete history of all task operations for debugging and accountability.

### Real-time Sync Agent (WebSocket)
Description: A real-time synchronization agent that listens to the "task-updates" topic via Dapr Pub/Sub. It broadcasts task changes to all connected clients in real-time using WebSocket connections, ensuring all users see updates immediately.
When to use: When implementing real-time collaboration features, live updates, or when users need to see task changes made by others instantly across multiple connected clients.