import { LoginFormValues, SignupFormValues, User } from '../lib/types';

// Authentication service for handling user authentication with custom backend API
class AuthService {
  // Login method
  async login(credentials: LoginFormValues) {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: credentials.email.trim(),
          password: credentials.password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Login failed' }));
        throw new Error(errorData.message || 'Login failed');
      }

      const data = await response.json();

      // Store the token in localStorage
      if (data.access_token) {
        localStorage.setItem('auth_token', data.access_token);
      }

      return data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  // Signup method
  async signup(userData: SignupFormValues) {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: userData.email.trim(),
          password: userData.password,
          name: (userData.name ?? '').trim() || 'User',
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Signup failed' }));
        throw new Error(errorData.message || 'Signup failed');
      }

      const data = await response.json();

      // Store the token in localStorage
      if (data.access_token) {
        localStorage.setItem('auth_token', data.access_token);
      }

      return data;
    } catch (error) {
      console.error('Signup error:', error);
      throw error;
    }
  }

  // Logout method
  async logout() {
    try {
      // Clear the stored token
      localStorage.removeItem('auth_token');
    } catch (error) {
      console.error('Logout error:', error);
      throw error;
    }
  }

  // Get current session/user info
  async getSession(): Promise<User | null> {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        return null;
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const userData = await response.json();
        return userData;
      } else {
        // Token is invalid, clear it
        localStorage.removeItem('auth_token');
        return null;
      }
    } catch (error) {
      console.error('Get session error:', error);
      return null;
    }
  }

  // Get current user
  getCurrentUser() {
    return this.getSession();
  }

  // Get current token
  async getToken(): Promise<string | null> {
    try {
      const token = localStorage.getItem('auth_token');
      return token;
    } catch (error) {
      console.error('Get token error:', error);
      return null;
    }
  }

  // Check if user is authenticated
  async isAuthenticated(): Promise<boolean> {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      return false;
    }

    try {
      // Verify the token by attempting to get user info
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      return response.ok;
    } catch (error) {
      console.error('Auth check error:', error);
      return false;
    }
  }

  // Initialize auth state from stored data
  async initializeAuth() {
    // Nothing needed here since we store token in localStorage
  }

  // Refresh token if needed
  async refreshToken(): Promise<string | null> {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        return null;
      }

      // Verify the token by attempting to get user info
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        return token;
      } else {
        // Token is invalid, clear it
        localStorage.removeItem('auth_token');
        return null;
      }
    } catch (error) {
      console.error('Refresh token error:', error);
      // Clear token if there's an error
      localStorage.removeItem('auth_token');
      return null;
    }
  }
}

// Export a singleton instance
export const authService = new AuthService();

// Export the class for potential extension/instantiation
export default AuthService;