'use client';

import { useState } from 'react';

interface DateTimePickersProps {
  dueDateValue?: string;
  reminderTimeValue?: string;
  onDueDateChange: (date: string) => void;
  onReminderTimeChange: (time: string) => void;
}

export default function DateTimePickers({
  dueDateValue = '',
  reminderTimeValue = '',
  onDueDateChange,
  onReminderTimeChange
}: DateTimePickersProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label htmlFor="dueDate" className="block text-sm font-medium text-[--text-secondary] mb-2">
          Due Date
        </label>
        <input
          type="datetime-local"
          id="dueDate"
          value={dueDateValue}
          onChange={(e) => onDueDateChange(e.target.value)}
          className="w-full px-4 py-3 bg-white/50 border border-[--border-light] rounded-lg focus:outline-none focus:ring-2 focus:ring-[--color-primary]/50 focus:border-[--color-primary] transition-all"
        />
      </div>

      <div>
        <label htmlFor="reminderTime" className="block text-sm font-medium text-[--text-secondary] mb-2">
          Reminder Time
        </label>
        <input
          type="datetime-local"
          id="reminderTime"
          value={reminderTimeValue}
          onChange={(e) => onReminderTimeChange(e.target.value)}
          className="w-full px-4 py-3 bg-white/50 border border-[--border-light] rounded-lg focus:outline-none focus:ring-2 focus:ring-[--color-primary]/50 focus:border-[--color-primary] transition-all"
        />
      </div>
    </div>
  );
}