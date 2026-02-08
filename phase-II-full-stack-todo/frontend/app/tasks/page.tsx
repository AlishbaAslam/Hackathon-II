'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../../hooks/useAuth';
import { useTasks } from '../../hooks/useTasks';
import EditTaskModal from '../../components/tasks/EditTaskModal';
import Link from 'next/link';
import { Task } from '../../lib/types';

export default function TasksPage() {
  const { user, loading: authLoading } = useAuth();
  const {
    tasks,
    loading: tasksLoading,
    error,
    fetchTasks,
    createTask,
    toggleTaskCompletion,
    deleteTask,
    updateTask
  } = useTasks();

  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [activeFilter, setActiveFilter] = useState<'all' | 'active' | 'completed'>('all');

  // Edit modal state
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isUpdatingTask, setIsUpdatingTask] = useState(false);

  useEffect(() => {
    if (!authLoading && user) {
      fetchTasks();
    }
  }, [authLoading, user, fetchTasks]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;

    try {
      await createTask({
        title: newTaskTitle,
        description: newTaskDescription || undefined
      });
      setNewTaskTitle('');
      setNewTaskDescription('');
      setShowForm(false);
    } catch (err) {
      console.error('Failed to create task:', err);
    }
  };

  const handleToggle = async (task: Task) => {
    try {
      await toggleTaskCompletion(task.id, !task.completed);
    } catch (err) {
      console.error('Failed to update task:', err);
    }
  };

  const handleDelete = async (taskId: string) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(taskId);
      } catch (err) {
        console.error('Failed to delete task:', err);
      }
    }
  };

  const handleEdit = (task: Task) => {
    setEditingTask(task);
    setIsEditModalOpen(true);
  };

  const handleUpdateTask = async (taskId: string, data: { title: string; description?: string }) => {
    setIsUpdatingTask(true);
    try {
      await updateTask(taskId, data);
      setIsEditModalOpen(false);
      setEditingTask(null);
    } catch (err) {
      console.error('Failed to update task:', err);
    } finally {
      setIsUpdatingTask(false);
    }
  };

  const handleCloseEditModal = () => {
    setIsEditModalOpen(false);
    setEditingTask(null);
  };

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[--background-gradient-start] to-[--background-gradient-end] py-12">
        <div className="text-center">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-[--color-primary] border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]">
            <span className="sr-only">Loading...</span>
          </div>
          <p className="mt-4 text-[--text-secondary]">Loading your tasks...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[--background-gradient-start] to-[--background-gradient-end] py-12">
        <div className="text-center max-w-md mx-auto p-8 glass rounded-2xl border border-white/20">
          <h2 className="text-2xl font-bold text-[--text-primary] mb-4">Please log in to access your tasks</h2>
          <p className="text-[--text-secondary] mb-6">Sign in to manage your tasks and boost your productivity.</p>
          <Link href="/login" className="inline-block px-6 py-3 bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white rounded-lg hover:from-[--color-primary-dark] hover:to-[--color-accent] transition-all transform hover:scale-105 shadow-[--glow-card]">
            Go to Login
          </Link>
        </div>
      </div>
    );
  }

  // Filter tasks based on active filter
  const filteredTasks = tasks.filter(task => {
    if (activeFilter === 'active') return !task.completed;
    if (activeFilter === 'completed') return task.completed;
    return true; // 'all'
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-[--background-gradient-start] to-[--background-gradient-end] py-8">
      <div className="max-w-4xl mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="glass rounded-2xl p-6 mb-8 border border-white/20"
        >
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
            <div>
              <h2 className="text-2xl font-bold text-[--text-primary]">Your Tasks</h2>
              <p className="text-[--text-secondary] mt-1">Manage and organize your daily activities</p>
            </div>
            <button
              onClick={() => setShowForm(!showForm)}
              className="px-6 py-3 bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white rounded-lg hover:from-[--color-primary-dark] hover:to-[--color-accent] transition-all transform hover:scale-105 shadow-[--glow-card] flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              {showForm ? 'Cancel' : 'Add Task'}
            </button>
          </div>

          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="glass rounded-lg p-4 border border-red-200 text-[--color-error] mb-6 flex items-center"
            >
              <svg className="w-5 h-5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{error}</span>
            </motion.div>
          )}

          {/* Task creation form */}
          <AnimatePresence>
            {showForm && (
              <motion.form
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                onSubmit={handleSubmit}
                className="mb-8 glass rounded-xl p-6 border border-white/20"
              >
                <div className="mb-4">
                  <label htmlFor="task-title" className="block text-sm font-medium text-[--text-secondary] mb-2">
                    Task Title *
                  </label>
                  <input
                    type="text"
                    id="task-title"
                    value={newTaskTitle}
                    onChange={(e) => setNewTaskTitle(e.target.value)}
                    className="w-full px-4 py-3 bg-white/50 border border-[--border-light] rounded-lg focus:outline-none focus:ring-2 focus:ring-[--color-primary]/50 focus:border-[--color-primary] transition-all"
                    placeholder="What needs to be done?"
                    required
                  />
                </div>
                <div className="mb-6">
                  <label htmlFor="task-description" className="block text-sm font-medium text-[--text-secondary] mb-2">
                    Description (Optional)
                  </label>
                  <textarea
                    id="task-description"
                    value={newTaskDescription}
                    onChange={(e) => setNewTaskDescription(e.target.value)}
                    className="w-full px-4 py-3 bg-white/50 border border-[--border-light] rounded-lg focus:outline-none focus:ring-2 focus:ring-[--color-primary]/50 focus:border-[--color-primary] transition-all"
                    placeholder="Add details..."
                    rows={3}
                  />
                </div>
                <div className="flex justify-end gap-3">
                  <button
                    type="submit"
                    className="px-6 py-3 bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white rounded-lg hover:from-[--color-primary-dark] hover:to-[--color-accent] transition-all transform hover:scale-105 shadow-[--glow-card]"
                  >
                    Create Task
                  </button>
                </div>
              </motion.form>
            )}
          </AnimatePresence>

          {/* Filter tabs */}
          <div className="flex flex-wrap gap-2 mb-6">
            {(['all', 'active', 'completed'] as const).map((filter) => (
              <button
                key={filter}
                onClick={() => setActiveFilter(filter)}
                className={`px-4 py-2 text-sm font-medium rounded-lg transition-all ${
                  activeFilter === filter
                    ? 'bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white shadow-[--glow-card]'
                    : 'bg-white/50 text-[--text-secondary] hover:bg-white/70 border border-white/20'
                }`}
              >
                {filter.charAt(0).toUpperCase() + filter.slice(1)} (
                {filter === 'all'
                  ? tasks.length
                  : filter === 'active'
                    ? tasks.filter(t => !t.completed).length
                    : tasks.filter(t => t.completed).length
                })
              </button>
            ))}
          </div>
        </motion.div>

        {/* Tasks list */}
        <div className="mb-8">
          {tasksLoading ? (
            <div className="text-center py-12">
              <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-[--color-primary] border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"></div>
              <p className="mt-4 text-[--text-secondary]">Loading your tasks...</p>
            </div>
          ) : filteredTasks.length === 0 ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center py-12 glass rounded-2xl p-8 border border-white/20"
            >
              <div className="w-16 h-16 bg-gradient-to-br from-[--color-primary] to-[--color-accent] rounded-full flex items-center justify-center mx-auto mb-4 shadow-[--glow-card]">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-[--text-primary] mb-2">
                {activeFilter === 'all'
                  ? 'No tasks yet'
                  : activeFilter === 'active'
                    ? 'No active tasks'
                    : 'No completed tasks'}
              </h3>
              <p className="text-[--text-secondary] mb-4">
                {activeFilter === 'all'
                  ? 'Create your first task to get started!'
                  : activeFilter === 'active'
                    ? 'Great job! All tasks are completed.'
                    : 'No tasks have been completed yet.'}
              </p>
              {activeFilter === 'all' && (
                <button
                  onClick={() => setShowForm(true)}
                  className="px-4 py-2 bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white rounded-lg hover:from-[--color-primary-dark] hover:to-[--color-accent] transition-all shadow-[--glow-card]"
                >
                  Create Task
                </button>
              )}
            </motion.div>
          ) : (
            <AnimatePresence>
              <div className="grid gap-4">
                {filteredTasks.map((task, index) => (
                  <motion.div
                    key={task.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.3, delay: index * 0.05 }}
                    className={`glass rounded-xl p-6 border border-white/20 hover:shadow-[--glow-card] transition-all duration-300 transform hover:-translate-y-0.5 ${
                      task.completed
                        ? 'bg-white/70'
                        : 'bg-white/90'
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-3 flex-1 min-w-0">
                        <button
                          onClick={() => handleToggle(task)}
                          className={`flex-shrink-0 mt-0.5 w-5 h-5 rounded-full border flex items-center justify-center transition-colors ${
                            task.completed
                              ? 'bg-[--color-success] border-[--color-success] text-white'
                              : 'border-[--border-medium] hover:border-[--color-primary] text-transparent'
                          }`}
                          aria-label={task.completed ? "Mark as incomplete" : "Mark as complete"}
                        >
                          {task.completed && (
                            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                            </svg>
                          )}
                        </button>
                        <div className="flex-1 min-w-0">
                          <h3 className={`text-[--text-primary] font-medium ${
                            task.completed
                              ? 'text-[--text-muted] line-through'
                              : 'text-[--text-primary]'
                          }`}>
                            {task.title}
                          </h3>
                          {task.description && (
                            <p className={`mt-1 text-sm ${
                              task.completed ? 'text-[--text-muted] line-through' : 'text-[--text-secondary]'
                            }`}>
                              {task.description}
                            </p>
                          )}
                          <div className="mt-2 flex items-center text-xs text-[--text-muted]">
                            <svg className="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            <span>Created: {new Date(task.createdAt).toLocaleDateString()}</span>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2 ml-4">
                        <button
                          onClick={() => handleEdit(task)}
                          className="p-1.5 text-[--text-secondary] hover:text-[--color-primary] hover:bg-white/20 rounded-md transition-colors"
                          aria-label="Edit task"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>
                        <button
                          onClick={() => handleDelete(task.id)}
                          className="p-1.5 text-[--text-secondary] hover:text-[--color-error] hover:bg-red-500/10 rounded-md transition-colors"
                          aria-label="Delete task"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </AnimatePresence>
          )}
        </div>

        {/* Edit Task Modal */}
        {editingTask && (
          <EditTaskModal
            task={editingTask}
            isOpen={isEditModalOpen}
            onClose={handleCloseEditModal}
            onSubmit={handleUpdateTask}
            loading={isUpdatingTask}
          />
        )}
      </div>
    </div>
  );
}
