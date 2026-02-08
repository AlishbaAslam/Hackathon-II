'use client';

import { useState } from 'react';
import TaskForm from './TaskForm';
import { TaskFormValues } from '../../lib/types';

interface AddTaskButtonProps {
  onAdd: (data: TaskFormValues) => void;
  loading?: boolean;
}

export default function AddTaskButton({ onAdd, loading = false }: AddTaskButtonProps) {
  const [showForm, setShowForm] = useState(false);

  const handleSubmit = (data: TaskFormValues) => {
    onAdd(data);
    setShowForm(false);
  };

  if (showForm) {
    return (
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="text-lg font-medium text-gray-900 mb-3">Add New Task</h3>
        <TaskForm
          onSubmit={handleSubmit}
          onCancel={() => setShowForm(false)}
          submitLabel="Create Task"
          cancelLabel="Cancel"
          loading={loading}
        />
      </div>
    );
  }

  return (
    <button
      onClick={() => setShowForm(true)}
      className="bg-[--color-primary] text-white px-4 py-2 rounded-md hover:bg-[--color-primary-dark]"
    >
      + Add Task
    </button>
  );
}