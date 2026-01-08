import { useState, useEffect, useCallback } from 'react';
import { Task, CreateTaskRequest, UpdateTaskRequest } from '../lib/types';
import { taskService } from '../services/task-service';
import { useAuth } from './useAuth';

// Define the tasks context type
interface TasksContextType {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  fetchTasks: () => Promise<void>;
  createTask: (taskData: CreateTaskRequest) => Promise<Task>;
  updateTask: (taskId: string, taskData: UpdateTaskRequest) => Promise<Task>;
  toggleTaskCompletion: (taskId: string, completed: boolean) => Promise<Task>;
  deleteTask: (taskId: string) => Promise<void>;
  markTaskComplete: (taskId: string) => Promise<Task>;
  markTaskIncomplete: (taskId: string) => Promise<Task>;
}

// Custom hook for managing tasks
export const useTasks = (): TasksContextType => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Get auth context to access user and token
  const { user, isAuthenticated } = useAuth();

  // Fetch tasks for the current user
  const fetchTasks = useCallback(async () => {
    if (!isAuthenticated || !user) {
      setTasks([]);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const userTasks = await taskService.getTasks(user.id);
      setTasks(userTasks);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch tasks');
      setTasks([]);
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated, user]);

  // Create a new task
  const createTask = async (taskData: CreateTaskRequest): Promise<Task> => {
    if (!isAuthenticated || !user) {
      throw new Error('User not authenticated');
    }

    try {
      const newTask = await taskService.createTask(user.id, taskData);
      setTasks(prev => [...prev, newTask]);
      return newTask;
    } catch (err: any) {
      setError(err.message || 'Failed to create task');
      throw err;
    }
  };

  // Update an existing task
  const updateTask = async (taskId: string, taskData: UpdateTaskRequest): Promise<Task> => {
    if (!isAuthenticated || !user) {
      throw new Error('User not authenticated');
    }

    try {
      const updatedTask = await taskService.updateTask(user.id, taskId, taskData);
      setTasks(prev => prev.map(task => task.id === taskId ? updatedTask : task));
      return updatedTask;
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
      throw err;
    }
  };

  // Toggle task completion status
  const toggleTaskCompletion = async (taskId: string, completed: boolean): Promise<Task> => {
    if (!isAuthenticated || !user) {
      throw new Error('User not authenticated');
    }

    try {
      const updatedTask = await taskService.toggleTaskCompletion(user.id, taskId, completed);
      setTasks(prev => prev.map(task => task.id === taskId ? updatedTask : task));
      return updatedTask;
    } catch (err: any) {
      setError(err.message || 'Failed to update task completion');
      throw err;
    }
  };

  // Delete a task
  const deleteTask = async (taskId: string): Promise<void> => {
    if (!isAuthenticated || !user) {
      throw new Error('User not authenticated');
    }

    try {
      await taskService.deleteTask(user.id, taskId);
      setTasks(prev => prev.filter(task => task.id !== taskId));
    } catch (err: any) {
      setError(err.message || 'Failed to delete task');
      throw err;
    }
  };

  // Mark task as complete
  const markTaskComplete = async (taskId: string): Promise<Task> => {
    return toggleTaskCompletion(taskId, true);
  };

  // Mark task as incomplete
  const markTaskIncomplete = async (taskId: string): Promise<Task> => {
    return toggleTaskCompletion(taskId, false);
  };

  // Fetch tasks when user or authentication state changes
  useEffect(() => {
    if (isAuthenticated) {
      fetchTasks();
    } else {
      setTasks([]);
    }
  }, [isAuthenticated, user, fetchTasks]);

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    toggleTaskCompletion,
    deleteTask,
    markTaskComplete,
    markTaskIncomplete,
  };
};