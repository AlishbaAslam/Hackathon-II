'use client';

import { Task } from '../../lib/types';
import TaskItem from './TaskItem';
import { useState } from 'react';

interface TaskListProps {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  searchTerm: string;
  filter: 'all' | 'active' | 'completed' | 'pending' | 'high-priority' | 'recurring' | 'overdue';
  setSearchTerm: (term: string) => void;
  setFilter: (filter: 'all' | 'active' | 'completed' | 'pending' | 'high-priority' | 'recurring' | 'overdue') => void;
  onToggle: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onEdit?: (task: Task) => void;
}

export default function TaskList({
  tasks,
  loading,
  error,
  searchTerm,
  filter,
  setSearchTerm,
  setFilter,
  onToggle,
  onDelete,
  onEdit
}: TaskListProps) {
  const handleFilterChange = (newFilter: 'all' | 'active' | 'completed' | 'pending' | 'high-priority' | 'recurring' | 'overdue') => {
    setFilter(newFilter);
  };

  // Create a mapping of task IDs to consistent short IDs based on original order
  const taskShortIdMap = tasks.reduce((map, task, index) => {
    map[task.id] = index + 1;
    return map;
  }, {} as Record<string, number>);

  if (loading) {
    return (
      <div className="glass rounded-2xl p-8 border border-white/20">
        <div className="flex justify-center items-center py-8">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-[--color-primary] border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]">
            <span className="sr-only">Loading...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass rounded-2xl p-6 border border-red-200 text-[--color-error] mb-4">
        <div className="flex items-center">
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="glass rounded-2xl p-6 border border-white/20">
      {/* Search and filter controls */}
      <div className="mb-6">
        {/* Search input */}
        <div className="relative mb-4">
          <input
            type="text"
            placeholder="Search tasks by title, description, or tags..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-4 py-3 bg-white/50 border border-[--border-light] rounded-lg focus:outline-none focus:ring-2 focus:ring-[--color-primary]/50 focus:border-[--color-primary] transition-all"
          />
          {searchTerm && (
            <button
              onClick={() => setSearchTerm('')}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-[--text-secondary] hover:text-[--color-primary]"
            >
              ✕
            </button>
          )}
        </div>

        {/* Filter buttons */}
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => handleFilterChange('all')}
            className={`px-4 py-2 text-sm rounded-lg font-medium transition-all ${
              filter === 'all'
                ? 'bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white shadow-[--glow-card]'
                : 'bg-white/50 text-[--text-secondary] hover:bg-white/70 border border-white/20'
            }`}
          >
            All ({tasks.length})
          </button>
          <button
            onClick={() => handleFilterChange('active')}
            className={`px-4 py-2 text-sm rounded-lg font-medium transition-all ${
              filter === 'active'
                ? 'bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white shadow-[--glow-card]'
                : 'bg-white/50 text-[--text-secondary] hover:bg-white/70 border border-white/20'
            }`}
          >
            Active ({tasks.filter(t => !t.completed).length})
          </button>
          <button
            onClick={() => handleFilterChange('completed')}
            className={`px-4 py-2 text-sm rounded-lg font-medium transition-all ${
              filter === 'completed'
                ? 'bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white shadow-[--glow-card]'
                : 'bg-white/50 text-[--text-secondary] hover:bg-white/70 border border-white/20'
            }`}
          >
            Completed ({tasks.filter(t => t.completed).length})
          </button>
          <button
            onClick={() => handleFilterChange('high-priority')}
            className={`px-4 py-2 text-sm rounded-lg font-medium transition-all ${
              filter === 'high-priority'
                ? 'bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white shadow-[--glow-card]'
                : 'bg-white/50 text-[--text-secondary] hover:bg-white/70 border border-white/20'
            }`}
          >
            High Priority ({tasks.filter(t => !t.completed && t.priority === 'high').length})
          </button>
          <button
            onClick={() => handleFilterChange('recurring')}
            className={`px-4 py-2 text-sm rounded-lg font-medium transition-all ${
              filter === 'recurring'
                ? 'bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white shadow-[--glow-card]'
                : 'bg-white/50 text-[--text-secondary] hover:bg-white/70 border border-white/20'
            }`}
          >
            Recurring ({tasks.filter(t => t.isRecurring === true).length})
          </button>
          <button
            onClick={() => handleFilterChange('overdue')}
            className={`px-4 py-2 text-sm rounded-lg font-medium transition-all ${
              filter === 'overdue'
                ? 'bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white shadow-[--glow-card]'
                : 'bg-white/50 text-[--text-secondary] hover:bg-white/70 border border-white/20'
            }`}
          >
            Overdue ({tasks.filter(t => !t.completed && t.dueDate && new Date(t.dueDate) < new Date()).length})
          </button>
        </div>
      </div>

      {/* Tasks list */}
      {tasks.length === 0 ? (
        <div className="text-center py-12">
          <div className="mx-auto w-16 h-16 bg-gradient-to-br from-[--color-primary] to-[--color-accent] rounded-full flex items-center justify-center mb-4 shadow-[--glow-card]">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-[--text-primary] mb-2">
            {searchTerm
              ? 'No tasks match your search'
              : filter === 'all'
                ? 'No tasks yet'
                : filter === 'active' || filter === 'pending'
                  ? 'No active tasks'
                  : filter === 'completed'
                    ? 'No completed tasks'
                    : filter === 'high-priority'
                      ? 'No high priority tasks'
                      : filter === 'recurring'
                        ? 'No recurring tasks'
                        : filter === 'overdue'
                          ? 'No overdue tasks'
                          : 'No tasks found'}
          </h3>
          <p className="text-[--text-secondary] mb-4">
            {searchTerm
              ? `Try adjusting your search term`
              : filter === 'all'
                ? 'Get started by creating your first task!'
                : filter === 'active' || filter === 'pending'
                  ? 'Great job! All tasks are completed.'
                  : filter === 'completed'
                    ? 'Start working on new tasks to see them here.'
                    : filter === 'high-priority'
                      ? 'All tasks have lower priority levels.'
                      : filter === 'recurring'
                        ? 'Create a recurring task to see it here.'
                        : filter === 'overdue'
                          ? 'No tasks are currently overdue.'
                          : 'No tasks match this filter.'}
          </p>
        </div>
      ) : (
        <ul className="divide-y divide-white/20">
          {tasks.map((task, index) => {
            // Add shortId based on the consistent mapping (original task order)
            const taskWithShortId = {
              ...task,
              shortId: taskShortIdMap[task.id]
            };
            return (
              <TaskItem
                key={task.id}
                task={taskWithShortId}
                onToggle={onToggle}
                onDelete={onDelete}
                onEdit={onEdit}
              />
            );
          })}
        </ul>
      )}
    </div>
  );
}