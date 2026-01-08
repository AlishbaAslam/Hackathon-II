import { useAuthContext } from '../contexts/AuthContext';

// Custom hook to use auth context
export const useAuth = () => {
  return useAuthContext();
};