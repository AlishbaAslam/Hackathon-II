'use client';

import { useState, useRef, KeyboardEvent } from 'react';

interface TagInputProps {
  value?: string;
  onChange: (tags: string) => void;
  placeholder?: string;
}

export default function TagInput({ value = '', onChange, placeholder = 'Enter tags separated by commas...' }: TagInputProps) {
  const [inputValue, setInputValue] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  // Parse tags from the value string
  const tags = value ? value.split(',').map(tag => tag.trim()).filter(tag => tag) : [];

  // Add a new tag
  const addTag = (tag: string) => {
    if (tag.trim() && !tags.includes(tag.trim())) {
      const newTags = [...tags, tag.trim()];
      onChange(newTags.join(','));
      setInputValue('');
    }
  };

  // Remove a tag
  const removeTag = (tagToRemove: string) => {
    const newTags = tags.filter(tag => tag !== tagToRemove);
    onChange(newTags.join(','));
  };

  // Handle input key events
  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      addTag(inputValue);
    } else if (e.key === 'Backspace' && !inputValue && tags.length > 0) {
      // Remove last tag when backspacing on empty input
      const lastTag = tags[tags.length - 1];
      removeTag(lastTag);
    }
  };

  // Handle paste event to extract tags
  const handlePaste = (e: React.ClipboardEvent<HTMLInputElement>) => {
    e.preventDefault();
    const pastedText = e.clipboardData.getData('text');
    const newTags = pastedText.split(/[,;\s]+/).map(tag => tag.trim()).filter(tag => tag);

    const uniqueNewTags = newTags.filter(tag => !tags.includes(tag) && tag);
    if (uniqueNewTags.length > 0) {
      const allTags = [...tags, ...uniqueNewTags];
      onChange(allTags.join(','));
    }
  };

  return (
    <div className="relative">
      <div className="flex flex-wrap gap-2 p-2 bg-white/50 border border-[--border-light] rounded-lg min-h-[44px]">
        {tags.map((tag, index) => (
          <span
            key={index}
            className="inline-flex items-center gap-1 px-3 py-1 bg-[--color-primary]/20 text-[--color-primary] rounded-full text-sm"
          >
            {tag}
            <button
              type="button"
              onClick={() => removeTag(tag)}
              className="text-[--color-primary] hover:text-[--color-primary-dark] focus:outline-none"
              aria-label={`Remove ${tag} tag`}
            >
              ×
            </button>
          </span>
        ))}
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          onPaste={handlePaste}
          placeholder={tags.length === 0 ? placeholder : ''}
          className="flex-1 min-w-[120px] bg-transparent border-none focus:outline-none focus:ring-0 text-[--text-primary]"
        />
      </div>
      <div className="mt-1 text-xs text-[--text-secondary]">
        Press Enter, comma, or space to add tags. Click × to remove tags.
      </div>
    </div>
  );
}