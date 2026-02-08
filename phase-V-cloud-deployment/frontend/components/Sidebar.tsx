'use client';

import { Plus, BookOpen, CheckCircle, LogOut } from 'lucide-react';
import Button from '@/components/ui/Button';
import Link from 'next/link';
import { useAuth } from '../hooks/useAuth';

interface SidebarProps {
  sidebarOpen: boolean;
  setSidebarOpen: React.Dispatch<React.SetStateAction<boolean>>;
  onAddTaskClick: () => void;
  currentView: 'dashboard' | 'all-tasks';
  setCurrentView: React.Dispatch<React.SetStateAction<'dashboard' | 'all-tasks'>>;
}

export default function Sidebar({
  sidebarOpen,
  setSidebarOpen,
  onAddTaskClick,
  currentView,
  setCurrentView
}: SidebarProps) {
  const { logout, user } = useAuth();

  return (
    <aside className={`bg-white dark:bg-gray-800 border-r border-t border-gray-200 dark:border-gray-700 transition-all duration-300 ${sidebarOpen ? 'w-64 pt-5' : 'w-20'} flex flex-col`}>
      <div className={`p-4 border-b border-gray-200 dark:border-gray-700 flex items-center ${sidebarOpen ? 'justify-start mt-0 pt-0' : 'justify-center'}`}>
        <button
          className="p-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white flex items-center justify-center"
          onClick={() => setSidebarOpen(!sidebarOpen)}
        >
          <svg className={`${sidebarOpen ? 'h-7 w-7' : 'h-8 w-8'} transition-all duration-300`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        {sidebarOpen && (
          <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent hover:cursor-pointer ml-3 transition-all duration-300">
            TodoFlow
          </Link>
        )}
      </div>

      <nav className="flex-1 p-4 space-y-2">
        <button
          onClick={onAddTaskClick}
          className="w-full flex items-center justify-center gap-3 px-3 py-2 bg-indigo-600 text-white dark:text-gray-300 rounded-lg mb-4 hover:bg-indigo-700 transition-colors duration-200 ease-in-out"
        >
          <Plus className={`${sidebarOpen ? 'h-5 w-5' : 'h-6 w-6'} transition-all duration-300`} />
          {sidebarOpen && <span>Add Task</span>}
        </button>

        <button
          onClick={() => setCurrentView('dashboard')}
          className={`flex items-center ${sidebarOpen ? 'justify-start' : 'justify-center'} gap-3 px-3 py-2 rounded-lg w-full text-left ${
            currentView === 'dashboard'
              ? 'bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300'
              : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
          }`}
        >
          <BookOpen className={`${sidebarOpen ? 'h-5 w-5' : 'h-6 w-6'} transition-all duration-300`} />
          {sidebarOpen && <span>Dashboard</span>}
        </button>

        <button
          onClick={() => setCurrentView('all-tasks')}
          className={`flex items-center ${sidebarOpen ? 'justify-start' : 'justify-center'} gap-3 px-3 py-2 rounded-lg w-full text-left ${
            currentView === 'all-tasks'
              ? 'bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300'
              : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
          }`}
        >
          <CheckCircle className={`${sidebarOpen ? 'h-5 w-5' : 'h-6 w-6'} transition-all duration-300`} />
          {sidebarOpen && <span>My Tasks</span>}
        </button>
      </nav>

      <div className="p-4 mt-auto">
        <button
          onClick={logout}
          className={`w-full flex items-center ${sidebarOpen ? 'justify-start' : 'justify-center'} gap-3 px-3 py-3 rounded-lg text-left text-indigo-600 hover:bg-indigo-50 dark:text-indigo-400 dark:hover:bg-indigo-900/20`}
        >
          <div className={`flex items-center justify-center flex-shrink-0 ${sidebarOpen ? 'h-10 w-10' : 'h-12 w-12'} rounded-full bg-indigo-100 dark:bg-indigo-900 text-indigo-600 dark:text-indigo-300 text-base font-medium transition-all duration-300`}>
            {user?.name?.charAt(0)?.toUpperCase() || user?.email?.charAt(0)?.toUpperCase() || 'U'}
          </div>
          {sidebarOpen && <span className="text-sm font-medium">Logout</span>}
        </button>
      </div>
    </aside>
  );
}