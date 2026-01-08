import { LoginFormValues, SignupFormValues } from '../lib/types';
import { authClient } from '../lib/auth';

// Authentication service for handling user authentication with Better Auth
class AuthService {
  // Login method
  async login(credentials: LoginFormValues) {
    try {
      const response = await authClient.signIn.email({
        email: credentials.email,
        password: credentials.password,
        callbackURL: '/dashboard', // Redirect after successful login
      });
      return response;
    } catch (error) {
      throw error;
    }
  }

  // Signup method
  async signup(userData: SignupFormValues) {
    try {
      const response = await authClient.signUp.email({
        email: userData.email,
        password: userData.password,
        name: userData.name,
        callbackURL: '/dashboard', // Redirect after successful signup
      });
      return response;
    } catch (error) {
      throw error;
    }
  }

  // Logout method
  async logout() {
    try {
      await authClient.signOut();
    } catch (error) {
      console.error('Logout error:', error);
      throw error;
    }
  }

  // Get current session
  async getSession() {
    try {
      const session = await authClient.getSession();
      return session;
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
      const session = await authClient.getSession();
      if (session?.session) {
        // Better Auth provides JWT token through session
        return session.session.token;
      }
      return null;
    } catch (error) {
      console.error('Get token error:', error);
      return null;
    }
  }

  // Check if user is authenticated
  async isAuthenticated(): Promise<boolean> {
    const session = await this.getSession();
    return session !== null && session.session !== null;
  }

  // Initialize auth state from stored data
  async initializeAuth() {
    // Better Auth handles session persistence automatically
    // No additional initialization needed
  }

  // Refresh token if needed
  async refreshToken(): Promise<string | null> {
    try {
      const session = await authClient.getSession();
      if (session?.session) {
        return session.session.token;
      }
      return null;
    } catch (error) {
      console.error('Refresh token error:', error);
      return null;
    }
  }
}

// Export a singleton instance
export const authService = new AuthService();

// Export the class for potential extension/instantiation
export default AuthService;