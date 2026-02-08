'use client';

import { Task } from '../../lib/types';
import { useState } from 'react';

interface TaskItemProps {
  task: Task;
  onToggle: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onEdit?: (task: Task) => void;
}

export default function TaskItem({ task, onToggle, onDelete, onEdit }: TaskItemProps) {
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      setIsDeleting(true);
      onDelete(task.id);
    }
  };

  const handleEdit = () => {
    if (onEdit) {
      onEdit(task);
    }
  };

  return (
    <li className="py-4 px-2 hover:bg-white/10 rounded-lg transition-colors">
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3 flex-1 min-w-0">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={() => onToggle(task)}
            className="mt-1 h-5 w-5 text-[--color-primary] border-[--border-medium] rounded focus:ring-[--color-primary] focus:ring-2 cursor-pointer"
          />
          <div className="flex-1 min-w-0">
            <span
              className={`text-[--text-primary] font-medium ${task.completed ? 'line-through text-[--text-muted]' : ''}`}
            >
              {task.title}
            </span>
            {task.description && (
              <p className={`mt-1 text-sm ${task.completed ? 'text-[--text-muted]' : 'text-[--text-secondary]'}`}>
                {task.description}
              </p>
            )}
            <p className="mt-1 text-xs text-[--text-muted]">
              Created: {new Date(task.createdAt).toLocaleDateString()}
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-3 ml-4">
          {onEdit && (
            <button
              onClick={handleEdit}
              className="text-[--text-secondary] hover:text-[--color-primary] transition-colors p-1 rounded-md hover:bg-white/20"
              aria-label="Edit task"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
          )}
          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className={`${
              isDeleting
                ? 'text-[--text-muted]'
                : 'text-[--color-error] hover:text-red-700 hover:bg-red-500/10'
            } transition-colors p-1 rounded-md`}
            aria-label="Delete task"
          >
            {isDeleting ? (
              <svg className="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            ) : (
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            )}
          </button>
        </div>
      </div>
    </li>
  );
}