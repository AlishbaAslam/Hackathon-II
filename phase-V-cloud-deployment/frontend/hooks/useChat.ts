import { useState, useCallback } from 'react';
import { apiClient } from '@/lib/api';
import { useAuth } from './useAuth';

interface Message {
  id?: number;
  role: 'user' | 'assistant';
  content: string;
  createdAt?: string;
}

interface UseChatOptions {
  userId?: string;
  initialMessages?: Message[];
}

interface UseChatResult {
  messages: Message[];
  sendMessage: (message: string) => Promise<void>;
  isLoading: boolean;
  error: string | null;
  clearMessages: () => void;
}

const useChat = (options: UseChatOptions = {}): UseChatResult => {
  const { userId: providedUserId, initialMessages = [] } = options;
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();

  const sendMessage = useCallback(async (message: string) => {
    if (!message.trim()) {
      setError('Message cannot be empty');
      return;
    }

    const currentUserId = providedUserId || user?.id;
    if (!currentUserId) {
      setError('User not authenticated');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Add user message to UI immediately
      const userMessage: Message = {
        role: 'user',
        content: message,
      };

      setMessages(prev => [...prev, userMessage]);

      // Send message to backend
      const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;
      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await apiClient.chat(currentUserId, message, token);

      // Add assistant response to messages
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.response,
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Failed to send message. Please try again.');

      // Add error message to chat
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [providedUserId, user?.id]);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return {
    messages,
    sendMessage,
    isLoading,
    error,
    clearMessages,
  };
};

export default useChat;