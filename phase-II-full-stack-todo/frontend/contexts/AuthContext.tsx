'use client';

import { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import { authClient } from '../lib/auth';
import { User } from '../lib/types';

// Define the authentication context type
interface AuthContextType {
  user: any | null; // Better Auth user type
  readonly token: string | null;
  readonly isAuthenticated: boolean;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, name?: string) => Promise<void>;
  logout: () => void;
  initializeAuth: () => void;
  refreshAuth: () => void;
}

// Create the authentication context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Auth provider component
export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<any | null>(null); // Better Auth user type
  const [loading, setLoading] = useState(true);

  // Initialize authentication state
  useEffect(() => {
    initializeAuth();
  }, []);

  // Initialize auth state from stored data
  const initializeAuth = async () => {
    setLoading(true);
    try {
      // Try to get user from stored token
      const token = localStorage.getItem('auth_token');
      if (token) {
        // We could make a call to verify the token and get user info
        // For now, we'll just set a placeholder and the user can be fetched when needed
        // Or we can decode the JWT to get user info if needed
        try {
          // Simple JWT token decoding to extract user info if needed
          // For now, we'll just indicate that there's a token
          // In a real implementation, you might want to validate the token with the backend
        } catch (e) {
          // If token is invalid, clear it
          localStorage.removeItem('auth_token');
        }
      }
    } catch (error) {
      console.error('Error initializing auth:', error);
    } finally {
      setLoading(false);
    }
  };

  // Login function - now using backend's auth system instead of Better Auth
  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      // Use the backend's auth system instead of Better Auth
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Login failed' }));
        throw new Error(errorData.message || 'Login failed');
      }

      const data = await response.json();

      // Store the token in localStorage or session storage
      if (data.access_token) {
        localStorage.setItem('auth_token', data.access_token);
      }

      // Set user data from the response
      if (data.user) {
        setUser(data.user);
      }

      return data;
    } catch (error) {
      setLoading(false);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  // Signup function - now using backend's auth system instead of Better Auth
  const signup = async (email: string, password: string, name?: string) => {
    setLoading(true);
    try {
      // Use the backend's auth system instead of Better Auth
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Signup failed' }));
        throw new Error(errorData.message || 'Signup failed');
      }

      const data = await response.json();

      // Store the token in localStorage or session storage
      if (data.access_token) {
        localStorage.setItem('auth_token', data.access_token);
      }

      // Set user data from the response
      if (data.user) {
        setUser(data.user);
      }

      return data;
    } catch (error) {
      setLoading(false);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  // Logout function
  const logout = async () => {
    try {
      // Clear the stored token
      localStorage.removeItem('auth_token');
      setUser(null);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  // Force refresh auth state
  const refreshAuth = async () => {
    try {
      const result = await authClient.getSession();
      const session = 'data' in result ? result.data : null;

      if (session?.user) {
        setUser(session.user);
      } else {
        setUser(null);
      }
    } catch (error) {
      console.error('Refresh auth error:', error);
    }
  };

  // Provide context value
  const value = {
    user,
    get token() {
      // Get token from localStorage
      return localStorage.getItem('auth_token');
    },
    get isAuthenticated() {
      return !!user;
    },
    loading,
    login,
    signup,
    logout,
    initializeAuth,
    refreshAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use auth context
export const useAuthContext = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuthContext must be used within an AuthProvider');
  }
  return context;
};