---
id: 0007
title: recurring-task-auto-reschedule-fix
stage: red
date: 2025-12-31
surface: cli
model: Claude Sonnet 4.5
feature: 001-todo-advanced
branch: 001-todo-advanced
user: Claude
command: /sp.implement
labels: [bug-fix, recurring-tasks, auto-reschedule, overdue]
links:
  spec: specs/001-todo-advanced/spec.md
  ticket:
  adr:
  pr:
files:
  - src/todo_service.py
  - tests/unit/test_recurrence.py
tests:
  - tests/unit/test_recurrence.py::test_auto_clone_overdue_recurring
  - tests/unit/test_recurrence.py::test_recurrence_cloning
  - tests/unit/test_alerts.py::test_get_upcoming_alerts
---

## Prompt

Issue: Recurring tasks are NOT auto-rescheduled unless marked complete.

Root Cause:
- Recurrence cloning is only triggered in `toggle_complete`
- Overdue recurring tasks remain static unless manually completed or batch-rescheduled

Fix (Required Changes):
1. Auto-clone recurring tasks when they become overdue
   - On app startup OR before rendering task list:
     - Detect overdue + recurring + not completed
     - Clone next occurrence
     - Mark old instance as archived (not completed)

2. Update `reschedule_overdue_tasks()` logic:
   - IF task is recurring → clone forward using recurrence rule
   - ELSE → move due_date to today
   - Never modify original recurrence chain incorrectly

3. Guardrails:
   - Prevent duplicate clones using `root_id`
   - Clone only once per overdue cycle

Acceptance Criteria:
- Daily task auto-creates next instance when time passes
- No manual "Mark Complete" required for recurrence
- Batch reschedule does NOT break recurring series

## Response snapshot

Successfully implemented the fix for recurring tasks not auto-rescheduling when overdue:

## Changes Made:

1. **Added `_check_overdue_recurring_tasks()` method** in `src/todo_service.py`:
   - Automatically detects overdue recurring tasks
   - Clones next occurrence using recurrence rules
   - Prevents duplicate clones using root_id tracking
   - Called from all task-returning methods (get_all_tasks, get_upcoming_alerts, filter_tasks, sort_tasks, search_tasks)

2. **Updated `reschedule_overdue_tasks()` method**:
   - For recurring tasks: Creates next occurrence instead of moving original date
   - For non-recurring tasks: Moves due date to new date (unchanged behavior)
   - Added `_clone_recurring_task_directly()` helper to avoid completion status changes

3. **Updated all task-returning methods** to call auto-check:
   - `get_all_tasks()`, `get_upcoming_alerts()`, `filter_tasks()`, `sort_tasks()`, `search_tasks()`
   - Ensures overdue recurring tasks are properly cloned when users view any task list

4. **Enhanced testing** in `tests/unit/test_recurrence.py`:
   - Updated existing test to use future dates to avoid auto-cloning interference
   - Added new test `test_auto_clone_overdue_recurring()` to verify new functionality

## Key Features:
- Recurring tasks now auto-clone when they become overdue (no manual completion needed)
- Batch rescheduling properly handles recurring tasks by creating next occurrences
- Duplicate prevention ensures only one next occurrence per series
- All existing functionality preserved
- New functionality thoroughly tested

## Outcome

- ✅ Impact: Recurring tasks now auto-create next instance when overdue without manual completion
- 🧪 Tests: All tests pass including new auto-cloning test
- 📁 Files: Updated todo_service.py with new functionality, updated tests
- 🔁 Next prompts: Ready for user validation and potential new feature requests
- 🧠 Reflection: Implementation properly addresses the core issue while maintaining backward compatibility

## Evaluation notes (flywheel)

- Failure modes observed: None - all functionality working as expected
- Graders run and results (PASS/FAIL): PASS - all tests pass and functionality works correctly
- Prompt variant (if applicable): Bug fix implementation prompt
- Next experiment (smallest change to try): User validation of the new auto-cloning behavior
