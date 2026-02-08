'use client';

import { useAuth } from '../../hooks/useAuth';
import { useTasks } from '../../hooks/useTasks';
import { useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';

export default function DashboardPage() {
  const { user, loading: authLoading } = useAuth(); 
  const { tasks, loading: tasksLoading, fetchTasks } = useTasks();

  useEffect(() => {
    if (!authLoading && user) {
      fetchTasks();
    }
  }, [authLoading, user, fetchTasks]);

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[--background-gradient-start] to-[--background-gradient-end] py-12">
        <div className="text-center">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-[--color-primary] border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]">
            <span className="sr-only">Loading...</span>
          </div>
          <p className="mt-4 text-[--text-secondary]">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[--background-gradient-start] to-[--background-gradient-end] py-12">
        <div className="text-center max-w-md mx-auto p-8 glass rounded-2xl border border-white/20">
          <h2 className="text-2xl font-bold text-[--text-primary] mb-4">Please log in to access the dashboard</h2>
          <p className="text-[--text-secondary] mb-6">Sign in to view your productivity overview.</p>
          <Link href="/login" className="inline-block px-6 py-3 bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white rounded-lg hover:from-[--color-primary-dark] hover:to-[--color-accent] transition-all transform hover:scale-105 shadow-[--glow-card]">
            Go to Login
          </Link>
        </div>
      </div>
    );
  }

  const completedTasks = tasks.filter(task => task.completed).length;
  const pendingTasks = tasks.filter(task => !task.completed).length;
  const completionRate = tasks.length > 0 ? Math.round((completedTasks / tasks.length) * 100) : 0;

  // Create a mapping of task IDs to consistent short IDs based on original order
  const taskShortIdMap = tasks.reduce((map, task, index) => {
    map[task.id] = index + 1;
    return map;
  }, {} as Record<string, number>);

  return (
    <div className="min-h-screen bg-gradient-to-br from-[--background-gradient-start] to-[--background-gradient-end] py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-10"
        >
          <h1 className="text-3xl font-bold text-[--text-primary]">Dashboard</h1>
          <p className="text-[--text-secondary] mt-2">Welcome back, {user.name || user.email}! Here's your productivity overview.</p>
        </motion.div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="glass card-hover rounded-2xl p-6 border border-white/20"
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-medium text-[--text-secondary]">Total Tasks</h3>
                <p className="text-3xl font-bold text-[--color-primary] mt-2">{tasks.length}</p>
              </div>
              <div className="w-14 h-14 bg-gradient-to-br from-[--color-primary] to-[--color-accent] rounded-xl flex items-center justify-center shadow-[--glow-card]">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="glass card-hover rounded-2xl p-6 border border-white/20"
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-medium text-[--text-secondary]">Completed</h3>
                <p className="text-3xl font-bold text-[--color-success] mt-2">{completedTasks}</p>
              </div>
              <div className="w-14 h-14 bg-gradient-to-br from-[--color-success] to-emerald-400 rounded-xl flex items-center justify-center shadow-[--glow-card]">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="glass card-hover rounded-2xl p-6 border border-white/20"
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-medium text-[--text-secondary]">Pending</h3>
                <p className="text-3xl font-bold text-[--color-warning] mt-2">{pendingTasks}</p>
              </div>
              <div className="w-14 h-14 bg-gradient-to-br from-[--color-warning] to-amber-400 rounded-xl flex items-center justify-center shadow-[--glow-card]">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="glass card-hover rounded-2xl p-6 border border-white/20"
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-medium text-[--text-secondary]">Completion Rate</h3>
                <p className="text-3xl font-bold text-[--color-accent] mt-2">{completionRate}%</p>
              </div>
              <div className="w-14 h-14 bg-gradient-to-br from-[--color-accent] to-purple-400 rounded-xl flex items-center justify-center shadow-[--glow-card]">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Charts and Recent Tasks Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Task Progress Chart Placeholder */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="lg:col-span-1 glass rounded-2xl p-6 border border-white/20"
          >
            <h3 className="text-lg font-semibold text-[--text-primary] mb-4">Task Progress</h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-[--text-secondary]">Completed</span>
                <span className="font-medium text-[--color-success]">{completedTasks}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-[--color-success] to-emerald-500 h-2 rounded-full transition-all duration-500 ease-out"
                  style={{ width: `${completionRate}%` }}
                ></div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-[--text-secondary]">Pending</span>
                <span className="font-medium text-[--color-warning]">{pendingTasks}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-[--color-warning] to-amber-500 h-2 rounded-full transition-all duration-500 ease-out"
                  style={{ width: `${100 - completionRate}%` }}
                ></div>
              </div>
            </div>
          </motion.div>

          {/* Recent Tasks */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
            className="lg:col-span-2 glass rounded-2xl p-6 border border-white/20"
          >
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold text-[--text-primary]">Recent Tasks</h2>
              <Link
                href="/tasks"
                className="px-4 py-2 bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white rounded-lg hover:from-[--color-primary-dark] hover:to-[--color-accent] transition-all shadow-[--glow-card]"
              >
                View All Tasks
              </Link>
            </div>

            {tasksLoading ? (
              <div className="text-center py-8">
                <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-[--color-primary] border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"></div>
                <p className="mt-4 text-[--text-secondary]">Loading your tasks...</p>
              </div>
            ) : tasks.length === 0 ? (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-gradient-to-br from-[--color-primary] to-[--color-accent] rounded-full flex items-center justify-center mx-auto mb-4 shadow-[--glow-card]">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <h3 className="text-lg font-medium text-[--text-primary] mb-2">No tasks yet</h3>
                <p className="text-[--text-secondary] mb-4">Get started by creating your first task!</p>
                <Link
                  href="/tasks"
                  className="inline-block px-4 py-2 bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white rounded-lg hover:from-[--color-primary-dark] hover:to-[--color-accent] transition-all shadow-[--glow-card]"
                >
                  Create Task
                </Link>
              </div>
            ) : (
              <div className="overflow-hidden rounded-lg border border-[--border-light]">
                <table className="min-w-full divide-y divide-[--border-light]">
                  <thead className="bg-white/50">
                    <tr>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-[--text-secondary] uppercase tracking-wider">
                        Task
                      </th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-[--text-secondary] uppercase tracking-wider">
                        Status
                      </th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-[--text-secondary] uppercase tracking-wider">
                        Created
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white/50 divide-y divide-[--border-light]">
                    {tasks.slice(0, 5).map((task, index) => (
                      <motion.tr
                        key={task.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.3, delay: 0.7 + index * 0.1 }}
                        className="hover:bg-white/50 transition-colors"
                      >
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-[--text-primary] truncate max-w-xs">
                            {taskShortIdMap[task.id] && <span className="font-bold text-[--color-primary] mr-2">{taskShortIdMap[task.id]}.</span>}{task.title}
                          </div>
                          {task.description && (
                            <div className="text-sm text-[--text-secondary] truncate max-w-xs">{task.description}</div>
                          )}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                            task.completed
                              ? 'bg-green-100 text-green-800 bg-gradient-to-r from-green-100 to-emerald-100 text-green-800'
                              : 'bg-yellow-100 text-yellow-800 bg-gradient-to-r from-yellow-100 to-amber-100 text-yellow-800'
                          }`}>
                            {task.completed ? 'Completed' : 'Pending'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-[--text-secondary]">
                          {new Date(task.createdAt).toLocaleDateString()}
                        </td>
                      </motion.tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
}