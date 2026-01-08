# Frontend Development Skill for Full-Stack Todo App

## Overview
A reusable skill for developing the Next.js 16 frontend of the Hackathon II Phase 2 Full-Stack Todo App with TypeScript and Tailwind CSS. This skill enables modular, spec-driven frontend development aligned with the monorepo structure.

## Metadata
- **Skill Name**: frontend-dev
- **Category**: frontend
- **Domain**: Next.js 16, TypeScript, Tailwind CSS
- **Integration**: Spec-Driven Development (SDD) workflow
- **Agents**: Spec Architect, UI Agent, API Communication Agent

## Purpose
Enable consistent, modular, and spec-compliant frontend development for the full-stack todo application. This skill provides a standardized approach for creating UI components, integrating with backend APIs, and maintaining alignment with specifications.

## Prerequisites
- Node.js 18+ and npm/yarn/pnpm
- Next.js 16 project structure in `/frontend` directory
- TypeScript configuration
- Tailwind CSS configured
- Spec files in `/specs` directory
- API endpoints defined in backend specs

## Core Capabilities

### 1. Component Development
- Create Next.js 16 components with TypeScript
- Implement responsive UI with Tailwind CSS
- Follow component hierarchy patterns
- Ensure accessibility compliance
- Implement proper state management patterns

### 2. Spec Integration
- Generate UI components based on spec requirements
- Validate component implementations against specs
- Update component documentation to match specs
- Create mock data aligned with API specs

### 3. API Integration
- Connect frontend components to backend REST APIs
- Handle JWT authentication tokens
- Implement proper error handling and loading states
- Create API service layer for clean separation

### 4. Styling & UX
- Apply Tailwind CSS utility classes
- Maintain consistent design system
- Implement responsive layouts
- Ensure cross-browser compatibility

## Usage Patterns

### Pattern 1: Component Creation from Spec
```
1. Read spec requirements from `/specs/.../feature.spec.md`
2. Identify UI components needed for the feature
3. Create component files in `/frontend/src/components`
4. Implement TypeScript interfaces based on spec
5. Apply Tailwind CSS classes for styling
6. Add unit tests for components
7. Update documentation
```

### Pattern 2: API Integration
```
1. Review API endpoint specs in `/specs/api/...`
2. Create API service functions in `/frontend/src/services`
3. Implement authentication token handling
4. Create custom hooks for API calls
5. Add error handling and loading states
6. Test API integration
```

### Pattern 3: Feature Implementation
```
1. Parse feature requirements from spec
2. Identify required UI components
3. Plan component hierarchy
4. Create TypeScript types/models
5. Implement components with Tailwind CSS
6. Integrate with backend APIs
7. Add responsive design
8. Validate against original spec
```

## File Structure Conventions

### Component Structure
```
/frontend/src/components/
├── [FeatureName]/
│   ├── [ComponentName].tsx
│   ├── [ComponentName].test.tsx
│   └── index.ts
├── [FeatureName]/types.ts
└── [FeatureName]/hooks.ts
```

### Page Structure
```
/frontend/src/app/
├── [page]/
│   ├── page.tsx
│   ├── layout.tsx
│   └── loading.tsx
└── globals.css
```

### Service Structure
```
/frontend/src/services/
├── api.ts
├── auth.ts
├── [feature].ts
└── types.ts
```

## Implementation Guidelines

### TypeScript Best Practices
- Use TypeScript interfaces for all props and data models
- Implement proper type safety for API responses
- Use generics when appropriate
- Leverage TypeScript utility types

### Tailwind CSS Guidelines
- Use consistent color palette defined in `tailwind.config.js`
- Apply responsive design with Tailwind breakpoints
- Use utility classes for styling (avoid custom CSS when possible)
- Implement dark mode support where applicable

### Component Architecture
- Create reusable, composable components
- Implement proper prop drilling vs context patterns
- Use Next.js 16 features (App Router, Server Components)
- Follow React best practices (hooks, memoization)

