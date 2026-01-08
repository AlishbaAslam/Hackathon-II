# Hackathon II – Todo App (Phase I + Phase II)

This repository contains an **evolutionary todo project** built using **Spec-Driven Development (SDD)** (Spec‑Kit Plus). It includes:

- **Phase I (Completed / Frozen):** a Python **CLI** todo application with **in-memory storage**.
- **Phase II (Completed):** a **full-stack web application** with a Next.js frontend and FastAPI backend, using JWT authentication and a relational database.

This README documents the project purpose, key features, folder structure, and setup/usage information for both phases.

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
- Tailwind CSS responsive UI (target: 320px–1920px)
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

---

## Folder Structure

Top-level:

```
.
├── console/                   # Phase I: Python CLI todo app
├── phase-II-full-stack-todo/  # Phase II: full-stack web app
│   ├── backend/               # FastAPI + SQLModel API
│   └── frontend/              # Next.js 16 UI
├── specs/                     # Specifications (backend + UI, plus history)
├── history/                   # Prompt History Records (PHR)
├── console/README.md          # Phase I usage details
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
│   └── README.md
└── frontend/
    ├── app/                     # Next.js App Router pages/layouts
    ├── components/
    ├── contexts/
    ├── hooks/
    ├── lib/                     # Central API client + shared types
    ├── services/
    ├── package.json
    └── README.md
```

---

## Setup & Usage

### Prerequisites

- **Phase I**: Python 3.13+ and `uv`
- **Phase II backend**: Python 3.12+ (per `phase-II-full-stack-todo/backend/pyproject.toml`) and `uv`
- **Phase II frontend**: Node.js + npm
- Optional for Phase II: PostgreSQL (or Neon); backend defaults to SQLite if not configured

> Note: the repository uses separate `pyproject.toml` / dependency graphs for Phase I vs Phase II.

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

Common variables (see `phase-II-full-stack-todo/backend/src/config.py`):

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

## Important Notes (from the Project Constitution)

- **Spec-Driven Development is mandatory**: changes should be made via specs first, then implemented.
- **Progressive evolution**: phases should not be skipped; Phase I is completed/frozen.
- **Security**: no hardcoded secrets; authentication and user isolation are required for web phases.
- **Correctness and predictability**: task lifecycle should behave deterministically; edge cases should be handled gracefully.
- **Maintainability**: keep code modular with clear responsibilities (avoid duplicate logic).

---

## Development Workflow (Spec‑Kit Plus)

If you’re using Claude Code with this repo, follow:

1. `/sp.specify` – update/create feature spec
2. `/sp.plan` – create implementation plan
3. `/sp.tasks` – generate task breakdown
4. `/sp.implement` – implement from approved specs

See `CLAUDE.md` for repo-specific guidance.
