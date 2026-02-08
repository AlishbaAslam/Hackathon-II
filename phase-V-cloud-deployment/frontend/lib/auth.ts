// Client-side auth utilities
// Using custom auth system with backend API calls instead of Better Auth

export const authClient = {
  // Placeholder to avoid breaking existing references
  getSession: async () => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      try {
        // Try to verify token with backend
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/auth/me`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const userData = await response.json();
          return {
            data: {
              user: userData
            }
          };
        }
      } catch (error) {
        console.error('Error getting session:', error);
      }
    }

    return { data: null };
  }
};

export const auth = { /* This is just for server-side */ };