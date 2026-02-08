'use client';

import { useState } from 'react';
import { Task } from '../lib/types';
import { motion } from 'framer-motion';
import { Calendar } from 'lucide-react';

interface TaskCardProps {
  task: Task;
  onToggle: (task: Task) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
}

export default function TaskCard({ task, onToggle, onEdit, onDelete }: TaskCardProps) {
  const [isHovered, setIsHovered] = useState(false);

  // Determine if task is overdue
  const isOverdue = task.dueDate && new Date(task.dueDate) < new Date() && !task.completed;

  // Helper functions to check date conditions
  const isToday = (date: string) => {
    const taskDate = new Date(date);
    const today = new Date();
    return taskDate.getDate() === today.getDate() &&
           taskDate.getMonth() === today.getMonth() &&
           taskDate.getFullYear() === today.getFullYear();
  };

  const isTomorrow = (date: string) => {
    const taskDate = new Date(date);
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    return taskDate.getDate() === tomorrow.getDate() &&
           taskDate.getMonth() === tomorrow.getMonth() &&
           taskDate.getFullYear() === tomorrow.getFullYear();
  };

  // Format date to "15 Feb 2026" format
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    });
  };

  // Determine due date text and color
  let dueDateText = '';
  let dueDateColor = 'text-gray-500 dark:text-gray-400'; // Default gray
  let isDueSoonOrOverdue = false;

  if (task.dueDate) {
    if (isToday(task.dueDate)) {
      dueDateText = 'Today';
      dueDateColor = 'text-red-600 dark:text-red-400'; // Red for today
      isDueSoonOrOverdue = true;
    } else if (isTomorrow(task.dueDate)) {
      dueDateText = 'Tomorrow';
      dueDateColor = 'text-gray-500 dark:text-gray-400'; // Gray for tomorrow
      isDueSoonOrOverdue = true;
    } else {
      dueDateText = formatDate(task.dueDate);
      // Red for overdue, otherwise gray
      if (isOverdue) {
        dueDateColor = 'text-red-600 dark:text-red-400';
        isDueSoonOrOverdue = true;
      } else {
        dueDateColor = 'text-gray-500 dark:text-gray-400'; // Regular gray
      }
    }
  }

  // Priority color classes
  const priorityColors = {
    high: 'bg-red-500',
    medium: 'bg-yellow-500',
    low: 'bg-green-500',
  };

  const priorityColor = priorityColors[task.priority as keyof typeof priorityColors] || 'bg-gray-500';

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      whileHover={{ y: -2 }}
      className="bg-white rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden hover:shadow-md transition-shadow relative"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className={`absolute left-0 top-0 bottom-0 w-2 ${
        task.priority === 'high' ? 'bg-red-500' :
        task.priority === 'medium' ? 'bg-yellow-500' :
        'bg-green-500'
      }`}></div>

      <div className="p-4 pl-6"> {/* Extra left padding to account for priority bar */}
        <div className="flex items-start gap-3">
          <button
            onClick={() => onToggle(task)}
            className="flex-shrink-0 w-5 h-5 mt-1 rounded border flex items-center justify-center transition-colors"
            aria-label={task.completed ? "Mark as incomplete" : "Mark as complete"}
          >
            {task.completed ? (
              <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
            ) : (
              <span className="w-3 h-3 border border-gray-300"></span>
            )}
          </button>

          <div className="flex-1 min-w-0">
            {task.priority && task.priority !== 'medium' && (
              <span className={`${
                task.priority === 'high'
                  ? 'bg-red-100 text-red-800 border-red-200'
                  : task.priority === 'low'
                    ? 'bg-green-100 text-green-800 border-green-200'
                    : 'bg-yellow-100 text-yellow-800 border-yellow-200'
              } rounded px-2 py-1 text-xs font-medium mr-2 mb-2`}>
                {task.priority.toUpperCase()}
              </span>
            )}

            <h3 className={`text-lg font-medium ${task.completed ? 'text-gray-500 line-through' : 'text-gray-900 dark:text-white'}`}>
              {task.title}
            </h3>

            {task.description && (
              <p className={`text-sm ${task.completed ? 'text-gray-400 line-through' : 'text-gray-600 dark:text-gray-400'} mt-1 line-clamp-2`}>
                {task.description}
              </p>
            )}

            <div className="mt-3 flex flex-wrap gap-2">
              {task.tags && task.tags.split(',').map((tag, index) => (
                <span key={index} className="text-xs px-2 py-1 rounded-full bg-purple-100 text-purple-800 border border-purple-200">
                  {tag.trim()}
                </span>
              ))}

              {task.dueDate && (
                <span className="flex items-center gap-1 text-sm">
                  <Calendar className="h-3 w-3 text-gray-500" />
                  <span className={dueDateColor}>
                    {dueDateText}
                  </span>
                </span>
              )}
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}