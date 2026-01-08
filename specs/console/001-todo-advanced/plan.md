# Implementation Plan: 001-todo-advanced

**Branch**: `001-todo-advanced` | **Date**: 2025-12-31 | **Spec**: [specs/001-todo-advanced/spec.md](../spec.md)

## Summary

This plan covers the implementation of the **Advanced Level (Intelligent Task Management)**. We will introduce an automation engine for recurring tasks, integrate precise time-based scheduling, and implement a proactive notification system within the CLI interface.

## Technical Context

- **Language/Version**: Python 3.13+
- **Primary Dependencies**: standard library (`datetime`, `threading`, `time`)
- **Storage**: In-memory (extension of current `Task` objects)
- **Notification Method**: Interactive CLI Alerts (top-of-menu and immenent-action warnings)
- **Design Pattern**: Command/Template pattern for recurrence (instances cloned from root settings).

## Constitution Check

- **Spec-Driven**: Maps to `001-todo-advanced/spec.md`.
- **Backward Compatibility**: Existing tasks (Basic/Intermediate) default to `recurrence=None`.
- **No Persistence**: Still strictly in-memory per project constraints.
- **Clean Code**: Modular implementation of Recurrence and Notification logic.

## Project Structure

```text
src/
├── models.py        # Updated Task with recurrence/time fields
├── todo_service.py  # Recurrence engine & rescheduling logic
├── cli.py           # Background alert thread & new menu items
└── main.py          # (No change)

specs/001-todo-advanced/
├── spec.md          # Approved specification
├── plan.md          # This file
├── checklists/
│   ├── requirements.md
│   └── architecture.md
└── tasks.md         # Next step
```

## Architecture Decisions

### 1. Recurring Task Intervals
**Decision**: Support `Daily`, `Weekly`, and `Monthly`.
**Rationale**: These cover 95% of routine user needs. More complex cron-like expressions are deferred to keep complexity low and CLI simple.
**Tradeoff**: No support for "every Tuesday/Thursday" yet; users can create multiple weekly tasks if needed.

### 2. Notification Method
**Decision**: CLI-based Alerts over browser/system notifications.
**Rationale**: True to the terminal-centric constitution. Native system notifications bring platform-specific dependencies (e.g. `plyer` or `win10toast`) which violates the "standard library only" constraint unless explicitly overridden.
**Execution**: A background thread in `cli.py` will monitor the task list and set a "global alert" flag visible during menu navigation.

### 3. Auto-Rescheduling Data Structure
**Decision**: Cloned Instances.
**Rationale**: When a recurring task is completed, it stays completed (for history). A *new* task with a new ID is generated for the next occurrence. The `root_id` will link the series together.

### 4. Error Handling for Time/Date
**Decision**: Strict validation with immediate re-prompt.
**Rationale**: Inconsistent date/time data breaks sorting and alert logic. Immediate correction ensures the in-memory state is always valid.

## Implementation Roadmap

1.  **Phase 1: Recurrence Core**:
    - Update `Task` model.
    - Implement `_clone_recurring_task(task_id)` in `TodoService`.
    - Modify `toggle_complete` to trigger cloning if recurrence exists.
2.  **Phase 2: Time & Alerts**:
    - Add `due_time` validation and storage.
    - Implement `check_notifications()` in `TodoService`.
    - Spawn a notification monitor thread in `cli.py`.
3.  **Phase 3: Rescheduling UI**:
    - Add "Overdue Reschedule" logic to `TodoService` (moving all to current date).
    - Update CLI menu with a dedicated "Intelligence" or "Advanced" sub-menu.

## Testing Strategy

- **Automation Tests**:
    - Verify `Monthly` tasks handle end-of-month correctly (Jan 31 -> Feb 28/29).
    - Verify priority/tags persist in cloned tasks.
    - Verify alert flag triggers exactly 1 minute before `due_time`.
- **Manual UX Validation**:
    - Set up 3 complex recurring tasks.
    - Verify "Batch Reschedule" clears the overdue segment correctly.
    - Test invalid time entry (e.g. 14:65).
