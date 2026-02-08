'use client';

import { useState, useEffect, useMemo } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { useTasks } from '../../hooks/useTasks';
import Link from 'next/link';
import { motion } from 'framer-motion';
import {
  Search,
  Sun,
  Moon,
  Bell,
  Plus,
  Settings,
  BookOpen,
  Tag,
  Heart,
  ShoppingBag,
  ArrowLeft,
  CheckCircle,
  Circle,
  Clock,
  TrendingUp,
  AlertTriangle,
  Calendar
} from 'lucide-react';
import Button from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import Input from '@/components/ui/Input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Progress } from '@/components/ui/Progress';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/Avatar';
import TaskFormModal from '@/components/TaskFormModal';
import Sidebar from '@/components/Sidebar';

export default function DashboardPage() {
  const { user, loading: authLoading, logout } = useAuth();
  const { tasks, allTasks, loading: tasksLoading, createTask, updateTask, deleteTask, markTaskComplete, markTaskIncomplete, setFilter, filter, setSearchTerm, searchTerm } = useTasks();
  const [isMounted, setIsMounted] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalLoading, setModalLoading] = useState(false);
  const [currentView, setCurrentView] = useState<'dashboard' | 'all-tasks'>('dashboard');
  const [editingTask, setEditingTask] = useState<any>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [sortOption, setSortOption] = useState('dueDate-asc');

  // Calculate pending reminders count
  const pendingRemindersCount = useMemo(() => {
    if (!allTasks) return 0;
    const now = new Date();
    return allTasks.filter(task =>
      !task.completed &&
      task.remindAt &&
      new Date(task.remindAt) > now
    ).length;
  }, [allTasks]);

  // Handler for notification bell click
  const handleNotificationClick = () => {
    // TODO: Open notifications/reminders dropdown or modal
    console.log('Notifications clicked - pending reminders:', pendingRemindersCount);
  };

  useEffect(() => {
    setIsMounted(true);
  }, []);

  // Handler for creating a new task
  const handleCreateTask = async (taskData: any) => {
    setModalLoading(true);
    try {
      await createTask(taskData);
      setIsModalOpen(false);
    } catch (error) {
      console.error('Failed to create task:', error);
    } finally {
      setModalLoading(false);
    }
  };

  // Handler for updating an existing task
  const handleUpdateTask = async (taskData: any) => {
    if (!editingTask) return;

    setModalLoading(true);
    try {
      await updateTask(editingTask.id, taskData);
      setEditingTask(null);
      setIsModalOpen(false);
      setIsEditing(false);
    } catch (error) {
      console.error('Failed to update task:', error);
    } finally {
      setModalLoading(false);
    }
  };

  // Memoized sorted tasks based on sort option
  const sortedTasks = useMemo(() => {
    if (!tasks) return [];

    return [...tasks].sort((a, b) => {
      switch (sortOption) {
        case 'dueDate-asc':
          if (!a.dueDate && !b.dueDate) return 0;
          if (!a.dueDate) return 1;
          if (!b.dueDate) return -1;
          return new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime();

        case 'dueDate-desc':
          if (!a.dueDate && !b.dueDate) return 0;
          if (!a.dueDate) return 1;
          if (!b.dueDate) return -1;
          return new Date(b.dueDate).getTime() - new Date(a.dueDate).getTime();

        case 'priority-desc':
          const priorityMapDesc: Record<string, number> = { 'high': 3, 'medium': 2, 'low': 1 };
          const aPriority = a.priority ? priorityMapDesc[a.priority] || 0 : 0;
          const bPriority = b.priority ? priorityMapDesc[b.priority] || 0 : 0;
          return bPriority - aPriority;

        case 'priority-asc':
          const priorityMapAsc: Record<string, number> = { 'high': 3, 'medium': 2, 'low': 1 };
          const aPriorityAsc = a.priority ? priorityMapAsc[a.priority] || 0 : 0;
          const bPriorityAsc = b.priority ? priorityMapAsc[b.priority] || 0 : 0;
          return aPriorityAsc - bPriorityAsc;

        case 'newest':
          return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();

        case 'oldest':
          return new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime();

        case 'title-asc':
          return a.title.localeCompare(b.title);

        default:
          return 0;
      }
    });
  }, [tasks, sortOption]);

  // Memoized sorted tasks for dashboard (recent tasks only)
  const dashboardSortedTasks = useMemo(() => {
    if (!allTasks) return [];

    return [...allTasks].sort((a, b) => {
      return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
    });
  }, [allTasks]);

  if (authLoading || !isMounted) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12">
        <div className="text-center">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-indigo-600 border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12">
        <div className="text-center max-w-md mx-auto p-8 bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Please log in to access the dashboard</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">Sign in to view your productivity overview.</p>
          <Link href="/login" className="inline-block px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all transform hover:scale-105 shadow-lg">
            Go to Login
          </Link>
        </div>
      </div>
    );
  }

  // Calculate stats based on all tasks (not filtered)
  const completedTasks = allTasks.filter(task => task.completed).length;
  const pendingTasks = allTasks.filter(task => !task.completed).length;
  const totalTasks = allTasks.length;

  // Priority tasks
  const priorityTasks = allTasks.filter(task => task.priority === 'high');

  return (
    <div className="min-h-screen w-full bg-gray-50 dark:bg-gray-900 flex">
      {/* Sidebar */}
      <Sidebar
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
        onAddTaskClick={() => setIsModalOpen(true)}
        currentView={currentView}
        setCurrentView={setCurrentView}
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4 flex-1">
              <Button
                variant="outline"
                size="sm"
                className="lg:hidden"
                onClick={() => setSidebarOpen(!sidebarOpen)}
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </Button>

              <div className="w-full max-w-3xl">
                <Input
                  placeholder="Find tasks, tags or descriptions..."
                  className="w-full bg-gray-50 dark:bg-gray-700 border-gray-300 dark:border-gray-600"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  leftIcon={<Search className="h-5 w-5 text-gray-400" />}
                />
              </div>
            </div>

            <div className="flex items-center space-x-3">
              {/* Notification Bell Icon */}
              <button
                onClick={handleNotificationClick}
                className="relative p-2 text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-200 transition-colors rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
                aria-label="Notifications"
              >
                <Bell className="h-6 w-6" />
                {pendingRemindersCount > 0 && (
                  <span className="absolute top-1 right-1 flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
                  </span>
                )}
              </button>

              {/* User Avatar */}
              <div className="h-8 w-8 rounded-full bg-indigo-100 dark:bg-indigo-900 flex items-center justify-center text-indigo-600 dark:text-indigo-300 text-sm font-medium">
                {user?.name?.charAt(0)?.toUpperCase() || user?.email?.charAt(0)?.toUpperCase() || 'U'}
              </div>
              <div className="hidden md:block">
                <p className="text-sm font-medium text-gray-900 dark:text-white">{user.name || user.email}</p>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto p-6">
          <div className="w-full">
            {/* Conditional rendering based on current view */}
            {currentView === 'dashboard' && (
              <div>
                {/* Welcome Message */}
                <motion.div
                  initial={{ opacity: 0, y: -20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                  className="mb-8"
                >
                  <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Good morning, {user.name || 'Alex'}! 👋</h1>
                  <p className="text-gray-600 dark:text-gray-400 mt-2">
                    You have {pendingTasks} tasks pending today. Let's get them done!
                  </p>
                </motion.div>

                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.1 }}
                  >
                    <Card>
                      <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
                        <CardTitle className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Tasks</CardTitle>
                        <TrendingUp className="h-5 w-5 text-indigo-500" />
                      </CardHeader>
                      <CardContent>
                        <div className="text-2xl font-bold">{totalTasks}</div>
                        <p className="text-xs text-gray-500 dark:text-gray-400">All your tasks</p>
                      </CardContent>
                    </Card>
                  </motion.div>

                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                  >
                    <Card>
                      <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
                        <CardTitle className="text-sm font-medium text-gray-500 dark:text-gray-400">Completed</CardTitle>
                        <CheckCircle className="h-5 w-5 text-green-500" />
                      </CardHeader>
                      <CardContent>
                        <div className="text-2xl font-bold text-green-600">{completedTasks}</div>
                        <p className="text-xs text-gray-500 dark:text-gray-400">Tasks finished</p>
                      </CardContent>
                    </Card>
                  </motion.div>

                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.3 }}
                  >
                    <Card>
                      <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
                        <CardTitle className="text-sm font-medium text-gray-500 dark:text-gray-400">Pending</CardTitle>
                        <Circle className="h-5 w-5 text-yellow-500" />
                      </CardHeader>
                      <CardContent>
                        <div className="text-2xl font-bold text-yellow-600">{pendingTasks}</div>
                        <p className="text-xs text-gray-500 dark:text-gray-400">Tasks to do</p>
                      </CardContent>
                    </Card>
                  </motion.div>
                </div>

                {/* Recent Tasks Section */}
                <div className="mb-8">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white">RECENT TASKS</h2>
                    <Button className="flex items-center gap-2 bg-blue-900 hover:bg-blue-800" onClick={() => setIsModalOpen(true)}>
                      Add Task
                    </Button>
                  </div>

                  <div className="space-y-4">
                    {dashboardSortedTasks.slice(0, 5).map((task, index) => (
                      <motion.div
                        key={task.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.3, delay: 0.05 * index }}
                        className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden"
                      >
                        <div className="flex">
                          <div className="flex-1 p-4">
                            <div className="flex items-start gap-3">
                              <input
                                type="checkbox"
                                checked={task.completed}
                                onChange={(e) => {
                                  if (e.target.checked) {
                                    markTaskComplete(task.id);
                                  } else {
                                    markTaskIncomplete(task.id);
                                  }
                                }}
                                className="mt-1 h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                              />
                              <div className="flex-1">
                                {task.priority && (
                                  <>
                                    {console.log(`Task ${task.id} priority:`, task.priority)} {/* Debugging log */}
                                    <span className={`${
                                      task.priority === 'high'
                                        ? 'bg-red-100 text-red-800 border-red-200'
                                        : task.priority === 'medium'
                                          ? 'bg-yellow-100 text-yellow-800 border-yellow-200'
                                          : task.priority === 'low'
                                            ? 'bg-green-100 text-green-800 border-green-200'
                                            : 'bg-gray-100 text-gray-800 border-gray-200'
                                    } rounded px-2 py-1 text-xs font-medium mr-2 mb-2`}>
                                      {task.priority.toUpperCase()}
                                    </span>
                                  </>
                                )}

                                <h3 className={`text-lg font-medium ${
                                  task.completed ? 'text-gray-500 line-through' : 'text-gray-900 dark:text-white'
                                }`}>
                                  {task.title}
                                </h3>
                                <div className="flex items-center gap-2 mt-2 text-sm w-full flex-wrap">
                                  <div className="flex flex-wrap gap-1">
                                    {task.tags && task.tags.split(',').filter(tag => tag.trim() !== '').map((tag, idx) => (
                                      <span key={idx} className="text-xs px-2 py-1 rounded-full bg-purple-100 text-purple-800 border border-purple-200">
                                        {tag.trim()}
                                      </span>
                                    ))}
                                    {task.dueDate && (
                                      <span className="flex items-center gap-1">
                                        <Calendar className="h-4 w-4 text-gray-500 dark:text-gray-400" />
                                        {(() => {
                                          console.log(`Task ${task.id} dueDate:`, task.dueDate); // Debug log
                                          try {
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
                                                    {dueDate.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })}
                                                  </span>
                                                  <span className="text-red-600 dark:text-red-400 text-xs">(Overdue)</span>
                                                </>
                                              );
                                            } else {
                                              return (
                                                <span className="text-gray-500 dark:text-gray-400">
                                                  {dueDate.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })}
                                                </span>
                                              );
                                            }
                                          } catch (error) {
                                            console.error(`Error parsing due date for task ${task.id}:`, error); // Debug log
                                            // If there's an error parsing the date, show the raw date
                                            return <span className="text-gray-500 dark:text-gray-400">{task.dueDate}</span>;
                                          }
                                        })()}
                                      </span>
                                    )}
                                  </div>
                                </div>

                                {task.description && (
                                  <p className={`text-gray-600 dark:text-gray-400 mt-1 ${
                                    task.completed ? 'line-through' : ''
                                  } line-clamp-2`}>
                                    {task.description}
                                  </p>
                                )}
                              </div>
                            </div>
                          </div>
                        </div>
                      </motion.div>
                    ))}

                    {allTasks.length === 0 && (
                      <div className="text-center py-12">
                        <div className="w-16 h-16 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                          <CheckCircle className="h-8 w-8 text-white" />
                        </div>
                        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">No tasks yet</h3>
                        <p className="text-gray-600 dark:text-gray-400 mb-4">Get started by creating your first task.</p>
                        <Button onClick={() => setIsModalOpen(true)}>
                          <Plus className="mr-2 h-4 w-4" />
                          Create Task
                        </Button>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}

            {currentView === 'all-tasks' && (
              <div>
                {/* Task Filters */}
                <div className="mb-6">
                  <div className="flex flex-wrap gap-2 mb-6">
                    <button
                      onClick={() => setFilter('all')}
                      className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                        filter === 'all' && !searchTerm
                          ? 'bg-indigo-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
                      }`}
                    >
                      All
                    </button>
                    <button
                      onClick={() => setFilter('active')}
                      className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                        filter === 'active'
                          ? 'bg-indigo-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
                      }`}
                    >
                      Active
                    </button>
                    <button
                      onClick={() => setFilter('completed')}
                      className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                        filter === 'completed'
                          ? 'bg-indigo-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
                      }`}
                    >
                      Completed
                    </button>
                    <button
                      onClick={() => setFilter('high-priority')}
                      className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                        filter === 'high-priority'
                          ? 'bg-red-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
                      }`}
                    >
                      High Priority
                    </button>
                    <button
                      onClick={() => setFilter('recurring')}
                      className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                        filter === 'recurring'
                          ? 'bg-purple-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
                      }`}
                    >
                      Recurring
                    </button>
                    <button
                      onClick={() => setFilter('overdue')}
                      className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                        filter === 'overdue'
                          ? 'bg-orange-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
                      }`}
                    >
                      Overdue
                    </button>
                  </div>

                  {/* Add Task Button */}
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                      {filter === 'all' && !searchTerm ? 'All Tasks' :
                       filter === 'active' ? 'Active Tasks' :
                       filter === 'completed' ? 'Completed Tasks' :
                       filter === 'high-priority' ? 'High Priority Tasks' :
                       filter === 'recurring' ? 'Recurring Tasks' :
                       filter === 'overdue' ? 'Overdue Tasks' :
                       filter === 'today' ? 'Today\'s Tasks' :
                       filter === 'upcoming' ? 'Upcoming Tasks' : 'Tasks'}
                      <span className="bg-gray-100 text-gray-800 text-sm px-2 py-1 rounded-full ml-2 dark:bg-gray-700 dark:text-gray-200">
                        {tasks.length}
                      </span>
                    </h2>
                    <div className="flex items-center gap-1.5">
                      <div className="relative">
                        <select
                          value={sortOption}
                          onChange={(e) => setSortOption(e.target.value)}
                          className="px-4 py-2.5 text-base h-11 w-56 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 appearance-none bg-white dark:bg-gray-800 dark:border-gray-600 dark:text-white"
                        >
                          <option value="dueDate-asc">Due Date (ascending)</option>
                          <option value="dueDate-desc">Due Date (descending)</option>
                          <option value="priority-desc">Priority (High to Low)</option>
                          <option value="priority-asc">Priority (Low to High)</option>
                          <option value="newest">Newest First</option>
                          <option value="oldest">Oldest First</option>
                          <option value="title-asc">Title (A-Z)</option>
                        </select>
                        <svg className="absolute right-2 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                        </svg>
                      </div>
                      <Button className="flex items-center gap-2 bg-blue-900 hover:bg-blue-800" onClick={() => setIsModalOpen(true)}>
                        Add Task
                      </Button>
                    </div>
                  </div>

                  {/* Task List */}
                  <div className="space-y-4">
                    {sortedTasks.map((task, index) => (
                      <motion.div
                        key={task.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.3, delay: 0.05 * index }}
                        className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden"
                      >
                        <div className="flex">
                          <div className="flex-1 p-4">
                            <div className="flex items-start gap-3">
                              <input
                                type="checkbox"
                                checked={task.completed}
                                onChange={(e) => {
                                  if (e.target.checked) {
                                    markTaskComplete(task.id);
                                  } else {
                                    markTaskIncomplete(task.id);
                                  }
                                }}
                                className="mt-1 h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                              />
                              <div className="flex-1">
                                {task.priority && (
                                  <>
                                    {console.log(`Task ${task.id} priority:`, task.priority)} {/* Debugging log */}
                                    <span className={`${
                                      task.priority === 'high'
                                        ? 'bg-red-100 text-red-800 border-red-200'
                                        : task.priority === 'medium'
                                          ? 'bg-yellow-100 text-yellow-800 border-yellow-200'
                                          : task.priority === 'low'
                                            ? 'bg-green-100 text-green-800 border-green-200'
                                            : 'bg-gray-100 text-gray-800 border-gray-200'
                                    } rounded px-2 py-1 text-xs font-medium mr-2 mb-2`}>
                                      {task.priority.toUpperCase()}
                                    </span>
                                  </>
                                )}

                                <h3 className={`text-lg font-medium ${
                                  task.completed ? 'text-gray-500 line-through' : 'text-gray-900 dark:text-white'
                                }`}>
                                  {task.title}
                                </h3>
                                <div className="flex items-center gap-2 mt-2 text-sm w-full flex-wrap">
                                  <div className="flex flex-wrap gap-1">
                                    {task.tags && task.tags.split(',').filter(tag => tag.trim() !== '').map((tag, idx) => (
                                      <span key={idx} className="text-xs px-2 py-1 rounded-full bg-purple-100 text-purple-800 border border-purple-200">
                                        {tag.trim()}
                                      </span>
                                    ))}
                                    {task.dueDate && (
                                      <span className="flex items-center gap-1">
                                        <Calendar className="h-4 w-4 text-gray-500 dark:text-gray-400" />
                                        {(() => {
                                          console.log(`Task ${task.id} dueDate:`, task.dueDate); // Debug log
                                          try {
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
                                                    {dueDate.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })}
                                                  </span>
                                                  <span className="text-red-600 dark:text-red-400 text-xs">(Overdue)</span>
                                                </>
                                              );
                                            } else {
                                              return (
                                                <span className="text-gray-500 dark:text-gray-400">
                                                  {dueDate.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })}
                                                </span>
                                              );
                                            }
                                          } catch (error) {
                                            console.error(`Error parsing due date for task ${task.id}:`, error); // Debug log
                                            // If there's an error parsing the date, show the raw date
                                            return <span className="text-gray-500 dark:text-gray-400">{task.dueDate}</span>;
                                          }
                                        })()}
                                      </span>
                                    )}
                                  </div>
                                </div>

                                {task.description && (
                                  <p className={`text-gray-600 dark:text-gray-400 mt-1 ${
                                    task.completed ? 'line-through' : ''
                                  } line-clamp-2`}>
                                    {task.description}
                                  </p>
                                )}
                              </div>
                              <div className="flex items-center gap-2 ml-4">
                                <button
                                  onClick={() => {
                                  // Set task to edit and open modal
                                  setEditingTask(task);
                                  setIsEditing(true);
                                  setIsModalOpen(true);
                                }}
                                  className="text-gray-500 hover:text-blue-600 transition-colors"
                                  aria-label="Edit task"
                                >
                                  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                  </svg>
                                </button>
                                <button
                                  onClick={() => deleteTask(task.id)}
                                  className="text-gray-500 hover:text-red-600 transition-colors"
                                  aria-label="Delete task"
                                >
                                  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                  </svg>
                                </button>
                              </div>
                            </div>
                          </div>
                        </div>
                      </motion.div>
                    ))}

                    {sortedTasks.length === 0 && (
                      <div className="text-center py-12">
                        <div className="w-16 h-16 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                          <CheckCircle className="h-8 w-8 text-white" />
                        </div>
                        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">No tasks found</h3>
                        <p className="text-gray-600 dark:text-gray-400 mb-4">
                          {searchTerm ? 'No tasks match your search.' :
                           filter === 'completed' ? 'You haven\'t completed any tasks yet.' :
                           'You don\'t have any tasks right now.'}
                        </p>
                        <Button onClick={() => setIsModalOpen(true)}>
                          <Plus className="mr-2 h-4 w-4" />
                          Create Task
                        </Button>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}

          </div>
        </main>
      </div>


      {/* Task Form Modal */}
      <TaskFormModal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setEditingTask(null);
          setIsEditing(false);
        }}
        onSubmit={isEditing ? handleUpdateTask : handleCreateTask}
        initialData={editingTask || undefined}
        submitLabel={editingTask ? 'Update Task' : 'Create Task'}
        loading={modalLoading}
      />
    </div>
  );
}