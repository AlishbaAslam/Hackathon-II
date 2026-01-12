# CLAUDE.md - Console Todo App

This file provides guidance for Claude Code when working with the console-based todo application project.

## Project Overview

This is a Python console application that implements a comprehensive todo list manager. The application provides a command-line interface for managing tasks with features like due dates, priorities, completion status, and search functionality.

## Current Implementation Status

The todo app currently supports the following features:
- **Task Management**: Create, read, update, and delete tasks
- **Task Properties**: Title, description, due date, priority levels (high/medium/low), completion status
- **Task Search**: Find tasks by title or description
- **Task Filtering**: View pending vs completed tasks
- **Recurring Tasks**: Support for recurring tasks with different patterns
- **Time Display**: AM/PM time format display
- **Batch Operations**: Multiple tasks can be processed together
- **Auto-rescheduling**: Incomplete overdue tasks can be automatically rescheduled

## Development Workflow

1. **Specification & Planning** (`/sp.specify`, `/sp.plan`, `/sp.tasks`)
   - Follow the existing spec-driven approach
   - Specifications are in `specs/001-todo-cli/spec.md`
   - Implementation plan in `specs/001-todo-cli/plan.md`
   - Tasks breakdown in `specs/001-todo-cli/tasks.md`

2. **Implementation** (`/sp.implement`)
   - All code is located in the `src/` directory
   - Follow the existing architecture (models, service, CLI separation)

## Code Architecture

### Module Organization

```
src/
├── models.py        # Data classes (Task, Priority, RecurrencePattern)
├── todo_service.py  # Business logic (CRUD operations, task management)
├── cli.py           # Console interface (menu, input handling, display)
└── main.py          # Entry point
```

### Key Classes and Functions

- **models.py**: Contains `Task` dataclass with all task properties
- **todo_service.py**: Core business logic including task storage and operations
- **cli.py**: Handles user interaction, menu display, and input processing
- **main.py**: Application entry point

## Code Standards

### Python Conventions
- **PEP 8** compliance required
- Type hints for all function signatures
- Use dataclasses for data models
- Clear, descriptive variable and function names

### Console Application Specifics
- **User Experience**: Provide clear prompts and error messages
- **Input Validation**: Validate all user inputs and provide helpful feedback
- **Menu Navigation**: Maintain intuitive menu flow with clear options
- **Display Format**: Use consistent formatting for task lists and details

## Key Features to Maintain

1. **Task Management**:
   - Add tasks with title, description, due date, priority
   - Mark tasks as complete/incomplete
   - Edit existing tasks
   - Delete tasks

2. **Search & Filter**:
   - Search tasks by title or description
   - Filter by completion status
   - Filter by priority level

3. **Advanced Features**:
   - Recurring tasks with different patterns
   - Due date management and overdue tracking
   - Batch operations on multiple tasks
   - AM/PM time display

## Technical Constraints

- Python 3.13+ only
- In-memory storage (no files, no database)
- UV-managed virtual environment
- No third-party runtime dependencies
- Console-based interface only

## Development Guidelines

### Adding New Features
- Follow the existing MVC-like separation (models, service, CLI)
- Maintain consistency with existing UI patterns
- Ensure new features work with existing search/filter functionality
- Test integration with recurring task system if applicable

### Error Handling
- Provide user-friendly error messages
- Handle invalid date formats gracefully
- Validate priority levels and other enum values
- Maintain application stability during error conditions

### User Interface Consistency
- Keep menu options consistent with existing patterns
- Use similar prompt formats throughout the application
- Maintain readable output formatting for task lists
- Follow existing input validation patterns

## Success Criteria

- New features integrate seamlessly with existing functionality
- Console interface remains intuitive and user-friendly
- All existing features continue to work correctly
- Code maintains separation of concerns
- Error handling is robust and user-friendly