# Frontend (Next.js) — CLAUDE.md

This folder contains the **Phase II web frontend** for the Todo app. It is a **Next.js 16 (App Router) + React 18 + TypeScript** application styled with **Tailwind CSS**, and it communicates with the FastAPI backend via a centralized API client.

## Purpose

- Provide the user-facing UI for authentication and task management
- Enforce a clean separation between UI components, hooks, and API/service logic
- Attach JWT tokens to authenticated API requests
- Deliver a responsive, accessible experience (target: WCAG 2.1 AA)

## Key features

- **Authentication UI**: signup + login screens and auth state management
- **Task CRUD UI**: create, view, edit, delete tasks
- **Completion state**: mark tasks complete/incomplete
- **Consistent UX states**: loading, empty, and error handling patterns
- **API integration**: centralized client and typed request/response models

## Tech stack

- **Next.js**: 16.x (App Router)
- **React**: 18.x
- **TypeScript**: 5.x
- **Styling**: Tailwind CSS
- **UI helpers**: Headless UI, Heroicons
- **Animations**: Framer Motion
- **Auth**: Better Auth (client-side integration) with JWT-bearing API calls

## High-level architecture

- `app/` is the entrypoint using **Next.js App Router**.
  - Server Components are the default.
  - Client Components are used where interactivity/state is required (`'use client'`).
- `services/` owns network calls (task + auth services).
- `lib/` owns shared types and the centralized API client.
- `hooks/` provides React hooks that bridge UI components to services.
- `components/` contains reusable UI and feature components.

## Directory structure

```
frontend/
├── app/                      # Next.js App Router pages and layouts
│   ├── (auth)/               # Authentication routes (login/signup)
│   ├── dashboard/            # Authenticated landing area
│   ├── tasks/                # Task management route(s)
│   ├── layout.tsx            # Root layout
│   ├── page.tsx              # Landing page
│   ├── globals.css           # Global styles (Tailwind base)
│   ├── error.tsx             # App-level error boundary UI
│   └── not-found.tsx         # 404 UI
├── components/
│   ├── auth/                 # LoginForm, SignupForm, etc.
│   ├── tasks/                # TaskList, TaskItem, modals/dialogs
│   └── ui/                   # Shared UI primitives (Button, Input, Modal, Toast)
├── contexts/                 # React contexts (e.g., AuthContext)
├── hooks/                    # Custom hooks (useAuth, useTasks)
├── lib/                      # Shared utilities (api client, auth helpers, types)
├── services/                 # API/service layer (auth-service, task-service)
├── public/                   # Static assets
├── next.config.mjs           # Next.js config
├── tailwind.config.ts        # Tailwind configuration
├── tsconfig.json             # TypeScript configuration
└── package.json              # Frontend scripts and dependencies
```

## Important files

- `lib/api.ts`: Central API client; responsible for base URL, headers, and JWT attachment.
- `contexts/AuthContext.tsx`: Frontend auth state (current user/token) and helpers.
- `services/*`: Backend-facing calls for authentication and tasks.
- `lib/types.ts`: Shared TypeScript types for task/auth data.

## Environment variables

The frontend expects a backend base URL via a public env var.

Create a `.env.local` file in this `frontend/` directory:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Common commands

From this folder:

- `npm install`
- `npm run dev`
- `npm run build`
- `npm run start`
- `npm run lint`

## Conventions (project-specific)

- Keep API calls centralized (prefer `lib/api.ts` + `services/*`).
- Avoid inline styles; use Tailwind utility classes.
- Add `'use client'` only when needed.
- Handle loading/empty/error states in UI components.
- Do not store secrets in this repo; use `.env.local` for local config.
