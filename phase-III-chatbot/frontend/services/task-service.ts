import { Task, CreateTaskRequest, UpdateTaskRequest, TaskListResponse, TaskSingleResponse } from '../lib/types';
import { apiClient } from '../lib/api';

// Task service for handling task operations
class TaskService {
  // Get all tasks for a user
  async getTasks(userId: string): Promise<Task[]> {
    try {
      // Get the token from localStorage - check if window is available
      let token;
      if (typeof window !== 'undefined') {
        token = localStorage.getItem('auth_token');
      }

      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await apiClient.getTasks(userId, token);
      return response.tasks;
    } catch (error) {
      console.error('Error getting tasks:', error);
      throw error;
    }
  }

  // Create a new task
  async createTask(userId: string, taskData: CreateTaskRequest): Promise<Task> {
    try {
      // Get the token from localStorage - check if window is available
      let token;
      if (typeof window !== 'undefined') {
        token = localStorage.getItem('auth_token');
      }

      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await apiClient.createTask(userId, taskData, token);
      return response;
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  }

  // Update an existing task
  async updateTask(userId: string, taskId: string, taskData: UpdateTaskRequest): Promise<Task> {
    try {
      // Get the token from localStorage - check if window is available
      let token;
      if (typeof window !== 'undefined') {
        token = localStorage.getItem('auth_token');
      }

      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await apiClient.updateTask(userId, taskId, taskData, token);
      return response;
    } catch (error) {
      console.error('Error updating task:', error);
      throw error;
    }
  }

  // Toggle task completion status
  async toggleTaskCompletion(userId: string, taskId: string, completed: boolean): Promise<Task> {
    try {
      // Get the token from localStorage - check if window is available
      let token;
      if (typeof window !== 'undefined') {
        token = localStorage.getItem('auth_token');
      }

      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await apiClient.toggleTaskCompletion(userId, taskId, completed, token);
      return response;
    } catch (error) {
      console.error('Error toggling task completion:', error);
      throw error;
    }
  }

  // Delete a task
  async deleteTask(userId: string, taskId: string): Promise<void> {
    try {
      // Get the token from localStorage - check if window is available
      let token;
      if (typeof window !== 'undefined') {
        token = localStorage.getItem('auth_token');
      }

      if (!token) {
        throw new Error('No authentication token found');
      }

      await apiClient.deleteTask(userId, taskId, token);
    } catch (error) {
      console.error('Error deleting task:', error);
      throw error;
    }
  }

  // Update task title and description
  async updateTaskDetails(
    userId: string,
    taskId: string,
    title: string,
    description?: string
  ): Promise<Task> {
    return this.updateTask(userId, taskId, { title, description });
  }

  // Mark task as complete
  async markTaskComplete(userId: string, taskId: string): Promise<Task> {
    return this.toggleTaskCompletion(userId, taskId, true);
  }

  // Mark task as incomplete
  async markTaskIncomplete(userId: string, taskId: string): Promise<Task> {
    return this.toggleTaskCompletion(userId, taskId, false);
  }
}

// Export a singleton instance
export const taskService = new TaskService();

// Export the class for potential extension/instantiation
export default TaskService;