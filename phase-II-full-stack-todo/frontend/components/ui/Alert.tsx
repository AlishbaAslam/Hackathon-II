'use client';

import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  InformationCircleIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon,
  XMarkIcon,
} from '@heroicons/react/24/outline';

interface AlertProps {
  type?: 'info' | 'success' | 'warning' | 'error';
  title?: string;
  children: React.ReactNode;
  onClose?: () => void;
  dismissible?: boolean;
  autoDismiss?: boolean;
  autoDismissDelay?: number;
  className?: string;
}

export default function Alert({
  type = 'info',
  title,
  children,
  onClose,
  dismissible = true,
  autoDismiss = false,
  autoDismissDelay = 5000,
  className = '',
}: AlertProps) {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    if (autoDismiss && onClose) {
      const timer = setTimeout(() => {
        handleClose();
      }, autoDismissDelay);
      return () => clearTimeout(timer);
    }
  }, [autoDismiss, autoDismissDelay, onClose]);

  const handleClose = () => {
    setIsVisible(false);
    setTimeout(() => {
      onClose?.();
    }, 300);
  };

  const typeClasses = {
    info: {
      bg: 'bg-[--color-secondary]/10',
      border: 'border-[--color-secondary]/20',
      text: 'text-[--color-secondary]',
      icon: 'text-[--color-secondary]',
      hover: 'hover:bg-[--color-secondary]/20',
      ring: 'focus:ring-[--color-secondary]',
      shadow: 'shadow-[--color-secondary]/10',
    },
    success: {
      bg: 'bg-[--color-success]/10',
      border: 'border-[--color-success]/20',
      text: 'text-[--color-success]',
      icon: 'text-[--color-success]',
      hover: 'hover:bg-[--color-success]/20',
      ring: 'focus:ring-[--color-success]',
      shadow: 'shadow-[--color-success]/10',
    },
    warning: {
      bg: 'bg-[--color-warning]/10',
      border: 'border-[--color-warning]/20',
      text: 'text-[--color-warning]',
      icon: 'text-[--color-warning]',
      hover: 'hover:bg-[--color-warning]/20',
      ring: 'focus:ring-[--color-warning]',
      shadow: 'shadow-[--color-warning]/10',
    },
    error: {
      bg: 'bg-[--color-error]/10',
      border: 'border-[--color-error]/20',
      text: 'text-[--color-error]',
      icon: 'text-[--color-error]',
      hover: 'hover:bg-[--color-error]/20',
      ring: 'focus:ring-[--color-error]',
      shadow: 'shadow-[--color-error]/10',
    },
  };

  const typeIcons = {
    info: InformationCircleIcon,
    success: CheckCircleIcon,
    warning: ExclamationTriangleIcon,
    error: XCircleIcon,
  };

  const styles = typeClasses[type];
  const Icon = typeIcons[type];

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, y: -20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -20, scale: 0.95 }}
          transition={{ duration: 0.3, ease: 'easeOut' }}
          className={`
            relative overflow-hidden rounded-xl border ${styles.border} ${styles.bg}
            shadow-lg ${styles.shadow} ${className}
          `}
        >
          {/* Animated gradient border effect */}
          <motion.div
            className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"
            animate={{
              x: ['-100%', '100%'],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              repeatDelay: 3,
            }}
            style={{ width: '200%' }}
          />

          <div className="relative flex items-start p-4">
            <div className={`flex-shrink-0 ${styles.icon}`}>
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.1, type: 'spring', stiffness: 200 }}
              >
                <Icon className="h-5 w-5" aria-hidden="true" />
              </motion.div>
            </div>

            <div className="ml-3 flex-1">
              {title && (
                <motion.h3
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.1 }}
                  className={`text-sm font-semibold ${styles.text}`}
                >
                  {title}
                </motion.h3>
              )}
              <motion.div
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: title ? 0.15 : 0.1 }}
                className={`mt-1 text-sm ${styles.text}`}
              >
                {children}
              </motion.div>
            </div>

            {dismissible && (
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2 }}
                className="ml-4 flex-shrink-0"
              >
                <button
                  type="button"
                  onClick={handleClose}
                  className={`
                    inline-flex rounded-lg p-1.5
                    ${styles.bg} ${styles.text} ${styles.hover}
                    focus:outline-none focus-visible:ring-2 ${styles.ring}
                    transition-colors duration-150
                  `}
                  aria-label="Dismiss"
                >
                  <XMarkIcon className="h-4 w-4" aria-hidden="true" />
                </button>
              </motion.div>
            )}
          </div>

          {/* Progress bar for auto-dismiss */}
          {autoDismiss && (
            <motion.div
              className={`absolute bottom-0 left-0 h-1 ${(styles.icon.includes('[--color-secondary]') ? 'bg-[--color-secondary]' :
                styles.icon.includes('[--color-success]') ? 'bg-[--color-success]' :
                styles.icon.includes('[--color-warning]') ? 'bg-[--color-warning]' :
                'bg-[--color-error]')}`}
              initial={{ scaleX: 1 }}
              animate={{ scaleX: 0 }}
              transition={{ duration: autoDismissDelay / 1000, ease: 'linear' }}
            />
          )}
        </motion.div>
      )}
    </AnimatePresence>
  );
}

// Hook for managing alerts
export function useAlert() {
  const [alert, setAlert] = useState<{
    type: 'info' | 'success' | 'warning' | 'error';
    message: string;
    title?: string;
  } | null>(null);

  const showAlert = (type: 'info' | 'success' | 'warning' | 'error', message: string, title?: string) => {
    setAlert({ type, message, title });
  };

  const hideAlert = () => {
    setAlert(null);
  };

  return { alert, showAlert, hideAlert };
}
