'use client';

import { useState, useEffect } from 'react';
import { TaskFormValues } from '../../lib/types';

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
  const [formData, setFormData] = useState<TaskFormValues>({
    title: initialData.title || '',
    description: initialData.description || ''
  });

  useEffect(() => {
    setFormData({
      title: initialData.title || '',
      description: initialData.description || ''
    });
  }, [initialData]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="p-6">
      <div className="mb-4">
        <label htmlFor="title" className="block text-sm font-medium text-[--text-secondary] mb-2">
          Task Title *
        </label>
        <input
          type="text"
          id="title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          className="w-full px-4 py-3 bg-white/50 border border-[--border-light] rounded-lg focus:outline-none focus:ring-2 focus:ring-[--color-primary]/50 focus:border-[--color-primary] transition-all"
          placeholder="What needs to be done?"
          required
        />
      </div>
      <div className="mb-6">
        <label htmlFor="description" className="block text-sm font-medium text-[--text-secondary] mb-2">
          Description (Optional)
        </label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          className="w-full px-4 py-3 bg-white/50 border border-[--border-light] rounded-lg focus:outline-none focus:ring-2 focus:ring-[--color-primary]/50 focus:border-[--color-primary] transition-all"
          placeholder="Add details..."
          rows={3}
        />
      </div>
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