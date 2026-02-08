'use client';

import { ReactNode } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { useRouter } from 'next/navigation';

interface DashboardLayoutProps {
  children: ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const { logout } = useAuth();
  const router = useRouter();

  const handleLogout = async () => {
    try {
      await logout();
      router.push('/login');
      router.refresh();
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };
  return (
    <div className="h-screen w-screen bg-gradient-to-br from-[--background-gradient-start] to-[--background-gradient-end] overflow-hidden flex flex-col">
      <div className="flex-1 overflow-y-auto w-full">
        <div className="w-full h-full">
          {children}
        </div>
      </div>
    </div>
  );
}