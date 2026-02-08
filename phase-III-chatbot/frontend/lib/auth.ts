import { createAuthClient } from 'better-auth/client';

// Client-side API client for Better Auth
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_FRONTEND_URL || 'http://localhost:3000',
  // We don't need to pass the full server-side auth instance to the client
});

export const auth = { /* This is just for server-side */ };