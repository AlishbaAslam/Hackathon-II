'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import Button from '@/components/ui/Button';
import Link from 'next/link';
import { CheckCircle, Circle, AlertCircle, Clock, Calendar, Repeat, Tag as TagIcon } from 'lucide-react';
import { motion } from 'framer-motion';

interface Task {
  id: string | number;
  title: string;
  description?: string;
  completed: boolean;
  priority?: 'high' | 'medium' | 'low';
  dueDate?: string;
  tags?: string;
  recurring?: boolean;
}

interface RecentTasksProps {
  tasks: Task[];
  loading: boolean;
  onTaskToggle?: (id: string | number) => void;
}

export default function RecentTasks({ tasks, loading, onTaskToggle }: RecentTasksProps) {
  // Priority colors
  const getPriorityColor = (priority?: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  // Priority icons
  const getPriorityIcon = (priority?: string) => {
    switch (priority) {
      case 'high': return <AlertCircle className="h-4 w-4 text-red-500" />;
      case 'medium': return <AlertCircle className="h-4 w-4 text-yellow-500" />;
      case 'low': return <Circle className="h-4 w-4 text-green-500" />;
      default: return <Circle className="h-4 w-4 text-gray-500" />;
    }
  };

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Recent Tasks</CardTitle>
        <Link href="/tasks">
          <Button variant="outline">View All</Button>
        </Link>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="text-center py-8">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-indigo-600 border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"></div>
            <p className="mt-4 text-gray-600 dark:text-gray-400">Loading your tasks...</p>
          </div>
        ) : tasks.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <CheckCircle className="h-8 w-8 text-white" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">No tasks yet</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">Get started by creating your first task!</p>
            <Link href="/tasks">
              <Button>
                <Circle className="mr-2 h-4 w-4" />
                Create Task
              </Button>
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {tasks.slice(0, 5).map((task, index) => (
              <motion.div
                key={task.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: 0.1 * index }}
                className="flex items-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
              >
                <input
                  type="checkbox"
                  checked={task.completed}
                  className="h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                  onChange={() => onTaskToggle?.(task.id)} // This would trigger task completion in real app
                />

                <div className="ml-4 flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <p className={`text-sm font-medium truncate ${task.completed ? 'text-gray-500 dark:text-gray-400 line-through' : 'text-gray-900 dark:text-white'}`}>
                      {task.title}
                    </p>
                    <div className="flex items-center space-x-2">
                      {task.recurring && (
                        <Repeat className="h-4 w-4 text-blue-500" />
                      )}
                      <Badge variant="secondary" className={getPriorityColor(task.priority)}>
                        {getPriorityIcon(task.priority)}
                        <span className="ml-1 capitalize">{task.priority}</span>
                      </Badge>
                    </div>
                  </div>

                  {task.description && (
                    <p className="text-sm text-gray-500 dark:text-gray-400 truncate mt-1">
                      {task.description}
                    </p>
                  )}

                  <div className="flex flex-wrap gap-2 mt-2">
                    {task.dueDate && (
                      <span className="flex items-center gap-1 text-sm">
                        <Calendar className="h-4 w-4 text-gray-500 dark:text-gray-400" />
                        {(() => {
                          const dueDate = new Date(task.dueDate);
                          const today = new Date();
                          const tomorrow = new Date(today);
                          tomorrow.setDate(tomorrow.getDate() + 1);

                          // Set time to 00:00 for accurate comparison
                          today.setHours(0, 0, 0, 0);
                          tomorrow.setHours(0, 0, 0, 0);
                          dueDate.setHours(0, 0, 0, 0);

                          if (dueDate.getTime() === today.getTime()) {
                            return <span className="text-red-600 dark:text-red-400">Today</span>;
                          } else if (dueDate.getTime() === tomorrow.getTime()) {
                            return <span className="text-gray-500 dark:text-gray-400">Tomorrow</span>;
                          } else if (dueDate < today && !task.completed) {
                            return (
                              <>
                                <span className="text-red-600 dark:text-red-400">
                                  {dueDate.toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' })}
                                </span>
                                <span className="text-red-600 dark:text-red-400 text-xs">(Overdue)</span>
                              </>
                            );
                          } else {
                            return (
                              <span className="text-gray-500 dark:text-gray-400">
                                {dueDate.toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' })}
                              </span>
                            );
                          }
                        })()}
                      </span>
                    )}

                    {task.tags && (
                      <Badge variant="outline" className="text-xs">
                        {task.tags}
                      </Badge>
                    )}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}