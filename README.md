# Hackathon II – Todo App (Phase I + Phase II + Phase III)

This repository contains an **evolutionary todo project** built using **Spec-Driven Development (SDD)** (Spec‑Kit Plus). It includes:

- **Phase I (Completed / Frozen):** a Python **CLI** todo application with **in-memory storage**.
- **Phase II (Completed):** a **full-stack web application** with a Next.js frontend and FastAPI backend, using JWT authentication and a relational database.
- **Phase III (Completed):** an **AI-powered chatbot** with natural language processing using OpenAI Agents SDK and MCP tools for task management.

This README documents the project purpose, key features, folder structure, and setup/usage information for all three phases.

---

## Purpose

Build a todo system that evolves in clearly-scoped phases while staying **predictable**, **maintainable**, and **spec-driven**.

Per the project constitution (`.specify/memory/constitution.md`):

- All implementation should trace back to approved specifications.
- Phases progress sequentially (**CLI → Web → Cloud Native AI**, etc.).
- **Security and user isolation** are mandatory for authenticated phases.

---

## Key Features

### Phase I — Console (CLI)

Located in `console/`.

- **Core CRUD**: add, view, update, delete tasks
- **Completion**: mark complete/incomplete
- **Search & filter**: keyword search, status, priority, tags
- **Sorting**: due date, priority, alphabetical
- **Rich metadata**: description, priority, tags, due dates/times, recurrence
- **Recurring tasks**: daily / weekly / monthly recurrence with next-instance generation
- **Overdue handling**: detection + auto/batch rescheduling
- **Notifications**: background imminent-deadline alerts (console)
- **Storage**: **in-memory only** (no DB/files) — constitution Phase I scope

### Phase II — Full-Stack Web App

Located in `phase-II-full-stack-todo/`.

#### Frontend (Next.js)

- Next.js 16 **App Router** + React + TypeScript
- Tailwind CSS responsive UI
- Authentication UI (login/signup) and auth state management
- Task CRUD UI with loading/empty/error states
- Centralized API client that attaches JWT bearer tokens

#### Backend (FastAPI)

- FastAPI + SQLModel
- **JWT authentication** (stateless)
- **User isolation**: all task operations are scoped to the authenticated user
- Task CRUD endpoints (user-scoped routes)
- Pagination with limit/offset
- Interactive docs: Swagger (`/docs`) + ReDoc (`/redoc`)

### Phase III — AI-Powered Chatbot

Located in `phase-II-full-stack-todo/` with integrated AI functionality.

#### AI Chatbot Features

- **Natural Language Processing**: Interact with your todo list using natural language
- **OpenAI Agents SDK**: Powered by AI agents that understand task commands
- **MCP Tools**: Managed Control Plane tools for secure task operations
- **Conversational Interface**: Add, update, delete, and manage tasks through chat
- **State Management**: Conversation persistence in database
- **User Isolation**: All AI operations respect user boundaries

#### Supported Natural Language Commands

- "Add a task to buy groceries" → Creates new task
- "Show me all my tasks" → Lists all tasks
- "What's pending?" → Lists pending tasks
- "Mark task 3 as complete" → Marks task as complete
- "Delete the meeting task" → Deletes specified task
- "Change task 1 to 'Call mom tonight'" → Updates task
- "What have I completed?" → Lists completed tasks

#### MCP Tools Specification

- **add_task**: Create a new task with title and description
- **list_tasks**: Retrieve tasks with optional status filter
- **complete_task**: Mark a task as complete
- **delete_task**: Remove a task from the list
- **update_task**: Modify task title or description

---

## Tech Stack

### Phase I (CLI)
- **Language**: Python 3.13+
- **Package Manager**: uv
- **Storage**: In-memory (no database)

### Phase II (Full-Stack Web)
#### Backend
- **Framework**: FastAPI 0.115+
- **Database**: PostgreSQL 15+ (Neon DB compatible)
- **ORM**: SQLModel 0.0.24+
- **Authentication**: JWT via python-jose
- **Password Hashing**: bcrypt via passlib
- **Testing**: pytest 8.0+
- **Package Manager**: uv

