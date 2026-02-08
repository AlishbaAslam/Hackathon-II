'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error(error);
  }, [error]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8 text-center">
        <div>
          <h1 className="text-9xl font-bold text-gray-400">500</h1>
          <h2 className="mt-4 text-2xl font-bold text-gray-900">Something went wrong!</h2>
          <p className="mt-2 text-gray-600">
            An unexpected error occurred. Please try again.
          </p>
        </div>
        <div className="mt-6">
          <button
            onClick={() => reset()}
            className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
          >
            Try again
          </button>
        </div>
      </div>
    </div>
  );
}