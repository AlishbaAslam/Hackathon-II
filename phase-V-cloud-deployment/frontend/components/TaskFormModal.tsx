'use client';

import { Fragment, useState, useEffect, useRef } from 'react';
import { Dialog, Transition } from '@headlessui/react';
import { TaskFormValues } from '../lib/types';

interface TaskFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: TaskFormValues) => void;
  initialData?: TaskFormValues;
  submitLabel?: string;
  loading?: boolean;
}

export default function TaskFormModal({
  isOpen,
  onClose,
  onSubmit,
  initialData = { title: '', description: '' },
  submitLabel = 'Create Task',
  loading = false
}: TaskFormModalProps) {
  // Convert dates to the correct format for the datetime-local input for initial state
  const initialDueDate = initialData.dueDate ? new Date(initialData.dueDate).toISOString().slice(0, 16) : '';
  const initialRemindAt = initialData.remindAt ? new Date(initialData.remindAt).toISOString().slice(0, 16) : '';

  const [formData, setFormData] = useState<TaskFormValues>({
    title: initialData.title || '',
    description: initialData.description || '',
    priority: initialData.priority || 'medium',
    dueDate: initialDueDate,
    tags: initialData.tags || '',
    isRecurring: initialData.isRecurring || false,
    recurrencePattern: initialData.recurrencePattern || 'daily',
    remindAt: initialRemindAt
  });

  const [tagsInput, setTagsInput] = useState(initialData.tags || '');
  const [isTagsFocused, setIsTagsFocused] = useState(false);
  const prevIsOpenRef = useRef(isOpen);

  // Update form data when initialData changes and modal is opening (for edit mode)
  useEffect(() => {
    // Check if modal just opened (transitioned from closed to open)
    const prevIsOpen = prevIsOpenRef.current;

    // Only update when the modal is transitioning from closed to open
    if (isOpen && !prevIsOpen && initialData) {
      // Convert dates to the correct format for the datetime-local input
      const formattedDueDate = initialData.dueDate ? new Date(initialData.dueDate).toISOString().slice(0, 16) : '';
      const formattedRemindAt = initialData.remindAt ? new Date(initialData.remindAt).toISOString().slice(0, 16) : '';

      console.log('Setting edit dueDate:', initialData.dueDate, '→', formattedDueDate); // Debug
      console.log('Setting edit remindAt:', initialData.remindAt, '→', formattedRemindAt); // Debug

      setFormData({
        title: initialData.title || '',
        description: initialData.description || '',
        priority: initialData.priority || 'medium',
        dueDate: formattedDueDate,
        tags: initialData.tags || '',
        isRecurring: initialData.isRecurring || false,
        recurrencePattern: initialData.recurrencePattern || 'daily',
        remindAt: formattedRemindAt
      });
      setTagsInput(initialData.tags || '');
    }

    // Update the ref to current value for next render
    prevIsOpenRef.current = isOpen;
  }, [isOpen, initialData]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;

    if (type === 'checkbox') {
      const target = e.target as HTMLInputElement;
      setFormData(prev => ({
        ...prev,
        [name]: target.checked
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const handleTagsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTagsInput(e.target.value);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' || e.key === ',' || e.key === ' ') {
      e.preventDefault();
      if (tagsInput.trim() && !formData.tags?.includes(tagsInput.trim())) {
        const newTag = tagsInput.trim();
        const currentTags = formData.tags ? formData.tags.split(',').filter(tag => tag.trim() !== '') : [];
        const updatedTags = [...currentTags, newTag].filter(tag => tag.trim() !== '');
        setFormData(prev => ({
          ...prev,
          tags: updatedTags.join(',')
        }));
        setTagsInput('');
      }
    }
  };

  const removeTag = (tagToRemove: string) => {
    const currentTags = formData.tags ? formData.tags.split(',') : [];
    const updatedTags = currentTags.filter(tag => tag.trim() !== tagToRemove);
    setFormData(prev => ({
      ...prev,
      tags: updatedTags.join(',')
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Set tags from the input field
    const finalTags = tagsInput.trim() ?
      [...(formData.tags ? formData.tags.split(',') : []), tagsInput.trim()].filter(tag => tag.trim() !== '').join(',') :
      formData.tags;

    console.log('Submitting task with priority:', formData.priority); // Debugging log
    console.log('Sending is_recurring:', formData.isRecurring); // Debugging log

    onSubmit({
      ...formData,
      tags: finalTags
    });
  };

  return (
    <Transition show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4 text-center">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-0 text-left align-middle shadow-xl transition-all">
                <Dialog.Title
                  as="h3"
                  className="bg-gray-50 px-6 py-4 text-lg font-semibold leading-6 text-gray-900 border-b"
                >
                  {initialData.title ? 'Edit Task' : 'Add New Task'}
                </Dialog.Title>

                <form onSubmit={handleSubmit} className="p-6">
                  <div className="mb-4">
                    <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
                      Title *
                    </label>
                    <input
                      type="text"
                      id="title"
                      name="title"
                      value={formData.title}
                      onChange={handleChange}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Task title"
                    />
                  </div>

                  <div className="mb-4">
                    <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                      Description
                    </label>
                    <textarea
                      id="description"
                      name="description"
                      value={formData.description || ''}
                      onChange={handleChange}
                      rows={3}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Task description"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div>
                      <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-1">
                        Priority
                      </label>
                      <select
                        id="priority"
                        name="priority"
                        value={formData.priority}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                      </select>
                    </div>

                    <div>
                      <label htmlFor="dueDate" className="block text-sm font-medium text-gray-700 mb-1">
                        Due Date
                      </label>
                      <input
                        type="datetime-local"
                        id="dueDate"
                        name="dueDate"
                        value={formData.dueDate}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div>
                      <label htmlFor="remindAt" className="block text-sm font-medium text-gray-700 mb-1">
                        Remind At
                      </label>
                      <input
                        type="datetime-local"
                        id="remindAt"
                        name="remindAt"
                        value={formData.remindAt}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>

                    <div>
                      <label htmlFor="recurrencePattern" className="block text-sm font-medium text-gray-700 mb-1">
                        Recurring
                      </label>
                      <div className="flex items-center">
                        <input
                          type="checkbox"
                          id="isRecurring"
                          name="isRecurring"
                          checked={formData.isRecurring}
                          onChange={handleChange}
                          className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <label htmlFor="isRecurring" className="ml-2 text-sm text-gray-700">
                          Enable
                        </label>
                      </div>

                      {formData.isRecurring && (
                        <select
                          id="recurrencePattern"
                          name="recurrencePattern"
                          value={formData.recurrencePattern}
                          onChange={handleChange}
                          className="mt-2 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                          <option value="daily">Daily</option>
                          <option value="weekly">Weekly</option>
                          <option value="monthly">Monthly</option>
                          <option value="yearly">Yearly</option>
                        </select>
                      )}
                    </div>
                  </div>

                  <div className="mb-6">
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Tags
                    </label>
                    <div className="relative">
                      <input
                        type="text"
                        value={tagsInput}
                        onChange={handleTagsChange}
                        onKeyDown={handleKeyDown}
                        onFocus={() => setIsTagsFocused(true)}
                        onBlur={() => setIsTagsFocused(false)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        placeholder="Type a tag and press Enter, comma, or space"
                      />
                      {isTagsFocused && (
                        <div className="absolute z-10 mt-1 w-full bg-white shadow-lg rounded-md py-1 max-h-60 overflow-auto">
                          <p className="text-xs text-gray-500 px-3 py-2">Press Enter, comma, or space to add a tag</p>
                        </div>
                      )}
                    </div>

                    <div className="flex flex-wrap gap-2 mt-2">
                      {formData.tags?.split(',').filter(tag => tag.trim() !== '').map((tag, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 border border-blue-200"
                        >
                          #{tag.trim()}
                          <button
                            type="button"
                            onClick={() => removeTag(tag.trim())}
                            className="ml-1 text-blue-600 hover:text-blue-800"
                          >
                            ×
                          </button>
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="flex justify-end space-x-3">
                    <button
                      type="button"
                      onClick={onClose}
                      className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg border border-gray-300"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      disabled={loading}
                      className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg disabled:opacity-50"
                    >
                      {loading ? 'Saving...' : submitLabel}
                    </button>
                  </div>
                </form>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
}