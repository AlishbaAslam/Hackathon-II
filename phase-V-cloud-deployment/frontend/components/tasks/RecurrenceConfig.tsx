'use client';

import { useState } from 'react';

interface RecurrenceConfigProps {
  isRecurringValue: boolean;
  recurrencePatternValue: string;
  onToggleRecurring: (enabled: boolean) => void;
  onPatternChange: (pattern: string) => void;
}

export default function RecurrenceConfig({
  isRecurringValue = false,
  recurrencePatternValue = 'daily',
  onToggleRecurring,
  onPatternChange
}: RecurrenceConfigProps) {
  return (
    <div className="mb-4 p-4 border border-[--border-light] rounded-lg bg-white/20">
      <div className="flex items-center mb-3">
        <input
          type="checkbox"
          id="isRecurring"
          checked={isRecurringValue}
          onChange={(e) => onToggleRecurring(e.target.checked)}
          className="w-4 h-4 text-[--color-primary] bg-white border-[--border-light] rounded focus:ring-[--color-primary] focus:ring-2"
        />
        <label htmlFor="isRecurring" className="ml-2 text-sm font-medium text-[--text-secondary]">
          Recurring Task
        </label>
      </div>

      {isRecurringValue && (
        <div className="ml-6">
          <div>
            <label htmlFor="recurrencePattern" className="block text-sm font-medium text-[--text-secondary] mb-2">
              Recurrence Pattern
            </label>
            <select
              id="recurrencePattern"
              value={recurrencePatternValue}
              onChange={(e) => onPatternChange(e.target.value)}
              className="w-full px-4 py-3 bg-white/50 border border-[--border-light] rounded-lg focus:outline-none focus:ring-2 focus:ring-[--color-primary]/50 focus:border-[--color-primary] transition-all"
            >
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
              <option value="yearly">Yearly</option>
            </select>
          </div>
        </div>
      )}
    </div>
  );
}