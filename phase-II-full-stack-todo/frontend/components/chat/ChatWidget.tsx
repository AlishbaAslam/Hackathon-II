'use client';

import React, { useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import ChatInterface from './ChatInterface';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const { user } = useAuth();

  // Only show chat widget if user is authenticated
  if (!user) {
    return null;
  }

  return (
    <>
      {/* Floating chat button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 bg-indigo-600 text-white p-4 rounded-full shadow-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 z-50 transition-all duration-300 transform hover:scale-105"
          aria-label="Open chat"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </button>
      )}

      {/* Chat interface when open */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 w-full max-w-sm h-[80vh] bg-white rounded-lg shadow-xl border border-gray-200 flex flex-col z-50 transition-all duration-300">
          <div className="flex justify-between items-center p-4 border-b border-gray-200 bg-indigo-600 text-white rounded-t-lg">
            <h3 className="font-semibold">AI Task Assistant</h3>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:text-gray-200 focus:outline-none"
              aria-label="Close chat"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
          <div className="flex-grow overflow-hidden">
            <ChatInterface onClose={() => setIsOpen(false)} />
          </div>
        </div>
      )}
    </>
  );
};

export default ChatWidget;