# Phase-II Full-Stack Todo Application

A modern, responsive todo application built with Next.js 16+, TypeScript, and Tailwind CSS. This application features user authentication, task management, and a clean, accessible UI.

## Features

- **User Authentication**: Secure login and signup with JWT tokens
- **Task Management**: Create, read, update, and delete tasks
- **Task Status**: Mark tasks as complete/incomplete
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Accessibility**: WCAG 2.1 AA compliant
- **Type Safety**: Full TypeScript support

## Tech Stack

- **Frontend**: Next.js 16+, React 18
- **Styling**: Tailwind CSS
- **UI Components**: Headless UI, Heroicons
- **Type Safety**: TypeScript
- **Authentication**: Better Auth (simulated)
- **API Communication**: Custom API client with JWT support

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

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

## Environment Variables

Create a `.env.local` file in the root directory:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run code linting

## API Integration

The application is designed to work with a backend API that follows these endpoints:

- Authentication: `/api/auth/login`, `/api/auth/signup`
- Tasks: `/api/users/{user_id}/tasks`, `/api/tasks/{task_id}`, `/api/tasks/{task_id}/complete`

## Testing

This application follows a test-driven approach. Unit and integration tests can be added in the `__tests__` directory.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request