### State Management
- Use React hooks for local component state
- Implement Context API for shared state when needed
- Consider external state management libraries only when necessary
- Implement proper error and loading states

## Quality Assurance

### Code Quality
- Follow Next.js best practices
- Maintain consistent code style
- Use TypeScript for type safety
- Implement proper error boundaries

### Testing
- Write unit tests for components
- Implement integration tests for API interactions
- Use testing library for React component testing
- Include accessibility tests

### Performance
- Implement code splitting where appropriate
- Optimize component rendering
- Use proper image optimization
- Implement proper caching strategies

## Integration Points

### With Spec Architect Agent
- Read feature specifications from `/specs/`
- Generate component requirements from specs
- Validate implementations against specs
- Update documentation based on spec changes

### With UI Agent
- Create UI components based on design requirements
- Implement responsive layouts
- Apply styling with Tailwind CSS
- Ensure accessibility compliance

### With API Communication Agent
- Integrate with backend REST APIs
- Handle JWT authentication
- Implement proper error handling
- Create API service layer

## Error Handling
- Implement proper error boundaries for components
- Handle API errors gracefully
- Provide user-friendly error messages
- Log errors appropriately for debugging

## Security Considerations
- Properly handle JWT tokens in frontend
- Implement CSRF protection where needed
- Sanitize user inputs in forms
- Follow Next.js security best practices

## Validation Checklist
- [ ] Components match spec requirements
- [ ] TypeScript types are properly defined
- [ ] Tailwind CSS is consistently applied
- [ ] API integration works correctly
- [ ] Responsive design is implemented
- [ ] Accessibility standards are met
- [ ] Tests pass successfully
- [ ] Code follows established patterns

## Examples

### Example Component Implementation
```tsx
// /frontend/src/components/TodoItem/TodoItem.tsx
import { useState } from 'react';
import { Todo } from '@/types/todo';

interface TodoItemProps {
  todo: Todo;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}

export const TodoItem = ({ todo, onToggle, onDelete }: TodoItemProps) => {
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await onDelete(todo.id);
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div className="flex items-center justify-between p-4 border rounded-lg shadow-sm">
      <div className="flex items-center">
        <input
          type="checkbox"
          checked={todo.completed}
          onChange={() => onToggle(todo.id)}
          className="h-4 w-4 text-blue-600 rounded"
        />
        <span className={`ml-3 ${todo.completed ? 'line-through text-gray-500' : ''}`}>
          {todo.title}
        </span>
      </div>
      <button
        onClick={handleDelete}
        disabled={isDeleting}
        className={`px-3 py-1 rounded ${
          isDeleting
            ? 'bg-gray-300 cursor-not-allowed'
            : 'bg-red-500 hover:bg-red-600 text-white'
        }`}
      >
        {isDeleting ? 'Deleting...' : 'Delete'}
      </button>
    </div>
  );
};
```

### Example API Integration
```tsx
// /frontend/src/services/todo.ts
import { Todo } from '@/types/todo';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || '/api';

interface ApiOptions {
  token?: string;
}

export const todoService = {
  async getAll(userId: string, options: ApiOptions = {}) {
    const response = await fetch(`${API_BASE}/${userId}/todos`, {
      headers: {
        'Authorization': `Bearer ${options.token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch todos');
    }

    return response.json() as Promise<Todo[]>;
  },

  async create(userId: string, todo: Omit<Todo, 'id'>, options: ApiOptions = {}) {
    const response = await fetch(`${API_BASE}/${userId}/todos`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${options.token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(todo),
    });

    if (!response.ok) {
      throw new Error('Failed to create todo');
    }

    return response.json() as Promise<Todo>;
  }
};
```

## Success Criteria
- Components implement all spec requirements
- TypeScript compilation succeeds without errors
- UI is responsive and accessible
- API integration works correctly
- Tests pass successfully
- Code follows established patterns and conventions
- Performance meets standards
- Security considerations are addressed