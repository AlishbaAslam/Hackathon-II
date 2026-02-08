import { useState, useEffect, useCallback } from 'react';
import { Task, CreateTaskRequest, UpdateTaskRequest } from '../lib/types';
import { taskService } from '../services/task-service';
import { useAuth } from './useAuth';

// Define the tasks context type
interface TasksContextType {
  tasks: Task[];
  allTasks: Task[]; // Unfiltered tasks for stats
  loading: boolean;
  error: string | null;
  searchTerm: string;
  filter: 'all' | 'active' | 'completed' | 'pending' | 'high-priority' | 'recurring' | 'overdue' | 'today' | 'upcoming' | 'low-priority' | 'medium-priority';
  setSearchTerm: (term: string) => void;
  setFilter: (filter: 'all' | 'active' | 'completed' | 'pending' | 'high-priority' | 'recurring' | 'overdue' | 'today' | 'upcoming' | 'low-priority' | 'medium-priority') => void;
  fetchTasks: () => Promise<void>;
  createTask: (taskData: CreateTaskRequest) => Promise<Task>;
  updateTask: (taskId: string, taskData: UpdateTaskRequest) => Promise<Task>;
  toggleTaskCompletion: (taskId: string, completed: boolean) => Promise<Task>;
  deleteTask: (taskId: string) => Promise<void>;
  markTaskComplete: (taskId: string) => Promise<Task>;
  markTaskIncomplete: (taskId: string) => Promise<Task>;
  filteredTasks: Task[];  // Additional property for filtered tasks with sorting
}

// Custom hook for managing tasks
export const useTasks = (): TasksContextType => {
  const [allTasks, setAllTasks] = useState<Task[]>([]); // Original unfiltered tasks
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [filter, setFilter] = useState<'all' | 'active' | 'completed' | 'pending' | 'high-priority' | 'recurring' | 'overdue' | 'today' | 'upcoming' | 'low-priority' | 'medium-priority'>('all');

  // Get auth context to access user and token
  const { user, isAuthenticated } = useAuth();

  // Function to filter and sort tasks based on search term and active filter
  const getFilteredTasks = useCallback(() => {
    let filtered = allTasks.filter(task => {
      // Apply search filter
      const matchesSearch = !searchTerm ||
        task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (task.description && task.description.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (task.tags && task.tags.toLowerCase().includes(searchTerm.toLowerCase()));

      // Apply status filter
      let matchesStatus = true;
      switch (filter) {
        case 'active':
        case 'pending':
          matchesStatus = !task.completed;
          break;
        case 'completed':
          matchesStatus = task.completed;
          break;
        case 'high-priority':
          matchesStatus = !task.completed && task.priority === 'high';
          break;
        case 'medium-priority':
          matchesStatus = !task.completed && task.priority === 'medium';
          break;
        case 'low-priority':
          matchesStatus = !task.completed && task.priority === 'low';
          break;
        case 'recurring':
          matchesStatus = task.isRecurring === true;
          break;
        case 'overdue':
          matchesStatus = !task.completed && task.dueDate ? new Date(task.dueDate) < new Date() : false;
          break;
        case 'today':
          matchesStatus = !task.completed && task.dueDate ?
            new Date(task.dueDate).toDateString() === new Date().toDateString() : false;
          break;
        case 'upcoming':
          matchesStatus = !task.completed && task.dueDate ?
            new Date(task.dueDate) > new Date() : false;
          break;
        case 'all':
        default:
          matchesStatus = true;
          break;
      }

      return matchesSearch && matchesStatus;
    });

    // Sort tasks: completed tasks at the bottom, incomplete at the top
    // Within each group, sort by priority (high to low) and then by due date (soonest first)
    filtered.sort((a, b) => {
      // If one is completed and the other is not, prioritize incomplete
      if (a.completed !== b.completed) {
        return a.completed ? 1 : -1;
      }

      // If both are completed or both are incomplete, sort by priority
      const priorityOrder: Record<string, number> = { high: 3, medium: 2, low: 1 };
      const priorityA = priorityOrder[a.priority || 'low'] ?? 1;
      const priorityB = priorityOrder[b.priority || 'low'] ?? 1;

      if (priorityA !== priorityB) {
        return priorityB - priorityA; // Higher priority first
      }

      // If priority is the same, sort by due date (earliest first for incomplete, latest first for completed)
      if (a.dueDate && b.dueDate) {
        const dateA = new Date(a.dueDate).getTime();
        const dateB = new Date(b.dueDate).getTime();

        if (a.completed && b.completed) {
          return dateB - dateA; // For completed tasks, latest first
        }
        return dateA - dateB; // For incomplete tasks, earliest first
      } else if (a.dueDate) {
        return -1; // Tasks with due dates come first
      } else if (b.dueDate) {
        return 1;
      }

      return 0; // If no due dates, maintain original order
    });

    return filtered;
  }, [allTasks, searchTerm, filter]);

  // tasks represents the filtered/sorted tasks
  const tasks = getFilteredTasks();

  // Fetch tasks for the current user
  const fetchTasks = useCallback(async () => {
    if (!isAuthenticated || !user) {
      setAllTasks([]);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const userTasks = await taskService.getTasks(user.id);
      console.log('Raw API response tasks:', userTasks.map(task => ({ id: task.id, title: task.title, dueDate: task.dueDate, due_date: (task as any).due_date }))); // Debugging log
      setAllTasks(userTasks); // Backend already sorts by newest first
    } catch (err: any) {
      setError(err.message || 'Failed to fetch tasks');
      setAllTasks([]);
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
      console.log('Creating task with data:', taskData); // Debugging log
      const newTask = await taskService.createTask(user.id, taskData);
      console.log('Created task with priority:', newTask.priority); // Debugging log
      setAllTasks(prev => [...prev, newTask]); // Add new task to the end
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
      setAllTasks(prev => prev.map(task => task.id === taskId ? updatedTask : task));
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
      setAllTasks(prev => prev.map(task => task.id === taskId ? updatedTask : task));
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
      setAllTasks(prev => prev.filter(task => task.id !== taskId));
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
      setAllTasks([]);
    }
  }, [isAuthenticated, user, fetchTasks]);

  const filteredTasks = getFilteredTasks();

  return {
    tasks: filteredTasks, // Return filtered and sorted tasks
    allTasks, // Return all unfiltered tasks for stats
    loading,
    error,
    searchTerm,
    filter,
    setSearchTerm,
    setFilter,
    fetchTasks,
    createTask,
    updateTask,
    toggleTaskCompletion,
    deleteTask,
    markTaskComplete,
    markTaskIncomplete,
    filteredTasks,  // Additional property for filtered tasks with sorting
  };
};