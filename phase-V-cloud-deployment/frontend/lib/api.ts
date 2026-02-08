import { Task, User, LoginResponse, SignupResponse, TaskListResponse, TaskSingleResponse, ErrorResponse, CreateTaskRequest, UpdateTaskRequest } from './types';

// Base API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// API client class for centralized API communication
class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  // Helper method to get auth headers - now accepts token parameter
  private getAuthHeaders(token?: string) {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  // Helper method to make API requests - now accepts token parameter
  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
    token?: string
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const config: RequestInit = {
      ...options,
      headers: {
        ...this.getAuthHeaders(token),
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorResponse: ErrorResponse = {
          error: `HTTP ${response.status}`,
          message: errorData.message || response.statusText,
        };
        throw errorResponse;
      }

      // For 204 No Content responses, return null
      if (response.status === 204) {
        return null as T;
      }

      return await response.json();
    } catch (error) {
      if (error instanceof TypeError) {
        // Network error
        throw {
          error: 'Network Error',
          message: 'Unable to connect to the server. Please check your connection.',
        } as ErrorResponse;
      }
      throw error;
    }
  }

  // Authentication methods
  async login(email: string, password: string): Promise<LoginResponse> {
    return this.request<LoginResponse>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async signup(email: string, password: string, name?: string): Promise<SignupResponse> {
    return this.request<SignupResponse>('/api/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password, name }),
    });
  }

  // Task methods - now accept token parameter to match compiled version
  async getTasks(userId: string, token: string): Promise<TaskListResponse> {
    const response = await this.request<any>(`/api/${userId}/tasks`, {
      method: 'GET',
    }, token);
    // Map the response to handle snake_case to camelCase
    return {
      tasks: response.tasks.map((task: any) => this.mapTaskResponse(task))
    };
  }

  async createTask(userId: string, taskData: CreateTaskRequest, token: string): Promise<Task> {
    // Backend returns task directly, not wrapped in {task: ...}
    // The backend should handle field aliasing automatically
    const response = await this.request<any>(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(taskData),
    }, token);
    return this.mapTaskResponse(response);
  }

  async updateTask(userId: string, taskId: string, taskData: UpdateTaskRequest, token: string): Promise<Task> {
    // Backend returns task directly, not wrapped in {task: ...}
    // The backend should handle field aliasing automatically
    const response = await this.request<any>(`/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    }, token);
    return this.mapTaskResponse(response);
  }

  async toggleTaskCompletion(userId: string, taskId: string, completed: boolean, token: string): Promise<Task> {
    // Backend returns task directly, not wrapped in {task: ...}
    const response = await this.request<any>(`/api/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
      body: JSON.stringify({ completed }),
    }, token);
    return this.mapTaskResponse(response);
  }

  // Helper to map backend response to frontend Task type
  // Backend uses snake_case, frontend uses camelCase
  private mapTaskResponse(response: any): Task {
    console.log('Mapping task response:', response); // Debug log
    console.log('Raw due_date from backend:', response.due_date); // Debug log for due_date specifically

    // Handle the due_date field - backend returns it as due_date (snake_case)
    let dueDateValue: string | undefined;
    console.log('Checking for due_date in response:', response); // Additional debug
    if (response.due_date !== undefined && response.due_date !== null) {
      console.log('Found due_date in response:', response.due_date); // Additional debug
      // If backend returns due_date as string, convert it to proper format
      dueDateValue = typeof response.due_date === 'string' ? response.due_date :
                     response.due_date instanceof Date ? response.due_date.toISOString() :
                     response.due_date ? new Date(response.due_date).toISOString() : undefined;
    } else if (response.dueDate) {
      console.log('Found dueDate in response (fallback):', response.dueDate); // Additional debug
      // Fallback for camelCase
      dueDateValue = response.dueDate;
    } else {
      console.log('No due date found in response'); // Additional debug
    }

    const mappedTask: Task = {
      id: response.id,
      title: response.title,
      description: response.description,
      completed: response.is_completed,
      userId: response.user_id,
      createdAt: response.created_at,
      updatedAt: response.updated_at,
      dueDate: dueDateValue,
      priority: response.priority,
      tags: response.tags,
      isRecurring: response.is_recurring,
      recurrencePattern: response.recurrence_pattern,
      remindAt: response.remind_at,
      parentTaskId: response.parent_task_id
    };

    console.log('Mapped dueDate for task', response.id, ':', mappedTask.dueDate, 'from raw', response.due_date); // Debug log
    return mappedTask;
  }

  async deleteTask(userId: string, taskId: string, token: string): Promise<void> {
    await this.request<void>(`/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    }, token);
  }

  // Chat methods
  async chat(userId: string, message: string, token: string, conversationId?: number): Promise<{conversation_id: number, response: string, tool_calls: any[]}> {
    const requestBody: {message: string, conversation_id?: number} = {
      message: message
    };

    if (conversationId) {
      requestBody.conversation_id = conversationId;
    }

    return this.request<{conversation_id: number, response: string, tool_calls: any[]}>(`/api/${userId}/chat`, {
      method: 'POST',
      body: JSON.stringify(requestBody),
    }, token);
  }
}

// Export a singleton instance
export const apiClient = new ApiClient();

// Export the class for potential extension/instantiation
export default ApiClient;