'use client';

import { Task, TaskFormValues } from '../../lib/types';
import TaskForm from './TaskForm';
import { Fragment } from 'react';
import { Dialog, Transition } from '@headlessui/react';

interface EditTaskModalProps {
  task: Task;
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (taskId: string, data: TaskFormValues) => void;
  loading?: boolean;
}

export default function EditTaskModal({
  task,
  isOpen,
  onClose,
  onSubmit,
  loading = false
}: EditTaskModalProps) {
  const handleSubmit = (data: TaskFormValues) => {
    onSubmit(task.id, data);
  };

  return (
    <Transition show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-10" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black bg-opacity-25" />
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
              <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all glass border border-white/20">
                <Dialog.Title
                  as="h3"
                  className="text-lg font-medium leading-6 text-[--text-primary]"
                >
                  Edit Task
                </Dialog.Title>
                <div className="mt-2">
                  <TaskForm
                    initialData={{
                      title: task.title,
                      description: task.description || ''
                    }}
                    onSubmit={handleSubmit}
                    onCancel={onClose}
                    submitLabel="Update Task"
                    loading={loading}
                  />
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
}