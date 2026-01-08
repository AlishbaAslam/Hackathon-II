# Implementation Plan: Todo Console App - Phase I

**Branch**: `001-todo-cli` | **Date**: 2025-12-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/sp.specify` with one clarification resolved

## Summary

Build a clean, spec-driven, in-memory Todo console application in Python 3.13+ that implements five core CRUD features (add, view, update, delete, mark complete). The application uses a menu-driven CLI interface with in-memory task storage, following spec-driven development principles with Spec-Kit Plus.

## Technical Context

| Aspect | Value |
|--------|-------|
| **Language/Version** | Python 3.13+ |
| **Primary Dependencies** | Standard library only (no third-party) |
| **Storage** | In-memory (Python list/dictionary) |
| **Testing** | Manual validation only (Phase I scope) |
| **Target Platform** | Console/CLI (cross-platform) |
| **Project Type** | Single console application |
| **Performance Goals** | <2 seconds per interaction |
| **Constraints** | No files, no database, no external dependencies |
| **Scale/Scope** | Single user, single session |

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | ✅ PASS | All features from approved spec |
| II. Simplicity and Clarity | ✅ PASS | Beginner-friendly Python code |
| III. Correctness of Business Logic | ✅ PASS | Clear task lifecycle defined |
| IV. Maintainability | ✅ PASS | Modular structure planned |
| V. Deterministic Behavior | ✅ PASS | In-memory only, no side effects |
| PEP 8 Compliance | ✅ PASS | Enforced in code standards |
| Separation of Concerns | ✅ PASS | CLI, service, models separated |

## Key Design Decisions

### D1: Task Data Structure

| Option | Description | Trade-offs |
|--------|-------------|------------|
| **A. List of dictionaries** | `[{"id": 1, "title": "...", "completed": False}, ...]` | Simple, intuitive for beginners. O(n) lookup for ID operations. |
| **B. Dictionary by ID** | `{1: {"title": "...", "completed": False}, ...}` | O(1) lookup, slightly more complex structure. |
| **C. List of Task objects** | List of dataclass instances | Most Pythonic, type-safe, best for maintainability. |

**Selected**: Option C - List of Task objects (dataclass)

**Rationale**: Dataclasses provide type safety, auto-generated `__repr__`, and are idiomatic Python 3.7+. The O(n) lookup for ID-based operations is acceptable given the expected small number of tasks in Phase I. This approach prioritizes clarity and maintainability as per the constitution.

### D2: Unique ID Generation

| Option | Description | Trade-offs |
|--------|-------------|------------|
| **A. Auto-increment integer** | `next_id = len(tasks) + 1` or `max_id + 1` | Simple, predictable, matches spec requirement. Risk of ID reuse if tasks deleted. |
| **B. UUID4** | `uuid.uuid4()` | Unique, no collisions. Harder to read/remember, verbose. |
| **C. Monotonic counter** | Class-level counter with `@classmethod` | Clean, ensures uniqueness, recoverable state. |

**Selected**: Option A - Auto-increment integer

**Rationale**: Matches spec requirement (FR-009) for sequential integer IDs starting from 1. Simple and predictable for users. The potential ID reuse after deletion is acceptable for Phase I scope.

### D3: Console UI Design

| Option | Description | Trade-offs |
|--------|-------------|------------|
| **A. Menu-driven (numbered)** | "1. Add Task  2. View Tasks  3. ..." | Intuitive, low learning curve. Requires navigation steps. |
| **B. Command-based** | `add "task title"`, `view`, `done 1` | Power user friendly, faster once learned. Requires memorization. |
| **C. Hybrid** | Both menu and command support | Most flexible, higher implementation complexity. |

**Selected**: Option A - Menu-driven

**Rationale**: Simplicity and clarity are core principles. Menu-driven interface is beginner-friendly and matches the spec assumption of "numbered menu navigation (1-5)". This reduces cognitive load for hackathon judges and new developers.

### D4: Error Handling Strategy

| Option | Description | Trade-offs |
|--------|-------------|------------|
| **A. Re-prompt on invalid input** | Show error, ask again | Better UX, allows correction. Slightly more code. |
| **B. Default values** | Use sensible defaults | Quick, but may mask user intent. |
| **C. Abort operation** | Return to main menu | Simple, but frustrating UX. |

**Selected**: Option A - Re-prompt on invalid input

**Rationale**: Matches the clarification response. Better user experience allows correction of mistakes. Clear error messages help users understand what went wrong.

## Project Structure

### Documentation

```
specs/001-todo-cli/
├── spec.md              # Feature specification
├── plan.md              # This file
└── checklists/
    └── requirements.md  # Spec quality checklist
```

### Source Code

```
todo-console-app/
├── src/
│   ├── __init__.py
│   ├── models.py        # Task dataclass
│   ├── todo_service.py  # Business logic (CRUD operations)
│   ├── cli.py           # Console interface, menu handling
│   └── main.py          # Entry point
├── history/
│   ├── prompts/         # PHR records
│   └── adr/             # Architecture decision records
├── .specify/
│   ├── memory/
│   │   └── constitution.md
│   └── templates/
├── README.md
├── CLAUDE.md
└── pyproject.toml       # UV configuration
```

**Structure Decision**: Single project with clear module separation:
- `models.py` - Data layer (Task definition)
- `todo_service.py` - Business logic layer
- `cli.py` - Presentation layer (user interaction)
- `main.py` - Application entry point

## Module Breakdown

### models.py
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    """Represents a single todo task."""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
```

