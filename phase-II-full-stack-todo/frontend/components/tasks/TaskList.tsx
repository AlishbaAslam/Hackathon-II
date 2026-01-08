'use client';

import { Task } from '../../lib/types';
import TaskItem from './TaskItem';
import { useState } from 'react';

interface TaskListProps {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  onToggle: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onEdit?: (task: Task) => void;
  filter?: 'all' | 'active' | 'completed';
  onFilterChange?: (filter: 'all' | 'active' | 'completed') => void;
}

export default function TaskList({
  tasks,
  loading,
  error,
  onToggle,
  onDelete,
  onEdit,
  filter = 'all',
  onFilterChange
}: TaskListProps) {
  const [activeFilter, setActiveFilter] = useState<'all' | 'active' | 'completed'>(filter);

  const handleFilterChange = (newFilter: 'all' | 'active' | 'completed') => {
    setActiveFilter(newFilter);
    if (onFilterChange) {
      onFilterChange(newFilter);
    }
  };

  // Filter tasks based on active filter
  const filteredTasks = tasks.filter(task => {
    if (activeFilter === 'active') return !task.completed;
    if (activeFilter === 'completed') return task.completed;
    return true; // 'all'
  });

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
      {/* Filter buttons */}
      <div className="flex flex-wrap gap-2 mb-6">
        <button
          onClick={() => handleFilterChange('all')}
          className={`px-4 py-2 text-sm rounded-lg font-medium transition-all ${
            activeFilter === 'all'
              ? 'bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white shadow-[--glow-card]'
              : 'bg-white/50 text-[--text-secondary] hover:bg-white/70 border border-white/20'
          }`}
        >
          All ({tasks.length})
        </button>
        <button
          onClick={() => handleFilterChange('active')}
          className={`px-4 py-2 text-sm rounded-lg font-medium transition-all ${
            activeFilter === 'active'
              ? 'bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white shadow-[--glow-card]'
              : 'bg-white/50 text-[--text-secondary] hover:bg-white/70 border border-white/20'
          }`}
        >
          Active ({tasks.filter(t => !t.completed).length})
        </button>
        <button
          onClick={() => handleFilterChange('completed')}
          className={`px-4 py-2 text-sm rounded-lg font-medium transition-all ${
            activeFilter === 'completed'
              ? 'bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white shadow-[--glow-card]'
              : 'bg-white/50 text-[--text-secondary] hover:bg-white/70 border border-white/20'
          }`}
        >
          Completed ({tasks.filter(t => t.completed).length})
        </button>
      </div>

      {/* Tasks list */}
      {filteredTasks.length === 0 ? (
        <div className="text-center py-12">
          <div className="mx-auto w-16 h-16 bg-gradient-to-br from-[--color-primary] to-[--color-accent] rounded-full flex items-center justify-center mb-4 shadow-[--glow-card]">
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
              ? 'Get started by creating your first task!'
              : activeFilter === 'active'
                ? 'Great job! All tasks are completed.'
                : 'Start working on new tasks to see them here.'}
          </p>
        </div>
      ) : (
        <ul className="divide-y divide-white/20">
          {filteredTasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onToggle={onToggle}
              onDelete={onDelete}
              onEdit={onEdit}
            />
          ))}
        </ul>
      )}
    </div>
  );
}