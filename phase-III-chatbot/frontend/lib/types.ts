// User type definition
export interface User {
  id: string;
  email: string;
  name?: string;
  createdAt: string;
  updatedAt: string;
}

// Task type definition
export interface Task {
  id: string;
  shortId?: number;  // Optional short ID for UI display (1-based index)
  title: string;
  description?: string;
  completed: boolean;
  userId: string;
  createdAt: string;
  updatedAt: string;
}

// Authentication response types
export interface LoginResponse {
  token: string;
  user: User;
}

export interface SignupResponse {
  token: string;
  user: User;
}

export interface ErrorResponse {
  error: string;
  message: string;
}

// Task API response types
export interface TaskListResponse {
  tasks: Task[];
}

export interface TaskSingleResponse {
  task: Task;
}

// Form data types
export interface LoginFormValues {
  email: string;
  password: string;
}

export interface SignupFormValues {
  email: string;
  password: string;
  name?: string;
}

export interface TaskFormValues {
  title: string;
  description?: string;
  completed?: boolean;
}

// API request types
export interface CreateTaskRequest {
  title: string;
  description?: string;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}