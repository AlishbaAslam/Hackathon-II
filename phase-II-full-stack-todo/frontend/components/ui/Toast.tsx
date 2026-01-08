import { useEffect, useState } from 'react';
import { XMarkIcon } from '@heroicons/react/24/outline';

interface ToastProps {
  message: string;
  type?: 'info' | 'success' | 'warning' | 'error';
  duration?: number; // in milliseconds, default 3000ms
  onClose?: () => void;
}

export default function Toast({ message, type = 'info', duration = 3000, onClose }: ToastProps) {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        setVisible(false);
        if (onClose) onClose();
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  if (!visible) return null;

  // Define type-specific classes
  const typeClasses = {
    info: 'bg-[--color-secondary] text-white',
    success: 'bg-[--color-success] text-white',
    warning: 'bg-[--color-warning] text-white',
    error: 'bg-[--color-error] text-white',
  };

  return (
    <div className={`fixed top-4 right-4 p-4 rounded-md shadow-lg z-50 flex items-center ${typeClasses[type]}`}>
      <span className="mr-2">{message}</span>
      <button
        onClick={() => {
          setVisible(false);
          if (onClose) onClose();
        }}
        className="ml-2"
      >
        <XMarkIcon className="h-5 w-5" />
      </button>
    </div>
  );
}