#### Frontend
- **Framework**: Next.js 16+, React 18
- **Styling**: Tailwind CSS
- **UI Components**: Headless UI, Heroicons
- **Type Safety**: TypeScript
- **Authentication**: Better Auth
- **API Communication**: Custom API client with JWT support

### Phase III (AI Chatbot)
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK
- **Backend**: Python FastAPI
- **Frontend**: OpenAI ChatKit
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT

---

## Folder Structure

Top-level:

```
.
├── console/                   # Phase I: Python CLI todo app
├── phase-II-full-stack-todo/  # Phase II: full-stack web app + Phase III: AI features
│   ├── backend/               # FastAPI + SQLModel API + MCP tools + AI endpoints
│   │   ├── src/
│   │   │   ├── main.py              # App entrypoint (CORS, routers, handlers)
│   │   │   ├── config.py            # Env-based settings
│   │   │   ├── models/              # SQLModel entities + Conversation/Message models
│   │   │   ├── routers/             # auth + tasks + chat endpoints
│   │   │   ├── services/            # business logic + agent service + conversation service
│   │   │   ├── mcp_tools/           # MCP tools for AI agent interaction
│   │   │   └── core/                # DB/session, dependencies, security
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   ├── CLAUDE.md                # Claude Code repo instructions
│   │   └── README.md
│   └── frontend/              # Next.js 16 UI + ChatKit integration
│       ├── app/               # Next.js App Router pages/layouts
│       ├── components/        # Reusable UI components
│       ├── lib/               # Shared utilities and API functions
│       ├── services/          # API service layer
│       ├── hooks/             # Custom React hooks
│       ├── chat/              # AI chatbot UI components
│       ├── public/            # Static assets
│       ├── package.json
│       ├── CLAUDE.md          # Claude Code repo instructions
│       └── README.md
├── specs/                     # Specifications (backend + UI + chatbot, plus history)
├── history/                   # Prompt History Records (PHR)
├── README.md                  # Phase I, II and III usage details
├── CLAUDE.md                  # Claude Code repo instructions
└── .specify/memory/constitution.md  # Project constitution (governance)
```

### Phase I (console) structure

```
console/
├── src/
│   ├── main.py          # Entry point
│   ├── cli.py           # Console menus + input handling
│   ├── todo_service.py  # Business logic (CRUD, recurrence, scheduling)
│   └── models.py        # Task model + enums
├── tests/
├── pyproject.toml
└── README.md
```

### Phase II (full-stack) structure

```
phase-II-full-stack-todo/
├── backend/
│   ├── src/
│   │   ├── main.py              # App entrypoint (CORS, routers, handlers)
│   │   ├── config.py            # Env-based settings
│   │   ├── core/                # DB/session, dependencies, security
│   │   ├── models/              # SQLModel entities
│   │   ├── routers/             # auth + tasks endpoints
│   │   └── services/            # business logic
│   ├── tests/
│   ├── pyproject.toml
│   ├── CLAUDE.md                # Claude Code repo instructions
│   └── README.md
└── frontend/
    ├── app/                     # Next.js App Router pages/layouts
    ├── components/
    ├── contexts/
    ├── hooks/
    ├── lib/                     # Central API client + shared types
    ├── services/
    ├── package.json
    ├── CLAUDE.md                # Claude Code repo instructions
    └── README.md
```

### Phase III (AI Chatbot) additions

