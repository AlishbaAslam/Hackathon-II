# Quickstart Guide: Frontend UI for Todo Web Application

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Access to the backend API (FastAPI server)
- Better Auth configured for authentication

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Environment configuration**
   Create a `.env.local` file in the frontend root:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
   ```

4. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. **Access the application**
   Open [http://localhost:3000](http://localhost:3000) in your browser

## Key Components

### Authentication Components
- `LoginForm` - Handles user login with email/password
- `SignupForm` - Handles user registration
- `AuthWrapper` - Protects routes requiring authentication

### Task Components
- `TaskList` - Displays all tasks with filtering options
- `TaskItem` - Individual task with completion toggle
- `TaskForm` - Create/edit task functionality
- `TaskActions` - Delete and other task-specific actions

### Layout Components
- `Header` - Navigation and user profile
- `Sidebar` - Application navigation
- `Footer` - Additional links and information

## API Integration

The application uses a centralized API client located in `lib/api.ts` that:
- Attaches JWT tokens to all authenticated requests
- Handles common error responses
- Provides consistent request/response patterns

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL` - Base URL for the backend API
- `NEXT_PUBLIC_BETTER_AUTH_URL` - Base URL for authentication endpoints
- `NEXT_PUBLIC_JWT_SECRET` - Secret for JWT verification (if needed client-side)

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run code linting
- `npm run test` - Run unit tests