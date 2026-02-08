'use client';

import { forwardRef, useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  variant?: 'default' | 'outlined' | 'filled';
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      error,
      helperText,
      variant = 'default',
      leftIcon,
      rightIcon,
      className = '',
      id,
      value,
      defaultValue,
      onChange,
      ...props
    },
    ref
  ) => {
    const [isFocused, setIsFocused] = useState(false);
    const [hasValue, setHasValue] = useState(!!value || !!defaultValue);
    const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;
    const inputRef = useRef<HTMLInputElement>(null);

    // Sync hasValue with value changes
    useEffect(() => {
      setHasValue(!!value && String(value).length > 0);
    }, [value]);

    // Check if input has content on mount
    useEffect(() => {
      if (defaultValue || value) {
        setHasValue(true);
      }
    }, [defaultValue, value]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setHasValue(e.target.value.length > 0);
      onChange?.(e);
    };

    const baseClasses = `
      w-full px-4 py-3 bg-white rounded-lg
      text-gray-900 placeholder-gray-400
      transition-all duration-200
      focus:outline-none
    `;

    const variantClasses = {
      default: `
        border border-gray-200
        focus:ring-2 focus:ring-[--color-primary]/20 focus:border-[--color-primary]
        hover:border-gray-300
      `,
      outlined: `
        border-2 border-gray-200
        focus:ring-2 focus:ring-[--color-primary]/20 focus:border-[--color-primary]
        hover:border-gray-300
      `,
      filled: `
        border border-transparent
        bg-gray-50
        focus:ring-2 focus:ring-[--color-primary]/20 focus:bg-white
        hover:bg-gray-100
      `,
    };

    const errorClasses = error ? 'border-red-500 focus:ring-red-500/20 focus:border-red-500' : '';

    const inputClasses = [
      baseClasses,
      variantClasses[variant],
      errorClasses,
      leftIcon ? 'pl-10' : '',
      rightIcon ? 'pr-10' : '',
      className,
    ].filter(Boolean).join(' ');

    const labelClasses = `
      absolute left-4 top-3.5 pointer-events-none
      transition-all duration-200 ease-out
      text-gray-500
      ${isFocused || hasValue
        ? '-top-2 left-2 text-xs bg-white px-1.5 text-[--color-primary] font-medium'
        : ''
      }
      ${error ? 'text-red-500' : ''}
    `;

    return (
      <div className="w-full relative">
        {/* Input container */}
        <div className="relative">
          {/* Left icon */}
          {leftIcon && (
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none z-10">
              {leftIcon}
            </div>
          )}

          {/* Floating label or regular label */}
          {label ? (
            <div className="relative">
              <motion.label
                htmlFor={inputId}
                className={labelClasses}
                animate={{
                  scale: isFocused || hasValue ? 0.875 : 1,
                }}
                transition={{ duration: 0.2 }}
              >
                {label}
              </motion.label>
              <input
                ref={inputRef}
                id={inputId}
                className={inputClasses}
                onFocus={() => setIsFocused(true)}
                onBlur={() => setIsFocused(false)}
                onChange={handleChange}
                value={value}
                defaultValue={defaultValue}
                {...props}
              />
            </div>
          ) : (
            <input
              ref={inputRef}
              id={inputId}
              className={inputClasses}
              onFocus={() => setIsFocused(true)}
              onBlur={() => setIsFocused(false)}
              onChange={handleChange}
              value={value}
              defaultValue={defaultValue}
              {...props}
            />
          )}

          {/* Right icon */}
          {rightIcon && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none z-10">
              {rightIcon}
            </div>
          )}
        </div>

        {/* Error message with animation */}
        <AnimatePresence mode="wait">
          {error && (
            <motion.p
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="mt-1.5 text-sm text-red-500 flex items-center gap-1"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              {error}
            </motion.p>
          )}
        </AnimatePresence>

        {/* Helper text */}
        {!error && helperText && (
          <p className="mt-1.5 text-sm text-gray-500">{helperText}</p>
        )}

        {/* Focus ring effect */}
        {isFocused && !error && (
          <motion.div
            className="absolute inset-0 rounded-lg -z-10"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.2 }}
          >
            <div className="absolute inset-0 rounded-lg shadow-[0_0_0_4px_rgba(var(--color-primary-rgb),0.1)]" />
          </motion.div>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;