### todo_service.py
```python
from typing import List, Optional
from models import Task

class TodoService:
    """Manages task operations in memory."""

    def __init__(self) -> None:
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Create a new task with auto-generated ID."""

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks."""

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""

    def update_task(self, task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None) -> bool:
        """Update task title and/or description."""

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""

    def toggle_complete(self, task_id: int) -> bool:
        """Toggle task completion status."""
```

### cli.py
```python
from todo_service import TodoService

def display_menu() -> None:
    """Show main menu options."""

def get_menu_choice() -> int:
    """Get and validate menu choice."""

def get_task_input() -> tuple[str, str]:
    """Get task title and optional description."""

def get_task_id(prompt: str) -> int:
    """Get and validate task ID from user."""

def run_cli() -> None:
    """Main CLI loop."""
```

### main.py
```python
from cli import run_cli

if __name__ == "__main__":
    run_cli()
```

## CLI Interaction Flow

```
+-----------------------------------+
|      TODO CONSOLE APP v1.0        |
+-----------------------------------+
|                                   |
|  1. Add Task                      |
|  2. View Tasks                    |
|  3. Update Task                   |
|  4. Delete Task                   |
|  5. Mark Complete                 |
|  6. Exit                          |
|                                   |
|  Enter your choice (1-6): 1       |
|                                   |
+-----------------------------------+

Add Task
---------
Enter title: Buy groceries
Enter description (optional): Milk, eggs, bread
Task added successfully! (ID: 1)

[Returns to main menu]
```

## Data Model Design

### Task Entity

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `id` | int | > 0, unique | Auto-generated sequential ID |
| `title` | str | 1-255 chars, required | Task description |
| `description` | str or None | 0-1000 chars, optional | Additional details |
| `completed` | bool | default False | Completion status |

### In-Memory Storage

```python
# todo_service.py
class TodoService:
    def __init__(self) -> None:
        self._tasks: List[Task] = []  # Main task storage
        self._next_id: int = 1        # ID counter
```

## Feature Implementation Checklist

### F1: Add Task
- [ ] Validate non-empty title (re-prompt on empty)
- [ ] Accept optional description (empty string for no description)
- [ ] Create Task with auto-increment ID starting at 1
- [ ] Default completed status = False
- [ ] Return created Task object

### F2: View Task List
- [ ] Display header with column labels
- [ ] Show each task: ID, title, description (if present), status
- [ ] Format status as "[X]" for complete, "[ ]" for incomplete
- [ ] Handle empty list case with helpful message

### F3: Update Task
- [ ] Validate task ID exists
- [ ] Accept new title (optional - keep original if empty)
- [ ] Accept new description (optional - keep original if empty)
- [ ] Update only provided fields
- [ ] Show success/error message

### F4: Delete Task
- [ ] Validate task ID exists
- [ ] Remove task from list
- [ ] Show success/error message

### F5: Mark Complete
- [ ] Validate task ID exists
- [ ] Toggle completed status (complete ↔ incomplete)
- [ ] Show new status in message

## Validation Strategy

### Input Validation Rules

| Field | Rule | Error Message |
|-------|------|---------------|
| Menu choice | 1-6 integer | "Invalid choice. Please enter a number between 1 and 6." |
| Task title | 1-255 chars, not empty | "Title cannot be empty. Please try again." |
| Task ID | Positive integer, exists | "Task with ID X not found. Please enter a valid ID." |

### Error Handling Flow

```
User Input
    ↓
Validate
    ↓
[Valid] → Execute operation → Show success
    ↓
[Invalid] → Show error message → Re-prompt
```

## Testing Strategy (Manual Validation)

| Feature | Test Case | Expected Result |
|---------|-----------|-----------------|
| **Add Task** | Enter empty title | Error message, re-prompt |
| **Add Task** | Valid title only | Task created with ID |
| **Add Task** | Title + description | Task created with both fields |
| **View Tasks** | Empty list | "No tasks" message |
| **View Tasks** | Multiple tasks | All tasks displayed correctly |
| **Update Task** | Non-existent ID | Error message |
| **Update Task** | Valid ID, new title | Title updated, description preserved |
| **Delete Task** | Non-existent ID | Error message |
| **Delete Task** | Valid ID | Task removed from list |
| **Mark Complete** | Toggle twice | Status changes complete → incomplete |

## Deliverables

| File | Description |
|------|-------------|
| `src/main.py` | Entry point |
| `src/models.py` | Task dataclass |
| `src/todo_service.py` | Business logic |
| `src/cli.py` | Console interface |
| `README.md` | Setup and usage instructions |
| `CLAUDE.md` | Claude Code usage rules |
| `.specify/memory/constitution.md` | Project constitution |

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Implement features in order: models → service → CLI → main
3. Validate against success criteria (SC-001 through SC-005)