```
phase-II-full-stack-todo/
├── backend/
│   ├── src/
│   │   ├── models/
│   │   │   ├── conversation.py  # Conversation entity
│   │   │   └── message.py       # Message entity
│   │   ├── routers/
│   │   │   └── chat.py          # Chat endpoint
│   │   ├── services/
│   │   │   ├── agent_service.py      # AI agent logic
│   │   │   ├── conversation_service.py # Conversation management
│   │   │   └── conversation_service_async.py # Async conversation management
│   │   ├── mcp_tools/           # MCP tools for AI interaction
│   │   │   └── task_mcp_tools.py # Task-related MCP tools
│   │   └── services/
│   │       └── openrouter_client.py # OpenRouter integration
├── specs/
│   └── phase-III-chatbot/       # Chatbot specifications
│       ├── overview.md
│       ├── features/
│       ├── api/
│       ├── database/
│       ├── mcp-tools.md
│       └── agent-behavior.md
└── frontend/
    ├── components/
    │   └── chat/                # Chat UI components
    └── hooks/
        └── useChat.ts           # Chat hook
```

---

## Setup & Usage

### Prerequisites

- **Phase I**: Python 3.13+ and `uv`
- **Phase II backend**: Python 3.12+ (per `phase-II-full-stack-todo/backend/pyproject.toml`) and `uv`
- **Phase II frontend**: Node.js + npm
- **Phase III**: Python 3.13+, Node.js, and OpenAI account for OpenRouter

---

## Phase I — Run the Console App

```bash
cd console
uv sync
uv run python -m src.main
```

See `console/README.md` for full CLI usage.

---

## Phase II — Run the Backend (FastAPI)

```bash
cd phase-II-full-stack-todo/backend
uv sync
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Backend configuration (env vars)

The backend loads environment variables from a local `.env` file (if present). Defaults exist, but for JWT auth you should set a strong secret.

Backend URLs:

- `http://localhost:8000/health`
- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

Run backend tests:

```bash
pytest
```

---

## Phase II — Run the Frontend (Next.js)

```bash
cd phase-II-full-stack-todo/frontend
npm install
```

Create `phase-II-full-stack-todo/frontend/.env.local`:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Then:

```bash
npm run dev
```

Open `http://localhost:3000`.

---

## Phase III — Run the AI Chatbot

### Backend Setup for Chatbot

First, set up the backend with chatbot capabilities:

```bash
cd phase-II-full-stack-todo/backend
uv sync
uv run python -m src.services.agent_service  # Initialize agent
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Environment Variables for AI Features

Create or update `.env` in the backend directory:

### Frontend Setup for Chatbot UI

The chatbot UI integrates with OpenAI ChatKit. To configure:

1. Deploy your frontend to get a production URL
2. Add your domain to OpenAI's domain allowlist at https://platform.openai.com/settings/organization/security/domain-allowlist
3. Set the environment variable in your frontend `.env.local`:

```env
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key-here
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Chat API Endpoint

The chatbot uses a stateless endpoint that persists conversation state to the database:

**Endpoint**: `POST /api/{user_id}/chat`

**Request**:
```json
{
  "conversation_id": 123,
  "message": "Add a task to buy groceries"
}
```

**Response**:
```json
{
  "conversation_id": 123,
  "response": "I've added the task 'buy groceries' to your list.",
  "tool_calls": [{"name": "add_task", "arguments": {"title": "buy groceries"}}]
}
```

---

## Important Notes (from the Project Constitution)

- **Spec-Driven Development is mandatory**: changes should be made via specs first, then implemented.
- **Progressive evolution**: phases should not be skipped; Phase I is completed/frozen.
- **Security**: no hardcoded secrets; authentication and user isolation are required for web phases.
- **Correctness and predictability**: task lifecycle should behave deterministically; edge cases should be handled gracefully.
- **Maintainability**: keep code modular with clear responsibilities (avoid duplicate logic).

---

## Development Workflow (Spec‑Kit Plus)

If you're using Claude Code with this repo, follow:

1. `/sp.specify` – update/create feature spec
2. `/sp.plan` – create implementation plan
3. `/sp.tasks` – generate task breakdown
4. `/sp.implement` – implement from approved specs

For Phase III development:
1. `/chatbot-spec-writer` – create chatbot specifications
2. `/mcp-tool-designer` – design MCP tools
3. `/chat-endpoint-builder` – implement chat endpoints
4. `/ai-agent-logic` – configure AI agent behavior

See `CLAUDE.md` for repo-specific guidance.