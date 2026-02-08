'use client';

import { useForm } from 'react-hook-form';
import { TaskFormValues } from '../../lib/types';
import TagInput from './TagInput';
import DateTimePickers from './DateTimePickers';
import RecurrenceConfig from './RecurrenceConfig';

interface TaskFormProps {
  initialData?: TaskFormValues;
  onSubmit: (data: TaskFormValues) => void;
  onCancel?: () => void;
  submitLabel?: string;
  cancelLabel?: string;
  loading?: boolean;
}

export default function TaskForm({
  initialData = { title: '', description: '' },
  onSubmit,
  onCancel,
  submitLabel = 'Save Task',
  cancelLabel = 'Cancel',
  loading = false
}: TaskFormProps) {
  const {
    register,
    handleSubmit,
    setValue,
    watch,
    reset,
    formState: { errors }
  } = useForm<TaskFormValues>({
    defaultValues: {
      title: initialData.title || '',
      description: initialData.description || '',
      priority: initialData.priority || 'medium',
      dueDate: initialData.dueDate || '',
      tags: initialData.tags || '',
      isRecurring: initialData.isRecurring || false,
      recurrencePattern: initialData.recurrencePattern || 'daily',
      remindAt: initialData.remindAt || ''
    }
  });

  // Watch specific fields to conditionally render sections
  const isRecurring = watch('isRecurring') || false;

  // Handle form submission
  const handleFormSubmit = (data: TaskFormValues) => {
    onSubmit(data);
  };

  // Callback functions for the custom components
  const handleTagsChange = (tags: string) => {
    setValue('tags', tags);
  };

  const handleDueDateChange = (date: string) => {
    setValue('dueDate', date);
  };

  const handleReminderTimeChange = (time: string) => {
    setValue('remindAt', time);
  };

  const handleToggleRecurring = (enabled: boolean) => {
    setValue('isRecurring', enabled);
  };

  const handlePatternChange = (pattern: string) => {
    setValue('recurrencePattern', pattern);
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="p-6">
      <div className="mb-4">
        <label htmlFor="title" className="block text-sm font-medium text-[--text-secondary] mb-2">
          Task Title *
        </label>
        <input
          type="text"
          id="title"
          {...register('title', { required: 'Task title is required' })}
          className={`w-full px-4 py-3 bg-white/50 border ${
            errors.title ? 'border-red-500' : 'border-[--border-light]'
          } rounded-lg focus:outline-none focus:ring-2 focus:ring-[--color-primary]/50 focus:border-[--color-primary] transition-all`}
          placeholder="What needs to be done?"
        />
        {errors.title && (
          <p className="mt-1 text-sm text-red-500">{errors.title.message}</p>
        )}
      </div>

      <div className="mb-6">
        <label htmlFor="description" className="block text-sm font-medium text-[--text-secondary] mb-2">
          Description (Optional)
        </label>
        <textarea
          id="description"
          {...register('description')}
          className="w-full px-4 py-3 bg-white/50 border border-[--border-light] rounded-lg focus:outline-none focus:ring-2 focus:ring-[--color-primary]/50 focus:border-[--color-primary] transition-all"
          placeholder="Add details..."
          rows={3}
        />
      </div>

      {/* Priority Selection */}
      <div className="mb-4">
        <label htmlFor="priority" className="block text-sm font-medium text-[--text-secondary] mb-2">
          Priority
        </label>
        <select
          id="priority"
          {...register('priority')}
          className="w-full px-4 py-3 bg-white/50 border border-[--border-light] rounded-lg focus:outline-none focus:ring-2 focus:ring-[--color-primary]/50 focus:border-[--color-primary] transition-all"
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>

      {/* Date and Time Pickers */}
      <div className="mb-4">
        <DateTimePickers
          dueDateValue={watch('dueDate')}
          reminderTimeValue={watch('remindAt')}
          onDueDateChange={handleDueDateChange}
          onReminderTimeChange={handleReminderTimeChange}
        />
      </div>

      {/* Tags Input */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-[--text-secondary] mb-2">
          Tags (Optional)
        </label>
        <TagInput
          value={watch('tags')}
          onChange={handleTagsChange}
          placeholder="Enter tags (press Enter, comma, or space to add)"
        />
      </div>

      {/* Recurring Task Configuration */}
      <RecurrenceConfig
        isRecurringValue={isRecurring}
        recurrencePatternValue={watch('recurrencePattern') || 'daily'}
        onToggleRecurring={handleToggleRecurring}
        onPatternChange={handlePatternChange}
      />

      <div className="flex gap-3">
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-3 bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white rounded-lg hover:from-[--color-primary-dark] hover:to-[--color-accent] transition-all shadow-[--glow-card] disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Saving...' : submitLabel}
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="px-6 py-3 bg-white text-[--text-primary] rounded-lg border border-[--border-light] hover:border-[--color-primary] transition-all"
          >
            {cancelLabel}
          </button>
        )}
      </div>
    </form>
  );
}